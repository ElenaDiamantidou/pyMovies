import scipy as sp
from scipy.misc import imread, imshow
import cv2, time, sys, glob, os, math
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from numpy import array




img = imread('nao.jpg')
img1 = imread('lotr1.png')

grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
grayImage_ = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

#grayImage = grayImage.astype('uint8')
grayImage_ = grayImage_.astype('uint8')

#diff = abs(grayImage - grayImage_)
print img
#array = data.tolist()
#thefile = open('map.txt', 'w')
#for item in array:
  #thefile.write("%s\n" % item)
