from __future__ import division

import sys
import math

import pygame
from pygame.locals import *

#----------------------------------------
# Based on Grip by Stuart Laxton
#
#
#----------------------------------------

class Game:
    def __init__(self):
        pygame.init()
        self.mainClock = pygame.time.Clock()
        self._init_game_context()

        pass

    def _init_game_context(self):
        # set up the window
        WINDOWWIDTH = 800
        WINDOWHEIGHT = 400
        self.windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
        pygame.display.set_caption('PSZT')
        self.playerSettings = []

        # set up the colors
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)

        # set up variables
        self.moveLeft = False
        self.moveRight = False
        self.moveUp = False
        self.moveDown = False
        self.MOVESPEED = 50
        self.position = None
        self.playerImage = None
        self.carSettings = [16, 0, 12, 20, 2, 60, 2,
                       120]  # 0-Max Speed, 1-Current Count, 2-Acceleration rate, 3-Braking Rate, 4-Free Wheel, 5-Gear Change,6-Turn Speed,7-Max Boost
        self.movespeed = [0, 0, 2, 0]  # 0-Current movespeed, 1-Max movespeed, 2-Rotation speed, 3-Turn Speed Multiply
        self.position = [650, 250, 0, 0, 0, 0]  # 0-1 Track position, 2-3 Background position, 4-5 Previous position
        self.rotRect = (110, 44)
        self.degree = 0  # Player rotation angle
        self.radians = 0
        self.moveRadians = 0
        self.drawTrack = [1, 'laps1.txt']
        self.fps = [0, 60, 10, 60, 0]  # 0-On/Off, 1-Set Point, 2-Actual FPS, 3-Lowest Recorded, 4-Highest Recorded
        self.playerSettings = [WINDOWWIDTH / 2 - 50, WINDOWHEIGHT / 2, 0,
                          0]  # 0-Player Horizontal, 1-Player Vertical, 2-Rotation position (x5 for degrees)
        self.curser = [40, 190, 200, 50]  # Start position for the curser on the menu
        self.option = [0, 'Start Trial', 'Settings', 'Quit', 0]  # menu options
        self.oldFrontPosition = [0, 0]
        self.oldRearPosition = [0, 0]
        self.frontWheel = [0, 0]
        self.rearWheel = [0, 0]
        self.boost = []

        self.basicFont = pygame.font.Font("fonts/font_game.otf", 24)

        overheadImage = pygame.image.load('graphics/overhead_tile.png').convert_alpha()
        trackImage11 = pygame.image.load('graphics/b-1-1.png').convert_alpha()
        trackImage21 = pygame.image.load('graphics/b-2-1.png').convert_alpha()
        trackImage31 = pygame.image.load('graphics/b-3-1.png').convert_alpha()
        trackImage41 = pygame.image.load('graphics/b-4-1.png').convert_alpha()
        trackImage5 = pygame.image.load('graphics/st-v-3.png').convert_alpha()
        trackImage51 = pygame.image.load('graphics/st-v-3-k1.png').convert_alpha()
        trackImage52 = pygame.image.load('graphics/st-v-3-k2.png').convert_alpha()
        trackImage53 = pygame.image.load('graphics/st-v-3-k3.png').convert_alpha()
        trackImage54 = pygame.image.load('graphics/st-v-3-k4.png').convert_alpha()
        trackImage6 = pygame.image.load('graphics/st-h-3.png').convert_alpha()
        trackImage61 = pygame.image.load('graphics/st-h-3-k1.png').convert_alpha()
        trackImage62 = pygame.image.load('graphics/st-h-3-k2.png').convert_alpha()
        trackImage63 = pygame.image.load('graphics/st-h-3-k3.png').convert_alpha()
        trackImage64 = pygame.image.load('graphics/st-h-3-k4.png').convert_alpha()
        trackImage12 = pygame.image.load('graphics/b-1-2.png').convert_alpha()
        trackImage22 = pygame.image.load('graphics/b-2-2.png').convert_alpha()
        trackImage32 = pygame.image.load('graphics/b-3-2.png').convert_alpha()
        trackImage42 = pygame.image.load('graphics/b-4-2.png').convert_alpha()
        trackImage13 = pygame.image.load('graphics/b-1-3.png').convert_alpha()
        trackImage23 = pygame.image.load('graphics/b-2-3.png').convert_alpha()
        trackImage33 = pygame.image.load('graphics/b-3-3.png').convert_alpha()
        trackImage43 = pygame.image.load('graphics/b-4-3.png').convert_alpha()
        trackImage14 = pygame.image.load('graphics/b-1-4.png').convert_alpha()
        trackImage24 = pygame.image.load('graphics/b-2-4.png').convert_alpha()
        trackImage34 = pygame.image.load('graphics/b-3-4.png').convert_alpha()
        trackImage44 = pygame.image.load('graphics/b-4-4.png').convert_alpha()

    def main_game(self):
        pass


    def framerate(self):
        fps = self.fps
        self.mainClock.tick(fps[1])
        fps[2] = int(self.mainClock.get_fps())
        if fps[2] < fps[3]:
            fps[3] = fps[2]
        if fps[2] > fps[4]:
            fps[4] = fps[2]

    def menu(self):
        # run the menu loop
        self.moveUp = False
        self.moveDown = False

        while self.option[4] == 0:# Option [4] is the selection output bit
            # check for events
            for _event in pygame.event.get():
                if _event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if _event.type == KEYDOWN:
                        # change the keyboard variables
                        if _event.key == K_UP or _event.key == ord('w'):  # Curser Up
                            self.moveDown = False
                            self.moveUp = True
                        if _event.key == K_DOWN or _event.key == ord('s'):  # Curser Down
                            self.moveUp = False
                            self.moveDown = True
                        if _event.key == K_RETURN or _event.key == K_SPACE: # Select current option
                            if self.curser[1] == 190:  # Start game
                                self.position = [(self.WINDOWWIDTH/2)+50, (self.WINDOWHEIGHT/2)-50, 0, 0, 0, 0]
                                self.playerImage = playerGraphics()
                                self.boost = []
                                self.playerSettings[2] = 0
                                self.option[4] = 1
                            if self.curser[1] == 290:  # Quit game
                                pygame.quit()
                                sys.exit()

                if _event.type == KEYUP:
                        if _event.key == K_ESCAPE:
                            pygame.quit()
                            sys.exit()
                        if _event.key == K_UP or _event.key == ord('w'):
                            self.moveUp = False
                        if _event.key == K_DOWN or _event.key == ord('s'):
                            self.moveDown = False

            # move the Curser
            if self.moveDown and self.curser[1] < 290:
                self.curser[1] += self.MOVESPEED
                self.moveDown = False
            if self.moveUp and self.curser[1] > 180:
                self.curser[1] -= self.MOVESPEED
                self.moveUp = False

            # draw the background onto the surface & draw the banner
            drawBack()
            moveTrack()

            # draw the curser onto the surface
            pygame.draw.rect(windowSurface, WHITE, (curser[0],curser[1],curser[2],curser[3]),1)

            # draw the options onto the surface
            text1 = basicFont.render(option[1], True, WHITE,)
            text2 = basicFont.render(option[2], True, WHITE,)
            text3 = basicFont.render(option[3], True, WHITE,)
            windowSurface.blit(text1, (52,202))
            windowSurface.blit(text2, (52,252))
            windowSurface.blit(text3, (52,302))

            framerate()
            # draw the window onto the screen
            pygame.display.update()

def playerGraphics():
    playerImage = pygame.image.load('graphics/car4.png').convert_alpha()
    return playerImage

def moveTrack():
    windowSurface.blit(trackImage62,(position[0]-1000,position[1]-115))
    windowSurface.blit(trackImage6,(position[0]-700,position[1]-100))
    windowSurface.blit(trackImage6,(position[0]-400,position[1]-100))
    windowSurface.blit(trackImage6,(position[0]-100,position[1]-100))
    windowSurface.blit(trackImage6,(position[0],position[1]-100))
    windowSurface.blit(trackImage64,(position[0]+300,position[1]-100))
    windowSurface.blit(trackImage41,(position[0]+600,position[1]-100))
    windowSurface.blit(trackImage31,(position[0]+600,position[1]+300))
    windowSurface.blit(trackImage63,(position[0]+300,position[1]+385))
    windowSurface.blit(trackImage6,(position[0],position[1]+400))
    windowSurface.blit(trackImage6,(position[0]-300,position[1]+400))
    windowSurface.blit(trackImage61,(position[0]-600,position[1]+400))
    windowSurface.blit(trackImage12,(position[0]-1100,position[1]+400))
    windowSurface.blit(trackImage22,(position[0]-1100,position[1]+900))
    windowSurface.blit(trackImage62,(position[0]-600,position[1]+1085))
    windowSurface.blit(trackImage6,(position[0]-300,position[1]+1100))
    windowSurface.blit(trackImage6,(position[0],position[1]+1100))
    windowSurface.blit(trackImage6,(position[0]+300,position[1]+1100))
    windowSurface.blit(trackImage6,(position[0]+600,position[1]+1100))
    windowSurface.blit(trackImage63,(position[0]+900,position[1]+1085))
    windowSurface.blit(trackImage34,(position[0]+1200,position[1]+700))
    windowSurface.blit(trackImage53,(position[0]+1585,position[1]+400))
    windowSurface.blit(trackImage54,(position[0]+1585,position[1]+100))
    windowSurface.blit(trackImage41,(position[0]+1500,position[1]-300))
    windowSurface.blit(trackImage21,(position[0]+1100,position[1]-400))
    windowSurface.blit(trackImage44,(position[0]+700,position[1]-1100))
    windowSurface.blit(trackImage11,(position[0]+300,position[1]-1100))
    windowSurface.blit(trackImage31,(position[0]+200,position[1]-700))
    windowSurface.blit(trackImage63,(position[0]-100,position[1]-615))
    windowSurface.blit(trackImage62,(position[0]-100,position[1]-615))
    windowSurface.blit(trackImage22,(position[0]-600,position[1]-800))
    windowSurface.blit(trackImage41,(position[0]-700,position[1]-1200))
    windowSurface.blit(trackImage64,(position[0]-1000,position[1]-1200))
    windowSurface.blit(trackImage61,(position[0]-1000,position[1]-1200))
    windowSurface.blit(trackImage14,(position[0]-1700,position[1]-1200))
    windowSurface.blit(trackImage24,(position[0]-1700,position[1]-500))

def drawBack():
    if position[2] >= 200:
        position[2] -=200
    if position[2] <= -200:
        position[2] += 200
    if position[3] >= 200:
        position[3] -= 200
    if position[3] <= -200:
        position[3] += 200
    windowSurface.blit(overheadImage,(position[2]+1200,position[3]-200))
    windowSurface.blit(overheadImage,(position[2]+1000,position[3]-200))
    windowSurface.blit(overheadImage,(position[2]+800,position[3]-200))
    windowSurface.blit(overheadImage,(position[2]+600,position[3]-200))
    windowSurface.blit(overheadImage,(position[2]+400,position[3]-200))
    windowSurface.blit(overheadImage,(position[2]+200,position[3]-200))
    windowSurface.blit(overheadImage,(position[2],position[3]-200))
    windowSurface.blit(overheadImage,(position[2]-200,position[3]-200))
    windowSurface.blit(overheadImage,(position[2]+1200,position[3]))
    windowSurface.blit(overheadImage,(position[2]+1000,position[3]))
    windowSurface.blit(overheadImage,(position[2]+800,position[3]))
    windowSurface.blit(overheadImage,(position[2]+600,position[3]))
    windowSurface.blit(overheadImage,(position[2]+400,position[3]))
    windowSurface.blit(overheadImage,(position[2]+200,position[3]))
    windowSurface.blit(overheadImage,(position[2],position[3]))
    windowSurface.blit(overheadImage,(position[2]-200,position[3]))
    windowSurface.blit(overheadImage,(position[2]+1200,position[3]+200))
    windowSurface.blit(overheadImage,(position[2]+1000,position[3]+200))
    windowSurface.blit(overheadImage,(position[2]+800,position[3]+200))
    windowSurface.blit(overheadImage,(position[2]+600,position[3]+200))
    windowSurface.blit(overheadImage,(position[2]+400,position[3]+200))
    windowSurface.blit(overheadImage,(position[2]+200,position[3]+200))
    windowSurface.blit(overheadImage,(position[2],position[3]+200))
    windowSurface.blit(overheadImage,(position[2]-200,position[3]+200))
    windowSurface.blit(overheadImage,(position[2]+1200,position[3]+400))
    windowSurface.blit(overheadImage,(position[2]+1000,position[3]+400))
    windowSurface.blit(overheadImage,(position[2]+800,position[3]+400))
    windowSurface.blit(overheadImage,(position[2]+600,position[3]+400))
    windowSurface.blit(overheadImage,(position[2]+400,position[3]+400))
    windowSurface.blit(overheadImage,(position[2]+200,position[3]+400))
    windowSurface.blit(overheadImage,(position[2],position[3]+400))
    windowSurface.blit(overheadImage,(position[2]-200,position[3]+400))
    windowSurface.blit(overheadImage,(position[2]+1200,position[3]+600))
    windowSurface.blit(overheadImage,(position[2]+1000,position[3]+600))
    windowSurface.blit(overheadImage,(position[2]+800,position[3]+600))
    windowSurface.blit(overheadImage,(position[2]+600,position[3]+600))
    windowSurface.blit(overheadImage,(position[2]+400,position[3]+600))
    windowSurface.blit(overheadImage,(position[2]+200,position[3]+600))
    windowSurface.blit(overheadImage,(position[2],position[3]+600))
    windowSurface.blit(overheadImage,(position[2]-200,position[3]+600))

def getDistance(degree):
    x = oldCenter[0] + 62*math.cos(degree) # car.png has 110x44px; we need to be outside of it, even when degree = 45
    y = oldCenter[1] + 62*math.sin(degree) # dx, dy are taken form trigonometry
    pointAhead = (int(x), int(y))
    colour = windowSurface.get_at(pointAhead)
    while(colour[0] >= 88 and colour[0] <= 91 and colour[1]>=88 and colour[1]<=91 and colour[2]>=88 and colour[2] <= 91 # road colour = [89,89,89]
          and x<WINDOWWIDTH-6 and y<WINDOWHEIGHT-6 and x>6 and y>6):
        x = x+ 5*math.cos(degree) # cooridinates depend on the current angle, we check with the step 5px in both directions (x,y)
        y = y + 5*math.sin(degree)
        pointAhead = (int(x),int(y))
        colour = windowSurface.get_at(pointAhead)
    pygame.draw.rect(windowSurface, WHITE, (int(x), int(y), 5, 5), 1) # draw cursor
    distance = math.sqrt((x - oldCenter[0])**2 + (y- oldCenter[1])**2) # from formula for distance in x,y coordinate system
    textDistance = 'Distance ahead:'+ str(distance)
    textDisplay = basicFont.render(textDistance, True, WHITE, )
    windowSurface.blit(textDisplay, (20, 20))



def rotation(image,where,degree):
    # Calculate rotated graphics & centre position
    surf =  pygame.Surface((100,50))
    rotatedImage = pygame.transform.rotate(image,degree)
    blittedRect = windowSurface.blit(surf, where)
    oldCenter = blittedRect.center
    rotatedSurf =  pygame.transform.rotate(surf, degree)
    rotRect = rotatedSurf.get_rect()
    rotRect.center = oldCenter
    return rotatedImage, rotRect, oldCenter


menu()

while option[4]==1:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            # change the keyboard variables
            if event.key == K_LEFT:
                moveRight = False
                moveLeft = True
            if event.key == K_RIGHT:
                moveLeft = False
                moveRight = True
            if event.key == K_UP:
                moveDown = False
                moveUp = True
            if event.key == K_DOWN:
                moveDown = True
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                moveUp = False
                movespeed = [0,0,2,0]
                option[4]=0
                menu()
            if event.key == K_LEFT or event.key == ord('a'):
                moveLeft = False
            if event.key == K_RIGHT or event.key == ord('d'):
                moveRight = False
            if event.key == K_UP:
                moveUp = False
            if event.key == K_DOWN:
                moveDown = False

    # Get rotated graphics
    where = playerSettings[0], playerSettings[1]
    playerRotatedImage, rotRect, oldCenter = rotation(playerImage, where,degree)

    # draw the track background onto the surface
    drawBack()

    # draw the track onto the surface
    moveTrack()

    # Check the background colour
    colour = windowSurface.get_at((oldCenter))# centre colour
    if colour[0] >= 88 and colour[0] <= 91 or colour[0] == 165 or colour[0] == 255:
        1;
    else:
        movespeed[2] = 3
        if movespeed[0] >4:
            carSettings[1] -= carSettings[3]*2

    # draw the player onto the surface
    windowSurface.blit(playerRotatedImage,rotRect)

    # Calculate player direction rotation
    degree = -5 * playerSettings[2]
    moveRadians = radians = -degree * (3.142/180)

    position[0]-=(movespeed[0]*((math.cos(moveRadians))))
    position[1]-=(movespeed[0]*((math.sin(moveRadians))))
    frontWheel[0]=position[0]-(30*((math.cos(radians))))
    frontWheel[1]=position[1]-(30*((math.sin(radians))))
    rearWheel[0]=position[0]+(30*(math.cos(radians)))
    rearWheel[1]=position[1]+(30*(math.sin(radians)))
    position[2]-=(movespeed[0]*((math.cos(moveRadians))))
    position[3]-=(movespeed[0]*((math.sin(moveRadians))))

    if moveLeft:    # Turn Left
        if movespeed[0] > 0:
            carSettings[6]-=1
            if carSettings[6]==0:
                playerSettings[2] -= 1
                carSettings[6] = movespeed[2]
                if playerSettings[2] < 0:
                    playerSettings[2]=71

    if moveRight:
        if movespeed[0] > 0:
            carSettings[6]-=1
            if carSettings[6]==0:
                playerSettings[2] += 1
                carSettings[6] = movespeed[2]
                if playerSettings[2]>71:
                    playerSettings[2]=0

    # move the player
    if moveDown:    # Braking
        carSettings[1] -= carSettings[3]
    if moveUp:    # Accelerate
        carSettings[1] += carSettings[2]
    else:
        carSettings[1] -= carSettings[4]
        movespeed[1] = carSettings[0]

    if carSettings[1] >= carSettings[5] and movespeed[0] < movespeed[1]:# Change up gear
        movespeed[0] +=1
        carSettings[1] = 0
    elif carSettings[1] >= carSettings[5] and movespeed[0] >= movespeed[1]:# Accelerate Limiter
        carSettings[1] = carSettings[5]
    elif carSettings[1] < 0 and movespeed[0] == 0: # Braking limiter
        carSettings[1]=0
        movespeed[0]=0
    elif carSettings[1] <0:# Change down gears
        movespeed[0] -=1
        carSettings[1]=carSettings[5]
    if movespeed[0] > movespeed[1]:
        carSettings[1] -= carSettings[3]

    # draw the window onto the screen
    framerate()
    getDistance(moveRadians)
    pygame.display.update()
