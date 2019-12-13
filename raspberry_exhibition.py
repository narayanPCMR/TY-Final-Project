#Exhibition Demo

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#from ultrasonic import sonic
from claw import Arm
from gpiozero import DistanceSensor
from motors import MotorController
from time import sleep
import webinterface

if __name__ == "__main__":
    MotorController.begin()
    claw = Arm()
    sensor1 = DistanceSensor(echo=4, trigger=5, max_distance=2)
    webinterface.setClawObj(claw)
    webinterface.begin()
    
    print('Reading ultrasonic')
    while True:
        distance=sensor1.distance
        print(distance)
        
        if distance >= 0.10 and distance <= 0.15:
            print("Arm move")
            claw.openClaw()
            claw.armReach()
            sleep(1)
            th = claw.sweepServo('claw', Arm.CLAW_CLOSE, 0.05)
            claw.claw_state = "closed"
            sleep(0.2)
            claw.armRestingPos()
            th.join()
        
        sleep(0.2)
