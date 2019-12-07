import time
import picamera

def camera(cnt):
    camera = picamera.PiCamera()
    camera.resolution = (800,600)
    camera.capture("ex"+str(cnt)+".jpg")
    camera.close()
