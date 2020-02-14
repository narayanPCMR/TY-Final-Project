# import the necessary packages
from imutils.video import VideoStream
from pyzbar import pyzbar
import imutils
import time
import cv2

class QR:
	def detectQR(self,img):
		frame = img
		frame = imutils.resize(frame, width=400)
		# find the barcodes in the frame and decode each of the barcodes
		barcodes = pyzbar.decode(frame)
		# loop over the detected barcodes
		for barcode in barcodes:
			(x, y, w, h) = barcode.rect
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
		cv2.imshow("Barcode Scanner", frame)	