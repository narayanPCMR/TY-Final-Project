from camera import Camera
from utils import Utils
from time import time
import threading
import cv2

CASCADE = "data/cascadeold.xml"

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
    trkTh = None
    
    def __init__(self, bbox, img):
        #Position as percentage
        self.x, self.y, self.w, self.h = bbox[0], bbox[1], bbox[2], bbox[3]
        
        x = int(self.x * img.shape[1])
        y = int(self.y * img.shape[0])
        w = int(self.w * img.shape[1])
        h = int(self.h * img.shape[0])
        
        self.trackedImg = img[y:y + h, x:x + w]
        
        print("Added a tracker at:", self.x, self.y, "of size", self.w, self.h)
        
        #Limit to 2 trackers
        #if len(Tracker.AllTrackers) >= 1: return
        
        #ar = -1
        #my_rect = (self.x, self.y, self.w, self.h)
        #for trk in Tracker.AllTrackers:
        #    trk_rect = (trk.x, trk.y, trk.w, trk.h)
        #    intersect_rect = Utils.intersection(my_rect, trk_rect)
        #    ar = Utils.area(intersect_rect)
        #    #if ar > 0: break
        #else:
        #    self.tracker = cv2.TrackerCSRT_create()
        #    self.tracker.init(img, (x, y, w, h))
        #    
        #    #Add the tracker to list of trackers
        #    self.id = Tracker.GlobTrackerID
        #    Tracker.GlobTrackerID += 1
        #    Tracker.AllTrackers.append(self)
        #
        
        self.tracker = cv2.TrackerCSRT_create()
        self.tracker.init(img, (x, y, w, h))
        self.id = Tracker.GlobTrackerID
        Tracker.GlobTrackerID += 1
        Tracker.AllTrackers.append(self)
        
    
    def getPosTupleImage(self, img):
        x, y = int(self.x * img.shape[1]), int(self.y * img.shape[0])
        w, h = int(self.w * img.shape[1]), int(self.h * img.shape[0])
        return (x, y, w, h)
    
    
    def begin():
        #Create a thread
        Tracker.trkTh = threading.Thread(target=Tracker.trackerLoop)
        Tracker.trkStopEv = threading.Event()
        Tracker.trkTh.start()
    
    def end():
        Tracker.trkStopEv.set()
        if Tracker.trkTh != None:
            Tracker.trkTh.join()
    
    def trackerLoop():
        return
        for img in Camera.waitFrame():
            if Tracker.trkStopEv.is_set():
                print("Tracker stopped")
                break
            if Utils.pickupPhase != 2:
                continue
            
            for tr in Tracker.AllTrackers:
                a = trk.track(img)
                
                if a == -1:
                    Tracker.AllTrackers.remove(trk)
                    break
    
    
    def track(self, image_whole):
        success, box = self.tracker.update(image_whole)
        
        if success:
            self.lost_time = None
            self.isTracking = True
            
            box_x = box[0] / image_whole.shape[1]
            box_y = box[1] / image_whole.shape[0]
            box_w = (box[2] / image_whole.shape[1])
            box_h = (box[3] / image_whole.shape[0])
            
            self.x, self.y, self.w, self.h = box_x, box_y, box_w, box_h
        else:
            if self.lost_time is None:
                self.lost_time = time()
                print("Lost tracker {}".format(self.id))
                self.isTracking = False
            if time() - self.lost_time > 2.0:
                print("Removing tracker {}".format(self.id))
                Utils.pickupPhase = 1
                Tracker.AllTrackers.remove(self)


class CascadeDetector:
    scale = 1.12
    minN = 3
    
    def __init__(self):
        self.cascade = cv2.CascadeClassifier(CASCADE)
    
    def detect(self, img):
        b = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        b = cv2.equalizeHist(b)
        detections = self.cascade.detectMultiScale(b, self.scale, self.minN)
        
        return detections

class DNNDetector:
    modelDir = "./data/dnn/"
    
    def __init__(self):
        self.model = cv2.dnn.readNetFromTensorflow(self.modelDir+'frozen_inference_graph.pb', self.modelDir+'frozen_graph.pbtxt')
        self.classNames = open(self.modelDir+'labels.txt').read().split('\n')
    
    def detect(self, image):
        self.model.setInput(
            cv2.dnn.blobFromImage(image, size=(300, 300), swapRB=True, crop = False)
        )
        output = self.model.forward()
        
        detections = []
        for detection in output[0,0,:,:]:
            confidence = detection[2]
            if confidence > .6:
                print("Detection found with confidence:", confidence)
                
                class_id = int(detection[1])
                print("Accepted a paper")
                image_height, image_width, _ = image.shape
                
                box_x = detection[3]
                box_y = detection[4]
                box_width = detection[5] - box_x
                box_height = detection[6] - box_y
                detections.append((box_x, box_y, box_width, box_height))
                
                break
                
        return detections


class Detector(DNNDetector):
    def __init__(self):
        super().__init__()
        
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
        for img in Camera.waitFrame(640, 360):
            if self.detStopEv.is_set():
                break
            
            if Utils.pickupPhase == 1:
                print("Checking...")
                detections = self.detect(img)
                for dtx in detections:
                    Tracker(dtx, img)
                    
                    #Set to next phase
                    Utils.pickupPhase += 1
                    break
