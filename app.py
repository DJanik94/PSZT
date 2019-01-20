from __future__ import division

import sys
import math

import pygame
from pygame.locals import *
import controller
import random as r

# ----------------------------------------
# Based on Grip by Stuart Laxton
#
#
# ----------------------------------------


class Game:
    
    def __init__(self):
        pygame.init()
        self.mainClock = pygame.time.Clock()
        self._init_game_context()
        self._init_game_settings()
        self.controller = controller.FuzzyCarController()
        
    def _init_game_context(self):
        # set up the window
        self.WINDOWWIDTH = 1200
        self.WINDOWHEIGHT = 600
        self.window_surfacee = pygame.display.set_mode((self.WINDOWWIDTH, self.WINDOWHEIGHT), 0, 32)
        pygame.display.set_caption('PSZT Game Project')
        self.player_settings = []

        # set up the colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)

        # init variables
        self.move_left = False
        self.move_right = False
        self.move_up = False
        self.move_down = False
        self.old_center = None
        self.speed = 50
        self.player_image = None
        self.degree = 0  # Player rotation angle
        self.radians = 0
        self.move_radians = 0
        self.drawTrack = [1, 'laps1.txt']
        self.cursor = [40, 190, 200, 50]  # Start self.position for the cursor on the menu
        self.option = [0, 'Start Trial','Mode: player','Mode: auto','Quit', 0] # menu self.options
        self.old_front_position = [0, 0]
        self.old_read_position = [0, 0]
        self.front_wheel = [0, 0]
        self.rear_wheel = [0, 0]
        self.boost = []
        self.auto_mode = False
        self.number_of_boxes = 20
        self.box_positions = [(r.randint(-2500, 1200), r.randint(-2500, 1200)) for _ in range(self.number_of_boxes)]

        self.boxes_list = None
        self.basicFont = pygame.font.Font("fonts/font_game.otf", 24)

        self.overhead_image = pygame.image.load('graphics/overhead_tile.png').convert_alpha()
        self.trackImage11 = pygame.image.load('graphics/b-1-1.png').convert_alpha()
        self.trackImage21 = pygame.image.load('graphics/b-2-1.png').convert_alpha()
        self.trackImage31 = pygame.image.load('graphics/b-3-1.png').convert_alpha()
        self.trackImage41 = pygame.image.load('graphics/b-4-1.png').convert_alpha()
        self.trackImage53 = pygame.image.load('graphics/st-v-3-k3.png').convert_alpha()
        self.trackImage54 = pygame.image.load('graphics/st-v-3-k4.png').convert_alpha()
        self.trackImage6 = pygame.image.load('graphics/st-h-3.png').convert_alpha()
        self.trackImage61 = pygame.image.load('graphics/st-h-3-k1.png').convert_alpha()
        self.trackImage62 = pygame.image.load('graphics/st-h-3-k2.png').convert_alpha()
        self.trackImage63 = pygame.image.load('graphics/st-h-3-k3.png').convert_alpha()
        self.trackImage64 = pygame.image.load('graphics/st-h-3-k4.png').convert_alpha()
        self.trackImage12 = pygame.image.load('graphics/b-1-2.png').convert_alpha()
        self.trackImage22 = pygame.image.load('graphics/b-2-2.png').convert_alpha()
        self.trackImage14 = pygame.image.load('graphics/b-1-4.png').convert_alpha()
        self.trackImage24 = pygame.image.load('graphics/b-2-4.png').convert_alpha()
        self.trackImage34 = pygame.image.load('graphics/b-3-4.png').convert_alpha()
        self.trackImage44 = pygame.image.load('graphics/b-4-4.png').convert_alpha()
        self.boxImage = pygame.image.load('graphics/woodenBox.png').convert_alpha()

    def _init_game_settings(self):
        self.car_settings = [16,  # 0-Max Speed,
                             0,  # 1-Current Count
                             10,  # 2-Acceleration rate
                             80,  # 3-Braking Rate
                             2,  # 4-Free Wheel
                             80,  # 5-Gear Change
                             2,  # 6-Turn Speed
                             120,  # 7-Max Boost
                             1]     # 8 - Ratio Degree?

        self.move_speed = [0,  # 0-Current self.move_speed
                           0,  # 1-Max self.move_speed
                           2,  # 2-Rotation speed
                           0]  # 3-Turn Speed Multiply

        self.position = [650,  # 0-1 Track self.position
                         250,
                         0,  # 2-3 Background self.position
                         0,
                         0,  # 4-5 Previous self.position
                         0]

        self.fps = [0,  # 0-On/Off
                    60,  # 1-Set Point
                    10,  # 2-Actual FPS
                    60,  # 3-Lowest Recorded
                    0]  # 4-Highest Recorded

        self.player_settings = [self.WINDOWWIDTH / 2 - 50,  # 0-Player Horizontal
                               self.WINDOWHEIGHT / 2,  # 1-Player Vertical
                               0,  # 2-Rotation self.position (x5 for degrees)
                               0]

        self.rot_rect = (110, 44)


        
    def frame_rate(self):
        fps = self.fps
        self.mainClock.tick(fps[1])
        fps[2] = int(self.mainClock.get_fps())
        if fps[2] < fps[3]:
            fps[3] = fps[2]
        if fps[2] > fps[4]:
            fps[4] = fps[2]

    def menu(self):
        # run the menu loop
        self.move_up = False
        self.move_down = False
        self.move_left = False
        self.move_right = False
        self._init_game_settings()

        while self.option[5] == 0:  # self.option [5] is the selection output bit
            # check for events
            for _event in pygame.event.get():
                if _event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if _event.type == KEYDOWN:
                    # change the keyboard variables
                    if _event.key == K_UP or _event.key == ord('w'):  # cursor Up
                        self.move_down = False
                        self.move_up = True
                    if _event.key == K_DOWN or _event.key == ord('s'):  # cursor Down
                        self.move_up = False
                        self.move_down = True
                    if _event.key == K_RETURN or _event.key == K_SPACE:  # Select current self.option
                        if self.cursor[1] == 190:  # Start game
                            self.position = [(self.WINDOWWIDTH / 2) + 50, (self.WINDOWHEIGHT / 2) - 50, 0, 0, 0, 0]
                            self.player_image = self.player_graphics()
                            self.boost = []
                            self.player_settings[2] = 0
                            self.option[5] = 1
                        if self.cursor[1] == 290:  # Quit game
                            pygame.quit()
                            sys.exit()
                    if _event.key == K_RIGHT or _event.key == ord('a'):
                        if self.cursor[1] == 240:  # choose mode
                            if (self.auto_mode == True):
                                self.auto_mode = False
                            else:
                                self.auto_mode = True

                if _event.type == KEYUP:
                    if _event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if _event.key == K_UP or _event.key == ord('w'):
                        self.move_up = False
                    if _event.key == K_DOWN or _event.key == ord('s'):
                        self.move_down = False

            # move the cursor
            if self.move_down and self.cursor[1] < 290:
                self.cursor[1] += self.speed
                self.move_down = False
            if self.move_up and self.cursor[1] > 180:
                self.cursor[1] -= self.speed
                self.move_up = False

            # draw the background onto the surface & draw the banner
            self.drawBack()
            self.move_track()

            # draw the cursor onto the surface
            pygame.draw.rect(self.window_surfacee, self.WHITE,
                             (self.cursor[0], self.cursor[1], self.cursor[2], self.cursor[3]), 1)

            # draw the self.options onto the surface
            text1 = self.basicFont.render(self.option[1], True, self.WHITE, )
            if not self.auto_mode:
                text2 = self.basicFont.render(self.option[2], True, self.WHITE, )
            else:
                text2 = self.basicFont.render(self.option[3], True, self.WHITE, )

            text3 = self.basicFont.render(self.option[4], True, self.WHITE, )
            self.window_surfacee.blit(text1, (52, 202))
            self.window_surfacee.blit(text2, (52, 252))
            self.window_surfacee.blit(text3, (52, 302))

            self.frame_rate()
            # draw the window onto the screen
            pygame.display.update()

    def player_graphics(self):
        player_image = pygame.image.load('graphics/car.png').convert_alpha()
        return player_image

    def move_track(self):

        self.window_surfacee.blit(self.trackImage62, (self.position[0] - 1000, self.position[1] - 115))
        self.window_surfacee.blit(self.trackImage6, (self.position[0] - 700, self.position[1] - 100))
        self.window_surfacee.blit(self.trackImage6, (self.position[0] - 400, self.position[1] - 100))
        self.window_surfacee.blit(self.trackImage6, (self.position[0] - 100, self.position[1] - 100))
        self.window_surfacee.blit(self.trackImage6, (self.position[0], self.position[1] - 100))
        self.window_surfacee.blit(self.trackImage64, (self.position[0] + 300, self.position[1] - 100))
        self.window_surfacee.blit(self.trackImage41, (self.position[0] + 600, self.position[1] - 100))
        self.window_surfacee.blit(self.trackImage31, (self.position[0] + 600, self.position[1] + 300))
        self.window_surfacee.blit(self.trackImage63, (self.position[0] + 300, self.position[1] + 385))
        self.window_surfacee.blit(self.trackImage6, (self.position[0], self.position[1] + 400))
        self.window_surfacee.blit(self.trackImage6, (self.position[0] - 300, self.position[1] + 400))
        self.window_surfacee.blit(self.trackImage61, (self.position[0] - 600, self.position[1] + 400))
        self.window_surfacee.blit(self.trackImage12, (self.position[0] - 1100, self.position[1] + 400))
        self.window_surfacee.blit(self.trackImage22, (self.position[0] - 1100, self.position[1] + 900))
        self.window_surfacee.blit(self.trackImage62, (self.position[0] - 600, self.position[1] + 1085))
        self.window_surfacee.blit(self.trackImage6, (self.position[0] - 300, self.position[1] + 1100))
        self.window_surfacee.blit(self.trackImage6, (self.position[0], self.position[1] + 1100))
        self.window_surfacee.blit(self.trackImage6, (self.position[0] + 300, self.position[1] + 1100))
        self.window_surfacee.blit(self.trackImage6, (self.position[0] + 600, self.position[1] + 1100))
        self.window_surfacee.blit(self.trackImage63, (self.position[0] + 900, self.position[1] + 1085))
        self.window_surfacee.blit(self.trackImage34, (self.position[0] + 1200, self.position[1] + 700))
        self.window_surfacee.blit(self.trackImage53, (self.position[0] + 1585, self.position[1] + 400))
        self.window_surfacee.blit(self.trackImage54, (self.position[0] + 1585, self.position[1] + 100))
        self.window_surfacee.blit(self.trackImage41, (self.position[0] + 1500, self.position[1] - 300))
        self.window_surfacee.blit(self.trackImage21, (self.position[0] + 1100, self.position[1] - 400))
        self.window_surfacee.blit(self.trackImage44, (self.position[0] + 700, self.position[1] - 1100))
        self.window_surfacee.blit(self.trackImage11, (self.position[0] + 300, self.position[1] - 1100))
        self.window_surfacee.blit(self.trackImage31, (self.position[0] + 200, self.position[1] - 700))
        self.window_surfacee.blit(self.trackImage63, (self.position[0] - 100, self.position[1] - 615))
        self.window_surfacee.blit(self.trackImage62, (self.position[0] - 100, self.position[1] - 615))
        self.window_surfacee.blit(self.trackImage22, (self.position[0] - 600, self.position[1] - 800))
        self.window_surfacee.blit(self.trackImage41, (self.position[0] - 700, self.position[1] - 1200))
        self.window_surfacee.blit(self.trackImage64, (self.position[0] - 1000, self.position[1] - 1200))
        self.window_surfacee.blit(self.trackImage61, (self.position[0] - 1000, self.position[1] - 1200))
        self.window_surfacee.blit(self.trackImage14, (self.position[0] - 1700, self.position[1] - 1200))
        self.window_surfacee.blit(self.trackImage24, (self.position[0] - 1700, self.position[1] - 500))

        #for point in self.box_positions:
            #self.window_surfacee.blit(self.boxImage, (self.position[0] + point[0], self.position[1] + point[1]))

        self.boxes_list = [None]*5
        self.window_surfacee.blit(self.boxImage, (self.position[0] - 120, self.position[1] - 20))
        self.window_surfacee.blit(self.boxImage, (self.position[0] - 45, self.position[1] - 300))
        self.window_surfacee.blit(self.boxImage, (self.position[0] - 10, self.position[1] - 200))
        self.window_surfacee.blit(self.boxImage, (self.position[0] - 500, self.position[1] - 500))
        self.window_surfacee.blit(self.boxImage, (self.position[0] + 300, self.position[1] + 100))
        box0 = Rect(self.position[0] - 120, self.position[1] - 20, 50, 50)
        box1 = Rect(self.position[0] - 45, self.position[1] - 300, 50, 50)
        box2 = Rect(self.position[0] - 10, self.position[1] - 200, 50, 50)
        box3 = Rect(self.position[0] - 500, self.position[1] - 500, 50, 50)
        box4 = Rect(self.position[0] + 300, self.position[1] + 100, 50, 50)
        self.boxes_list[0] = box0
        self.boxes_list[1] = box1
        self.boxes_list[2] = box2
        self.boxes_list[3] = box3
        self.boxes_list[4] = box4

        """self.boxes_list = [Rect(self.position[0] + position[0], self.position[1] + position[1], 50, 50) for position in self.box_positions]

        for point in self.box_positions:
            self.window_surfacee.blit(self.boxImage, (self.position[0] + point[0], self.position[1] + point[1]))"""

    def drawBack(self):
        if self.position[2] >= 200:
            self.position[2] -= 200
        if self.position[2] <= -200:
            self.position[2] += 200
        if self.position[3] >= 200:
            self.position[3] -= 200
        if self.position[3] <= -200:
            self.position[3] += 200
        self.window_surfacee.blit(self.overhead_image, (self.position[2] + 1200, self.position[3] - 200))
        self.window_surfacee.blit(self.overhead_image, (self.position[2] + 1000, self.position[3] - 200))
        self.window_surfacee.blit(self.overhead_image, (self.position[2] + 800, self.position[3] - 200))
        self.window_surfacee.blit(self.overhead_image, (self.position[2] + 600, self.position[3] - 200))
        self.window_surfacee.blit(self.overhead_image, (self.position[2] + 400, self.position[3] - 200))
        self.window_surfacee.blit(self.overhead_image, (self.position[2] + 200, self.position[3] - 200))
        self.window_surfacee.blit(self.overhead_image, (self.position[2], self.position[3] - 200))
        self.window_surfacee.blit(self.overhead_image, (self.position[2] - 200, self.position[3] - 200))
        self.window_surfacee.blit(self.overhead_image, (self.position[2] + 1200, self.position[3]))
        self.window_surfacee.blit(self.overhead_image, (self.position[2] + 1000, self.position[3]))
        self.window_surfacee.blit(self.overhead_image, (self.position[2] + 800, self.position[3]))
        self.window_surfacee.blit(self.overhead_image, (self.position[2] + 600, self.position[3]))
        self.window_surfacee.blit(self.overhead_image, (self.position[2] + 400, self.position[3]))
        self.window_surfacee.blit(self.overhead_image, (self.position[2] + 200, self.position[3]))
        self.window_surfacee.blit(self.overhead_image, (self.position[2], self.position[3]))
        self.window_surfacee.blit(self.overhead_image, (self.position[2] - 200, self.position[3]))
        self.window_surfacee.blit(self.overhead_image, (self.position[2] + 1200, self.position[3] + 200))
        self.window_surfacee.blit(self.overhead_image, (self.position[2] + 1000, self.position[3] + 200))
        self.window_surfacee.blit(self.overhead_image, (self.position[2] + 800, self.position[3] + 200))
        self.window_surfacee.blit(self.overhead_image, (self.position[2] + 600, self.position[3] + 200))
        self.window_surfacee.blit(self.overhead_image, (self.position[2] + 400, self.position[3] + 200))
        self.window_surfacee.blit(self.overhead_image, (self.position[2] + 200, self.position[3] + 200))
        self.window_surfacee.blit(self.overhead_image, (self.position[2], self.position[3] + 200))
        self.window_surfacee.blit(self.overhead_image, (self.position[2] - 200, self.position[3] + 200))
        self.window_surfacee.blit(self.overhead_image, (self.position[2] + 1200, self.position[3] + 400))
        self.window_surfacee.blit(self.overhead_image, (self.position[2] + 1000, self.position[3] + 400))
        self.window_surfacee.blit(self.overhead_image, (self.position[2] + 800, self.position[3] + 400))
        self.window_surfacee.blit(self.overhead_image, (self.position[2] + 600, self.position[3] + 400))
        self.window_surfacee.blit(self.overhead_image, (self.position[2] + 400, self.position[3] + 400))
        self.window_surfacee.blit(self.overhead_image, (self.position[2] + 200, self.position[3] + 400))
        self.window_surfacee.blit(self.overhead_image, (self.position[2], self.position[3] + 400))
        self.window_surfacee.blit(self.overhead_image, (self.position[2] - 200, self.position[3] + 400))
        self.window_surfacee.blit(self.overhead_image, (self.position[2] + 1200, self.position[3] + 600))
        self.window_surfacee.blit(self.overhead_image, (self.position[2] + 1000, self.position[3] + 600))
        self.window_surfacee.blit(self.overhead_image, (self.position[2] + 800, self.position[3] + 600))
        self.window_surfacee.blit(self.overhead_image, (self.position[2] + 600, self.position[3] + 600))
        self.window_surfacee.blit(self.overhead_image, (self.position[2] + 400, self.position[3] + 600))
        self.window_surfacee.blit(self.overhead_image, (self.position[2] + 200, self.position[3] + 600))
        self.window_surfacee.blit(self.overhead_image, (self.position[2], self.position[3] + 600))
        self.window_surfacee.blit(self.overhead_image, (self.position[2] - 200, self.position[3] + 600))

    def getDistance(self, degree):
        degree_d = 17 * (3.142 / 180)
        x_a = self.old_center[0] + 62 * math.cos(
            degree)  # car.png has 110x44px; we need to be outside of it, even when degree = 45
        y_a = self.old_center[1] + 62 * math.sin(degree)  # dx, dy are taken form trigonometry
        x_l = self.old_center[0] + 62 * math.cos(degree - degree_d)
        y_l = self.old_center[1] + 62 * math.sin(degree - degree_d)
        x_r = self.old_center[0] + 62 * math.cos(degree + degree_d)
        y_r = self.old_center[1] + 62 * math.sin(degree + degree_d)
        point_a = (int(x_a), int(y_a))
        point_l = (int(x_l), int(y_l))
        point_r = (int(x_r), int(y_r))
        colour_a = self.window_surfacee.get_at(point_a)
        colour_l = self.window_surfacee.get_at(point_l)
        colour_r = self.window_surfacee.get_at(point_r)

        while (88 <= colour_a[0] <= 91 and 88 <= colour_a[1] <= 91 and 88 <= colour_a[2] <= 91
               and x_a < self.WINDOWWIDTH - 6 and y_a < self.WINDOWHEIGHT - 6 and x_a > 6 and y_a > 6):
            x_a = x_a + 2 * math.cos(degree)
            y_a = y_a + 2 * math.sin(degree)
            point_a = (int(x_a), int(y_a))
            colour_a = self.window_surfacee.get_at(point_a)
        while (88 <= colour_l[0] <= 91 and 91 >= colour_l[1] >= 88 <= colour_l[2] <= 91
               and x_l < self.WINDOWWIDTH - 6 and y_l < self.WINDOWHEIGHT - 6 and x_l > 6 and y_l > 6):
            x_l = x_l + 2 * math.cos(degree - degree_d)
            y_l = y_l + 2 * math.sin(degree - degree_d)
            point_l = (int(x_l), int(y_l))
            colour_l = self.window_surfacee.get_at(point_l)
        while (88 <= colour_r[0] <= 91 and 88 <= colour_r[1] <= 91 and 88 <= colour_r[2] <= 91
               and x_r < self.WINDOWWIDTH - 6 and y_r < self.WINDOWHEIGHT - 6 and x_r > 6 and y_r > 6):
            x_r = x_r + 2 * math.cos(degree + degree_d)
            y_r = y_r + 2 * math.sin(degree + degree_d)
            point_r = (int(x_r), int(y_r))
            colour_r = self.window_surfacee.get_at(point_r)
        pygame.draw.rect(self.window_surfacee, self.WHITE, (int(x_a), int(y_a), 5, 5), 1)
        pygame.draw.rect(self.window_surfacee, self.WHITE, (int(x_l), int(y_l), 5, 5), 1)
        pygame.draw.rect(self.window_surfacee, self.WHITE, (int(x_r), int(y_r), 5, 5), 1)

        distanceAhead = math.sqrt((x_a - self.old_center[0]) ** 2 + (y_a - self.old_center[1]) ** 2) - 62
        distanceRight = math.sqrt((x_r - self.old_center[0]) ** 2 + (y_r - self.old_center[1]) ** 2) - 62
        distanceLeft = math.sqrt((x_l - self.old_center[0]) ** 2 + (y_l - self.old_center[1]) ** 2) - 62
        textDistance = 'Distance ahead:' + str(distanceAhead)
        textDisplay = self.basicFont.render(textDistance, True, self.WHITE, )
        #self.window_surfacee.blit(textDisplay, (20, 20))
        #print (round(distanceLeft, 2), round(distanceAhead, 2),  round(distanceRight, 2))
        return round(distanceLeft, 2), round(distanceAhead, 2),  round(distanceRight, 2)

    def collisionDetect(self, degree):
        if self.rot_rect.collidelist(self.boxes_list) != -1:
            colliding_box = self.boxes_list[self.rot_rect.collidelist(self.boxes_list)]
            xA = self.old_center[0] + 44 * math.cos(degree)
            yA = self.old_center[1] + 44 * math.sin(degree)
            xB = self.old_center[0] - 44 * math.cos(degree)
            yB = self.old_center[1] - 44 * math.sin(degree)
            distanceAhead = math.sqrt((xA - colliding_box.center[0]) ** 2 + (yA - colliding_box.center[1]) ** 2)
            distanceBackwards = math.sqrt((xB - colliding_box.center[0]) ** 2 + (yB - colliding_box.center[1]) ** 2)
            pygame.draw.rect(self.window_surfacee, self.WHITE, (int(xA), int(yA), 5, 5), 1)  # for tests
            pygame.draw.rect(self.window_surfacee, self.WHITE, (int(xB), int(yB), 5, 5), 1)  # for tests
            if (distanceAhead < 50):
                self.car_settings[1] = -self.car_settings[1]  # value from tests
                self.move_speed[0] = -5

            elif (distanceBackwards < 50):
                self.car_settings[1] = -self.car_settings[1]  # value from tests
                self.move_speed[0] = 5


    def rotation(self, image, where, degree):
        # Calculate rotated graphics & centre self.position
        surf = pygame.Surface((100, 50))
        rotated_image = pygame.transform.rotate(image, degree)
        blitted_rect = self.window_surfacee.blit(surf, where)
        old_center = blitted_rect.center
        rotated_surf = pygame.transform.rotate(surf, degree)
        rot_rect = rotated_surf.get_rect()
        rot_rect.center = old_center
        return rotated_image, rot_rect, old_center

    def play(self):

        self.menu()

        where = self.player_settings[0], self.player_settings[1]
        self.playerrotated_image, self.rot_rect, self.old_center = self.rotation(self.player_image, where, self.degree)
        #self.auto_mode = True
        while self.option[5] == 1:
            if self.auto_mode:
                self.auto_control()
            else:
                self.player_control()

            # Get rotated graphics
            where = self.player_settings[0], self.player_settings[1]
            self.playerrotated_image, self.rot_rect, self.old_center = self.rotation(self.player_image, where, self.degree)

            # draw the track background onto the surface
            self.drawBack()

            # draw the track onto the surface
            self.move_track()

            # Check the background colour
            colour = self.window_surfacee.get_at(self.old_center)  # centre colour
            if colour[0] >= 88 and colour[0] <= 91 or colour[0] == 165 or colour[0] == 255:
                1;
            else:
                self.move_speed[2] = 3
                if self.move_speed[0] > 4:
                    self.car_settings[1] -= self.car_settings[3] * 2

            # draw the player onto the surface
            self.window_surfacee.blit(self.playerrotated_image, self.rot_rect)

            # Calculate player direction rotation
            self.degree = -5 * self.player_settings[2]
            self.move_radians = radians = -self.degree * (3.142 / 180)

            self.position[0] -= (self.move_speed[0] * ((math.cos(self.move_radians))))
            self.position[1] -= (self.move_speed[0] * ((math.sin(self.move_radians))))
            self.front_wheel[0] = self.position[0] - (30 * ((math.cos(radians))))
            self.front_wheel[1] = self.position[1] - (30 * ((math.sin(radians))))
            self.rear_wheel[0] = self.position[0] + (30 * (math.cos(radians)))
            self.rear_wheel[1] = self.position[1] + (30 * (math.sin(radians)))
            self.position[2] -= (self.move_speed[0] * ((math.cos(self.move_radians))))
            self.position[3] -= (self.move_speed[0] * ((math.sin(self.move_radians))))

            if self.move_left:  # Turn Left
                if self.move_speed[0] != 0:
                    self.car_settings[6] -= 1
                    if self.car_settings[6] == 0:
                        self.player_settings[2] -= self.car_settings[8]
                        self.car_settings[6] = self.move_speed[2]
                        if self.player_settings[2] < 0:
                            self.player_settings[2] = 71

            if self.move_right:
                if self.move_speed[0] != 0:
                    self.car_settings[6] -= 1
                    if self.car_settings[6] == 0:
                        self.player_settings[2] += self.car_settings[8]
                        self.car_settings[6] = self.move_speed[2]
                        if self.player_settings[2] > 71:
                            self.player_settings[2] = 0

                # move the player
                if self.move_down:  # Braking
                    self.car_settings[1] -= self.car_settings[3]
                if self.move_up:  # Accelerate
                    self.car_settings[1] += self.car_settings[2]
                elif self.move_speed[0] >= 0:
                    self.car_settings[1] -= self.car_settings[4]
                    self.move_speed[1] = self.car_settings[0]
                elif self.move_speed[0] < 0:
                    self.car_settings[1] += self.car_settings[4]
                    self.move_speed[1] = self.car_settings[0]

                if self.car_settings[1] >= self.car_settings[5] and self.move_speed[0] < self.move_speed[1]:  # Change up gear
                    self.move_speed[0] += 1
                    self.car_settings[1] = 0
                elif self.car_settings[1] >= self.car_settings[5] and self.move_speed[0] >= self.move_speed[1]:  # Accelerate Limiter
                    self.car_settings[1] = self.car_settings[5]
                elif self.car_settings[1] < 0 and self.move_speed[0] == -self.car_settings[0] and self.move_down:  # moveBackwards
                    self.car_settings[1] = -self.car_settings[1]
                elif self.car_settings[1] < 0 and self.move_speed[0] <= 0 and self.move_down == False:  # Braking limiter
                    self.car_settings[1] = 0
                    self.move_speed[0] = 0
                elif self.car_settings[1] < 0:  # Change down gears
                    self.move_speed[0] -= 1
                    self.car_settings[1] = self.car_settings[5]
                if self.move_speed[0] > self.move_speed[1]:
                    self.car_settings[1] -= self.car_settings[3]

            self.collisionDetect(self.move_radians)
            # draw the window onto the screen
            self.frame_rate()
            self.getDistance(self.move_radians)
            pygame.display.update()

    def player_control(self):
        for _event in pygame.event.get():
            if _event.type == QUIT:
                pygame.quit()
                sys.exit()
            if _event.type == KEYDOWN:
                # change the keyboard variables
                if _event.key == K_LEFT:
                    self.move_right = False
                    self.move_left = True
                if _event.key == K_RIGHT:
                    self.move_left = False
                    self.move_right = True
                if _event.key == K_UP:
                    self.move_down = False
                    self.move_up = True
                if _event.key == K_DOWN:
                    self.move_down = True
            if _event.type == KEYUP:
                if _event.key == K_ESCAPE:
                    self.move_up = False
                    self.move_speed = [0, 0, 2, 0]
                    self.option[5] = 0
                    self.menu()
                if _event.key == K_LEFT or _event.key == ord('a'):
                    self.move_left = False
                if _event.key == K_RIGHT or _event.key == ord('d'):
                    self.move_right = False
                if _event.key == K_UP:
                    self.move_up = False
                if _event.key == K_DOWN:
                    self.move_down = False

    def auto_control(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    self.move_up = False
                    self.move_speed = [0, 0, 2, 0]
                    self.option[5] = 0
                    self.menu()

        left, ahead, right = self.getDistance(self.move_radians)
        speedRatio, dirRatio = self.controller.compute(left, ahead, right)
        #speedRatio =100;
        #dirRatio = -100;
        if (dirRatio < 0):  # <
            self.car_settings[8] = (-dirRatio + 110) * 0.01  # from 0.1 to 2.1
            self.move_left = True
            self.move_right = False
        if (dirRatio > 0):
            self.car_settings[8] = (dirRatio + 110) * 0.01
            self.move_left = False
            self.move_right = True
        if (dirRatio == 0):
            self.move_left = False
            self.move_right = False
        if (speedRatio > 0):
            self.car_settings[2] = abs(speedRatio) * 0.1  # from 0 to 12
            self.move_up = True
            self.move_down = False
        if (speedRatio < 0):  # >
            self.car_settings[3] = abs(speedRatio) * 1.2  # from 0 to 20  ->100
            self.move_up = False
            self.move_down = True
        if (speedRatio == 0):
            self.move_up = False
            self.move_down = False




if __name__ == '__main__':
    game = Game()
    game.play()
