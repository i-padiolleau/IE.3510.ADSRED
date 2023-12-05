from ev3dev2.motor import LargeMotor
from time import sleep
from pixycamev3.pixy2 import Pixy2

MOTOR_SPEED = 500  # Motor speed in degrees per second
TURN_ANGLE = 180  # Turn angle in degrees
TURN_ANGLE_UP_DOWN = 90  # Turn angle for up and down motion in degrees

# Connect large motors to different output ports, e.g., output port A, B, and C
motor_forward = LargeMotor('outA')
motor_up_down_1 = LargeMotor('outB')
motor_up_down_2 = LargeMotor('outC')

pixy2 = Pixy2(port=2, i2c_address=0x54)

pixy2.set_lamp(1, 0)

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

while True:
    detected_objects = pixy2.get_blocks(1, 1)
    print("Detected Objects: {}".format(detected_objects))

    # Check if the Pixy2 camera detects any objects
    if detected_objects:
        print("Objects detected. Turning 180 degrees.")
        turn_robot(TURN_ANGLE)  # Turn the robot 180 degrees

        print("Turning up and down 90 degrees.")
        turn_up_down(TURN_ANGLE_UP_DOWN)  # Turn the robot up and down by 90 degrees

    sleep(1)  # Sleep for 1 second to avoid excessive loop frequency
