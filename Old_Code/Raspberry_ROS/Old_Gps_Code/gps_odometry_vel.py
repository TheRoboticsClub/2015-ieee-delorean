import rospy
from sensor_msgs.msg import NavSatFix
import time
import calendar
import threading
import math
from geometry_msgs.msg import TwistStamped
from std_msgs.msg import String


class velData:


    def __init__(self):

        self.Xvector = 0
        self.Yvector = 0
        self.oldTime = calendar.timegm(time.gmtime())
        self.currentTime = calendar.timegm(time.gmtime())
        self.dt = 0


def velCallback(data, vel):

    #rospy.loginfo(fix)
    vel.Xvector = data.twist.linear.x
    vel.Yvector = data.twist.linear.y


def getCompass(angle):

    if(angle >= 0 and angle < 45):
        print('this program is heading to the North!')

    else if(angle >= 45 and angle < 90):
        print('this program is heading to the NorthEast!')

    else if(angle >= 90 and angle < 135):
        print('this program is heading to the SouthEast!')

    else if(angle >= 135 and angle < 180):
        print('this program is heading to the South!')

    else if(angle >= 180 and angle < 225):
        print('this program is heading to the SouthWest!')

    else if(angle >= 225 and angle < 270):
        print('this program is heading to the West!')

    else if(angle >= 270 and angle < 315):
        print('this program is heading to the NorthWest!')

    else if(angle >= 315 and angle < 360):
        print('this program is heading to the North!')

    else:
        print('unknown orientation:', angle)


def computeHeading(vel, pub):

    print('x speed vector is', vel.Xvector)
    print('y speed vector is', vel.Yvector)
    xVel = vel.Xvector
    yVel = vel.Yvector

    relativeAngle = math.atan(yVel/xVel)

    if(relativeAngle => 0 and relativeAngle <= 135):
        print('the angle is between 0 and 135 degrees')
        mappedAngle = (-1)*relativeAngle + 135

    else if(relativeAngle > 135 and relativeAngle <= 315):
        print('the angle is between 135 and 315 degrees')
        mappedAngle = (-1)*relativeAngle + 495

    else:
        print('unknown angle')

    print(mappedAngle)
    getCompass(mappedAngle)
    velMsg = String()
    velMsg.data = mappedAngle
    pub.publish(velMsg)
    time.sleep(1)


if __name__ == '__main__':

    vel = velData()
    rospy.Subscriber('/vel', TwistStamped, velCallback, vel)
    pub = rospy.publisher('/gps/heading', String, queue_size=10)
    t = threading.Thread(target=computeHeading, args=(vel,pub))
    t.daemon = True
    t.start()
    rospy.spin()
