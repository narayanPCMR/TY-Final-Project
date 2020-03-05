from camera import Camera
from claw import Arm
from tracker import Detector, Tracker
from motors import MotorController
from utils import Utils
from time import sleep, time
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
    Tracker.begin()
    
    arm = Arm()
    
    webinterface.setClawObj(arm)
    
    Utils.pickupPhase = 0
    frameNumber = 0
    
    print("Starting")
    
    for img in Camera.waitFrame():
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
        
        Distance.loop()
        
        if Utils.pickupPhase == 3:
            arm.openClaw()
            arm.armReach()
            arm.closeClaw()
            arm.armRestingPos()
            print("paper ball grabbed")
            Utils.pickupPhase=4
        
        if Utils.pickupPhase == 4:
            arm.rotateClawBack()
            arm.openClaw()
            arm.rotateClawFront()
            arm.closeClaw()
            print("paper ball put in dustbin")
            Utils.pickupPhase=0
            
        if Utils.pickupPhase == 2:
            if len(Tracker.AllTrackers) > 0:
                t = time()
                
                while time() - t < 0.3:
                    d = Distance.distance()
                    
                    if d <= 12.0:
                        Utils.pickupPhase = 3
                        break
                    
                    tObj = Tracker.AllTrackers[0]
                    
                    #print("Tracker at:", tObj.x, tObj.y, tObj.w, tObj.h)
                    
                    #Calculate middle of rectangle, which is the actual value
                    actualX = (tObj.x+tObj.w/2)
                    targetX = 0.5
                    xError = targetX - actualX
                    
                    print("Error value is {:.3f}".format(xError))
                    
                    turnSpeed = xError * TURNFACTOR
                    
                    MotorController.customControl((0.7 + turnSpeed, 0.7 - turnSpeed))
                    
                    #~ 2 frames
                    sleep(0.05)
                MotorController.stop()
            else:
                #Object lost, go back to detecting
                Utils.pickupPhase = 0
        
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
    Tracker.end()
    Camera.end()
    cv2.destroyAllWindows()
