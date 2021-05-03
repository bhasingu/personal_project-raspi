#!/usr/bin/env python
import rospy
from std_msgs.msg import String, Float32
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

TRIG_FRONT = 23
ECHO_FRONT = 24

TRIG_LEFT = 25
ECHO_LEFT = 20

TRIG_RIGHT = 8
ECHO_RIGHT = 21

print("Distance Measurement In Progress")

GPIO.setup(TRIG_FRONT,GPIO.OUT)
GPIO.setup(TRIG_LEFT,GPIO.OUT)
GPIO.setup(TRIG_RIGHT,GPIO.OUT)

GPIO.setup(ECHO_FRONT,GPIO.IN)
GPIO.setup(ECHO_LEFT,GPIO.IN)
GPIO.setup(ECHO_RIGHT,GPIO.IN)

GPIO.output(TRIG_FRONT, False)
GPIO.output(TRIG_LEFT, False)
GPIO.output(TRIG_RIGHT, False)

print("Waiting For Sensor To Settle")

time.sleep(2)

def talker():
	pub_front = rospy.Publisher('ultrasonic_front', Float32, queue_size=10)
	pub_left = rospy.Publisher('ultrasonic_left', Float32, queue_size=10)
	pub_right = rospy.Publisher('ultrasonic_right', Float32, queue_size=10)
	rospy.init_node('ultrasonic_sensors', anonymous=True)
	rate = rospy.Rate(10) # 10hz
	while not rospy.is_shutdown():
		GPIO.output(TRIG_FRONT, True)
		time.sleep(0.00001)
		GPIO.output(TRIG_FRONT, False)
		while GPIO.input(ECHO_FRONT)==0:
			pulse_start = time.time()
		while GPIO.input(ECHO_FRONT)==1:
			pulse_end = time.time()
		pulse_duration = pulse_end - pulse_start
		distance = pulse_duration * 17150
		distance = (round(distance, 2)) / 100
		#rospy.loginfo(distance)
		pub_front.publish(distance)

		GPIO.output(TRIG_LEFT, True)
		time.sleep(0.00001)
		GPIO.output(TRIG_LEFT, False)
		while GPIO.input(ECHO_LEFT)==0:
			pulse_start = time.time()
		while GPIO.input(ECHO_LEFT)==1:
			pulse_end = time.time()
		pulse_duration = pulse_end - pulse_start
		distance = pulse_duration * 17150
		distance = (round(distance, 2)) / 100
		#rospy.loginfo(str(distance))
		pub_left.publish(distance)

		GPIO.output(TRIG_RIGHT, True)
		time.sleep(0.00001)
		GPIO.output(TRIG_RIGHT, False)
		while GPIO.input(ECHO_RIGHT)==0:
			pulse_start = time.time()
		while GPIO.input(ECHO_RIGHT)==1:
			pulse_end = time.time()
		pulse_duration = pulse_end - pulse_start
		distance = pulse_duration * 17150
		distance = (round(distance, 2)) / 100
		rospy.loginfo(str(distance))
		pub_right.publish(distance)
		rate.sleep()

if __name__ == '__main__':
	try:
		talker()
	except rospy.ROSInterruptException:
		pass
	finally:
		print("\nGPIO.cleanup")
		GPIO.cleanup()
