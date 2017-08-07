# pyMovies
shot detection, feature extract

**NEED TO INSTALL** <br />
OpenCV 3.0 <br />
Numpy <br />
Scipy <br />

**Files** <br />
#### shotDetection_HD.py <br />
Shot Detection using Histogram differences <br />
HD computes the difference between the histograms of two consecutive frames <br />
a histogram is a table that contains for each color within a frame the number of pixels that are shaded in that color <br />

#### shotDetection_ECR.py <br />
Shot Detection using Edge change ratio <br />
The ECR attempts to compare the actual content of two frames. <br />
It transforms both frames to edge pictures, i. e. it extracts the probable outlines of objects within the pictures <br />

#### renameShots.py <br />
rename files from a directory to <br />
Shot_xx.avi <br />
_help to annotate files_
