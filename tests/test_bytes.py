import pytest

import pathlib
import os
from PIL import Image

from image_quantizer import quantize_image, PALETTES, image_to_bytes

data_path = pathlib.Path(__file__).parents[0] / "data"
test_image = data_path / "cliff.jpg"


def test_data_path():
    assert os.path.isdir(data_path)
    assert os.path.isfile(test_image)


def test_quantize_image():
    with Image.open(test_image) as image:
        quantized_image_7color = quantize_image(image, palette=PALETTES["WAVESHARE-EPD-7COLOR"])
        data = image_to_bytes(quantized_image_7color)
        print(f"bytes: {data[:50]}")
