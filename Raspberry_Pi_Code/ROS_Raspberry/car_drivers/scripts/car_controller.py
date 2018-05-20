#!/usr/bin/env python

import rospy
from bondpy import bondpy
from std_msgs.msg import String
import sys
from geometry_msgs.msg import Twist
import calendar
import time
import threading

class Timer:


    def __init__(self):
        self.dt = 100
        self.arrived = False
        self.old_time = calendar.timegm(time.gmtime())
        self.time_now = calendar.timegm(time.gmtime())


def ping_verifier(counter):

    while True:
        if(counter.arrived):
            #print('order arrived!')
            counter.old_time = counter.time_now
            counter.arrived = False

        counter.time_now = calendar.timegm(time.gmtime())
        counter.dt = counter.time_now - counter.old_time
        print(counter.dt)
        if(counter.dt >= 3):
            print('stopping car!!!')
            stop_msg = Twist()
            stop_msg.linear.x = 0.5
            stop_msg.angular.z = 0.5
            pub.publish(stop_msg)


        time.sleep(1)


def ping_receiver(data, counter):

    counter.arrived = True


def callback(data):
    rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data)
    pub.publish(data)


def listener(counter):


    rospy.spin()

if __name__ == '__main__':
    counter = Timer()
    global pub
    pub = rospy.Publisher('/arduino/cmd_vel', Twist, queue_size=10)
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("/ping", String, ping_receiver, counter)
    rospy.Subscriber('/turtle1/cmd_vel', Twist, callback)
    t = threading.Thread(target=ping_verifier, args=(counter,))
    t.daemon = True
    t.start()
    listener(counter)
