from time import sleep

from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank, MediumMotor
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.led import Leds
from ev3dev2.sound import Sound

motor_forward = LargeMotor(OUTPUT_A)

print(motor_forward.position)

motor_forward.on_for_degrees(speed=10, degrees=180)
motor_forward.wait_until_not_moving()

print(motor_forward.position)

motor_forward.on_for_degrees(speed=10, degrees=-90)
motor_forward.wait_until_not_moving()

print(motor_forward.position)
