import dataNode as Dn
import characteristic as Char
import random as Rd
#import keras as Ks

class oGuesser:
    #Initializations
    dataSet = []
    trainingData = []
    chars = {} #Characteristics as {n:characteristic}
    revChars = {} #Characteristics as {characteristic:n}

    #Settings


    def __init__(self, dataBase):
        self.processData(dataBase)
        #print(self.chars)
        #print(self.dataSet)
        #print(self.trainingData)


    def processData(self, db):
        """Processes the data into a format usable by training."""
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