from PIL import Image
import io
from typing import Union

from .palette import Palette

PALETTE = [
    0, 0, 0,  # Black
    255, 255, 255,  # White
    0, 128, 0,  # Green
    0, 0, 255,  # Blue
    255, 0, 0,  # Red
    255, 255, 0,  # Yellow
    255, 170, 0,  # Orange
]


def quantize_image(image: Image.Image, palette: Union[Palette, list], dither: bool = True) -> Image.Image:
    # Create auxiliary image to hold the palette
    palette_image = Image.new("P", (16, 16))

    image.load()
    palette_image.load()
    # Palette needs to be padded to 256 size, we repeat colors, it doesn't matter which
    palette_size_required = 256
    if isinstance(palette, list):
        palette = Palette(palette)
    palette_flat = palette.flat()
    assert len(palette_flat) <= palette_size_required * 3
    palette_padded = [palette_flat[i % len(palette_flat)]
                      for i in range(palette_size_required * 3)]
    palette_image.putpalette(palette_padded)

    quantized_image = image.quantize(palette=palette_image, dither=dither)

    return quantized_image


def pillow_image_to_bytes(image, format="PNG"):
    buffer = io.BytesIO()
    image.save(buffer, format=format)
    return buffer.getvalue()
