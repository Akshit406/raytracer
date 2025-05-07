import os
import math
from PIL import Image
from checkerboardMaterial import ChequeredMaterial
from engine import RenderEngine
from scene import Scene
from color import Color
from light import Light
from material import Material
from point import Point
from sphere import Sphere
from vector import Vector

WIDTH = 960
HEIGHT = 540
NUM_FRAMES = 60  # Total frames in animation
FRAME_FOLDER = "frames"
PNG_FOLDER = "converted_frames"
GIF_OUTPUT = "animation.gif"

# Create necessary directories
os.makedirs(FRAME_FOLDER, exist_ok=True)
os.makedirs(PNG_FOLDER, exist_ok=True)

def animated_render():
    CAMERA = Vector(0, -0.35, -1)
    frames = []

    for frame in range(NUM_FRAMES):
        t = frame / NUM_FRAMES * 2 * math.pi  # Normalize time over one cycle
        bounce_height = 0.3 * abs(math.sin(t))  # Bouncing effect (keeps it above ground)

        OBJECTS = [
            # Ground Plane (unchanged)
            Sphere(
                Point(0, 10000.5, 1),
                10000.0,
                ChequeredMaterial(
                    color1=Color.from_hex("#420500"),
                    color2=Color.from_hex("#e6b87d"),
                    ambient=0.2,
                    reflective=0.2,
                ),
            ),
            # Blue ball (bouncing)
            Sphere(Point(3.75, bounce_height - 0.1, 6), 0.6, Material(Color.from_hex("#000FF"))),
            # Pink ball (unchanged)
            Sphere(Point(-0.75, bounce_height-0.1, 2.25), 0.6, Material(Color.from_hex("#803980"))),
        ]

        LIGHTS = [
            Light(Point(1.5, -0.5, -10), Color.from_hex("#FFFFFF")),
            Light(Point(-0.5, -10.5, 0), Color.from_hex("#E6E6E6")),
        ]

        scene = Scene(CAMERA, OBJECTS, LIGHTS, WIDTH, HEIGHT)
        render_engine = RenderEngine()
        image = render_engine.render(scene)

        # Save PPM frame
        ppm_path = os.path.join(FRAME_FOLDER, f"frame_{frame:03d}.ppm")
        with open(ppm_path, "w") as img_file:
            image.write_ppm(img_file)

        # Convert to PNG
        png_path = os.path.join(PNG_FOLDER, f"frame_{frame:03d}.png")
        img = Image.open(ppm_path)
        img.save(png_path)
        frames.append(img)

        print(f"Frame {frame+1}/{NUM_FRAMES} rendered")

    # Generate animated GIF from PNG frames
    frames[0].save(GIF_OUTPUT, save_all=True, append_images=frames, duration=33, loop=0)
    print(f"Animation saved as {GIF_OUTPUT}")

if __name__ == "__main__":
    animated_render()
