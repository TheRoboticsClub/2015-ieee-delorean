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


def getDistance(lon1, lon2, lat1, lat2):


    phi_1 = math.radians(lat1)
    phi_2 = math.radians(lat2)
    phi_delta = math.radians(lat2-lat1)
    landa_delta = math.radians(lon2-lon1)

    a = math.sin(phi_delta/2) * math.sin(phi_delta/2) + math.cos(phi_1) * math.cos(phi_2) * math.sin(landa_delta/2) * math.sin(landa_delta/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c

    return d


def getHeadingError(currentHeading, currentLat, currentLong, targetLat, targetLong):


    dlon = 0
    cLat = 0
    tLat = 0
    a1 = 0
    a2 = 0
    targetHeading = 0
    dlon = math.radians(targetLong-currentLong)
    cLat = math.radians(currentLat)
    tLat = math.radians(targetLat)
    a1 = math.sin(dlon) * math.cos(tLat)
    a2 = math.sin(cLat) * math.cos(tLat) * math.cos(dlon)
    a2 = math.cos(cLat) * math.sin(tLat) - a2
    a2 = math.atan2(a1, a2)
    if (a2 < 0.0):
        a2 = a2 + 2*math.pi

    targetHeading = math.degrees(a2)

    headingError = targetHeading - currentHeading

    return headingError



def twistVehicle(currentHeading, steeringParameter, tparameter):

    if (headingError < -180):
        headingError += 360

    if (headingError > 180):
        headingError -= 360

    if(math.fabs(orientation) <= 5):
        steeringValue = 0.5
        print "Going straight"

    elif(orientation < 0):
        
        Left = (headingError*0.5)/90 #instead of 180 maximum, just testing
        steeringValue = 0.35 - Left - float(steeringParameter) #left
        print "Going left",steeringValue

    elif(orientation > 0):
        Right = ((headingError-360)*0.5)/(270-360) #same as the other
        steeringValue = 0.65 + Right + float(steeringParameter) #right
        print "Going right",steeringValue

    else:
        steeringValue = 0.5
        print "Going straight"

    throttleValue = 0.547 + float(tparameter)
    moveMsg = Twist()
    moveMsg.angular.z = steeringValue
    moveMsg.linear.x = throttleValue
    pub.publish(moveMsg)



def fixCallback(data, args):

    targetLat = args[0]
    targetLong = args[1]
    gps_data = args[2]
    gps_data.currentLatitude = data.latitude
    gps_data.currentLongitude = data.longitude

    currentLat = gps_data.currentLatitude
    currentLong = gps_data.currentLongitude
    currentHeading = args[3].orientation
    steeringParameter = args[4]
    tparameter = args[5]

    points_distance = getDistance(float(currentLong), float(targetLong), float(currentLat), float(targetLat))
    headingError = getHeadingError(currentHeading, currentLat, currentLong, targetLat, targetLong)


    if(points_distance < 5):
        print('you arrived at your destination!')
        stopCar()
        rospy.signal_shutdown("Node stopped because the car reached it's destination")

    else:
        print("")
        print("")
        print("Calculated distance to point:", points_distance)
        print("Calculated heading error to point:", headingError)
        twistVehicle(headingError, steeringParameter, tparameter)
        print("")
        print("")

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
        compass.orientation = compass.orientation - 2*math.py

     compass.orientation = math.degrees(compass.orientation)

    #print compass.orientation

def startRoutine():

    moveMsg = Twist()
    moveMsg.angular.z = 0.5
    moveMsg.linear.x = 0.547
    pub.publish(moveMsg)
    time.sleep(2)


if __name__ =='__main__':

    try:
        goalLatitude = sys.argv[1]
        goalLongitude = sys.argv[2]
        steeringParameter = sys.argv[3]
        tparameter = sys.argv[4]
        gps = gpsData()
        compass = compassObject()

        rospy.init_node('gps_path_planner', anonymous=True)
        global pubping
        pubping = rospy.Publisher('/ping', String, queue_size=10)
        t = threading.Thread(target=ping_sender, args=(0,))
        t.daemon = True
        t.start()
        global pub
        pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
        startRoutine()
        FixcallbackArguments = [goalLatitude, goalLongitude, gps, compass, steeringParameter, tparameter]
        rospy.Subscriber('/arduino/compass', Float32, compassCallback, compass)
        time.sleep(1)
        rospy.Subscriber('/fix', NavSatFix, fixCallback, FixcallbackArguments)
        rospy.spin()
        rospy.on_shutdown(stopCar)

    except IndexError:

        print "Usage: goalLatitude goalLongitude steeringAdjustValue throttleAdjustValue"
