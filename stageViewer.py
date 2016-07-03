import os
import sys
import pygame
import linecache

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (50, 50)

class StageEditor(object):
    def __init__(self, stageFileName = "finalDestination.txt"):
        object.__init__(self)
        self.initializeGame(stageFileName)

    def initializeGame(self, stageFileName):
        pygame.init()
        pygame.display.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((1200, 600))
        imageFileName = linecache.getline(stageFileName, 1).strip()
        self.background = pygame.image.load(imageFileName)
        self.background = self.background.convert()
        self.screen.blit(self.background, (0, 0))
        self.font = pygame.font.SysFont(None, 18)

    def getEvents(self):
        self.event = pygame.event.get()

    def importMouseCoords(self):
        (self.mouseX, self.mouseY) = pygame.mouse.get_pos()
        self.mouseXText = self.font.render(str(self.mouseX), 1, (255, 255, 255))
        self.mouseYText = self.font.render(str(self.mouseY), 1, (255, 255, 255))

    def renderTheScreen(self, fps = 30):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.mouseXText, (0, 0))
        self.screen.blit(self.mouseYText, (0, 10))
        pygame.draw.circle(self.screen, (255, 0, 0), (self.mouseX, self.mouseY), 5,  1)
        self.flip()
        self.clock.tick(fps)

    def flip(self):
        pygame.display.flip()

    def checkForKeepGoing(self):
        for event in self.event:
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return False
        return True

    def run(self):
        self.getEvents()
        while(self.checkForKeepGoing()):
            self.getEvents()
            self.importMouseCoords()
            self.renderTheScreen()
        self.quitGame()

    def quitGame(self):
        pygame.display.quit()
        pygame.quit()

if __name__ == "__main__":
    test = StageEditor()
    test.run()
