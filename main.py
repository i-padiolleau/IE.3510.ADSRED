from threading import Thread
from time import sleep
from ev3dev2.motor import LargeMotor,MediumMotor,  OUTPUT_A, OUTPUT_D, OUTPUT_C, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.led import Leds
from ev3dev2.sound import Sound

from pixycamev3.pixy2 import Pixy2

class Robot() : 

    def __init__(self, Port_out_forward, Port_out_tilt, Port_out_shoot ):
        self.pixy2 = Pixy2(port=1, i2c_address=0x54)
        self.motor_forward = LargeMotor(Port_out_forward)
        self.motor_tilt = LargeMotor(Port_out_tilt)
        self.motor_shoot = MediumMotor(Port_out_shoot)

        self.motor_forward_starting_position = self.motor_forward.position
        self.motor_tilt_starting_position =  self.motor_tilt.position

        self.angle_x = 0
        self.angle_y = 0

        self.pixy2.set_lamp(1, 0)
        sleep(0.5)
        self.pixy2.set_lamp(0, 0)

    def reboot(self) : 

        self.motor_forward.on_to_position(10, self.motor_forward_starting_position)
        self.motor_tilt.on_to_position(10, self.motor_tilt_starting_position)

    def scan_sequence(self):

        self.motor_forward.on_for_degrees(speed=10, degrees=60* 2.5)
        self.motor_forward.on_for_degrees(speed=10, degrees=-120* 2.5)
        self.motor_tilt.on_for_degrees(10,27)
        self.motor_forward.on_for_degrees(speed=10, degrees=120* 2.5)
        self.motor_tilt.on_for_degrees(10,27)
        self.motor_forward.on_for_degrees(speed=10, degrees=-120* 2.5)
        self.reboot()
        self.scan_sequence()

    def detect(self) :  
        nbr, target = self.pixy2.get_blocks(1,1)

        if nbr >= 1 : 
            return target
        else : 
            return []

    def follow_target(self, target) : 
        x = target[0].x_center
        y = target[0].y_center
        w = target[0].width
        h = target[0].height

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



def main():

    robot = Robot(OUTPUT_A, OUTPUT_C, OUTPUT_D)
    t = Thread(target=robot.scan_sequence)
    t.start()
    t1 = Thread(target=robot.detect())
    while True:
        if len(robot.detect()) > 0 :
            robot.


if __name__ == "__main__" :
    main()
