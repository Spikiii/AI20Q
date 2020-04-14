class characteristic:
    charName = ""
    truthVal = True
    qType = 0

    def __init__(self, cn = "", tv = True, qTyped = 0):
        self.charName = cn.lower()
        self.truthVal = tv
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

    def getQType(self):
        """Returns the question type of the object"""
        return self.qType

    def setQType(self, q):
        """Sets the question type of the object."""
        self.qType = q