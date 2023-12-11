#!/usr/bin/env python3

from time import sleep

from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.led import Leds

from pixycamev3.pixy2 import Pixy2

pixy2 = Pixy2(port=2, i2c_address=0x54)

pixy2.set_lamp(1, 0)
sleep(0.5)
pixy2.set_lamp(0, 0)

resolution = pixy2.get_resolution()
WIDTH = resolution.width
HEIGHT = resolution.height

print('Frame width:  ', resolution.width)
print('Frame height: ', resolution.height)

while True :
    nbr , target = pixy2.get_blocks(1,1)
    if nbr == 1 : 
        sig = blocks[0].sig
        x = blocks[0].x_center
        y = blocks[0].y_center
        w = blocks[0].width
        h = blocks[0].height

        print(sig, x, y , w, h)

    sleep(10)
