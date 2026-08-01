---
name: build123d
description: 'CAD modeling with build123d Python library. Use when creating 3D models,
  exporting to GLB/STEP/STL, or doing boolean operations (union, difference, intersection).
  Triggers on: CAD, 3D modeling, sphere'
---

---
name: build123d
description: CAD modeling with build123d Python library. Use when creating 3D models, exporting to GLB/STEP/STL, or doing boolean operations (union, difference, intersection). Triggers on: CAD, 3D modeling, sphere, box, cylinder, mesh export, GLB, STEP, STL, solid modeling, parametric design, threads, fasteners, bolts, nuts, screws, gears, pipes, flanges, bearings, bd_warehouse, spur gear, helical gear, bevel gear, planetary gear, ring gear, cycloid gear, rack and pinion, gggears, herringbone, gear mesh, gear train.
---

# build123d CAD Modeling

## Zero-Setup with uv

No installation required. Run any build123d script with:

```bash
uvx --from build123d python script.py
```

This automatically downloads build123d and runs your script. First run takes ~30s, subsequent runs are instant.

**Install uv** (if not already installed):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Critical: Imports

All exports are in the **main module**:

```python
from build123d import Sphere, Box, Cylinder, export_gltf, export_step, export_stl
```

**NEVER** use `from build123d.exporters import ...` - this module does not exist.

## Quick Start Example

```python
#!/usr/bin/env python3
from build123d import Sphere, Box, export_gltf, Pos

# Create shapes
sphere = Sphere(radius=20)
box = Pos(15, 0, 0) * Box(10, 10, 10)

# Boolean union
result = sphere + box

# Export to GLB (for web viewers, Three.js)
export_gltf(result, "./model.glb", binary=True)
print("Exported model.glb")
```

Run it:
```bash
uvx --from build123d python my_model.py
```

## Geometry Inspection (Optional)

To inspect geometry properties, add this to your script:

```python
def inspect(shape):
    bbox = shape.bounding_box()
    print(f"Size: {bbox.max.X - bbox.min.X:.1f} x {bbox.max.Y - bbox.min.Y:.1f} x {bbox.max.Z - bbox.min.Z:.1f}")
    print(f"Volume: {shape.volume:.1f}")
    print(f"Faces: {len(shape.faces())}, Edges: {len(shape.edges())}")

inspect(result)
```

A full inspection harness is available in `scripts/harness.py` for advanced use.

## Quick Reference

### Shapes
```python
Box(length, width, height)
Sphere(radius=20)
Cylinder(radius=10, height=25)
Cone(bottom_radius=15, top_radius=5, height=20)
Torus(major_radius=20, minor_radius=5)
```

### Boolean Operations
```python
union = shape1 + shape2           # Fuse
difference = shape1 - shape2      # Cut
intersection = shape1 & shape2    # Common volume
```

### Positioning
```python
from build123d import Pos, Rot
moved = Pos(x, y, z) * shape      # Translate
rotated = Rot(rx, ry, rz) * shape # Rotate (degrees)
```

### Export
```python
export_gltf(shape, "./out.glb", binary=True)  # GLB for web
export_step(shape, "./out.step")              # CAD interchange
export_stl(shape, "./out.stl")                # 3D printing
```

## Examples by Capability

21 runnable examples in `references/examples/`:

### Basics (01-08)
- `01_simple_shapes.py` - Box, Sphere, Cylinder, Cone, Torus
- `02_boolean_operations.py` - Union (+), difference (-), intersection (&)
- `03_export_formats.py` - GLB, STEP, STL, BREP export
- `04_positioning.py` - Pos(), Rot() transforms
- `05_sketch_extrude.py` - 2D sketch to 3D solid
- `06_fillet_chamfer.py` - Edge rounding and beveling
- `07_csg_classic.py` - Classic CSG operations
- `08_hole_pattern.py` - GridLocations for hole patterns

### 3D Operations
- `loft.py` - Connect multiple profiles
- `vase.py` - **Revolve** + edge filtering + shelling
- `tea_cup.py` - Revolve + **sweep** for handle

### Advanced Techniques
- `roller_coaster.py` - **Helix** + Spline curves
- `packed_boxes.py` - **pack()** algorithm
- `toy_truck.py` - **Joints** for assembly
- `dual_color_3mf.py` - Multi-color 3MF export

Run any example:
```bash
uvx --from build123d python references/examples/01_simple_shapes.py
```

## Advanced Patterns

For builder mode, edge filtering, loft, sweep, revolve:
See `references/advanced-patterns.md`

## bd_warehouse - Parametric Parts Library

For threads, fasteners, simple gears, pipes, flanges, and bearings: See `references/bd-warehouse-reference.md`

```bash
uvx --from build123d --with bd_warehouse python script.py
```

Examples: `09_bd_warehouse_threads.py` through `14_bd_warehouse_bearings.py`

## gggears - Advanced Gear Generation

For advanced parametric gears (spur, helical, bevel, planetary, cycloid, racks): See `references/gggears-reference.md`

```bash
uvx --from build123d --with "gggears @ git+https://github.com/GarryBGoode/gggears" python script.py
```

Examples: `15_gggears_spur.py` through `20_gggears_rack.py`

**Quick example:**
```python
from gggears import SpurGear, UP
from build123d import export_gltf

gear1 = SpurGear(number_of_teeth=12, module=2.0, height=10.0)
gear2 = SpurGear(number_of_teeth=24, module=2.0, height=10.0)
gear1.mesh_to(gear2, target_dir=UP)

assembly = gear1.build_part() + gear2.build_part()
export_gltf(assembly, "./gears.glb", binary=True)
```

## Post-Processing Pipeline

After exporting GLB, you can optimize and verify:

```bash
# 1. Optimize for web delivery (optional)
bunx @gltf-transform/cli optimize model.glb optimized.glb --compress draco

# 2. Render to image for visual verification
bunx render-glb model.glb preview.png
```

See the **gltf-transform** and **render-glb** plugins for full documentation.

## Source Repositories

- **build123d**: https://github.com/gumyr/build123d
- **bd_warehouse**: https://github.com/gumyr/bd_warehouse
- **gggears**: https://github.com/GarryBGoode/gggears
- **render-glb**: https://github.com/rawwerks/render-glb
