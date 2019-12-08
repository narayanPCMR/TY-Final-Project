import cv2
import os
import random
import numpy as np
from tqdm import tqdm

MINNEGWIDTH = 320
MAXNEGWIDTH = 320

if __name__ == "__main__":
    print("Do not run this script")
    print("run \"train.py\"")
    exit()

def rotate_image(mat, angle):
    """
    https://stackoverflow.com/a/47248339
    Rotates an image (angle in degrees) and expands image to avoid cropping
    """

    height, width = mat.shape[:2] # image shape has 3 dimensions
    image_center = (width/2, height/2) # getRotationMatrix2D needs coordinates in reverse order (width, height) compared to shape

    rotation_mat = cv2.getRotationMatrix2D(image_center, angle, 1.)

    # rotation calculates the cos and sin, taking absolutes of those.
    abs_cos = abs(rotation_mat[0,0]) 
    abs_sin = abs(rotation_mat[0,1])

    # find the new width and height bounds
    bound_w = int(height * abs_sin + width * abs_cos)
    bound_h = int(height * abs_cos + width * abs_sin)

    # subtract old image center (bringing image back to origo) and adding the new image center coordinates
    rotation_mat[0, 2] += bound_w/2 - image_center[0]
    rotation_mat[1, 2] += bound_h/2 - image_center[1]

    # rotate image with the new bounds and translated rotation matrix
    rotated_mat = cv2.warpAffine(mat, rotation_mat, (bound_w, bound_h))
    return rotated_mat

def augment(AugPositive, AugNegative, samplewidth, out_dir):
    if AugPositive:
        print("Augmenting Positive images...")
        pp = os.listdir("pos")
        a = 1
        for x in tqdm(pp):
            im = cv2.imread("pos/"+x)
            height = im.shape[0]
            width = im.shape[1]
            
            aspect = height / width
            
            #TEST
            aspect = 1.0
            
            #Supposed to be equal sizes, but whatever.
            width = samplewidth
            height = width*aspect
            
            for aaa in range(2):
                gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                gray = gray * random.uniform(0.8, 1.0)
                
                #if random.random() > 0.4:
                #    img = cv2.equalizeHist(img)
                img = cv2.resize(gray, (int(width), int(height)))
                cv2.imwrite(out_dir+"/p/"+str(a)+".jpg", img)
                a += 1
        print("Done")
    if AugNegative:
        print("Augmenting Negative images...")
        pp = os.listdir("neg")
        a = 1
        for x in tqdm(pp):
            im = cv2.imread("neg/"+x)
            height = im.shape[0]
            width = im.shape[1]
            aspect = height / width
            maxDim = np.argmax(im.shape)
            
            for aaaaaa in range(2):
                #9:16
                if maxDim == 0:
                    ima = rotate_image(im, 90)
                    height = ima.shape[0]
                    width = ima.shape[1]
                    aspect = height / width
                    w = int(random.uniform(MINNEGWIDTH, MAXNEGWIDTH))
                    h = w*aspect
                    #h = int(random.uniform(400, 700))
                    #w = h / aspect
                #16:9
                else:
                    w = int(random.uniform(MINNEGWIDTH, MAXNEGWIDTH))
                    h = w*aspect
                    ima = im
                
                img = cv2.resize(ima, (int(w), int(h)))
                #if random.random() > 0.5:
                #    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                #    img = cv2.equalizeHist(img)
                #else:
                #hsvImg = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                #rand = random.uniform(0.6, 1.0)
                #hsvImg[:, :, 2] = rand * hsvImg[:, :, 2]
                #img = cv2.cvtColor(hsvImg, cv2.COLOR_HSV2BGR)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                cv2.imwrite(out_dir+"/n/"+str(a)+".jpg", img)
                a += 1
        print("Done")