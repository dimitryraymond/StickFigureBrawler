from CONSTANT import *
from Frame import *

class Action(object):    
    def __init__(self, characterName, begFrame, endFrame, spriteSheet):
        object.__init__(self)
        self.frame = []
        self.lagFrames = 0
        self.actionType = None
        self.repeatFrames = None
        self.actionIndex = 0
        self.numOfFrames = 0
        self.force = (0, 0)
        self.damage = 0
        self.characterName = characterName
        self.begFrame = begFrame
        self.endFrame = endFrame
        self.spriteSheet = spriteSheet
        self.importFrames()
        self.setStartingFrame()

    def importFrames(self):
        for i in range(self.begFrame, self.endFrame + 1, 1):
            self.addFrame(Frame(self.characterName, i, self.spriteSheet))

    def setNumOfFrames(self, num):
        self.numOfFrames = num
        
    def setFrame(self, frame):
        self.frame = frame
        
    def setType(self, actionType):
        self.actionType = actionType

    def setLagFrames(self, lagFrames):
        self.lagFrames = lagFrames

    def setRepeatFrames(self, repeatFrames):
        self.repeatFrames = repeatFrames

    def setStartingFrame(self):
        self.currentFrame = self.getFrame(0)

    def setForce(self, force):
        self.force = force

    def setDamage(self, damage):
        self.damage = damage
        
    def getFrame(self, index = None):
        if index is None:
            return self.frame
        else:
            return self.frame[index]

    def getType(self):
        return self.actionType

    def getLagFrames(self):
        return self.lagFrames
    
    def getRepeatFrames(self):
        return repeatFrames

    def getNumOfFrames(self):
        return self.numOfFrames

    def getForce(self):
        return self.force

    def getDamage(self):
        return self.damage
    
    def addFrame(self, frame):
        self.frame.append(frame)
        self.setNumOfFrames(self.getNumOfFrames() + 1)
        
    def popFrame(self, index):
        self.frame.pop(index)
        self.setNumOfFrames(self.getNumOfFrames() - 1)

    #reset action back to the beginning
    def reset(self):
        self.actionIndex = 0
        
    #advance the frame's index
    def advanceFrame(self):
        if self.actionIndex >= self.getNumOfFrames():
            self.actionIndex = 0
        self.currentFrame = self.getFrame(self.actionIndex)
        self.actionIndex+=1
    
    #this will will set the frame of the animation
    def do(self):
        #handle this based on wether there are any repeat frames for the action
        if self.repeatFrames is None:
            #set the next frame of the character
            self.advanceFrame()
        else:
            #what to do before the frames to repeat
            if self.actionIndex < self.repeatFrames[0]:
                self.advanceFrame()
            #what to do during the frames to repeat
            elif self.actionIndex >= self.repeatFrames[0] and self.actionIndex <= self.repeatFrames[1]:
                if self.actionIndex > self.repeatFrames[1]:
                    self.actionIndex = self.repeatFrames[0]
                self.currentFrame = self.getFrame(self.actionIndex)
                self.actionIndex+=1
                #if the index is too high then reset it back to the beginning of repeat frames
                if self.actionIndex > self.repeatFrames[1]:
                    self.actionIndex = self.repeatFrames[0]
            #what to do after the frames to repeat
            elif self.actionIndex > self.repeatFrames[1]:
                self.advanceFrame()

if __name__ == "__main__":
    pass
