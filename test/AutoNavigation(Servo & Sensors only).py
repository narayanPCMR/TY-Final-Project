import RPi.GPIO as GPIO
import time

#servo part ->intializing pins
servoPIN1 = 17
servoPIN2 = 17

GPIO.setup(servoPIN1, GPIO.OUT)
GPIO.setup(servoPIN2, GPIO.OUT)

#ultrasonics part ->intializing pins
TRIG1 = 23#change pins according to convinence
ECHO1 = 24                                 
TRIG2 = 23#change pins according to convinence
ECHO2 = 24  

#initialize servos
p1 = GPIO.PWM(servoPIN1, 50) # GPIO pin for PWM with 50Hz
p2 = GPIO.PWM(servoPIN2, 50)
p1.start(2.5) # Initialization
p2.start(2.5) # Initialization
i=2.5;

#intialize ultasonics
GPIO.setup(TRIG1,GPIO.OUT)                  #Set pin as GPIO out
GPIO.setup(ECHO1,GPIO.IN) 
GPIO.setup(TRIG2,GPIO.OUT)                  
GPIO.setup(ECHO2,GPIO.IN) 

def sonic():
 

  GPIO.output(TRIG, False)                 #Set TRIG as LOW
  print ("Waitng For Sensor To Settle")
  time.sleep(2)                            #Delay of 2 seconds

  GPIO.output(TRIG, True)                  #Set TRIG as HIGH
  time.sleep(0.00001)                      #Delay of 0.00001 seconds
  GPIO.output(TRIG, False)                 #Set TRIG as LOW

  while GPIO.input(ECHO)==0:               #Check whether the ECHO is LOW
    pulse_start = time.time()              #Saves the last known time of LOW pulse

  while GPIO.input(ECHO)==1:               #Check whether the ECHO is HIGH
    pulse_end = time.time()                #Saves the last known time of HIGH pulse 

  pulse_duration = pulse_end - pulse_start #Get pulse duration to a variable

  distance = pulse_duration * 17150        #Multiply pulse duration by 17150 to get distance
  distance = round(distance, 2)            #Round to two decimal points

  if distance > 2 and distance < 400:      #Check whether the distance is within range
    print ("Distance:",distance - 0.5,"cm")  #Print distance with 0.5 cm calibration
  else:
    print ("Out Of Range")                   #display out of range

try:
  while True:
   while(i>=10):
    p1.ChangeDutyCycle(i)
    sonic()
    p2.ChangeDutyCycle(i)
    sonic()
    time.sleep(0.5)
    i+=2.5;

   while(i<=2.5):
    p1.ChangeDutyCycle(i)
    sonic()
    p2.ChangeDutyCycle(i)
    sonic()
    time.sleep(0.5)
    i-=2.5;

except KeyboardInterrupt:
  p.stop()
  GPIO.cleanup()
