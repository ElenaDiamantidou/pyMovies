import tensorflow as tf
from PIL import Image
import numpy as np
from scipy import misc
import os, sys, cv2, glob

directory = sys.argv[1]
files = directory + "*.png"
splt = directory.split('/')
newDirectory = splt[0] + "_NP"
count = 0
if not os.path.exists(newDirectory):
	os.makedirs(newDirectory)

for image_path in glob.glob(files):
	imgPNG = misc.imread(image_path)
	imgNPY = np.asarray(imgPNG)
	imgFileName = splt[0] + "_" + str(count) + ".npy"
	count += 1
	os.chdir(newDirectory)
	np.save(imgFileName,imgNPY)
	os.chdir("../")
