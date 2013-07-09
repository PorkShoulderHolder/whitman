__author__ = 'Lisa'
import csv
import nltk
import pickle
import requests
import json
from jsonmaker import saveToFileAsJson,saveToFileAsBSON

from NE_Tagger import *;

whitmantext = csv.reader(open('cleanedWhitmanData.txt'))
fileToWrite = csv.writer(open('dataWithCities.txt','w+'),delimiter = ',');
dataFile = csv.reader(open('sortedCities.txt','r'),delimiter = ',');



cityArray = []
whitmanArray = []
foundCities = []
dataWithCities = []
dataToPickle = []


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
        print whitmanArray.index(row)/float(len(whitmanArray))
        words =[]
        entry = False
        try:
            entry = NE_Record(str(row[4]),str(row[1]))
            entry.url = str(row[0])
            entry.properDate = str(row[2])

            #date processing
            dateCompnents = word_tokenize(entry.properDate)
            entry.year = dateCompnents[len(dateCompnents) - 1]
            entry.month = dateCompnents[0]
            entry.normalizedTime = row[3]

            words.extend(entry.gpe)
            words.extend(entry.locations)
            words.extend(entry.organizations)
        except Exception as e:
            pass
        for word in words:
            address = binarySearch(word)
            if address:
                newrow = []
                newrow.append(word)
                newrow.append(row[2])
                newrow.append(row[3])
                newrow.append(row[0])
                newrow.append(address)
                try:
                    geocode_url = "http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=true&region=us" % address
                    data = json.loads(requests.get(geocode_url).content)
                    lat = data['results'][0]['geometry']['location']['lat']
                    lng = data['results'][0]['geometry']['location']['lng']
                    newrow.append([lat,lng])
                    if entry:
                        entry.latlngs.append((lat,lng))
                except:
                    newrow.append('n/a')
                newrow.append(address)
                fileToWrite.writerow(newrow)
                foundCities.append(word)
        newRow = row.append(foundCities)
        dataWithCities.append(newRow)
        if entry:
            dataToPickle.append(entry)
    pickle.dump(dataToPickle,open('taggedData.txt','wb'))
    saveToFileAsBSON(dataToPickle,'whitmanbson.bson')
    saveToFileAsJson(dataToPickle,'whitmanjson.json',readable=False)


run()


