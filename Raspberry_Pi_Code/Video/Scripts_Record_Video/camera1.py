##
import os
from io import BytesIO
from time import sleep
import datetime as dt
from picamera import PiCamera

camera = PiCamera()
##constants

destination = '/home/miguel/Vídeos'


def cameraSettings():
    camera.resolution = (1280, 720)
    camera.video_stabilization = True


def record():
    filename = os.path.join(destination, dt.datetime.now().strftime('%Y-%m-%d_%H.%M.%S.h264'))
    camera.start_recording(filename, format='h264', quality = 10)

def stopRecord():
    camera.stop_recording(splitter_port = 1)

if __name__ == '__main__':
    ##camera = PiCamera()
    cameraSettings()
    record()
    sleep(30)
    stopRecord()
