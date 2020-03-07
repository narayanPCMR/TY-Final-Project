from utils import Utils, Pinout
from gpiozero import DistanceSensor
from time import sleep
from speech import Speech
speech = Speech()

class Distance:
    def begin():
        Distance.sensor = DistanceSensor(echo=Pinout.PIN_ULTRASOINIC_ECHO, trigger=Pinout.PIN_ULTRASOINIC_TRIG)
    
    def distance():
        distance= Distance.sensor.distance * 100
        return round(distance,3)
    
    def loop():
        if Utils.pickupPhase == 0:
            d = Distance.distance()
            print("Stage 0,", d, "cm")
            if(d < 80):
                print("Something found infront of me! Moving to phase 1")
                speech.speak(speech.BEGUN)
                Utils.pickupPhase = 1
                
        
if __name__=="__main__":
    Distance.begin()
    d= Distance.distance()

    print(d)
