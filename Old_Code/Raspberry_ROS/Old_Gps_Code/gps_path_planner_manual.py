#!/usr/bin/env python

import rospy
from sensor_msgs.msg import NavSatFix
from std_msgs.msg import String
from geometry_msgs.msg import Twist
import time
import calendar
import threading
import math
import sys

R = 6378100
MAXSTEERING = 26.56


class gpsData:

    def __init__(self):

        self.bearing = 0
        self.distance = 0
        self.currentLatitude = 0
        self.currentLongitude = 0
        self.oldLatitude = 0
        self.oldLongitude = 0


def getDistance(lon1, lon2, lat1, lat2):


    phi_1 = math.radians(lat1)
    phi_2 = math.radians(lat2)
    phi_delta = math.radians(lat2-lat1)
    landa_delta = math.radians(lon2-lon1)

    a = math.sin(phi_delta/2) * math.sin(phi_delta/2) + math.cos(phi_1) * math.cos(phi_2) * math.sin(landa_delta/2) * math.sin(landa_delta/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c
    #print('----------------------------------------')
    #print('Im at: ', lat1, lon1, 'And the distence to', lat2, lon2, 'is', d)
    #print('----------------------------------------')

    landa_1 = math.radians(lon1)
    landa_2 = math.radians(lon2)

    y = math.sin(landa_2-landa_1) * math.cos(phi_2)
    x = math.cos(phi_1)*math.sin(phi_2) - math.sin(phi_1)*math.cos(phi_2)*math.cos(landa_2-landa_1)
    brng = math.degrees(math.atan2(y, x))

    return (d, brng)


def twistVehicle(distance, bearing):

    if(bearing >= 0 and bearing < 26.56):
        steeringValue = (((bearing-0.0)*0.5)/MAXSTEERING) + 0.5
        print('steering to the right')

    elif(bearing > 26.56):
        steeringValue = 1.0

    elif(bearing > -26.56 and bearing < 0):
        steeringValue = ((bearing+MAXSTEERING)*0.5/MAXSTEERING) + 0.0
        print('steering to the left')

    elif(bearing < -26.56):
        steeringValue = 0.0

    print(steeringValue)


def fixCallback(data, args):

    goalLatitude = args[0]
    goalLongitude = args[1]
    gps_data = args[2]
    currentLatitude = args[3]
    currentLongitude = args[4]
    gps_data.currentLatitude = data.latitude
    gps_data.currentLongitude = data.longitude

    (points_distance, bearing) = getDistance(float(currentLongitude), float(goalLongitude), float(currentLatitude), float(goalLatitude))
    print(points_distance, bearing)

    if(points_distance < 5):
        print('you arrived at your destination!')
        print('orientation is', bearing, 'degrees')

    else:
        twistVehicle(points_distance, bearing)

def hello(pub):
    print('hello')


if __name__ =='__main__':

    goalLatitude = sys.argv[1]
    goalLongitude = sys.argv[2]
    currentLa = sys.argv[3]
    currentLo = sys.argv[4]
    gps = gpsData()

    callbackArguments = [goalLatitude, goalLongitude, gps, currentLa, currentLo]
    rospy.init_node('gps_path_planner', anonymous=True)
    rospy.Subscriber('/gps/fix', NavSatFix, fixCallback, callbackArguments)
    pub = rospy.Publisher('/arduino/cmd_vel', Twist, queue_size=10)
    global stopPub
    stopPub = rospy.Publisher('/arduino/cmd_vel', Twist, queue_size=10)
    #rospy.Subscriber('/gps/distance', NavSatFix, fixCallback)
    #rospy.Subscriber('/gps/bearing', NavSatFix, fixCallback)
    #rospy.Subscriber('/vel', NavSatFix, fixCallback)
    rospy.spin()
    #rospy.on_shutdown(hello)
