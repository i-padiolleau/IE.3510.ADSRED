from ev3dev.ev3 import *
import time

# Constants
DIST_THRESHOLD = 40  # Distance threshold in centimeters
MOTOR_RUNTIME = 5000  # Motor runtime in milliseconds
MOTOR_SPEED = 500  # Motor speed in degrees per second
TURN_ANGLE = 180  # Turn angle in degrees
TURN_ANGLE_UP_DOWN = 90  # Turn angle for up and down motion in degrees
SEARCH_COLOR = ColorSensor.COLOR_RED  # Change to the desired color

# Connect the Ultrasonic Sensor to any input port, e.g., input port 1
us = UltrasonicSensor('in1')

# Connect large motors to different output ports, e.g., output port A, B, and C
motor_forward = LargeMotor('outA')
motor_up_down_1 = LargeMotor('outB')
motor_up_down_2 = LargeMotor('outC')

# Connect a color sensor to any input port, e.g., input port 2
color_sensor = ColorSensor('in2')

# Ensure the sensors and motors are connected

#assert us.connected, "Connect a single ultrasonic sensor to any sensor port"
#assert motor_forward.connected, "Connect a large motor to any motor port for forward motion"
#assert motor_up_down_1.connected, "Connect a large motor to any motor port for up and down motion 1"
#assert motor_up_down_2.connected, "Connect a large motor to any motor port for up and down motion 2"
#assert color_sensor.connected, "Connect a color sensor to any sensor port"

# Configure the sensors
us.mode = 'US-DIST-CM'
color_sensor.mode = 'COL-COLOR'  # Set color sensor to detect colors

# Function to measure and return the distance
def measure_distance():
    return us.value() / 10  # convert mm to cm

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

# Testing the sensors and motors
while True:
    distance = measure_distance()
    color = color_sensor.value()

    print(f"Distance: {distance} cm, Color: {color}")

    # Check if the distance is greater than the threshold
    if distance > DIST_THRESHOLD:
        print("Distance greater than", DIST_THRESHOLD, "cm. Moving forward.")
        move_forward(MOTOR_RUNTIME)  # Move forward for 5 seconds

    # Check if the color sensor detects the specified color
    if color == SEARCH_COLOR:
        print(f"Color {SEARCH_COLOR} detected. Turning 180 degrees.")
        turn_robot(TURN_ANGLE)  # Turn the robot 180 degrees

        print("Turning up and down 90 degrees.")
        turn_up_down(TURN_ANGLE_UP_DOWN)  # Turn the robot up and down by 90 degrees

    # Wait a bit before the next measurement
    time.sleep(0.5)
