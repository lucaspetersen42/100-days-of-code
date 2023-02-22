from pathlib import Path
from typing import Tuple, List


class Image:
    def __init__(self, path: Tuple[str, Path]):
        self.path = path

    def convert_to_grayscale(self):
        """Converter imagem para preto e branco."""
        pass

    def find_lines(self) -> Tuple[List[float], List[float]]:
        """Achar a disposição das linhas na imagem."""
        pass

    def find_points(self, x_lines: List[float], y_lines: List[float]):
        """
        Achar as coordenadas A, D de todas as células, fazendo o cruzamento das linhas.

        A .______.B
          |      |
          |      |
        C .______. D
        """
        pass

    def read_cell(self):
        """Usar OCR para determinar o que tá escrito na célula."""
        pass

    def create_dataframe(self):
        """Criar dataframe a partir da leitura das células."""
        pass
