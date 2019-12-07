import RPi.GPIO as GPIO
import time
from camera import *

cnt = 0

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
def tilt():
    global cnt
    if (GPIO.input(20) == True):
        print("기울임!")
        cnt += 1
        camera(cnt)
        
    else:
        print("안기울임!")

if __name__=="__main__":
    GPIO.setwarnings(False)
    setup()
    try:
        while True:
            tilt()
            time.sleep(0.5)
    except KeyboardInterrupt:
        GPIO.cleanup()
    
    