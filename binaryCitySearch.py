import csv
import nltk
import pickle
import requests
import json

whitmantext = csv.reader(open('cleanedWhitmanData.txt'))
dataFile = csv.reader(open('sortedCities.txt','r'),delimiter = ',');
fileToWrite = csv.writer(open('dataWithCities.txt','w+'),delimiter = ',');


cityArray = []
whitmanArray = []
dataWithCities = []
for row in dataFile:
	cityArray.append(row)

for row in whitmantext:
	whitmanArray.append(row);

def stringComparator(a,b):
	if a == b:
		return 0
	array = [a,b]
	array.sort()
	if a == array[0]:
		return 1
	else:
		return -1

def binarySearch(word):

	word = str(word)
	if word != word.title():
		return False
	high = len(cityArray)-1;
	low = 0;
	count = 0
	while abs(high-low) > 1:
		count = count +1
		mid = low + abs(high-low)/2
		result = stringComparator(word,cityArray[mid][1]);
		if  result == -1:
			low = mid;
		elif result == 1:
			high = mid;
		else:
			return word;
	return False

def run():
	for row in whitmanArray:
		words =[]
		try:
			words = nltk.word_tokenize(str(row[4]))
			#tokens = nltk.pos_tag(words)
		except:
			continue
		foundCities = []
		for word in words:
			address = binarySearch(word);
			if address:
				newrow = []
				newrow.append(word)
				newrow.append(row[2])
				newrow.append(row[3])
				newrow.append(row[0])
				newrow.append(address)
				try:
					geocode_url = "http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=true&region=us" % address
					print address 
					data = json.loads(requests.get(geocode_url).content)
					lat = data['results'][0]['geometry']['location']['lat']
					lng = data['results'][0]['geometry']['location']['lng']
					newrow.append([lat,lng])
					print [lat,lng]
					
				except:
					newrow.append('n/a')
				newrow.append(address)
				newrow.append
				fileToWrite.writerow(newrow)
				foundCities.append(word)
		newRow = row.append(foundCities)
		dataWithCities.append(newRow)		

run()



