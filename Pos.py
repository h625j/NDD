import RPi.GPIO as GPIO
import time

def setup():
    GPIO.setmode(GPIO.BCM)
    #GPIO.setup(21, GPIO.OUT)
    GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
# def LEDon():
#     GPIO.output(21, True)
    
# def LEDoff():
#     GPIO.output(21, False)

def LED(channel):
    print("기울임!")
    
# def LED2(channel):
#     print("안기울임!")
    
def loop():
    if (GPIO.input(20) == True):
        print("기울임!")
    else:
        print("안기울임!")

if __name__=="__main__":
    GPIO.setwarnings(False)
    setup()
    try:
        while True:
            loop()
            time.sleep(0.5)
    except KeyboardInterrupt:
        GPIO.cleanup()
    
    