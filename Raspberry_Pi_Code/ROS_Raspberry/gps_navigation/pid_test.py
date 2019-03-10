#!/usr/bin/env python

import rospy
import time
from simple_pid import PID
from std_msgs.msg import Float32


def ping_sender(number):

    while True:
        hello_str = 'ping!'
        #rospy.loginfo(hello_str)
        pubping.publish(hello_str)
        time.sleep(1)


def speed_sensor_callback(data, pid):

    speed = data.data
    pid_output = pid(speed)
    Msg = Float32()
    Msg.data = pid_output
    pub.publish(Msg)



if __name__ =='__main__':


    global pub
    pub = rospy.Publisher('/pid/pid_output', Float32, queue_size=10)

    pid = PID(1, 0.1, 0.05, setpoint = 1.4)
    pid.output_limits = (0.5, 0.55)
    rospy.Subscriber('/arduino/speed', Float32, speed_sensor_callback, pid)

    rospy.spin()
