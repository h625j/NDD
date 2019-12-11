import RPi.GPIO as GPIO

rPin=23                             #빨간 led : GPIO 13번 핀
yPin=24                             #노란 led : GPIO 18번 핀
gPin=25                             #초록 led : GPIO 15번 핀
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(rPin, GPIO.OUT)          #GPIO핀 출력모드 설정
GPIO.setup(yPin, GPIO.OUT)
GPIO.setup(gPin, GPIO.OUT)
    
def ledctl(num1,num2):                    #색깔 별 led를 켜고 끄기 위한 함수
    
    GPIO.output(rPin, False)
    GPIO.output(yPin, False)
    GPIO.output(gPin, False)

    if num1!=0 and num2!=0:
        print("tripleLED{}{}".format(num1,num2))
        GPIO.output(num1,True)
        GPIO.output(num2,True)
       
       
   