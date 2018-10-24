#!/usr/bin/env python

import rospy
from sensor_msgs.msg import NavSatFix
from std_msgs.msg import String
from std_msgs.msg import Float32
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

        self.distance = 0
        self.currentLatitude = 0
        self.currentLongitude = 0
        self.oldLatitude = 0
        self.oldLongitude = 0

class compassObject:

    def __init__(self):

        self.orientation = 0


def getDistance(lon1, lon2, lat1, lat2, orientation):


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

    #This next code is to calculate the points angle

    #lon1 is currentLongitude, lon2 is goalLongitude, lat1 is currentLatitude and lat2 is goalLatitude

    targetLong = lon2
    currentLong = lon1
    targetLat = lat1
    currentLat = lat2

    dlon = math.radians(targetLong-currentLong)
    cLat = math.radians(currentLat)
    tLat = math.radians(targetLat)
    a1 = math.sin(dlon) * math.cos(tLat)
    a2 = math.sin(cLat) * math.cos(tLat) * math.cos(dlon)
    a2 = math.cos(cLat) * math.sin(tLat) - a2
    a2 = math.atan2(a1, a2)
    if (a2 < 0.0):
        a2 += (math.pi)*2

    targetHeading = math.degrees(a2)
    TwoPointAngle = targetHeading - orientation

    return (d, TwoPointAngle)


def twistVehicle(orientation, steeringParameter, tparameter):


    if(orientation <= 5 or orientation >= 355):
        steeringValue = 0.5
        print "Going straight"

    elif(orientation > 0 and orientation < 180):
        Left =(orientation*0.5)/90
        steeringValue = 0.35 - Left - float(steeringParameter) #left
        if(steeringValue < 0.2):
            sterringValue = 0.2

        print "Going left",steeringValue
        #print Left

    elif(orientation >= 180 and orientation < 360):
        Right = ((orientation-360)*0.5)/(270-360)
        steeringValue = 0.65 + Right + float(steeringParameter) #right
        if(steeringValue > 0.8):
            steeringValue = 0.8

        print "Going right",steeringValue
        #print Right

    else:
        steeringValue = 0.5
        #print "Going straight"

    throttleValue = 0.547 + float(tparameter)
    moveMsg = Twist()
    moveMsg.angular.z = steeringValue
    moveMsg.linear.x = throttleValue
    pub.publish(moveMsg)



def fixCallback(data, args):


    orientation = args[0].orientation
    steeringParameter = args[1]
    tparameter = args[2]
    twistVehicle(orientation, steeringParameter, tparameter)


def stopCar():

    stopMsg = Twist()
    stopMsg.linear.x = 0.5
    stopMsg.angular.z = 0.5
    pub.publish(stopMsg)
    print('stopping car!')


def ping_sender(number):

    while True:
        hello_str = 'ping!'
        #rospy.loginfo(hello_str)
        pubping.publish(hello_str)
        time.sleep(1)


def compassCallback(data, compass):


    compass.orientation = data.data
    compass.orientation = math.radians(compass.orientation - 0.011)
    if(compass.orientation < 0):
        compass.orientation = compass.orientation + 2*math.pi

    if(compass.orientation > 2*math.pi):
        compass.orientation = compass.orientation - 2*math.pi



    compass.orientation = math.degrees(compass.orientation)

    #print "North:", compass.orientation

def startRoutine():

    moveMsg = Twist()
    moveMsg.angular.z = 0.5
    moveMsg.linear.x = 0.54
    pub.publish(moveMsg)
    time.sleep(1)


if __name__ =='__main__':

    try:
        steeringParameter = sys.argv[1]
	tparameter = sys.argv[2]
        gps = gpsData()
        compass = compassObject()

        rospy.init_node('go_north', anonymous=True)
        global pubping
        pubping = rospy.Publisher('/ping', String, queue_size=10)
        t = threading.Thread(target=ping_sender, args=(0,))
        t.daemon = True
        t.start()
        global pub
        pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
        startRoutine()
        FixcallbackArguments = [compass, steeringParameter, tparameter]
        rospy.Subscriber('/arduino/compass', Float32, compassCallback, compass)
        time.sleep(1)
        rospy.Subscriber('/fix', NavSatFix, fixCallback, FixcallbackArguments)
        rospy.spin()
        rospy.on_shutdown(stopCar)

    except IndexError:

        print "Usage: goalLatitude goalLongitude steeringAdjustValue"
