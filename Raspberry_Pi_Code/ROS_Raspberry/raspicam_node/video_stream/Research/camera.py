#!/usr/bin/env python

import picamera
import numpy as np

def record_video(hresolution, vresolution, framerate, duration, format, file_name):

	with picamera.PiCamera() as camera:

		camera.resolution = (hresolution, vresolution)
		camera.framerate = framerate
		camera.start_recording(file_name, format)
		camera.wait_recording(duration)
		camera.stop_recording()

if __name__== "__main__":

	print("Horizonal resolution")
	hresolution = int(raw_input())
	print("Vertical resolution")
	vresolution = int(raw_input())
	print("Time resolution")
	framerate = int(raw_input())
	print("Video duration")
	duration = int(raw_input())
	print("format")
	format = raw_input()
	print("File name")
	file_name = raw_input()
	record_video(hresolution, vresolution, framerate, duration, format, file_name)
	
