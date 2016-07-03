import os
import sys
import pygame
from importHitboxes import *
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (50, 50)

filename = "jedi0.png"

if filename == "brawler.png":
    width = 128 
    height = 128
    rows = 14
    cols = 14
elif filename == "swordsman.png":
    width = 128
    height = 128
    rows = 14
    cols = 12
elif filename == "jedi0.png":
    width = 200
    height = 128
    rows = 14
    cols = 13
elif filename == "bruiser.png":
    width = 250 
    height = 180
    rows = 15
    cols = 15

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height))
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((128, 128, 128))
screen.blit(background, (0, 0))
pygame.display.flip()
sprite_sheet = pygame.image.load(filename).convert()
sprite_sheet.set_colorkey(sprite_sheet.get_at((0, 0)))

def pause(silent = False):
    if(silent):
        clock.tick(1)
    else:
        length = int(input("give input to start the countdown"))
        for i in range(length):
            print(length - i)
            clock.tick(1)
        print("start")
    
def importFrames(filename):
    frames = []
    for j in range(rows):         #for each row
        for i in range(cols):     #for each col
            imageNum = j * cols + i + 1
            screen.blit(background, (0, 0))
            sprite_sheet.set_clip(pygame.Rect(i * width, j * height, width, height))
            image = sprite_sheet.subsurface(sprite_sheet.get_clip())
            frames.append(image)
    return frames

def getIndexOfClosest(array, mouseCoords):
    smallest = -1
    smallestNew = -1
    distance = 10000
    for hitbox in array:
        smallestNew+=1
        dx = hitbox[0][0] - mouseCoords[0]
        dy = hitbox[0][1] - mouseCoords[1]
        distanceNew = pow(pow(dx, 2) + pow(dy, 2), .5)
        if distanceNew < distance:
            distance = distanceNew
            smallest = smallestNew
    return smallest

keepGoing = True
doBreak = False
frames = importFrames(filename)

importFrames = ImportCircles("jedi hurtboxes.txt")
#hitBoxCircles = [[] for i in range(len(frames))]
hitBoxCircles = importFrames.data

font = pygame.font.SysFont(None, 18)
mouseCoords = 0
radius = 1
radiusCoords = (0, screen.get_height() - 10)
imageNum = 0
clipboard = 0
doBreak = False
while(not doBreak):
    keepGoing = True
    string = str(imageNum + 1)
    indexText = font.render(string, 1, (0, 0, 0))
    indexCoords = (screen.get_width() - 30, 0)
    pygame.mouse.set_visible(False)
    while(keepGoing):
        (mouseX, mouseY) = pygame.mouse.get_pos()
        mouseXText = font.render(str(mouseX), 1, (0, 0, 0))
        mouseYText = font.render(str(mouseY), 1, (0, 0, 0))
        radiusText = font.render(str(radius), 1, (0, 0, 0))
        screen.blit(background, (0, 0))
        screen.blit(frames[imageNum], (0, 0))
        screen.blit(indexText, indexCoords)
        screen.blit(mouseXText, (0, 0))
        screen.blit(mouseYText, (0, 10))
        screen.blit(radiusText, radiusCoords)
        pygame.draw.circle(screen, (0, 255, 0), (mouseX, mouseY), radius, 1)
        for hitbox in hitBoxCircles[imageNum]:
            pygame.draw.circle(screen, (0, 255, 255), hitbox[0], hitbox[1], 1)
        pygame.display.flip()
        clock.tick(16)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                keepGoing = False
                #move to the next frame
                if event.key == pygame.K_RIGHT:
                    imageNum+=1
                    if imageNum > rows * cols - 1:
                        imageNum = 0
                #move to the previous frame
                elif event.key == pygame.K_LEFT:
                    imageNum-=1
                    if imageNum < 0:
                        imageNum = rows * cols - 1
                #add a circle to the frame
                if event.key == pygame.K_RETURN:
                    #print("Hitbox circle added")
                    circle = ((mouseX, mouseY), radius)
                    hitBoxCircles[imageNum].append(circle)
                #delete the closest circle to the pointer
                if event.key == pygame.K_BACKSPACE:
                    if(len(hitBoxCircles[imageNum]) > 0):
                       #print("Hitbox circle deleted")
                       hitBoxCircles[imageNum].pop(getIndexOfClosest(hitBoxCircles[imageNum], (mouseX, mouseY)))
                    else:
                       #print("No hitboxes to delete")
                        pass
                #this is a copy and pase feature when i move between similar frames
                if event.key == pygame.K_c:
                    clipboard = hitBoxCircles[imageNum]
                if event.key == pygame.K_v:
                    for circle in clipboard:
                        hitBoxCircles[imageNum].append(circle)
                if event.key == pygame.K_DELETE:
                    hitBoxCircles[imageNum] = []
            #adjust the radius based on mouse clicks
            if pygame.mouse.get_pressed() == (0, 0, 1):
                radius+=1
            elif pygame.mouse.get_pressed() == (1, 0, 0):
                radius-=1
                if radius < 1:
                    radius = 1
            #check for quit
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                keepGoing = False
                doBreak = True
                
pygame.display.quit()
pygame.quit()

frameNum = 0

#remember the original print path
temp = sys.stdout
#redirect all print statements to a file
with open('jedi hurtboxes.txt', 'w') as sys.stdout:
    for line in hitBoxCircles:
        frameNum+=1
        string1 = "%s: " %frameNum
        string2 = str(line)
        string2 = string2.replace('(', '[')
        string2 = string2.replace(')', ']')
        print(string1, string2)
#restore the original print path
sys.stdout = temp






