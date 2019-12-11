# Cascade Classifier training helper

## Requirements
Download opencv <= 3.4 and copy opencv_traincascade.exe, opencv_createsamples.exe and opencv_world347d.dll here
Install tqdm, opencv and numpy for python (using pip)


## Usage
Just run:
python train.py
or
python3 train.py
To begin training.


Before doing that, open train.py in an editor to change parameters if you want.


cropper.py was used to take original pics of the object and crop them automatically
(The original images are not in the current folder)




## Meanings:
train.py - Simplifies the commands and does some checking before running opencv_traincascade
You have to run this script

makeData.py - Creates necessary lists of pos and neg
augment.py - duplicates images with changes

"neg" folder contains random background images that do not contain the object
"pos" folder only contains the object you need (cropped using cropper.py)
"output" folder is created automatically by train.py
	"data" folder contains the training stages files and the output file
	"n", "p" contains processed negative and positive images respectively, done by the script
	"bg.txt" is the list of negative images
	"paper.info" is the list of positive images
	"paper.vec" is created by opencv_createsamples

While training:
	POS count : consumed    <a> : <b>
		a is how many positive images we are feeding, b is how many it is using
	NEG count : acceptanceRatio    <a> : <b>
		a is how many negative images we are feeding, b is the acceptance ratio of positive to negative
			(b can be plotted on a graph vs stage, approaching 0)
			(ideal value is 0.0003)
	In the training table:
		N is the stage it is processing
		HR is Hit Rate
		FA is False Ararm Rate