from camera import Camera
import threading
import cv2

CASCADE = "data/haarcascade_frontalface_alt.xml"

class Tracker:
    AllTrackers = []
    
    x = 0
    y = 0
    w = 0
    h = 0
    trackedImg = None
    
    def __init__(self, x, y, w, h, img):
        #Position as percentage
        self.x = x / img.shape[1]
        self.y = y / img.shape[0]
        self.w = w / img.shape[1]
        self.h = h / img.shape[0]
        self.trackedImg = img[y:y+h,x:x+w]
        
        #You see the problem? That's why we need to use intersection check
        
        #Add the tracker to list of trackers
        Tracker.AllTrackers.append(self)
    
    def getPosTupleImage(self, img):
        x, y = int(self.x * img.shape[1]), int(self.y * img.shape[0])
        w, h = int(self.w * img.shape[1]), int(self.h * img.shape[0])
        return (x, y, w, h)
    
    def track(self, image_whole):
        print("[TODO]")

class Detector:
    scale = 1.2
    minN = 4
    
    def __init__(self):
        self.cascade = cv2.CascadeClassifier(CASCADE)
        
        #Create a thread
        self.detTh = threading.Thread(target=Detector.detectLoop, args=(self,))
        self.detStopEv = threading.Event()
    
    def begin(self):
        self.detStopEv.clear()
        self.detTh.start()
    
    def end(self):
        self.detStopEv.set()
        self.detTh.join()
    
    def detectLoop(self):
        frameNo = 0
        for img in Camera.waitFrame(320, 240):
            if self.detStopEv.is_set():
                break
            
            if frameNo > 3:
                frameNo = 0
                b = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                b = cv2.equalizeHist(b)
                
                objects = self.cascade.detectMultiScale(b, self.scale, self.minN)
                for o in objects:
                    Tracker(*o, img)
            
            frameNo += 1