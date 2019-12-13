import gpiozero

M1_FORWARDPIN  = 17
M1_BACKWARDPIN = 18
M1_ENABLEPIN   = None

M2_FORWARDPIN  = 22
M2_BACKWARDPIN = 23
M2_ENABLEPIN   = None

USING_PWM = True

class MotorController:
    def begin():
        MotorController.robot = gpiozero.Robot(left=(M1_FORWARDPIN, M1_BACKWARDPIN, M1_ENABLEPIN), right=(M2_FORWARDPIN, M2_BACKWARDPIN, M2_ENABLEPIN), pwm=USING_PWM)
    
    def forward():
        MotorController.robot.forward()
    
    def backward():
        MotorController.robot.backward()
    
    def right():
        MotorController.robot.right()
    
    def left():
        MotorController.robot.left()
    
    def stop():
        MotorController.robot.stop()
    
    def customControl( speeds):
        MotorController.robot.value = speeds
    
    def customLeftMotor( speed):
        MotorController.robot.left_motor.value = speed
    
    def customRightMotor(speed):
        MotorController.robot.right_motor.value = speed
