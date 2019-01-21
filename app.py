from __future__ import division

import sys
import math

import pygame
from pygame.locals import *


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
        
    def _init_game_context(self):
        # set up the window
        self.WINDOWWIDTH = 800
        self.WINDOWHEIGHT = 400
        self.window_surface = pygame.display.set_mode((self.WINDOWWIDTH, self.WINDOWHEIGHT), 0, 32)
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
        self.option = [0, 'Start Trial', 'Settings', 'Quit', 0]  # menu self.options
        self.old_front_position = [0, 0]
        self.old_read_position = [0, 0]
        self.front_wheel = [0, 0]
        self.rear_wheel = [0, 0]
        self.boost = []

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

    def _init_game_settings(self):
        self.car_settings = [16,  # 0-Max Speed,
                             0,  # 1-Current Count
                             12,  # 2-Acceleration rate
                             20,  # 3-Braking Rate
                             2,  # 4-Free Wheel
                             60,  # 5-Gear Change
                             2,  # 6-Turn Speed
                             120]  # 7-Max Boost

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

        while self.option[4] == 0:  # self.option [4] is the selection output bit
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
                            self.option[4] = 1
                        if self.cursor[1] == 290:  # Quit game
                            pygame.quit()
                            sys.exit()

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
            pygame.draw.rect(self.window_surface, self.WHITE,
                             (self.cursor[0], self.cursor[1], self.cursor[2], self.cursor[3]), 1)

            # draw the self.options onto the surface
            text1 = self.basicFont.render(self.option[1], True, self.WHITE, )
            text2 = self.basicFont.render(self.option[2], True, self.WHITE, )
            text3 = self.basicFont.render(self.option[3], True, self.WHITE, )
            self.window_surface.blit(text1, (52, 202))
            self.window_surface.blit(text2, (52, 252))
            self.window_surface.blit(text3, (52, 302))

            self.frame_rate()
            # draw the window onto the screen
            pygame.display.update()

    def player_graphics(self):
        player_image = pygame.image.load('graphics/car4.png').convert_alpha()
        return player_image

    def move_track(self):

        self.window_surface.blit(self.trackImage62, (self.position[0] - 1000, self.position[1] - 115))
        self.window_surface.blit(self.trackImage6, (self.position[0] - 700, self.position[1] - 100))
        self.window_surface.blit(self.trackImage6, (self.position[0] - 400, self.position[1] - 100))
        self.window_surface.blit(self.trackImage6, (self.position[0] - 100, self.position[1] - 100))
        self.window_surface.blit(self.trackImage6, (self.position[0], self.position[1] - 100))
        self.window_surface.blit(self.trackImage64, (self.position[0] + 300, self.position[1] - 100))
        self.window_surface.blit(self.trackImage41, (self.position[0] + 600, self.position[1] - 100))
        self.window_surface.blit(self.trackImage31, (self.position[0] + 600, self.position[1] + 300))
        self.window_surface.blit(self.trackImage63, (self.position[0] + 300, self.position[1] + 385))
        self.window_surface.blit(self.trackImage6, (self.position[0], self.position[1] + 400))
        self.window_surface.blit(self.trackImage6, (self.position[0] - 300, self.position[1] + 400))
        self.window_surface.blit(self.trackImage61, (self.position[0] - 600, self.position[1] + 400))
        self.window_surface.blit(self.trackImage12, (self.position[0] - 1100, self.position[1] + 400))
        self.window_surface.blit(self.trackImage22, (self.position[0] - 1100, self.position[1] + 900))
        self.window_surface.blit(self.trackImage62, (self.position[0] - 600, self.position[1] + 1085))
        self.window_surface.blit(self.trackImage6, (self.position[0] - 300, self.position[1] + 1100))
        self.window_surface.blit(self.trackImage6, (self.position[0], self.position[1] + 1100))
        self.window_surface.blit(self.trackImage6, (self.position[0] + 300, self.position[1] + 1100))
        self.window_surface.blit(self.trackImage6, (self.position[0] + 600, self.position[1] + 1100))
        self.window_surface.blit(self.trackImage63, (self.position[0] + 900, self.position[1] + 1085))
        self.window_surface.blit(self.trackImage34, (self.position[0] + 1200, self.position[1] + 700))
        self.window_surface.blit(self.trackImage53, (self.position[0] + 1585, self.position[1] + 400))
        self.window_surface.blit(self.trackImage54, (self.position[0] + 1585, self.position[1] + 100))
        self.window_surface.blit(self.trackImage41, (self.position[0] + 1500, self.position[1] - 300))
        self.window_surface.blit(self.trackImage21, (self.position[0] + 1100, self.position[1] - 400))
        self.window_surface.blit(self.trackImage44, (self.position[0] + 700, self.position[1] - 1100))
        self.window_surface.blit(self.trackImage11, (self.position[0] + 300, self.position[1] - 1100))
        self.window_surface.blit(self.trackImage31, (self.position[0] + 200, self.position[1] - 700))
        self.window_surface.blit(self.trackImage63, (self.position[0] - 100, self.position[1] - 615))
        self.window_surface.blit(self.trackImage62, (self.position[0] - 100, self.position[1] - 615))
        self.window_surface.blit(self.trackImage22, (self.position[0] - 600, self.position[1] - 800))
        self.window_surface.blit(self.trackImage41, (self.position[0] - 700, self.position[1] - 1200))
        self.window_surface.blit(self.trackImage64, (self.position[0] - 1000, self.position[1] - 1200))
        self.window_surface.blit(self.trackImage61, (self.position[0] - 1000, self.position[1] - 1200))
        self.window_surface.blit(self.trackImage14, (self.position[0] - 1700, self.position[1] - 1200))
        self.window_surface.blit(self.trackImage24, (self.position[0] - 1700, self.position[1] - 500))

    def drawBack(self):
        if self.position[2] >= 200:
            self.position[2] -= 200
        if self.position[2] <= -200:
            self.position[2] += 200
        if self.position[3] >= 200:
            self.position[3] -= 200
        if self.position[3] <= -200:
            self.position[3] += 200
        self.window_surface.blit(self.overhead_image, (self.position[2] + 1200, self.position[3] - 200))
        self.window_surface.blit(self.overhead_image, (self.position[2] + 1000, self.position[3] - 200))
        self.window_surface.blit(self.overhead_image, (self.position[2] + 800, self.position[3] - 200))
        self.window_surface.blit(self.overhead_image, (self.position[2] + 600, self.position[3] - 200))
        self.window_surface.blit(self.overhead_image, (self.position[2] + 400, self.position[3] - 200))
        self.window_surface.blit(self.overhead_image, (self.position[2] + 200, self.position[3] - 200))
        self.window_surface.blit(self.overhead_image, (self.position[2], self.position[3] - 200))
        self.window_surface.blit(self.overhead_image, (self.position[2] - 200, self.position[3] - 200))
        self.window_surface.blit(self.overhead_image, (self.position[2] + 1200, self.position[3]))
        self.window_surface.blit(self.overhead_image, (self.position[2] + 1000, self.position[3]))
        self.window_surface.blit(self.overhead_image, (self.position[2] + 800, self.position[3]))
        self.window_surface.blit(self.overhead_image, (self.position[2] + 600, self.position[3]))
        self.window_surface.blit(self.overhead_image, (self.position[2] + 400, self.position[3]))
        self.window_surface.blit(self.overhead_image, (self.position[2] + 200, self.position[3]))
        self.window_surface.blit(self.overhead_image, (self.position[2], self.position[3]))
        self.window_surface.blit(self.overhead_image, (self.position[2] - 200, self.position[3]))
        self.window_surface.blit(self.overhead_image, (self.position[2] + 1200, self.position[3] + 200))
        self.window_surface.blit(self.overhead_image, (self.position[2] + 1000, self.position[3] + 200))
        self.window_surface.blit(self.overhead_image, (self.position[2] + 800, self.position[3] + 200))
        self.window_surface.blit(self.overhead_image, (self.position[2] + 600, self.position[3] + 200))
        self.window_surface.blit(self.overhead_image, (self.position[2] + 400, self.position[3] + 200))
        self.window_surface.blit(self.overhead_image, (self.position[2] + 200, self.position[3] + 200))
        self.window_surface.blit(self.overhead_image, (self.position[2], self.position[3] + 200))
        self.window_surface.blit(self.overhead_image, (self.position[2] - 200, self.position[3] + 200))
        self.window_surface.blit(self.overhead_image, (self.position[2] + 1200, self.position[3] + 400))
        self.window_surface.blit(self.overhead_image, (self.position[2] + 1000, self.position[3] + 400))
        self.window_surface.blit(self.overhead_image, (self.position[2] + 800, self.position[3] + 400))
        self.window_surface.blit(self.overhead_image, (self.position[2] + 600, self.position[3] + 400))
        self.window_surface.blit(self.overhead_image, (self.position[2] + 400, self.position[3] + 400))
        self.window_surface.blit(self.overhead_image, (self.position[2] + 200, self.position[3] + 400))
        self.window_surface.blit(self.overhead_image, (self.position[2], self.position[3] + 400))
        self.window_surface.blit(self.overhead_image, (self.position[2] - 200, self.position[3] + 400))
        self.window_surface.blit(self.overhead_image, (self.position[2] + 1200, self.position[3] + 600))
        self.window_surface.blit(self.overhead_image, (self.position[2] + 1000, self.position[3] + 600))
        self.window_surface.blit(self.overhead_image, (self.position[2] + 800, self.position[3] + 600))
        self.window_surface.blit(self.overhead_image, (self.position[2] + 600, self.position[3] + 600))
        self.window_surface.blit(self.overhead_image, (self.position[2] + 400, self.position[3] + 600))
        self.window_surface.blit(self.overhead_image, (self.position[2] + 200, self.position[3] + 600))
        self.window_surface.blit(self.overhead_image, (self.position[2], self.position[3] + 600))
        self.window_surface.blit(self.overhead_image, (self.position[2] - 200, self.position[3] + 600))

    def getDistance(self, degree):
        x = self.old_center[0] + 62 * math.cos(
            degree)  # car.png has 110x44px; we need to be outside of it, even when degree = 45
        y = self.old_center[1] + 62 * math.sin(degree)  # dx, dy are taken form trigonometry
        point_ahead = (int(x), int(y))
        colour = self.window_surface.get_at(point_ahead)
        while (colour[0] >= 88 and colour[0] <= 91 and colour[1] >= 88 and colour[1] <= 91 and colour[2] >= 88 and
               colour[2] <= 91  # road colour = [89,89,89]
               and x < self.WINDOWWIDTH - 6 and y < self.WINDOWHEIGHT - 6 and x > 6 and y > 6):
            x = x + 5 * math.cos(
                degree)  # cooridinates depend on the current angle, we check with the step 5px in both directions (x,y)
            y = y + 5 * math.sin(degree)
            point_ahead = (int(x), int(y))
            colour = self.window_surface.get_at(point_ahead)
        pygame.draw.rect(self.window_surface, self.WHITE, (int(x), int(y), 5, 5), 1)  # draw cursor
        distance = math.sqrt((x - self.old_center[0]) ** 2 + (
                y - self.old_center[1]) ** 2)  # from formula for distance in x,y coordinate system
        text_distance = 'Distance ahead:' + str(distance)
        text_display = self.basicFont.render(text_distance, True, self.WHITE, )
        self.window_surface.blit(text_display, (20, 20))

    def rotation(self, image, where, degree):
        # Calculate rotated graphics & centre self.position
        surf = pygame.Surface((100, 50))
        rotated_image = pygame.transform.rotate(image, degree)
        blitted_rect = self.window_surface.blit(surf, where)
        old_center = blitted_rect.center
        rotated_surf = pygame.transform.rotate(surf, degree)
        rot_rect = rotated_surf.get_rect()
        rot_rect.center = old_center
        return rotated_image, rot_rect, old_center

    def play(self):

        self.menu()
        
        while self.option[4] == 1:
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
                        self.option[4] = 0
                        self.menu()
                    if _event.key == K_LEFT or _event.key == ord('a'):
                        self.move_left = False
                    if _event.key == K_RIGHT or _event.key == ord('d'):
                        self.move_right = False
                    if _event.key == K_UP:
                        self.move_up = False
                    if _event.key == K_DOWN:
                        self.move_down = False

            # Get rotated graphics
            where = self.player_settings[0], self.player_settings[1]
            self.playerrotated_image, self.rot_rect, self.old_center = self.rotation(self.player_image, where, self.degree)

            # draw the track background onto the surface
            self.drawBack()

            # draw the track onto the surface
            self.move_track()

            # Check the background colour
            colour = self.window_surface.get_at(self.old_center)  # centre colour
            if colour[0] >= 88 and colour[0] <= 91 or colour[0] == 165 or colour[0] == 255:
                1;
            else:
                self.move_speed[2] = 3
                if self.move_speed[0] > 4:
                    self.car_settings[1] -= self.car_settings[3] * 2

            # draw the player onto the surface
            self.window_surface.blit(self.playerrotated_image, self.rot_rect)

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
                if self.move_speed[0] > 0:
                    self.car_settings[6] -= 1
                    if self.car_settings[6] == 0:
                        self.player_settings[2] -= 1
                        self.car_settings[6] = self.move_speed[2]
                        if self.player_settings[2] < 0:
                            self.player_settings[2] = 71

            if self.move_right:
                if self.move_speed[0] > 0:
                    self.car_settings[6] -= 1
                    if self.car_settings[6] == 0:
                        self.player_settings[2] += 1
                        self.car_settings[6] = self.move_speed[2]
                        if self.player_settings[2] > 71:
                            self.player_settings[2] = 0

            # move the player
            if self.move_down:  # Braking
                self.car_settings[1] -= self.car_settings[3]
            if self.move_up:  # Accelerate
                self.car_settings[1] += self.car_settings[2]
            else:
                self.car_settings[1] -= self.car_settings[4]
                self.move_speed[1] = self.car_settings[0]

            if self.car_settings[1] >= self.car_settings[5] and self.move_speed[0] < self.move_speed[1]:  # Change up gear
                self.move_speed[0] += 1
                self.car_settings[1] = 0
            elif self.car_settings[1] >= self.car_settings[5] and self.move_speed[0] >= self.move_speed[1]:  # Accelerate Limiter
                self.car_settings[1] = self.car_settings[5]
            elif self.car_settings[1] < 0 and self.move_speed[0] == 0:  # Braking limiter
                self.car_settings[1] = 0
                self.move_speed[0] = 0
            elif self.car_settings[1] < 0:  # Change down gears
                self.move_speed[0] -= 1
                self.car_settings[1] = self.car_settings[5]
            if self.move_speed[0] > self.move_speed[1]:
                self.car_settings[1] -= self.car_settings[3]

            # draw the window onto the screen
            self.frame_rate()
            self.getDistance(self.move_radians)
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.play()
