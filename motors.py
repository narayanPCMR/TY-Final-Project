import gpiozero

M1_FORWARDPIN  = 17
M1_BACKWARDPIN = 18
M1_ENABLEPIN   = None

M2_FORWARDPIN  = 22
M2_BACKWARDPIN = 23
M2_ENABLEPIN   = None

USING_PWM = True

class MotorController:
    speed = 0.5
    robot = None
    def begin():
        MotorController.robot = gpiozero.Robot(left=(M1_FORWARDPIN, M1_BACKWARDPIN), right=(M2_FORWARDPIN, M2_BACKWARDPIN), pwm=USING_PWM)
    
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
    
    def customLeftMotor( speed):
        MotorController.robot.left_motor.value = speed
    
    def customRightMotor(speed):
        MotorController.robot.right_motor.value = speed


