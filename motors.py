import gpiozero
from utils import Pinout
from gpiozero.pins.pigpio import PiGPIOFactory

factory = PiGPIOFactory(host='localhost')

M1_FORWARDPIN  = Pinout.PIN_MOTORLEFT1
M1_BACKWARDPIN = Pinout.PIN_MOTORLEFT2
M1_ENABLEPIN   = None

M2_FORWARDPIN  = Pinout.PIN_MOTORRIGHT1
M2_BACKWARDPIN = Pinout.PIN_MOTORRIGHT2
M2_ENABLEPIN   = None

USING_PWM = True

class MotorController:
    #speed = 0.9
    speed = 1.0
    robot = None
    
    def begin():
        MotorController.robot = gpiozero.Robot(left=(M1_FORWARDPIN, M1_BACKWARDPIN), right=(M2_FORWARDPIN, M2_BACKWARDPIN), pwm=USING_PWM, pin_factory=factory)
    
    def forward():
        MotorController.robot.forward(speed=MotorController.speed)
    
    def backward():
        MotorController.robot.backward(speed=MotorController.speed)
    
    def right():
        MotorController.robot.right(speed=MotorController.speed)
    
    def left():
        MotorController.robot.left(speed=MotorController.speed)
    
    def stop():
        MotorController.robot.stop()
    
    def customControl(speeds):
        MotorController.robot.value = speeds
    
    def customLeftMotor(speed):
        MotorController.robot.left_motor.value = speed
    
    def customRightMotor(speed):
        MotorController.robot.right_motor.value = speed


