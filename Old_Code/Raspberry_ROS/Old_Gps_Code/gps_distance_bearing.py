#!/usr/bin/env python

import rospy
from sensor_msgs.msg import NavSatFix
from std_msgs.msg import String
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

    #print(lat1, lon1, lat2, lon2)
    phi_1 = math.radians(lat1)
    phi_2 = math.radians(lat2)
    phi_delta = math.radians(lat2-lat1)
    landa_delta = math.radians(lon2-lon1)

    a = math.sin(phi_delta/2) * math.sin(phi_delta/2) + math.cos(phi_1) * math.cos(phi_2) * math.sin(landa_delta/2) * math.sin(landa_delta/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c
    print('---------------------')
    print('distance is:', d)

    landa_1 = math.radians(lon1)
    landa_2 = math.radians(lon2)

    y = math.sin(landa_2-landa_1) * math.cos(phi_2)
    x = math.cos(phi_1)*math.sin(phi_2) - math.sin(phi_1)*math.cos(phi_2)*math.cos(landa_2-landa_1)
    brng = math.degrees(math.atan2(y, x))

    print('bearing is:', brng)
    print('--------------------')

    return (brng, d)


def fixCallback(data, gps):

    #rospy.loginfo(data)
    gps.currentLatitude = data.latitude
    gps.currentLongitude = data.longitude
    (bearing, distance) = computeBearing(gps.oldLongitude, gps.currentLongitude, gps.oldLatitude, gps.currentLatitude)
    msg = String()
    msg.data = str(distance)
    distance_pub.publish(msg)
    msg.data = str(bearing)
    bearing_pub.publish(msg)
    gps.oldLatitude = data.latitude
    gps.oldLongitude = data.longitude


if __name__ =='__main__':

    gps = gpsData()
    rospy.init_node('gps_odom_node', anonymous=True)
    rospy.loginfo('GPS fixes reader initialized')
    global bearing_pub
    global distance_pub
    bearing_pub = rospy.Publisher('/gps/bearing', String, queue_size=10)
    distance_pub = rospy.Publisher('/gps/distance', String, queue_size=10)
    rospy.Subscriber('/gps/fix', NavSatFix, fixCallback, gps)
    #t = threading.Thread(target=positionDifference, args=(gps,))
    #t.daemon = True
    #t.start()
    #lat1 = float(raw_input('Lat1: '))
    #lon1 = float(raw_input('Long1: '))
    #lat2 = float(raw_input('Lat2: '))
    #lon2 = float(raw_input('Long2: '))
    #computeBearing(lon1, lon2, lat1, lat2)
    rospy.spin()
