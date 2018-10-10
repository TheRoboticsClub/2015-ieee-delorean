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


def twistVehicle(orientation, steeringParameter,tparameter):

    
    if(orientation < 180):
        Left = ((orientation-360)*0.2)/(180-360)
        steeringValue = 0.35 - Left #float(steeringParameter) #left
        print "Going left",steeringValue

    elif(orientation > 180):
        Right = (orientation*0.2)/180
        steeringValue = 0.65 + Right #float(steeringParameter) #right
        print "Going right",steeringValue

    else:
        steeringValue = 0.5
        print "Going straight"
    
    throttleValue = 0.547 + tparameter
    moveMsg = Twist()
    moveMsg.angular.z = steeringValue
    moveMsg.linear.x = throttleValue
    pub.publish(moveMsg)



def fixCallback(data, args):

    steeringParameter = args[0]
    tparameter = args[1]
    orientation = args[2].orientation
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
        compass.orientation = compass.orientation - 2*math.py
     
     compass.orientation = math.degrees(compass.orientation)
        
    #print compass.orientation

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

        rospy.init_node('gps_path_planner', anonymous=True)
        global pubping
        pubping = rospy.Publisher('/ping', String, queue_size=10)
        t = threading.Thread(target=ping_sender, args=(0,))
        t.daemon = True
        t.start()
        global pub
        pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
        startRoutine()
        rospy.Subscriber('/arduino/compass', Float32, compassCallback, compass)
        FixcallbackArguments = [steeringParameter, tparameter, compass]
        time.sleep(1)
        rospy.Subscriber('/fix', NavSatFix, fixCallback, FixcallbackArguments)
        rospy.spin()
        rospy.on_shutdown(stopCar)

    except IndexError:

        print "Usage: goalLatitude goalLongitude steeringAdjustValue"
