from pandas import DataFrame
from typing import Union, List
from PIL import Image, ImageOps

intensities = [' ', '.', ',', ':', 'i', 'l', 'w', 'W']
intensities.reverse()
number = Union[float, int]


def remap(val: number, curr_min: number, curr_max: number, new_min: number, new_max: number) -> int:
    return int(round((val - curr_min) / (curr_max - curr_min) * (new_max - new_min) + new_min, 0))


def read_image(path: str, resolution: number = 1) -> Image.Image:
    """Ler imagem na resolução especificada, como grayscale."""
    image = Image.open(path)
    grayscale_image = ImageOps.grayscale(image)
    width, height = grayscale_image.size
    new_width = int(round(width * resolution, 0))
    new_height = int(round(height * resolution, 0))
    resized_image = grayscale_image.resize((new_width, new_height))
    return resized_image


def turn_into_chars(image: Image.Image) -> List[List[str]]:
    """Converter objeto Image.Image para 2D List com as intensidades de cor representadas com caractéres."""
    image_as_chars = []
    width, height = image.size
    for j in range(height):
        row = []
        for i in range(width):
            pixel_color = image.getpixel((i, j))
            pixel_color_remapped = remap(val=pixel_color, curr_min=0, curr_max=255, new_min=0, new_max=len(intensities) - 1)
            row.append(intensities[pixel_color_remapped])
        image_as_chars.append(row)
    return image_as_chars


def copy_chars_to_clipboard(chars: List[List[str]]) -> None:
    image_as_df = DataFrame(chars)
    image_as_df.to_clipboard(index=False, header=False)


def main(path):
    image = read_image(path, resolution=0.2)
    chars = turn_into_chars(image)
    copy_chars_to_clipboard(chars)


if __name__ == '__main__':
    main(r"C:\Users\Lucas Petersen\Desktop\20160617_154847.jpg")
