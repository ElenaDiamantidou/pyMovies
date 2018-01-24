import scipy as sp
from scipy.misc import imread, imshow
import cv2, time, sys, glob, os, math
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from numpy import array


# initialize OpenCV methods for histogram comparison
#OPENCV 3.0 Methods
OPENCV_METHODS = (
	("Correlation", cv2.HISTCMP_CORREL),
	("Chi-Squared", cv2.HISTCMP_CHISQR),
	("Intersection", cv2.HISTCMP_INTERSECT),
	("Hellinger", cv2.HISTCMP_BHATTACHARYYA))
fgbg = cv2.createBackgroundSubtractorMOG2()
fgbg_ = cv2.createBackgroundSubtractorMOG2()

img = imread('lotr2.png')
img1 = imread('lotr3.png')

grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#grayImage = grayImage.astype('uint8')
grayImage = grayImage.astype('uint8')

grayImage_ = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
#grayImage = grayImage.astype('uint8')
grayImage_ = grayImage_.astype('uint8')
fgmask = fgbg.apply(grayImage)
fgmask_ = fgbg_.apply(grayImage_)

hist = cv2.calcHist([fgmask],[0],None,[256],[0,256])
hist_ = cv2.calcHist([fgmask_],[0],None,[256],[0,256])
cv2.imwrite('lotr1BS.png',fgmask_)

histName = 'lotr5HD.png'
#hist = cv2.calcHist([fgmask],[0],None,[256],[0,256])
#plt.clf()
#plt.hist(img.ravel(),256,[0,256])
#plt.savefig(histName)
#plt.imshow(thr, cmap = 'gray')
plt.show()
histDiff = cv2.compareHist(hist_, hist, cv2.HISTCMP_BHATTACHARYYA)
print histDiff
