from color import Color

class Material:
    """Defines how a surface interacts with light."""

    def __init__(self, color=Color.from_hex("#FFFFFF"), ambient=0.05, diffuse=1.0, specular=1.0, reflective=0.5,transparency=0.5, refractive=1.0):
        self.color = color              # Base color of the material
        self.ambient = ambient          # Ambient reflection coefficient
        self.diffuse = diffuse          # Diffuse reflection coefficient (Lambert)
        self.specular = specular        # Specular reflection coefficient (Blinn-Phong)
        self.reflective = reflective    # Reflection coefficient (0 to 1)
        self.transparency = transparency  
        self.refractive = refractive  # Refraction index (for transparent materials)


    def color_at(self, position):
        """Returns the color of the material at a given point."""
        return self.color


