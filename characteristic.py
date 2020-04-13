class characteristic:
    charName = ""
    truthVal = True
    qType = 0
    aliases = []

    def __init__(self, cn = "", tv = True, als = [], qTyped = 0):
        self.charName = cn.lower()
        self.truthVal = tv
        self.aliases = als
        self.qType = qTyped

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

    def getQType(self):
        """Returns the question type of the object"""
        return self.qType

    def setQType(self, q):
        """Sets the question type of the object."""
        self.qType = q