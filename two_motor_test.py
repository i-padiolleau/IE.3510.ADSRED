#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1, INPUT_2
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.led import Leds
from time import sleep

motor_forward = LargeMotor(OUTPUT_A)
motor_tilt = MoveTank(OUTPUT_B, OUTPUT_C)


print(motor_forward.position)
print(motor_forward.position())
motor_tilt.reset()
