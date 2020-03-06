from cv2 import VideoCapture, waitKey, resize, putText, FONT_HERSHEY_SIMPLEX, LINE_AA, getTextSize, flip, getRotationMatrix2D, warpAffine
from numpy import zeros
import threading
from time import time, sleep
import numpy as np

RESIZETO_WIDTH = 480
RESIZETO_HEIGHT = 360

class Camera:
    def begin(index = 0):
        Camera.camIdx = index
        Camera.camera = VideoCapture(index)
        Camera.__waitFrameEvent = threading.Event()
        Camera.__stopEvent = threading.Event()
        Camera.__currImg = zeros((RESIZETO_HEIGHT, RESIZETO_WIDTH, 3))
        Camera.__last_correct_frame = time()

        Camera.readThread = threading.Thread(target = Camera.__update)
        Camera.readThread.start()
        return Camera.readThread
    
    def end():
        Camera.__stopEvent.set()
        Camera.readThread.join()

    def rotate_bound(image, angle):
        # grab the dimensions of the image and then determine the
        # center
        (h, w) = image.shape[:2]
        (cX, cY) = (w // 2, h // 2)
        # grab the rotation matrix (applying the negative of the
        # angle to rotate clockwise), then grab the sine and cosine
        # (i.e., the rotation components of the matrix)
        M = getRotationMatrix2D((cX, cY), -angle, 1.0)
        cos = np.abs(M[0, 0])
        sin = np.abs(M[0, 1])
        # compute the new bounding dimensions of the image
        nW = int((h * sin) + (w * cos))
        nH = int((h * cos) + (w * sin))
        # adjust the rotation matrix to take into account translation
        M[0, 2] += (nW / 2) - cX
        M[1, 2] += (nH / 2) - cY
        # perform the actual rotation and return the image
        return warpAffine(image, M, (nW, nH)) 

    def __centerText(text):
        font = FONT_HERSHEY_SIMPLEX
        textsize = getTextSize(text, font, 1, 2)[0]
        textX = int((Camera.__currImg.shape[1] - textsize[0]) / 2)
        textY = int((Camera.__currImg.shape[0] + textsize[1]) / 2)
        putText(Camera.__currImg, text, (textX, textY), font, 1, (8, 16, 255), 2, LINE_AA)

    def __update():
        while not Camera.__stopEvent.is_set():
            ret, img = Camera.camera.read()
            if ret:
                img = Camera.rotate_bound(img, 90)
                #img = resize(img, (RESIZETO_WIDTH, RESIZETO_HEIGHT))
                Camera.__currImg = img
                Camera.__last_correct_frame = time()
            else:
                if time() - Camera.__last_correct_frame > 1.0:
                    Camera.__currImg = zeros((RESIZETO_HEIGHT, RESIZETO_WIDTH, 3))
                    Camera.__centerText("No camera detected!")
                    Camera.__last_correct_frame = time()
                    if not Camera.camera.isOpened():
                        Camera.camera = VideoCapture(Camera.camIdx)

            sleep(0.02)
            Camera.__waitFrameEvent.set()

    def waitFrame(w = RESIZETO_WIDTH, h = RESIZETO_HEIGHT):
        while True:
            Camera.__waitFrameEvent.wait()
            Camera.__waitFrameEvent.clear()
            yield resize(Camera.__currImg, (w, h))