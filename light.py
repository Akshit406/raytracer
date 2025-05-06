from color import Color

class Light:
    """A simple point light source in the scene."""
    
    def __init__(self, position, color=Color.from_hex("#FFFFFF")):
        self.position = position  # Position of the light source (a Point or Vector)
        self.color = color        # Color/intensity of the ligh

 
