import pygame

class status(object):
    AIRBORNE = "Airborne"
    GROUNDED = "Ground"
    
    
class actionType(object):
    GROUND = "Ground"
    AIR = "Air"
    SMASH = "Smash"

#this will be used to help keep track of previous and currrent action
class move(object):
    IDLE = "Idle"
    WALK = "Walk"
    JUMP = "Jump"
    CROUCH = "Crouch"
    UNCROUCH = "Uncrouch"
    BLOCK = "Block"
    FALL = "Fall"
    FALLSTUNNED = "FallStunned"
    LAND = "Land"
    LANDSTUNNED = "LandStunned"
    LAY = "Lay"
    GETUP = "Getup"
    nHIT = "neutralHit"
    sHIT = "sideHit"
    uHIT = "upHit"
    dHIT = "downHit"
    nSPC = "neutralSpecial"
    sSPC = "sideSpecial"
    uSPC = "upSpecial"
    dSPC = "downSpecial"
    sSMASH = "sideSmash"
    uSMASH = "upSmash"
    dSMASH = "downSmash"
    nAIR = "neutralAir"
    fAIR = "forwardAir"
    dAIR = "downAir"
    uAIR = "upAir"
    bAIR = "backAir"
    nAIRSPC = "neutralAirSpecial"
    sAIRSPC = "sideAirSpecial"
    uAIRSPC = "upAirSpecial"
    dAIRSPC = "downAirSpecial"

    #putting these in an array will add functionality with the parallel indexes
    array = [IDLE, WALK, JUMP, CROUCH, UNCROUCH, BLOCK, FALL, FALLSTUNNED,
            LAND, LANDSTUNNED, LAY, GETUP, nHIT, sHIT, uHIT, dHIT,
            nSPC, sSPC, uSPC, dSPC, sSMASH, uSMASH, dSMASH, nAIR,
            fAIR, dAIR, uAIR, bAIR, nAIRSPC, sAIRSPC, uAIRSPC, dAIRSPC]            

class direction(object):
    RIGHT = "Right"
    LEFT = "Left"

class jedi(object):
    filename = "jedi.png"
    width = 200
    height = 128
    rows = 14
    cols = 13

class controls(object):
    #up, down, left, right
    #normal hit, smash hit, special, jump, 
    players = [[pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d,
                pygame.K_t, pygame.K_y, pygame.K_u, pygame.K_SPACE],
               [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT,
                pygame.K_KP7, pygame.K_KP8, pygame.K_KP9, pygame.K_KP0]]

class color(object):
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 191, 255)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    DARK_BLUE = (0, 0, 255)
    players = [GREEN, DARK_BLUE]
    weapons = [RED, DARK_BLUE]

class physics(object):
    g = 10
    
