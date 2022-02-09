import pytest

import pathlib
import os
from PIL import Image

from waveshare_epaper_image import quantize_image, PALETTES

data_path = pathlib.Path(__file__).parents[0] / "data"
test_image = data_path / "avatar.jpg"


def test_data_path():
    assert os.path.isdir(data_path)
    assert os.path.isfile(test_image)


def test_quantize_image():
    with Image.open(test_image) as image:
        quantize_image(image, palette=PALETTES["BLACK-WHITE-RED"])

    with Image.open(test_image) as image:
        result = Image.new("RGB", (2 * image.width, 2 * image.height))

        quantized_image_bw = quantize_image(image, palette=PALETTES["BLACK-AND-WHITE"])
        quantized_image_bwr = quantize_image(image, palette=PALETTES["BLACK-WHITE-RED"])
        quantized_image_7color = quantize_image(image, palette=PALETTES["WAVESHARE-EPD-7COLOR"])

        # combine images
        result.paste(image, (0, 0))
        result.paste(quantized_image_bw, (image.width, 0))
        result.paste(quantized_image_bwr, (0, image.height))
        result.paste(quantized_image_7color, (image.width, image.width))

        result.show()
