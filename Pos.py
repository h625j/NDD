import RPi.GPIO as GPIO
import time
import picamera

cnt = 0

def setup():
    global camera    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
def tilt():
    global cnt
    camera = picamera.PiCamera()
    camera.resolution = (1200,800)
    if (GPIO.input(20) == True):
        print("기울임!")
        cnt += 1
        camera.capture("tilted"+str(cnt)+".jpg")
        time.sleep(2)
        camera.close()
        
    else:
        print("안기울임!")

if __name__=="__main__":
    GPIO.setwarnings(False)
    setup()
    try:
        while True:
            tilt()
            time.sleep(0.5)
    except KeyboardInterrupt:
        GPIO.cleanup()
    
    