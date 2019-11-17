
#Motor Control with the Raspberry Pi




import RPi.GPIO as GPIO
import time
 
#GPIO Mode (BOARD / BCM)->This u check @PCMR
GPIO.setmode(GPIO.BCM)

gpio.setmode(gpio.BOARD)

#setting motor pins
gpio.setup(7, gpio.OUT)
gpio.setup(11, gpio.OUT)
gpio.setup(13, gpio.OUT)
gpio.setup(15, gpio.OUT)

 
#set GPIO Pins FOR RIGHT SENSOR
GPIO_TRIGGERR = 18
GPIO_ECHOR = 24

#SET PINS FOR LEFT SENSOR
GPIO_TRIGGERL = 18
GPIO_ECHOL = 24

 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGERR, GPIO.OUT)
GPIO.setup(GPIO_ECHOR, GPIO.IN)

GPIO.setup(GPIO_TRIGGERL, GPIO.OUT)
GPIO.setup(GPIO_ECHOL, GPIO.IN)
 
def distanceR():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGERR, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGERR, False)
 
    StartTimeR = time.time()
    StopTimeR = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHOR) == 0:
        StartTimeR = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHOR) == 1:
        StopTimeR = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTimeR - StartTimeR
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distanceR = (TimeElapsed * 34300) / 2
 
    return distanceR

def distanceL():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGERL, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGERL, False)
 
    StartTimeL = time.time()
    StopTimeL = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHOL) == 0:
        StartTimeL = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHOL) == 1:
        StopTimeL = time.time()
 
    # time difference between start and arrival
    TimeElapsedL = StopTimeL - StartTimeL
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distanceL = (TimeElapsed * 34300) / 2
 
    return distanceL
 
if __name__ == '__main__':
    try:
        while True:
            distL = distanceL()
	    distR = distanceR()
          #  print ("Measured Distance = %.1f cm" % dist)
           # time.sleep(1)

	if(distL <15cm && distR<15cm)
		gpio.output(7, True)#move forward u have not shared manual code so do it here
		
	else if(distL <15cm)
		gpio.output(11, True)#move right

	else if(distR <15cm)
		gpio.output(13, True)#move left

	else
		
		gpio.output(15, False)#continue moving straight  until  find obstacle
		time.sleep(0.5)
		gpio.cleanup()











	
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()




































		
