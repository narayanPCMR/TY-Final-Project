import cv2
import numpy as np

VIDEOFILE = '[filename].mp4'
VIDSOURCE = 0

vid = cv2.VideoCapture(VIDSOURCE)

faceCascade = cv2.CascadeClassifier(r'output\data\cascade.xml')

scale = 1.3
minN = 6


oldFaces = []
def putFace(elem):
    global oldFaces
    if len(oldFaces) < 1:
        oldFaces.append(elem)
    else:
        oldFaces = oldFaces[1:] + [elem]
def popOldFrame():
    global oldFaces
    if len(oldFaces)>0:
        oldFaces = oldFaces[1:]

faceHeatMap = None

faces = []
templ = None
frameNo = 0
while True:
    ret, img = vid.read()
    if not ret:
        if VIDSOURCE is not VIDEOFILE:
            print("Please connect a webcam to detect objects, or use a video file")
        break
    img = cv2.resize(img, (320, 240))
    
    b = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    b = cv2.equalizeHist(b)
    
    faces = faceCascade.detectMultiScale(b, scale, minN)
    if len(faces) > 0:
        putFace(faces)
    
    #Draw all faces
    faceHeatMap = np.zeros(img.shape, dtype=np.float32)
    for fList in oldFaces:
        for face in fList:
            cv2.rectangle(img, (face[0], face[1]), (face[0]+face[2], face[1]+face[3]), (0, 255, 0), 2)
            #cv2.putText(img, "Scale: {:.4f}".format(scale), (face[0], face[1]-8), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            faceHeatMap[face[1]:face[1]+face[3], face[0]:face[0]+face[2]] += 0.03
    
    if frameNo % 3 == 0:
        popOldFrame()
    
    #Rescale so opencv can display
    faceHeatMap = faceHeatMap * 255
    faceHeatMap = faceHeatMap.astype(np.uint8)
    heatMap = cv2.applyColorMap(faceHeatMap, cv2.COLORMAP_JET)
    
    cv2.imshow("Heat map", heatMap)
    cv2.imshow("Output", img)
    
    frameNo += 1
    k = cv2.waitKey(30)
    
    if k == 27:
        break

cv2.destroyAllWindows()