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
    dataSet = []
    trainingData = []

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
    model = ""
    try:
        model = load_model(modelPath)
    except:
        model = Sequential()
        model.add(Dense(20, input_dim = 21, activation = "relu")) #We can screw around with these later
        model.add(Dense(25, activation = "relu")) #to figure out what works best for the model
        model.add(Dense(30, activation = "sigmoid"))
        model.compile(loss = 'binary_crossentropy', optimizer = 'adam', metrics = ['accuracy'])
        model.save(modelPath)

    def __init__(self, dataBase):
        self.processData(dataBase)

        #print(self.chars)
        #print(self.dataSet)
        #print(self.trainingData)
        #print(self.letters)
        #print(self.revLetters)


    def processData(self, db):
        """Processes the data into a format usable by training. This is called as part of initialization."""
        for i in db:
            tags = i.getTags()
            chs = []
            charsRand = []

            for j in range(len(tags)): #Gets all of the tags, and builds char list
                if (tags[j].getTruth()):
                    if(tags[j].get() not in self.revChars):
                        self.chars[len(self.chars)] = tags[j].get()
                        self.revChars[tags[j].get()] = len(self.revChars)
                else:
                    if("!" + tags[j].get() not in self.revChars):
                        self.chars[len(self.chars)] = "!" + tags[j].get()
                        self.revChars["!" + tags[j].get()] = len(self.revChars)

            for j in tags: #Converts the tags into numbers, based on our char list
                if(j.getTruth()):
                    chs.append(self.revChars[j.get()])
                else:
                    chs.append(self.revChars["!" + j.get()])
            self.dataSet.append([i.get(), i.getCat(), chs]) #Adds them to dataSet

            if(len(chs) >= 20):
                charsRand = Rd.sample(chs, k = 20) #Gets 20 random characteristics
            else:
                charsRand = Rd.sample(chs, k = len(chs))
            self.trainingData.append([i.get(), i.getCat(), charsRand])

    def train(self, epochs = 20):
        """Trains the model."""
        X = []
        y = []

        for i in self.trainingData:
            row = [] #Creating X data
            row.append(self.revCats[i[1]])
            for j in i[2]:
                row.append(j)

            characters = [] #Creating Y data
            for j in i[0]:
                characters.append(self.revLetters[j])
            if(len(characters) < 30): #Making sure that the rest of characters is filled with 0s.
                for j in range(len(characters), 30):
                    characters.append(0)

            X.append(row)
            y.append(characters)

        print(X)
        print(np.shape(X))
        print(y)
        print(np.shape(y))

        self.model.fit(np.array(X), np.array(y), epochs = epochs)
        self.model.save(self.modelPath)