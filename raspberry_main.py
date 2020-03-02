from camera import Camera
from claw import Arm
from tracker import Detector, Tracker
from motors import MotorController
from utils import Utils
from time import sleep
from Stage0 import Distance
import webinterface

import cv2

turnSpeed = 0.0

TURNFACTOR = 0.4

if __name__ == "__main__":
    Camera.begin()
    MotorController.begin()
    webinterface.begin()
    Distance.begin()
    
    detector = Detector()
    detector.begin()
    
    Utils.pickupPhase = 0
    frameNumber = 0
    
    
    for img in Camera.waitFrame():
        MotorController.stop()
        
        #Update trackers
        for trk in Tracker.AllTrackers:
            #if frameNumber % 2 == 0:
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
        
        if Utils.pickupPhase == 0:
            d = Distance.distance()
            if(d < 20):
                print("Checking if any paper is detected...")
                detections = detector.detect(img)
                if len(detections) > 0:
                    print("Paper detected! Moving to phase 1")
                    Utils.pickupPhase = 1
                    #Utils.pickupPhase = 2
                else:
                    print("Nope! not paper, will turn around")
                    while Distance.distance() < 20:
                        print("Spinning round and round")
                        MotorController.right()
                        #sleep(0.05)
                    MotorController.stop()
                    
        if Utils.pickupPhase == 3:
            Arm.openClaw()
            Arm.armReach()
            Arm.closeClaw()
            Arm.armRestingPos()
            print("paper ball grabbed")
            Utils.pickupPhase=4
        
        if Utils.pickupPhase == 4:
            Arm.rotateClawBack()
            Arm.rotateClawFront()
            Arm.openClaw()
            print("paper ball put in dustbin")
            Utils.pickupPhase=0
            
        if Utils.pickupPhase == 2:
            if len(Tracker.AllTrackers) > 0:
                tObj = Tracker.AllTrackers[0]
                
                #print("Tracker at:", tObj.x, tObj.y, tObj.w, tObj.h)
                
                #Calculate middle of rectangle, which is the actual value
                actualX = (tObj.x+tObj.w/2)
                targetX = 0.5
                xError = targetX - actualX
                
                print("Error value is {:.3f}".format(xError))
                
                turnSpeed = xError * TURNFACTOR
                
                MotorController.customControl((0.7 + turnSpeed, 0.7 - turnSpeed))
                sleep(0.1)
            else:
                #Object lost, go back to detecting
                Utils.pickupPhase = 0
        
        '''
        if len(Tracker.AllTrackers) > 1:
            for j in range(len(Tracker.AllTrackers)):
                trk = Tracker.AllTrackers[j]
                for i in range(j+1, len(Tracker.AllTrackers)):
                    intersect_rect = Utils.intersection(trk.getPosTupleImage(draw), Tracker.AllTrackers[i].getPosTupleImage(draw))
                    cv2.rectangle(draw, (intersect_rect[0], intersect_rect[1]), (intersect_rect[0] + intersect_rect[2], intersect_rect[1]+intersect_rect[3]), (255, 0, 0))
        '''
        
        frameNumber += 1
        cv2.imshow("Win", draw)
        k = cv2.waitKey(16)
        
        if k == ord("s"):
            box = cv2.selectROI("Win", img, fromCenter=False,
                showCrosshair=True)
            bbox = [0,0,0,0]
            bbox[0] = box[0] / img.shape[1]
            bbox[1] = box[1] / img.shape[0]
            bbox[2] = box[2] / img.shape[1]
            bbox[3] = box[3] / img.shape[0]
            Tracker(bbox, img)
            Utils.pickupPhase = 2
        
        if k == ord("c"):
            Tracker.AllTrackers = []
            Utils.pickupPhase = 0
        
        if k == ord('q') or k == 27:
            break
    
    print("Quit")
    MotorController.stop()
    detector.end()
    Camera.end()
    cv2.destroyAllWindows()
