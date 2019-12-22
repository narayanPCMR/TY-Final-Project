from camera import Camera
from utils import Utils
import threading
import cv2

CASCADE = "data/cascade.xml"

class Tracker:
    AllTrackers = []
    
    x = 0
    y = 0
    w = 0
    h = 0
    trackedImg = None
    orb = None
    bf = None
    
    def begin():
        Tracker.multiTracker = cv2.MultiTracker_create()
    
    def __init__(self, x, y, w, h, img):
        #Position as percentage
        self.x = x / img.shape[1]
        self.y = y / img.shape[0]
        self.w = w / img.shape[1]
        self.h = h / img.shape[0]
        self.trackedImg = img[y:y+h,x:x+w]
        
        #if len(Tracker.AllTrackers) > 0: return
        
        my_rect = (self.x, self.y, self.w, self.h)
        for trk in Tracker.AllTrackers:
            trk_rect = (trk.x, trk.y, trk.w, trk.h)
            intersect_rect = Utils.intersection(my_rect, trk_rect)
            ar = Utils.area(intersect_rect)
            if ar > 0: break
        else:
            self.tracker = cv2.TrackerCSRT_create()
            
            multiTracker.add(self.tracker, img, self.getPosTupleImage(img))
            
            #Add the tracker to list of trackers
            Tracker.AllTrackers.append(self)
        
    def getPosTupleImage(self, img):
        x, y = int(self.x * img.shape[1]), int(self.y * img.shape[0])
        w, h = int(self.w * img.shape[1]), int(self.h * img.shape[0])
        return (x, y, w, h)
    
    def track(image_whole):
        success, boxes = Tracker.multiTracker.update(image_whole)
        print(success)
        
        #res = cv2.matchTemplate(image_whole, self.trackedImg, cv2.TM_CCOEFF)
        #min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        #max_loc = (max_loc[0]/image_whole.shape[1], max_loc[1]/image_whole.shape[0])
        
        #if abs(max_loc[0]-self.x) > self.w*2 or abs(max_loc[1]-self.y) > self.h*2:
        #    print("Object lost")
        #else:
        #    self.x, self.y = max_loc
        
        
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