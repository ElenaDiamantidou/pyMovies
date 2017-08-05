'''
Shot Detection using histograms
Compare frames histograms
Difference Threshold = 20%
Save shots > 1MB to .avi
'''

import cv2, time, sys, glob, os
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from numpy import array
import scipy
import scipy.signal
import scipy.cluster.hierarchy as hier
import scipy.spatial.distance as dist
import datetime
from scipy.interpolate import interp1d
import collections
import csv

# initialize OpenCV methods for histogram comparison
#OPENCV 3.0 Methods
OPENCV_METHODS = (
	("Correlation", cv2.HISTCMP_CORREL),
	("Chi-Squared", cv2.HISTCMP_CHISQR),
	("Intersection", cv2.HISTCMP_INTERSECT),
	("Hellinger", cv2.HISTCMP_BHATTACHARYYA))
#detect movie shots
#execute ->
#python shotDetection.py  movie.mp4 (.avi .mov etc)

def main(argv):
	fileName = argv.split('.')
	count = shotCounter = 0
	histDiff = histDiff_ = 0
	success = True
	mov = []

	#create directory to save shots
	folderName = fileName[0]
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
	        if  success == True:
	            grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	            #convert to uint8 for writing ndarrays to video
	            grayImage = grayImage.astype('uint8')
	            image = image.astype('uint8')

	            #histogram
	            histName = str(count)
	            hist = cv2.calcHist([grayImage],[0],None,[256],[0,256])
	            #hist = cv2.normalize(hist).flatten()
	            plt.clf()
	            #plt.hist(grayImage.ravel(),256,[0,256])
	            #plt.savefig(histName)

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
	        count = count + 1
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
		if os.path.getsize(directory[f]) < 524288:
			os.remove(directory[f])


if __name__ == '__main__':
	if len(sys.argv) > 2:
		movies = sys.argv
		movies.remove('shotDetectionHistogram.py')
		for mov in range(len(movies)):
			os.chdir('/home/ediamant/Thesis/pyMovies')
			print movies[mov]
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
					print ', '.join(row)
					movie = ', '.join(row)
					main(movie)
					tempDelete()

		else:
			main(sys.argv[1])
			tempDelete()
	else:
		print 'Need movie file input'

	cv2.destroyAllWindows()
