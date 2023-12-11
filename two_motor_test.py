#!/usr/bin/env python3

from time import sleep

from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank
from ev3dev2.sound import Sound
from pixycamev3.pixy2 import Pixy2

spkr = Sound()
pixy2 = Pixy2(port=2, i2c_address=0x54)
motor_forward = LargeMotor(OUTPUT_A)
motor_tilt = MoveTank(OUTPUT_B, OUTPUT_C)

pixy2.set_lamp(1, 0)
sleep(0.5)
pixy2.set_lamp(0, 0)

resolution = pixy2.get_resolution()
MOTOR_SPEED = 10

voice = True

# PID constants (adjust these based on your system and tuning)
kp = 1.0  # Proportional gain
ki = 0.1  # Integral gain
kd = 0.01  # Derivative gain

comptx = 0
compty = 0
compt_dist = 0
compute_dist = False
bb_box = []
Align = False

# Initialize PID variables
prev_error_x = 0
integral_x = 0

prev_error_y = 0
integral_y = 0

while True:
    nbr, target = pixy2.get_blocks(3, 1)

    if nbr == 1:
        if voice:
            spkr.speak("target detected")
            voice = False
            Align = True
        x = target[0].x_center
        y = target[0].y_center
        w = target[0].width
        h = target[0].height
        print(x, y, w, h)

        if Align:
            # Calculate error
            error_x = x - 158  # Assume the target is centered at x-coordinate 158
            error_y = y - 104  # Assume the target is centered at y-coordinate 104

            # Update integral terms for x-axis
            integral_x = integral_x + error_x

            # Update integral terms for y-axis
            integral_y = integral_y + error_y

            # Calculate PID outputs
            pid_output_x = kp * error_x + ki * integral_x + kd * (error_x - prev_error_x)
            pid_output_y = kp * error_y + ki * integral_y + kd * (error_y - prev_error_y)

            # Update motor positions based on PID outputs
            motor_forward.on(SpeedPercent(MOTOR_SPEED - pid_output_x), brake=False)
            motor_tilt.on(SpeedPercent(MOTOR_SPEED - pid_output_y), brake=False)

            # Save current errors for the next iteration
            prev_error_x = error_x
            prev_error_y = error_y

            comptx += 1 if abs(error_x) < 10 else 0
            compty += 1 if abs(error_y) < 10 else 0

            if comptx >= 3 and compty >= 3:
                print("ready")
                Align = False
                compute_dist = True
                spkr.speak("Ready to fire")

        if compute_dist:
            if compt_dist >= 10:
                average_w, average_h = map(lambda z: sum(z) / len(bb_box), zip(*bb_box))
                print(average_w, average_h)
                break
            else:
                bb_box.append([w, h])
                compt_dist += 1

    sleep(0.2)
