import dataNode as Dn
import characteristic as Char
#import oGuesser as oG
import gameState as Gs
import cPicker as cP
import qBuilder as qB
import nonMLOGuesser as oG

#Initializations
dataBase = []

#Settings
charDictPath = "data/charDict.txt"
dataPath = "data/data.txt"
confidenceGuess = 0.5 #Controls the confidence that the AI is willing to guess at
minQuestions = 10 #Minimum number of questions to wait before guessing

#Dictionaries
charDict = {} #Characteristic dictionary as {characteristic:(id,qtype)}

def loadData(cDP = charDictPath, dP = dataPath):
    """Loads the data specified at dataPath."""
    global charDict
    global dataBase

    rawCharDict = []
    rawData = []

    #Clearing out the old charDict and dataBase
    charDict = {}
    dataBase = []


    #Reads through the characteristic dictionary file line by line
    with open(cDP, "r") as f:
        for line in f:
            rawCharDict.append(line[:-1])

    #Creates charDict
    for i in rawCharDict:
        if(i != "" and i[0] != "#"): #Ignores any line that has a # at its start or is empty
            line = i.split(",")
            charDict[line[1]] = (int(line[0]), int(line[2]))

    #Reads through the data file line by line
    with open(dP, "r") as f:
        for line in f:
            rawData.append(line[:-1])

    #Creates dataBase
    for i in rawData:
        if(i != "" and i[0] != "#"): #Ignores any line that has a # at its start or is empty
            line = i.split(",")
            chars = []
            for j in range(2, len(line)):
                charName = str.lower(line[j])
                if(line[j][0] == "!"):
                    c = Char.characteristic(charName[1:], False, charDict[charName[1:]][1])
                else:
                    c = Char.characteristic(charName, True, charDict[charName][1])
                chars.append(c)

            dn = Dn.dataNode(str.lower(line[0]), str.lower(line[1]), chars)
            dataBase.append(dn)

def saveData(cPD = charDictPath, dP = dataPath):
    """Saves the data to the file specified at dataPath."""
    global charDict
    global dataBase

    #Creating charDict file
    charLines = []
    tags = []
    charLines.append("#Character Dictionary")
    charLines.append("#ID,char,qtype")
    charLines.append("")

    #Converts everything in qDict to a string format for export
    id = 0
    for i in dataBase:
        for j in i.getTags():
            if(j.get() not in tags):
                tags.append(j.get())
                try:
                    charLines.append(str(id) + "," + j.get() + "," + str(charDict[j.get()][1]))
                except:
                    charLines.append(str(id) + "," + j.get() + "," + "-1")
                id += 1

    #Write charLines into cPD
    with open(cPD, "w") as f:
        for i in charLines:
            f.write(str(i) + "\n")
        f.write("\n#END OF FILE#")
    f.close()

    #Creating dataBase file
    dataLines = []
    dataLines.append("#Data set")
    dataLines.append("#other name,category,char1,char2,...")
    dataLines.append("#Categories: animal,plant,mineral,other")
    dataLines.append("")

    #Converts everything in dataBase to a string format for export
    for i in dataBase:
        chs = i.get() + "," + i.getCat()
        for j in i.getTags():
            if(j.getTruth()):
                chs += "," + j.get()
            else:
                chs += "," + "!" + j.get()
        dataLines.append(chs)

    #Write dataLines into dP
    with open(dP, "w") as f:
        for i in dataLines:
            f.write(str(i) + "\n")
        f.write("\n#END OF FILE#")
    f.close()

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

def playGame():
    """Starts the game, and controls the overarching gameplay logic."""
    exitCode = None
    while(exitCode is None):
        exitCode = mainMenu()
        print("")

def mainMenu():
    """The introductory UI screen for the text-based version of the game."""
    print("Welcome to 20 Questions!")
    print("Enter [q]uit at any point to exit.")
    print("")
    print("What mode do you want to use? '[G]ame' or '[D]ata'")
    mode = input("> ") #figure out which user class this user is in
    mode = mode.lower()
    modeSelecting = True
    while(modeSelecting):
        if mode == "game" or mode == "g":
            modeSelecting = False
            play20Q()
            return
        elif mode == "data" or mode == "d":
            modeSelecting = False
            dataMode()
            return
        elif mode == "quit" or mode == "q":
            return "EXIT"
        else:
            print("Please enter a valid mode.")
            mode = str.lower(input("> "))

def dataMode():
    """Data exploration mode"""
    modeSelecting = True
    mode = ""

    print("Please select a mode: 'Search by [o]bject', 'Search by [c]haracteristic', 'Search by [s]imilarity'.")
    input1 = str.lower(input("> "))
    while(modeSelecting):
        if input1 == "search by object" or input1 == "object" or input1 == "o":
            modeSelecting = False
            mode = "o"
        elif input1 == "search by characteristic" or input1 == "characteristic" or input1 == "c":
            modeSelecting = False
            mode = "c"
        elif input1 == "search by similarity" or input1 == "similarity" or input1 == "s":
            modeSelecting = False
            mode = "s"
        elif input1 == "quit" or input1 == "q":
            return
        else:
            print("Please enter a valid mode.")
            input1 = str.lower(input("> "))

    objSearching = True
    while(objSearching):
        obj = ("",0)
        if(mode == "o"):
            print("Please enter the object you would like to search for:")
            input2 = str.lower(input("> "))
            for i in dataBase:
                if(i.get() == input2):
                    obj = (input2,dataBase.index(i))
            if(obj == ("",0)):
                print("It looks like your object was not found in the database.")
                getObjFeedBack(input2)

            else:
                print("[" + str(len(dataBase[obj[1]].getTags())) + "] characteristics associated with [" + obj[0] + "]:")
                for i in dataBase[obj[1]].getTags():
                    print(" " + i.get())

            entrySelecting = True

            print("Would you like to search for another object?[y/n]")
            input1 = input("> ")

            while(entrySelecting):
                if (input1 == "yes" or input1 == "y"):
                    entrySelecting = False
                    objSearching = True
                elif (input1 == "no" or input1 == "n" or input1 == "quit" or input1 == "q"):
                    return
                else:
                    print("Please enter [y] or [n].")
                    input1 = str.lower(input("> "))

        elif(mode == "s"):
            print("Please enter the object you would like to search for:")
            input2 = str.lower(input("> "))
            for i in dataBase:
                if(i.get() == input2):
                    obj = (input2,dataBase.index(i))
            if(obj == ("",0)):
                print("It looks like your object was not found in the database.")
                getObjFeedBack(input2)
            else:
                #Calculating all similarities
                dataBase[obj[1]].calcSim(dataBase)
                sims = dataBase[obj[1]].getSims()
                for i in list(sims.keys()):
                    if(sims[i] < confidenceGuess):
                        sims.pop(i)

                sims.pop(obj[0]) #Making sure that obj is not in the list

                print("[" + str(len(sims)) + "] objects with high similarity associated with [" + obj[0] + "]:")
                if(len(sims) == 0):
                    print("")
                else:
                    for i in sims:
                        print(" " + i)
                    print("")

            entrySelecting = True

            print("Would you like to search for another object?[y/n]")
            input1 = input("> ")

            while(entrySelecting):
                if (input1 == "yes" or input1 == "y"):
                    entrySelecting = False
                    objSearching = True
                elif (input1 == "no" or input1 == "n" or input1 == "quit" or input1 == "q"):
                    return
                else:
                    print("Please enter [y] or [n].")
                    input1 = str.lower(input("> "))

        elif(mode == "c"):
            print("Please enter the characteristic you would like to search for:")
            input2 = str.lower(input("> "))
            for i in dataBase:
                for j in i.getTags():
                    if (input2 == j.get()):
                        obj = (input2, dataBase.index(i))
            if(obj == ("", 0)):
                print("It looks like that characteristic was not found in the database.")
            else:
                charCount = 0
                objs = []
                for i in dataBase:
                    charFound = False
                    for j in i.getTags():
                        if(obj[0] == j.get() and j.getTruth()):
                            charCount += 1
                            charFound = True
                    if(charFound):
                        objs.append(i)

                print("[" + str(len(objs)) + "] objects with the characteristic [" + obj[0] + "]:")
                for i in objs:
                    print(" " + i.get())

            entrySelecting = True

            print("Would you like to search for another characteristic?[y/n]")
            input1 = input("> ")

            while(entrySelecting):
                if (input1 == "yes" or input1 == "y"):
                    entrySelecting = False
                    objSearching = True
                elif (input1 == "no" or input1 == "n" or input1 == "quit" or input1 == "q"):
                    return
                else:
                    print("Please enter [y] or [n].")
                    input1 = str.lower(input("> "))

        else:
            print("::Error in mode selection::")

def getObjFeedBack(obj):
    """Gets a response from the user to whether or not they would like to create an entry, and then to enter some characteristics."""

    entrySelecting = True

    print("Would you like to create an entry for [" + obj + "]? [y/n]")
    input1 = input("> ")

    while(entrySelecting):
        if(input1 == "yes" or input1 == "y"):
            entrySelecting = False
        elif(input1 == "no" or input1 == "n" or input1 == "quit" or input1 == "q"):
            return
        else:
            print("Please enter [y] or [n].")
            input1 = str.lower(input("> "))

    categorySelecting = True
    cat = ""

    print("Please enter the category of [" + obj + "]: '[A]nimal', '[P]lant', '[M]ineral', or '[O]ther'.")
    input2 = str.lower(input("> "))
    while (categorySelecting):
        if input2 == "animal" or input2 == "a":
            categorySelecting = False
            cat = "animal"
        elif input2 == "plant" or input2 == "p":
            categorySelecting = False
            cat = "plant"
        elif input2 == "mineral" or input2 == "m":
            categorySelecting = False
            cat = "mineral"
        elif input2 == "other" or input2 == "o":
            categorySelecting = False
            cat = "other"
        elif input2 == "quit" or input2 == "q":
            return
        else:
            print("Please enter a valid category.")
            input2 = str.lower(input("> "))

    print("Please enter 3 - 5 characteristics of [" + obj + "].")
    print("If you would like to negate a characteristic, put a ! before the characteristic.")
    print("For example, if your object is [mouse], !wings means that a mouse does not have wings.")
    print("If you do not want to enter a characteristic, just press enter.")

    charsRaw = []
    chars = []

    for i in range(1, 6):
        charsRaw.append(input(str(i) + ". "))
    for i in charsRaw:
        if(i != "" and i[0] == "!"):
            chars.append(Char.characteristic(i[1:], False, -1))
        elif(i != "" and i[0] != "!"):
            chars.append(Char.characteristic(i, True, -1))
    dataBase.append(Dn.dataNode(obj, cat, chars))
    saveData()

    print("Entry created.")

def play20Q():
    """Plays the game!"""
    categorySelecting = True

    print("Please enter your category: '[A]nimal', '[P]lant', '[M]ineral', or '[O]ther'.")
    input1 = str.lower(input("> "))
    while (categorySelecting):
        if input1 == "animal" or input1 == "a":
            categorySelecting = False
            game.setCategory("animal")
        elif input1 == "plant" or input1 == "p":
            categorySelecting = False
            game.setCategory("plant")
        elif input1 == "mineral" or input1 == "m":
            categorySelecting = False
            game.setCategory("mineral")
        elif input1 == "other" or input1 == "o":
            categorySelecting = False
            game.setCategory("other")
        elif input1 == "quit" or input1 == "q":
            return
        else:
            print("Please enter a valid category.")
            input1 = str.lower(input("> "))

    questions = 0  # keeps track of number of questions asked
    playing = True  # keeps track of whether the player is still playing

    while (playing and questions <= 19):
        questions += 1  # increment questions
        guess = oG.guessObject(game)

        if((guess[1] >= confidenceGuess and questions >= minQuestions and guess[0] not in game.getObjs()) or questions == 20):
            print(str(questions) + ". I think it is a [" + guess[0] + "]")
            print("Is this correct? [y/n]")
            ans = str.lower(input("> "))
            entering = True
            game.addObj(guess[0])

            while(entering):
                if(ans == "y" or ans == "yes"):
                    playing = False
                    entering = False
                    addChars(guess[0], game)
                elif(ans == "n" or ans == "no"):
                    entering = False
                elif(ans == "quit" or ans == "q"):
                    return
                else:
                    print("Please enter [y] or [n].")
                    ans = str.lower(input("> "))
        else:
            obj = []
            for i in dataBase:
                    if(i.get() == guess[0]):
                        obj = i
            char = cP.getChar(game, obj)  # get the characteristic to check about this round
            print(str(questions) + ". " + qB.getQuestion(char) + " [y/n]")
            ans = str.lower(input("> "))  # builds a question and asks the user
            entering = True
            while (entering):
                if ans == "y" or ans == "yes":  # set the truth value of the  characteristic
                    char.setTruth(True)
                    entering = False
                elif ans == "n" or ans == "no":
                    char.setTruth(False)
                    entering = False
                elif ans == "quit" or ans == "q":
                    return
                else:
                    print("Please enter [y] or [n].")
                    ans = str.lower(input("> "))

            game.addChar(char)  # update the gameState

    print("Thank you for playing!")

def addChars(obj, g):
    """Adds the characteristics defined in a gamestate g to an object, obj."""
    objs = []
    for i in dataBase:
        objs.append(i.get())
    dataBase[objs.index(obj)].addTag(g.getChars())
    saveData()

loadData()
saveData()

#Game initializations
oG = oG.oGuesser(dataBase)
cP = cP.cPicker(dataBase, charDict)
qB = qB.qBuilder()
game = Gs.gameState()

playGame()

#for i in range(0,1):
#    oG.train()
#    print("Test with 'Tomato':", oG.guessObject(Gs.gameState("plant", "vegetable,red skin,red inside,sour flavor,medium size,round shaped,thin stem")))
#    print("Test with some of 'Duck':", oG.guessObject(Gs.gameState("animal","living,larger than breadbox,can walk,can fly,can swim,lays eggs,!mammal,!rodent,bird,!has fur,has feathers")))
#    print()
