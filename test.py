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
motor_tilt = MoveTank(OUTPUT_B, OUTPUT_C)

pixy2.set_lamp(1, 0)
sleep(0.5)
pixy2.set_lamp(0, 0)

resolution = pixy2.get_resolution()
MOTOR_SPEED = 10

voice = True

comptx = 0
compty = 0
compt_dist = 0
compute_dist = False
bb_box = []
while True :
    nbr , target = pixy2.get_blocks(3,1)
    if nbr == 1 : 
        if voice : 
            spkr.speak("target detected") 
            voice = False
            Align = True
        x = target[0].x_center
        y = target[0].y_center
        w = target[0].width
        h = target[0].height
        print(x, y , w, h)
        if Align :
            if x < 148 : 
                angle_x = 30 - (x/158 * 30)
                motor_forward.on_for_degrees(speed=MOTOR_SPEED, degrees=angle_x* 2.5)
                motor_forward.wait_until_not_moving()
            elif x > 168 :
                angle_x =  -((x-158)/158 * 30) 
                motor_forward.on_for_degrees(speed=MOTOR_SPEED, degrees=angle_x* 2.5)
                motor_forward.wait_until_not_moving()        
            else : 
                comptx += 1
            if y < 94 : 
                angle_y = 20 - (y/104 * 20)
                motor_tilt.on_for_degrees(MOTOR_SPEED,MOTOR_SPEED,angle_y)
                motor_tilt.wait_until_not_moving()
            elif y > 114 :
                angle_y =  -((y-104)/104 * 20) 
                motor_tilt.on_for_degrees(MOTOR_SPEED,MOTOR_SPEED,angle_y)
                motor_tilt.wait_until_not_moving()        
            else :
                compty += 1
            if comptx >= 3 and compty >= 3 : 
                print("ready")
                Align = False
                compute_dist = True
                spkr.speak("Ready to fire") 


        if compute_dist :
            if compt_dist >= 10 : 
                average_w, average_h = map(lambda z: sum(z) / len(bb_box), zip(*bb_box))
                print(average_w, average_h)
                break
            else : 
                bb_box.append([w,h])
                compt_dist += 1 
    sleep(0.2)
