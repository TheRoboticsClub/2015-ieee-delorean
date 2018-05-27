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
