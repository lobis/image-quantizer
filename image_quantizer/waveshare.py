from PIL import Image

from .palette import Palette, PALETTES


class DisplayConfig:
    palette: Palette
    size: tuple

    def __init__(self, palette: Palette, size: tuple):
        self.palette = palette
        self.size = size

    def __eq__(self, other):
        return self.palette == other.palette and self.size == other.size


WAVESHARE_EPAPER_DISPLAY_CONFIGS = {
    "WAVESHARE-EPD-7COLOR": DisplayConfig(palette=PALETTES["WAVESHARE-EPD-7COLOR"], size=(600, 448))
}


def prepare_image(image: Image.Image, size: tuple) -> Image.Image:
    display_x, display_y = size
    display_ratio = display_x / display_y

    image_x, image_y = image.size
    image_ratio = image_x / image_y

    offset = [0, 0]
    if image_ratio > display_ratio:
        offset[0] = image.size[0] - display_ratio * image.size[1]
    else:
        offset[1] = image.size[1] - image.size[0] / display_ratio

    new_x = image.size[0] - offset[0]
    new_y = image.size[1] - offset[1]

    image = image.crop((0, 0, new_x, new_y))

    image.thumbnail(size, Image.ANTIALIAS)

    assert image.size == size

    return image


def image_to_waveshare_bytes(image: Image.Image,
                             config: DisplayConfig = WAVESHARE_EPAPER_DISPLAY_CONFIGS["WAVESHARE-EPD-7COLOR"],
                             verify: bool = True) -> bytes:
    # Only works with 7 color ePaper display (yet)
    assert config == WAVESHARE_EPAPER_DISPLAY_CONFIGS["WAVESHARE-EPD-7COLOR"]

    palette = config.palette

    # verify image is compatible, it should be a quantized image with the corresponding palette
    if verify:
        unique_colors = set(list(image.getdata()))
        color = unique_colors.pop()  # get any item from set
        unique_colors.add(color)  # add it back
        assert isinstance(color, int)
        assert len(unique_colors) <= len(palette)
        assert min(unique_colors) >= 0
        assert max(unique_colors) < len(palette)

    assert image.size == (config.size[0], config.size[1]), \
        f"image size '{image.size}' does not match display size '{config.size}'"

    image_flat = list(image.getdata())

    result = bytearray(int(len(image_flat) / 2))
    for i in range(len(result)):
        result[i] = image_flat[2 * i] * 16 + image_flat[2 * i + 1]

    return bytes(result)
