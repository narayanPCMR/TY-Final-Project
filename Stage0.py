from utils import Utils
from gpiozero import DistanceSensor
from time import sleep

class Distance:
    
    def begin():
        Distance.sensor = DistanceSensor(echo=4, trigger=24)
    
    def distance():
        distance= Distance.sensor.distance * 100
        return round(distance,3)
    
    def loop():
        if Utils.pickupPhase == 0:
            d = Distance.distance()
            if(d < 20):
                print("Something found infront of me! Moving to phase 1")
                Utils.pickupPhase = 1
                
        
if __name__=="__main__":
    Distance.begin()
    d= Distance.distance()

    print(d)
