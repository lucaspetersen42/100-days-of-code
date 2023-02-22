import numpy as np
from scipy.optimize import fsolve


def h(phi):
    return np.log(abs(float(1 / (np.cos(phi))) + float(np.tan(phi))))


def project(phi, theta):
    """phi [latitude], theta [longitude] => theta [x], h(phi) [y]"""
    return theta, h(phi)


def remap(inp1, inp2, out1, out2, val_in):
    return (val_in - inp1) / (inp2 - inp1) * (out2 - out1) + out1


def rgb2hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)


def createColors(inicial, final, n):
        ri, gi, bi = ImageColor.getcolor(inicial, 'RGB')
        rf, gf, bf = ImageColor.getcolor(final, 'RGB')
        reds = np.linspace(ri, rf, n)
        greens = np.linspace(gi, gf, n)
        blues = np.linspace(bi, bf, n)

        color = []

        for i, c in enumerate(reds):
            c = rgb2hex(int(round(reds[i].tolist(), 0)), int(round(greens[i].tolist(), 0)),
                        int(round(blues[i].tolist(), 0)))
            color.append(c)

        return color


def create_map(image: str):
    d_lat = 0
    d_long = np.pi
    im = Image.open(r"C:\Users\Lucas Petersen\Desktop\world.jpg").resize((W, H), Image.ANTIALIAS)
    rgb_im = im.convert('RGB')
    lats = np.linspace(- K * np.pi / 2, K * np.pi / 2, N)
    longs = np.linspace(- K * np.pi / 2, K * np.pi / 2, M)
    for lat in lats:
        lat += d_lat
        if d_lat > np.pi:
            d_lat = 2 * np.pi - d_lat
        for long in longs:
            long += d_long
            if d_long > np.pi:
                d_long = 2 * np.pi - d_lat
            x, y = project(lat, long)
            x = remap(min(longs), max(longs), 0, W, x)
            y = remap(min(lats), max(lats), 0, H, y)
            int_x = int(round(x, 0))
            int_y = int(round(y, 0))
            try:
                map_color_as_rgb = rgb_im.getpixel((int_x, int_y))
            except IndexError as e:
                map_color_as_rgb = (255, 0, 0)
            map_color = rgb2hex(*map_color_as_rgb)
            canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill=map_color, width=0)


def create_colormap(equator_color: str, pole_color: str):
    colors = createColors(equator_color, pole_color, N // 2)
    colors_reverse = colors[::-1]
    colors_ = colors_reverse
    colors_.extend(colors)
    colors = colors_
    lats = np.linspace(- K * np.pi / 2, K * np.pi / 2, N)
    longs = np.linspace(- K * np.pi / 2, K * np.pi / 2, M)
    for lat, color in zip(lats, colors):
        for long in longs:
            x, y = project(lat, long)
            x = remap(min(longs), max(longs), 0, W, x)
            y = remap(min(lats), max(lats), 0, H, y)
            canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill=color, width=0)



if __name__ == '__main__':
    import tkinter as tk
    from PIL import ImageColor, Image
    W, H = 700, 500
    K = 0.999  # com 1 > K > 0
    N = 150
    M = 150

    def trigger_create_colormap(event):
        return create_colormap(equator_color='#eb8f4d', pole_color='#4debb9')


    def trigger_create_map(event):
        return create_map(r"C:\Users\Lucas Petersen\Desktop\world.jpg")

    window = tk.Tk()
    window.title('Mapa Mundi')
    window.geometry(f'{W}x{H}')
    canvas = tk.Canvas(window, background='black')
    canvas.place(x=0, y=0, width=W, height=H)
    window.bind('<space>', trigger_create_colormap)
    window.bind('<c>', trigger_create_map)
    window.mainloop()

