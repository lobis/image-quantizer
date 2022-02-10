from PIL import Image

from typing import Union
import io

from .palette import Palette, PALETTES


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


def image_to_bytes(image: Image.Image, format: str = "PNG") -> bytes:
    buffer = io.BytesIO()
    image.save(buffer, format=format)
    return buffer.getvalue()
