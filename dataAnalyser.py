import csv
import sys
import math
import matplotlib
import nltk
import time
import calendar

dataFile = csv.reader(open('whitmanData.txt', 'r'), delimiter=',');
newArray = []
fileToWrite = csv.writer(open('cleanedWhitmanData.txt','w+'),delimiter = ',');
counter = 0
monthIndex = dict((v,k) for k,v in enumerate(calendar.month_abbr))
maxDate = 0;
minDate = 10000000000000000000000000;
for row in dataFile:
	newRow = []

	#add url

	newRow.append(row[0])
	tokens = nltk.word_tokenize(str(row[1]))
	
	letterInfo = ''
	#add participants
	for token in tokens[0:len(tokens)-3]:
		letterInfo = letterInfo + ' ' + str(token)
	newRow.append(letterInfo);

	#add readable date

	tokens = tokens[len(tokens)-3:len(tokens)]

	year = tokens[2]
	if len(year)>4:
		year = year[0:4];
	month = 1
	try:
		month = monthIndex[tokens[1][0:3]]
	except:
		month = 1
		print 'bad month'
	day = tokens[0]
	day = day.replace(',','0');
	day = day.replace('?','0');
	day = day.replace('\xe2',' ')
	day = day.replace('\x80',' ')
	day = day.replace('\x93',' ')
	day = day.replace('\x94',' ')	
	try:
		int(day);
	except:
		day = 1;
		print ' bad day'

	#add 200 so time works

	
	try:
		t = (int(year)+100,int(month), int(day), 0, 0, 0, 0, 0,0)
	except:
		print 'failed time' 
		continue
	#add time since epoch

	newRow.append(tokens[1][0:3] + ' ' + str(day).replace('\xe2\x80\x94','').replace('\xe2\x80\x93','') + ', ' + str(year));
	try:
		sinceEpoch = time.mktime(t)
		print sinceEpoch;
		newRow.append(sinceEpoch)
		if sinceEpoch < minDate:
			minDate = sinceEpoch
		if sinceEpoch > maxDate:
			maxDate = sinceEpoch
	except:
		newRow.append('n/a')
	row[2] = row[2].replace('\n',' ')
	row[2] = row[2].replace('\n',' ')
	row[2] = row[2].replace('\xe2',' ')
	row[2] = row[2].replace('\x80',' ')
	row[2] = row[2].replace('\x93',' ')
	row[2] = row[2].replace('\x94',' ')
	newRow.append(row[2]);
	newArray.append(newRow)
#a = tuple(newArray)
newArray = sorted(newArray, key=lambda newArray_entry: newArray_entry[3])
newArray.append([maxDate-minDate])	
for row in newArray:
	try:
		row[3] = math.fabs(row[3] - minDate)/math.fabs(minDate-maxDate);
		print row[3]
	except:
		pass
	counter = counter + 1
	fileToWrite.writerow(row)

print len(newArray)
	
