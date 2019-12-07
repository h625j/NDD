
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
irpin = 21


GPIO.setup(irpin, GPIO.IN)

try:
    while True:
        x = GPIO.input(irpin)
        #print(x)
        time.sleep(0.5)
        if x != 1:
            print("사람임")
        else:
            print("물건임")
except KeyboardInterrupt:
    GPIO.cleanup()
