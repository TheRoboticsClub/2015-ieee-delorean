#!/usr/bin/env python

import rospy
from sensor_msgs.msg import NavSatFix
import time
import calendar
import threading
import math

R = 6378100

class gpsData:

    def __init__(self):

        self.oldLatitude = 0
        self.oldLongitude = 0
        self.currentLatitude = 0
        self.currentLongitude = 0


def computeBearing(lon1, lon2, lat1, lat2):

    φ1 = math.radians(lat1)
    φ2 = math.radians(lat2)
    Δφ = math.radians(lat2-lat1)
    Δλ = math.radians(lon2-lon1)

    a = math.sin(Δφ/2) * math.sin(Δφ/2) + math.cos(φ1) * math.cos(φ2) * math.sin(Δλ/2) * math.sin(Δλ/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c

    print('distance is:', d)

    λ1 = math.radians(lon1)
    λ2 = math.radians(lon2)

    y = math.sin(λ2-λ1) * math.cos(φ2)
    x = math.cos(φ1)*math.sin(φ2) - math.sin(φ1)*math.cos(φ2)*math.cos(λ2-λ1)
    brng = math.degrees(math.atan2(y, x))

    print('bearing is:', brng)


def fixCallback(fix, gps):

    #rospy.loginfo(fix)
    gps.currentLatitude = fix.latitude
    gps.currentLongitude = fix.longitude


if __name__ =='__main__':

    gps = gpsData()
    rospy.init_node('gps_odom_node', anonymous=True)
    rospy.loginfo('GPS fixes reader initialized')
    rospy.Subscriber('/gps/fix', NavSatFix, fixCallback, gps)
    #t = threading.Thread(target=positionDifference, args=(gps,))
    #t.daemon = True
    #t.start()
    lat1 = float(raw_input('Lat1: '))
    lon1 = float(raw_input('Long1: '))
    lat2 = float(raw_input('Lat2: '))
    lon2 = float(raw_input('Long2: '))
    computeBearing(lon1, lon2, lat1, lat2)
    rospy.spin()
