from bluedot import BlueDot
from gpiozero import Motor
from signal import pause

bd = BlueDot(cols=2, rows=2)

fr = Motor(23, 22)
fl = Motor(24, 25)
rl = Motor(10, 9)
rr = Motor(7, 8)


motors = [[fl, fr],[rl, rr]]

def move(pos):
    print("button {}.{} pressed, Top:{}, Bottom:{}".format(pos.col, pos.row, pos.top, pos.bottom))
    m = motors[pos.row][pos.col]
    if pos.bottom:
        m.backward()
    else:
        m.forward()

def stop(pos):
    print("button {}.{} released, Top:{}, Bottom:{}".format(pos.col, pos.row, pos.top, pos.bottom))
    m = motors[pos.row][pos.col]
    m.stop()

bd.when_pressed = move
bd.when_released = stop
pause()

