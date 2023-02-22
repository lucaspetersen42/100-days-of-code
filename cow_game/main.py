import pygame
import random
import time
from abc import ABC, abstractmethod

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# ToDo: Conseguir clicar na vaquina com o Mouse e mudar a posição dela
# ToDo: Criar função pra unir vaquinhas


class Game:
    def __init__(self):
        pygame.init()
        self.minute_event = 0
        self.screen_width = 500
        self.screen_height = 500
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), 0, 32)
        pygame.display.set_caption('Jogo da Vaquinha')
        self.clock = pygame.time.Clock()
        self.running = True
        self.coins = 0
        self.cows = []
        self.fps = 30
        while self.running:
            self.run()

    def update_objects(self):
        if self.minute_event % (10 * self.fps) == 0:
            for cow in self.cows:
                self.coins += cow.generate_coin()

        if self.minute_event % self.fps == 0:
            for cow in self.cows:
                cow.update()

    def draw_objects(self):
        for cow in self.cows:
            cow_obj = pygame.Rect(cow.pos_x - 40, cow.pos_y - 40, 40, 40)
            pygame.draw.rect(self.screen, WHITE, cow_obj)

    def run(self):
        self.clock.tick(self.fps)
        self.minute_event += 1
        if self.minute_event % (10 * self.fps) == 0:
            print(self.coins)
            self.minute_event = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.create_cow()
        self.update_objects()
        self.screen.fill(BLACK)
        self.draw_objects()
        pygame.display.flip()

    def create_cow(self):
        r_x, r_y = random.randint(0, self.screen_width), random.randint(0, self.screen_height)
        new_cow = BabyCow(r_x, r_y, self.screen_width, self.screen_height)
        self.cows.append(new_cow)


class Cow(ABC):
    def __init__(self, x, y, screen_width, screen_height):
        self.pos_x = x
        self.pos_y = y
        self.step = 1
        self.screen_width = screen_width
        self.screen_height = screen_height

    def move(self):
        """Mover vaca randomicamente."""
        self.pos_x += random.randint(-self.step, self.step)
        self.pos_y += random.randint(-self.step, self.step)
        if self.pos_x >= self.screen_width:
            self.pos_x -= 1
        elif self.pos_x <= 0:
            self.pos_x += 1
        if self.pos_y >= self.screen_height:
            self.pos_y -= 1
        elif self.pos_y <= 0:
            self.pos_y += 1

    def update(self):
        """Atualizar estado da vaca."""
        self.move()

    @abstractmethod
    def generate_coin(self):
        """Gerar Moedas."""


class BabyCow(Cow):
    def __init__(self, x, y, screen_width, screen_height):
        self.coin_value = 1
        super().__init__(x, y, screen_width, screen_height)

    def generate_coin(self):
        return self.coin_value


class AdultCow(Cow):
    def __init__(self, x, y, screen_width, screen_height):
        self.coin_value = 10
        super().__init__(x, y, screen_width, screen_height)

    def generate_coin(self):
        return self.coin_value


class BigAdultCow(Cow):
    def __init__(self, x, y, screen_width, screen_height):
        self.coin_value = 50
        self.max_coin_value = 100
        self.max_coin_chance = .1
        super().__init__(x, y, screen_width, screen_height)

    def generate_coin(self):
        r = random.randint(0, 100)
        coin = self.coin_value if r/100 > self.max_coin_chance else self.max_coin_value


if __name__ == '__main__':
    game = Game()
