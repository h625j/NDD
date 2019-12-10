import RPi.GPIO as GPIO

rPin=14
yPin=18
gPin=15
GPIO.setmode(GPIO.BCM)
GPIO.setup(rPin, GPIO.OUT)
GPIO.setup(yPin, GPIO.OUT)
GPIO.setup(gPin, GPIO.OUT)
    
def ledctl(num):
    #빨강
    if num==1:
        GPIO.output(rPin, True)
        GPIO.output(yPin, False)
        GPIO.output(gPin, False)
    #노랑
    elif num==2:
        GPIO.output(yPin, True)
        GPIO.output(rPin, False)
        GPIO.output(gPin, False)
    #초록
    else:
        GPIO.output(gPin, True)
        GPIO.output(rPin, False)
        GPIO.output(yPin, False)
    