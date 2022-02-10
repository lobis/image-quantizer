class RGB:
    R: int
    G: int
    B: int

    def __init__(self, rgb: list = None, r: int = None, g: int = None, b: int = None):
        r_g_b_none = r is None and g is None and b is None
        assert not (rgb is not None and not r_g_b_none), \
            "use 'rgb' or 'r', 'g', 'b' as initializers, not both"
        if rgb is None:
            if r_g_b_none:
                r, g, b = 0, 0, 0  # default
            # if one of r, g or b is defined, all need to be defined
            else:
                assert r is not None and g is not None and b is not None, \
                    "if one of 'r', 'g' and 'b' are defined, all need to be defined"
            rgb = [r, g, b]

        assert len(rgb) == 3, \
            "Color must have 3 elements [R,G,B] each represented as an integer from 0 to 255"
        for value in rgb:
            assert isinstance(value, int), \
                f"value '{value}' in {rgb} is not an integer"
            assert 0 <= value <= 255, \
                f"value '{value}' in {rgb} is not between 0 and 255"
        self.R = rgb[0]
        self.G = rgb[1]
        self.B = rgb[2]

    def __eq__(self, other):
        if not isinstance(other, RGB):
            other = RGB(other)
        return self.R == other.R and self.G == other.G and self.B == other.B

    def __iter__(self):
        for value in [self.R, self.G, self.B]:
            yield value

    def __repr__(self):
        return f"[R={self.R}, G={self.G}, B={self.B}]"


class Palette(list):
    def __init__(self, palette: list = None):
        # initializer is a list containing lists of 3 numbers (RBG colors)
        # i.e. initializer = [[0, 255, 0], [255, 0, 255], ...]
        if palette is None:
            palette = [[0, 0, 0], [255, 255, 255]]

        colors = []

        for color in palette:
            # check if color is valid
            rgb = RGB(color)
            rgb = [rgb.R, rgb.G, rgb.B]
            assert rgb not in colors
            colors.append(rgb)

        super(Palette, self).__init__(colors)

    def __repr__(self):
        return f"""Palette with {len(self)} colors: {", ".join([str(color) for color in self])}"""

    def flat(self):
        return sum(self, start=[])


PALETTES = {
    "BLACK-AND-WHITE": Palette([
        [0, 0, 0],  # Black
        [255, 255, 255],  # White
    ]),
    "BLACK-WHITE-RED": Palette([
        [0, 0, 0],  # Black
        [255, 255, 255],  # White
        [255, 0, 0],  # Red
    ]),
    "WAVESHARE-EPD-7COLOR": Palette([
        [0, 0, 0],  # Black
        [255, 255, 255],  # White
        [0, 128, 0],  # Green
        [0, 0, 255],  # Blue
        [255, 0, 0],  # Red
        [255, 255, 0],  # Yellow
        [255, 170, 0],  # Orange
    ])
}
