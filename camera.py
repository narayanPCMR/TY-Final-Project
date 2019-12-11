from cv2 import VideoCapture, waitKey, resize, putText, FONT_HERSHEY_SIMPLEX, LINE_AA, getTextSize
from numpy import zeros
import threading
from time import time, sleep

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