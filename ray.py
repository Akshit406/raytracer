class Ray:
    """A ray is defined by an origin point and a normalized direction vector."""

    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction.normalize()

    def point_at(self,t):
        """Returns the point at distance t along the ray."""
        return self.origin + self.direction * t

   
