import gpiozero

M1_FORWARDPIN  = 4
M1_BACKWARDPIN = 14
M1_ENABLEPIN   = None

M2_FORWARDPIN  = 17
M2_BACKWARDPIN = 18
M2_ENABLEPIN   = None

USING_PWM = True

class IOController:
    def begin():
        IOController.robot = gpiozero.Robot(left=(M1_FORWARDPIN, M1_BACKWARDPIN, M1_ENABLEPIN), right=(M2_FORWARDPIN, M2_BACKWARDPIN, M2_ENABLEPIN), pwm=USING_PWM)
    
    def forward():
        IOController.robot.forward()
    
    def backward():
        IOController.robot.backward()
    
    def right():
        IOController.robot.right()
    
    def left():
        IOController.robot.left()
    
    def stop():
        IOController.robot.stop()
    
    def customControl( speeds):
        IOController.robot.value = speeds
    
    def customLeftMotor( speed):
        IOController.robot.left_motor.value = speed
    
    def customRightMotor(speed):
        IOController.robot.right_motor.value = speed
