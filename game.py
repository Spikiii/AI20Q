import dataNode as Dn
import characteristic as Char
from characteristic import characteristic as ch
import oGuesser as oG
import gameState as gS
import cPicker as cP
import qBuilder as qB
#import oGuesser as oG
import nonMLOGuesser as oG

#Initializations
dataBase = []
game = gS.gameState()

#Settings
dataPath = "data/data.txt"
charDictPath = "data/charDict.txt"

def buildDataBase():
    """Builds the database that the AI will use. Make sure to run this before anything else."""
    rawData = []
    with open(dataPath, "r") as f: #Reads through the data line by line
        for line in f:
            rawData.append(line[:-1])

    for i in rawData: #Ignores any line that has a # at its start or is empty
        if(i != "" and i[0] != "#"):
            line = i.split(",")
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

def ui_screen():
    """The introductory UI screen for the text-based version of the game. Used as part of playGame(). """
    print("What mode do you want to use? '[G]ame' or '[D]ata'")
    mode = input("> ") #figure out which user class this user is in
    mode = mode.lower()
    modeSelecting = True
    while(modeSelecting):
        if mode == "data" or mode == "d":
            print("This feature isn't implemented yet, but it will be in the future.")
            print("Please select '[G]ame' for this demo.")
            print("")
            mode = input("What mode do you want to use? '[G]ame' or '[D]ata'")
        elif mode == "game" or mode == "g":
            modeSelecting = False
            print("Please enter your category: '[A]nimal', '[P]lant', '[M]ineral', or '[O]ther'.")
            input1 = input("> ")
            input1 = input1.lower()
            categorySelecting = True
            while(categorySelecting):
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
                else:
                    print("Please enter a valid category.")
                    input1 = input("> ")
                    print("")
        else:
            print("Please enter a valid mode.")
            mode = input("> ")
            print("")

def playGame():
    """Plays the game!"""

    ui_screen()
    questions = 0  # keeps track of number of questions asked
    playing = True  # keeps track of whether the player is still playing
    while (playing):
        questions += 1  # increment questions
        char = cP.getChar(game)  # get the characteristic to check about this round
        print(qB.getQuestion(char) + " [y/n]")
        ans = input("> ")  # builds a question and asks the user
        entering = True
        while (entering):
            if ans == "y":  # set the truth value of the  characteristic
                char.setTruth(True)
                entering = False
            elif ans == "n":
                char.setTruth(False)
                entering = False
            else:
                print("Please enter [y] or [n].")
                ans = input("> ")

        game.addChar(char)  # update the gameState

        ## TODO: guess if we have a high enough confidence value

        if questions == 19:
            guess = oG.guessObject(game)
            print("I think it is a [" + guess[0] + "]")
            input("Is this correct? [y/n]\n")
            playing = False

    print("Thank you for playing!")
    return guess

buildDataBase()

oG = oG.oGuesser(dataBase, charDictPath)
cP = cP.cPicker(dataBase, charDictPath)
qB = qB.qBuilder()

playGame()

#for i in range(0,1):
#    oG.train()
#    print("Test with 'Tomato':", oG.guessObject(gS.gameState("plant", "vegetable,red skin,red inside,sour flavor,medium size,round shaped,thin stem")))
#    print("Test with some of 'Duck':", oG.guessObject(gS.gameState("animal","living,larger than breadbox,can walk,can fly,can swim,lays eggs,!mammal,!rodent,bird,!has fur,has feathers")))
#    print()
