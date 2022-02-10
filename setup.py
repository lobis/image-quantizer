import pathlib
from distutils.core import setup

ROOT_DIR = pathlib.Path(__file__).parent
README = (ROOT_DIR / "README.md").read_text()

setup(
    name="image-quantizer",
    version="0.0.0",
    description="Convert image into quantized image compatible with epaper display",
    long_description=README,
    url="https://github.com/lobis/image-quantizer",
    author="Luis Antonio Obis Aparicio",
    author_email="luis.antonio.obis@gmail.com",
    packages=["image_quantizer"],
    requires=["Pillow"]
)
