import pygame
import math


class Player:
    def __init__(self, game):
        self.game = game

        self.image_file = pygame.image.load(
            self.game.data / "sprites/player.png"
        ).convert()

        self.image_file.set_colorkey((0, 0, 0))
        self.rect = self.image_file.get_rect()

        self.angle = 0
        self.distance = min(self.game.window.RENDER_SIZE) / 6
        self.speed = 0.15

        self.center = (game.window.RENDER_SIZE[0] / 2, game.window.RENDER_SIZE[1] / 2)

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, val):
        degrees = 90 + val * 180 / math.pi
        self.image = pygame.transform.rotate(self.image_file, -degrees)
        self._angle = val

    def check_collision(self, angle):
        for segment in self.game.obstacles.obstacle_segments:
            if segment.distance - segment.width < self.distance < segment.distance:
                if (
                    segment.angle % 2 * math.pi
                    < self.angle % 2 * math.pi
                    < segment.angle % 2 * math.pi + math.pi / 3
                ):
                    return True

    def update(self, dt):
        if self.game.input.moving_left:
            self.angle -= self.speed
        elif self.game.input.moving_right:
            self.angle += self.speed

        self.angle += self.game.spin

        x = self.center[0] + self.distance * math.cos(self.angle)
        y = self.center[1] + self.distance * math.sin(self.angle)
        self.rect.center = (x, y)

    def render(self):
        self.game.window.screen.blit(self.image, self.rect)