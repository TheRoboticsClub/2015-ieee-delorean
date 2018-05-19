#!/usr/bin/env python

import rospy
from bondpy import bondpy
from std_msgs.msg import String
import sys
from geometry_msgs.msg import Twist

def formed():
    print "Bonded with controller node"


def broken():
    print "Lost connection with controller node"
    stop_msg = Twist()
    stop_msg.linear.x = 0.5
    stop_msg.angular.z = 0.5
    pub.publish(stop_msg)


def callback(data):
    rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data)
    pub.publish(data)


def listener():
    global pub
    pub = rospy.Publisher('/arduino/cmd_vel', Twist, queue_size=10)
    rospy.init_node('controlteclas', anonymous=True)
    rospy.Subscriber('/turtle1/cmd_vel', Twist, callback)
    b = bondpy.Bond("car_controller_heartbeat","bond_1", on_broken=broken, on_formed=formed)
    b.start()
    rospy.spin()


if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
