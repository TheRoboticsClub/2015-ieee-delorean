#! /usr/bin/env python


import rospy
from std_msgs.msg import String
from sensor_msgs.msg import NavSatFix
from geometry_msgs.msg import Twist
import time

gps_localizations = [(40.2327416667, -3.74915),(40.232850, -3.749118
),(40.233082, -3.749074
),(40.233425, -3.748955
),(40.233765, -3.748826
), (40.234029, -3.748721
), (40.234275, -3.748659
)]

def talker():
    pub = rospy.Publisher('gps/fix', NavSatFix, queue_size=10)
    rospy.init_node('fake_gps', anonymous=True)

    pub2 = rospy.Publisher('vel', Twist, queue_size=10)

    rate = rospy.Rate(2) # 10hz
    loc_index = 0
    while not rospy.is_shutdown():
        #print(loc_index)
        fake_localization = NavSatFix()
        fake_vel = Twist()
        #fake_vel.frame_id = "/gps"
        #fake_localization.header.stamp = time.time()
        fake_localization.header.frame_id = '/gps'
        fake_localization.status.status = 1
        fake_localization.status.service = 1
        #print(gps_localizations[loc_index][0], gps_localizations[loc_index][1])
        fake_localization.latitude = gps_localizations[loc_index][0]
        fake_localization.longitude = gps_localizations[loc_index][1]
        print(fake_localization.latitude, fake_localization.longitude)
        fake_localization.altitude = 0.0
        fake_localization.position_covariance = [1.3224999999999998, 0.0, 0.0, 0.0, 1.3224999999999998, 0.0, 0.0, 0.0, 5.289999999999999]
        fake_localization.position_covariance_type = 1
        #fake_vel.header.frame_id = "/gps"
        pub.publish(fake_localization)
        pub2.publish(fake_vel)
        if(loc_index == len(gps_localizations)-1):
            loc_index = 0
        else:
            loc_index = loc_index + 1
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
