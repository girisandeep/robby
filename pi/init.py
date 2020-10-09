# Write your code here :-)
from gpiozero import Robot
robby = Robot(left=(7,8),right=(10, 9))
l = robby.left
r = robby.right
f = robby.forward
b = robby.backward
s = robby.stop