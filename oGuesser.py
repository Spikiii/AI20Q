import random as Rd
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.models import load_model
from keras.optimizers import SGD
import numpy as np

class oGuesser:
    #Initializations
    dataBase = []
    trainingData = []
    charDictPath = ""

    #Settings
    modelPath = "Models/oGuesser.h5"
    vb = 0 #Verbose

    #Dictionaries
    chars = {} #Characteristics as {n:characteristic}
    revChars = {} #Characteristics as {characteristic:n}
    cats = {0:"animal", 1:"plant", 2:"mineral", 3:"other"} #Categories
    revCats = {"animal":0, "plant":1, "mineral":2, "other":3}
    letters = {} #Letters as {n:letter}
    revLetters = {} #Letters as {letter:n}

    #Setting up stuff for Keras
    model = []
    try:
        model = load_model(modelPath)
    except:
        model = Sequential()
        model.add(Dense(40, input_dim = 41, activation = "relu"))
        model.add(Dense(35, activation="sigmoid"))
        model.add(Dense(30, activation = "sigmoid"))

        opt = SGD(lr = 0.000001, decay = 1e-6, momentum = 0.9, nesterov = True)
        model.compile(loss = 'binary_crossentropy', optimizer = opt, metrics = ['accuracy'])
        model.save(modelPath)

    def __init__(self, dB, cD):
        self.dataBase = dB
        self.charDictPath = cD

        self.processData()
        self.buildLetterDict()

        #print(self.chars)
        #print(self.trainingData)

    def processData(self):
        """Processes the data into a format usable by training. This is called as part of initialization."""
        #Clearing out any previous data
        self.trainingData = []
        self.chars = {}
        self.revChars = {}

        self.buildChars()

        #try:
        #    self.loadChars()
        #except:
        #    self.buildChars()

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
                charsRand.append(chs[j] / (len(self.chars) - 1))
                thsRand.append(tags[j].getTruth())

            self.trainingData.append([i.get(), i.getCat(), charsRand, thsRand])

    def buildLetterDict(self):
        """Creates a dictionary of letters. This is called as part of initialization."""
        for i in self.trainingData:
            for j in i[0]:
                if (not j in self.revLetters):
                    self.letters[len(self.letters)] = j
                    self.revLetters[j] = len(self.revLetters)

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

    def train(self, epochs = 1000):
        """Trains the model."""
        X = []
        y = []

        for i in self.trainingData:
            row = []  # Creating X data
            row.append(self.revCats[i[1]])
            for j in range(len(i[2])):
                row.append(i[2][j])
                if (i[3][j]):
                    row.append(1)
                else:
                    row.append(0)
            if(len(row) < 41): # Making sure that the rest of row is filled with 0.
                for j in range(len(row), 41):
                    row.append(0)

            characters = []  # Creating Y data
            for j in i[0]:
                characters.append(self.revLetters[j])
            if(len(characters) < 30):  # Making sure that the rest of characters is filled with spaces.
                for j in range(len(characters), 30):
                    characters.append(self.revLetters[" "])

            X.append(row)
            y.append(characters)

        self.model.fit(np.array(X), np.array(y), epochs = epochs, verbose = self.vb)
        self.model.save(self.modelPath)

    def guessObject(self, g):
        """Guesses an object based on a characteristic array passed in. Will be updated to accept gameStates when those are implemented."""

        chars = []
        charsRaw = g.getChars()

        #Get the category and add it to the start of the array
        try:
            chars.append(self.revCats[g.getCategory()])
        except:
            print("::Error in category name::")
            chars.append(3) #Assumes its an 'other' if there's an error

        #Build the rest of chars, and convert them into numbers
        for i in charsRaw:
            try:
                chars.append(self.revChars[i.get()]) #Adding in the characteristic's ID
                if(i.getTruth()): #Adding in the characteristic's truth value
                    chars.append(1)
                else:
                    chars.append(0)
            except:
                self.chars[len(self.chars)] = i.get()
                self.revChars[i.get()] = len(self.revChars)
                self.saveChars()

                chars.append(self.revChars[i.get()]) #Do the same as ^
                if (i.getTruth()):
                    chars.append(1)
                else:
                    chars.append(0)

        #Makes sure that chars is of the correct length [<20 characteristics]
        if (len(chars) < 41):
            for j in range(len(chars), 41):
                chars.append(0)
        if(len(chars) > 41):
            chars = Rd.sample(chars, k = 41)

        #Normalizing the characteristic values
        for i in range(0, len(chars)):
            chars[i] = chars[i] / (len(self.chars) + 1)

        prediction = self.model.predict(np.array([chars]))
        predictionString = ""

        #Converting the prediction into integers for the letter dictionary
        for i in range(0, len(prediction[0])):
            prediction[0][i] = round(prediction[0][i] * len(self.letters))
            if (prediction[0][i] >= len(self.letters) - 1):
                prediction[0][i] = len(self.letters) - 1
            if (prediction[0][i] < 0):
                prediction[0][i] = 0

        print(prediction)

        #Turning the prediction into a string
        for i in prediction[0]:
            predictionString = predictionString + self.letters[i]

        g.addObj(prediction)
        return predictionString