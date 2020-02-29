#Exhibition Demo

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#from ultrasonic import sonic
from claw import Arm
from gpiozero import DistanceSensor
from motors import MotorController
from utils import Utils
from time import sleep
import webinterface

if __name__ == "__main__":
    MotorController.begin()
    claw = Arm()
    sensor1 = DistanceSensor(echo=4, trigger=24, max_distance=2)
    webinterface.setClawObj(claw)
    webinterface.begin()
    
    print('Reading ultrasonic')
    while True:
        if Utils.mode == "auto":
            distance=sensor1.distance
            print(distance)
            
            if distance >= 0.13 and distance <= 0.25:
                print("Arm move")
                claw.openClaw()
                claw.armReach()
                sleep(1)
                
                MotorController.forward()
                sleep(0.1)
                th = claw.sweepServo('claw', Arm.CLAW_CLOSE, 0.05)
                claw.claw_state = "closed"
                sleep(0.6)
                MotorController.stop()
                th.join()
                
                sleep(0.2)
                claw.armRestingPos()
        
        sleep(0.2)
