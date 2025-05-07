from color import Color

class ChequeredMaterial:
    """chessboard like pattern"""

    def __init__(
        self,
        color1=Color.from_hex("#FFFFFF"),
        color2=Color.from_hex("#000000"),
        ambient=0.05,
        diffuse=1.0,
        specular=1.0,
        reflective=0.5,
    ):
        self.color1 = color1
        self.color2 = color2
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.reflective = reflective

    def color_at(self, position):
        if int((position.x + 5.0) * 3.0) % 2 == int(position.z * 3.0) % 2:
            return self.color1
        else:
            return self.color2