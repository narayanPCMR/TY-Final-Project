#TEST CODE, do not put in project
import gpiozero as gz
from gpiozero.pins.pigpio import PiGPIOFactory
pf = PiGPIOFactory()
from time import time, sleep

s1 = gz.AngularServo(13, min_angle=0,max_angle=180, min_pulse_width=0.0006, max_pulse_width=0.0024, pin_factory=pf)
s2 = gz.AngularServo(6, min_angle=0,max_angle=180, min_pulse_width=0.0006, max_pulse_width=0.0024, pin_factory=pf)

u1 = gz.DistanceSensor(trigger=19, echo=26, max_distance=2.0, pin_factory=pf)
u2 = gz.DistanceSensor(trigger=20, echo=21, max_distance=2.0, pin_factory=pf)

while True:
    s1.value = -0.9
    s2.value = 0.9
    sleep(0.8)
    s = time()
    while time() - s < 1:
        print("Back distance right: {:.2f}cm, Back distance left: {:.2f}cm".format(u1.distance*100, u2.distance*100))
        sleep(0.2)
    s1.value = 0.9
    s2.value = -0.9
    sleep(0.8)
    s = time()
    while time() - s < 1:
        print("Front distance right: {:.2f}cm, Front distance left: {:.2f}cm".format(u1.distance*100, u2.distance*100))
        sleep(0.2)
    