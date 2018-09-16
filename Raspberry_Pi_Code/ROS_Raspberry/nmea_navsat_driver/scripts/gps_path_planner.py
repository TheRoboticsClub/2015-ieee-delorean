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
    #print('----------------------------------------')
    #print('Im at: ', lat1, lon1, 'And the distence to', lat2, lon2, 'is', d)
    #print('----------------------------------------')
    return (d)


def twistVehicle(distance, orientation, steeringParameter):

    steeringValue = 0.5
    throttleValue = 0.5417

    if(orientation >= 0 and orientation < 26.56):
        steeringValue = (((orientation-0.0)*0.5)/MAXSTEERING) + 0.5
        print('steering to the right')

    elif(orientation > 26.56):
        steeringValue = 1.0 - steeringParameter

    elif(orientation > -26.56 and orientation < 0):
        steeringValue = ((orientation+MAXSTEERING)*0.5/MAXSTEERING) + 0.0
        print('steering to the left')

    elif(orientation < -26.56):
        steeringValue = 0.0 + steeringParameter

    moveMsg = Twist()
    moveMsg.angular.z = steeringValue
    moveMsg.linear.x = throttleValue
    pub.publish(moveMsg)


def getBearing():

    print('test')



def fixCallback(data, args):

    goalLatitude = args[0]
    goalLongitude = args[1]
    gps_data = args[2]
    gps_data.currentLatitude = data.latitude
    gps_data.currentLongitude = data.longitude
    orientation = args[3].orientation
    steeringParameter = args[4]

    (points_distance) = getDistance(float(gps_data.currentLongitude), float(goalLongitude), float(gps_data.currentLatitude), float(goalLatitude))
    (points_bearing) = getBearing()

    print('Point to point distance:', points_distance)
    print('Angle from car to North Pole:', orientation)

    if(points_distance < 5):
        print('you arrived at your destination!')
        stopCar()

    else:
        twistVehicle(points_distance, orientation, steeringParameter)


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
    #print compass.orientation

def startRoutine():

    moveMsg = Twist()
    moveMsg.angular.z = 0.0
    moveMsg.linear.x = 0.54
    pub.publish(moveMsg)


if __name__ =='__main__':

    goalLatitude = sys.argv[1]
    goalLongitude = sys.argv[2]
    steeringParameter = sys.argv[3]
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
    FixcallbackArguments = [goalLatitude, goalLongitude, gps, compass, steeringParameter]
    rospy.Subscriber('/arduino/compass', Float32, compassCallback, compass)
    time.sleep(2)
    rospy.Subscriber('/fix', NavSatFix, fixCallback, FixcallbackArguments)
    rospy.spin()
    rospy.on_shutdown(stopCar)
