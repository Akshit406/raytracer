class Plane:
    def __init__(self, point, normal_vector, material):
        self.point = point
        self.normal_vector = normal_vector  # Renamed to avoid confusion
        self.material = material

    def intersect_ray(self, ray):
        denom = self.normal_vector.dot_product(ray.direction)
        if abs(denom) > 1e-6:
            t = (self.point - ray.origin).dot_product(self.normal_vector) / denom
            if t >= 0:
                return t
        return None

    def normal(self, _):
        return self.normal_vector  # Always return the same normal for a plane