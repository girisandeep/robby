import tensorflow as tf


##---- Ultra Sonic ----
import RPi.GPIO as GPIO

class UltraSonic():
    def __init__(self):
        #GPIO Mode (BOARD / BCM)
        GPIO.setmode(GPIO.BCM)
         
        #set GPIO Pins
        GPIO_TRIGGER = 18
        GPIO_ECHO = 22
         
        #set GPIO direction (IN / OUT)
        GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(GPIO_ECHO, GPIO.IN)
    
    def get_distance(self):
        try:
            dist = self._distance()
            return dist
        # Reset by pressing CTRL + C
        except KeyboardInterrupt:
            print("Measurement stopped by User")
            GPIO.cleanup()
    def cleaup(self):
        GPIO.cleanup()

    def _distance():
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
from enum import IntEnum
class Move(IntEnum):
    STOP = 0
    FORWARD = 1
    LEFT = 2
    RIGHT = 3
    BACKWARD = 4

robot_move_fns = [robot.stop, robot.forward, robot.left, robot.right, robot.backward]


## -- ENV:Take and SavePicture ---
from picamera import PiCamera
import time
import numpy as np
import os
from PIL import Image

from signal import pause
class EnvResetBlue():
    def __init__(self, env):
        self.env = env
        self.bd = BlueDot()

    def start(self)
        self.bd.when_released = self.mark_user_ack
        self.env.state_changed = self.change_color
        pause

    def _mark_user_ack(self):
        self.env.user_ack = True
    def _change_color(self):
        if self.end.done == True:
            self.bd.color = (255, 0, 0)
            self.bd.border = True
        else:
            self.bd.color = (0, 0, 255)
            self.bd.border = False

class PersistCam():
    def __init__(self, folder="data"):
        self.camera = PiCamera()
        if not os.isdir(folder):
            os.mkdir(folder)
    def capture(self):
        output = np.empty((720, 1280, 3), dtype=np.uint8)
        self.camera.capture(output, 'rgb')

        im = Image.fromarray(output)
        filename = datetime.datetime.today().strftime('%Y-%m-%d_%H-%M-%S-%M-%f.jpeg')
        filepath = folder + "/" + filename
        im.save(filepath)
        return (output, filepath, filename)

    def close():
        self.camera.close()

class Env():
    def __init__(self):
        self.ultrasonic = UltraSonic()
        self.cam = PersistCam()
        self.done = False
        self.user_ack = False
        self.state_changed = None

    def _is_safe(self):
        dist = self.ultrasonic.get_distance()
        if dist < 15:
            return False
        else:
            return True

    def reset(self):

        while self.done and not self.user_ack:
            time.sleep(1)
            print("Waiting for user ack on BlueDot")
        
        self.user_ack = False
        return self._observe()

    def _update_state(self, done):
        self.done = done
        if self.state_changed:
            self.state_changed()

    def _observe(self):
        self.obs = self.cam.capture()
        if self._is_safe():
            reward = 0
            self._update_state(1)
        else:
            reward = 1
            self._update_state(0)
        
        return (self.obs, reward, self.done, {})

    def step(self, move):
        if done:
            return (self.obs, 0, self.done, {})
        if move == Move.FORWARD and not self._is_safe():
            self._update_state(1)
            return (self.obs, 0, self.done, {})
        self._step_robot(move)
        return self._observe()

    def _step_robot(self, move):
        robot_move_fns[move]()
        time.sleep(0.2)
        robot_move_fns[Move.STOP]()

from random import choice
def random_policy(obs):
    return choice(list(Move)[1:])

policy = random_policy

env = Env()

for game_plays in range(100):
    print("Game Play: ", gameplay)
    
    obs, reward, done, info = env.reset() #It will wait for user ack

    while done != 0:
        
        mv = policy(current_pic)

        obs, reward, done, info = env.step(mv)
