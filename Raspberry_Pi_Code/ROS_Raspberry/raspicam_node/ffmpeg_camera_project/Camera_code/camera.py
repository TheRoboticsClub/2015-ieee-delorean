#!/usr/bin/env python

import picamera
import numpy as np

with picamera.PiCamera() as camera:

	camera.resolution = (720, 576)
	camera.framerate = 30
	camera.start_recording('test.yuv', 'yuv')
	camera.wait_recording(10)
	camera.stop_recording()
