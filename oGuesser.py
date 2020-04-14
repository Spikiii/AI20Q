import random as Rd
from keras.models import Sequential
from keras.layers import Dense
from keras.models import load_model
from keras.optimizers import SGD
import numpy as np

class oGuesser:
    #Initializations
    data = []
    charDictPath = ""

    #Settings
    modelPath = "Models/oGuesser.h5"
    vb = 0 #Verbose
    vs = 0.1 #Validation split
    bs = 32 #Batch size

    #Dictionaries
    chars = {} #Characteristics as {n:characteristic}
    revChars = {} #Characteristics as {characteristic:n}
    cats = {0:"animal", 1:"plant", 2:"mineral", 3:"other"} #Categories
    revCats = {"animal":0, "plant":1, "mineral":2, "other":3}

    #Setting up stuff for Keras
    model = []
    try:
        model = load_model(modelPath)
    except:
        model = Sequential()
        model.add(Dense(40, input_dim = 41, activation = "relu"))
        model.add(Dense(35, activation = "relu"))
        model.add(Dense(30, activation = "sigmoid"))

        opt = SGD(lr = 0.1, decay = 1e-6, momentum = 0.9)
        model.compile(loss = 'binary_crossentropy', optimizer = opt, metrics = ['accuracy'])
        model.save(modelPath)

    def __init__(self, dB, cD):
        for i in dB:
            self.data.append([i.get(), i.getCat(), i.getTags(), i.getQType()])
        self.charDictPath = cD

        self.buildChars()

        #print(self.chars)
        #print(self.trainingData)

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

    def shuffleChars(self, chs):
        """Shuffles an array of characteristics."""
        if(len(chs) >= 20):
            chsRand = Rd.sample(chs, k = 20) #Gets 20 random indexes
        else:
            chsRand = Rd.sample(chs, k = len(chs))

        return chsRand

    def processChars(self, chs):
        """Shuffles an array of 20 characteristics given by chs, and processes it into the format used for training."""
        charsRand = self.shuffleChars(chs)
        processedChars = []

        for i in charsRand:
            processedChars.append(self.revChars[i.get()] / (len(self.chars) - 1))
            if(i.getTruth()):
                processedChars.append(1)
            else:
                processedChars.append(0)

        #Making sure that there are exactly 20 characteristics + truth values, and adding 0s if not.
        if(len(processedChars) < 40):
            for j in range(len(processedChars), 40):
                processedChars.append(0)

        return(processedChars)

    def train(self, epochs = 500):
        """Trains the model."""
        X = []
        y = []

        for i in self.data:
            row = [self.revCats[i[1]]]  # Creating X data
            row += self.processChars(i[2])

            characters = []  # Creating Y data
            for j in i[0]:
                characters.append(self.revLetters[j] / (len(self.revLetters)))
            if(len(characters) < 30):  # Making sure that the rest of characters is filled with spaces.
                for j in range(len(characters), 30):
                    characters.append(self.revLetters[" "] / (len(self.revLetters) - 1))

            X.append(row)
            y.append(characters)

        hist = self.model.fit(np.array(X), np.array(y), batch_size = self.bs, epochs = epochs, verbose = self.vb, validation_split = self.vs)
        print("Acc:", hist.history["accuracy"][-1], "Loss:", hist.history["loss"][-1])

        self.model.save(self.modelPath)

    def guessObject(self, g):
        """Guesses an object based on a characteristic array passed in. Will be updated to accept gameStates when those are implemented."""

        chars = []

        #Get the category and add it to the start of the array
        try:
            chars.append(self.revCats[g.getCategory().lower()])
        except:
            print("::Error in category name::")
            chars.append(3) #Assumes its an 'other' if there's an error

        chars += self.processChars(g.getChars())

        prediction = self.model.predict(np.array([chars]))
        predictionString = ""

        #Converting the prediction into integers for the letter dictionary
        for i in range(0, len(prediction[0])):
            prediction[0][i] = round(prediction[0][i] * (len(self.letters) - 1))
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