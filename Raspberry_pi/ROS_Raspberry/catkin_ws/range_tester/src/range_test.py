#!/usr/bin/env python

import rospy
from std_msgs.msg import String
import sys
from geometry_msgs.msg import Twist
import os

'''
def ping_controller():
    
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    rospy.init_node('range_test', anonymous=True)
    os.system('rosnode ping serial_node')
    print('he perdido la conexion con el nodo!!!!')
'''

if __name__ == '__main__':
    try:
        #ping_controller()
        print('hola')
    except rospy.ROSInterruptException:
        pass
