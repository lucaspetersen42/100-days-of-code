import numpy as np
import tkinter as tk
import matplotlib
import matplotlib.cm as cm
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

matplotlib.use('TkAgg')


class Plotter:
    def __init__(self, array: np.array, cmap: str = 'gray'):
        self.arr = array
        self.cmap = cmap
        self.window = tk.Tk()
        self.window.geometry('800x650')
        self.window.title('Slicer and Plotter')
        self.window.resizable(False, False)
        self.window.configure(background='white')
        self.fig = Figure(figsize=(8, 6.5), dpi=100)
        self.canvas = None
        self.slider = tk.Scale(self.window, from_=0, to=len(array)-1, orient=tk.HORIZONTAL, command=self.update_slice,
                               length=300, background='white', highlightthickness=0, showvalue=False, resolution=.1,
                               troughcolor='#c4dcff')
        self.slider.pack()
        self.update_slice(None)
        self.window.mainloop()

    def plot(self, _slice: np.array):
        self.clear_plot()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        if not self.canvas:
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.window)
            self.canvas.get_tk_widget().pack(side="bottom", fill="both", expand=True)
        self.canvas.draw_idle()
        # nipy_spectral // BuPu
        ax.imshow(_slice, cmap=self.cmap, interpolation='nearest')

    def clear_plot(self):
        self.fig.clear()
        if self.canvas:
            self.canvas.draw_idle()

    def update_slice(self, event):
        slider_val = float(self.slider.get())
        index = int(round(slider_val, 0))
        _slice = self.arr[index]
        average_color = np.mean(_slice, axis=(0, 1))
        cmap_average = eval(f'cm.{self.cmap}(average_color)')
        to_int = lambda val: int(round(val * 255, 0))
        cmap_average_rgb = tuple(map(to_int, cmap_average[:3]))
        cmap_average_hex = '#%02x%02x%02x' % cmap_average_rgb
        self.slider.config(troughcolor=cmap_average_hex)
        self.plot(_slice=_slice)


if __name__ == '__main__':
    my_arr = np.load('perlin.npy')
    # my_arr = np.load(r"C:\Users\Lucas Petersen\Documents\image_as_array.npy")
    # my_arr = np.rot90(my_arr)
    # my_arr = np.invert(my_arr)
    my_arr = np.swapaxes(my_arr, 0, 2)
    program = Plotter(my_arr, 'nipy_spectral')
