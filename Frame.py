import pygame
import linecache
from Hitbox import *
from Hurtbox import *
from CONSTANT import *

class Frame(object):
    #to import a frame just use the character name and the index of the frame
    #then apply the index to the given sprite sheet
    def __init__(self, characterName, frameNum, spriteSheet):
        object.__init__(self)
        self.frameNum = frameNum
        self.sprite_sheet = spriteSheet
        self.image = None
        self.hitbox = None
        self.hurtbox = None
        self.displacement = (0, 0)
        self.velocity = (0, 0)
        #derive the file names based on the character name
        self.displacementFileName = "%s displacement.txt" %characterName
        self.velocityFileName = "%s velocity.txt" %characterName
        self.hitboxFileName = "%s hitboxes.txt" %characterName
        self.hurtboxFileName = "%s hurtboxes.txt" %characterName
        self.hurtboxDataFileName = "%s hurtbox force.txt" %characterName

        #import and set the object attributes
        self.setImage(self.importImage(frameNum))
        self.setHitbox(self.importHitboxes())
        self.setHurtbox(self.importHurtboxes())
        self.setDisplacement(self.importDisplacement())
        self.setVelocity(self.importVelocity())

    def importImage(self, frameNum):
        #get the coords of the clip for the sprite sheet
        coords = (frameNum % jedi.cols, frameNum // jedi.cols)
        #scale the coords to a snip size
        self.sprite_sheet.set_clip(pygame.Rect(coords[0] * jedi.width, coords[1] * jedi.height,
                                          jedi.width, jedi.height))
        image = self.sprite_sheet.subsurface(self.sprite_sheet.get_clip())
        return(image)

    def importHitboxes(self):
        #get to the correct line and convert the string to circles
        line = linecache.getline(self.hitboxFileName, self.frameNum + 1)
        #convert the string to useful data and return it as hitboxes
        circles = self.convertToCircles(line)
        return Hitbox(circles)

    def importHurtboxes(self):
        #get data and convert it to circles
        line = linecache.getline(self.hurtboxFileName, self.frameNum + 1)
        circles = self.convertToCircles(line)
        #later use the [name] hurtbox data to get rest of the hurtbox data
        forceString = linecache.getline(self.hurtboxDataFileName, self.frameNum + 1)
        force = int(forceString.strip())
        return Hurtbox(circles, 0, force)

    def importDisplacement(self):
        line = linecache.getline(self.displacementFileName, self.frameNum + 1)
        values = line.strip().split(", ")
        displacement = (float(values[0]), float(values[1]))
        return displacement

    def importVelocity(self):
        line = linecache.getline(self.velocityFileName, self.frameNum + 1)
        values = line.strip().split(", ")
        velocity = (int(values[0]), int(values[1]))
        return velocity
        
    def setImage(self, imageSurface):
        self.image = imageSurface

    def setHitbox(self, hitbox):
        self.hitbox = hitbox

    def setHurtbox(self, hurtbox):
        self.hurtbox = hurtbox

    def setDisplacement(self, displacement):
        self.displacement = displacement

    def setVelocity(self, velocity):
        self.velocity = velocity

    def getImage(self):
        return self.image

    def getHitbox(self):
        return self.hitbox

    def getHurtbox(self):
        return self.hurtbox

    def getDisplacement(self):
        return self.displacement

    def getVelocity(self):
        return self.velocity

    def convertToCircles(self, line):
        #i will render all the circles in here
        circles = []
        start = line.find("[")
        #cut off both ends of the string
        line = line[start + 3: len(line) - 3]
        #split the line into circles using common strings between each circle
        values = line.split("], [[")
        for value in values:
            #split the full circle to coords and radius
            parts = value.split("], ")
            #split each part of the circle into its coords
            center = parts[0].split(", ")
            #check to make sure you actally have data in the string
            if center != ['']:
                radius = parts[1]
                center[0] = int(center[0])
                center[1] = int(center[1])
                radius = int(radius)
                circle = Circle(center, radius)
                circles.append(circle)
        return circles
        

if __name__ == "__main__":
    pass
