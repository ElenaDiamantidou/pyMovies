import cv2, time, sys, glob, os, math
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from numpy import array
import scipy
import csv

# initialize OpenCV methods for histogram comparison
#OPENCV 3.0 Methods
OPENCV_METHODS = (
	("Correlation", cv2.HISTCMP_CORREL),
	("Chi-Squared", cv2.HISTCMP_CHISQR),
	("Intersection", cv2.HISTCMP_INTERSECT),
	("Hellinger", cv2.HISTCMP_BHATTACHARYYA))


def main(argv):
	fileName = argv.split('.')
	count = shotCounter = 0
	histDiff = histDiff_ = 0
	fgmask = fgmask_ = 0
	success = True
	intensity = []

	#create directory to save shots
	folderName = fileName[0] + '_HD'
	if not os.path.exists(folderName):
		os.makedirs(folderName)

	vidCap = cv2.VideoCapture(argv)

	#initialize Background Subtraction Technique
	fgbg = cv2.createBackgroundSubtractorMOG2()
	vidCap.set(cv2.CAP_PROP_POS_FRAMES,2000)
	#count frames of video
	#counter = 50000
	try:
	    while (vidCap.isOpened()):
			success,image = vidCap.read()
			image = cv2.medianBlur(image,5)
			if  success == True:
				grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
				#convert to uint8 for writing ndarrays to video
				grayImage = grayImage.astype('uint8')
				image = image.astype('uint8')
				fgmask = fgbg.apply(grayImage)

				#histogram
				hist = cv2.calcHist([fgmask],[0],None,[256],[0,256])
				hist = int(hist[0])
				intensity.append(hist)

			else:
				break
	#use Ctrl+C to interrupt video and save shots
	except KeyboardInterrupt:
		pass

	#normalize
	norm = [float(i)/max(intensity) for i in intensity]
	#calculate average
	summury = sum(norm)
	m = summury/len(norm)
	print m
	vidCap.release()

if __name__ == '__main__':
	start_time = time.time()
	#read input file
	print 'INTENSITY --- ' + sys.argv[1]
	main(sys.argv[1])

	print("--- %s minutes ---" % ((time.time()/60) - (start_time/60)))
	#print also frames
	cv2.destroyAllWindows()
