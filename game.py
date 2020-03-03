import dataNode as Dn
import characteristic as Char

#Global variables
dataPath = "data.txt"
dataBase = []

def buildDataBase():
    """Builds the database that the AI will use. Make sure to run this before anything else."""
    rawData = []
    with open(dataPath) as f: #Reads through the data line by line
        for line in f:
            rawData.append(line[:-1])
    for i in rawData: #Ignores any line that has a # at its start or is empty
        if(i != "" and i[0] != "#"):
            line = i.split(", ")
            chars = []
            for j in range(2, len(line)):
                if(line[j][0] == "!"):
                    c = Char.characteristic(line[j][1:], False)
                else:
                    c = Char.characteristic(line[j], True)
                chars.append(c)

            dn = Dn.dataNode(line[0], line[1], chars)
            dataBase.append(dn)

def printDataBase():
    """Prints out the database. Mostly for testing purposes."""
    for i in dataBase:
        chars = []
        for j in i.getTags():
            if(j.getTruth()):
                chars.append(j.get())
            else:
                chars.append("!" + j.get())
        print(i.get(), i.getCat(), chars)

buildDataBase()
printDataBase()