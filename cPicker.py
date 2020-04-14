import characteristic as char
import random as Rd
import numpy as np

class cPicker:
    #Initializations
    dataBase = []
    trainingData = []
    charDictPath = ""

    #Settings
    modelPath = "Models/cPicker.h5"
    vb = 0 #Verbose

    #Dictionaries
    chars = {}  # Characteristics as {n:characteristic}
    revChars = {}  # Characteristics as {characteristic:n}
    qTypes = {} # Dictionary linking {characteristic:qType}

    def __init__(self, dB, cD):
        self.dataBase = dB
        self.charDictPath = cD

        self.loadChars()

    def buildChars(self):
        """Builds a characteristic dictionary from the database."""
        for i in self.dataBase:
            tags = i.getTags()
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
                self.qTypes[line[1]] = int(line[2])

    def getChar(self, gameState):
        """Gets a characteristic to ask about."""

        """if gameState.getCategory() == "animal":
            return char.characteristic("flying")
        elif gameState.getCategory() == "plant":
            return char.characteristic("bark")
        elif  gameState.getCategory() == "mineral":
            return char.characteristic("precious")
        else:
            return char.characteristic("living")"""
        picked = char.characteristic(Rd.choice(list(self.revChars.keys()))) #Gets a random characteristic from the characteristic dictionary
        picked.setQType(self.chars[picked.get()])
        return picked
        #TODO, above is demo code
