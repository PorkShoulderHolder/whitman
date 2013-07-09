__author__ = 'Lisa'
import jsonmaker
import pickle

data = pickle.load(open('taggedData.txt'))

wordFrequenciesByYear = []

print len(data)

#year based processing
letters = []
currentYear = 2013
outgoingLetters = 0
incomingLetters = 0
outgoingLetterTraffic = []
outgoingWordTraffic = []
incomingLetterTraffic = []
incomingWordTraffic = []
locations = []
nrmDates = []
outgoingWords = 0
incomingWords = 0
count = 0

def trackYear(ol,ow,il,iw):
    outgoingLetterTraffic.append(ol)
    outgoingWordTraffic.append(ow)
    incomingLetterTraffic.append(il)
    incomingWordTraffic.append(iw)


for letter in data:
    locations.append(letter.latlngs)
    nrmDates.append(letter.normalizedTime)
    if int(letter.year) > currentYear:
        outgoingLetterTraffic.append(outgoingLetters)
        outgoingWordTraffic.append(outgoingWords)
        incomingLetterTraffic.append(incomingLetters)
        incomingWordTraffic.append(incomingWords)
        outgoingWords = 0
        outgoingLetters = 0
        incomingWords = 0
        incomingLetters = 0
    currentYear = int(letter.year)
    try:
        if 'walt' and 'whitman' in letter.sender.lower():
            outgoingLetters += 1
            outgoingWords += len(letter.words)
    except Exception:
        pass
    try:
        if 'walt' and 'whitman' in letter.recipient.lower():
            incomingLetters += 1
            incomingWords += len(letter.words)
    except Exception:
        pass
    if count == len(data) - 1:
        outgoingLetterTraffic.append(outgoingLetters)
        outgoingWordTraffic.append(outgoingWords)
        incomingLetterTraffic.append(incomingLetters)
        incomingWordTraffic.append(incomingWords)
    count += 1

class Datum:
    def __init__(self):
        self.outgoingLetterTraffic = outgoingLetterTraffic
        self.outgoingWordTraffic = outgoingWordTraffic
        self.incomingLetterTraffic = incomingLetterTraffic
        self.incomingWordTraffic = incomingWordTraffic
        self.locations = locations
        self.normalizedDates = nrmDates

class Letter:
    def __init__(self):
        self.locations = locations

d = Datum()
jsonmaker.saveToFileAsBSON(d,'postageTrafficByYear.bson')
jsonmaker.saveToFileAsJson(d,'postageTrafficByYear.json',readable=True)


