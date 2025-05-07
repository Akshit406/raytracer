class Camera:
    """Represents a camera in the scene."""

    def __init__(self, position, direction):
        self.position = position  # This should be a Point object
        self.direction = direction  # This should be a Vector object

    def get_position(self):
        return self.position