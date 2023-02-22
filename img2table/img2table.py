# Converter uma imagem para uma tabela em HTML, determinando a resolução nos eixos X e Y;
# Transparência pode ser ignorada.

import numpy as np
from PIL import Image
from pathlib import Path
from typing import Optional, Tuple, Union


class Converter:
    def __init__(self):
        self.image_source: Optional[Path] = None
        self.image_data: Optional[np.array] = None
        self.image_as_html: Optional[str] = None

    def _read_image(self, file_source: Union[Path, str]) -> Tuple[int, int]:
        """Ler imagem como um 2D Array."""

        if isinstance(file_source, str):
            file_source = Path(file_source)

        if not file_source.is_file():
            raise FileNotFoundError('Arquivo de imagem não encontrado.')

        self.image_source = file_source
        img = Image.open(file_source)
        width, height = img.size
        img = img.convert('RGBA')
        img_as_array = np.array(list(img.getdata()))
        img_as_array = img_as_array.reshape((height, width, 4))
        self.image_data = img_as_array

        return width, height

    def _convert_to_table(self, img_width: int, img_height: int, x_res: float, y_res: float, ignore_alpha: bool) -> str:
        """Converter 2D Array para HTML Table."""

        table = []
        cell_width = int(1 // x_res)
        cell_height = int(1 // y_res)
        for y in range(0, img_height, cell_height):
            row = []
            for x in range(0, img_width, cell_width):
                pixel_color = list(map(str, self.image_data[y][x]))
                if ignore_alpha:
                    pixel_color[-1] = '1'
                else:
                    pixel_color[-1] = str(int(int(pixel_color[-1]) // 255))
                cell_color = f'rgba({", ".join(pixel_color)})'
                cell = f'<td style="background-color: {cell_color}; width: 1px; height: 1px;"></td>'
                row.append(cell)
            table.append(f'<tr>{"".join(row)}</tr>')

        table_html = f'<table style="border: 0px; border-collapse: collapse;">{"".join(table)}</table>'
        return table_html

    def image_to_table(self, file_source: Union[Path, str], x_res: float = 1, y_res: float = 1,
                       ignore_alpha: bool = False) -> str:
        """Converter imagem para HTML Table."""

        img_width, img_height = self._read_image(file_source)
        image_as_html = self._convert_to_table(img_width, img_height, x_res, y_res, ignore_alpha)
        self.image_as_html = image_as_html
        return image_as_html

    def export_html(self, html_data: Optional[str] = None, output_filepath: Union[Path, str] = None) -> Path:
        """Exportar HTML."""

        if output_filepath is None:
            output_filepath = Path().home().joinpath(r'Documents\img_as_table.html')

        if isinstance(output_filepath, str):
            output_filepath = Path(output_filepath)

        if not str(output_filepath).endswith('.html'):
            output_filepath = Path(str(output_filepath) + '.html')

        if html_data is None:
            if self.image_as_html is not None:
                html_data = self.image_as_html
            else:
                ValueError('O atributo "image_as_html" está com valor nulo. Rode a fução "image_to_table" primeiro.')
        with open(output_filepath, 'w') as file:
            file.write(html_data)
            file.close()

        return output_filepath

    def export_array(self, array: Optional[np.array] = None, output_filepath: Union[Path, str] = None) -> Path:
        """Exportar 2D Array."""

        if output_filepath is None:
            output_filepath = Path().home().joinpath(r'Documents\image_as_array.npy')

        if isinstance(output_filepath, str):
            output_filepath = Path(output_filepath)

        if not str(output_filepath).endswith('.npy'):
            output_filepath = Path(str(output_filepath) + '.npy')

        if array is None:
            array = self.image_data

        np.save(output_filepath, array)
        return output_filepath


if __name__ == '__main__':
    conv = Converter()
    tbl = conv.image_to_table(r"C:\Users\Lucas Petersen\Pictures\Saved Pictures\DonaldMad.jpeg", x_res=1, y_res=1)
    conv.export_array()
    print(tbl)
