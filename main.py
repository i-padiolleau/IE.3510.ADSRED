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

        self.pixy2.set_lamp(1, 0)
        sleep(0.5)
        self.pixy2.set_lamp(0, 0)

    def scan_sequence(self):

        self.motor_forward.on_for_degrees(speed=10, degrees=120)

    def detect(self) : 

        while True : 
            nbr, target = self.pixy2.get_blocks(1,1)

            if target : 
                self.motor_forward.stop()


test = Robot(OUTPUT_A, OUTPUT_D, OUTPUT_C)
test.scan_sequence()
test.detect()