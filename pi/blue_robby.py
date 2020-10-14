from bluedot import BlueDot
from gpiozero import Robot
from signal import pause

#cameradb = BlueDot(port=1)
bd = BlueDot()
robot = Robot(left=(9, 10), right=(7, 8))

def move(pos):
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

def stop():
    robot.stop()

print("Started!")
bd.when_pressed = move
bd.when_moved = move
bd.when_released = stop

pause()
