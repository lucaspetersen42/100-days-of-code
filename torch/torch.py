import sys
import pygame
from pygame.locals import QUIT, K_SPACE, KEYDOWN, BLEND_RGB_ADD
from random import randint
from typing import Tuple

BLACK = (0, 0, 0)
RED = (207, 68, 68)
ORANGE = (222, 128, 20)
MUSTARD = (168, 140, 13)
YELLOW = (168, 155, 13)
LIME = (155, 168, 13)
GREEN = (44, 125, 40)
TEAL = (82, 199, 160)
BLUE = (90, 155, 230)
PURPLE = (118, 90, 153)
PINK = (143, 95, 207)
LIGHT_PINK = (212, 123, 181)
SALMON = (212, 123, 136)


class Torch:
    def __init__(self, min_size: int = 30, max_size: int = 50, wobbliness: int = 10, fiestness: float = 1,
                 base_color: Tuple[int, int, int] = ORANGE, lastness: float = 55):
        self.min_size = min_size
        self.max_size = max_size if max_size > min_size else min_size
        self.wobbliness = wobbliness
        self.fiestness = fiestness
        self.base_color = base_color
        self.lastness = lastness

        self.orig_min_size = self.min_size
        self.orig_max_size = self.max_size
        self.orig_wobbliness = self.wobbliness
        self.orig_lastness = self.lastness
        self.flame_time = 0

        self.clock = pygame.time.Clock()
        pygame.init()
        pygame.display.set_caption('Torch')

        self.window_width = 800
        self.window_height = 650
        self.spotlight_coords = [0, 0]
        self.screen = pygame.display.set_mode((self.window_width, self.window_height), 0, 32)

        self.particles = []
        self.colors = [ORANGE, MUSTARD, YELLOW, LIME, GREEN, TEAL, BLUE, PURPLE, PINK, LIGHT_PINK, SALMON, RED]
        if self.base_color not in self.colors:
            self.base_color = ORANGE
        self.base_color_index = [i for i, val in enumerate(self.colors) if val == self.base_color][0]

        self.running = True
        while self.running:
            self.run()
            self.update()
            self.check_for_events()
        pygame.quit()
        sys.exit()

    def run(self):
        self.screen.fill(BLACK)
        self.spotlight_coords = list(map(lambda x: x + (randint(-self.wobbliness * 100, self.wobbliness * 100) / 100), pygame.mouse.get_pos()))
        new_particle = [self.spotlight_coords, [randint(0, 20) / 10 - 1, -5], randint(self.min_size, self.max_size)]
        self.particles.append(new_particle)

        for particle in self.particles:
            particle[0][0] += particle[1][0]
            particle[0][1] += particle[1][1]
            particle[2] -= 1
            particle[1][1] += 1 / self.lastness
            rect = pygame.Rect(int(particle[0][0]) - int(particle[2] / 2), int(particle[0][1]) - int(particle[2] / 2), int(particle[2]), int(particle[2]))
            pygame.draw.rect(self.screen, self.base_color, rect)
            size = particle[2] * 2
            get_shadow = lambda x, y, z: (x * 0.2, y * 0.2, z * 0.2)
            self.screen.blit(self.rect_surface(size, get_shadow(*self.base_color)), (int(particle[0][0] - size), int(particle[0][1] - size)), special_flags=BLEND_RGB_ADD)
            if particle[2] <= 0:
                self.particles.remove(particle)

    @classmethod
    def rect_surface(cls, size, _color):
        size = int(round(size, 0))
        surface = pygame.Surface((size * 2, size * 2))
        pygame.draw.rect(surface, _color, pygame.Rect(size // 2, size // 2, size, size))
        surface.set_colorkey(BLACK)
        return surface

    def update(self):
        pygame.display.update()
        self.clock.tick(60 * self.fiestness)
        if self.flame_time != 0:
            self.flame_time -= 1
            if self.flame_time == 0:
                self.min_size = self.orig_min_size
                self.max_size = self.orig_max_size
                self.wobbliness = self.orig_wobbliness
                self.lastness = self.orig_lastness
        self.base_color = self.colors[self.base_color_index % len(self.colors)]

    def check_for_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    self.base_color_index += 1
                if event.key == pygame.K_DOWN:
                    if self.min_size > 2:
                        self.min_size -= 1
                        self.max_size -= 1
                        self.orig_min_size -= 1
                        self.orig_max_size -= 1
                if event.key == pygame.K_UP:
                    if self.max_size <= max(self.window_width, self.window_height) / 10:
                        self.min_size += 1
                        self.max_size += 1
                        self.orig_min_size += 1
                        self.orig_max_size += 1
            if pygame.mouse.get_pressed()[0]:
                if self.flame_time == 0:
                    self.flame_time = 12
                    self.min_size *= 2
                    self.max_size *= 2
                    self.wobbliness *= 5
                    self.lastness *= 4



if __name__ == '__main__':
    torch = Torch()
