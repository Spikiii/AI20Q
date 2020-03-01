class characteristic:
    charName = ""
    aliases = []

    def __init__(self, cn = "", als = []):
        self.charName = cn
        self.aliases = als

    def get(self):
        """Gets this characteristic's name."""
        return self.charName

    def set(self, n):
        """Sets this characteristic's name."""
        self.charName = n

    def getAliases(self):
        """Gets a list of all characteristics """
        return self.aliases

    def addAlias(self, a):
        """Adds a new alias to this characteristic"""
        self.aliases.append(a)