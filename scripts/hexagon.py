import random

import numpy as np
import pygame

from itertools import chain


class HexagonManager:
    def __init__(self, game):
        self.segments = []
        self.game = game

        self.background_segments = []
        self.player_segments = []
        self.obstacle_segments = []
        self.vfx_segments = []

        self.speed = 8
        self.spin_offset = 0

        for i in range(3):
            self.background_segments.append(
                Segment(
                    self,
                    distance=max(self.game.window.RENDER_SIZE) / np.sin(np.pi / 3) / 2
                    + self.game.player.distance,
                    width=max(self.game.window.RENDER_SIZE) / np.sin(np.pi / 3) / 2,
                    angle=i * 2 * np.pi / 3,
                    colour=self.game.colour.bgcolour2,
                ),
            )

        for i in range(6):
            self.player_segments.extend(
                (
                    Segment(
                        self,
                        distance=self.game.player.distance - 25,
                        width=5,
                        angle=i * np.pi / 3,
                    ),
                    Segment(
                        self,
                        distance=self.game.player.distance - 30,
                        width=self.game.player.distance - 30,
                        angle=i * np.pi / 3,
                        colour=self.game.colour.bgcolour,
                    ),
                )
            )

    def spawn_hexagon(self):
        gaps_count = random.randint(1, 4)
        gaps = random.sample(range(6), gaps_count)
        for i in range(6):
            if i not in gaps:
                self.obstacle_segments.append(
                    Segment(
                        self,
                        width=min(self.game.window.RENDER_SIZE) / 15,
                        angle=i * np.pi / 3 + self.spin_offset,
                    ),
                )

    def spawn_vfx_hexagon(self):
        for i in range(6):
            self.vfx_segments.append(
                SegmentVFX(
                    self,
                    distance=(self.game.player.distance - 10) / 4,
                    width=self.game.player.distance / 4,
                    angle=i * np.pi / 3 + self.spin_offset,
                    decay_rate=0.05,
                    speed=5,
                ),
            )

    def update(self, dt):
        self.spin_offset += self.game.spin

        for segment in reversed(self.obstacle_segments):
            segment.distance -= self.speed
            segment.angle += self.game.spin

            if segment.distance <= 0:
                self.obstacle_segments.remove(segment)

        for segment in self.background_segments:
            segment.colour = self.game.colour.bgcolour2
            segment.angle += self.game.spin

        for segment in reversed(self.vfx_segments):
            segment.angle += self.game.spin
            segment.distance += segment.speed

            if segment.decay == 0:
                self.vfx_segments.remove(segment)

        for segment in self.player_segments:
            if segment.colour != (255, 255, 255):
                segment.colour = self.game.colour.bgcolour
            segment.angle += self.game.spin

        if dt % 45 == 0:
            self.spawn_hexagon()

    def render(self):
        for segment in chain(
            self.background_segments,
            self.obstacle_segments,
            self.vfx_segments,
            self.player_segments,
        ):
            segment.update()
            segment.render()


class Segment:
    def __init__(self, manager, distance=None, width=70, angle=0, colour=None):
        self.manager = manager

        self.colour = colour
        self.colour_key = (0, 0, 0)
        self.distance = distance

        self.max_distance = (
            (max(self.manager.game.window.RENDER_SIZE) / 2)
            / np.sin(np.pi / 3)
            / np.sin(np.pi / 3)
        ) + width * 2

        if self.distance is None:
            self.distance = self.max_distance
        if self.colour is None:
            self.colour = (255, 255, 255)
        elif self.colour == (0, 0, 0):
            self.colour_key = (255, 255, 255)

        self.width = width
        self.diagonal_width = self.width / np.sin(np.pi / 3)

        self.pixel_width = 2 * self.max_distance * np.cos(np.pi / 3)
        self.pixel_height = width

        self.segment_width = self.pixel_width

        self.image = pygame.Surface(
            (self.pixel_width, self.pixel_height), pygame.SRCALPHA
        ).convert_alpha()
        self.rect = self.image.get_rect()
        self.x_offset = self.manager.game.window.RENDER_SIZE[0] / 2
        self.y_offset = self.manager.game.window.RENDER_SIZE[1] / 2
        self.angle = angle

    def update(self):
        direct_distance = self.distance * np.sin(np.pi / 3) - self.width / 2
        x = self.x_offset + direct_distance * np.cos(self.angle)
        y = self.y_offset + direct_distance * np.sin(self.angle)
        self.center = (x, y)
        self.segment_width = 2 * self.distance * np.cos(np.pi / 3)

    def render(self):
        edge_offset = (self.pixel_width - self.segment_width) / 2

        self.image.fill((255, 255, 255, 0))

        pygame.draw.polygon(
            self.image,
            self.colour,
            [
                (edge_offset + 1, 0),
                (self.pixel_width - edge_offset, 0),
                (
                    self.pixel_width
                    - self.diagonal_width * np.cos(np.pi / 3)
                    - edge_offset,
                    self.pixel_height,
                ),
                (
                    self.diagonal_width * np.cos(np.pi / 3) + edge_offset + 1,
                    self.pixel_height,
                ),
            ],
        )

        pygame.draw.aaline(
            self.image,
            self.colour,
            (edge_offset + 1, 0),
            (self.pixel_width - edge_offset, 0),
        )

        pygame.draw.aaline(
            self.image,
            self.colour,
            (
                self.pixel_width
                - self.diagonal_width * np.cos(np.pi / 3)
                - edge_offset,
                self.pixel_height,
            ),
            (
                self.diagonal_width * np.cos(np.pi / 3) + edge_offset + 1,
                self.pixel_height,
            ),
        )

        degrees = self.angle * 180 / np.pi
        self.image_final = pygame.transform.rotate(self.image, -degrees - 90)
        self.manager.game.window.screen.blit(
            self.image_final, self.image_final.get_rect(center=self.center)
        )


class SegmentVFX(Segment):
    def __init__(
        self,
        *args,
        decay_rate,
        speed,
        **kwargs,
    ):

        super().__init__(*args, **kwargs)

        self.decay = 1
        self.decay_rate = decay_rate
        self.speed = speed
        self.original_width = self.pixel_height

        if len(self.colour) == 3:
            self.colour = [*self.colour, 255]
        else:
            self.colour[3] = 255

    def update(self):
        super().update()
        self.decay = max(0, self.decay - self.decay_rate)
        self.speed -= self.decay_rate
        self.colour[3] = 255 * self.decay
        self.pixel_height = self.original_width * self.decay
        self.diagonal_width = self.pixel_height / np.sin(np.pi / 3)
