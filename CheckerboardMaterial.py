from color import Color

class ChequeredMaterial:
    """Chessboard-like pattern with transparency and refraction support."""

    def __init__(
        self,
        color1=Color.from_hex("#FFFFFF"),
        color2=Color.from_hex("#000000"),
        ambient=0.05,
        diffuse=1.0,
        specular=1.0,
        reflective=0.5,
        transparency=0.0,  # Controls how much light passes through
        refractive=1.0,  # Index of refraction
    ):
        self.color1 = color1
        self.color2 = color2
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.reflective = reflective
        self.transparency = transparency
        self.refractive = refractive

    def color_at(self, position):
        """Determine color based on position for a checkered effect."""
        check_x = int((position.x + 5.0) * 3.0) % 2
        check_z = int(position.z * 3.0) % 2

        return self.color1 if check_x == check_z else self.color2

    def refract(self, incident_ray, normal):
        """Computes refracted direction using Snell’s Law."""
        eta_ratio = 1.0 / self.refractive  # Air to material transition
        cos_theta = -normal.dot_product(incident_ray.direction)
        sin2_theta = eta_ratio**2 * (1 - cos_theta**2)

        if sin2_theta > 1:  # Total internal reflection case
            return None

        refracted_dir = eta_ratio * incident_ray.direction + (eta_ratio * cos_theta - (1 - sin2_theta) ** 0.5) * normal
        return refracted_dir.normalize()
