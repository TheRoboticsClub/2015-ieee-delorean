#!/usr/bin/env python

from pykml import parser
from lxml import etree
import sys
import rospy
from sensor_msgs.msg import NavSatFix

#ros necessary declarations

initFile()
rospy.init_node('car_path_logger', anonymous=True)
rospy.subscriber('/fix', NavSatFix, append_fix)

def initFile():

    tree = etree.parse("car_real_path.kml")
    root = tree.getroot()

    #initialize the document
    for Document in root:
        for Placemark in Document:
            for LineString in Placemark:
                for coordinates in LineString:
                    raw_coordinates = coordinates.text
                    coordinates.text = "\n\t\t\t"

    tree = etree.ElementTree(root)
    tree.write('car_real_path.kml', xml_declaration=True)


def append_fix(data):

    new_longitude = data.longitude
    new_latitude = data.latitude

    tree = etree.parse("car_real_path.kml")
    root = tree.getroot()

    for Document in root:
        for Placemark in Document:
            for LineString in Placemark:
                for coordinates in LineString:
                    raw_coordinates = coordinates.text
                    coordinates.text = coordinates.text + " \t" + new_coordinates + "\n\t\t\t"

    tree = etree.ElementTree(root)
    tree.write('car_real_path.kml', xml_declaration=True)


rospy.spin()
