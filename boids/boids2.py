from __future__ import annotations

import os
import curses
import time
import random
from math import tau, ceil, sin, cos, atan
from numpy import mean
from typing import List, Tuple

CARACTERES_PEIXE = [' ↑ ', ' ↗ ', ' → ', ' ↘ ', ' ↓ ', ' ↙ ', ' ← ', ' ↖ ']
GRID_VAZIO = '   '
LARGURA_TELA = 40
ALTURA_TELA = 38
FPS = 30
DISTANCE_CONSTANT = 4 * sin(tau / 8)


class Peixe:
    def __init__(self):
        order = False
        if order:
            self.x: float = LARGURA_TELA / 2  # random.uniform(0, LARGURA_TELA)
            self.y: float = ALTURA_TELA / 2  # random.uniform(0, ALTURA_TELA)
        else:
            self.x: float = random.uniform(0, LARGURA_TELA)
            self.y: float = random.uniform(0, ALTURA_TELA)
        self.velocidade: float = random.uniform(0.0015, 0.008)
        self.aceleracao: float = 0
        self.angulo: float = random.uniform(0, tau)

    def atualizar(self) -> None:
        """Atualizar os atributos do Peixe."""

        self.x += cos(self.angulo - tau / 4) * self.velocidade
        self.y += sin(self.angulo - tau / 4) * self.velocidade

        # O que fazer se o peixe sair do grid?
        if self.x > LARGURA_TELA:
            self.x = 0
        elif self.x < 0:
            self.x = LARGURA_TELA
        if self.y > ALTURA_TELA:
            self.y = 0
        elif self.y < 0:
            self.y = ALTURA_TELA

        self.velocidade += self.aceleracao


    def separar(self) -> None:
        """Afastar dos peixes da vizinhança, para não ocupar o mesmo lugar que todos (o exato baricentro)."""
        return

    def alinhar(self, peixes_proximos: List[Peixe]) -> None:
        """Girar na média do sentido dos peixes da vizinhança."""

        # Achar valores médios de ângulo e velocidade
        angulo_med = mean([peixe.angulo for peixe in peixes_proximos])
        velocidade_med = mean([peixe.velocidade for peixe in peixes_proximos])

        # Transformar vetor angulo * velocidade de v.u para <x;y>
        vetor_x, vetor_y = cos(self.angulo) * self.velocidade, sin(self.angulo) * self.velocidade
        vetor_med_x, vetor_med_y = cos(angulo_med) * velocidade_med, sin(angulo_med) * velocidade_med

        # Subtrair vetores
        diff_x = abs(vetor_x - vetor_med_x)
        diff_y = abs(vetor_y - vetor_med_y)

        # Transformar vetor <x;y> para v.u
        if diff_x == 0:
            diff_x = 0.001
        diff_angulo = atan(diff_y / diff_x)
        diff_velocidade = cos(diff_angulo) / diff_x

        # Assign
        self.angulo = diff_angulo
        self.velocidade = diff_velocidade

    def reunir(self) -> None:
        """Se aproximar do baricentro dos peixes na vizinhança."""
        return

    def definir_char(self):
        """Determinar qual o caracter certo pra representar o Peixe, a partir do ângulo do mesmo."""

        index = int(ceil(8 * self.angulo / tau) - 1)
        return CARACTERES_PEIXE[index]

    def encaixar_no_grid(self) -> Tuple[int, int]:
        """Arredondar as coordenadas do Peixe para uma posição existente no grid."""
        return int(round(self.x, 0)) - 1, int(round(self.y, 0)) - 1


class Cardume:
    def __init__(self, n_peixes: int):
        self.peixes: List[Peixe] = [Peixe() for _ in range(n_peixes)]

    def atualizar(self) -> None:
        for peixe in self.peixes:
            peixes_proximos = self.achar_peixes_proximos(peixe)
            peixe.alinhar(peixes_proximos)
            peixe.atualizar()

    def adicionar_peixe(self, peixe: Peixe):
        """Adicionar Peixe ao Cardume."""

        if isinstance(peixe, Peixe):
            self.peixes.append(peixe)

    def achar_peixes_proximos(self, peixe: Peixe, raio_de_busca: float = min(ALTURA_TELA, LARGURA_TELA) / 20):
        """Buscar Peixes do mesmo Cardume que estejam dentro de um determinado raio de busca."""

        x0, y0 = peixe.x, peixe.y
        esta_proximo = lambda px: (abs(px.x - x0) + abs(px.y - y0)) / raio_de_busca <= DISTANCE_CONSTANT
        peixes_proximos = list(filter(esta_proximo, self.peixes))
        return peixes_proximos

    @staticmethod
    def calcular_baricentro(self, vizinhanca_de_peixes: List[Peixe]) -> Tuple[float, float]:
        """Calcular o baricentro (centro de massa) de n-Peixes coexistindo em uma vizinhança."""
        pass

    def exibir(self) -> None:
        """Exibir configuração atual do Cardume."""
        self.atualizar()
        matriz = []
        for index_linha in range(ALTURA_TELA):
            linha = [GRID_VAZIO] * LARGURA_TELA
            linha.append('   |')
            matriz.append(linha)
        matriz.append(['___'] * (LARGURA_TELA + 1))
        for peixe in self.peixes:
            grid_x, grid_y = peixe.encaixar_no_grid()
            matriz[grid_y][grid_x] = peixe.definir_char()

        for index, ln in enumerate(matriz):
            stdscr.addstr(index, 0, ''.join(ln))
        stdscr.refresh()


if __name__ == '__main__':
    os.system('cls')
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()

    try:
        cardume = Cardume(150)
        for _ in range(300):
            cardume.exibir()
            time.sleep(FPS / 6000)

    finally:
        curses.echo()
        curses.nocbreak()
        curses.endwin()
