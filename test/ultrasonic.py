from gpiozero import DistanceSensor
from threading import Thread, Event
from utils import Utils
from time import sleep

class AutoNavigator:
    sensor1 = DistanceSensor(echo=18, trigger=17, max_distance=2)#set pins for sensor1
    sensor2 = DistanceSensor(echo=23, trigger=24, max_distance=2)#set pins for sensor2
    servo1 = Servo(14)#set pins for servo1
    servo2 = Servo(15)#set pins for servo2
    operating = False
    
    def begin():
        AutoNavigator.th = Thread(target=AutoNavigator.update)
        AutoNavigator.ev = Event()
        AutoNavigator.th.start()
    
    def end():
        AutoNavigator.ev.set()
    
    def engage():
        AutoNavigator.operating = True
        print("Navigating automatically.")
    
    def disengage():
        AutoNavigator.operating = False
    
    def update():
        while not AutoNavigator.ev.is_set():
            while not AutoNavigator.operating:
                sleep(0.1)
            if Utils.pickupPhase == 1:
                #Move servos so they face the front
                AutoNavigator.servo1.min()
                sleep(0.5)
                a = AutoNavigator.sensor1.distance * 100
                print(a)
                AutoNavigator.servo1..mid()
                sleep(0.5)
                a=AutoNavigator.sensor1.distance * 100
                print(a)
                AutoNavigator.servo1..max()
                sleep(0.5)
                a=AutoNavigator.sensor1.distance * 100
                print(a)
                #Read the values continuously
            

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