---
name: components
description: Vuer 3D component reference - primitives, meshes, URDF, cameras, lighting, images (plugin:vuer@vuer)
---

# Vuer Components

Import: `from vuer.schemas import Box, Sphere, TriMesh, Urdf, PointCloud, ...`

## Common Properties

All components: `key`, `position=[x,y,z]`, `rotation=[x,y,z]`, `scale`, `matrix` (4x4), `children`

## Primitives

```python
Box(key="box", args=[w, h, d], color="red")
Sphere(key="s", args=[radius, wSegs, hSegs])
Cylinder(key="c", args=[rTop, rBot, height, segs])
Capsule(key="cap", args=[radius, height, capSegs, radSegs])
Cone, Plane, Ring, Torus, TorusKnot
```

## Custom Geometry

```python
TriMesh(key="mesh", vertices=np.array, faces=np.array, colors=np.array)
PointCloud(key="pcd", vertices=np.array, colors=np.array, size=0.01)
```

## Models

```python
Urdf(key="robot", src="/static/robot.urdf", jointValues={"joint1": 0.5})
Glb(key="model", src="/static/model.glb", scale=0.1)
Obj, Ply, Stl, Fbx, Dae  # Same pattern
Splat(key="splat", src="/static/scene.splat")  # Gaussian splatting
```

## Cameras & Lighting

```python
PerspectiveCamera(key="cam", fov=75, position=[5,5,5], makeDefault=True)
Frustum(key="f", fov=60, aspect=1.6, near=0.1, far=10, showFrustum=True)
AmbientLight, DirectionalLight, PointLight, SpotLight
```

## Images

```python
Img(src="url", key="img")                    # DOM image
Img(np_array, key="np")                      # From numpy
Image(img_array, position=[0,1,-2], key="p") # 3D plane
ImageBackground(src="bg.jpg", distance=10)   # Camera-facing
```

## Interaction

```python
Movable(key="m", children=[Box(key="box")])  # Drag & drop
Gripper(key="g", pinchWidth=0.04)            # Gripper viz
```

## Organization

```python
group(key="grp", children=[...])
Scene(children=[...], bgChildren=[Grid()], rawChildren=[AmbientLight()])
DefaultScene(...)  # Includes default lighting/controls
```
