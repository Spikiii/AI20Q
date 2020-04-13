import characteristic

class dataNode:
    name = ""
    category = ""
    chars = []
    similarities = {}

    def __init__(self, nm = "", cat = "Other", chs = [], sims = {}):
        self.name = nm
        self.category = cat
        self.chars = chs
        self.similarities = {}

    def get(self):
        """Gets the name of this dataNode."""
        return self.name

    def set(self, nm):
        """Sets the name of this dataNode."""
        self.name = nm

    def getCat(self):
        """Gets the category of this dataNode."""
        return self.category

    def setCat(self, cat):
        """Sets the category of this dataNode. Make sure that cat is a string."""
        self.category = cat

    def getTags(self):
        """Gets all of the characteristic tags associated with this object."""
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

    def __cSim(self, n):
        """calcSim is a wrapper method for this method."""
        sim = 0.0  # Similarity, ranges from 0.0 (no shared tags) to 1.0 (all shared tags)

        #Making self's characteristic array
        chs = []
        chs.append(self.category)
        for i in self.chars:
            chs.append(i.get())

        #Making n's characteristic array
        ntags = []
        ntags.append(n.getCat())
        for i in n.getTags():
            ntags.append(i.get())

        #Comparison and calculation
        for i in ntags:
            if (i in chs):
                sim += 1
        for i in chs:
            if (i in ntags):
                sim += 1
        sim = sim / (len(self.chars) + len(ntags) + 1)

        self.similarities[n.get()] = sim

    def calcSim(self, dns):
        """Calculates the similarities between this dataNode and another dataNode, dns. You can pass in either a single dataNode or a list of dataNodes."""
        if(type(dns) is list):
            for i in dns:
                self.__cSim(i)
        if(type(dns) is dataNode):
            self.__cSim(dns)
        self.remDupes()

    def getSims(self):
        """Returns this dataNode's similarities. """
        return self.similarities
