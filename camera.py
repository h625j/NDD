import time
import picamera
import web



def camera(cnt):
    camera = picamera.PiCamera()
    camera.resolution = (800,600)
    camera.capture("static/"+"img.jpg")
    time.sleep(1)
    camera.close()
