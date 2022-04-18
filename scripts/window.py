import pygame


class Window:

    WINDOW_SIZE = 960, 720
    RENDER_SIZE = 960 * 0.6, 720 * 0.6

    def __init__(self, game):
        self.game = game
        self.blit_size = [0, 0]
        self.blit_offset = [0, 0]

        self.final_display = pygame.display.set_mode(self.WINDOW_SIZE)
        self.screen = pygame.Surface(self.RENDER_SIZE).convert()
        pygame.display.set_caption("Super Hexagon")

    def update(self):
        self.blit_size[0] = int(self.WINDOW_SIZE[0] * (1 + self.game.audio.zoom / 100))
        self.blit_size[1] = int(self.WINDOW_SIZE[1] * (1 + self.game.audio.zoom / 100))
        self.blit_offset[0] = self.WINDOW_SIZE[0] / 2 - self.blit_size[0] / 2
        self.blit_offset[1] = self.WINDOW_SIZE[1] / 2 - self.blit_size[1] / 2

    def render(self):
        scaled = pygame.transform.scale(self.screen, self.blit_size)
        self.final_display.blit(scaled, self.blit_offset)
        pygame.display.update()