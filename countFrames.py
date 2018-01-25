'''
Extract and Count Frames from Videos
Save frames > to .png

#execute ->
#python countFrames.py  movie.mp4 (.avi .mov etc)
Use CTRL+C to terminate each video shot detection
'''

import cv2, sys, os, time
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from numpy import array
import scipy
import csv


def main(argv):
	fileName = argv.split('.')
	success = True
	counter = 0
	#create directory to save shots
	folderName = fileName[0] + '_Frames'
	if not os.path.exists(folderName):
		os.makedirs(folderName)
	vidCap = cv2.VideoCapture(argv)
	imgFileName = fileName[0] + '_Frame' + str(counter) +'.png'
	os.chdir(folderName)
	#count frames of video
	try:
	    while (vidCap.isOpened()):
	        #print('Read a new frame: ', success)
			success,image = vidCap.read()
			if  success == True:
				#possible transform img
				grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
				#convert to uint8 for writing ndarrays to video
				grayImage = grayImage.astype('uint8')
				image = image.astype('uint8')
				counter += 1
				imgFileName = fileName[0] + '_Frame' + str(counter) +'.png'
				cv2.imwrite(imgFileName,image)
			else:
				break
	#use Ctrl+C to interrupt video
	except KeyboardInterrupt:
		print counter

	vidCap.release()


if __name__ == '__main__':
	#read input file
	print 'Frames Counter --- ' + sys.argv[1]
	video = sys.argv[1]
	cap = cv2.VideoCapture(video)
	length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
	#for frames extraction call main
	#main(video)
	print(length)
