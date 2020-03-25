import characteristic as char

class cPicker:
    #Initializations
    temp = False

    def __init__(self):
        self.temp = True

    def getChar(self, gameState):
        if gameState.getCategory() == "animal":
            return char.characteristic("flying")
        elif gameState.getCategory() == "plant":
            return char.characteristic("bark")
        elif  gameState.getCategory() == "mineral":
            return char.characteristic("precious")
        else:
            return char.characteristic("living")
        #TODO, above is demo code
