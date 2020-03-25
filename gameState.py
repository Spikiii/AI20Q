import dataNode

class gameState:
    charsKnown = []
    objectsGuessed = []
    category = ""

    def __init__(self, cat = "", chs = [], objs = []):
        self.category = cat
        self.chars = chs
        self.objects = objs

    def getChars(self):#return the chars known
        return self.charsKnown

    def getObjs(self):#returns the list of objects guessed so far
        return self.objectsGuessed

    def getCategory(self):#gets the category of the game
        return self.category

    def addChar(self, char):#adds a characteristic to the list
<<<<<<< HEAD
        charsKnown.append(char)

    def addObj(self, object):#adds an object to the list of
        objectsGuessed.append(object)
=======
        self.chars.append(char)

    def addObj(self, object):#adds an object to the list of 
        self.objects.append(object)
>>>>>>> 9bbf9c1a61350dc50f27077d89eba40954634962
