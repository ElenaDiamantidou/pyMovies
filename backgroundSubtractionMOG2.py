'''
Shot Detection using Background Subtraction
Difference Threshold = 15%
Save shots > 1MB to .avi

#execute ->
#python shotDetection_BS.py  movie.mp4 (.avi .mov etc)
Use CTRL+C to terminate each video shot detection
'''

import cv2, time, sys, glob, os
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import math
from numpy import array
import scipy
import csv


def main(argv):
	fileName = argv.split('.')
	count = shotCounter = 0
	fgmask = fgmask_ = 0
	diff = diff_ = 0
	success = True
	distance = []

	#create directory to save shots
	folderName = fileName[0] + '_BS'
	if not os.path.exists(folderName):
		os.makedirs(folderName)

	vidCap = cv2.VideoCapture(argv)
	framerate = vidCap.get(cv2.CAP_PROP_FPS)
	vidCap.set(1, 3000)
	#initialize Background Subtraction Technique
	fgbg = cv2.createBackgroundSubtractorMOG2()
	#first frame
	success,image = vidCap.read()
	grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	os.chdir(folderName)

    #initialize video writer
	height , width  =  grayImage.shape
	fourcc = cv2.VideoWriter_fourcc('X', 'V' ,'I', 'D')
	#add zero parameter for grayscale video
	videoFileName = fileName[0] + '_Shot' + str(shotCounter) +'.avi'
	video = cv2.VideoWriter(videoFileName,fourcc, framerate, (width,height))
	#first frame
	#s = (height, width)
	#inframe = np.zeros(s)
	fgmask_ = fgbg.apply(image)

	#count frames of video
	try:
	    while (vidCap.isOpened()):
			#print('Read a new frame: ', success)
			success,image = vidCap.read()
			image_ = cv2.medianBlur(image,5)
			if  success == True:
				image_ = image_.astype('uint8')
				fgmask = fgbg.apply(image_)

				diff =  np.sum((fgmask_-fgmask)**2)
				distance.append(diff)
				thr = np.mean(distance)
				#diff = abs(fgmask - fgmask_)
				#diff = np.mean(diff)
				#distance = abs(diff - diff_)
				a = math.ceil((abs(diff-thr)).item())
				#print len(str(a))
				if len(str(a)) > 7:
					shotCounter += 1
					#print 'Shot_' + str(shotCounter)
					videoFileName = fileName[0] + '_Shot' + str(shotCounter) +'.avi'
					video = cv2.VideoWriter(videoFileName,fourcc, framerate, (width,height))
				video.write(image)
				fgmask_ = fgmask


				#cv2.imshow('frame',fgmask)
				#if cv2.waitKey(1) & 0xFF == ord('q'):
					#break

			else:
				break
			count = count + 5
	#use Ctrl+C to interrupt video and save shots
	except KeyboardInterrupt:
		tempDelete()

	vidCap.release()
	video.release()

#delete files
def tempDelete():
	print 'clean files'
	directory = os.listdir('.')
	for f in range (len(directory)):
		#return in bytes
		#204800 -> 200KB
		#524288 bytes for mini clips
		#1048576 bytes for movies
		if os.path.getsize(directory[f]) < 1048576:
			os.remove(directory[f])


if __name__ == '__main__':
	start_time = time.time()
	#read input file
	if len(sys.argv) > 2:
		movies = sys.argv
		movies.remove('shotDetectionHistogram.py')
		for mov in range(len(movies)):
			os.chdir('/home/ediamant/Thesis/pyMovies')
			print 'SHOT DETECTION --- ' + movies[mov]
			main(movies[mov])
			tempDelete()
	elif len(sys.argv) == 2:
		mov = sys.argv[1]
		fileName = mov.split('.')
		if fileName[1] == 'csv':
			#check for csv input
			print 'R e a d i n g    C S V'
			with open(mov, 'rb') as csvfile:
				spamreader = csv.reader(csvfile)
				for row in spamreader:
					os.chdir('/home/ediamant/Thesis/pyMovies')
					print 'SHOT DETECTION --- ' + ', '.join(row)
					movie = ', '.join(row)
					main(movie)
					tempDelete()

		else:
			print 'SHOT DETECTION --- ' + sys.argv[1]
			main(sys.argv[1])
			tempDelete()
	else:
		print 'Need movie file input'

	print("--- %s minutes ---" % ((time.time()/60) - (start_time/60)))
	#print also frames
	cv2.destroyAllWindows()
