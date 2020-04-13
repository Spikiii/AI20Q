import dataNode as Dn
import characteristic as Char
import oGuesser as oG
import gameState as Gs
import cPicker as cP
import qBuilder as qB
#import oGuesser as oG
import nonMLOGuesser as oG

#Initializations
dataBase = []

#Settings
dataPath = "data/data.txt"
charDictPath = "data/charDict.txt"
confidenceGuess = 0.8 #Controls the confidence that the AI is willing to guess at

def loadData(dP = dataPath):
    """Loads the data specified at dataPath."""
    global dataBase

    rawData = []
    dataBase = []

    with open(dP, "r") as f: #Reads through the data line by line
        for line in f:
            rawData.append(line[:-1])

    for i in rawData:
        if(i != "" and i[0] != "#"): #Ignores any line that has a # at its start or is empty
            line = i.split(",")
            chars = []
            for j in range(2, len(line)):
                if(line[j][0] == "!"):
                    c = Char.characteristic(str.lower(line[j][1:]), False)
                else:
                    c = Char.characteristic(str.lower(line[j]), True)
                chars.append(c)

            dn = Dn.dataNode(str.lower(line[0]), str.lower(line[1]), chars)
            dataBase.append(dn)

def saveData(dP = dataPath):
    """Saves the data to the file specified at dataPath."""
    lines = []
    lines.append("#Data set")
    lines.append("#other name,category,char1,char2,...")
    lines.append("#Categories: animal,plant,mineral,other")
    lines.append("")

    #Converts everything in the dataBase to a string format for export
    for i in dataBase:
        chs = i.get() + "," + i.getCat()
        for j in i.getTags():
            if(j.getTruth()):
                chs += "," + j.get()
            else:
                chs += "," + "!" + j.get()
        lines.append(chs)

    with open(dP, "w") as f:
        for i in lines:
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
            print("Please enter your category: '[A]nimal', '[P]lant', '[M]ineral', or '[O]ther'.")
            input1 = str.lower(input("> "))
            categorySelecting = True
            while(categorySelecting):
                if input1 == "animal" or input1 == "a":
                    categorySelecting = False
                    game.setCategory("animal")
                    play20Q()
                elif input1 == "plant" or input1 == "p":
                    categorySelecting = False
                    game.setCategory("plant")
                    play20Q()
                elif input1 == "mineral" or input1 == "m":
                    categorySelecting = False
                    game.setCategory("mineral")
                    play20Q()
                elif input1 == "other" or input1 == "o":
                    categorySelecting = False
                    game.setCategory("other")
                    play20Q()
                elif input1 == "quit" or input1 == "q":
                    return "EXIT"
                else:
                    print("Please enter a valid category.")
                    input1 = str.lower(input("> "))
                    print("")
        elif mode == "data" or mode == "d":
            print("This feature isn't implemented yet, but it will be in the future.")
            print("Please select '[G]ame' for this demo.")
            print("")
            return
        elif mode == "quit" or mode == "q":
            return "EXIT"
        else:
            print("Please enter a valid mode.")
            mode = str.lower(input("> "))
            print("")

def play20Q():
    """Plays the game!"""
    questions = 0  # keeps track of number of questions asked
    playing = True  # keeps track of whether the player is still playing
    while (playing and questions <= 19):
        questions += 1  # increment questions
        guess = oG.guessObject(game)

        if(guess[1] >= confidenceGuess or questions == 20):
            print(str(questions) + ". I think it is a [" + guess[0] + "]")
            print("Is this correct? [y/n]")
            ans = str.lower(input("> "))
            entering = True
            while(entering):
                if(ans == "y" or ans == "yes"):
                    playing = False
                    entering = False
                elif(ans == "n" or ans == "no"):
                    entering = False
                elif(ans == "quit" or ans == "q"):
                    return
                else:
                    print("Please enter [y] or [n].")
                    ans = str.lower(input("> "))
        else:
            char = cP.getChar(game)  # get the characteristic to check about this round
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

loadData()

#Game initializations
oG = oG.oGuesser(dataBase, charDictPath)
cP = cP.cPicker(dataBase, charDictPath)
qB = qB.qBuilder()
game = Gs.gameState()

playGame()

#for i in range(0,1):
#    oG.train()
#    print("Test with 'Tomato':", oG.guessObject(Gs.gameState("plant", "vegetable,red skin,red inside,sour flavor,medium size,round shaped,thin stem")))
#    print("Test with some of 'Duck':", oG.guessObject(Gs.gameState("animal","living,larger than breadbox,can walk,can fly,can swim,lays eggs,!mammal,!rodent,bird,!has fur,has feathers")))
#    print()
