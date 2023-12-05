#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.led import Leds

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.

MOTOR_RUNTIME = 5000  # Motor runtime in milliseconds
MOTOR_SPEED = 500  # Motor speed in degrees per second
TURN_ANGLE = 180  # Turn angle in degrees
TURN_ANGLE_UP_DOWN = 90  # Turn angle for up and down motion in degrees

from pixycamev3.pixy2 import Pixy2

pixy2 = Pixy2(port=2, i2c_address=0x54)

pixy2.set_lamp(1, 0)

# Connect large motors to different output ports, e.g., output port A, B, and C
"motor_forward = LargeMotor('outA')
motor_up_down_1 = LargeMotor('outA')
motor_up_down_2 = LargeMotor('outB')

# Function to move the robot forward for a specified time
def move_forward(time_sp):
    motor_forward.run_timed(time_sp=time_sp, speed_sp=MOTOR_SPEED)
    motor_forward.wait_until_not_moving()  # Wait until the motor stops

# Function to turn the robot by a specified angle
def turn_robot(angle):
    motor_forward.run_to_rel_pos(position_sp=angle, speed_sp=MOTOR_SPEED)
    motor_forward.wait_until_not_moving()  # Wait until the motor stops

# Function to turn the robot up and down by a specified angle for both motors
def turn_up_down(angle):
    motor_up_down_1.run_to_rel_pos(position_sp=angle, speed_sp=MOTOR_SPEED)
    motor_up_down_2.run_to_rel_pos(position_sp=angle, speed_sp=MOTOR_SPEED)
    
    # Wait until both motors stop
    motor_up_down_1.wait_until_not_moving()
    motor_up_down_2.wait_until_not_moving()

while True :
    detected_objects = pixy2.get_blocks(1,1)
    print("Distance: {} cm, Detected Objects: {}".format(distance, detected_objects))

    # Check if the Pixy2 camera detects any objects
    if detected_objects:
        print("Objects detected. Turning 180 degrees.")
        turn_robot(TURN_ANGLE)  # Turn the robot 180 degrees

        print("Turning up and down 90 degrees.")
        turn_up_down(TURN_ANGLE_UP_DOWN)  # Turn the robot up and down by 90 degrees
    sleep(1000)
