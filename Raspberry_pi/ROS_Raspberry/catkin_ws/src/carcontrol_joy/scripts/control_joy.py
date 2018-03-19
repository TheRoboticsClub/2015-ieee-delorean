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

def mapsteering(axis):
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



def mapthrottle(axis, currentgear):
    aux_axis = 0.5

    if axis >= 0.0:
        aux_axis = abs((axis/2.0) + 0.5)

        if currentgear == 0:
            if aux_axis < 0.6:
                return aux_axis
            else:
                return 0.6

        elif currentgear == 1:
            if aux_axis < 0.65:
                return aux_axis
            else:
                return 0.65

        elif currentgear == 2:
            if aux_axis < 0.7:
                return aux_axis
            else:
                return 0.7

        else:
            if aux_axis >= 1.0:
                return 1.0

            else:
                return aux_axis

    else
        if currentgear == 0:
            if aux_axis < 0.4:
                return aux_axis
            else:
                return 0.4

        elif currentgear == 1:
            if aux_axis < 0.35:
                return aux_axis
            else:
                return 0.35

        elif currentgear == 2:
            if aux_axis < 0.3:
                return aux_axis
            else:
                return 0.3

        else:
            if aux_axis <= 0.0:
                return 0.0

            else:
                return aux_axis


def changegear(data, buttonstate):

    geardown = data.buttons[10]
    gearup = data.buttons[11]

    if gearup == 1 and buttonstate.r1 == 0 and buttonstate.currentgear < 3:
        rospy.loginfo('boton pulsado')
        buttonstate.r1 = 1
        buttonstate.currentgear += 1

    elif gearup == 0 and buttonstate.r1 == 1:
        rospy.loginfo('devuelvo el boton a 0')
        buttonstate.r1 = 0


    if geardown == 1 and buttonstate.l1 == 0 and buttonstate.currentgear > 0:
        rospy.loginfo('boton pulsado')
        buttonstate.l1 = 1
        buttonstate.currentgear -= 1

    elif geardown == 0 and buttonstate.l1 == 1:
        rospy.loginfo('devuelvo el boton a 0')
        buttonstate.l1 = 0


    rospy.loginfo(buttonstate.currentgear)

def callback(data, buttonstate):

    changegear(data, buttonstate)
    twist = Twist()
    twist.linear.x = mapthrottle(data.axes[3], buttonstate.currentgear)
    twist.angular.z = mapsteering(-data.axes[0])
    rospy.loginfo(twist)
    pub.publish(twist)

# Intializes everything
def start():
    # publishing to "turtle1/cmd_vel" to control turtle1
    global pub
    pub = rospy.Publisher('/arduino/cmd_vel', Twist, queue_size=10)
    # subscribed to joystick inputs on topic "joy"

    class button:
        l1 = 0
        r1 = 0
        currentgear = 0


    buttonstate = button()
    buttonstate.r1 = 0
    buttonstate.l1 = 0
    buttonstate.currentgear = 0
    rospy.Subscriber("joy", Joy, callback, buttonstate)
    # starts the node
    rospy.init_node('Joy2Turtle')
    b = bondpy.Bond("car_controller_heartbeat","bond_1", on_broken=broken, on_formed=formed)
    b.start()
    rospy.spin()

if __name__ == '__main__':

    start()
