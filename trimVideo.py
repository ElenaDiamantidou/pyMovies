'''
trim a movie [segmetation]
execute
python trimVideo.py movieFile startTime endTime
**startTime and endTime count to minutes
'''

import sys, os
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

movie = sys.argv[1]
start = int(sys.argv[2]) * 60
end = int(sys.argv[3]) * 60
count = sys.argv[4]
targetName = movie.split('.')
print targetName, type(targetName)
targetName = targetName[0] + '_' + count + '.mp4'
ffmpeg_extract_subclip(movie, start, end, targetName)
