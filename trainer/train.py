import os
import augment
import makeData

#====================
#Parameter tuning
#====================

#==== Environment ====
OPENCV_CREATESAMPLES_LOCATION = "opencv_createsamples.exe"

OPENCV_TRAINCASCADE_LOCATION = "opencv_traincascade.exe"

OUTPUT_DIR = "output"

#==== Basic ====

#Number of stages of cascade - Don't keep above 20 (it will take forever)
STAGES = 14

#How much % of positive images to actually use - keep below 1.00, but above 0.50
PERCENT_POS = 0.80


#Where the output will be saved
#Best to name this based on parameters
#Leave blank to disable
#[NOTE] Works only on Linux (due to tee command)
LOG_FILE = ""


#================ WARNING ================
#If you change any parameter from here, delete the "output" folder before starting


#==== Cascade Parameters ====

#Can be HAAR, LBP or HOG (HOG does not work on OpenCV anymore)
FEATURE_TYPE = "HAAR"

#Image resolution - Keep below 25 and above 16
#This will also serve as the number of unique features
IMGSIZE = 20


#==== Boost Parameters ====
#(These may improve accuracy and/or speed of training)

#Boost Type - Can be DAB, RAB, LB, GAB (this is default)
BOOST_TYPE = "RAB"

#Maximum False-alarm rate - Keep below 1.0, idk the conditions of this
MAX_FA_RATE = 0.5


#==== HAAR Feature Parameters ====
#(Does not work if using other feature)

#Mode - Can be BASIC, CORE, ALL
HAAR_FEATURE_MODE = "BASIC"


#====================
#End of Parameter tuning
#====================



#DO NOT TOUCH THIS
augpos = False
augneg = False


#====================
#Set up the folder for training.
#This is only done once, and
#skipped after training starts
#====================

if not os.path.exists(OUTPUT_DIR):
    os.mkdir(OUTPUT_DIR)

if not os.path.exists(OUTPUT_DIR+"/data"):
    os.mkdir(OUTPUT_DIR+"/data")

if not os.path.exists(OUTPUT_DIR+"/data/params.xml"):
    if not os.path.exists(OUTPUT_DIR+"/p"):
        os.mkdir(OUTPUT_DIR+"/p")
        augpos = True
    if not os.path.exists(OUTPUT_DIR+"/n"):
        os.mkdir(OUTPUT_DIR+"/n")
        augneg = True
    
    augment.augment(augpos, augneg, IMGSIZE, OUTPUT_DIR)
    
    makeData.makeData(IMGSIZE, OUTPUT_DIR)
    
    numPos = len(os.listdir(OUTPUT_DIR+"/p"))
    
    os.system(r"{0} -info {1}/paper.info -num {2} -w {3} -h {3} -vec {1}/paper.vec".format(OPENCV_CREATESAMPLES_LOCATION, OUTPUT_DIR, numPos, IMGSIZE))

numPosT = int(len(os.listdir(OUTPUT_DIR+"/p")) * PERCENT_POS)
numNegT = len(os.listdir(OUTPUT_DIR+"/p"))


#========================================================
#This is where training happens
#
#It can take a very long time - even days
#Press Ctrl+C to stop at any time
#Run this script again to resume
#
#Delete the "output" (OUTPUT_DIR) folder to restart everything
#Do not delete anything else
#
#The parameters can be adjusted from the constants
#at the beginning of the file.
#Some parameters (numPos, numNeg, ...) are handled
#automatically
#========================================================

log_cmd = ""
if LOG_FILE is not "":
    log_cmd = "| tee -a \"{}\"".format(LOG_FILE)

os.system(r"{0} -data {1}/data -vec {1}/paper.vec -bg {1}/bg.txt -numPos {2} -numNeg {3} -numStages {4} -w {5} -h {5} -featureType {6} -bt {7} -mode {8} -maxFalseAlarmRate {9} {10}".format(OPENCV_TRAINCASCADE_LOCATION, OUTPUT_DIR, numPosT, numNegT, STAGES, IMGSIZE, FEATURE_TYPE, BOOST_TYPE, HAAR_FEATURE_MODE, MAX_FA_RATE, log_cmd))