#!/usr/bin/env python

import rospy
from geometry_msgs.msg import TwistStamped
from simple_pid import PID
import math


class velClass:

    def __init__(self):

        self.speed = 0
        self.old_value = 0
        self.current_value = 0


def callback(data, vel):

    x = data.twist.linear.x
    y = data.twist.linear.y
    actual_speed = math.sqrt((x^2) + (y^2))
    print actual_speed





if __name__ =='__main__':

    pid = PID(1, 0.1, 0.05)
    pid.setpoint = 0.55
    pid.sample_time = 1  # update every 1 second
    pid.output_limits = (0.547, 0.556)

    rospy.init_node('vel_test', anonymous=True)
    velobj = velClass()
    rospy.Subscriber('/arduino/compass', Float32, callback, velobj)
    rospy.spin()
