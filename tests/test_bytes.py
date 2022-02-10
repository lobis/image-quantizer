import pytest

import pathlib
import os
from PIL import Image

from image_quantizer import quantize_image, image_to_waveshare_bytes, prepare_image, WAVESHARE_EPAPER_DISPLAY_CONFIGS

data_path = pathlib.Path(__file__).parents[0] / "data"
test_image = data_path / "cliff.jpg"


def test_data_path():
    assert os.path.isdir(data_path)
    assert os.path.isfile(test_image)


def test_waveshare_bytes():
    name = "WAVESHARE-EPD-7COLOR"
    config = WAVESHARE_EPAPER_DISPLAY_CONFIGS[name]
    with Image.open(test_image) as image:
        image_resized = prepare_image(image, size=config.size)
        assert image_resized.size == config.size
        quantized_image_7color = quantize_image(image_resized, palette=name)
        data = image_to_waveshare_bytes(quantized_image_7color)
        print(f"bytes: {data[:50]}")
