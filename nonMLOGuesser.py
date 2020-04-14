import random as Rd
import dataNode as dN
import numpy as np

class oGuesser:
    #Initializations
    dataBase = []
    data = []
    charDictPath = ""

    #Settings

    #Dictionaries
    cats = {0:"animal", 1:"plant", 2:"mineral", 3:"other"} #Categories
    revCats = {"animal":0, "plant":1, "mineral":2, "other":3}

    def __init__(self, dB, cD):
        for i in dB:
            self.data.append([i.get().lower(), i.getCat(), i.getTags()])
            self.dataBase.append(dN.dataNode(i.get().lower(), i.getCat(), i.getTags()))

    def guessObject(self, g):
        """Guesses an object based on a gameState passed in. Returns a tuple of (object, similarity)"""

        dNode = dN.dataNode("",g.getCategory(),g.getChars())
        dNode.calcSim(self.dataBase)
        sims = dNode.getSims()
        revSims = {}

        for i, j in sims.items():
            revSims[j] = i

        maxSim = 0.0
        for i in revSims:
            if(i > maxSim):
                maxSim = i

        return(revSims[maxSim], maxSim)