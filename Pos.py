import RPi.GPIO as GPIO
import time
import dht11
from camera import *
import threading

cnt = 0
instance = dht11.DHT11(pin=21)

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
def sit():
    global instance
    result = instance.read()
    temp_pre=0
    if result.is_valid():
        temp_pre = result.humidity
    print("처음 습도 : "+str(temp_pre))
    flag=True
    while flag:
        result = instance.read()
        if result.is_valid():
            temp_post = result.humidity
            if temp_post-temp_pre>1:
                print("sitting")
                flag=False
                
    print("틸트수행")
        
#     tilt()
    
# def tilt():
#     global cnt
#     if (GPIO.input(20) == True):
#         print("기울임!")
#         cnt += 1
#         camera(cnt)
        
#     else:
#         print("안기울임!")

if __name__=="__main__":
    GPIO.setwarnings(False)
    setup()
    try:
        while True:
            sit()
            time.sleep(0.5)
    except KeyboardInterrupt:
        GPIO.cleanup()
    