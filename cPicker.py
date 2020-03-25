class cPicker:

    def getChar(gameState):
        if gameState.getCategory() == "Animal":
            return characteristic("flying", null, null)
        else if gameState.getCategory() == "Plant":
            return characteristic("bark", null, null)
        else if  gameState.getCategory() == "Minera"l:
            return characteristic("precious", null, null)
        #TODO, above is demo code
