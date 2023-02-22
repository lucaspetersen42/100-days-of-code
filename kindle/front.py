"""
GUI para:
- Ver livros no Kindle
- Ver progresso em cada livro
- Gerenciar (Enviar novos livros, alterar informações, apagar livros, etc)
"""

import tkinter as tk

TITLE = 'Gerenciador de Kindle'
W, H = 500, 500
X, Y = 0, 0

window = tk.Tk()
window.title(TITLE)
window.geometry(f'{W}x{H}+{X}+{Y}')
window.resizable(False, False)
window.configure(background='red')

# Code Here

window.mainloop()
