class characteristic:
    charName = ""
    truthVal = True
    aliases = []

    def __init__(self, cn = "", tv = True, als = []):
        self.charName = cn
        self.truthVal = tv
        self.aliases = als

    def get(self):
        """Gets this characteristic's name."""
        return self.charName

    def set(self, n):
        """Sets this characteristic's name."""
        self.charName = n

    def getTruth(self):
        """Gets this characteristic's truth value."""
        return self.truthVal

    def setTruth(self, tv):
        """Sets this characteristic's truth value."""
        self.truthVal = tv

    def getAliases(self):
        """Gets a list of all characteristics """
        return self.aliases

    def addAlias(self, a):
        """Adds a new alias to this characteristic"""
        self.aliases.append(a)