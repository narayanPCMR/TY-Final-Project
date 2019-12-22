import os
import cv2
from tqdm import tqdm
from multiprocessing import Pool
import random
from augment import rotate_image

toDoFolders = dict()
pics_person_folders = "originalpics"
people_name = os.listdir(pics_person_folders)

for person in people_name:
    files_person = os.listdir(pics_person_folders + "/" + person)
    for persons_file in files_person:
        if os.path.isdir(pics_person_folders + "/" + person + "/" + persons_file):
            if pics_person_folders+"_"+person not in toDoFolders.keys():
                toDoFolders[pics_person_folders+"_"+person] = []
            toDoFolders[pics_person_folders+"_"+person].append({"folder": pics_person_folders + "/" + person, "name": persons_file})


def blurDetect(image):
    return cv2.Laplacian(image, cv2.CV_64F).var()


def processBatch(image_group):
    print(image_group)
    return
    img_counter = 1
    #template_image_file = image_group["folder"] + "/" + image_group["name"] + ".png"
    #template_image = cv2.imread(template_image_file)
    backSub = cv2.createBackgroundSubtractorMOG2()
    
    all_images = os.listdir(image_group["folder"] + "/" + image_group["name"])
    all_images = [(image_group["folder"] + "/" + image_group["name"] + "/" + y) for y in all_images if (y[-4:]==".jpg" or y[-4:]==".png")]
    
    #original_template_image = template_image.copy()
    #mVal = 0
    
    print(image_group["folder"] + "/" + image_group["name"])
    
    for image_file in tqdm(all_images):
        try:
            img = cv2.imread(image_file)
        
            w = img.shape[1]
            small_img = cv2.resize(img, (1280, 720))
            blAmt = blurDetect(small_img)
            if ((w < 1000 and blAmt < 10) or (w >= 1000 and blAmt < 130)):
                continue
            
            fgMask = backSub.apply(img)
            
            cv2.imshow('FG Mask', fgMask)
            
            #template_w, template_h = template_image.shape[1], template_image.shape[0]
            #res = cv2.matchTemplate(img, template_image, cv2.TM_CCOEFF)
            #min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            
            #if max_val < 12000000:
            #    continue
            
            #top_left = max_loc
            #bottom_right = (top_left[0] + template_w, top_left[1] + template_h)
            
            #cropped = img[top_left[1]:bottom_right[1],top_left[0]:bottom_right[0]]
            
            #if abs(max_val-mVal)>1000000:
            #if random.random() < 0.4:
            #    template_image = cropped
            
            #if random.random() < 0.45:
            #    template_image = original_template_image
            
            image_filename = "pos/" + folder + "_" + image_group["name"] + "_" + str(img_counter) + ".png"
            cropped = cv2.resize(cropped, (200, 200))
            
            #cv2.imwrite(image_filename, cropped)
            #mVal = 0
            
            img_counter += 1
        
            #if mVal == 0:
            #    mVal = max_val
        except:
            print("Error")
                
if __name__ == "__main__":
    p = Pool(1)#len(toDoFolders))
    for folder in toDoFolders:
        p.map(processBatch, toDoFolders[folder])
    p.close()
    p.join()