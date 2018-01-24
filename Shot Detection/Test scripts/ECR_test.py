import scipy as sp
from scipy.misc import imread, imshow
import cv2, time, sys, glob, os, math
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from numpy import array



dilate_rate = 5
img = imread('lotr4.png')
img1 = imread('lotr5.png')

grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
grayImage_ = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

grayImage = grayImage.astype('uint8')
grayImage_ = grayImage_.astype('uint8')

edge = cv2.Canny(grayImage, 0, 200)
dilated = cv2.dilate(edge, np.ones((dilate_rate, dilate_rate)))
inverted = (255 - dilated)
#cv2.imwrite('lotrECR5.png',inverted)
edge_ = cv2.Canny(grayImage_, 0, 200)
dilated_ = cv2.dilate(edge_, np.ones((dilate_rate, dilate_rate)))
inverted_ = (255 - dilated_)

log_and1 = (edge_ & inverted)
log_and2 = (edge & inverted_)
pixels_sum_new = np.sum(edge)
pixels_sum_old = np.sum(edge_)
out_pixels = np.sum(log_and1)
in_pixels = np.sum(log_and2)

safe_div = lambda x,y: 0 if y == 0 else x / y
ecr = max(safe_div(float(in_pixels),float(pixels_sum_new)), safe_div(float(out_pixels),float(pixels_sum_old)))
print ecr
