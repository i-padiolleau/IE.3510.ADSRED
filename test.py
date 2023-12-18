#!/usr/bin/env python3

from time import sleep

from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_D, OUTPUT_C, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.led import Leds
from ev3dev2.sound import Sound

from pixycamev3.pixy2 import Pixy2

spkr = Sound()
pixy2 = Pixy2(port=2, i2c_address=0x54)
motor_forward = LargeMotor(OUTPUT_A)
motor_tilt = LargeMotor( OUTPUT_C)

print(motor_forward.position , motor_tilt.position)

pixy2.set_lamp(1, 0)
sleep(0.5)
pixy2.set_lamp(0, 0)

resolution = pixy2.get_resolution()
MOTOR_SPEED = 10

voice = True

i = 0 
sequence=[1,1,1,1,2,-1,-1,-1,-1,2,1,1,1,1,-1,-1,-1,-1,-2,1,1,1,1,-2,-1,-1,-1,-1]
compt = 0
comptx = 0
compty = 0
compt_dist = 0
compute_dist = False
bb_box = []
pos_on_x = False
pos_on_y = False
test = input("start_scanning press enter")
while True :
    nbr , target = pixy2.get_blocks(3,1)
    if nbr >= 1 : 
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
                compt = 0
            elif x > 168 :
                angle_x =  -((x-158)/158 * 30) 
                motor_forward.on_for_degrees(speed=MOTOR_SPEED, degrees=angle_x* 2.5)
                motor_forward.wait_until_not_moving()        
                compt = 0
            else : 
                pos_on_x = True
            if y < 94 : 
                angle_y = 20 - (y/104 * 20)
                motor_tilt.on_for_degrees(MOTOR_SPEED,angle_y)
                motor_tilt.wait_until_not_moving()
                compt = 0
            elif y > 114 :
                angle_y =  -((y-104)/104 * 20) 
                motor_tilt.on_for_degrees(MOTOR_SPEED,angle_y)
                motor_tilt.wait_until_not_moving()  
                compt = 0
            else :
                pos_on_y = True
            if pos_on_x and pos_on_y : 
                compt += 1 
            if compt >= 5 : 
                print("ready")
                Align = False
                compute_dist = True
                spkr.speak("Ready to fire") 


        if compute_dist :
            if compt_dist >= 5 : 
                average_w, average_h = map(lambda z: sum(z) / len(bb_box), zip(*bb_box))
                print(average_w, average_h)  
                distance_on_x = (125*316) / average_w
                distance_on_y = (105*208) / average_h
                print("distance with x : {}mm".format(distance_on_x))
                print("distance with y : {}mm".format(distance_on_y))
                compute_dist = False  
                Align = True            
            else : 
                bb_box.append([w,h])
                compt_dist += 1 

    else : 
        move = sequence[i]
        print(i, move)
        if move == 1 : 
            motor_forward.on_for_degrees(speed=MOTOR_SPEED, degrees=30 * 2.5)
        elif move == -1 : 
            motor_forward.on_for_degrees(speed=MOTOR_SPEED, degrees=-30 * 2.5)
        elif move == 2 : 
            motor_tilt.on_for_degrees(MOTOR_SPEED,27)
        elif move == -2 : 
            motor_tilt.on_for_degrees(MOTOR_SPEED,-27)
        i += 1 
        if i ==28 : 
            print(motor_forward.position , motor_tilt.position)

            i = 0 

    sleep(0.2)
