#!/usr/bin/env python

import rospy
from sensor_msgs.msg import NavSatFix
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist
import time
import calendar
import threading
import math
import sys

R = 6378100

class compassObject:

    def __init__(self):

        self.orientation = 0
        self.currentLatitude = 0
        self.currentLongitude = 0
        self.oldLatitude = 0
        self.oldLongitude = 0


def getOrientation(lat1, lon1, lat2, lon2):

    phi_1 = math.radians(lat1)
    phi_2 = math.radians(lat2)
    phi_delta = math.radians(lat2-lat1)
    landa_delta = math.radians(lon2-lon1)

    landa_1 = math.radians(lon1)
    landa_2 = math.radians(lon2)

    y = math.sin(landa_2-landa_1) * math.cos(phi_2)
    x = math.cos(phi_1)*math.sin(phi_2) - math.sin(phi_1)*math.cos(phi_2)*math.cos(landa_2-landa_1)
    orientation = math.degrees(math.atan2(y, x))

    return orientation


def fixCallback(data, args):

    compass = args[0]
    compassMsg = args[1]
    currentLatitude = data.latitude
    currentLongitude = data.longitude
    oldLatitude = compass.oldLatitude
    oldLongitude = compass.oldLongitude

    orientation = getOrientation(currentLatitude, currentLongitude, oldLatitude, oldLongitude)

    compass.oldLatitude = currentLatitude
    compass.oldLongitude = currentLongitude

    compassMsg.data = orientation
    rospy.loginfo(compassMsg)
    compassPub.publish(compassMsg)


if __name__ =='__main__':

    compass = compassObject()
    compassMsg = Float32()
    rospy.init_node('gps_compass', anonymous=True)
    rospy.Subscriber('/gps/fix', NavSatFix, fixCallback, (compass, compassMsg))
    global compassPub
    compassPub = rospy.Publisher('/gps/compass', Float32, queue_size=10)
    rospy.spin()
