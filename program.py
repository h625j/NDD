import RPi.GPIO as GPIO
import time
import dht11
from camera import *
from tripleLED import *
import threading
from flask import Flask, render_template

cnt = 0
instance = dht11.DHT11(pin=21)
flag2=False
tilt1 = 20
tilt2 = 16

app= Flask(__name__)

@app.after_request
def add_header(response):
    """
    Add
    headers to both force latest IE rendering engine or Chrome Frame
    and
    also to cache the rendered page for 10 minutes
    """
    response.headers['X-UA-Compatible']='IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

@app.route("/")
def hello():
    return render_template("main.html")

class AsyncTask:
    def __init__(self):
        pass
    
    def task1(self):
        app.run(host='0.0.0.0', port=80, debug=True)
        threading.Timer(1,self.task1).start()
        
    def task2(self):
        sit()
        threading.Timer(1,self.task2).start()
        
    def task3(self):
        tilt()
        threading.Timer(1,self.task3).start()
        
def main():
    at = AsyncTask()
    at.task1()
    at.task2()
    at.task3()
        

# class WebThread(threading.Thread):
#     def __init__(self,threadID,name):
#         threading.Thread.__init__(self)
#         self.threadID=threadID
#         self.name=name
#     def run(self):
#         webrun(self.name)
        
# def webrun(threadName):
#     app.run(host='0.0.0.0', port=80, debug=True)

# class TiltThread(threading.Thread):
#     def __init__(self,threadID,name):
#         threading.Thread.__init__(self)
#         self.threadID=threadID
#         self.name=name
#     def run(self):
#         tilt(self.name)

# class SitThread(threading.Thread):
#     def __init__(self,threadID,name):
#         threading.Thread.__init__(self)
#         self.threadID=threadID
#         self.name=name
#     def run(self):
#         sit(self.name)        
    
def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(tilt1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(tilt2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
def sit():
    global flag2
    global instance
    result = instance.read()
    temp_pre=0
    if result.is_valid():
        temp_pre = result.humidity
    #print("처음 습도 : "+str(temp_pre))
    flag=True
    while flag:
        result = instance.read()
        if result.is_valid():
            temp_post = result.humidity
            if temp_post-temp_pre>1:
                print("sitting")
                flag2=True
                flag=False                
    
def tilt():
    global cnt
    global flag2

    #while True:
    if (GPIO.input(tilt1) == True and flag2 == True and GPIO.input(tilt2) == True):
        print("둘다")
        cnt += 1
        if cnt%10==0:
            print("기울임!")
            camera()
            ledctl(1)
    elif (GPIO.input(tilt1) == True and flag2 == True and GPIO.input(tilt2) == False):
        print("tilt1만")
        ledctl(2)
    elif (GPIO.input(tilt1) == False and flag2 == True and GPIO.input(tilt2) == False):
        print("둘다아님")
        ledctl(3)
    else:
        ledctl(4)
    time.sleep(0.5)
            
if __name__=="__main__":
    GPIO.setwarnings(False)
    setup()
    try: 
        main()  
    except KeyboardInterrupt:
        GPIO.cleanup()
    