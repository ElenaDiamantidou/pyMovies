import sys, os, cv2
import numpy as np

imgPath = sys.argv[1]
img = cv2.imread(imgPath)
#find image info
height, width, channels = img.shape
print height,width,channels
