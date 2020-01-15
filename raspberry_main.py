from camera import Camera
from tracker import Detector, Tracker
from motors import MotorController
from utils import Utils
import webinterface

import cv2

if __name__ == "__main__":
    Camera.begin()
    MotorController.begin()
    webinterface.begin()
    
    detector = Detector()
    detector.begin()
    
    for img in Camera.waitFrame():
        #Update trackers
        for trk in Tracker.AllTrackers:
            a = trk.track(img)
            if a == -1:
                Tracker.AllTrackers.remove(trk)
                break
        
        draw = img.copy()
        #Draw trackers
        for t in Tracker.AllTrackers:
            x, y, w, h = t.getPosTupleImage(draw)
            color = (0, 0, 255)
            if t.isTracking:
                color = (0, 255, 0)
            
            text = "ID {}".format(t.id)
            cv2.putText(draw, text, (x - 10, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.rectangle(draw, (x, y), (x + w, y + h), color)
        
        '''
        if len(Tracker.AllTrackers) > 1:
            for j in range(len(Tracker.AllTrackers)):
                trk = Tracker.AllTrackers[j]
                for i in range(j+1, len(Tracker.AllTrackers)):
                    intersect_rect = Utils.intersection(trk.getPosTupleImage(draw), Tracker.AllTrackers[i].getPosTupleImage(draw))
                    cv2.rectangle(draw, (intersect_rect[0], intersect_rect[1]), (intersect_rect[0] + intersect_rect[2], intersect_rect[1]+intersect_rect[3]), (255, 0, 0))
        '''
        
        cv2.imshow("Win", draw)
        k = cv2.waitKey(16)
        
        if k == ord("s"):
            box = cv2.selectROI("Win", img, fromCenter=False,
                showCrosshair=True)
            Tracker(box, img)
        
        if k == ord('q') or k == 27:
            break
    
    print("Quit")
    detector.end()
    Camera.end()
    cv2.destroyAllWindows()