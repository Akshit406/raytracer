from color import Color

class Light:
    """A simple point light source in the scene."""
    
    def __init__(self, position, color=Color.from_hex("#FFFFFF")):
        self.position = position
        self.color = color

    def __repr__(self):
        return f"Light(position={self.position}, color={self.color})"
