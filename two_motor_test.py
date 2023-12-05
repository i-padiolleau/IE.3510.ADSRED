#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()
left_motor = Motor(Port.A)
right_motor = Motor(Port.B)

robot = DriveBase(left_motor, right_motor, wheel_diameter=55.5, axle_track=104)
# Write your program here.

robot.turn(90)
robot.stop()
left_motor.brake()
right_motor.brake()
ev3.speaker.beep()

#left_motor = left_motor.run_target(1000,90)
#right_motor = right_motor.run_target(1000,90)