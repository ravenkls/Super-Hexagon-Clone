import sys
from pathlib import Path

import pygame
from pygame.locals import *
import numpy as np
import random

from scripts.audio import Audio
from scripts.input import InputManager
from scripts.hexagon import HexagonManager
from scripts.player import Player
from scripts.audio import SongAnalysis
from scripts.colour import ColourChanger
from scripts.window import Window


class SuperHexagon:

    FRAME_RATE = 60

    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.init()

        self.clock = pygame.time.Clock()

        self.frame_count = 0

        self.data = Path("data")

        self.spin = 0.02

        self.window = Window(self)
        self.input = InputManager()
        self.audio = Audio(self)
        self.colour = ColourChanger(self)
        self.player = Player(self)
        self.obstacles = HexagonManager(self)

    def mainloop(self):
        self.audio.set_song("heart")
        self.audio.bass_threshold = 14
        self.audio.play()

        while True:
            self.colour.update()
            self.colour.render()

            self.audio.update()

            self.input.process_inputs()

            self.obstacles.update(self.frame_count)
            self.obstacles.render()

            self.player.update(self.frame_count)
            self.player.render()

            self.window.update()
            self.window.render()

            self.clock.tick(self.FRAME_RATE)
            self.frame_count += 1


if __name__ == "__main__":
    game = SuperHexagon()
    game.mainloop()
