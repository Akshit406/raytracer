from image import Image
from ray import Ray
from point import Point
from color import Color
from material import Material  
from light import Light  
import sys
import multiprocessing
from functools import partial
import math


class RenderEngine:
    """Renders 3D objects into a 2D image using ray tracing."""

    MAX_DEPTH = 7
    MIN_DISPLACEMENT = 0.0001

    def refract(self,ray_direction, normal, eta_ratio):
        """Compute refracted direction using Snell's Law."""
        cos_theta = -normal.dot_product(ray_direction)
        sin2_theta = eta_ratio**2 * (1 - cos_theta**2)

        if sin2_theta > 1:  
            return None  # Total internal reflection occurs

        refracted_dir = eta_ratio * ray_direction + (eta_ratio * cos_theta - math.sqrt(1 - sin2_theta)) * normal
        return refracted_dir.normalize()


    def render_chunk(self, start_y, end_y, width, scene, max_reflections):
            """Render a portion of the image"""
            pixels = [[None for _ in range(width)] for _ in range(end_y - start_y)]
            camera = scene.camera
            aspect_ratio = float(width) / scene.height
            x_min, x_max = -1.0, 1.0
            pixel_width_step = (x_max - x_min) / (width - 1)
            y_min, y_max = -1.0 / aspect_ratio, 1.0 / aspect_ratio
            pixel_height_step = (y_max - y_min) / (scene.height - 1)

            for j in range(start_y, end_y):
                y = y_min + j * pixel_height_step
                for i in range(width):
                    x = x_min + i * pixel_width_step
                    ray = Ray(camera, (Point(x, y) - camera))
                    pixels[j - start_y][i] = self.ray_trace(ray, scene, max_reflections)  

            return (start_y, pixels)

    def render(self, scene, max_reflections=3):
        import sys
        import multiprocessing
        from functools import partial

        width = scene.width
        height = scene.height
        num_processes = multiprocessing.cpu_count()
        chunk_size = height // num_processes

        with multiprocessing.Pool(processes=num_processes) as pool:
            render_partial = partial(self.render_chunk, width=width, scene=scene, max_reflections=max_reflections)
            chunks = [(i * chunk_size, min((i + 1) * chunk_size, height)) for i in range(num_processes)]

            results = pool.starmap(render_partial, chunks)

        pixels = Image(width, height)
        for start_y, chunk_pixels in results:
            for j, row in enumerate(chunk_pixels):
                for i, color in enumerate(row):
                    pixels.set_pixel(i, start_y + j, color)

            progress = (start_y / height) * 100
            sys.stdout.write(f"\rRendering: {progress:.2f}%")
            sys.stdout.flush()

        print("\nRendering complete!")
        return pixels
    
    def ray_trace(self, ray, scene, depth=0):
        """Trace a ray through the scene and compute color with reflection & refraction."""
        if depth >= self.MAX_DEPTH:
            return Color(0, 0, 0)  # Stop recursion

        dist_hit, obj_hit = self.find_nearest(ray, scene)
        if obj_hit is None:
            return Color(0, 0, 0)  # No intersection

        hit_pos = ray.point_at(dist_hit)
        hit_normal = obj_hit.normal(hit_pos)
        material = obj_hit.material
        obj_color = material.color_at(hit_pos)
        color = obj_color * material.ambient  # Ambient shading

        # Refraction Handling
        if material.transparency > 0:
            eta_ratio = 1.0 / material.refractive  # Air (1.0) 
            refracted_dir = self.refract(ray.direction, hit_normal, eta_ratio)

            if refracted_dir:
                refracted_ray = Ray(hit_pos + refracted_dir * self.MIN_DISPLACEMENT, refracted_dir)
                color += self.ray_trace(refracted_ray, scene, depth + 1) * material.transparency

        # Reflection Handling
        reflected_dir = ray.direction - 2 * ray.direction.dot_product(hit_normal) * hit_normal
        reflected_ray = Ray(hit_pos + hit_normal * self.MIN_DISPLACEMENT, reflected_dir)
        color += self.ray_trace(reflected_ray, scene, depth + 1) * material.reflective

        # Light interaction (Lambertian shading & specular highlights)
        for light in scene.lights:
            to_light = Ray(hit_pos, light.position - hit_pos).direction.normalize()
            color += obj_color * material.diffuse * max(0, hit_normal.dot_product(to_light))
            
            half_vector = (to_light + (scene.camera - hit_pos).normalize()).normalize()
            color += light.color * material.specular * max(0, hit_normal.dot_product(half_vector)) ** 50  # Specular exponent

        return color

    def find_nearest(self, ray, scene):
        """Find the nearest object that the ray intersects in the scene."""
        dist_min = None
        obj_hit = None
        for obj in scene.objects:
            dist = obj.intersect_ray(ray)  # Use intersect_ray instead of intersects
            if dist is not None and (obj_hit is None or dist < dist_min):
                dist_min = dist
                obj_hit = obj
        return dist_min, obj_hit
    
    def color_at(self, obj_hit, hit_pos, normal, scene):
        """Calculate the color at the intersection point based on lighting and material."""
        material = obj_hit.material
        obj_color = material.color_at(hit_pos)
        to_cam = scene.camera - hit_pos
        color = material.ambient * Color.from_hex("#FFFFFF")  
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