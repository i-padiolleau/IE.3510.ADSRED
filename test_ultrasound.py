# Modified Python code for an EV3 Lego robot to test the Ultrasonic Distance Sensor
# and turn a big motor for 5 seconds if the distance is greater than 40 cm

from ev3dev.ev3 import *
import time

# Connect the Ultrasonic Sensor to any input port, e.g., input port 1
us = UltrasonicSensor('in1') 

# Connect a large motor to any output port, e.g., output port A
motor = LargeMotor('outA')

# Ensure the sensor and motor are connected
assert us.connected, "Connect a single ultrasonic sensor to any sensor port"
assert motor.connected, "Connect a large motor to any motor port"

# Configure the sensor for distance measurements in centimeters
us.mode='US-DIST-CM'

# Function to measure and return the distance
def measure_distance():
    # Measure the distance and return it
    return us.value()/10  # convert mm to cm

# Testing the sensor
while True:
    distance = measure_distance()
    print("Distance:", distance, "cm")

    # Check if the distance is greater than 40 cm
    if distance > 40:
        print("Distance greater than 40 cm. Turning motor on.")
        motor.run_timed(time_sp=5000, speed_sp=500)  # Run motor for 5 seconds

    # Wait a bit before the next measurement
    time.sleep(0.5)
