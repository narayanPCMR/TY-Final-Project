from motors import MotorController
from time import sleep

if __name__ == "__main__":
    MotorController.begin()

    #MotorController.speed=0.8
    MotorController.right()
    sleep(1)
    MotorController.speed=0.34
    MotorController.right()
    
   # MotorController.left()
   # sleep(2)
    MotorController.stop()
    


