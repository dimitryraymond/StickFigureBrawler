from Circle import *

class Hitbox(object):
    def __init__(self, circle = []):
        object.__init__(self)
        self.circle = []
        if len(circle) > 1:
            for unit in circle:
                self.addCircle(unit)        
        
    def addCircle(self, circles):
        self.circle.append(circles)
        #print("circle added")

    def deleteCircle(self, index):
        #make sure you try to delete within bounds
        if index >= 0 and index + 1 <= len(self.circle):
            self.circle.pop(index)
        else:
            print("Tried to delete a circle of index of %d" %index)
            index = 0

    #get the full array of circles for collisions        
    def getCircles(self):
        return self.circle

    #get just one circle
    def getCircle(self, index):
        return self.circle[index]

    def printCircle(self, index):
        printing = self.getCircle(index)
        self.getCircle(index).printCircle()

if __name__ == "__main__":
    a = ((1, 1), 1)
    a = Circle(a[0], a[1])
    asdf = Hitbox((a, a))
    print(asdf.getCircle(1))
    
