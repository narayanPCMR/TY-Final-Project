import pigpio
import time
import threading
from utils import Utils
from utils import Pinout

class Arm:
    CLAW_OPEN = 1200
    CLAW_CLOSE = 2100
    ARM_L_REST = 1400
    ARM_L_DOWN = 2250
    ARM_H_REST = 1800
    ARM_H_DOWN = 600
    CLAW_ROTATE_FRONT = 600
    CLAW_ROTATE_BACK = 2500

    
    #pinList = {'claw': 13, 'linear': 19, 'height': 6,'rotate':26}
    servos = {'claw': [Pinout.PIN_SERVOCLAW, CLAW_CLOSE],
              'linear': [Pinout.PIN_SERVOLEFT, ARM_L_REST],
              'height': [Pinout.PIN_SERVORIGHT, ARM_H_REST],
              'rotate':[Pinout.PIN_SERVOROTATE, CLAW_ROTATE_FRONT]
              }
    
    claw_state = "closed"
    
    def __init__(self):
        self.pi = pigpio.pi()
        
        for s in self.servos:
            self.pi.set_servo_pulsewidth(*self.servos[s])
    
    def moveTowards(self, servo_id, pos, step_delay):
        step_dir = 40
        
        if self.servos[servo_id][1] > pos:
            step_dir = -40
        
        for i in range(self.servos[servo_id][1], pos, step_dir):
            self.pi.set_servo_pulsewidth(self.servos[servo_id][0], i)
            #self.servos[servo_id][0].ChangeDutyCycle(i / 10)
            time.sleep(step_delay)
        
        self.servos[servo_id][1] = pos
    
    
    def sweepServo(self, servo_id, pos, step_delay = 0.03):
        th = threading.Thread(target = Arm.moveTowards, args = (self, servo_id, pos, step_delay))
        th.start()
        return th
    
    def openClaw(self):
        self.sweepServo('claw', Arm.CLAW_OPEN, 0.05).join()
        self.claw_state = "open"
    
    def closeClaw(self):
        self.sweepServo('claw', Arm.CLAW_CLOSE, 0.05).join()
        self.claw_state = "closed"

    def armRestingPos(self):
        arm_a = self.sweepServo('linear', Arm.ARM_L_REST)
        arm_b = self.sweepServo('height', Arm.ARM_H_REST)
        arm_a.join()
        arm_b.join()
    
    def armReach(self):
        arm_a = self.sweepServo('linear', Arm.ARM_L_DOWN)
        arm_b = self.sweepServo('height', Arm.ARM_H_DOWN)
        arm_a.join()
        arm_b.join()
    
    def armAt(self, percent):
        lin = Utils.rangePercent(percent, Arm.ARM_L_REST, Arm.ARM_L_DOWN)
        hei = Utils.rangePercent(percent, Arm.ARM_H_REST, Arm.ARM_H_DOWN)
        
        arm_a = self.sweepServo('linear', int(lin))
        arm_b = self.sweepServo('height', int(hei))
        arm_a.join()
        arm_b.join()
    
    def rotateClawFront(self):
        self.sweepServo('rotate',Arm.CLAW_ROTATE_FRONT,0.02)
        
    def rotateClawBack(self):
        self.sweepServo('rotate',Arm.CLAW_ROTATE_BACK,0.02).join()

if __name__ == "__main__":
    arm = Arm()
    arm.closeClaw()
    time.sleep(2)
    
    print("Start")
    while True:
        arm.openClaw()
        arm.armReach()
        arm.closeClaw()
        arm.armRestingPos()
        print("paper ball grabbed")        
        arm.rotateClawBack()
        time.sleep(1)
        arm.openClaw()
        arm.rotateClawFront()
        print("paper ball put in dustbin")
        
"""
currPos1=7
currPos2=8
pinList={'claw':20,'linear':21,'height':16}
servos={}

for i in pinList:
    GPIO.setup(pinList[i],GPIO.OUT)
    servos[i]=GPIO.PWM(pinList[i],50)
    servos[i].start(7)

def closeClaw():
    for i in range(60,105):
        servos['claw'].ChangeDutyCycle(i/10)
        time.sleep(0.025)

def openClaw():
    servos['claw'].ChangeDutyCycle(6)

#TODO: Simultaneous both servos
def arm_resting_pos():
    global currPos1, currPos2
    if(currPos1<7):
        for i in range(currPos1*10,70,1):
            servos['linear'].ChangeDutyCycle(i/10)
            time.sleep(0.025)
    elif(currPos1>=7):
        for i in range(currPos1*10,70,-1):
            servos['linear'].ChangeDutyCycle(i/10)
            time.sleep(0.025)
    currPos1=7
    
    if(currPos2<7):
        for i in range(currPos2*10,70,1):
            servos['height'].ChangeDutyCycle(i/10)
            time.sleep(0.025)
    elif(currPos1>=7):
        for i in range(currPos2*10,70,-1):
            servos['height'].ChangeDutyCycle(i/10)
            time.sleep(0.025)
    currPos2=7

def arm_reach():
    global currPos1, currPos2
    if(currPos1<10.5):
        for i in range(currPos1*10,105,1):
            servos['linear'].ChangeDutyCycle(i/10)
            time.sleep(0.025)
    elif(currPos1>=10.5):
        for i in range(currPos1*10,105,-1):
            servos['linear'].ChangeDutyCycle(i/10)
            time.sleep(0.025)
    currPos1=10
    
    if(currPos2<7):
        for i in range(currPos2*10,70,1):
            servos['height'].ChangeDutyCycle(i/10)
            time.sleep(0.025)
    elif(currPos1>=7):
        for i in range(currPos2*10,70,-1):
            servos['height'].ChangeDutyCycle(i/10)
            time.sleep(0.025)
    currPos2=10

openClaw()
arm_resting_pos()

time.sleep(1)

arm_reach()
closeClaw()

time.sleep(1)

arm_resting_pos()

time.sleep(2)

openClaw()
"""

'''
> servos['height'].ChangeDutyCycle(4)
>>> servos['linear'].ChangeDutyCycle(3)
>>> servos['linear'].ChangeDutyCycle(12)
>>> servos['linear'].ChangeDutyCycle(11)
>>> servos['height'].ChangeDutyCycle(4)
>>> servos['height'].ChangeDutyCycle(4)
>>> servos['height'].ChangeDutyCycle(5)
>>> servos['height'].ChangeDutyCycle(3)
>>> servos['height'].ChangeDutyCycle(4)
>>> servos['claw'].ChangeDutyCycle(3)
>>> servos['claw'].ChangeDutyCycle(5)
>>> servos['claw'].ChangeDutyCycle(11)
>>> servos['linear'].ChangeDutyCycle(7)
>>> servos['height'].ChangeDutyCycle(8)
'''


