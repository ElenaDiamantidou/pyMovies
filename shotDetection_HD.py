'''
Shot Detection using Histogram differences
HD computes the difference between the histograms of two consecutive frames
a histogram is a table that contains for each color within a frame the number of pixels that are shaded in that color
Difference Threshold = 15%
Save shots > 1MB to .avi

#execute ->
#python shotDetection_HD.py  movie.mp4 (.avi .mov etc)
Use CTRL+C to terminate each video shot detection
'''

import cv2, time, sys, glob, os
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
	success = True
	mov = []

	#create directory to save shots
	folderName = fileName[0] + '_HD'
	if not os.path.exists(folderName):
		os.makedirs(folderName)

	vidCap = cv2.VideoCapture(argv)
	framerate = vidCap.get(cv2.CAP_PROP_FPS)
	#first frame
	success,image = vidCap.read()
	grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	#first histogram to compare
	histName = str(count)
	hist_ = cv2.calcHist([grayImage],[0],None,[256],[0,256])
	os.chdir(folderName)

    #initialize video writer
	height , width  =  grayImage.shape
	fourcc = cv2.VideoWriter_fourcc('X', 'V' ,'I', 'D')
	#add zero parameter for grayscale video
	videoFileName = fileName[0] + '_Shot' + str(shotCounter) +'.avi'
	video = cv2.VideoWriter(videoFileName,fourcc, framerate, (width,height))

	#count frames of video
	try:
	    while (vidCap.isOpened()):
			#print('Read a new frame: ', success)
			success,image = vidCap.read()
			image = cv2.medianBlur(image,5)
			if  success == True:
				grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
				#convert to uint8 for writing ndarrays to video
				grayImage = grayImage.astype('uint8')
				image = image.astype('uint8')

				thr = cv2.adaptiveThreshold(grayImage, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 5, 10)
				print thr
				#adaptive Threshold

				#histogram
				histName = str(count)
				hist = cv2.calcHist([grayImage],[0],None,[256],[0,256])
				#hist = cv2.normalize(hist).flatten()
				#plt.clf()
				#plt.hist(grayImage.ravel(),256,[0,256])
				#plt.savefig(histName)

				#plt.imshow(thr, cmap = 'gray')
				#plt.show()

				#compare histograms
				histDiff_ = histDiff
				histDiff = cv2.compareHist(hist_, hist, cv2.HISTCMP_BHATTACHARYYA)
				diff = abs(histDiff_ - histDiff)

				if diff > 0.15:
					shotCounter += 1
					videoFileName = fileName[0] + '_Shot' + str(shotCounter) +'.avi'
					video = cv2.VideoWriter(videoFileName,fourcc, framerate, (width,height))
				hist_ = hist
				video.write(image)
				#cv2.imshow('frame',grayImage)
				#if cv2.waitKey(1) & 0xFF == ord('q'):
				#    break

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
