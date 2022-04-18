import pygame
import random
import numpy as np


class ColourChanger:
    def __init__(self, game):
        self.game = game
        self.colours = (
            (255, 61, 61),  # red
            (255, 164, 61),  # orange
            (145, 255, 61),  # green
            (61, 255, 187),  # blue
            (255, 61, 239),  # violet
        )
        self.current_background = [random.choice(self.colours)]

    @property
    def bgcolour(self):
        return tuple(self.current_background[0])

    @property
    def bgcolour2(self):
        return tuple(np.asarray(self.current_background[0]) * 0.9)

    def change_colour(self):
        new_background = random.choice([c for c in self.colours if c != self.bgcolour])
        self.current_background = np.linspace(
            self.bgcolour, new_background, int(self.game.FRAME_RATE * 0.2)
        )

    def update(self):
        if len(self.current_background) > 1:
            self.current_background = np.delete(self.current_background, 0, axis=0)

    def render(self):
        self.game.window.screen.fill(self.bgcolour)
        self.game.window.final_display.fill(self.bgcolour)