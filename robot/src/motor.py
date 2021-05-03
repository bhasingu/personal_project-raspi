#!/usr/bin/env python

import time
import board
from adafruit_motorkit import MotorKit
import rospy
from std_msgs.msg import String

kit = MotorKit(i2c=board.I2C())

# Omni-wheel dimensions
N = 330 #N - RPM (revolutions per minute)
D = 0.06 #D - Diameter in meters
# v = 2pi*(D/2)*(N/60)
v = 1.03673 #v - linear velocity at the wheel in meters/second
# From experimental analysis however, the velocity is 0.92 m/s

def callback(data):
	if data.data == "stop":

		kit.motor1.throttle = 0.0
		kit.motor2.throttle = 0.0
		kit.motor3.throttle = 0.0
		kit.motor4.throttle = 0.0

	if data.data == "forward":

		kit.motor1.throttle = 0.5
		kit.motor2.throttle = 0.5
		kit.motor3.throttle = 0.5
		kit.motor4.throttle = 0.5

	if data.data == "reverse":

		kit.motor1.throttle = -0.5
		kit.motor2.throttle = -0.5
		kit.motor3.throttle = -0.5
		kit.motor4.throttle = -0.5

	if data.data == "rotate_cw":
                kit.motor1.throttle = 0.5
                kit.motor2.throttle = -0.5
                kit.motor3.throttle = 0.5
                kit.motor4.throttle = -0.5

	if data.data == "rotate_ccw":
                kit.motor1.throttle = -0.5
                kit.motor2.throttle = 0.5
                kit.motor3.throttle = -0.5
                kit.motor4.throttle = 0.5

def listener():
	rospy.init_node('motion_command_listener', anonymous=True)
	rospy.Subscriber("motion_command", String, callback)
	rospy.spin()
if __name__ == '__main__':
	listener()
