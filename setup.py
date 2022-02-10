import pathlib
from distutils.core import setup

__version__ = ""  # added to prevent linting error
exec(open("image_quantizer/version.py").read())  # loads __version__

ROOT_DIR = pathlib.Path(__file__).parent
README = (ROOT_DIR / "README.md").read_text()

setup(
    name="image-quantizer",
    version=__version__,
    description="Convert image into quantized image compatible with Waveshare epaper display",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/lobis/image-quantizer",
    author="Luis Antonio Obis Aparicio",
    author_email="luis.antonio.obis@gmail.com",
    packages=["image_quantizer"],
    requires=["Pillow"]
)
