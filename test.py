#!/usr/bin/env python3

from time import sleep

from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.led import Leds
from ev3dev2.sound import Sound

from pixycamev3.pixy2 import Pixy2

spkr = Sound()
pixy2 = Pixy2(port=2, i2c_address=0x54)
motor_forward = LargeMotor(OUTPUT_A)

pixy2.set_lamp(1, 0)
sleep(0.5)
pixy2.set_lamp(0, 0)

resolution = pixy2.get_resolution()
WIDTH = resolution.width
HEIGHT = resolution.height
MOTOR_SPEED = 50

print('Frame width:  ', resolution.width)
print('Frame height: ', resolution.height)

while True :
    nbr , target = pixy2.get_blocks(1,1)
    if nbr == 1 : 
        spkr.speak("target detected")
        x = target[0].x_center
        y = target[0].y_center
        w = target[0].width
        h = target[0].height
        if x < WIDTH/2 : 
            motor_forward.on_for_degrees(speed=MOTOR_SPEED, degrees=10)
            motor_forward.wait_until_not_moving()
        
        print( x, y , w, h)

    sleep(1)
