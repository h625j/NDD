import RPi.GPIO as GPIO   
import time  
 
#GPIO 핀 17,27을 사용한다.
GPIOIN = 21
 
#핀 넘버링을 BCM 방식을 사용한다.
GPIO.setmode(GPIO.BCM)   
print ("HC-SR501 motion detection start")
#17번 핀을 입력용, 27번 핀을 출력용으로 설정한다.
#출력용 핀은 LED 상태를 확인하기 위해 사용하는 핀으로 실제 동작과는 무관하다.
GPIO.setup(GPIOIN, GPIO.IN)    
try: 
    while True:  
        #HC-SR501센서의 출력 값을 읽는다.
        state =  GPIO.input(GPIOIN)
        if(state == True):
            print ("state: Motion detected")
            state = False
        else:
            print ("state: No Motion")
        #HC-SR501센서의 출력 값을 LED로 보낸다.
        time.sleep(0.1)  
except KeyboardInterrupt:   
    GPIO.cleanup()       