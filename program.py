import RPi.GPIO as GPIO
import time
import dht11
from camera import *
from tripleLED import *
import threading

cnt = 0
instance = dht11.DHT11(pin=21)
flag2=False
tilt1 = 20
tilt2 = 16

app= Flask(__name__)

@app.after_request
def add_header (response):
    """
    Add
    headers to both force latest IE rendering engine or Chrome Frame
    and
    also to cache the rendered page for 10 minutes
    """
    response.headers['X UA Compatible']='IE=Edge,chrome=1'
    response.headers['Cache Control'] = 'public , max-age =0'
    return response

@app.route("/")
def hello():
    return render_template("main.html")

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
    GPIO.setup(tilt1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(tilt2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    
def sit(threadName):
    print("Starting",threadName)
    global flag2
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
                flag2=True
                flag=False
                
    
def tilt(threadName):
    global cnt
    global flag2
    print("Starting",threadName)

    while True:
        if (GPIO.input(20) == True and flag2==True):
            cnt += 1
            if cnt%20==0:
                print("기울임!")
                camera(cnt)
                ledctl(1)
        time.sleep(0.5)

if __name__=="__main__":
    GPIO.setwarnings(False)
    setup()
    app.run(host='0.0.0.0', port=80, debug=True)
    try: 
        thread1 = TiltThread(1, "tilt")
        thread2 = SitThread(2, "sit")
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()
    except KeyboardInterrupt:
        GPIO.cleanup()
    