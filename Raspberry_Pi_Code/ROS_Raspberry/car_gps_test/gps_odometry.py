#!/usr/bin/env python

import rospy
from sensor_msgs.msg import NavSatFix
import time
import calendar
import threading
import math


class gpsData:


    def __init__(self):

        self.oldLatitude = 0
        self.oldLongitude = 0
        self.currentLatitude = 0
        self.currentLongitude = 0
        self.oldTime = calendar.timegm(time.gmtime())
        self.currentTime = calendar.timegm(time.gmtime())
        self.dt = 0


def fixCallback(fix, gps):

    #rospy.loginfo(fix)
    gps.currentLatitude = fix.latitude
    gps.currentLongitude = fix.longitude

def computeHeading(gps, dLat, dLong):

    latA = gps.oldLatitude
    latB = gps.currentLongitude
    longA = gps.oldLongitude
    longB = gps.currentLongitude

    x = math.cos(latB) * math.sin(dLong)
    y = math.cos(latA) * math.sin(latB) - math.sin(latA) * math.cos(latB)*math.cos(dLong)
    bearing = math.atan2(x, y)
    print('bearing is', bearing)


def positionDifference(gps):

    while True:
        dLat = gps.currentLatitude - gps.oldLatitude
        dLong = gps.currentLongitude - gps.oldLongitude

        gps.oldLatitude = gps.currentLatitude
        gps.oldLongitude = gps.currentLongitude

        computeHeading(gps, dLat, dLong)

        time.sleep(1)


if __name__ == '__main__':

    gps = gpsData()
    rospy.init_node('gps_odom_node', anonymous=True)
    rospy.loginfo('GPS fixes reader initialized')
    rospy.Subscriber('/gps/fix', NavSatFix, fixCallback, gps)
    t = threading.Thread(target=positionDifference, args=(gps,))
    t.daemon = True
    t.start()
    rospy.spin()
