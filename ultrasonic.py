#import RPi.GPIO as GPIO
import time
from gpiozero import DistanceSensor

class Ultrasonic:
    sensor1 = DistanceSensor(echo=4, trigger=5, max_distance=2)

"""

#ultrasonics part ->intializing pins
TRIG = 5#change pins according to convinence
ECHO = 4

#intialize ultasonics
GPIO.setup(TRIG,GPIO.OUT)                  #Set pin as GPIO out
GPIO.setup(ECHO,GPIO.IN)
GPIO.output(TRIG, False)                 #Set TRIG as LOW

def sonic():
    GPIO.output(TRIG, True)                  #Set TRIG as HIGH
    time.sleep(0.00001)                      #Delay of 0.00001 seconds
    GPIO.output(TRIG, False)                 #Set TRIG as LOW
    
    pulse_start = 0
    pulse_end = 0
    
    while GPIO.input(ECHO)==0:               #Check whether the ECHO is LOW
        pulse_start = time.time()              #Saves the last known time of LOW pulse

    while GPIO.input(ECHO)==1:               #Check whether the ECHO is HIGH
        pulse_end = time.time()                #Saves the last known time of HIGH pulse 

    pulse_duration = pulse_end - pulse_start #Get pulse duration to a variable

    distance = pulse_duration * 17150        #Multiply pulse duration by 17150 to get distance
    distance = round(distance, 2)            #Round to two decimal points
    
    return distance
"""