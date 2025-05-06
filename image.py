class Image:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pixels = [[None for _ in range(width)] for _ in range(height)]
        # Defining a 2D array of pixels with the given width and height
        # Each pixel is a Color object (a subclass of the Vector class)

    def set_pixel(self, x, y, color):
        self.pixels[y][x] = color

    def write_ppm(self, img_file):
        def to_byte(x):
            return round(max(min(x * 255, 255), 0))

        # defines the ppm file
        img_file.write(f"P3 {self.width} {self.height}\n255\n")
        for row in self.pixels:
            for color in row:
                img_file.write(f"{to_byte(color.x)} {to_byte(color.y)} {to_byte(color.z)} ")
