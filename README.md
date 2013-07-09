whitman
=======

A Collection of the tools I made to scrape, analyse, and catalogue all of Walt Whitman's correspondence from 1860 to 1875.
more importantly text, pickled, JSON, and BSON representations of said data.

##NE_Tagger

The NE_Tagger object takes a section of text as well as an optional text heading parameter and then performs the
relevant named entity recognition and populates its people, locations,

    >>>from NE_Tagger import NE_Record

    >>>netagger = NE_Tagger("Dear mother, the heat is awful, please let me come home to Camden, Mass", "Letter from Walt Whitman to his Mother")

    >>>print netagger.sender

    "Walt Whitman"

    >>>print netagger.locations

    ["Camden"]

etc...

##jsonmaker

The jsonmaker object provides a light wrapper for the json module to convert python objects to json/bson files

    >>>from jsonmaker import *

    >>>saveToFileAsJSON(obj,'myfile.json',readable = True)

    >>>saveToFileAsBSON(obj,'myfile.bson)
