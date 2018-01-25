'''
Shot Detection using Edge change ratio
The ECR attempts to compare the actual content of two frames.
It transforms both frames to edge pictures, i. e. it extracts the probable outlines of objects within the pictures
Difference Threshold = 60% similarity
Save shots > 1MB to .avi

#execute ->
#python shotDetection_ECR.py  movie.mp4 (.avi .mov etc)
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
	count = shotCounter = 0
	ecr = ecr_ = 0
	success = True
	mov = []
	dilate_rate = 5

	#create directory to save shots
	folderName = fileName[0] + '_ECR'
	if not os.path.exists(folderName):
		os.makedirs(folderName)

	vidCap = cv2.VideoCapture(argv)
	framerate = vidCap.get(cv2.CAP_PROP_FPS)
	vidCap.set(cv2.CAP_PROP_POS_FRAMES,0)
	#first frame
	success,image = vidCap.read()
	grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	edge_ = cv2.Canny(grayImage, 0, 200)
	dilated_ = cv2.dilate(edge_, np.ones((dilate_rate, dilate_rate)))
	inverted_ = (255 - dilated_)

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
				safe_div = lambda x,y: 0 if y == 0 else x / y
				grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
				#convert to uint8 for writing ndarrays to video
				grayImage = grayImage.astype('uint8')
				image = image.astype('uint8')

				#edge change ratio
				edge = cv2.Canny(grayImage, 0, 200)
				dilated = cv2.dilate(edge, np.ones((dilate_rate, dilate_rate)))
				inverted = (255 - dilated)

				log_and1 = (edge_ & inverted)
				log_and2 = (edge & inverted_)
				pixels_sum_new = np.sum(edge)
				pixels_sum_old = np.sum(edge_)
				out_pixels = np.sum(log_and1)
				in_pixels = np.sum(log_and2)

				ecr = ecr_
				ecr = max(safe_div(float(in_pixels),float(pixels_sum_new)), safe_div(float(out_pixels),float(pixels_sum_old)))
				diff = abs(ecr - ecr_)
				if ecr > 0.7:
					shotCounter += 1
					videoFileName = fileName[0] + '_Shot' + str(shotCounter) +'.avi'
					video = cv2.VideoWriter(videoFileName,fourcc, framerate, (width,height))
				edge_ = edge
				dilated_ = dilated
				inverted_ = inverted
				video.write(image)
				#cv2.imshow('frame',grayImage)
				#if cv2.waitKey(1) & 0xFF == ord('q'):
				    #break

			else:
				break
			count = count + 5
			#vidCap.set(cv2.CAP_PROP_POS_FRAMES,framerate+count)
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
		if os.path.getsize(directory[f]) < 524288:
			os.remove(directory[f])


if __name__ == '__main__':
	#read input file
	start_time = time.time()
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
