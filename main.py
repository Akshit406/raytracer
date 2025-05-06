from color import Color
from point import Point
from vector import Vector
from material import Material
from light import Light
from sphere import Sphere
from camera import Camera
from scene import Scene
from engine import RenderEngine
from image import Image

def main():
    camera_position = Point(0, 0, -5)  # Position of the camera in 3D space
    camera_direction = Vector(0, 0, 1)  # Direction the camera is facing
    camera = Camera(camera_position, camera_direction)

    
    red_material = Material(color=Color.from_hex("#FF0000"), ambient=0.1, diffuse=0.7, specular=0.5)
    green_material = Material(color=Color.from_hex("#00FF00"), ambient=0.1, diffuse=0.7, specular=0.5)
    
    sphere1 = Sphere(center=Point(0, -1, 3), radius=1, material=red_material)
    sphere2 = Sphere(center=Point(2, 0, 4), radius=1, material=green_material)
    
    light_position = Point(-5, 5, -10)  # Position of the light source
    light_color = Color.from_hex("#FFFFFF")  # White light
    light = Light(position=light_position, color=light_color)
    
    scene = Scene(
        camera=camera,
        objects=[sphere1, sphere2],
        lights=[light],
        width=800,
        height=600
    )
    
    render_engine = RenderEngine()
    image = render_engine.render(scene)
    
    with open("output.ppm", "w") as img_file:
        image.write_ppm(img_file)
    
    print("Rendering complete! Image saved as 'output.ppm'.")

if __name__ == "__main__":
    main()
