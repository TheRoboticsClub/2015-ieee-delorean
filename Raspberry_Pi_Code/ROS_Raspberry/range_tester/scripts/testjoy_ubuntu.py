#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
from std_msgs.msg import String
from bondpy import bondpy
import os
import sys
import time
import threading


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
            if aux_axis < 0.5417:
                return aux_axis
            else:
                return 0.5417

        elif currentgear == 1:
            if aux_axis < 0.56:
                return aux_axis
            else:
                return 0.56

        elif currentgear == 2:
            if aux_axis < 0.60:
                return aux_axis
            else:
                return 0.60

        else:
            if aux_axis >= 1.0:
                return 1.0

            else:
                return aux_axis

    else:

        aux_axis = abs((axis/2.0) + 0.5)

        if currentgear == 0 and reversegear > 0:
            if aux_axis > 0.48:
                return aux_axis
            else:
                return 0.48

        elif currentgear == 1 and reversegear > 0:
            if aux_axis > 0.46:
                return aux_axis
            else:
                return 0.46

        elif currentgear == 2 reversegear > 0:
                return 0.5

        else:
            if aux_axis <= 0.0:
                return 0.5

            else:
                return aux_axis


def changegear(data, buttonstate):

    geardown = data.buttons[4]
    gearup = data.buttons[5]
    reversegear = data.button[6]

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
    twist.linear.x = mapthrottle(data.axes[4], buttonstate.currentgear)
    twist.angular.z = mapsteering(-data.axes[0])
    rospy.loginfo(twist)
    pub.publish(twist)

def talker():

    class button:
        l1 = 0
        r1 = 0
        currentgear = 0
        reversegear = 0


    buttonstate = button()
    buttonstate.r1 = 0
    buttonstate.l1 = 0
    buttonstate.currentgear = 0
    buttonstate.reversegear = 0
    rospy.Subscriber("joy", Joy, callback, buttonstate)
    rospy.spin()


def ping_sender(number):

    while True:
        hello_str = 'ping!'
        #rospy.loginfo(hello_str)
        pubping.publish(hello_str)
        time.sleep(1)



if __name__ == '__main__':
    try:
        global pubping
        pubping = rospy.Publisher('/ping', String, queue_size=10)
        global pub
        pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
        rospy.init_node('talker', anonymous=True)
        t = threading.Thread(target=ping_sender, args=(0,))
        t.daemon = True
        t.start()
        talker()
    except rospy.ROSInterruptException:
        pass
