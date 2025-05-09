# Raytracer

This project implements a **basic raytracing engine** in Python, capable of rendering **realistic 3D images and videos** with lighting, shadows, reflections, and refraction.

## Features
- **Ray tracing** for realistic image rendering  
- **Multiprocessing** support for faster rendering  
- **Transparency and refraction** simulation  
- **Custom materials and textures**  
- **Animation rendering** with Pillow  
- **Integration with FFmpeg** for video creation  

---

## Installation & Setup

### 1. **Clone the Repository**
```
git clone https://github.com/YOUR_USERNAME/raytracer-project.git
cd raytracer-project
```
### 2. Install Dependencies
```
pip install pillow numpy tqdm ffmpeg-python multiprocessing

```
### 3. Run the Raytracer scene gif
```
python main.py
```

## Modify scene

You can update scene.py to:

> Add new objects (spheres, planes),
> Adjust lighting positions,
> Set camera angles,

```
OBJECTS = [Sphere(Point(-0.75, 0.1, 1.25), 0.6, Material(Color.from_hex("#803980"))), ]
```




