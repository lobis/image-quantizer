import pytest

from image_quantizer import RGB, Palette, PALETTES


def test_color():
    with pytest.raises(AssertionError):
        # values in 0 to 255
        RGB([0, 500, 0])

    with pytest.raises(AssertionError):
        # values in 0 to 255
        RGB([0, 0, -2])

    with pytest.raises(AssertionError):
        # no decimals
        RGB([120.0, 0, 0])

    with pytest.raises(AssertionError):
        # only one, not both initializations
        RGB(rgb=[0, 0, 0], r=0)

    with pytest.raises(AssertionError):
        # all three have to be defined
        RGB(r=0, b=0)

    assert RGB(rgb=[120, 0, 255]) == RGB(r=120, g=0, b=255)
    assert RGB() == [0, 0, 0] == list(RGB())

    print(f"Default RGB: {RGB()}")


def test_palette():
    palette = Palette([[0, 0, 0], [255, 255, 255]])
    print(palette)

    with pytest.raises(AssertionError):
        # each color is length 3 (RGB)
        Palette([[0, 0, 0], [255, 255, 255, 0]])

    with pytest.raises(AssertionError):
        # no duplicates
        Palette([[0, 120, 0], [0, 120, 0]])

    palette = Palette([[0, 0, 0], [255, 255, 255]])
    assert len(palette) == 2

    palette_flat = Palette([[0, 0, 120], [255, 0, 255]]).flat()
    print(palette_flat)
    assert len(palette_flat) == 6


def test_default_palettes():
    assert len(PALETTES) == 3
    for palette in PALETTES.values():
        assert isinstance(palette, Palette)
