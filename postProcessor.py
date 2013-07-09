import csv
import sys
import math
import nltk
import matplotlib.pyplot as plt


dataFile = csv.reader(open('cleanedWhitmanData.txt', 'r'), delimiter=',');
sentLen = []
dates = []

for row in dataFile:
	try:
		sentences = nltk.sent_tokenize(str(row[4]))
		words = nltk.word_tokenize(str(row[4]))
		for word in words:
			if len(word) < 2 or word != 'I':
				words.remove(word);
		if len(words)/len(sentences) > 40:
			continue
		dates.append(float(row[3]))
		print row[3]
		sentLen.append(float(len(words))/len(sentences))
	except:
		print 'baad'


def movingavg(period):
	mvgAvg = []
	ma = []
	for value in sentLen:
		if len(mvgAvg) <= period:
			mvgAvg.append(value)
		else:
			mvgAvg.remove(mvgAvg[0])
			mvgAvg.append(value)
		a = 0
		for v in mvgAvg:
			a = a + v
		a = float(a)/len(mvgAvg)
		ma.append(a)
	return ma     

ma = movingavg(200);
print(ma)
plt.plot(dates,ma)
plt.scatter(dates,sentLen,1)
plt.show()

