import RPi.GPIO as GPIO
import time
import dht11
from camera import *
from tripleLED import *
import threading
from flask import Flask, render_template
from supersonic import *

cnt = 0
instance = dht11.DHT11(pin=21)
dflag=False
flag2=False
tilt1 = 20
tilt2 = 16
dis = 0

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
        print("서버")
        app.run(host='0.0.0.0', port=80, debug=True)
        threading.Timer(1,self.task1).start()
        
    def task2(self):        
        sit()
        threading.Timer(2,self.task2).start()
        
    def task3(self):
        tilt()
        threading.Timer(1,self.task3).start()
    def task4(self):
        dist()
        threading.Timer(1,self.task4).start()
        
def main():
    at = AsyncTask()
    at.task2()
    at.task3()
    at.task4()
    at.task1()   
    
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
def dist():
    global dis
    dis = distance()
    if (dis > 2000):
        return
                
def tilt():
    global cnt
    global flag2
    global dis
    t1 = GPIO.input(tilt1)
    t2 = GPIO.input(tilt2)
    chk=calc(t1, t2, dis)

#     #while True:
#     if (t1 == True and flag2 == True and t2 == True and dis>20):
#         ledctl(1)
#         cnt += 1
#         if cnt%10==0:
#             print("빨간불")
#             camera()            
#     elif (t1 == True and flag2 == True and t2 == False and dis >10 and dis < 20):
#         print("tilt1만")
#         ledctl(2)
#     elif (t1 == False and flag2 == True and t2 == False and dis <10):
#         print("둘다아님")
#         ledctl(3)
#     else:
#         ledctl(4)
    
    if flag2==True:
        if chk==1:
            ledctl(1)
            cnt += 1
            if cnt%10==0:
                print("빨간불")
                camera() 
        else:
            ledctl(chk)
   
    #time.sleep(0.5)
    
def calc(t1, t2, dis):
   
    if (t1 ==False and t2 == False):
        return 3
    elif ((t1 == True and t2 ==False and dis<20) or(t1 == True and t2 == True and dis<20)):
        return 2
    elif (t1 == True and t2 == False and dis>20) or (t1 == True and t2 == True and dis>20):
        return 1
    else:
        return 4
    
            
if __name__=="__main__":
    GPIO.setwarnings(False)
    setup()
    try:
        sit()
        main()  
    except KeyboardInterrupt:
        GPIO.cleanup()
    