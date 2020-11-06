from bluedot import BlueDot
from gpiozero import Motor
from signal import pause
from mecanum import MnCart
from time import sleep
import math

# bd = BlueDot(cols=2, rows=2)

# fr = Motor(23, 22)
# fl = Motor(24, 25)
# rl = Motor(10, 9)
# rr = Motor(7, 8)


# motors = [[fl, fr],[rl, rr]]

# def move(pos):
#     print("button {}.{} pressed, Top:{}, Bottom:{}".format(pos.col, pos.row, pos.top, pos.bottom))
#     m = motors[pos.row][pos.col]
#     if pos.bottom:
#         m.backward()
#     else:
#         m.forward()

# def stop(pos):
#     print("button {}.{} released, Top:{}, Bottom:{}".format(pos.col, pos.row, pos.top, pos.bottom))
#     m = motors[pos.row][pos.col]
#     m.stop()

# bd.when_pressed = move
# bd.when_released = stop
# pause()

mc = MnCart((24, 25), (23, 22), (10, 9), (7, 8))

moves = [mc.backward, mc.backleft, mc.leftslide, mc.forwardleft, mc.forward, mc.forwardright, mc.rightslide, mc.backright, mc.backward]


def swiped(swipe):
    print("Swiped")
    print("speed={}".format(swipe.speed))
    print("angle={}".format(swipe.angle))
    print("distance={}".format(swipe.distance))
    moves[round(swipe.angle/45.0)+4]()
    sleep(swipe.distance/2)
    mc.stop()

count = 0
def rotated(rotation):
    global count
    count += rotation.value
    print("{} {} {}".format(count,
                            rotation.clockwise,
                            rotation.anti_clockwise))
    if rotation.clockwise:
        mc.turn_cw()
    else:
        mc.turn_ccw()

def calculate_angle(x, y):
    angle = math.atan(abs(y/x))*180/math.pi
    print("Actual Angle: ", angle)
    if x >= 0:
        if y>= 0:
            angle = angle
        else:
            angle = 360 - angle
    else:
        if y>= 0:
            angle = 180 - angle
        else:
            angle = 180 + angle
    return angle

moves_xy = [mc.rightslide, mc.forwardright, mc.forward, mc.forwardleft, mc.leftslide, mc.backleft, mc.backward, mc.backright, mc.rightslide]
def moved(pos):
    print("x, y: {}, {} ".format(pos.x, pos.y))
    angle = calculate_angle(pos.x, pos.y)
    print("angle: ", angle)
    moves_xy[round(angle/45.0)]()

bd = BlueDot(rows=2)
# bd.when_swiped = swiped
bd[0,1].when_rotated = rotated
bd[0,0].when_moved = moved
bd[0,0].when_released = mc.stop

pause()
