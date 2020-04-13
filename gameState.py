import characteristic as cs

class gameState:
    category = ""
    charsKnown = []
    objectsGuessed = []

    def __init__(self, cat = "", chs = [], objs = []):
        if(type(chs) is str): #If row pulled directly from data
            chars = str.split(chs,",")
            for i in chars:
                if(i[0] == "!"):
                    self.charsKnown += [cs.characteristic(i[1:], False)]
                else:
                    self.charsKnown += [cs.characteristic(i, True)]
        else: #If list of characteristics passed in
            self.charsKnown = chs

        self.category = cat
        self.objectsGuessed = objs

    def getCategory(self):
        """Gets the category of the game."""
        return self.category

    def setCategory(self, cat):
        """Sets the category of the game."""
        self.category = cat

    def getChars(self):
        """Gets the known characteristics."""
        return self.charsKnown

    def addChar(self, char):
        """Adds a characteristic to the known characteristics list."""
        self.charsKnown.append(char)

    def getObjs(self):
        """Gets the objects that have been guessed so far."""
        return self.objectsGuessed

    def addObj(self, obj):
        """Adds an object to the guessed objects list."""
        self.objectsGuessed.append(obj)