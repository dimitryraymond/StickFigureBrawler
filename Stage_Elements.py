class Platform(object):
    def __init__(self, coords, fallThrough = True):
        object.__init__(self)
        self.setCoords(coords)
        self.setFallThrough(fallThrough)
        
    def setCoords(self, coords):
        self.coords = coords

    def setFallThrough(self, fallThrough):
        self.fallThrough = fallThrough

    def getCoords(self):
        return self.coords

    def getFallThrough(self):
        return self.fallThrough

class Barier(object):
    def __init__(self, coords):
        object.__init__(self)
        self.setCoords(coords)

    def setCoords(self, coords):
        self.coords = coords

    def getCoords(self):
        return self.coords

