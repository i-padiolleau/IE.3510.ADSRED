#!/usr/bin/env python3

from time import sleep

from ev3dev2.motor import MediumMotor , LargeMotor, OUTPUT_A,OUTPUT_B, OUTPUT_D, OUTPUT_C, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.led import Leds
from ev3dev2.sound import Sound

from math import sqrt, cos , sin, atan

from pixycamev3.pixy2 import Pixy2

spkr = Sound()
pixy2 = Pixy2(port=1, i2c_address=0x54)
motor_forward = LargeMotor(OUTPUT_A)
motor_tilt = LargeMotor( OUTPUT_B)
motor_shoot = MediumMotor(OUTPUT_D)

print(motor_forward.position , motor_tilt.position)

motor_forward_starting_position , motor_tilt_starting_position = motor_forward.position , motor_tilt.position

pixy2.set_lamp(1, 0)
sleep(0.5)
pixy2.set_lamp(0, 0)

resolution = pixy2.get_resolution()

def reboot(x, y, motor1, motor2) : 
    motor1.on_to_position(15, x)
    motor2.on_to_position(15, y)
    motor1.wait_while('running')
    motor2.wait_while('running')


voice = True

i = 0 
sequence=[-1,-1,-1,-1,1,1,1,1,1,1,1,1,2,-1,-1,-1,-1,-1,-1,-1,-1,2,1,1,1,1,1,1,1,1,-1,-1,-1,-1,-1,-1,-1,-1,-2,1,1,1,1,1,1,1,1,-2,-1,-1,-1,-1]
compt = 0
comptx = 0
compty = 0
compt_dist = 0
compute_dist = False
bb_box = []
pos_on_x = False
pos_on_y = False
detect = False
compt_loss = 0 
shoot = False
test = input("start_scanning press enter :")
while True :
    nbr , target = pixy2.get_blocks(1,1)
    pos_on_x = False
    pos_on_y = False
    if nbr >= 1 : 
        detect = True
        if voice : 
            voice = False
            Align = True
        x = target[0].x_center
        y = target[0].y_center
        w = target[0].width
        h = target[0].height
        if Align :
            if x < 148 : 
                angle_x = 30 - (x/158 * 30)
                motor_forward.on_for_degrees(speed=15, degrees=angle_x* 2.5)
                motor_forward.wait_while('running')
                compt = 0
            elif x > 168 :
                angle_x =  -((x-158)/158 * 30) 
                motor_forward.on_for_degrees(speed=15, degrees=angle_x* 2.5)
                motor_forward.wait_while('running')        
                compt = 0
            else : 
                pos_on_x = True
            if y < 94 : 
                angle_y = 20 - (y/104 * 20)
                motor_tilt.on_for_degrees(6,angle_y)
                motor_tilt.wait_while('running')
                compt = 0
            elif y > 114 :
                angle_y =  -((y-104)/104 * 20) 
                motor_tilt.on_for_degrees(6,angle_y)
                motor_tilt.wait_while('running')  
                compt = 0
        
            else :
                pos_on_y = True
            if pos_on_x and pos_on_y : 
                compt += 1 
            if compt >= 5 : 
                print("ready")
                Align = False
                compute_dist = True
                compt = 0 


        if compute_dist :
            if compt_dist >= 15 : 
                average_w, average_h = map(lambda z: sum(z) / len(bb_box), zip(*bb_box))
                average_diag = sqrt((average_w**2) + (average_h**2))

                distance = (378*0.16) / average_diag
                compute_dist = False  
                shoot = True            
                bb_box = []
                compt_dist = 0
            else : 
                bb_box.append([w,h])
                compt_dist += 1 

        if shoot : 
            print(motor_tilt.position -motor_tilt_starting_position)
            print(distance)
            # print(compute_shooting_angle(motor_tilt.position -motor_tilt_starting_position, distance))
            reglage_angle = 3.74 + (0.06*(motor_tilt.position - motor_tilt_starting_position))  + (13.37*distance)
            # motor_tilt.on_for_degrees(10,20)
            motor_tilt.on_for_degrees(10,reglage_angle)
            motor_shoot.on_for_degrees(speed=23, degrees=-380)
            motor_shoot.wait_while('running')

            motor_shoot.on_for_degrees(speed=23, degrees=380)
            motor_shoot.wait_while('running')
            reboot(motor_forward_starting_position , motor_tilt_starting_position,motor_forward, motor_tilt)
            i = 0 
            shoot = False
            voice = True

    elif detect :
        if compt_loss >= 5 : 
            detect = False
            print("target lose")
            reboot(motor_forward_starting_position , motor_tilt_starting_position,motor_forward, motor_tilt)
            i = 0 
            compt_loss = 0
            voice = True 
            Align = False
        else :
            compt_loss += 1 

    else : 
        move = sequence[i]
        if move == 1 : 
            motor_forward.on_for_degrees(speed=15, degrees=30 * 2.5)
            motor_forward.wait_while('running')
        elif move == -1 : 
            motor_forward.on_for_degrees(speed=15, degrees=-30 * 2.5)
            motor_forward.wait_while('running')
        elif move == 2 : 
            motor_tilt.on_for_degrees(10,27)
            motor_tilt.wait_while('running')
        elif move == -2 : 
            motor_tilt.on_for_degrees(10,-27)
            motor_tilt.wait_while('running')
        i += 1 
        if i ==len(sequence) : 

            i = 0 

