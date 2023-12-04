# Python code for an EV3 Lego robot to test the Ultrasonic Distance Sensor

from ev3dev.ev3 import *

# Connect the Ultrasonic Sensor to any input port, e.g., input port 1
us = UltrasonicSensor('in1') 

# Ensure the sensor is connected
assert us.connected, "Connect a single ultrasonic sensor to any sensor port"

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
    # Wait a bit before the next measurement
    time.sleep(0.5)
