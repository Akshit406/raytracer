from math import sqrt

class Sphere:
    """A sphere in 3D space, defined by center, radius, and material."""

    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material

    def intersect_ray(self, ray):
        """
        Checks if the ray intersects with the sphere.
        Returns the distance to the intersection point or None if there's no intersection.
        """
        sphere_to_ray = ray.origin - self.center

        # Coefficients for the quadratic equation: a*t^2 + b*t + c = 0
        a = 1  # Because ray.direction is normalized
        b = 2 * ray.direction.dot_product(sphere_to_ray)
        c = sphere_to_ray.dot_product(sphere_to_ray) - self.radius * self.radius

        discriminant = b * b - 4 * a * c

        if discriminant < 0:
            return None

        sqrt_discriminant = sqrt(discriminant)
        t1 = (-b - sqrt_discriminant) / (2 * a)
        t2 = (-b + sqrt_discriminant) / (2 * a)

        if t1 > 0:
            return t1
        elif t2 > 0:
            return t2

        return None

    def normal(self, surface_point):
        """Returns the normal vector at the surface point of the sphere."""
        return (surface_point - self.center).normalize()

    def __repr__(self):
        return f"Sphere(center={self.center}, radius={self.radius})"
