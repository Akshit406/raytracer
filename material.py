from color import Color

class Material:
    """Defines how a surface interacts with light."""
    
    def __init__(self, color=Color.from_hex("#FFFFFF"), ambient=0.05, diffuse=1.0, specular=1.0):
        self.color = color              # Base color of the material
        self.ambient = ambient          # Ambient reflection coefficient
        self.diffuse = diffuse          # Diffuse reflection coefficient (Lambert)
        self.specular = specular        # Specular reflection coefficient (Blinn-Phong)

    def color_at(self, obj_hit, hit_pos, scene):
        """Returns the color of the material at a given point."""
        return self.color

