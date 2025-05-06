class Scene:
    """Holds all data required to render a 3D scene."""

    def __init__(self, camera, objects, lights, width, height):
        self.camera = camera     # Position of the camera
        self.objects = objects   # List of objects in the scene
        self.lights = lights     # List of light sources
        self.width = width       # Image width in pixels
        self.height = height     # Image height in pixels

   