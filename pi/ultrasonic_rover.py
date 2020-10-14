#Libraries
import RPi.GPIO as GPIO
import time
import random
from bluedot import BlueDot
from gpiozero import Robot
from signal import pause

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 22
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
 
def distance():
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
    distance = (TimeElapsed * 34300) / 2
 
    return distance

def start_ultrsonic_rover(robot):
    while True:
        dist = distance()
        print("Distance: ", dist)
        if dist < 10 or dist > 2000:
            print("Too Close. Reverse")
            robot.backward()
        elif dist < 100:
            print("Noticed nearby obstruction")
            ch = random.choice(range(1))
            if ch == 0:
                print("Taking left")
                robot.left()
            else:
                print("Taking right")
                robot.right()
        else:
            robot.forward(0.5)
            print("Moving forward")
        time.sleep(1)
        robot.stop()

def start_bluetooth(robot):
    bd = BlueDot()

    def move_b(pos):
        print("Move!")
        if pos.top:
            print("forward()")
            robot.forward()
        elif pos.bottom:
            print("bottom")
            robot.backward()
        elif pos.left:
            print("left")
            robot.left()
        elif pos.right:
            print("right")
            robot.right()

    def stop_b():
        robot.stop()

    print("Started!")
    bd.when_pressed = move_b
    bd.when_moved = move_b
    bd.when_released = stop_b
    pause()

if __name__ == '__main__':
    try:
        robot = Robot(left=(9, 10), right=(7, 8))
        # start_bluetooth(robot)
        start_ultrsonic_rover(robot)

    except KeyboardInterrupt as e:
        print("Measurement stopped by User")
        GPIO.cleanup()
