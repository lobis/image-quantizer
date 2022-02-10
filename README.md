# Image Quantizer

Simple Python package to convert an image into a quantized image using a customizable palette. Resulting image can be
displayed by ePaper displays such as Waveshare displays.

## Installation

It can be installed as a PyPi package

```
pip install --user image-quantizer
```

It can also be installed manually

```
git clone https://github.com/lobis/image-quantizer
cd image-quantizer
python3 setup.py install --user
```

## Usage

```
from image_quantizer import quantize_image

with Image.open("tests/data/cliff.jpg") as image:
    quantized_image = quantize_image(image, palette=PALETTES["WAVESHARE-EPD-7COLOR"])
    quantized_image.save("cliffs-quantized.png")
```

![input example image](https://raw.githubusercontent.com/lobis/image-quantizer/main/tests/data/cliff.jpg "Input example image")

![quantized example image](https://raw.githubusercontent.com/lobis/image-quantizer/main/tests/data/cliff-quantized-7color.png "Quantized example image")

### Custom palette

```
from image_quantizer import quantize_image, PALETTES

# Existing palette names
print(PALETTES)

palette = [
    [0, 0, 0],  # white
    [255, 255, 255],  # black
    [0, 0, 255],  # blue
    [0, 255, 0],  # green
]

with Image.open("tests/data/cliff.jpg") as image:
    quantized_image_custom = quantize_image(image, palette=palette)
    quantized_image_custom.show()
```

![quantized example image](https://raw.githubusercontent.com/lobis/image-quantizer/main/tests/data/cliff-quantized-custom.png "Quantized example image")
