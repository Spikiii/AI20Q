import characteristic as char
import dataNode as dN
import random as Rd
import numpy as np

class cPicker:
    #Initializations
    data = []
    dataBase = []

    #Settings
    modelPath = "Models/cPicker.h5"
    vb = 0 #Verbose

    #Dictionaries
    chars = {}  # Characteristics as {n:characteristic}
    qTypes = {} # Dictionary linking {characteristic:qType}

    def __init__(self, dB, cD):
        for i in dB:
            self.data.append([i.get().lower(), i.getCat(), i.getTags()])
            self.dataBase.append(dN.dataNode(i.get().lower(), i.getCat(), i.getTags()))
        self.chars = cD

    def getChar(self, gameState, currGuess):
        GChar = Rd.choice(list(self.chars.keys()))
        for i in currGuess.getTags():
            flag = False
            currChar = i.get()
            for k in gameState.getChars():
                if(currChar == k.get()):
                    flag = True
            if (flag == False):
                GChar = i.get()
        picked = char.characteristic(GChar, True, self.chars[GChar][1])  #Gets a random characteristic from the characteristic dictionary
        return picked
