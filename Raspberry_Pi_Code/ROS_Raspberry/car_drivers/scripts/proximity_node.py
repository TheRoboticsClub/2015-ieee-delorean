#!/usr/bin/env python

import time
import RPi.GPIO as GPIO
import rospy
from std_msgs.msg import Bool

GPIO.setmode(GPIO.BOARD)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def my_callback(channel):
    print "Proximity detected"
    msg = Bool()
    msg.data = True
    publisher.publish(msg)



GPIO.add_event_detect(24, GPIO.RISING, callback=my_callback, bouncetime=300)


try:
    rospy.init_node('proximity_node', anonymous=True)
    global publisher
    publisher = rospy.Publisher('/proximity_alert', Bool, queue_size=10)
    rospy.spin()

except KeyboardInterrupt:
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit
GPIO.cleanup()           # clean up GPIO on normal exit
