import characteristic

class dataNode:
    category = ""
    chars = []
    similarities = {}

    def __init__(self, cat = "Other", chs = [], sims = {}):
        self.category = cat
        self.chars = chs
        self.similarities = {}

    def getCat(self):
        """Gets the category of this dataNode."""
        return self.category

    def setCat(self, cat):
        """Sets the category of this dataNode. Make sure that cat is a string."""
        self.category = cat

    def getTags(self):
        """Gets all of the characteristic tags associated with this object"""
        return self.chars

    def addTag(self, chs):
        """Adds the specified characteristic(s). You can pass in either a single characteristic or an array of characteristics"""
        if(type(chs) is list):
            for i in chs:
                self.chars.append(i)
        if(type(chs) is characteristic):
            self.chars.append(chs)
        self.remDupes()

    def remTag(self, ch):
        """Removes the specified characteristic tag. Make sure that ch is a characteristic."""
        self.chars.remove(ch)

    def remDupes(self):
        """Goes through this dataNode's characteristic tag list and removes all duplicates."""
        chs = []
        for i in self.chars:
            if(i.get() in chs):
                self.remTag(i)
            else:
                chs.append(i.get())

    def calcSim(self, n):
        """Calculates the similarities between this dataNode and another dataNode, n."""
        sim = 0.0 #Similarity, ranges from 0.0 (no shared tags) to 1.0 (all shared tags)
        ntags = n.getTags()

        for i in ntags:
            if(i in self.chars):
                sim += 1.0
        for i in self.chars:
            if(i in ntags):
                sim += 1.0
        sim = sim / (ntags.length() + self.chars.length())
        self.similarities[n] = sim

    def getSims(self):
        """Returns this dataNode's similarities. """
        return self.similarities