import json
import pyperclip
import tkinter as tk
import tkinter.messagebox
from enum import Enum
from random import choice
from typing import List, Tuple
from unidecode import unidecode
from string import ascii_letters

ENTRY_SIZE = 40
ENTRY_SPACING_X = 30
ENTRY_SPACING_Y = 40
WINDOW_X_POS = 200
WINDOW_Y_POS = 200
MARGIN_X = 30
MARGIN_Y = 30
WINDOW_WIDTH = (5 * ENTRY_SIZE) + (4 * ENTRY_SPACING_X) + (2 * MARGIN_X)
WINDOW_HEIGHT = (6 * ENTRY_SIZE) + (5 * ENTRY_SPACING_Y) + (2 * MARGIN_Y)
LABEL_WIDTH = (WINDOW_WIDTH - (2 * MARGIN_X)) / 2
LABEL_HEIGHT = 80
LABEL_SPACING_Y = 10
WINDOW_BACKGROUND_COLOR = '#453b42'
WIN_BACKGROUND = '#47ff8b'
LOSE_BACKGROUND = '#e86b6b'


class Entry(tk.Entry):
    def __init__(self, master: tk.Tk, **kwargs):
        self.text_variable = tk.StringVar()
        self.validate_command = (master.register(self.callback))
        super().__init__(master, relief=tk.FLAT, font=('Arial', '24'), justify=tk.CENTER, validate='all',
                         highlightthickness=4, highlightbackground='white', background=WINDOW_BACKGROUND_COLOR,
                         foreground='white', readonlybackground=WINDOW_BACKGROUND_COLOR, highlightcolor='lightblue',
                         validatecommand=(self.validate_command, '%P'), textvariable=self.text_variable, **kwargs)

    @classmethod
    def callback(cls, entry_content: str):
        return entry_content in ascii_letters and len(entry_content) <= 1


class Label(tk.Label):
    def __init__(self, master: tk.Tk, **kwargs):
        super().__init__(master, relief=tk.FLAT, font=('Arial', '16'), justify=tk.CENTER, **kwargs)


class Status(Enum):
    VERDE = dict(color='#2d802a', emoji='🟩')
    AMARELO = dict(color='#a68500', emoji='🟨')
    CINZA = dict(color='#616161', emoji='⬛')


class Game:
    def __init__(self, master: tk.Tk, words: List[str]):
        self.master = master
        self.master.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{WINDOW_X_POS}+{WINDOW_Y_POS}')
        self.master.title('ChutaBem!')
        self.master.configure(background=WINDOW_BACKGROUND_COLOR)
        self.master.resizable(False, False)
        self.words = words
        self.words_normalizadas = list(map(self.normalize, words))
        self.word = choice(words)
        self.word_normalizada = self.normalize(self.word)
        self.round = 0
        self.status = []

        self.entries = []
        for word_row_index in range(6):
            word_row = []
            for letter_entry_index in range(5):
                letter_entry = Entry(self.master)
                letter_entry.place(
                    x=MARGIN_X + ((ENTRY_SIZE + ENTRY_SPACING_X) * letter_entry_index),
                    y=MARGIN_Y + ((ENTRY_SIZE + ENTRY_SPACING_Y) * word_row_index),
                    width=ENTRY_SIZE,
                    height=ENTRY_SIZE
                )
                word_row.append(letter_entry)
            self.entries.append(word_row)
        print(self.word)
        self.update_entries_state()
        self.entries[0][0].focus()
        self.load_stats()

        self.master.bind('<Right>', self.move_right)
        self.master.bind('<Left>', self.move_left)
        self.master.bind('<BackSpace>', self.delete_and_move_left)
        self.master.bind('<Key>', self.auto_move_right)
        self.master.bind('<Return>', self.guess)

    @staticmethod
    def normalize(content: str):
        return unidecode(content)

    @staticmethod
    def get_entry_position(event) -> Tuple[int, int]:
        widget_name = str(event.widget)
        entry_id = None
        if '.!entry' in widget_name:
            entry_id = widget_name.replace('.!entry', '')
            entry_id = 0 if entry_id == '' else int(entry_id) - 1
            x_pos = entry_id % 5
            y_pos = entry_id // 5
            return x_pos, y_pos
        return 0, 0

    def move_right(self, event) -> None:
        x_pos, y_pos = self.get_entry_position(event)
        next_input_x_pos = x_pos + 1 if x_pos < 4 else 0
        self.entries[y_pos][next_input_x_pos].focus()

    def move_left(self, event) -> None:
        x_pos, y_pos = self.get_entry_position(event)
        next_input_x_pos = x_pos - 1 if x_pos > 0 else 4
        self.entries[y_pos][next_input_x_pos].focus()

    def auto_move_right(self, event) -> None:
        x_pos, y_pos = self.get_entry_position(event)
        next_input_x_pos = x_pos + 1 if x_pos < 4 else 4
        curr_entry_var = self.entries[y_pos][x_pos].text_variable
        curr_entry_var.set(curr_entry_var.get().upper())
        self.entries[y_pos][next_input_x_pos].focus()

    def delete_and_move_left(self, event) -> None:
        x_pos, y_pos = self.get_entry_position(event)
        entry_content = self.entries[y_pos][x_pos].get()
        if entry_content.strip() == '':
            next_input_x_pos = x_pos - 1 if x_pos > 0 else 0
            self.entries[y_pos][next_input_x_pos].focus()

    def update_entries_state(self) -> None:
        for word_row_index, word_row in enumerate(self.entries):
            if word_row_index == self.round:
                for entry in word_row:
                    entry.config(state="normal")
            else:
                for entry in word_row:
                    entry.config(state="readonly")

    @staticmethod
    def load_stats() -> dict:
        json_file = open('data.json')
        stats = json.load(json_file)
        json_file.close()
        return stats

    @staticmethod
    def save_stats(stats: dict, won_game: bool, number_of_guesses: int = None) -> None:
        stats['games_played'] += 1
        if won_game:
            stats['games_won'] += 1
            stats['curr_streak'] += 1
            stats['number_of_guesses'][str(number_of_guesses)] += 1
            if stats['curr_streak'] > stats['max_streak']:
                stats['max_streak'] = stats['curr_streak']
        else:
            stats['curr_streak'] = 0
        stats['win_percentage'] = stats['games_won'] / stats['games_played']
        json_file = open('data.json', 'w')
        json.dump(stats, json_file)
        json_file.close()

    def guess(self, event) -> None:
        word_row = self.entries[self.round]

        # Checar se a palavra foi preenchida completamente
        letras_chutadas = [entry.text_variable.get().strip().upper() for entry in word_row]
        letras_chutadas_normalizadas = list(map(self.normalize, letras_chutadas))
        if '' in letras_chutadas:
            tkinter.messagebox.showerror('ERRO', 'Digite todas as letras!')
            return

        # Checar se a palavra digitada existe
        palavra_chutada = ''.join(letras_chutadas_normalizadas)
        if palavra_chutada not in self.words_normalizadas:
            tkinter.messagebox.showerror('ERRO', 'Palavra Inválida!')
            return

        palavra_na_base = [w for w, wn in zip(self.words, self.words_normalizadas) if wn == palavra_chutada][0]

        # Checar status de cada letra
        status_letras = []
        for entry, letra_chutada_norm, letra_palavra_norm, letra_palavra_na_base in zip(
                word_row, letras_chutadas_normalizadas, self.word_normalizada, palavra_na_base):
            if letra_chutada_norm == letra_palavra_norm:
                status_letras.append(Status.VERDE)
            elif letra_chutada_norm in self.word_normalizada:
                status_letras.append(Status.AMARELO)
            else:
                status_letras.append(Status.CINZA)
            entry.text_variable.set(letra_palavra_na_base)

        # Atualizar cores e controle de status
        for status, entry in zip(status_letras, word_row):
            entry.config(readonlybackground=status.value['color'])
        self.status.append([status.value['emoji'] for status in status_letras])

        # Passar pro próximo round, ou acabar com o jogo (+ salvar stats)
        if all(status == Status.VERDE for status in status_letras):
            stats = self.load_stats()
            self.save_stats(stats, won_game=True, number_of_guesses=self.round + 1)
            self.load_final_screen(stats, won_game=True)
            return
        elif self.round == 5:
            stats = self.load_stats()
            self.save_stats(stats, won_game=False)
            self.load_final_screen(stats, won_game=False)
            return
        self.round += 1
        self.update_entries_state()
        self.entries[self.round][0].focus()

    def copy_results(self, stats: dict) -> str:
        extra_data = f'Games Played: {stats["games_played"]}\nWin Percentage: {stats["win_percentage"] * 100 :.0f}%' \
                     f'\nCurrent Streak: {stats["curr_streak"]}\nMax Streak: {stats["max_streak"]}\n\n'
        results = extra_data + '\n'.join([''.join(row) for row in self.status])
        pyperclip.copy(results)
        return results

    def load_final_screen(self, stats: dict, won_game: bool) -> None:
        self.master.unbind('<Right>')
        self.master.unbind('<Left>')
        self.master.unbind('<BackSpace>')
        self.master.unbind('<Key>')
        self.master.unbind('<Return>')
        self.master.bind('<R>', self.retry)
        self.master.bind('<r>', self.retry)

        for word_row in self.entries:
            for entry in word_row:
                entry.destroy()

        if won_game:
            self.master.title('ChutaBem! - VOCÊ GANHOU')
            new_bg = 'green'
        else:
            self.master.title('ChutaBem! - VOCÊ PERDEU')
            new_bg = 'red'
        self.master.configure(background=new_bg)

        games_played_label = Label(self.master, text=f'Games\nPlayed:\n{stats["games_played"]}', background=new_bg)
        games_played_label.place(x=MARGIN_X, y=MARGIN_Y, width=LABEL_WIDTH, height=LABEL_HEIGHT)

        win_percentage_label = Label(self.master, text=f'Win\nPercentage:\n{stats["win_percentage"] * 100 :.0f}%',
                                     background=new_bg)
        win_percentage_label.place(x=MARGIN_X + LABEL_WIDTH, y=MARGIN_Y, width=LABEL_WIDTH, height=LABEL_HEIGHT)

        curr_streak_label = Label(self.master, text=f'Current\nStreak:\n{stats["curr_streak"]}', background=new_bg)
        curr_streak_label.place(x=MARGIN_X, y=MARGIN_Y + LABEL_HEIGHT + LABEL_SPACING_Y,
                                width=LABEL_WIDTH, height=LABEL_HEIGHT)

        max_streak_label = Label(self.master, text=f'Max\nStreak:\n{stats["max_streak"]}', background=new_bg)
        max_streak_label.place(x=MARGIN_X + LABEL_WIDTH, y=MARGIN_Y + LABEL_HEIGHT + LABEL_SPACING_Y,
                               width=LABEL_WIDTH, height=LABEL_HEIGHT)

        # Stats Number Of Guesses como Gráfico
        guesses_stats_canvas = tk.Canvas(self.master, relief=tk.GROOVE, borderwidth=3)
        guesses_stats_canvas.place(x=MARGIN_X, y=MARGIN_Y + (2 * (LABEL_HEIGHT + LABEL_SPACING_Y)),
                                   width=2 * LABEL_WIDTH, height=2 * LABEL_HEIGHT)
        bar_width = (2 * LABEL_WIDTH) / 13
        margin = 20
        bar_values = [stats['number_of_guesses'][str(i)] for i in range(1, 7)]
        for (bar_index, bar), bar_x_pos in zip(enumerate(bar_values), range(1, 12, 2)):
            x0 = bar_x_pos * bar_width
            y0 = (2 * LABEL_HEIGHT) - (bar / max(bar_values)) * ((2 * LABEL_HEIGHT) - margin)
            x1 = (bar_x_pos + 1) * bar_width
            y1 = (2 * LABEL_HEIGHT)
            guesses_stats_canvas.create_rectangle(x0, y0, x1, y1, fill='orange')
            if bar > 0:
                guesses_stats_canvas.create_text(x0 + (bar_width / 2), y0 - (margin / 2), text=str(bar))
            guesses_stats_canvas.create_text(x0 + (bar_width / 2), y1 - (margin / 2), text=str(bar_index + 1))

        # Botão de copiar
        copiar_button = tk.Button(self.master, command=lambda: self.copy_results(stats),
                                  text='Copiar\nResultados', font=('Arial', '10'))
        copiar_button.place(x=MARGIN_X, y=MARGIN_Y + (2 * (LABEL_HEIGHT + LABEL_SPACING_Y)) + (2 * LABEL_HEIGHT) + LABEL_SPACING_Y,
                            width=LABEL_WIDTH * 2, height=ENTRY_SIZE)

        # Palavra correta
        for letter_entry_index in range(5):
            letter_entry = Entry(self.master, state='readonly')
            letter_entry.place(
                x=MARGIN_X + ((ENTRY_SIZE + ENTRY_SPACING_X) * letter_entry_index),
                y=MARGIN_Y + (2 * (LABEL_HEIGHT + LABEL_SPACING_Y)) + (2 * LABEL_HEIGHT) + (2 * LABEL_SPACING_Y) + ENTRY_SIZE,
                width=ENTRY_SIZE,
                height=ENTRY_SIZE
            )
            letter_entry.text_variable.set(self.word[letter_entry_index].upper())

    def retry(self, _):
        self.master.destroy()
        play_game(self.words)


def play_game(words: List[str]):
    my_window = tk.Tk()
    my_game = Game(my_window, words)
    my_window.mainloop()


if __name__ == '__main__':
    words_file = open('words.txt', 'r', encoding='utf-8')
    my_words = list(map(lambda x: x.replace('\n', '').upper(), words_file.readlines()))
    words_file.close()
    play_game(my_words)

