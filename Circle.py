class Circle(object):
    def __init__(self, coords, radius):
        object.__init__(self)
        self.setCoords(coords)
        self.setRadius(radius)

    def setCircle(self, coords, radius):
        self.setCoords(coords)
        self.setRadius(radius)

    def setCoords(self, coords):
        self.coords = coords

    def setRadius(self, radius):
        if radius >= 1:
            self.radius = radius
        else:
            self.radius = 1

    def getCircle(self):
        return (self.coords, self.radius)

    def getCircle(self):
        return self.coords

    def getCoords(self):
        return self.coords
        
    def getRadius(self):
        return self.radius

    def printCircle(self):
        print("(%d, %d), %d" %(self.coords[0], self.coords[1], self.radius))
