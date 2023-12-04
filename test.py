#!/usr/bin/env python3

from time import sleep

from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.led import Leds

from pixycamev3.pixy2 import Pixy2

pixy2 = Pixy2(port=2, i2c_address=0x54)

pixy2.set_lamp(1, 0)

while True :
    a = pixy2.get_blocks(1,1)
    print(a)

    sleep(1000)
