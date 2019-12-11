from camera import Camera
from tracker import Detector, Tracker

import cv2

if __name__ == "__main__":
    Camera.begin()
    
    detector = Detector()
    detector.begin()
    
    for img in Camera.waitFrame():
        #a = 0
        for t in Tracker.AllTrackers:
            x, y, w, h = t.getPosTupleImage(img)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0))
            #cv2.imshow("W" + str(a), t.trackedImg)
            #a += 1
        
        cv2.imshow("Win", img)
        k = cv2.waitKey(16)
        if k == ord('q') or k == 27:
            break
    
    print("Quit")
    detector.end()
    Camera.end()
    cv2.destroyAllWindows()