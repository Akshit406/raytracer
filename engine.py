from image import Image
from ray import Ray
from point import Point
from color import Color
from material import Material  
from light import Light  

class RenderEngine:
    """Renders 3D objects into a 2D image using ray tracing."""

    def render(self, scene, max_reflections=3):
        width = scene.width
        height = scene.height
        aspect_ratio = float(width) / height
        x_min = -1.0
        x_max = 1.0
        pixel_width_step = (x_max - x_min) / (width - 1)
        y_min = -1.0 / aspect_ratio
        y_max = 1.0 / aspect_ratio
        pixel_height_step = (y_max - y_min) / (height - 1)

        camera = scene.camera
        pixels = Image(width, height)

        for j in range(height):
            y = y_min + j * pixel_height_step
            for i in range(width):
                x = x_min + i * pixel_width_step
                ray = Ray(camera, (Point(x, y) - camera))
                pixels.set_pixel(i, j, self.ray_trace(ray, scene, max_reflections))
                
        return pixels
    
    def ray_trace(self, ray, scene, depth, max_reflections=3):
        """Trace a ray through the scene and compute its color with reflections."""
        if depth > max_reflections:
            return Color(0, 0, 0)  # stop recursion after max_reflections

        color = Color(0, 0, 0)
        # Find the nearest object hit by the ray in the scene
        dist_hit, obj_hit = self.find_nearest(ray, scene)
        if obj_hit is None:
            return color  

        hit_pos = ray.get_position(dist_hit)
        hit_normal = obj_hit.normal(hit_pos)
        color += self.color_at(obj_hit, hit_pos, hit_normal, scene)

        # Reflection calculation 
        if obj_hit.material.reflective > 0:
            reflection_ray = self.get_reflection_ray(ray, hit_pos, hit_normal)
            reflection_color = self.ray_trace(reflection_ray, scene, depth + 1, max_reflections)
            color += reflection_color * obj_hit.material.reflective

        return color

    def find_nearest(self, ray, scene):
        """Find the nearest object that the ray intersects in the scene."""
        dist_min = None
        obj_hit = None
        for obj in scene.objects:
            dist = obj.intersects(ray)
            if dist is not None and (obj_hit is None or dist < dist_min):
                dist_min = dist
                obj_hit = obj
        return dist_min, obj_hit
    
    def color_at(self, obj_hit, hit_pos, normal, scene):
        """Calculate the color at the intersection point based on lighting and material."""
        material = obj_hit.material
        obj_color = material.color
        to_cam = scene.camera - hit_pos
        color = material.ambient * obj_color  
        specular_k = 50 

        # Light calculations
        for light in scene.lights:
            to_light = Ray(hit_pos, light.position - hit_pos)
            to_light.direction = to_light.direction.normalize()  
            normal = normal.normalize()  
            # Diffuse shading (Lambert shading model)
            color += (obj_color * material.diffuse * max(0, normal.dot_product(to_light.direction)))

            # Specular shading (Blinn-Phong model)
            half_vector = (to_light.direction + to_cam).normalize()
            color += (light.color * material.specular * max(0, normal.dot_product(half_vector)) ** specular_k)

        return color

    def get_reflection_ray(self, ray, hit_pos, hit_normal):
        """Generate the reflection ray at the hit position with the given normal."""
        incoming_dir = ray.direction
        reflected_dir = incoming_dir - hit_normal * 2 * incoming_dir.dot_product(hit_normal)
        return Ray(hit_pos, reflected_dir)
