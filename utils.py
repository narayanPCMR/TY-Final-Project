
class Pinout:
    PIN_MOTORLEFT1 = 17#23#17
    PIN_MOTORLEFT2 = 22#18#18
    PIN_MOTORRIGHT1 = 18#17#22
    PIN_MOTORRIGHT2 = 23#22#23
    PIN_SERVOCLAW = 13
    PIN_SERVOLEFT = 19
    PIN_SERVORIGHT = 6
    PIN_SERVOROTATE = 26
    PIN_ULTRASOINIC_TRIG = 24
    PIN_ULTRASOINIC_ECHO = 4


class Utils:
    mode = "manual"
    pickupPhase = 0
    
    def rangePercent(p, a, b):
        return (b-a)*p+a
    
    def union(a,b):
        x = min(a[0], b[0])
        y = min(a[1], b[1])
        w = max(a[0]+a[2], b[0]+b[2]) - x
        h = max(a[1]+a[3], b[1]+b[3]) - y
        return (x, y, w, h)

    def intersection(a,b):
        """
        Calculate intersection of two rectangles
        """
        x = max(a[0], b[0])
        y = max(a[1], b[1])
        w = min(a[0]+a[2], b[0]+b[2]) - x
        h = min(a[1]+a[3], b[1]+b[3]) - y
        
        if w<0 or h<0: return (0,0,0,0)
        
        return (x, y, w, h)
    
    def area(r):
        return max(0, r[2]*r[3])