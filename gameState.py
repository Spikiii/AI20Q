import dataNode

class gameState:
    charsKnown = []
    objectsGuessed = []
    category = ""

    def __init__(self, cat = ""):
        self.category = cat

    def getChars(self):#return the chars known
        return self.charsKnown

    def getObjs(self):#returns the list of objects guessed so far
        return self.objectsGuessed

    def getCategory(self):#gets the category of the game
        return self.category

    def addChar(self, char):#adds a characteristic to the list
        charsKnown.append(char)

    def addObj(self, object):#adds an object to the list of
        objectsGuessed.append(object)
