import csv
import nltk
import pickle
import requests
import json
from NE_Tagger import NE_Record

whitmantext = csv.reader(open('cleanedWhitmanData.txt'))
datafile = csv.reader(open('sortedCities.txt', 'r'), delimiter=',')
fileToWrite = csv.writer(open('dataWithCities.txt', 'w+'), delimiter=',')

cityArray = []
whitmanArray = []
foundCities = []
dataWithCities = []
dataToPickle = []

for row in datafile:
    cityArray.append(row)

for row in whitmantext:
    whitmanArray.append(row)


def stringComparator(a, b):
    if a == b:
        return 0
    array = [a, b]
    array.sort()
    if a == array[0]:
        return 1
    else:
        return -1


def binarySearch(word):
    word = str(word)
    if word != word.title():
        return False
    high = len(cityArray) - 1;
    low = 0;
    count = 0
    while abs(high - low) > 1:
        count = count + 1
        mid = low + abs(high - low) / 2
        result = stringComparator(word, cityArray[mid][1]);
        if result == -1:
            low = mid;
        elif result == 1:
            high = mid;
        else:
            return word;
    return False