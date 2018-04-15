#!/usr/bin/python

import time
import picamera
import sys

MODE = sys.argv[1]
NAME = sys.argv[2]



if MODE == "V":

    VIDEO_NAME = NAME  + ".mpeg"
    with picamera.PiCamera() as picam:
        picam.start_preview()
        picam.start_recording(VIDEO_NAME)
        picam.wait_recording(20)
        picam.stop_recording()
        picam.stop_preview()
        picam.close()

elif MODE == "F":


    PHOTO_NAME = NAME  + ".jpeg"

    camara = picamera.PiCamera()

    camara.capture(PHOTO_NAME)

    camara.close()
