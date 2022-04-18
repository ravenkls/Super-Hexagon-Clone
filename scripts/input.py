import sys

import pygame
from pygame.locals import *


class InputManager:
    def __init__(self):
        self.moving_left = False
        self.moving_right = False

    def process_inputs(self):
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_a or event.key == K_LEFT:
                    self.moving_left = True
                elif event.key == K_d or event.key == K_RIGHT:
                    self.moving_right = True
            elif event.type == KEYUP:
                if event.key == K_a or event.key == K_LEFT:
                    self.moving_left = False
                elif event.key == K_d or event.key == K_RIGHT:
                    self.moving_right = False