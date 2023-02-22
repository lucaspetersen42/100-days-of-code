import os
import pygame
from typing import List
from random import randint
from math import tau, floor, sqrt

W = 1080
H = 720
TAU = 360  # tau
BLACK = (0, 0, 0)
SPRITE_IMAGE = os.path.join(os.path.dirname(__file__), 'sprite.png')
SPRITE_SIZE = 20
TICK = 30


class Member(pygame.sprite.Sprite):
    def __init__(self, angle_precision: int):
        self.image = pygame.transform.scale(pygame.image.load(SPRITE_IMAGE), (SPRITE_SIZE, SPRITE_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = randint(0, W)
        self.rect.y = randint(0, H)
        self.angle_precision: int = angle_precision
        self.angle: float = randint(0, floor(TAU * angle_precision)) / angle_precision
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.speed: float = 0
        self.acceleration: float = 0
        super().__init__()

    def __str__(self):
        return f'Member at ({self.rect.x}, {self.rect.y})'

    def steer(self, center_x, center_y):
        """Docstring Here."""
        dx = 1 if (center_x - self.rect.x) > 0 else -1
        dy = 1 if (center_y - self.rect.y) > 0 else -1
        brownian_x, brownian_y, brownian_angle = 0, 0, randint(-5, 5)
        self.rect.x += dx + brownian_x
        self.rect.y += dy + brownian_y
        self.image = pygame.transform.rotate(self.image, brownian_angle)

    def align(self):
        """Docstring Here."""
        pass

    def cohere(self):
        """Docstring Here."""
        pass


class Boid:
    def __init__(self, number_of_members: int = 10, angle_of_precision: int = 10, flockmates_radius: float = 60.0):
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((W, H), 0, 32)
        pygame.display.set_caption('Boids')

        self.members = pygame.sprite.Group()
        for member in range(number_of_members):
            self.members.add(Member(angle_of_precision))

        self.flockmates_radius = flockmates_radius
        self.running = True
        while self.running:
            self.recalculate_members()

    def __len__(self):
        return len(self.members)

    def recalculate_members(self):
        """Recalculate every member's route and position."""
        for member in self.members:
            member.steer(*self.get_baricenter(member))
        self.screen.fill((255))
        self.members.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(TICK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        # Separation - Steer to avoid crowding local flockmates
        # Alignment - Steer towards the average heading of local flockmates
        # Cohesion - Steer to move towards the baricenter of local flockmates
        pass

    @staticmethod
    def mean(flockmates: List[Member], axis: int) -> float:
        if axis == 0:
            return sum(m.rect.x for m in flockmates) / len(flockmates)
        elif axis == 1:
            return sum(m.rect.y for m in flockmates) / len(flockmates)
        else:
            raise ValueError('Axis must be 0 or 1.')

    @staticmethod
    def distance(member_a: Member, member_b: Member):
        return sqrt((member_a.rect.x - member_b.rect.x) ** 2 + (member_a.rect.y - member_b.rect.y) ** 2)

    def get_baricenter(self, member: Member) -> tuple:
        """Calculate the baricenter (center of mass) of the nearby flock."""
        flockmates = [m for m in self.members if self.distance(m, member) <= self.flockmates_radius]
        center_x = self.mean(flockmates, axis=0)
        center_y = self.mean(flockmates, axis=1)
        return center_x, center_y

    def get_local_flockmates(self, member: Member):
        """Search for flockmates nearby."""
        pass  # Use flockmates_radius


if __name__ == '__main__':
    pygame.init()
    my_boid = Boid(number_of_members=100)
