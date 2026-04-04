---
name: creative-pipeline
version: 1.0.0
description: "Generates Blender Python scripts for infrastructure visualization and ffmpeg commands for video production and social media export."
user-invocable: true
allowed-tools: Read Grep Glob Bash
metadata:
  extensions:
    gsd-skill-creator:
      version: 1
      createdAt: "2026-02-27"
      triggers:
        intents:
          - "Blender"
          - "3D visualization"
          - "infrastructure render"
          - "bpy script"
          - "pipe model"
          - "equipment visualization"
          - "camera path"
          - "ffmpeg"
          - "video export"
          - "social media"
          - "walkthrough"
          - "animation"
          - "coolant flow"
          - "thermal visualization"
        contexts:
          - "infrastructure visualization"
          - "data center rendering"
          - "engineering animation"
          - "stakeholder presentation"
domain: physical-infrastructure
tier: output
depends_on:
  - blueprint-engine
safety: no-engineering-decisions
applies_to:
  - skills/physical-infrastructure/**
  - "*.blend"
  - "*.py"
---

# Creative Pipeline Skill

## At a Glance

Generate Blender Python (bpy) scripts for 3D infrastructure visualization and ffmpeg command sequences for video production and social media export — turning technical engineering designs into communication-ready visual deliverables.

**Activation:** After engineering design is verified and documented. InfrastructureRequest with outputFormat including 'render'. Stakeholder presentations, client deliverables, social media content creation.

**Output types:**

1. **Blender bpy scripts:** Python scripts that run in Blender's Scripting workspace to create pipe geometry, equipment meshes, materials, lighting, camera paths, and animations.
2. **ffmpeg commands:** Shell commands that assemble rendered frames into video and export to social media formats (YouTube, Instagram Reel, Twitter/X, thumbnail).

**Prerequisites:**
- Blender 3.6+ installed (free from blender.org)
- ffmpeg installed and in PATH (free from ffmpeg.org)
- Completed engineering design with dimensions and layout from blueprint engine

**Quick-start — Blender script generation:**
```python
import bpy
# Clear scene, set units to metric, configure Cycles renderer
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.render.engine = 'CYCLES'
```

**Quick-start — ffmpeg social media export:**
```bash
# Assemble rendered frames into video
ffmpeg -framerate 30 -i render_%04d.png -c:v libx264 -pix_fmt yuv420p walkthrough.mp4
# Export for YouTube (1920x1080, 8 Mbps)
ffmpeg -i walkthrough.mp4 -vf "scale=1920:1080" -b:v 8M youtube.mp4
```

**Quick routing:**
- Creating pipe geometry? See [Pipe Routing as Bezier Curves](#pipe-routing-as-bezier-curves-creat-02)
- Modeling equipment? See [Equipment as Parametric Meshes](#equipment-as-parametric-meshes-creat-02)
- Setting up materials? See [Infrastructure Materials](#infrastructure-materials-creat-02)
- Camera animation? See [Camera Paths](#camera-paths-creat-03)
- Flow/thermal animation? See [Infrastructure Animations](#infrastructure-animations-creat-01-creat-03)
- Video production? See [ffmpeg Assembly Pipeline](#ffmpeg-assembly-pipeline-creat-04-creat-05)

---

## Blender Scene Generation (CREAT-01)

### Scene Setup and Initialization

Every infrastructure visualization script begins with scene initialization:

```python
import bpy
import math

# ── Clear default scene ──────────────────────────────────────
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# ── Set units to metric (millimeters for infrastructure) ─────
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'MILLIMETERS'

# ── Set render engine ────────────────────────────────────────
# EEVEE for fast preview, Cycles for photorealistic final render
bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.cycles.samples = 128  # Preview: 128, Final: 256-512

# ── Set render resolution ────────────────────────────────────
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080
bpy.context.scene.render.resolution_percentage = 100

# ── Set output format ────────────────────────────────────────
bpy.context.scene.render.image_settings.file_format = 'PNG'
bpy.context.scene.render.filepath = '//renders/'  # Relative to .blend file
```

### Lighting Setup

Three standard lighting configurations for infrastructure visualization:

**Studio lighting (3-point):**
```python
# Key light — main illumination at 45 degrees
bpy.ops.object.light_add(type='AREA', location=(5, -5, 8))
key_light = bpy.context.active_object
key_light.name = "Key_Light"
key_light.data.energy = 1000  # Watts
key_light.data.size = 3.0  # Soft shadow (larger = softer)

# Fill light — reduce shadow harshness, opposite side at lower intensity
bpy.ops.object.light_add(type='AREA', location=(-4, -3, 5))
fill_light = bpy.context.active_object
fill_light.name = "Fill_Light"
fill_light.data.energy = 400  # 40% of key light

# Rim light — edge definition from behind
bpy.ops.object.light_add(type='AREA', location=(0, 6, 6))
rim_light = bpy.context.active_object
rim_light.name = "Rim_Light"
rim_light.data.energy = 600
```

**HDRI environment (realistic ambient):**
```python
# Load HDRI for realistic outdoor/sky lighting
world = bpy.context.scene.world
world.use_nodes = True
nodes = world.node_tree.nodes
links = world.node_tree.links
nodes.clear()

bg_node = nodes.new(type='ShaderNodeBackground')
env_node = nodes.new(type='ShaderNodeTexEnvironment')
output_node = nodes.new(type='ShaderNodeOutputWorld')

# Load HDRI file (download from polyhaven.com — free CC0)
env_node.image = bpy.data.images.load('//hdri/industrial_hall.hdr')
bg_node.inputs['Strength'].default_value = 1.0

links.new(env_node.outputs['Color'], bg_node.inputs['Color'])
links.new(bg_node.outputs['Background'], output_node.inputs['Surface'])
```

**Volumetric (for coolant flow visualization with god rays):**
```python
# Add volumetric scatter to world for atmospheric depth
vol_node = nodes.new(type='ShaderNodeVolumePrincipled')
vol_node.inputs['Density'].default_value = 0.01  # Subtle atmosphere
vol_node.inputs['Anisotropy'].default_value = 0.3  # Forward scattering
links.new(vol_node.outputs['Volume'], output_node.inputs['Volume'])
```

---

## Pipe Routing as Bezier Curves (CREAT-02)

### Creating Pipe Geometry

Pipes are modeled as Bezier curves with a circular bevel profile. The bevel_depth sets the pipe outer radius.

```python
# Create pipe as Bezier curve with circular cross-section
bpy.ops.curve.primitive_bezier_curve_add()
curve = bpy.context.active_object
curve.name = "CoolingPipe_Supply"

# Configure curve as 3D pipe
curve_data = curve.data
curve_data.dimensions = '3D'
curve_data.bevel_depth = 0.0445  # Outer radius in meters (3" NPS = 88.9mm OD)
curve_data.bevel_resolution = 8  # Smoothness of circular cross-section
curve_data.fill_mode = 'FULL'

# Set pipe route using spline control points
spline = curve_data.splines[0]
spline.bezier_points[0].co = (0, 0, 3.0)       # Start point (meters)
spline.bezier_points[1].co = (5.0, 0, 3.0)     # End point (meters)

# Handle positions control curve direction (tangent at each point)
spline.bezier_points[0].handle_left = (-0.5, 0, 3.0)
spline.bezier_points[0].handle_right = (1.0, 0, 3.0)
spline.bezier_points[1].handle_left = (4.0, 0, 3.0)
spline.bezier_points[1].handle_right = (5.5, 0, 3.0)
```

### Adding Direction Changes (Elbows)

For pipe direction changes, add intermediate Bezier points with handle angles:

```python
# Add a point for a 90-degree direction change (elbow)
spline.bezier_points.add(1)  # Now 3 points total

# Route: horizontal run -> 90-deg down -> vertical drop
spline.bezier_points[0].co = (0, 0, 3.0)        # Horizontal start
spline.bezier_points[1].co = (4.0, 0, 3.0)      # Corner (elbow location)
spline.bezier_points[2].co = (4.0, 0, 0.5)      # Vertical end (drops to 0.5m)

# Set handles at corner for sharp 90-degree turn
spline.bezier_points[1].handle_left = (3.5, 0, 3.0)   # Approach from left
spline.bezier_points[1].handle_right = (4.0, 0, 2.5)  # Exit downward

# Handle type: AUTO for smooth curves, FREE for precise control
for point in spline.bezier_points:
    point.handle_left_type = 'FREE'
    point.handle_right_type = 'FREE'
```

### NPS to Blender bevel_depth Conversion Table

The bevel_depth parameter is the pipe outer radius in meters (OD / 2):

| NPS (inch) | OD (mm) | OD (m) | bevel_depth (m) | Common Use |
|------------|---------|--------|-----------------|------------|
| 1/2" | 21.3 | 0.0213 | 0.0107 | Small branch lines |
| 3/4" | 26.7 | 0.0267 | 0.0134 | Residential supply |
| 1" | 33.4 | 0.0334 | 0.0167 | Branch distribution |
| 1-1/2" | 48.3 | 0.0483 | 0.0242 | Medium branch lines |
| 2" | 60.3 | 0.0603 | 0.0302 | CDU branch connections |
| 3" | 88.9 | 0.0889 | 0.0445 | Supply/return headers |
| 4" | 114.3 | 0.1143 | 0.0572 | Main distribution |
| 6" | 168.3 | 0.1683 | 0.0842 | Large distribution |
| 8" | 219.1 | 0.2191 | 0.1096 | Plant piping |
| 10" | 273.1 | 0.2731 | 0.1366 | Large plant piping |
| 12" | 323.8 | 0.3238 | 0.1619 | Municipal/plant mains |

### Multi-Pipe Routing

For parallel supply/return headers, offset the second pipe by the pipe OD plus insulation thickness:

```python
# Create return pipe offset from supply pipe
offset_y = 0.20  # 200mm center-to-center (3" pipe + insulation + clearance)

bpy.ops.curve.primitive_bezier_curve_add()
return_pipe = bpy.context.active_object
return_pipe.name = "CoolingPipe_Return"
return_pipe.data.dimensions = '3D'
return_pipe.data.bevel_depth = 0.0445  # Same size as supply

spline_return = return_pipe.data.splines[0]
spline_return.bezier_points[0].co = (0, offset_y, 3.0)
spline_return.bezier_points[1].co = (5.0, offset_y, 3.0)
```

---

## Equipment as Parametric Meshes (CREAT-02)

### Creating Equipment from Dimensions

Equipment is modeled as scaled cube primitives positioned at their design locations:

```python
# Create CDU enclosure (600mm x 800mm x 1800mm)
bpy.ops.mesh.primitive_cube_add(location=(2.0, 0, 0.9))  # Center at half-height
cdu = bpy.context.active_object
cdu.name = "CDU_101"
cdu.scale = (0.3, 0.4, 0.9)  # Half-extents in meters (600/2, 800/2, 1800/2)
bpy.ops.object.transform_apply(scale=True)  # Apply scale to mesh data

# Create server rack (42U: 600mm x 1000mm x 2000mm)
bpy.ops.mesh.primitive_cube_add(location=(2.0, 2.0, 1.0))
rack = bpy.context.active_object
rack.name = "Rack_A01"
rack.scale = (0.3, 0.5, 1.0)
bpy.ops.object.transform_apply(scale=True)
```

### Standard Equipment Dimensions for Data Center

Use these dimensions for parametric mesh generation:

| Equipment | W x D x H (mm) | Blender scale (x, y, z) | Notes |
|-----------|----------------|------------------------|-------|
| Server rack (42U) | 600 x 1000 x 2000 | (0.3, 0.5, 1.0) | Standard EIA-310-E |
| Server rack (48U) | 600 x 1200 x 2200 | (0.3, 0.6, 1.1) | Deep rack for GPU servers |
| CDU (small) | 600 x 800 x 1800 | (0.3, 0.4, 0.9) | 30-60 kW range |
| CDU (large) | 800 x 1200 x 2000 | (0.4, 0.6, 1.0) | 100+ kW range |
| UPS (100 kVA) | 800 x 1000 x 1900 | (0.4, 0.5, 0.95) | Floor-standing |
| UPS (500 kVA) | 1200 x 1000 x 2000 | (0.6, 0.5, 1.0) | Large frame |
| Floor PDU | 600 x 800 x 1800 | (0.3, 0.4, 0.9) | With transformer |
| Pump (centrifugal) | 500 x 800 x 600 | (0.25, 0.4, 0.3) | Horizontal base-mounted |
| Panel board | 400 x 200 x 600 | (0.2, 0.1, 0.3) | Wall-mounted |
| Transformer (dry) | 1000 x 800 x 1200 | (0.5, 0.4, 0.6) | 500-1000 kVA |
| Cable tray (section) | 300 x 100 x 3000 | (0.15, 0.05, 1.5) | 12" ladder type |

### Equipment Detail — Louvers and Airflow Indicators

Add visual detail to equipment faces to indicate airflow direction:

```python
# Add edge loops to front face for louver appearance
bpy.context.view_layer.objects.active = cdu
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.loopcut_slide(
    MESH_OT_loopcut={'number_cuts': 8, 'smoothness': 0},
    TRANSFORM_OT_edge_slide={'value': 0}
)
bpy.ops.object.mode_set(mode='OBJECT')
```

---

## Infrastructure Materials (CREAT-02)

### Material Overview

Seven PBR (Physically Based Rendering) materials cover common infrastructure components. All use the Principled BSDF shader node for physically correct rendering.

| Material | Base Color (RGB) | Metallic | Roughness | Special | Engineering Use |
|----------|-----------------|----------|-----------|---------|----------------|
| Copper pipe | (0.83, 0.48, 0.22) | 1.0 | 0.2 | — | ASTM B88 tubing, heat exchangers |
| PVC pipe | (0.9, 0.9, 0.88) | 0.0 | 0.85 | — | DWV piping, conduit |
| Brushed steel | (0.6, 0.6, 0.62) | 1.0 | 0.3 | — | ASTM A53 pipe, structural steel |
| Insulation | (0.72, 0.62, 0.35) | 0.0 | 1.0 | — | Fiberglass/mineral wool jacket |
| Coolant | (0.2, 0.5, 1.0) | 0.0 | 0.0 | IOR=1.33, transmission=0.8 | Chilled water, glycol visualization |
| Concrete | (0.5, 0.5, 0.5) | 0.0 | 0.95 | — | Slab, walls, raised floor |
| Cable tray | (0.75, 0.75, 0.72) | 0.8 | 0.4 | — | Galvanized steel per NEMA VE 1 |

### Material Assignment

```python
# Assign material to pipe object
mat = bpy.data.materials.get("Infra_CopperPipe")
if mat is None:
    # Create material if not already loaded from blender-materials.py
    mat = bpy.data.materials.new(name="Infra_CopperPipe")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get('Principled BSDF')
    bsdf.inputs['Base Color'].default_value = (0.83, 0.48, 0.22, 1.0)
    bsdf.inputs['Metallic'].default_value = 1.0
    bsdf.inputs['Roughness'].default_value = 0.2

# Assign to object
pipe_obj = bpy.data.objects['CoolingPipe_Supply']
if pipe_obj.data.materials:
    pipe_obj.data.materials[0] = mat
else:
    pipe_obj.data.materials.append(mat)
```

**Full material setup scripts:** All 7 materials with complete Principled BSDF configuration, helper functions, and engineering context are available in `@references/blender-materials.py`. Paste the entire script into Blender's Scripting workspace and run to create all materials at once.

---

## Camera Paths (CREAT-03)

### Orbital Overview Camera

Camera orbits the scene center on a circular path — best for showing overall system layout:

```python
import math

# Create camera
bpy.ops.object.camera_add(location=(0, -10, 5))
camera = bpy.context.active_object
camera.name = "Camera_Orbital"
bpy.context.scene.camera = camera  # Set as active camera

# Create circular orbit path
bpy.ops.curve.primitive_bezier_circle_add(radius=10, location=(0, 0, 3))
orbit_path = bpy.context.active_object
orbit_path.name = "Camera_Orbit_Path"

# Add Follow Path constraint to camera
constraint = camera.constraints.new(type='FOLLOW_PATH')
constraint.target = orbit_path
constraint.use_fixed_location = False
constraint.forward_axis = 'TRACK_NEGATIVE_Z'
constraint.up_axis = 'UP_Y'

# Add Track To constraint (camera always looks at scene center)
track = camera.constraints.new(type='TRACK_TO')
track.target = bpy.data.objects.get('CDU_101')  # Or create an empty at center
track.track_axis = 'TRACK_NEGATIVE_Z'
track.up_axis = 'UP_Y'

# Set animation timeline
orbit_path.data.path_duration = 250  # 10 seconds at 25 fps
bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = 250

# Animate path evaluation
orbit_path.data.eval_time = 0
orbit_path.data.keyframe_insert('eval_time', frame=1)
orbit_path.data.eval_time = 250
orbit_path.data.keyframe_insert('eval_time', frame=250)
```

### Linear Walkthrough Camera

Camera moves along a straight path through the facility at eye level — best for showing hot/cold aisle layout:

```python
# Create walkthrough path (straight line through data hall)
bpy.ops.curve.primitive_bezier_curve_add()
walk_path = bpy.context.active_object
walk_path.name = "Camera_Walk_Path"
walk_path.data.dimensions = '3D'

spline = walk_path.data.splines[0]
spline.bezier_points[0].co = (0, -8, 1.7)   # Start: entrance at eye level (1.7m)
spline.bezier_points[1].co = (0, 12, 1.7)   # End: far side of data hall

# Smooth handles for gentle camera motion
spline.bezier_points[0].handle_right = (0, -4, 1.7)
spline.bezier_points[1].handle_left = (0, 8, 1.7)

# Create camera and attach to path
bpy.ops.object.camera_add()
walk_cam = bpy.context.active_object
walk_cam.name = "Camera_Walkthrough"

constraint = walk_cam.constraints.new(type='FOLLOW_PATH')
constraint.target = walk_path
constraint.forward_axis = 'FORWARD_Y'
constraint.up_axis = 'UP_Z'

# Animate over 15 seconds (375 frames at 25 fps)
walk_path.data.path_duration = 375
bpy.context.scene.frame_end = 375
walk_path.data.eval_time = 0
walk_path.data.keyframe_insert('eval_time', frame=1)
walk_path.data.eval_time = 375
walk_path.data.keyframe_insert('eval_time', frame=375)
```

### Detail Zoom Camera

Camera starts at overview distance and animates to focus on a specific component — best for highlighting equipment:

```python
# Create zoom path from far to close
bpy.ops.curve.primitive_bezier_curve_add()
zoom_path = bpy.context.active_object
zoom_path.name = "Camera_Zoom_Path"
zoom_path.data.dimensions = '3D'

target_pos = (2.0, 0, 0.9)  # CDU center position

spline = zoom_path.data.splines[0]
spline.bezier_points[0].co = (10, -8, 6)      # Start: overview (far, high)
spline.bezier_points[1].co = (3.0, -1.5, 1.2) # End: detail (close, eye level)

# Create camera with Track To constraint aimed at equipment
bpy.ops.object.camera_add()
zoom_cam = bpy.context.active_object
zoom_cam.name = "Camera_DetailZoom"

path_constraint = zoom_cam.constraints.new(type='FOLLOW_PATH')
path_constraint.target = zoom_path

track_constraint = zoom_cam.constraints.new(type='TRACK_TO')
target_empty = bpy.data.objects.new("Zoom_Target", None)
bpy.context.collection.objects.link(target_empty)
target_empty.location = target_pos
track_constraint.target = target_empty
track_constraint.track_axis = 'TRACK_NEGATIVE_Z'
track_constraint.up_axis = 'UP_Y'

# Animate over 5 seconds with ease-in/ease-out
zoom_path.data.path_duration = 125  # 5 sec at 25 fps
bpy.context.scene.frame_end = 125
```

### Camera Path Summary

| Path Type | Use Case | Duration | Camera Height | Orbit Radius |
|-----------|----------|----------|---------------|-------------|
| Orbital overview | Full system layout | 8-12 sec | 3-5m above center | 10-20m (scene dependent) |
| Linear walkthrough | Hot/cold aisle tour | 12-20 sec | 1.7m (eye level) | N/A (straight line) |
| Detail zoom | Equipment spotlight | 4-8 sec | Starts high, ends eye-level | N/A (linear approach) |

---

## Infrastructure Animations (CREAT-01, CREAT-03)

### Coolant Flow Animation (Particle System)

Particles follow the pipe curve path to visualize fluid flow:

```python
# Get the supply pipe curve object
pipe_obj = bpy.data.objects['CoolingPipe_Supply']

# Convert curve to mesh temporarily for particle emission
# (Particles emit from mesh faces, not curve surfaces)
bpy.context.view_layer.objects.active = pipe_obj
bpy.ops.object.convert(target='MESH', keep_original=True)
pipe_mesh = bpy.context.active_object
pipe_mesh.name = "CoolingPipe_Supply_Mesh"

# Create small sphere for coolant droplet visualization
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.01, location=(0, 0, -10))
droplet = bpy.context.active_object
droplet.name = "Coolant_Droplet"

# Assign coolant material to droplet
coolant_mat = bpy.data.materials.get("Infra_Coolant")
if coolant_mat:
    droplet.data.materials.append(coolant_mat)

# Add particle system to pipe mesh
bpy.context.view_layer.objects.active = pipe_mesh
bpy.ops.object.particle_system_add()
ps = pipe_mesh.particle_systems[0]
ps_settings = ps.settings

ps_settings.count = 200           # Number of particles (more = denser flow)
ps_settings.lifetime = 80         # Frames each particle lives
ps_settings.emit_from = 'FACE'    # Emit from pipe surface
ps_settings.render_type = 'OBJECT'
ps_settings.instance_object = droplet
ps_settings.particle_size = 1.0
ps_settings.size_random = 0.2     # Slight size variation for realism

# Set velocity along pipe normal (simulates flow direction)
ps_settings.normal_factor = 0.5   # Speed along surface normal
ps_settings.factor_random = 0.1   # Slight randomness
```

### Electrical Current Animation (Emissive Pulse)

Animate emission strength along a conductor to simulate current flow:

```python
# Create or get copper conductor material with emission node
mat = bpy.data.materials.new(name="Copper_Conductor_Animated")
mat.use_nodes = True
nodes = mat.node_tree.nodes
links = mat.node_tree.links
nodes.clear()

# Principled BSDF for base appearance
output = nodes.new(type='ShaderNodeOutputMaterial')
output.location = (600, 0)

bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
bsdf.location = (0, 0)
bsdf.inputs['Base Color'].default_value = (0.83, 0.48, 0.22, 1.0)
bsdf.inputs['Metallic'].default_value = 1.0
bsdf.inputs['Roughness'].default_value = 0.2

# Add emission for glow effect
bsdf.inputs['Emission Color'].default_value = (1.0, 0.8, 0.2, 1.0)  # Warm yellow
bsdf.inputs['Emission Strength'].default_value = 0

links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

# Animate emission strength: off -> bright -> off (pulse effect)
bpy.context.scene.frame_set(1)
bsdf.inputs['Emission Strength'].default_value = 0
bsdf.inputs['Emission Strength'].keyframe_insert('default_value', frame=1)

bpy.context.scene.frame_set(15)
bsdf.inputs['Emission Strength'].default_value = 10  # Peak brightness
bsdf.inputs['Emission Strength'].keyframe_insert('default_value', frame=15)

bpy.context.scene.frame_set(30)
bsdf.inputs['Emission Strength'].default_value = 0
bsdf.inputs['Emission Strength'].keyframe_insert('default_value', frame=30)

# For repeating pulse: set keyframe extrapolation to cycle
# (requires Graph Editor > Channel > Extrapolation Mode > Make Cyclic)
```

### Thermal Mapping Animation (Color Ramp from Temperature Data)

Color-code surfaces by temperature using a custom attribute driven by calculation data:

```python
# Create thermal visualization material
mat_thermal = bpy.data.materials.new(name="Thermal_Mapping")
mat_thermal.use_nodes = True
nodes = mat_thermal.node_tree.nodes
links = mat_thermal.node_tree.links
nodes.clear()

output = nodes.new(type='ShaderNodeOutputMaterial')
output.location = (800, 0)

bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
bsdf.location = (400, 0)

# Color ramp: blue (cold) -> green -> yellow -> red (hot)
color_ramp = nodes.new(type='ShaderNodeValToRGB')
color_ramp.location = (0, 0)
color_ramp.color_ramp.elements[0].position = 0.0
color_ramp.color_ramp.elements[0].color = (0.0, 0.0, 1.0, 1.0)  # Blue (cold)
color_ramp.color_ramp.elements.new(0.33)
color_ramp.color_ramp.elements[1].color = (0.0, 1.0, 0.0, 1.0)  # Green
color_ramp.color_ramp.elements.new(0.66)
color_ramp.color_ramp.elements[2].color = (1.0, 1.0, 0.0, 1.0)  # Yellow
color_ramp.color_ramp.elements[3].position = 1.0
color_ramp.color_ramp.elements[3].color = (1.0, 0.0, 0.0, 1.0)  # Red (hot)

# Attribute node to read temperature values from mesh custom attribute
attr_node = nodes.new(type='ShaderNodeAttribute')
attr_node.location = (-200, 0)
attr_node.attribute_name = "temperature"  # Custom per-vertex attribute

links.new(attr_node.outputs['Fac'], color_ramp.inputs['Fac'])
links.new(color_ramp.outputs['Color'], bsdf.inputs['Base Color'])
links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

# To apply temperature data to vertices:
# mesh.attributes.new(name='temperature', type='FLOAT', domain='POINT')
# mesh.attributes['temperature'].data[vertex_index].value = normalized_temp (0-1)
```

### Animation Summary

| Animation | Technique | Visual Effect | Frame Count |
|-----------|-----------|--------------|-------------|
| Coolant flow | Particle system on pipe mesh | Blue spheres flowing through pipes | 200-500 (8-20s) |
| Electrical current | Emissive keyframe animation | Glowing pulse along conductors | 60-150 (2-6s per cycle) |
| Thermal mapping | Color ramp + vertex attribute | Blue-to-red heat map on surfaces | Static or animated over time |

---

## ffmpeg Assembly Pipeline (CREAT-04, CREAT-05)

### Step 1: Assemble Rendered Frames into Base Video

After rendering animation frames from Blender (File > Render > Render Animation), assemble into video:

```bash
# Assemble PNG frames into H.264 video
# -framerate: must match Blender render settings (25 or 30 fps)
# -crf 18: visually lossless quality (lower = better, 0 = lossless, 23 = default)
ffmpeg -framerate 30 -i render_%04d.png \
    -c:v libx264 \
    -preset slow \
    -crf 18 \
    -pix_fmt yuv420p \
    walkthrough.mp4
```

### Step 2: Add Narration Audio (Optional)

```bash
# Combine video with narration audio track
ffmpeg -i walkthrough.mp4 -i narration.mp3 \
    -c:v copy \
    -c:a aac \
    -b:a 192k \
    -shortest \
    final.mp4
```

### Step 3: Social Media Exports

Four export presets for common platforms (full scripts in `@references/ffmpeg-presets.sh`):

**YouTube (16:9, 1920x1080, H.264):**
```bash
ffmpeg -i final.mp4 \
    -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" \
    -c:v libx264 -preset slow -crf 18 -b:v 8M -maxrate 10M -bufsize 20M \
    -pix_fmt yuv420p -c:a aac -b:a 192k \
    youtube_export.mp4
```

**Instagram Reel (9:16 portrait, 1080x1920):**
```bash
ffmpeg -i final.mp4 \
    -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=black" \
    -c:v libx264 -preset medium -crf 23 -b:v 3.5M \
    -pix_fmt yuv420p -c:a aac -b:a 128k -t 60 \
    instagram_reel.mp4
```

**Twitter/X (16:9, 1280x720, max 2:20):**
```bash
ffmpeg -i final.mp4 \
    -vf "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2" \
    -c:v libx264 -preset medium -crf 23 -b:v 5M \
    -pix_fmt yuv420p -c:a aac -b:a 128k -t 140 \
    twitter_export.mp4
```

**Thumbnail (JPEG still frame, 1280x720):**
```bash
# Extract a single frame at 5-second mark
ffmpeg -i final.mp4 \
    -ss 00:00:05 \
    -frames:v 1 \
    -vf "scale=1280:720" \
    -q:v 2 \
    thumbnail.jpg
```

### Social Media Format Summary

| Platform | Resolution | Aspect Ratio | Max Duration | Bitrate | Codec |
|----------|-----------|-------------|-------------|---------|-------|
| YouTube | 1920x1080 | 16:9 | Unlimited | 8 Mbps | H.264 |
| Instagram Reel | 1080x1920 | 9:16 | 60s (feed) / 90s (reel) | 3.5 Mbps | H.264 |
| Twitter/X | 1280x720 | 16:9 | 2:20 | 5 Mbps | H.264 |
| Thumbnail | 1280x720 | 16:9 | N/A (still) | N/A | JPEG |
| LinkedIn | 1920x1080 | 16:9 | 10 min | 8 Mbps | H.264 |

### Render Settings Recommendations

| Use Case | Render Engine | Samples | Resolution | Est. Time/Frame | Notes |
|----------|-------------|---------|------------|------------------|-------|
| Preview | EEVEE | N/A | 1280x720 | ~1s | Real-time preview, good for iteration |
| Draft | Cycles | 64 | 1920x1080 | ~15s | Noisy but compositionally correct |
| Final | Cycles | 256 | 1920x1080 | ~60s | Production quality |
| Thumbnail | Cycles | 512 | 2560x1440 | ~120s | High quality for downsampling |

---

## Deep Reference

### Complex Multi-Pipe Systems

For systems with many pipes (supply, return, condensate, makeup water), organize by system and color-code:

```python
# System color convention (matching ASME A13.1 pipe identification)
PIPE_SYSTEMS = {
    'chilled_water_supply': {'color': (0.0, 0.5, 1.0, 1.0), 'label': 'CWS'},
    'chilled_water_return': {'color': (0.0, 0.8, 0.3, 1.0), 'label': 'CWR'},
    'condenser_supply':     {'color': (1.0, 0.6, 0.0, 1.0), 'label': 'CS'},
    'condenser_return':     {'color': (1.0, 0.3, 0.0, 1.0), 'label': 'CR'},
    'condensate_drain':     {'color': (0.5, 0.5, 0.5, 1.0), 'label': 'CD'},
}

def create_pipe_material(system_name):
    config = PIPE_SYSTEMS[system_name]
    mat = bpy.data.materials.new(name=f"Pipe_{config['label']}")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get('Principled BSDF')
    bsdf.inputs['Base Color'].default_value = config['color']
    bsdf.inputs['Metallic'].default_value = 0.5
    bsdf.inputs['Roughness'].default_value = 0.4
    return mat
```

### Advanced PBR Materials (Bump Maps and Displacement)

For photorealistic concrete and insulation surfaces, add procedural bump mapping:

```python
# Concrete with procedural bump texture
mat = bpy.data.materials.get("Infra_Concrete")
nodes = mat.node_tree.nodes
links = mat.node_tree.links

# Add noise texture for surface irregularity
noise = nodes.new(type='ShaderNodeTexNoise')
noise.inputs['Scale'].default_value = 50.0
noise.inputs['Detail'].default_value = 6.0
noise.inputs['Roughness'].default_value = 0.6

# Add bump node to convert texture to normal perturbation
bump = nodes.new(type='ShaderNodeBump')
bump.inputs['Strength'].default_value = 0.3  # Subtle bump
bump.inputs['Distance'].default_value = 0.001

bsdf = nodes.get('Principled BSDF')
links.new(noise.outputs['Fac'], bump.inputs['Height'])
links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
```

### Camera Rig for Automated Pan-and-Scan

For large data halls requiring multiple camera angles:

```python
# Define camera waypoints (x, y, z, look_at_x, look_at_y, look_at_z)
WAYPOINTS = [
    (0, -10, 5, 0, 0, 2),      # Overview from entrance
    (0, 0, 1.7, 3, 0, 1),      # Aisle view looking at rack row
    (3, 0, 1.2, 3, 0, 0.9),    # CDU detail
    (0, 5, 1.7, -3, 5, 1),     # Opposite aisle
    (0, 10, 5, 0, 5, 2),       # Overview from far end
]

# Calculate total frames (5 seconds per segment)
fps = 25
seconds_per_segment = 5
total_frames = len(WAYPOINTS) * fps * seconds_per_segment
```

### ACES Color Management

For physically correct HDR rendering with proper color space:

```python
# Set color management to ACES (if available in Blender build)
bpy.context.scene.display_settings.display_device = 'sRGB'
bpy.context.scene.view_settings.view_transform = 'Filmic'  # Or 'AgX' in Blender 4.x
bpy.context.scene.view_settings.look = 'High Contrast'
bpy.context.scene.view_settings.exposure = 0.0
bpy.context.scene.view_settings.gamma = 1.0
```

### Geometry Nodes for Parametric Rack Arrays

For generating rows of identical racks automatically:

```python
# Instance racks along a line using Array modifier
rack_template = bpy.data.objects['Rack_A01']
array_mod = rack_template.modifiers.new(name="Row_Array", type='ARRAY')
array_mod.count = 10  # 10 racks per row
array_mod.relative_offset_displace = (0, 1.2, 0)  # 1.2m pitch (600mm rack + 600mm aisle)
array_mod.use_relative_offset = True
```

### Batch Rendering Script

For rendering all camera angles and animation sequences:

```python
# Render all camera paths sequentially
cameras = ['Camera_Orbital', 'Camera_Walkthrough', 'Camera_DetailZoom']

for cam_name in cameras:
    camera = bpy.data.objects.get(cam_name)
    if camera:
        bpy.context.scene.camera = camera
        bpy.context.scene.render.filepath = f'//renders/{cam_name}/'
        bpy.ops.render.render(animation=True)
        print(f"Rendered: {cam_name}")
```

### Output Passes for Compositing

Configure render passes for post-processing and compositing:

```python
# Enable useful render passes
view_layer = bpy.context.scene.view_layers[0]
view_layer.use_pass_diffuse_color = True
view_layer.use_pass_glossy_color = True
view_layer.use_pass_emit = True
view_layer.use_pass_ambient_occlusion = True
view_layer.use_pass_z = True  # Depth pass for DOF in compositing

# Enable denoising (Cycles only)
bpy.context.scene.cycles.use_denoising = True
bpy.context.scene.cycles.denoiser = 'OPENIMAGEDENOISE'
```

---

## Reference Files

| Reference | Purpose | Usage |
|-----------|---------|-------|
| @references/blender-materials.py | All 7 infrastructure materials as ready-to-paste bpy script | Paste into Blender Scripting workspace and run |
| @references/ffmpeg-presets.sh | All 4 social media export commands as bash functions | Source the file or copy individual commands |

---
*Creative Pipeline Skill v1.0.0 — Physical Infrastructure Engineering Pack*
*Phase 440-02 | References: Blender bpy API, ffmpeg, ASME A13.1 (pipe identification)*
*This skill generates visualization scripts only — no engineering decisions are made.*
