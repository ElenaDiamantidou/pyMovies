import tensorflow as tf
from PIL import Image
import numpy as np
from scipy import misc
import os, sys, cv2, glob

directory = sys.argv[1]
files = directory + "*.png"
splt = directory.split('/')
newDirectory = splt[0] + "_JPG"
count = 0
if not os.path.exists(newDirectory):
	os.makedirs(newDirectory)

for image_path in glob.glob(files):
	imgPNG = cv2.imread(image_path)
	imgFileName = splt[0] + "_" + str(count) + ".jpg"
	count += 1
	os.chdir(newDirectory)
	cv2.imwrite(imgFileName,imgPNG)
	os.chdir("../")
