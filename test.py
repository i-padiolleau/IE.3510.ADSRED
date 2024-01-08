#!/usr/bin/env python3

from time import sleep

from ev3dev2.motor import MediumMotor , LargeMotor, OUTPUT_A, OUTPUT_D, OUTPUT_C, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.led import Leds
from ev3dev2.sound import Sound

from pixycamev3.pixy2 import Pixy2

spkr = Sound()
pixy2 = Pixy2(port=1, i2c_address=0x54)
motor_forward = LargeMotor(OUTPUT_A)
motor_tilt = LargeMotor( OUTPUT_C)
motor_shoot = MediumMotor(OUTPUT_D)

print(motor_forward.position , motor_tilt.position)

motor_forward_starting_position , motor_tilt_starting_position = motor_forward.position , motor_tilt.position

pixy2.set_lamp(1, 0)
sleep(0.5)
pixy2.set_lamp(0, 0)

resolution = pixy2.get_resolution()

def reboot(x, y, motor1, motor2) : 
    motor1.on_to_position(10, x)
    motor2.on_to_position(10, y)
    motor1.wait_until_not_moving() 
    motor2.wait_until_not_moving() 

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
            spkr.speak("target detected") 
            voice = False
            Align = True
        x = target[0].x_center
        y = target[0].y_center
        w = target[0].width
        h = target[0].height
        if Align :
            if x < 148 : 
                angle_x = 30 - (x/158 * 30)
                motor_forward.on_for_degrees(speed=10, degrees=angle_x* 2.5)
                motor_forward.wait_until_not_moving()
                compt = 0
            elif x > 168 :
                angle_x =  -((x-158)/158 * 30) 
                motor_forward.on_for_degrees(speed=10, degrees=angle_x* 2.5)
                motor_forward.wait_until_not_moving()        
                compt = 0
            else : 
                pos_on_x = True
            if y < 94 : 
                angle_y = 20 - (y/104 * 20)
                motor_tilt.on_for_degrees(10,angle_y)
                motor_tilt.wait_until_not_moving()
                compt = 0
            elif y > 114 :
                angle_y =  -((y-104)/104 * 20) 
                motor_tilt.on_for_degrees(10,angle_y)
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
                compt = 0 


        if compute_dist :
            if compt_dist >= 15 : 
                average_w, average_h = map(lambda z: sum(z) / len(bb_box), zip(*bb_box))
                print(average_w, average_h)  
                distance_on_x = (125*316) / average_w
                distance_on_y = (105*208) / average_h
                print("distance with x : {}mm".format(distance_on_x))
                print("distance with y : {}mm".format(distance_on_y))
                compute_dist = False  
                shoot = True            
            else : 
                bb_box.append([w,h])
                compt_dist += 1 

        if shoot : 
            motor_tilt.on_for_degrees(10,20)
            motor_shoot.on_for_degrees(speed=20, degrees=-310)
            motor_shoot.wait_until_not_moving()

            motor_shoot.on_for_degrees(speed=20, degrees=310)
            motor_shoot.wait_until_not_moving()
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
        print(move)
        if move == 1 : 
            motor_forward.on_for_degrees(speed=10, degrees=30 * 2.5)
            motor_forward.wait_until_not_moving()
        elif move == -1 : 
            motor_forward.on_for_degrees(speed=10, degrees=-30 * 2.5)
            motor_forward.wait_until_not_moving()
        elif move == 2 : 
            motor_tilt.on_for_degrees(10,27)
            motor_tilt.wait_until_not_moving()
        elif move == -2 : 
            motor_tilt.on_for_degrees(10,-27)
            motor_tilt.wait_until_not_moving
        i += 1 
        if i ==len(sequence) : 

            i = 0 

