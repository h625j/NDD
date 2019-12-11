
import RPi.GPIO as GPIO

rPin=23                            
yPin=24                             
gPin=25                             
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


GPIO.setup(rPin, GPIO.OUT)         
GPIO.setup(yPin, GPIO.OUT)
GPIO.setup(gPin, GPIO.OUT)
    
GPIO.output(rPin,False)

GPIO.output(yPin,False)
GPIO.output(gPin,False)
       
       
   
