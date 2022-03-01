import pytest

import pathlib
import os
from PIL import Image

from image_quantizer import quantize_image, PALETTES, get_image_palette, split_image_by_color, RGB

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


def test_quantize_black_white_red():
    from image_quantizer import quantize_image

    with Image.open(test_image) as image:
        quantized_image_custom = quantize_image(image, palette="BLACK-WHITE-RED")
        new_image_path = test_image.parents[0] / f"{test_image.stem}-quantized-BWR.png"
        # quantized_image_custom.save(new_image_path)
        with Image.open(new_image_path) as test_result_image:
            assert list(test_result_image.getdata()) == list(quantized_image_custom.getdata())


def test_get_image_palette():
    image_path = test_image.parents[0] / f"{test_image.stem}-quantized-BWR.png"
    with Image.open(image_path) as image:
        palette = get_image_palette(image)

    print(palette)
    assert len(palette) == 3
    assert palette == PALETTES["BLACK-WHITE-RED"]


def test_split_image_by_colors():
    image_path = test_image.parents[0] / f"{test_image.stem}-quantized-BWR.png"

    with Image.open(image_path) as image:
        result = split_image_by_color(image)

    for color, image_split in result.items():
        assert color in [RGB([0, 0, 0]), RGB([255, 0, 0])]

        color_name = "WHITE"
        if color == RGB([0, 0, 0]):
            color_name = "BLACK"
        elif color == RGB([255, 0, 0]):
            color_name = "RED"

        new_image_path = test_image.parents[0] / f"{test_image.stem}-quantized-BWR-{color_name}.png"
        # image_split.save(new_image_path)
        with Image.open(new_image_path) as test_result_image:
            assert list(test_result_image.getdata()) == list(image_split.getdata())
