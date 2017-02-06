# -*- coding: utf-8 -*-

import picamera
import threading
import time
import datetime as dt

from logging import getLogger
logger = getLogger(__name__)

from config import CONFIG

def worker(camera, filename, lock):
    try:
        camera.start_recording(filename, quality=30, resize=(640, 480))
        camera.wait_recording(5)
        camera.stop_recording()
    finally:
        lock.release()
    
class VideoCapture(object):
    def __init__(self):
        self.lock = threading.Lock()
        self.camera = picamera.PiCamera(resolution=(640, 480), framerate=10)

    def capture(self):
        if self.lock.acquire(False):
            now = dt.datetime.now()
            timestamp = now.strftime("%s")
            filename = 'videos/capture-{}.mjpeg'.format(timestamp)
            logger.info('Start recording to {}'.format(filename))
            t = threading.Thread(target=worker, args=(self.camera, filename, self.lock))
            t.start()
        else:
            logger.debug('Camera already in recording')
    
if __name__ == "__main__":
    vc = VideoCapture()
    vc.capture()
    time.sleep(2)
    vc.capture()
    time.sleep(6)
    vc.capture()
