import pygame
import os
import sys
from CONSTANT import *
from Character import *
from Stage import *
from random import randint

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" %(50, 50)

class StickFigureBrawler(object):
    def __init__(self):
        object.__init__(self)
        self.initializeGame()
        self.initializeGameData()
        self.on = True
        
    def initializeGame(self):
        pygame.init()
        pygame.display.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((1200, 600))
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.fill((128, 128, 128))
        self.screen.blit(self.background, (0, 0))
        self.smallFont = pygame.font.SysFont(None, 24)
        self.mediumFont = pygame.font.SysFont(None, 32)
        self.bigFont = pygame.font.SysFont(None, 48)
        pygame.display.flip()

    def initializeGameData(self):
        self.keepGoing = True
        self.events = None
        self.stages = []
        self.importStages()
        self.setStageChoice(0)
        self.setNumOfPlayers(2)
        self.setPlayers()

    def getEvents(self):
        self.events = pygame.event.get()
        self.keyboard = pygame.key.get_pressed()        

    def checkForKeepGoing(self):
        for event in self.events:
            #check for keep going based on quitting
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return False
        #then check for keep going based on running out of lives
        for player in self.players:
            if player.getLives() < 1:
                return False
        return True

    def checkForDead(self):
        #i've decided to only check for fall off stage for  sides and bottom, and high top
        stageCoords = self.stages[self.stageChoice].getOutOfBounds()
        for player in self.players:            
            #check for sides
            if player.getCoords()[0] < stageCoords[0][0] or player.getCoords()[0] > stageCoords[1][0]:
                print("player fell off to the side")
                self.resetPlayer(player)
            elif player.getCoords()[1] > stageCoords[2][1]:
                print("player fell to the bottom")
                self.resetPlayer(player)
            elif player.getCoords()[1] < -stageCoords[2][1] / 2:
                print("player fell through the ceiling")
                self.resetPlayer(player)
            

    def resetPlayer(self, player):
        #reset the player to the next life
        player.setLives(player.getLives() - 1)
        #make the player respawn away from the side that he fell by choosing the farther spawn point of the stage
        #if player fell on left side
        if player.getCoords()[0] < 600:
            #choose the second(right) spawn point
            respawnIndex = 1
        #if player fell on the right side
        else:
            respawnIndex = 0
        respawnLocation = self.stages[self.stageChoice].getStartingPosition(respawnIndex)
        #raise the rewpawn location to make the player fall to get the effect of a respawn animation
        #adjusting the velocity also helps
        respawnLocation = (respawnLocation[0], respawnLocation[1] - 30)
        player.setCoords(respawnLocation)
        player.setVelocity((0, 20))
        player.setStatus(status.AIRBORNE)
        player.busy = True
        player.setCurrentAction(move.FALL)
        player.setDamage(0)
    
    #handle the collisions of characters
    def getCollisions(self):
        #first three lines here make sure you check collisions agains all entities except for themselves
        for playerA in self.players:
            for playerB in self.players:
                if not playerA == playerB:
                    for hurtCircle in playerA.currentFrame.getHurtbox().getCircles():
                        for hitCircle in playerB.currentFrame.getHitbox().getCircles():
                            if self.getCircleIntersection(hurtCircle, hitCircle, playerA, playerB):
                                #if there is a collision then get the values of that action and apply them to the character hit
                                action = playerA.getAction(move.array.index(playerA.currentAction))
                                velocity = action.getForce()
                                #modify velocity based on the character's damage
                                velocityRatio = (playerB.getDamage() + 50)/50
                                velocity = (velocity[0] * velocityRatio, velocity[1] * velocityRatio)
                                #lastly, modify the player
                                playerB.setVelocity(velocity)
                                playerB.setStatus(status.AIRBORNE)
                                playerB.addDamage(action.getDamage())
                                break
                                
                                
                            
    #check the collision of individual circles
    def getCircleIntersection(self, circleA, circleB, playerA, playerB):
        coordsA = (circleA.getCoords()[0] + playerA.getCoords()[0], circleA.getCoords()[1] + playerA.getCoords()[1]) 
        coordsB = (circleB.getCoords()[0] + playerB.getCoords()[0], circleB.getCoords()[1] + playerB.getCoords()[1])
        distance = pow(pow(coordsA[0] - coordsB[0], 2) + pow(coordsA[1] - coordsB[1], 2), .5)
        if distance - circleA.getRadius() - circleB.getRadius() <= 0:
            return True
        else:
            return False

    def getActions(self):
        for i in range(self.getNumOfPlayers()):
            #check to see if you need set busy to false
            if self.players[i].busy:
                #utilizing the index of the CONSTANT.move.array to generalize this code
                #print(self.players[i].getAction(move.array.index(self.players[i].currentAction)).actionIndex)
                if self.players[i].getAction(move.array.index(self.players[i].currentAction)).numOfFrames == (
                    self.players[i].getAction(move.array.index(self.players[i].currentAction)).actionIndex):
                    self.players[i].busy = False

                #let the character attack in the middle of the jump by checking the attack buttons
                if self.players[i].currentAction == move.JUMP:
                    for key in (4, 5, 6):
                        if self.checkForPressed(controls.players[i][key]):
                            self.players[i].busy = False

                
            #check to make sure the player isn't already busy before accepting input
            if not (self.players[i].busy):
                #first handle all ground events
                if self.players[i].getStatus() == status.GROUNDED:
                    #reset the double jump counter and the recovery counter
                    self.players[i].doubleJumpUsed = False
                    self.players[i].recoveryUsed = False
                    #check for uncrouch
                    if self.checkForKeyUP(controls.players[i][1]):
                        self.players[i].setCurrentAction(move.UNCROUCH)
                        self.players[i].busy = True
                    #else check if the player is walking
                    #btw if you set the status of a player to AIRBORNE then it checks if you fall off the platform or not
                    elif self.checkForPressed(controls.players[i][3]):
                        self.players[i].setCurrentAction(move.WALK)
                        self.players[i].setDirection(direction.RIGHT)
                    elif self.checkForPressed(controls.players[i][2]):
                        self.players[i].setCurrentAction(move.WALK)
                        self.players[i].setDirection(direction.LEFT)
                    #else, check for crouch
                    elif self.checkForUniquePressed(controls.players[i][1], i):
                        self.players[i].setCurrentAction(move.CROUCH)
                    #if no input then the player is idle
                    else:
                        self.players[i].setCurrentAction(move.IDLE)

                    #check for special hits
                    if self.checkForUniquePressed(controls.players[i][6], i):
                        self.players[i].setCurrentAction(move.nSPC)
                        self.players[i].busy = True
                    elif self.checkForOnlyTwoPressed(controls.players[i][6], controls.players[i][0], i) and not self.players[i].recoveryUsed:
                        self.players[i].setCurrentAction(move.uSPC)
                        self.players[i].busy = True
                        self.players[i].setStatus(status.AIRBORNE)
                        self.players[i].recoveryUsed = True
                    elif self.checkForOnlyTwoPressed(controls.players[i][6], controls.players[i][1], i):
                        self.players[i].setCurrentAction(move.dSPC)
                        self.players[i].busy = True
                        self.players[i].setStatus(status.AIRBORNE)
                    elif self.checkForOnlyTwoPressed(controls.players[i][6], controls.players[i][2], i):
                        self.players[i].setCurrentAction(move.sSPC)
                        self.players[i].setDirection(direction.LEFT)
                        self.players[i].busy = True
                        self.players[i].setStatus(status.AIRBORNE)
                    elif self.checkForOnlyTwoPressed(controls.players[i][6], controls.players[i][3], i):
                        self.players[i].setCurrentAction(move.sSPC)
                        self.players[i].setDirection(direction.RIGHT)
                        self.players[i].busy = True
                        self.players[i].setStatus(status.AIRBORNE)

                    #check for smash hits
                    elif self.checkForOnlyTwoPressed(controls.players[i][5], controls.players[i][0], i):
                        self.players[i].setCurrentAction(move.uSMASH)
                        self.players[i].busy = True
                    elif self.checkForOnlyTwoPressed(controls.players[i][5], controls.players[i][1], i):
                        self.players[i].setCurrentAction(move.dSMASH)
                        self.players[i].busy = True
                    elif self.checkForOnlyTwoPressed(controls.players[i][5], controls.players[i][2], i):
                        self.players[i].setCurrentAction(move.sSMASH)
                        self.players[i].setDirection(direction.LEFT)
                        self.players[i].busy = True
                        self.players[i].setStatus(status.AIRBORNE)
                    elif self.checkForOnlyTwoPressed(controls.players[i][5], controls.players[i][3], i):
                        self.players[i].setCurrentAction(move.sSMASH)
                        self.players[i].setDirection(direction.RIGHT)
                        self.players[i].busy = True
                        self.players[i].setStatus(status.AIRBORNE)

                    #check for normal hits
                    elif self.checkForUniquePressed(controls.players[i][4], i):
                        self.players[i].setCurrentAction(move.nHIT)
                        self.players[i].busy = True
                    elif self.checkForOnlyTwoPressed(controls.players[i][4], controls.players[i][0], i):
                        self.players[i].setCurrentAction(move.uHIT)
                        self.players[i].busy = True
                    elif self.checkForOnlyTwoPressed(controls.players[i][4], controls.players[i][1], i):
                        self.players[i].setCurrentAction(move.dHIT)
                        self.players[i].busy = True
                    elif self.checkForOnlyTwoPressed(controls.players[i][4], controls.players[i][2], i):
                        self.players[i].setCurrentAction(move.sHIT)
                        self.players[i].setDirection(direction.LEFT)
                        self.players[i].busy = True
                    elif self.checkForOnlyTwoPressed(controls.players[i][4], controls.players[i][3], i):
                        self.players[i].setCurrentAction(move.sHIT)
                        self.players[i].setDirection(direction.RIGHT)
                        self.players[i].busy = True

                    #check for jump left right and center
                    elif self.checkForOnlyTwoPressed(controls.players[i][7], controls.players[i][2], i):
                        self.players[i].setCurrentAction(move.JUMP)
                        self.players[i].busy = True
                        self.players[i].setStatus(status.AIRBORNE)
                        #give the character horizontal velocity, the move.JUMP action takes care of the vertical component of velocity
                        self.players[i].setVelocity((-20, self.players[i].getVelocity()[1]))
                    elif self.checkForOnlyTwoPressed(controls.players[i][7], controls.players[i][3], i):
                        self.players[i].setCurrentAction(move.JUMP)
                        self.players[i].busy = True
                        self.players[i].setStatus(status.AIRBORNE)
                        self.players[i].setVelocity((20, self.players[i].getVelocity()[1]))
                    elif self.checkForPressed(controls.players[i][7]):
                        self.players[i].setCurrentAction(move.JUMP)
                        self.players[i].busy = True
                        self.players[i].setStatus(status.AIRBORNE)
                    
                #now deal with everything while airborne        
                elif self.players[i].getStatus() == status.AIRBORNE:
                    #check for special moves
                    if self.checkForOnlyTwoPressed(controls.players[i][6], controls.players[i][0], i) and not self.players[i].recoveryUsed:
                        self.players[i].recoveryUsed = True
                        self.players[i].setCurrentAction(move.uAIRSPC)
                        self.players[i].busy = True
                    elif self.checkForOnlyTwoPressed(controls.players[i][6], controls.players[i][1], i):
                        self.players[i].setCurrentAction(move.dAIRSPC)
                        self.players[i].busy = True
                    elif self.checkForOnlyTwoPressed(controls.players[i][6], controls.players[i][2], i):
                        self.players[i].setCurrentAction(move.sAIRSPC)
                        self.players[i].setDirection(direction.LEFT)
                        self.players[i].busy = True
                    elif self.checkForOnlyTwoPressed(controls.players[i][6], controls.players[i][3], i):
                        self.players[i].setCurrentAction(move.sAIRSPC)
                        self.players[i].setDirection(direction.RIGHT)
                        self.players[i].busy = True
                    elif self.checkForUniquePressed(controls.players[i][6], i):
                        self.players[i].setCurrentAction(move.nAIRSPC)
                        self.players[i].busy = True

                    #check for normal hits (they can be used by either normal hit button or smash hit button)
                    elif self.checkForOnlyTwoPressed(controls.players[i][4], controls.players[i][0], i) or self.checkForOnlyTwoPressed(controls.players[i][5], controls.players[i][0], i):
                        self.players[i].setCurrentAction(move.uAIR)
                        self.players[i].busy = True
                    elif self.checkForOnlyTwoPressed(controls.players[i][4], controls.players[i][1], i) or self.checkForOnlyTwoPressed(controls.players[i][5], controls.players[i][1], i):
                        self.players[i].setCurrentAction(move.dAIR)
                        self.players[i].busy = True
                    elif self.checkForOnlyTwoPressed(controls.players[i][4], controls.players[i][2], i) or self.checkForOnlyTwoPressed(controls.players[i][5], controls.players[i][2], i):
                        #decide if this side move will be forward air or back air attack; based on the player's direction
                        if self.players[i].getDirection() == direction.LEFT:
                            self.players[i].setCurrentAction(move.fAIR)
                            self.players[i].busy = True
                        else:
                            self.players[i].setCurrentAction(move.bAIR)
                            self.players[i].busy = True
                    elif self.checkForOnlyTwoPressed(controls.players[i][4], controls.players[i][3], i) or self.checkForOnlyTwoPressed(controls.players[i][5], controls.players[i][3], i):
                        #decide if this side move will be forward air or back air attack based on the player's direction
                        if self.players[i].getDirection() == direction.RIGHT:
                            self.players[i].setCurrentAction(move.fAIR)
                            self.players[i].busy = True
                        else:
                            self.players[i].setCurrentAction(move.bAIR)
                            self.players[i].busy = True
                    elif self.checkForUniquePressed(controls.players[i][4], i) or self.checkForUniquePressed(controls.players[i][5], i):
                        self.players[i].setCurrentAction(move.nAIR)
                        self.players[i].busy = True
                    #check for second jump
                    #but make sure double jump hasn't been used
                    elif self.checkForOnlyTwoPressed(controls.players[i][7], controls.players[i][2], i) and (not self.players[i].doubleJumpUsed):
                        self.players[i].doubleJumpUsed = True
                        self.players[i].setCurrentAction(move.JUMP)
                        self.players[i].busy = True
                        self.players[i].setStatus(status.AIRBORNE)
                        #give the character horizontal velocity, the move.JUMP action takes care of the vertical component of velocity
                        self.players[i].setVelocity((self.players[i].getVelocity()[0] / 3  - 20, 0))
                    elif self.checkForOnlyTwoPressed(controls.players[i][7], controls.players[i][3], i) and not self.players[i].doubleJumpUsed:
                        self.players[i].doubleJumpUsed = True
                        self.players[i].setCurrentAction(move.JUMP)
                        self.players[i].busy = True
                        self.players[i].setStatus(status.AIRBORNE)
                        self.players[i].setVelocity((20, 0))
                    elif self.checkForPressed(controls.players[i][7]) and not self.players[i].doubleJumpUsed:
                        self.players[i].doubleJumpUsed = True
                        self.players[i].setCurrentAction(move.JUMP)
                        self.players[i].busy = True
                        self.players[i].setStatus(status.AIRBORNE)
                        #if you jump center in air then divide the horizontal momentum in half
                        self.players[i].setVelocity((self.players[i].getVelocity()[0] / 2, 0))
                        
                    else:
                        #if no events then continue falling
                        self.players[i].setCurrentAction(move.FALL)

                    #check for directional influence while in air
                    if self.checkForUniquePressed(controls.players[i][0], i):
                        self.players[i].setVelocity((self.players[i].getVelocity()[0], self.players[i].getVelocity()[1] + 5))
                    elif self.checkForUniquePressed(controls.players[i][1], i):
                        self.players[i].setVelocity((self.players[i].getVelocity()[0], self.players[i].getVelocity()[1] - 5))
                    elif self.checkForUniquePressed(controls.players[i][2], i):
                        self.players[i].setVelocity((self.players[i].getVelocity()[0] - 5, self.players[i].getVelocity()[1]))
                    elif self.checkForUniquePressed(controls.players[i][3], i):
                        self.players[i].setVelocity((self.players[i].getVelocity()[0] + 5, self.players[i].getVelocity()[1]))
                    
                        
                
                        
    def checkForKeyUP(self, key):
        keyup = False
        for event in self.events:
            if event.type == pygame.KEYUP and event.key == key:
                keyup = True
        return keyup


    def checkForPressed(self, keyPressed):
        pressed = False
        if self.keyboard[keyPressed] == 1:
            pressed = True
        return pressed

    def checkForUniquePressed(self, keyPressed, playerNum):
        pressed = False
        unique = True
        #check against the possible controls in the CONSTANT.controls.player[playerNum]
        #each player has only 8 buttons to choose from
        for key in controls.players[playerNum]:
            #check for each key other than key to test
            if not (key == keyPressed):
                if self.keyboard[key] == 1:
                    unique = False
            #check on the status of the key to test
            else:
                if self.keyboard[key] == 1:
                    pressed = True
        if pressed and unique:
            return True
        else:
            return False

    #refer to the logic of self.checkForUniquePressed(), very similar but reversed on order of keys tested
    def checkForOnlyTwoPressed(self, key1, key2, playerNum):
        pressed1 = False
        pressed2 = False
        unique = True
        #check both of the keys against the other possible controls of the player
        for key in controls.players[playerNum]:
            if (key == key1):
                if self.keyboard[key] == 1:
                    pressed1 = True
            elif (key == key2):
                if self.keyboard[key] == 1:
                    pressed2 = True
            else:
                if self.keyboard[key] == 1:
                    unique = False
        if pressed1 and pressed2 and unique:
            return True
        else:
            #print(pressed1, pressed2, unique)
            return False
                

    def checkForIdle(self):
        keyPressed = False
        for key in self.keyboard:
            if key == 1:
                keyPressed = True
                break
        #return idle keyboard
        return not keyPressed
            

    def applyActions(self):
        for player in self.players:
            player.doCurrentFrame()

    def applyGravity(self):
        for player in self.players:
            if player.getStatus() == status.AIRBORNE:
                player.velocity = (player.velocity[0], player.velocity[1] - physics.g)

    def checkForOffStage(self, player):
        platform = self.stages[self.stageChoice].getPlatform()[0]
        if player.getStatus() == status.AIRBORNE or (player.getStatus() == status.GROUNDED and player.velocity[1] < 0):
            #check if the player's coords are within the platform coords
            #(I added a margin of error of 10 px to account for the character's width), now you can stand on platforms like mario
            if player.coords[0] >= platform.getCoords()[0][0] - 10 and player.coords[0] <= platform.getCoords()[1][0] + 10:
                #check if the player's coords are now below or equal to the platform (within landing range)
                if player.coords[1] >= platform.getCoords()[0][1]:
                    player.velocity = (0, 0)
                    player.setCoords((player.getCoords()[0], platform.getCoords()[0][1]))
                    player.status = status.GROUNDED
                    #this is so that the current move can't be interrupted by landing. (you only do land animation if youre not busy)
                    if not player.busy:
                        player.setCurrentAction(move.LAND)
                        player.busy = True
        elif player.getStatus() == status.GROUNDED:
            if player.getCurrentAction() == move.WALK:
            #check if the coords of the player are off stage
                if player.coords[0] <= platform.getCoords()[0][0] - 10 or player.coords[0] >= platform.getCoords()[1][0] + 10:
                    player.setStatus(status.AIRBORNE)
                    player.setCurrentAction(move.FALL)
                    player.busy = False
                    
    
        
    def updateStage(self, drawElements = False):
        self.screen.blit(self.stages[self.stageChoice].getImage(), (0, 0))

    def drawStageElements(self):
        for platform in self.stages[self.stageChoice].getPlatform():
            pygame.draw.line(self.screen, color.RED, platform.getCoords()[0], platform.getCoords()[1], 3)
        
    def updatePlayers(self):
        for player in self.players:
            image = player.currentFrame.getImage()
            displacement = player.currentFrame.displacement
            velocity = player.currentFrame.velocity
            #apply the velocity of the frame to the character
            player.setVelocity((player.getVelocity()[0] + velocity[0], player.getVelocity()[1] + velocity[1]))
            #apply the velocity of the character to the character's displacement
            player.setCoords((player.getCoords()[0] + player.velocity[0], player.getCoords()[1] - player.velocity[1]))
            #apply the displacement of the frame to the character
            player.setCoords((player.getCoords()[0] + displacement[0], player.getCoords()[1] - displacement[1]))
            self.checkForOffStage(player)
            coords = player.getImageCoords()
            self.screen.blit(image, coords)

    def drawPlayerElements(self):
        #use the index to have different collors for each player
        index = 0
        for player in self.players:
            #draw the hitboxes
            for circle in player.currentFrame.getHitbox().getCircles():
                coords = (int(player.getImageCoords()[0] + circle.getCoords()[0]), int(player.getImageCoords()[1] + circle.getCoords()[1]))
                pygame.draw.circle(self.screen, color.players[index], coords, circle.getRadius(), 1)
            #draw the hurtboxes
            for circle in player.currentFrame.getHurtbox().getCircles():
                coords = (int(player.getImageCoords()[0] + circle.getCoords()[0]), int(player.getImageCoords()[1] + circle.getCoords()[1]))
                pygame.draw.circle(self.screen, color.BLACK, coords, circle.getRadius(), 3)
                pygame.draw.circle(self.screen, color.weapons[index], coords, circle.getRadius(), 1)
            index+=1

    def drawScoreboard(self):
        #help keep track of the information of each player
        for index in range(len(self.players)):
            self.players[index].playerName = self.smallFont.render(("Player %d" %(index + 1)), 1, color.players[index])
            self.players[index].playerLives = self.mediumFont.render(("Lives: %d" %self.players[index].getLives()), 1, color.players[index])
            self.players[index].playerDamage = self.bigFont.render(("%d%%" %self.players[index].getDamage()), 1, color.players[index])
        #manually place each text on the screen
        self.screen.blit(self.players[0].playerDamage, (150 - self.players[0].playerDamage.get_width() / 2, 20))
        self.screen.blit(self.players[0].playerLives, (150 - self.players[0].playerLives.get_width() / 2, 20 + self.players[0].playerDamage.get_height()))
        self.screen.blit(self.players[0].playerName, (150 - self.players[0].playerName.get_width() / 2, 20 + self.players[0].playerLives.get_height() + self.players[0].playerDamage.get_height()))

        self.screen.blit(self.players[1].playerDamage, (1050 - self.players[1].playerDamage.get_width() / 2, 20))
        self.screen.blit(self.players[1].playerLives, (1050 - self.players[1].playerLives.get_width() / 2, 20 + self.players[0].playerDamage.get_height()))
        self.screen.blit(self.players[1].playerName, (1050 - self.players[1].playerName.get_width() / 2, 20 + self.players[0].playerLives.get_height() + self.players[0].playerDamage.get_height()))

    def updateScreen(self, fps = 12):
        self.clock.tick(fps)
        self.updateStage()
        self.drawStageElements()
        self.applyGravity()
        self.updatePlayers()
        self.drawPlayerElements()
        self.drawScoreboard()
        pygame.display.flip()

    #stage choice control functions
    def getStageChoice(self):
        return self.stageChoice
    
    def setStageChoice(self, index):
        if index > len(self.stages) - 1:
            index = len(self.stages) - 1
            print("Invalid stage selection")
        elif index < 0:
            index = 0
            print("Invalid stage selection")
        else:
            self.stageChoice = index

    def importStages(self):
        self.stages.append(Stage("finalDestination.txt"))

    def setNumOfPlayers(self, numOfPlayers):
        self.numOfPlayers = numOfPlayers

    def getNumOfPlayers(self):
        return self.numOfPlayers
        
    def setPlayers(self):
        self.players = []
        for i in range(self.getNumOfPlayers()):
            self.players.append(Character("jedi"))
            self.players[i].setCoords(self.stages[self.stageChoice].getStartingPosition(i))

    def quitGame(self):
        pygame.display.quit()
        pygame.quit()
        
    #run the game and then quit
    def run(self):
        self.getEvents()
        while(self.checkForKeepGoing()):
            self.checkForDead()
            self.getEvents()
            self.getCollisions()
            self.getActions()
            self.applyActions()
            self.updateScreen()
        self.quitGame()
        

if __name__ == "__main__":
    test = StickFigureBrawler()
    test.run()
