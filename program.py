import RPi.GPIO as GPIO
import time
import dht11
from camera import *
import threading

cnt = 0
instance = dht11.DHT11(pin=21)

class TiltThread(threading.Thread):
    def __init__(self,threadID,name):
        threading.Thread.__init__(self)
        self.threadID=threadID
        self.name=name
    def run(self):
        tilt(self.name)

class SitThread(threading.Thread):
    def __init__(self,threadID,name):
        threading.Thread.__init__(self)
        self.threadID=threadID
        self.name=name
    def run(self):
        sit(self.name)        
    
def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
def sit(threadName):
    print("Starting",threadName)

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
                
    
def tilt(threadName):
    global cnt
    print("Starting",threadName)

    while True:
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
        thread1 = TiltThread(1, "tilt")
        thread2 = SitThread(2, "sit")
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()
    except KeyboardInterrupt:
        GPIO.cleanup()
    