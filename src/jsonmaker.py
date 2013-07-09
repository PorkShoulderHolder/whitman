__author__ = 'Sam'
from json import JSONEncoder,dumps
from random import Random,randrange
import pickle
from bson import json_util


class PythonObjectEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (list, dict, str, unicode, int, float, bool, type(None))):
            return JSONEncoder.default(self, obj)
        return {'_python_object': pickle.dumps(obj)}

#for testing purposes

class Bauble():
    def __init__(self):
        letters = 'qwewrtyasdfzxcv'
        self.nubs = randrange(0,10)
        self.niceness = Random()
        self.name = letters[randrange(0,15)].join('o').join(letters[randrange(0,15)])

def makeJSON(obj):
    return dumps(obj,cls=PythonObjectEncoder,default=lambda o: o.__dict__)

def makeBSON(obj):
    return json_util.dumps(obj,cls=PythonObjectEncoder,default=lambda o: o.__dict__)

def makePrettyJSON(obj):
    return dumps(obj,cls=PythonObjectEncoder,default=lambda o: o.__dict__,indent=4)

def saveToFileAsJSON(obj,filename,readable=False):
    with open(filename, 'w') as outfile:
        if readable:
            outfile.write(makePrettyJSON(obj))
        else:
            outfile.write(makeJSON(obj))


def saveToFileAsBSON(obj,filename):
    with open(filename, 'w') as outfile:
        outfile.write(makeBSON(obj))


