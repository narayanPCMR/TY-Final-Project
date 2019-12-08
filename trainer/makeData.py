import os
from tqdm import tqdm

#python.exe .\augment.py
#python.exe .\makeData.py
#opencv_createsamples.exe -info .\paper.info -num 68 -w 24 -h 24 -vec paper.vec
#opencv_createsamples.exe -vec .\paper.vec -w 24 -h 24
#opencv_traincascade.exe -data data -vec .\paper.vec -bg .\bg.txt -numPos 60 -numNeg 600 -numStages 18 -w 24 -h 24 -featureType LBP

if __name__ == "__main__":
    print("Do not run this script")
    print("run \"train.py\"")
    exit()
    
def makeData(size, out_dir):
    print("Creating paper.info")
    pos = os.listdir(out_dir+"/p")
    with open(out_dir+"/paper.info", "w") as f:
        for x in tqdm(pos):
            f.writelines("{} 1 0 0 {} {}\n".format("p/"+x, size, size))

    print("Creating bg.txt")
    neg = os.listdir(out_dir+"/n")
    with open(out_dir+"/bg.txt", "w") as f:
        for x in tqdm(neg):
            f.writelines("{}\n".format(out_dir+"/n/"+x))