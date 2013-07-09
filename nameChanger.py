import os


for filename in os.listdir("."):
	newName = os.path.splitext(filename)[0] + '_1000x1000'
	newExt = os.path.splitext(filename)[1]	
	os.rename(filename, newName+'.'+newExt)