import tkinter as tk


# Abrir e fechar porta
# Acender luz, barulho e contador quando tiver ligado
# Parar quando abrir porta
# Ligar se tiver digitado algo, senão 30 segundos por default
# Se clicar em ligar quando estiver rodando, adicionar 30 segundos
# Se clicar em parar uma vez, pausa
# Se clicar em parar duas vezes, reseta o contador
# Botão pra descongelar a partir do peso
# Botão pra fazer pipoca


def display_to_seconds(display_val: int):
    """Converter número digitado, que vai aparecer no display, pra valor real em segundos."""

    if display_val <= 99:
        return display_val
    else:
        minute_part = int(str(display_val)[:2])
        second_part = int(str(display_val)[2:])
        return minute_part * 60 + second_part


def seconds_to_display(seconds: int):
    """Converter valor real em segundos para o número que vai aparecer no display."""

    minute_part = str(seconds // 60)
    second_part = str(seconds % 60)
    return int(minute_part + second_part)
