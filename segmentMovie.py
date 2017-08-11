import cv2, time, sys, glob, os
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import math
from numpy import array
import scipy
import csv

if __name__ == '__main__':
    csvFileName = sys.argv[1]
    fileName = csvFileName.split('.')
    folderName = fileName[0]
    shots = []
    videoFile = sys.argv[2]
    count = shotCounter = duration = 0

    vidCap = cv2.VideoCapture(videoFile)
    framerate = vidCap.get(cv2.CAP_PROP_FPS)
    print framerate
    #print os.getcwd()
    csvFile = open(csvFileName, 'rb')
    read = csv.reader(csvFile)
    for row in read:
        shots.append([row[0], row[1]])


	#first frame
    success,image = vidCap.read()
    grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    height , width  =  grayImage.shape
    videoFileName = fileName[0] + '_Shot' + str(shotCounter) +'.avi'
    fourcc = cv2.VideoWriter_fourcc('X', 'V' ,'I', 'D')
    video = cv2.VideoWriter(videoFileName,fourcc, framerate, (width,height))

    if not os.path.exists(folderName):
        os.makedirs(folderName)
    else:
        os.chdir(folderName)
    #count frames of video
    try:
        while (vidCap.isOpened()):
            success,image = vidCap.read()
            if success == True:
                for i in range(len(shots)):
                    shotStart= int(shots[i][0])
                    shotEnd = int(shots[i][1])
                    if count == shotStart:
                        videoFileName = fileName[0] + '_Shot' + str(shotCounter) +'.avi'
                        video = cv2.VideoWriter(videoFileName,fourcc, fra, (width,height))
                        shotCounter += 1
                        vidCap.set(1,shotEnd)
                        break
                        #shots.remove(shots[i])
                    video.write(image)
            else:
            	break
            count = count + 1

            #use Ctrl+C to interrupt video and save shots
    except KeyboardInterrupt:
        vidCap.release()
        video.release()

    vidCap.release()
    video.release()
