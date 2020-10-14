#import tensorflow as tf

##---- Ultra Sonic ----
from bluedot import BlueDot
from datetime import datetime
from enum import IntEnum
from gpiozero import Robot
from picamera import PiCamera
from PIL import Image
from random import choice
from signal import pause
from signal import pause
import numpy as np
import os
import RPi.GPIO as GPIO
import threading
import time

#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 22

class UltraSonic():
    def __init__(self):
        #GPIO Mode (BOARD / BCM)
        GPIO.setmode(GPIO.BCM)
         
         
        #set GPIO direction (IN / OUT)
        GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(GPIO_ECHO, GPIO.IN)
    
    def get_distance(self):
        try:
            dist = self._distance()
            print("UltraSonic - get_distance: ", dist)
            return dist
        # Reset by pressing CTRL + C
        except KeyboardInterrupt:
            print("Measurement stopped by User")
            GPIO.cleanup()
    def cleaup(self):
        GPIO.cleanup()

    def _distance(self):
        # set Trigger to HIGH
        GPIO.output(GPIO_TRIGGER, True)
     
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER, False)
     
        StartTime = time.time()
        StopTime = time.time()
     
        # save StartTime
        while GPIO.input(GPIO_ECHO) == 0:
            StartTime = time.time()
        
        # save time of arrival
        while GPIO.input(GPIO_ECHO) == 1:
            StopTime = time.time()
     
        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        d = (TimeElapsed * 34300) / 2
     
        return d

##-------Robot--------
# Initiate Robot

robot = Robot(left=(9, 10), right=(7, 8))

class Move(IntEnum):
    STOP = 0
    FORWARD = 1
    LEFT = 2
    RIGHT = 3
    BACKWARD = 4

robot_move_fns = [robot.stop, robot.forward, robot.left, robot.right, robot.backward]


## -- ENV:Take and SavePicture ---
class EnvResetBlue():
    def __init__(self, env):
        self.env = env

    def start(self):
        self.bd = BlueDot()
        self.bd.when_released = self._mark_user_ack
        self.env.state_changed = self._change_color
        print("BlueDot Started")
        pause

    def _mark_user_ack(self):
        self.env.user_ack = True
    def _change_color(self):
        if self.env.done == True:
            self.bd.color = (255, 0, 0)
            self.bd.border = True
        else:
            self.bd.color = (0, 0, 255)
            self.bd.border = False

class PersistCam():
    def __init__(self, folder="deep_rover_data_images"):
        self.folder = folder
        self.camera = PiCamera()
        if not os.path.isdir(folder):
            os.mkdir(folder)
    def capture(self):
        print("Saving a pic.")
        output = np.empty((720, 1280, 3), dtype=np.uint8)
        self.camera.capture(output, 'rgb')

        im = Image.fromarray(output)
        filename = datetime.today().strftime('%Y-%m-%d_%H-%M-%S-%M-%f.jpeg')
        filepath = self.folder + "/" + filename
        im.save(filepath)
        return (output, filepath, filename)

    def close():
        self.camera.close()

class SessionObserver():
    def __init__(self, folder="deep_rover_data_sessions"):
        if not os.path.isdir(folder):
            os.mkdir(folder)
        filename = datetime.today().strftime('%Y-%m-%d_%H-%M-%S-%M-%f.csv')
        self.filehandle = open(folder + "/" + filename, "w+")
    def write(self, prev_img_loc, move, new_img_location, reward, done, info):
        self.filehandle.write("%s, %s, %s, %s, %s, %s " % (prev_img_loc, move, new_img_location, reward, done, info))
    def close(self):
        self.filehandle.close()

class Env():
    def __init__(self):
        self.ultrasonic = UltraSonic()
        self.cam = PersistCam()
        self.done = False
        self.user_ack = False
        self.state_changed = None
        self.sessionObserver = SessionObserver()

    def _is_safe(self):
        dist = self.ultrasonic.get_distance()
        if dist < 15:
            return False
        else:
            return True

    def reset(self):
        print("RESET: Self.done: ", self.done)
        if self.done:
            print("Waiting for user ack on BlueDot")
            while not self.user_ack:
                time.sleep(1)
            print("Recieved ACK")
            self.user_ack = False
            self._update_done(False)
        return self._observe()

    def _update_done(self, done):
        self.done = done
        if self.state_changed:
            self.state_changed()

    def _observe(self):
        self.obs = self.cam.capture()
        if not self._is_safe():
            reward = 0
            self._update_done(True)
        else:
            reward = 1
            self._update_done(False)
        
        return (self.obs, reward, self.done, {})

    def step(self, move):
        if self.done:
            return (self.obs, 0, self.done, {})
        if move == Move.FORWARD and not self._is_safe():
            self._update_done(True)
            return (self.obs, 0, self.done, {})
        prev_image = self.obs[1]
        self._step_robot(move)
        result = self._observe()
        self.sessionObserver.write(prev_image, int(move), result[0][1], result[1], result[2], result[3])
        return result

    def _step_robot(self, move):
        robot_move_fns[move]()
        time.sleep(0.2)
        robot_move_fns[Move.STOP]()

def random_policy(obs):
    return choice(list(Move)[1:])

policy = random_policy
env = Env()
print("Env created.")

user_ack_bd = EnvResetBlue(env)
t = threading.Thread(target=user_ack_bd.start)
t.start()

for game_play in range(100):
    print("Game Play: ", game_play)
    
    obs, reward, done, info = env.reset() #It will wait for user ack

    while done == 0:
        mv = policy(obs[0])
        obs, reward, done, info = env.step(mv)
        time.sleep(0.1)