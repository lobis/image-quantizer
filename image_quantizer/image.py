from PIL import Image

from typing import Union
import io
from typing import Dict

from .palette import Palette, PALETTES, RGB


def quantize_image(image: Image.Image, palette: Union[Palette, list, str], dither: bool = True) -> Image.Image:
    # Create auxiliary image to hold the palette
    palette_image = Image.new("P", (16, 16))

    image.load()
    palette_image.load()
    # Palette needs to be padded to 256 size, we repeat colors, it doesn't matter which
    palette_size_required = 256
    if isinstance(palette, str):
        assert palette in PALETTES.keys(), \
            f"pallete '{palette}' is not a valid palette name. Valid names are: {list(PALETTES.keys())}"
        palette = PALETTES[palette]
    elif isinstance(palette, list):
        palette = Palette(palette)

    palette_flat = palette.flat()
    assert len(palette_flat) <= palette_size_required * 3
    palette_padded = [palette_flat[i % len(palette_flat)]
                      for i in range(palette_size_required * 3)]
    palette_image.putpalette(palette_padded)

    quantized_image = image.quantize(palette=palette_image, dither=dither)

    return quantized_image


def get_image_palette(image: Image.Image) -> Palette:
    number_of_colors = len(image.getcolors())
    assert image.mode == "P", \
        f"""
        Input image mode is "{image.mode}" instead of "P", are you sure this image should be split by colors? 
        This Image has {number_of_colors} colors
        """
    original_palette = image.getpalette()
    result = []
    for i in range(number_of_colors):
        color = [original_palette[3 * i], original_palette[3 * i + 1], original_palette[3 * i + 2]]
        result.append(color)

    return Palette(result)


def split_image_by_color(image: Image.Image) -> Dict[RGB, Image.Image]:
    """
    :param image: Pillow image, of "P" type, such as the output of 'quantize_image'
    :return: dictionary mapping color name to image

    This method splits an image (a quantized image) into its different colors, except for white,
    which is considered the background color.
    It will return a dictionary mapping color to an image only containing the particular color with white as background
    """

    width, height = image.size

    palette = get_image_palette(image)
    assert [255, 255, 255] in palette, \
        f"""White color not in palette: {str(palette)}"""

    result = {color: Image.new("RGB", (width, height), (255, 255, 255)) for color in palette if
              color != RGB([255, 255, 255])}
    assert len(result) == len(palette) - 1

    white_color_position = 0
    for white_color_position, color in enumerate(palette):
        if color == RGB([255, 255, 255]):
            break

    for x in range(width):
        for y in range(height):
            pixel = image.getpixel((x, y))
            if pixel == white_color_position:
                continue
            for color_key in result:
                if palette[pixel] == color_key:
                    result_image = result[color_key]
                    result_image.putpixel((x, y), (color_key.R, color_key.G, color_key.B))
                    break

    return result


def image_to_bytes(image: Image.Image, format: str = "PNG") -> bytes:
    buffer = io.BytesIO()
    image.save(buffer, format=format)
    return buffer.getvalue()
