import tkinter as tk


class App:
    BALLOON_WIDTH = 95
    BALLOON_HEIGHT = 30

    def __init__(self, master: tk.Tk, rounds: int = 5):
        self.WIDTH = (3 * self.BALLOON_WIDTH * (rounds - 1)) + self.BALLOON_WIDTH
        self.HEIGHT = (((2 ** rounds) * self.BALLOON_HEIGHT) + (((2 ** rounds) - 1) * (self.BALLOON_HEIGHT // 2))) // 2
        print(f'{self.WIDTH}x{self.HEIGHT}')

        self.master = master
        self.master.title('Which One?')
        self.master.geometry(f'{self.WIDTH}x{self.HEIGHT}')
        self.master.resizable(False, False)

        self.rounds = rounds
        self._options = ()
        self.history = []

        self.canvas = tk.Canvas(self.master, background='white')
        self.canvas.place(x=0, y=0, width=self.WIDTH, height=self.HEIGHT)
        self.generate_options()

    @property
    def options(self):
        return self._options

    def generate_grid(self):
        return

    def generate_options(self):
        colors = ['red', 'orange', 'yellow', 'green', 'blue']
        dy = .25
        rate = 1.5

        for i in range(self.rounds - 1):
            exp = self.rounds - 1 - i
            x0 = 1.5 * i * self.BALLOON_WIDTH
            x1 = x0 + self.BALLOON_WIDTH
            color = colors[exp - 1]

            x0b = self.WIDTH - x0
            x1b = self.WIDTH - x1

            for j in range(2 ** exp):
                y0 = (j * rate * self.BALLOON_HEIGHT) + (dy * self.BALLOON_HEIGHT)
                y1 = y0 + self.BALLOON_HEIGHT
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color)
                self.canvas.create_rectangle(x0b, y0, x1b, y1, fill=color)

            dy = (dy * 2) + .5
            rate *= 2

        xc0 = (self.WIDTH - self.BALLOON_WIDTH) / 2
        yc0 = (self.HEIGHT - self.BALLOON_HEIGHT) / 2
        xc1 = xc0 + self.BALLOON_WIDTH
        yc1 = yc0 + self.BALLOON_HEIGHT
        self.canvas.create_rectangle(xc0, yc0, xc1, yc1, fill='purple')

if __name__ == '__main__':
    window = tk.Tk()
    app = App(window)
    window.mainloop()
