#!/usr/bin/env python

from pykml import parser
import os
import re
import sys

path = sys.argv[1]

with open(path) as f:

    doc = parser.parse(f).getroot()


raw_data =  doc.Document.Placemark.LineString.coordinates.text
raw_data = raw_data.replace("\t", "").replace("\n", "").replace(",0", "")
raw_data = re.split(",| ", raw_data)
del raw_data[len(raw_data)-1]

#print raw_data

index = 0

for i in range(0, len(raw_data)/2):

    print 'rosrun nmea_navsat driver ' +  raw_data[index+1] + ' ' +  raw_data[index] + ' 0' + ' 0'
    #os.sys('rosrun nmea_navsat driver ' +  raw_data[index+1] + ' ' +  raw_data[index] + ' 0' + ' 0')
    print 'The car reached the waypoint' + ' ' + str(i)
    index = index+2

print 'The car has completed the route'
