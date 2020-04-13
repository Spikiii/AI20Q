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
    chars = {} #Characteristics as {n:characteristic}
    revChars = {} #Characteristics as {characteristic:n}
    cats = {0:"animal", 1:"plant", 2:"mineral", 3:"other"} #Categories
    revCats = {"animal":0, "plant":1, "mineral":2, "other":3}

    def __init__(self, dB, cD):
        for i in dB:
            self.data.append([i.get().lower(), i.getCat(), i.getTags()])
            self.dataBase.append(dN.dataNode(i.get().lower(), i.getCat(), i.getTags()))
        self.charDictPath = cD

        #self.buildChars()

    def buildChars(self):
        """Builds a characteristic dictionary from the database."""
        for i in self.data:
            tags = i[2]
            for j in range(len(tags)): #Gets all of the tags, and builds char list
                if(tags[j].get() not in self.revChars):
                    self.chars[len(self.chars)] = tags[j].get()
                    self.revChars[tags[j].get()] = len(self.revChars)
        self.saveChars()

    def saveChars(self):
        """Saves the characteristic dictionary at the path specified at initialization."""
        chs = []
        for i in self.chars:
            chs.append([i, self.chars.get(i)])

        with open(self.charDictPath, "w") as f:
            f.writelines("#Character Dictionary\n")
            f.write("#Don't touch this please. The model will need to retrain if you do.\n")
            f.write("\n")
            for i in chs:
                f.write(str(i[0]) + "," + str(i[1]) + "\n")
            f.write("\n")
            f.write("#END OF FILE#")
        f.close()

    def loadChars(self):
        """Loads in the characteristic dictionary at the path specified at initialization."""
        chsRaw = []
        with open(self.charDictPath, "r") as f:
            for line in f:
                chsRaw.append(line[:-1])

        for i in chsRaw:
            if(i != "" and i[0] != "#"):
                line = i.split(",")
                self.chars[int(line[0])] = line[1]
                self.revChars[line[1]] = int(line[0])

    def train(self, epochs = 500):
        """Does nothing. I mean this is the non-machine learning version of oGuesser."""

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