#!/usr/bin/env python

import rospy
from std_msgs.msg import String
import sys
from geometry_msgs.msg import Twist
import os
import time


def ping_controller():
    
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    rospy.init_node('range_test_control', anonymous=True)
    while not rospy.is_shutdown():
        time.sleep(1)

if __name__ == '__main__':
    try:
        ping_controller()
    except rospy.ROSInterruptException:
        pass
