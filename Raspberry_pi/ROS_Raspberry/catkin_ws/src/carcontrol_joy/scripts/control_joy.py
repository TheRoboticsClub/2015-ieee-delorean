#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
from bondpy import bondpy
import os
import sys

# Author: Andrew Dai
# This ROS Node converts Joystick inputs from the joy node
# into commands for turtlesim

# Receives joystick messages (subscribed to Joy topic)
# then converts the joysick inputs into Twist commands
# axis 1 aka left stick vertical controls linear speed
# axis 0 aka left stick horizonal controls angular speed

def formed():
    print "Bonded with car node"


def broken():
    print "Lost connection with car node"

def mapping(axis):
    
    aux_axis = 0.5
    
    if axis >= 0.0:
        aux_axis = abs((axis/2.0) + 0.5)
        if aux_axis >= 1.0:
            return 1.0

        else:
            return aux_axis
            
    else:
        aux_axis = abs((abs(axis)/2.0) - 0.5)
        if aux_axis <= 0.0:
            return 0.0
        else:
            return aux_axis


def callback(data):
    twist = Twist()

    twist.linear.x = mapping(data.axes[3])
    twist.angular.z = mapping(-data.axes[0])
    rospy.loginfo(twist)
    pub.publish(twist)

# Intializes everything
def start():
    # publishing to "turtle1/cmd_vel" to control turtle1
    global pub
    pub = rospy.Publisher('/arduino/cmd_vel', Twist, queue_size=10)
    # subscribed to joystick inputs on topic "joy"
    rospy.Subscriber("joy", Joy, callback)
    # starts the node
    rospy.init_node('Joy2Turtle')
    b = bondpy.Bond("car_controller_heartbeat","bond_1", on_broken=broken, on_formed=formed)
    b.start()
    rospy.spin()

if __name__ == '__main__':
    start()
    
