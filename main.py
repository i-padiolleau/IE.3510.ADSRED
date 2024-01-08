from threading import Thread
from time import sleep
from ev3dev2.motor import LargeMotor,MediumMotor,  OUTPUT_A, OUTPUT_D, OUTPUT_C, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.led import Leds
from ev3dev2.sound import Sound

from pixycamev3.pixy2 import Pixy2

from math import sqrt

class Robot() : 

    def __init__(self, Port_out_forward, Port_out_tilt, Port_out_shoot ):
        self.pixy2 = Pixy2(port=2, i2c_address=0x54)
        self.motor_forward = LargeMotor(Port_out_forward)
        self.motor_tilt = LargeMotor(Port_out_tilt)
        self.motor_shoot = MediumMotor(Port_out_shoot)

        self.motor_forward_starting_position = self.motor_forward.position
        self.motor_tilt_starting_position =  self.motor_tilt.position

        self.angle_x = 0
        self.angle_y = 0

        self.target = []

        self.sequence_list = [1,2,-1,2,1,2,-1,1,-2,-1,-2,1,-2,-1]

        self.iteration = 0 

        self.bb_box = []

        self.distance = 0 

        self.motor_running = True

        self.pixy2.set_lamp(1, 0)
        sleep(0.5)
        self.pixy2.set_lamp(0, 0)

    def reboot(self) : 

        self.motor_forward.on_to_position(10, self.motor_forward_starting_position)
        self.motor_tilt.on_to_position(10, self.motor_tilt_starting_position)


    # def scan_sequence(self):

    #     self.motor_forward.on_for_degrees(speed=10, degrees=60* 2.5)
    #     self.motor_forward.on_for_degrees(speed=10, degrees=-120* 2.5)
    #     self.motor_tilt.on_for_degrees(10,27)
    #     self.motor_forward.on_for_degrees(speed=10, degrees=120* 2.5)
    #     self.motor_tilt.on_for_degrees(10,27)
    #     self.motor_forward.on_for_degrees(speed=10, degrees=-120* 2.5)
    #     self.reboot()
    #     self.scan_sequence()

    def movement(self) : 

        while True : 
            self.motor_forward.wait_until_not_moving()
            self.motor_tilt.wait_until_not_moving()
            self.motor_forward.on_for_degrees(speed=10, degrees=self.angle_x* 2.5)
            self.motor_tilt.on_for_degrees(speed=10, degrees=self.angle_y)


    def sequence(self) : 

        move = self.sequence_list[self.iteration]
        if move == 1 : 
            self.angle_x = 120
            self.angle_y = 0 
        elif move == -1 : 
            self.angle_x = -120
            self.angle_y = 0 
        elif move == 2 : 
            self.angle_y = 30 
            self.angle_x = 0          
        elif move == -2 : 
            self.angle_y = -30 
            self.angle_x = 0
        self.iteration += 1 
        if self.iteration ==len(self.sequence_list) : 
            self.iteration = 0 

    def compute_dist(self):

        average_w, average_h = map(lambda z: sum(z) / len(self.bb_box), zip(*self.bb_box))

        average_diag = sqrt((average_w^2) + (average_h^2))

        self.distance = (378*16) / average_diag

        print(self.distance)

    def detect(self) :  
        while True : 
            nbr, target = self.pixy2.get_blocks(1,1)

            if nbr >= 1 : 
                self.target = target
            else : 
                self.target = []

    def follow_target(self) : 
        x = self.target[0].x_center
        y = self.target[0].y_center
        w = self.target[0].width
        h = self.target[0].height

        if x < 148 : 
            self.angle_x = 30 - (x/158 * 30)
        elif x > 168 :
            self.angle_x =  -((x-158)/158 * 30) 
        else : 
            self.angle_x = 0

        if y < 94 : 
            self.angle_y = 20 - (y/104 * 20)
        elif y > 114 :
            self.angle_y =  -((y-104)/104 * 20) 
        else : 
            self.angle_y = 0 

        self.motor_forward.on_for_degrees(speed=10, degrees=self.angle_x* 2.5)
        self.motor_tilt.on_for_degrees(speed=10, degrees=self.angle_y)

        self.bb_box.append([w,h])

        self.compute_dist()
     
    def main_sequence(self): 
        while True : 
            if len(self.target) > 0 :
                self.motor_forward.stop()
                self.motor_tilt.stop()
                self.follow_target()
            else : 
                if not self.motor_running :
                    self.sequence()
            print(self.angle_x, self.angle_y)
    
        


def main():

    robot = Robot(OUTPUT_A, OUTPUT_C, OUTPUT_D)
    t = Thread(target=robot.movement)
    t.start()
    t1 = Thread(target=robot.detect)
    t1.start()
    t2 = Thread(target=robot.main_sequence)
    t2.start()
    # while True:
    #     jsp = True




if __name__ == "__main__" :
    main()
