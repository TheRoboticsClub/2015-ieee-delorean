#!/usr/bin/env python

import rospy
from std_msgs.msg import String
import sys
from geometry_msgs.msg import Twist
import os
import rosnode

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data)
    pub.publish(data)

def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('watch_dog', anonymous=True)
    global pub
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    rospy.Subscriber('/turtle1/watch_dog', Twist, callback)
    # spin() simply keeps python from exiting until this node is stopped
    found = True
    while found:
        lista_nodos = rosnode.get_node_names()
        if any('teclado' in s for s in lista_nodos):
            found = True

        else:
            found = False
            stop_msg = Twist()
            stop_msg.linear.x = 0.5
            stop_msg.angular.z = 0.5
            pub.publish(stop_msg)
    
    print('lost connetion with controller node')
        
    #rospy.spin()

if __name__ == '__main__':
    listener()
