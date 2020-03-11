import dataNode as Dn
import characteristic as Char
import random as Rd
from keras.models import Sequential
from keras.layers import Dense
from keras.models import load_model
import numpy as np
from string import ascii_lowercase

class oGuesser:
    #Initializations
    dataBase = []
    trainingData = []
    charDictPath = ""

    #Settings
    modelPath = "Models/oGuesser.h5"

    #Dictionaries
    chars = {} #Characteristics as {n:characteristic}
    revChars = {} #Characteristics as {characteristic:n}
    cats = {0:"animal", 1:"plant", 2:"mineral", 3:"other"} #Categories
    revCats = {"animal":0, "plant":1, "mineral":2, "other":3}
    letters = {index:letter for index, letter in enumerate(ascii_lowercase, start=1)} #Letters as {n:letter}
    revLetters = {letter:index for index, letter in enumerate(ascii_lowercase, start=1)} #Letters as {letter:n}

    #Setting up stuff for Keras
    model = []
    try:
        model = load_model(modelPath)
    except:
        model = Sequential()
        model.add(Dense(20, input_dim = 41, activation = "relu")) #We can screw around with these later
        model.add(Dense(25, activation = "relu")) #to figure out what works best for the model
        model.add(Dense(30, activation = "sigmoid"))
        model.compile(loss = 'binary_crossentropy', optimizer = 'adam', metrics = ['accuracy'])
        model.save(modelPath)

    def __init__(self, dB, cD):
        self.dataBase = dB
        self.charDictPath = cD

        self.processData()

        #print(self.chars)
        #print(self.trainingData)


    def processData(self):
        """Processes the data into a format usable by training. This is called as part of initialization."""
        #Clearing out any previous data
        self.trainingData = []
        self.chars = {}
        self.revChars = {}

        try:
            self.loadChars()
        except:
            self.buildChars()

        for i in self.dataBase:
            tags = i.getTags()
            chs = []
            randIndexes = []
            charsRand = []
            thsRand = []

            for j in tags: #Converts the tags into numbers, based on our char list
                chs.append(self.revChars[j.get()])

            if(len(chs) >= 20):
                randIndexes = Rd.sample(range(0, len(chs)), k = 20) #Gets 20 random indexes
            else:
                randIndexes = Rd.sample(range(0, len(chs)), k = len(chs))

            for j in randIndexes:
                charsRand.append(chs[j])
                thsRand.append(tags[j].getTruth())

            self.trainingData.append([i.get(), i.getCat(), charsRand, thsRand])

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


    def train(self, epochs = 50):
        """Trains the model."""
        X = []
        y = []

        for i in self.trainingData:
            row = [] #Creating X data
            row.append(self.revCats[i[1]])
            for j in range(len(i[2])):
                row.append(i[2][j])
                if(i[3][j]):
                    row.append(1)
                else:
                    row.append(0)

            characters = [] #Creating Y data
            for j in i[0]:
                characters.append(self.revLetters[j])
            if(len(characters) < 30): #Making sure that the rest of characters is filled with 0s.
                for j in range(len(characters), 30):
                    characters.append(0)

            X.append(row)
            y.append(characters)

        #print(X)
        #print(np.shape(X))
        #print(y)
        #print(np.shape(y))

        self.model.fit(np.array(X), np.array(y), epochs = epochs)
        self.model.save(self.modelPath)