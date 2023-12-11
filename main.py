from time import sleep
from ev3dev2.motor import LargeMotor, MoveTank, OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.led import Leds
from ev3dev2.sound import Sound
from pixycamev3.pixy2 import Pixy2

class Robot:
    def __init__(self):
        self.spkr = Sound()
        self.pixy2 = Pixy2(port=2, i2c_address=0x54)
        self.motor_forward = LargeMotor(OUTPUT_A)
        self.motor_tilt = MoveTank(OUTPUT_D, OUTPUT_C)
        self.pixy2.set_lamp(1, 0)
        sleep(0.5)
        self.pixy2.set_lamp(0, 0)
        self.MOTOR_SPEED = 10
        self.voice = True
        self.Align = False
        self.compute_dist = False
        self.bb_box = []
        self.pos_on_x = False
        self.pos_on_y = False
        self.compt = 0
        self.comptx = 0
        self.compty = 0
        self.compt_dist = 0

    def rotate_cam(self): 
        print(self.motor_forward.position)
        print(self.motor_tilt.position)
        self.motor_forward.on_for_degrees(speed=self.MOTOR_SPEED, degrees=16)
        self.motor_forward.wait_until_not_moving()

    def start_scanning(self):
        while True:
            nbr, target = self.pixy2.get_blocks(3, 1)
            if nbr == 1:
                if self.voice:
                    self.spkr.speak("target detected")
                    self.voice = False
                    self.Align = True
                x = target[0].x_center
                y = target[0].y_center
                w = target[0].width
                h = target[0].height
                print(x, y, w, h)
                self._align_robot(x, y, w, h)
                self._compute_distance(w, h)
            else : 
                self.rotate_cam()
            sleep(0.2)

    def _align_robot(self, x, y, w, h):
        if self.Align:
            if x < 148:
                angle_x = 30 - (x / 158 * 30)
                self.motor_forward.on_for_degrees(speed=self.MOTOR_SPEED, degrees=angle_x * 2.5)
                self.motor_forward.wait_until_not_moving()
            elif x > 168:
                angle_x = -((x - 158) / 158 * 30)
                self.motor_forward.on_for_degrees(speed=self.MOTOR_SPEED, degrees=angle_x * 2.5)
                self.motor_forward.wait_until_not_moving()
            else:
                self.pos_on_x = True

            if y < 94:
                angle_y = 20 - (y / 104 * 20)
                self.motor_tilt.on_for_degrees(self.MOTOR_SPEED, self.MOTOR_SPEED, angle_y)
                self.motor_tilt.wait_until_not_moving()
            elif y > 114:
                angle_y = -((y - 104) / 104 * 20)
                self.motor_tilt.on_for_degrees(self.MOTOR_SPEED, self.MOTOR_SPEED, angle_y)
                self.motor_tilt.wait_until_not_moving()
            else:
                self.pos_on_y = True

            if self.pos_on_x and self.pos_on_y:
                self.compt += 1
                print("presque")
            if self.compt >= 5:
                print("ready")
                self.Align = False
                self.compute_dist = True
                self.spkr.speak("Ready to fire")

    def _compute_distance(self,w,h):
        if self.compute_dist:
            if self.compt_dist >= 10:
                average_w, average_h = map(lambda z: sum(z) / len(self.bb_box), zip(*self.bb_box))
                print(average_w, average_h)
                distance_on_x = (100 * 316) / average_w
                distance_on_y = (100 * 208) / average_h
                print("distance with x : {}mm".format(distance_on_x))
                print("distance with y : {}mm".format(distance_on_y))
                self.compute_dist = False
                self.Align = True
            else:
                self.bb_box.append([w, h])
                self.compt_dist += 1

if __name__ == "__main__":
    my_robot = Robot()
    test = input("start_scanning press enter : ")
    my_robot.start_scanning()
