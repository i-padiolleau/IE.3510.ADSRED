#!/usr/bin/env python3

from time import sleep

from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.led import Leds
from ev3dev2.sound import Sound

from pixycamev3.pixy2 import Pixy2

spkr = Sound()
pixy2 = Pixy2(port=2, i2c_address=0x54)
motor_forward = LargeMotor(OUTPUT_A)
motor_tilt1 = LargeMotor(OUTPUT_B)
motor_tilt2 = LargeMotor(OUTPUT_C)

pixy2.set_lamp(1, 0)
sleep(0.5)
pixy2.set_lamp(0, 0)

resolution = pixy2.get_resolution()
MOTOR_SPEED = 50

voice = True

comptx = 0
compty = 0
while True :
    nbr , target = pixy2.get_blocks(3,1)
    if nbr == 1 :
        if voice : 
            spkr.speak("target detected") 
            voice = False
        x = target[0].x_center
        y = target[0].y_center
        w = target[0].width
        h = target[0].height
        print(x, y , w, h)
        if x < 148 : 
            angle = 30 - (x/158 * 30)
            motor_forward.on_for_degrees(speed=MOTOR_SPEED, degrees=angle* 2.5)
            motor_forward.wait_until_not_moving()
        elif x > 168 :
            angle =  -((x-158)/158 * 30) 
            motor_forward.on_for_degrees(speed=MOTOR_SPEED, degrees=angle* 2.5)
            motor_forward.wait_until_not_moving()        
        else : 
            comptx += 1
        if y < 94 : 
            angle = 20 - (x/104 * 20)
            motor_title1.on_for_degrees(speed=MOTOR_SPEED, degrees=angle)
            motor_forward.wait_until_not_moving()
        elif x > 114 :
            angle =  -((x-104)/104 * 20) 
            motor_forward.on_for_degrees(speed=MOTOR_SPEED, degrees=angle)
            motor_forward.wait_until_not_moving()        
        else :
            if compt == 3 :
                spkr.speak("Ready to fire") 
                pixy2.set_lamp(1, 0)
                sleep(0.5)
                pixy2.set_lamp(0, 0)
            else : 
                compt += 1 
    sleep(1)
