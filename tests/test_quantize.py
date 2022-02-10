import pytest

import pathlib
import os
from PIL import Image

from image_quantizer import quantize_image, PALETTES

data_path = pathlib.Path(__file__).parents[0] / "data"
test_image = data_path / "cliff.jpg"


def test_data_path():
    assert os.path.isdir(data_path)
    assert os.path.isfile(test_image)


def test_quantize_image():
    with Image.open(test_image) as image:
        quantized_image_7color = quantize_image(image, palette=PALETTES["WAVESHARE-EPD-7COLOR"])
        new_image_path = test_image.parents[0] / f"{test_image.stem}-quantized-7color.png"
        # quantized_image_7color.save(new_image_path)
        with Image.open(new_image_path) as test_result_image:
            assert list(test_result_image.getdata()) == list(quantized_image_7color.getdata())

    with Image.open(test_image) as image:
        result = Image.new("RGB", (2 * image.width, 2 * image.height))

        quantized_image_bw = quantize_image(image, palette=PALETTES["BLACK-AND-WHITE"])
        quantized_image_bwr = quantize_image(image, palette="BLACK-WHITE-RED")
        quantized_image_7color = quantize_image(image, palette=PALETTES["WAVESHARE-EPD-7COLOR"])
        with pytest.raises(AssertionError):
            quantize_image(image, palette="INVALID-PALETTE-NAME")

        # combine images
        result.paste(image, (0, 0))
        result.paste(quantized_image_bw, (image.width, 0))
        result.paste(quantized_image_bwr, (0, image.height))
        result.paste(quantized_image_7color, (image.width, image.height))

        result.show()


def test_quantize_custom_palette():
    from image_quantizer import quantize_image, PALETTES

    # Existing palette names
    print(PALETTES)

    palette = [
        [0, 0, 0],  # white
        [255, 255, 255],  # black
        [0, 0, 255],  # blue
        [0, 255, 0],  # green
    ]

    with Image.open(test_image) as image:
        quantized_image_custom = quantize_image(image, palette=palette)
        new_image_path = test_image.parents[0] / f"{test_image.stem}-quantized-custom.png"
        # quantized_image_custom.save(new_image_path)
        with Image.open(new_image_path) as test_result_image:
            assert list(test_result_image.getdata()) == list(quantized_image_custom.getdata())
