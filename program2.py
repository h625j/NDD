import RPi.GPIO as GPIO
import time
import threading                            #3개의 thread 생성
from flask import Flask, render_template    #Flask 웹 서버 
from camera import *                        #사진 촬영
from tripleLED2 import *                    #신호등 led 제어 
from supersonic import *                    #초음파 센서 측정 
import dht11                                #온습도 센서 측정


cnt = 0
dis = 0
dflag=False
flag2=False
tilt1 = 20              #기울기센서1 GPIO핀을 20번으로 설정
tilt2 = 16              #기울기센서2 GPIO핀을 16번으로 설정

app= Flask(__name__)    #현재 모듈의 플라스크 객체 생성

@app.after_request      #HTTP 요청 후 브라우저 응답 전 실행
def add_header(response):
    """
    Add
    headers to both force latest IE rendering engine or Chrome Frame
    and
    also to cache the rendered page for 10 minutes
    """
    response.headers['X-UA-Compatible']='IE=Edge,chrome=1'      #호환성 보기
    response.headers['Cache-Control'] = 'public, max-age=0'     #캐시 유효시간 0
    return response

@app.route("/")         #웹에서 루트로 접속 시 핸들러 동작
def hello():
    global starttime
    now = time.time()   #현재 시각 측정
    timeString = time.strftime("%H:%M:%S", time.gmtime(now-starttime))  #전체 공부 시간 
    templateData = {'title':'I Hate Turtle!', 'time':timeString}        
    return render_template("main.html", **templateData)                 #전체 공부 시간이 출력되도록 탬플릿 변경

class AsyncTask:                                                        #멀티 쓰레드 이용을 위한 객체
    def __init__(self):
        pass
    
    def task1(self):                                                    #thread1 : Flask 서버 
        print("서버")
        app.run(host='0.0.0.0', port=80, debug=True)
        threading.Timer(0.5,self.task1).start()                         #o.5초마다 task1 호출
        
    def task2(self):                                                    #thread2 : 온습도 측정 
        sit()
        threading.Timer(3,self.task2).start()                           

    def task3(self):                                                    #thread3 : 기울기 측정
        tilt()
        threading.Timer(1,self.task3).start()

    def task4(self):                                                    #thread4 : 거리 측정 (초음파 센서)
        dist()
        threading.Timer(2,self.task4).start()
        
def main():

    at = AsyncTask()                                                    #각각의 task는 최초 한번은 수행해야한다
    
    at.task2()                                                          
    at.task3()
    at.task4()
    at.task1()                                                          #웹서버를 먼저 실행하면 센서 측정이 안 되므로 마지막에 호출
    
    
def setup():                                                            #GPIO핀 설정
    global instance
    GPIO.setmode(GPIO.BCM)                                              
    GPIO.setup(tilt1, GPIO.IN, pull_up_down=GPIO.PUD_UP)            
    GPIO.setup(tilt2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    instance = dht11.DHT11(pin=21)



"""
    온습도 센서
    -사용자 착석 감지
    -착석 후 일정 시간 뒤 (습도 상승) 자세 측정 결과 led 표시
"""
def sit():
    global flag2
    global instance
    result = instance.read()                                            #온습도 센서의 측정 결과
    temp_pre=0
    if result.is_valid():
        temp_pre = result.humidity                                      #초기 습도
    #print("처음 습도 : "+str(temp_pre))
    
    while True:
        result = instance.read()
        if result.is_valid():
            temp_post = result.humidity                                 #현재 습도
            if temp_post-temp_pre>1:                                    #습도 변화>1 : 자세 측정 결과 출력
                print("sitting")
                flag2=True          
                break                                                   


"""
    초음파 센서
    -사용자 등과 등받이 거리 감지
    -일정 거리 이상은 구부정한 자세
    -2단계로 등의 자세 판단
"""          
def dist():                                                       
    global dis
    dis = distance()                                                    #사용자 등과 등받이 사이 거리
    if (dis > 2000):                                                    #측정 오류는 무시
        return


"""
    기울기 센서
    -사용자 고개의 기울기 감지
    -2개의 센서의 초기 각도를 다르게 한 후, 결과 값의 차이를 통해 3단계로 구분
    -3단계로 목의 자세 판단
"""               
def tilt():
    global cnt
    global flag2                                                        #습도 변화 +1 이후 자세 측정 결과 출력 위함                         
    global dis
    t1 = GPIO.input(tilt1)                                              #기울기센서1 측정 값 (90도 이상:True)
    t2 = GPIO.input(tilt2)                                              #기울기센서2 측정 값
    chk=calc(t1, t2, dis)                                               #기울기, 거리 측정 값으로 자세 판단 (목, 등 구부러짐)
    
    if flag2==True:                                                     #습도 변화 +1 이후 (착석 후 일정 시간 경과)
        if chk==1:      
            ledctl(1)
            cnt += 1
            if cnt%10==0:
                print("빨간불")
                camera() 
        else:
            ledctl(chk)
   
    #time.sleep(0.5)

"""
    목(3단계), 등(2단계) 자세 분류 후 5단계로 led 표시
"""    
def calc(t1, t2, dis):                                                  #기울기 센서, 초음파 센서 측정 값
    if t1 ==True and t2 == True:                                      #목 45도 미만, 등 편 상태 (바른 자세)
        return 13, 13                                                        #초록 LED 점등
    elif t1 == True and t2==False and dis>20:                                          #목 45도 이상, 등 편 상태 (주의 자세)
        return 13, 18                                                                          #노랑 LED 점등
    elif t1 == True and t2==False and dis<20:                                             
        return 18, 18                                                                            #빨강 LED 점등
    elif t1 == False and t2==False and dis>20:                                             
        return 18, 15
    elif t1==  False and t2==False and dis<20:
        return 15, 15
    else:                                                               #다 끄기
        return 0, 0
    
            
if __name__=="__main__":
    GPIO.setwarnings(False)
    setup()
    ledctl(4)
    starttime = time.time()
    try:
        #sit()
        main()  
    except KeyboardInterrupt:
        GPIO.cleanup()
    