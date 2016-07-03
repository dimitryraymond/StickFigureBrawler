from Action import *
from CONSTANT import *
import pygame
import copy

class Character(object):
    def __init__(self, characterName):
        object.__init__(self)
        self.initializeDefaultVariables()

        #derive the information filenames based on the character name
        self.characterName = characterName
        self.imageFileName = "%s0.png" %characterName
        self.actionRangesFileName = "%s action ranges.txt" %characterName
        #import and use the sprite sheet to generate the character's graphic data
        self.importSpriteSheet()
        self.importActions()
        self.importRepeatFrames()
        self.importActionForces()
        self.importActionDamage()
        self.generateMirrorActions()
        self.currentFrame = self.getAction(0).getFrame(0)
        #will need previous frame to smoothly process projectile like actions
        self.previousFrame = self.currentFrame
        

    def initializeDefaultVariables(self):
        self.actionR = []
        self.weight = 100
        self.busy = False
        self.stunned = False
        self.lives = 4
        self.status = status.GROUNDED
        self.direction = direction.RIGHT
        self.previousDirection = self.direction
        self.coords = (200, 400)
        self.previousCoords = self.coords
        self.velocity = (0, 0)
        self.doubleJumpUsed = False
        self.recoveryUsed = False
        self.currentAction = move.IDLE
        self.previousAction = self.currentAction
        self.controls = None
        self.damage = 0
        self.dead = False
        self.sprite_sheet = None
        
    def importActions(self):
        #first import the values from the txt file
        file = open(self.actionRangesFileName, 'r')
        #then add the action based on the values in each line of the text
        for line in file:
            #strip the \n character and split the line into two values
            line = line.strip()
            values = line.split(" ")
            values[0] = int(values[0])
            values[1] = int(values[1])
            self.addAction(values[0] - 1, values[1] - 1)
        file.close() 
        
    def addAction(self, begFrame, endFrame):
        #need to decide if i start with 0 or 1, prob 0
        newAction = Action(self.characterName, begFrame, endFrame, self.sprite_sheet)
        self.actionR.append(newAction)

    def generateMirrorActions(self):
        #copy the action by value
        self.actionL = copy.deepcopy(self.actionR)
        #use the current actions and make a mirror copy of them
        for i in range(len(self.actionR)):
            for j in range(len(self.actionR[i].frame)):
                #flip the image
                newImage = pygame.transform.flip(self.actionR[i].frame[j].image, True, False)
                self.actionL[i].frame[j].setImage(newImage)
                #flip the displacement
                newDisplacement = self.actionR[i].frame[j].displacement
                newDisplacement = (-newDisplacement[0], newDisplacement[1])
                self.actionL[i].frame[j].setDisplacement(newDisplacement)
                #flip the velocity
                newVelocity = self.actionR[i].frame[j].velocity
                newVelocity = (-newVelocity[0], newVelocity[1])
                self.actionL[i].frame[j].setVelocity(newVelocity)
                #flip the hitboxes
                for k in range(len(self.actionR[i].frame[j].hitbox.circle)):
                    newCircle = copy.deepcopy(self.actionR[i].frame[j].hitbox.circle[k])
                    newCoords = newCircle.getCoords()
                    #flip the x coords around the meridian of the frame
                    distanceFromMiddle = jedi.width / 2 - newCoords[0]
                    newCoords = (newCoords[0] + 2 * distanceFromMiddle, newCoords[1])
                    newCircle.setCoords(newCoords)
                    self.actionL[i].frame[j].hitbox.circle[k] = newCircle
                #flip the hurtboxes
                for k in range(len(self.actionR[i].frame[j].hurtbox.circle)):
                    newCircle = copy.deepcopy(self.actionR[i].frame[j].hurtbox.circle[k])
                    newCoords = newCircle.getCoords()
                    #flip the x coords around the meridian of the frame
                    distanceFromMiddle = jedi.width / 2 - newCoords[0]
                    newCoords = (newCoords[0] + 2 * distanceFromMiddle, newCoords[1])
                    newCircle.setCoords(newCoords)
                    self.actionL[i].frame[j].hurtbox.circle[k] = newCircle
            #flip the horizontal component of force
            self.actionL[i].setForce((self.actionR[i].getForce()[0] * -1, self.actionR[i].getForce()[1]))    

    def importActionForces(self):
        file = open("jedi action forces.txt")
        index = 0
        for line in file:
            values = line.strip().split(", ")
            values = (int(values[0]), int(values[1]))
            self.getAction(index).setForce(values)
            index+=1
        file.close()

    def importActionDamage(self):
        file = open("jedi action damage.txt")
        index = 0
        for line in file:
            value = line.strip()
            value = int(value)
            self.getAction(index).setDamage(value)
            index+=1
        file.close()
        
    def importRepeatFrames(self):
        #keep crouching 
        self.actionR[3].repeatFrames = [1, 1]
    
    def importSpriteSheet(self):
        self.sprite_sheet = pygame.image.load(self.imageFileName).convert()
        self.sprite_sheet.set_colorkey(self.sprite_sheet.get_at((0, 0)))
        #this is useful when the image ends up having bizare black squares around the character after editing the sprite sheet
        self.sprite_sheet = self.addColorKey(self.sprite_sheet)


    def addColorKey(self, surface, color = (0, 0, 0)):
        image = pygame.Surface(surface.get_size())
        image.fill(color)
        image.blit(surface, (0, 0))
        image.set_colorkey(color)
        return image

    #this is useless when getCurrentFrame processes all of the character's relevant data
    def setCurrentFrame(self, currentFrame):
        pass

    def doCurrentFrame(self):
        for i in range(32):
            if self.getCurrentAction() == move.array[i]:
                self.getAction(i).do()
                self.previousFrame = self.currentFrame
                self.currentFrame = self.getAction(i).currentFrame
        
    def setWeight(self, weight):
        self.weight = weight

    def setCurrentAction(self, action):
        #reset the index of the previous action back to 0
        #which is found by using the index of the array in the move class
        if not self.currentAction == action:
            #reset the index of the previous action to 0 if you do a different action
            self.getAction(move.array.index(self.previousAction)).reset()
            self.previousAction = self.currentAction
            self.currentAction = action
        
    def setDirection(self, direction):
        if not self.direction == direction:
            self.previousDirection = self.direction
            self.direction = direction

    def setStatus(self, status):
        self.status = status

    def setCoords(self, coords):
        self.coords = coords

    def setVelocity(self, velocity):
        self.velocity = velocity

    def setPreviousAction(self, previousAction):
        self.previousAction = previousAction

    def setDamage(self, damage):
        self.damage = damage

    def setDead(self, dead):
        self.dead = dead

    def setLives(self, lives):
        self.lives = lives

    def addDamage(self, damage):
        self.damage+=damage

    def getWeight(self):
        return self.weight

    def getAction(self, index = None):
        if index is None:
            if self.direction == direction.RIGHT:
                return self.actionR
            elif self.direction == direction.LEFT:
                return self.actionL
        else:
            if self.direction == direction.RIGHT:
                return self.actionR[index]
            elif self.direction == direction.LEFT:
                return self.actionL[index]

    def getDirection(self):
        return self.direction

    def getStatus(self):
        return self.status

    def getCoords(self):
        return self.coords

    #this will make it simpler when generating hitboxes and hurboxes
    def getImageCoords(self):
        return self.coords[0] - jedi.width / 2, self.coords[1] - jedi.height

    def getVelocity(self):
        return self.velocity

    def getPreviousAction(self):
        return self.previousAction

    def getCurrentAction(self):
        return self.currentAction
    
    def getDamage(self):
        return self.damage

    def getDead(self):
        return self.dead

    def getLives(self):
        return self.lives


if __name__ == "__main__":
    pygame.init()
    pygame.display.init()
    screen = pygame.display.set_mode((200, 128))
    jedi = Character("jedi")
    background = pygame.Surface(screen.get_size()).convert()
    background.fill((128, 128, 128))
    screen.blit(background, (0, 0))
    pygame.display.flip()
    clock = pygame.time.Clock()
    for action in jedi.getAction():
        for frame in action.getFrame():
            screen.blit(background, (0, 0))
            screen.blit(frame.getImage(), (0, 0))
            for circle in frame.getHitbox().getCircles():
                pygame.draw.circle(screen, (0, 255, 0), circle.getCoords(), circle.getRadius(), 1)
            for circle in frame.getHurtbox().getCircles():
                pygame.draw.circle(screen, (0, 255, 255), circle.getCoords(), circle.getRadius(), 1)
            clock.tick(12)
            pygame.display.flip()

    pygame.display.quit()
    pygame.quit()

