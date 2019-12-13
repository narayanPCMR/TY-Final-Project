#Exhibition Demo

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#from ultrasonic import sonic
from claw import Arm
from motors import MotorController
from time import sleep
import webinterface

if __name__ == "__main__":
    MotorController.begin()
    claw = Arm()
    webinterface.setClawObj(claw)
    webinterface.begin()
    
    print('Reading ultrasonic')
    while True:
        #distance=sonic()
        #print(distance)
        
        #if distance >= 10 and distance <= 15:
        #    print("Arm move")
        #    sleep(1)
        
        sleep(0.2)
