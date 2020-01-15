from camera import Camera
from utils import Utils
from time import time
import threading
import cv2

CASCADE = "data/cascade.xml"

class Tracker:
    AllTrackers = []
    GlobTrackerID = 0
    
    x = 0
    y = 0
    w = 0
    h = 0
    id = 0
    
    lost_time = None
    isTracking = False
    
    def __init__(self, bbox, img):
        #Position as percentage
        x, y, w, h = bbox
        self.x = x / img.shape[1]
        self.y = y / img.shape[0]
        self.w = w / img.shape[1]
        self.h = h / img.shape[0]
        #self.trackedImg = img[y:y+h,x:x+w]
        
        #Limit to 2 trackers
        if len(Tracker.AllTrackers) >= 5: return
        
        ar = -1
        my_rect = (self.x, self.y, self.w, self.h)
        for trk in Tracker.AllTrackers:
            trk_rect = (trk.x, trk.y, trk.w, trk.h)
            intersect_rect = Utils.intersection(my_rect, trk_rect)
            ar = Utils.area(intersect_rect)
            if ar > 0: break
        else:
            self.tracker = cv2.TrackerCSRT_create()
            self.tracker.init(img, tuple(bbox))
            
            #Add the tracker to list of trackers
            self.id = Tracker.GlobTrackerID
            Tracker.GlobTrackerID += 1
            Tracker.AllTrackers.append(self)
        
    def getPosTupleImage(self, img):
        x, y = int(self.x * img.shape[1]), int(self.y * img.shape[0])
        w, h = int(self.w * img.shape[1]), int(self.h * img.shape[0])
        return (x, y, w, h)
    
    def track(self, image_whole):
        success, box = self.tracker.update(image_whole)
        
        if success:
            self.lost_time = None
            self.isTracking = True
            box_x = box[0] / image_whole.shape[1]
            box_y = box[1] / image_whole.shape[0]
            box_w = box[2] / image_whole.shape[1]
            box_h = box[3] / image_whole.shape[0]
            
            self.x, self.y, self.w, self.h = box_x, box_y, box_w, box_h
            
            my_rect = (self.x, self.y, self.w, self.h)
            for trk in Tracker.AllTrackers:
                trk_rect = (trk.x, trk.y, trk.w, trk.h)
                intersect_rect = Utils.intersection(my_rect, trk_rect)
                ar = Utils.area(intersect_rect)
                #if ar > 0:
                #    return -1
        else:
            if self.lost_time is None:
                self.lost_time = time()
                print("Lost tracker {}".format(self.id))
                self.isTracking = False
            if time() - self.lost_time > 2.0:
                print("Removing tracker {}".format(self.id))
                Tracker.AllTrackers.remove(self)


class Detector:
    scale = 1.2
    minN = 3
    
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
                    Tracker(o, img)
            frameNo += 1