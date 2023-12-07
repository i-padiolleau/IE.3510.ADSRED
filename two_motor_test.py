from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1, INPUT_2
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.led import Leds
from time import sleep
from pixycamev3.pixy2 import Pixy2


MOTOR_SPEED = 50  # Motor speed in degrees per second
TURN_ANGLE = 180  # Turn angle in degrees
TURN_ANGLE_UP_DOWN = 90  # Turn angle for up and down motion in degrees

# Connect the Ultrasonic Sensor to any input port, e.g., input port 1
us = UltrasonicSensor(INPUT_1)

# Connect large motors to different output ports, e.g., output port A, B, and C
motor_forward = LargeMotor(OUTPUT_A)
motor_up_down_1 = LargeMotor(OUTPUT_B)
motor_up_down_2 = LargeMotor(OUTPUT_C)

pixy2 = Pixy2(port=2, i2c_address=0x54)

pixy2.set_lamp(1, 0)

# Configure the sensors
us.mode = 'US-DIST-CM'

# Function to measure and return the distance
def measure_distance():
    return us.distance_centimeters

# Function to turn the robot by a specified angle
def turn_robot(angle):
    motor_forward.on_for_degrees(speed=MOTOR_SPEED, degrees=angle)
    sleep(1)
    motor_forward.wait_until_not_moving()  # Wait until the motor stops

# Function to turn the robot up and down by a specified angle for both motors
def turn_up_down(angle):

    motor_up_down_1.on_for_degrees(speed=MOTOR_SPEED, degrees=angle)
    motor_up_down_2.on_for_degrees(speed=MOTOR_SPEED, degrees=angle)
    sleep(1)
    # Wait until both motors stop
    #motor_up_down_1.wait_while('running')
    #motor_up_down_2.wait_while('running')
    motor_up_down_1.wait_until_not_moving()
    motor_up_down_2.wait_until_not_moving()
    
while True:
    distance = measure_distance()
    
    detected_objects = pixy2.get_blocks(1, 1)
    print("Detected Objects: {}".format(detected_objects))
    print("Distance: {} cm, Detected Objects: {}".format(distance, detected_objects))

    # Check if the Pixy2 camera detects any objects
    if detected_objects:
        print("Objects detected. Turning 180 degrees.")
        turn_robot(TURN_ANGLE)  # Turn the robot 180 degrees

        print("Turning up and down 90 degrees.")
        turn_up_down(TURN_ANGLE_UP_DOWN)  # Turn the robot up and down by 90 degrees

    sleep(1)  # Sleep for 1 second to avoid excessive loop frequency
