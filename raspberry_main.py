from camera import Camera
from claw import Arm
from tracker import Detector, Tracker
from motors import MotorController
from utils import Utils
from time import sleep, time
from Stage0 import Distance
import webinterface
from speech import Speech 

import cv2

turnSpeed = 0.0

TURNFACTOR = -0.6

if __name__ == "__main__":
    Camera.begin()
    MotorController.begin()
    webinterface.begin()
    Distance.begin()
    speech=Speech()
    detector = Detector()
    detector.begin()
    Tracker.begin()
    speech.speak(speech.ON)
    arm = Arm()
    
    webinterface.setClawObj(arm)
    
    Utils.pickupPhase = 0
    frameNumber = 0
    
    print("Starting")
    if Utils.mode == "manual":
        speech.speak(Speech.AUTOOFF)
    else:
        speech.speak(Speech.AUTOON)
    
    for img in Camera.waitFrame():
        draw = img.copy()
        
        #===Begin automatic mode===
        if Utils.mode == "auto":
            Distance.loop()
            
            if Utils.pickupPhase == 3:
                arm.openClaw()
                arm.armReach()
                MotorController.speed = 0.7
                MotorController.forward()
                arm.closeClaw()
                MotorController.speed = 0.9
                MotorController.stop()
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
                Tracker.AllTrackers = []
                
            if Utils.pickupPhase == 2:
                if len(Tracker.AllTrackers) > 0:
                    Tracker.AllTrackers[0].track(img)
                    t = time()
                    
                    while time() - t < 0.2:
                        d = Distance.distance()
                        print(d)
                        
                        if d <= 25.0:
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
                        
                        MotorController.customControl((max(min(0.7 + turnSpeed, 1), 0), max(min(0.7 - turnSpeed, 1), 0)))
                        
                    MotorController.stop()
                    #~ 2 frames
                    #sleep(0.5)
                else:
                    #Object lost, go back to detecting
                    Utils.pickupPhase = 0
        
        #===End of automatic mode===
        
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
            speech.speak(speech.Restart)
            Utils.pickupPhase = 0
        
        if k == ord('m'):
            webinterface.toggleMode()
        
        if k == ord('q') or k == 27:
            speech.speak(speech.OFF)
            break
    
    print("Quit")
    MotorController.stop()
    detector.end()
    Tracker.end()
    Camera.end()
    cv2.destroyAllWindows()
