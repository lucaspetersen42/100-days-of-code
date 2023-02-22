from typing import List

WIDTH = 40
HEIGHT = 30
BACKGROUND = [['X' for x in range(WIDTH)] for y in range(HEIGHT)]


class Snake:
    def __init__(self):
        self.body: List[BodyPart] = []
        self.growing = False

    def update(self):
        self.move()
        if self.growing:
            self.grow()
        background = BACKGROUND
        for body_part in self.body:
            background[body_part.y][body_part.x] = '0'
        print(background)

    def move(self):
        # Copiar o movimento do item anterior em loop
        for body_index in range(len(self.body) - 1):
            self.body[body_index + 1].x = self.body[body_index].x
            self.body[body_index + 1].y = self.body[body_index].y

        # Atualizar movimento da cabeça se necessário
        pass
        return

    def grow(self):
        self.body.append(BodyPart(x=0, y=0))  # TODO


class BodyPart:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


def init():
    return

if __name__ == '__main__':
    init()
