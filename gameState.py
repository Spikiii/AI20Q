import dataNode

class gameState:
    chars = []
    objects = []
    category = ""

    def __init__(self, cat = "", chs = [], objs = []):
        self.category = cat
        self.chars = chs
        self.objects = objs

    def getChars(self):#return the charsGuessed
        return self.chars

    def getObjs(self):#returns the list of objects
        return self.objects

    def getCategory(self):#gets the category of the game
        return self.category

    def addChar(self, char):#adds a characteristic to the list
        self.chars.append(char)

    def addObj(self, object):#adds an object to the list of 
        self.objects.append(object)
