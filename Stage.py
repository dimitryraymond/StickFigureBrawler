import pygame
import linecache
from Stage_Elements import *

class Stage(object):
    def __init__(self, stageFileName):
        object.__init__(self)
        image = None
        platform = []
        barrier = []
        outOfBounds = None
        #the window size will be 1200x600
        #these are nicely spaced starting positions for both of the players
        startingPosition = [[300, 500], [900, 500]]
        #import the stage based on its stageFileName
        self.stageFileName = stageFileName
        self.setImage(self.importImage())
        self.setPlatform(self.importPlatform())
        self.setBarriers(self.importBarriers())
        self.setOutOfBounds(self.importOutOfBounds())
        self.setStartingPositions(self.importStartingPositions())

    #i will use these import function to get the preset contents of a stage
    #that's stored externally
    def importImage(self):
        imageFileName = linecache.getline(self.stageFileName, 1).strip()
        return pygame.image.load(imageFileName).convert()
        
    def importPlatform(self):
        line = linecache.getline(self.stageFileName, 2).strip()
        line = line[2:-2]
        values = line.split(", ")
        values = ((int(values[0]), int(values[1])), (int(values[2]), int(values[3])))
        return Platform(values, False)

    def importBarriers(self):
        pass

    def importOutOfBounds(self):
        line = linecache.getline(self.stageFileName, 4).strip()
        line = line[2:-2]
        values = line.split("], [")
        coords = []
        for value in values:
            coordsStr = value.split(", ")
            coords.append((int(coordsStr[0]), int(coordsStr[1])))
        return coords

    def importStartingPositions(self):
        line = linecache.getline(self.stageFileName, 5).strip()
        line = line[2:-2]
        values = line.split("], [")
        coords = []
        for value in values:
            coordsStr = value.split(", ")
            coords.append((int(coordsStr[0]), int(coordsStr[1])))
        return coords

    def drawElements(self):
        for platform in self.getPlatform():
            pygame.draw.line(self.getImage(), (255, 0, 0), (platform.getCoords()[0], platform.getCoords()[1]),  (platform.getCoords()[2], platform.getCoords()[3]), 3) 
    
    #setter methods
    def setImage(self, image):
        self.image = image

    def setPlatform(self, platform):
        self.platform = [platform]

    def setBarriers(self, barrier):
        self.barrier = barrier

    def setOutOfBounds(self, outOfBounds):
        self.outOfBounds = outOfBounds

    def setStartingPositions(self, startingPositions):
        self.startingPosition = startingPositions

    def addPlatform(self, platform):
        self.platform.append(platform)

    def addBarrier(self, barrier):
        self.barrier.append(barrier)

    #getter methods
    def getImage(self):
        return self.image

    def getPlatform(self):
        return self.platform

    def getBarrier(self):
        return self.barrier

    def getOutOfBounds(self):
        return self.outOfBounds

    def getStartingPositions(self):
        return self.startingPosition

    def getStartingPosition(self, index):
        return self.startingPosition[index]

if __name__ == "__main__":
    pygame.init()
    pygame.display.init()
    pygame.display.set_mode((1200, 600))
    asdf = Stage("finalDestination.txt")
    
