from utils import Utils
from gpiozero import DistanceSensor
from time import sleep

class Distance:
    
    def begin():
        Distance.sensor = DistanceSensor(echo=20, trigger=21)
    
    def distance():
        distance= Distance.sensor.distance * 100
        return round(distance,3)
        
        
if __name__=="__main__":
    Distance.begin()
    d= Distance.distance()

    print(d)
