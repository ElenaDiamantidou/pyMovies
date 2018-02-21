import os, sys

if __name__ == '__main__':
	#read keyboard input
	directory = sys.argv[1]
	typeData = sys.argv[2]
	shotCounter = 0

	if not os.path.exists(os.path.dirname(directory)):
		print '--- ' + directory + ' --- NOT A DIRECTORY'
	else:
		os.chdir(directory)
		#print os.listdir('.')
		for fileName in os.listdir("."):
			#print fileName
			newFileName = typeData + '_' + str(shotCounter) + '.png'
			os.rename(fileName, newFileName)
			shotCounter += 1
