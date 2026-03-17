---
name: build123d
description: This skill should be used when the user asks to "create a 3D model with build123d", "design parametric parts", "use builder mode", "use algebra mode", "select faces or edges", "export STEP or STL", or works with build123d CAD programming.
compatibility: opencode
license: Apache-2.0
metadata:
  category: cad
  version: 1.0.0
---

# build123d Development

## When to Use This Skill

### Primary Triggers (Explicit)

Use this skill when the user says:

- "create a 3D model with build123d"
- "design a parametric part in build123d"
- "use builder mode in build123d"
- "use algebra mode in build123d"
- "select faces/edges/vertices in build123d"
- "export to STEP/STL/DXF"
- "work with build123d"

### Contextual Triggers (Implicit)

Use this skill when:

- Working with Python CAD programming
- Creating parametric 3D models
- Developing mechanical parts or assemblies
- Need to manipulate geometric shapes programmatically
- Working with boundary representation (BREP) modeling

## Overview

build123d is a Python-based parametric CAD library built on OpenCascade. It provides two distinct programming modes:

1. **Algebra Mode** - Stateless, explicit object manipulation using operators
2. **Builder Mode** - Stateful contexts with implicit state tracking

**Core principle:** Choose the mode that matches the modeling pattern. Use Algebra Mode for simple, direct construction. Use Builder Mode for complex, context-aware workflows.

## Quick Reference

### Import Pattern

```python
from build123d import *
```

Note: While wildcard imports are generally discouraged, build123d scripts are typically self-contained and this is the standard pattern.

### Common Objects by Dimension

| Dimension | Objects | Operations |
|-----------|---------|------------|
| **1D** | Line, Arc, Spline, Helix, Bezier | add(), offset(), mirror(), split() |
| **2D** | Circle, Rectangle, Polygon, Ellipse | fillet(), chamfer(), offset(), extrude() |
| **3D** | Box, Cylinder, Sphere, Cone, Torus | fillet(), chamfer(), loft(), revolve() |

### Mode Comparison

| Aspect | Algebra Mode | Builder Mode |
|--------|--------------|--------------|
| **State** | Stateless | Stateful contexts |
| **Syntax** | `obj += part` | `with BuildPart():` |
| **Objects** | Explicit tracking | Implicit tracking |
| **Locations** | Manual transforms | Context-aware |
| **Best for** | Simple models | Complex workflows |

For detailed comparison, see `references/mode-comparison.md`.

## Algebra Mode Fundamentals

### Basic Pattern

```python
from build123d import *

# Create objects explicitly
sketch = Circle(5)
sketch -= Pos(2, 0) * Circle(1)

# Extrude to 3D
part = extrude(sketch, amount=10)

# Modify with operators
part += Pos(0, 0, 10) * Cylinder(3, 5)
```

### Key Operators

- `+=` - Add/union
- `-=` - Subtract/difference
- `*` - Transform (Location * Shape)
- `@` - Position along Edge/Wire (0.0 to 1.0)
- `%` - Tangent along Edge/Wire (0.0 to 1.0)
- `^` - Location along Edge/Wire (0.0 to 1.0)

### Selectors

Access shape topology with selectors that return ShapeLists:

```python
# Get all faces
faces = part.faces()

# Filter by property
top_face = part.faces().sort_by(Axis.Z)[-1]

# Group and select
cylinders = part.faces().filter_by(GeomType.CYLINDER)

# Chain operations
edges = part.edges().filter_by(lambda e: e.length > 5).sort_by(Axis.X)
```

## Builder Mode Fundamentals

### Context Structure

```python
from build123d import *

with BuildPart() as part_context:
    # 2D sketch on current plane
    with BuildSketch() as sketch:
        Rectangle(10, 10)
        with Locations((3, 3)):
            Circle(2, mode=Mode.SUBTRACT)
    
    # Extrude pending sketch
    extrude(amount=5)
    
    # Operations on pending objects
    fillet(edges().filter_by(Axis.Z), radius=0.5)

# Access result
final_part = part_context.part
```

### Context Types

- `BuildLine` - 1D curves and wires
- `BuildSketch` - 2D faces and sketches  
- `BuildPart` - 3D solids and parts
- `Locations` - Position multiple objects
- `GridLocations`, `PolarLocations`, `HexLocations` - Pattern locations

### Mode Parameter

Control how objects combine with context:

```python
Circle(5, mode=Mode.ADD)       # Union (default)
Circle(2, mode=Mode.SUBTRACT)  # Difference
Circle(3, mode=Mode.INTERSECT) # Intersection
Circle(4, mode=Mode.REPLACE)   # Replace all
Circle(1, mode=Mode.PRIVATE)   # Create but don't add
```

## Selectors and Filtering

Selectors return ShapeLists with powerful filtering methods:

```python
# Basic selectors
vertices = part.vertices()
edges = part.edges()
faces = part.faces()
solids = part.solids()

# Filter by geometry type
circles = faces.filter_by(GeomType.CIRCLE)
planes = faces.filter_by(GeomType.PLANE)

# Filter by property
long_edges = edges.filter_by(lambda e: e.length > 10)
large_faces = faces.filter_by(lambda f: f.area > 50)

# Sort by axis/property
sorted_faces = faces.sort_by(Axis.Z)
by_area = faces.sort_by(Face.area)

# Group by property
grouped = faces.group_by(Axis.Z)
top_group = grouped[-1]  # Highest Z group
bottom_group = grouped[0]  # Lowest Z group

# Operators for filtering
top_faces = faces >> Axis.Z      # Group by Z, get max
bottom_faces = faces << Axis.Z   # Group by Z, get min
max_faces = faces > Axis.Z       # Sort by Z, ascending
min_faces = faces < Axis.Z       # Sort by Z, descending
planar = faces | GeomType.PLANE  # Filter by type
```

## Common Operations

### 2D to 3D Conversion

```python
# Extrude
solid = extrude(sketch, amount=10)
solid = extrude(sketch, amount=10, both=True)  # Both directions
solid = extrude(sketch, amount=10, taper=5)    # Tapered

# Revolve
solid = revolve(sketch, axis=Axis.X, angle=360)

# Loft between profiles
solid = loft([sketch1, sketch2, sketch3])

# Sweep along path
solid = sweep(profile, path)
```

### Filleting and Chamfering

```python
# Fillet edges
part = fillet(part.edges().filter_by(Axis.Z), radius=1)

# Chamfer edges
part = chamfer(part.edges(), length=0.5)

# Full round (creates tangent blend)
sketch = full_round(sketch.edges(), radius=2)
```

### Boolean Operations (Algebra Mode)

```python
# Union
result = part1 + part2

# Difference
result = part1 - part2

# Intersection  
result = part1 & part2
```

## Positioning and Transformation

### Locations

```python
# Create locations
loc = Pos(10, 0, 5)              # Position
loc = Rot(45, 0, 0)              # Rotation
loc = Pos(10, 5) * Rot(45)       # Combined

# Apply to shapes
moved = loc * Circle(5)

# Planes for positioning
plane = Plane.XY                 # Standard planes
plane = Plane.XZ * Pos(10, 0, 0) # Offset plane
```

### Location Contexts (Builder Mode)

```python
with BuildPart():
    with Locations((0, 0, 0), (10, 0, 0), (0, 10, 0)):
        Cylinder(2, 10)  # Creates 3 cylinders
    
    with GridLocations(5, 5, 4, 4):
        Hole(1)  # Creates 4x4 grid of holes
    
    with PolarLocations(radius=10, count=6):
        Box(2, 2, 5)  # Creates 6 boxes in circle
```

## Data Import/Export

### Export Formats

```python
# STEP (CAD interchange)
export_step(part, "model.step")

# STL (3D printing)
export_stl(part, "model.stl")
export_stl(part, "model.stl", tolerance=0.01)  # Higher quality

# DXF (2D drawings)
export_dxf(sketch, "profile.dxf")

# SVG (2D graphics)
export_svg(sketch, "outline.svg")
```

### Import Formats

```python
# Import STEP
imported = import_step("existing.step")

# Import SVG (creates 2D sketch)
svg_sketch = import_svg("logo.svg")

# Import DXF
dxf_sketch = import_dxf("profile.dxf")
```

## Extending with Custom Objects

Create reusable parametric objects:

```python
class CustomBracket(BasePartObject):
    def __init__(
        self,
        width: float,
        height: float,
        thickness: float,
        hole_dia: float,
        mode: Mode = Mode.ADD,
    ):
        with BuildPart() as bracket:
            with BuildSketch():
                Rectangle(width, height)
            extrude(amount=thickness)
            
            with Locations(Plane.XY.offset(thickness)):
                with GridLocations(width-10, height-10, 2, 2):
                    CounterSinkHole(hole_dia, hole_dia*1.5)
        
        super().__init__(part=bracket.part, mode=mode)

# Use custom object
part = CustomBracket(50, 30, 5, 4)
```

## Common Patterns

### Parametric Design

```python
def create_gear(teeth: int, module: float, thickness: float):
    """Create parametric gear"""
    pitch_radius = teeth * module / 2
    
    with BuildPart() as gear:
        with BuildSketch():
            Circle(pitch_radius)
        extrude(amount=thickness)
    
    return gear.part
```

### Alignment Control

Most objects support `align` parameter:

```python
# Align to center
Rectangle(10, 5, align=(Align.CENTER, Align.CENTER))

# Align to min corner
Box(10, 10, 10, align=(Align.MIN, Align.MIN, Align.MIN))

# Mixed alignment
Cylinder(5, 10, align=(Align.CENTER, Align.CENTER, Align.MIN))
```

### Working with Assemblies

```python
from build123d import *

# Create assembly
assy = Assembly()

# Add parts with positions
assy.add(base_part, name="base")
assy.add(arm_part, name="arm", loc=Pos(10, 0, 20) * Rot(0, 45, 0))

# Access parts
base = assy["base"]
arm = assy["arm"]
```

## Debugging and Visualization

### Interactive Development

Use ocp_vscode for live visualization:

1. Install: `pip install ocp-vscode`
2. In VS Code, install "OCP CAD Viewer" extension
3. Use `show()` or `show_object()` to display shapes

```python
from build123d import *
from ocp_vscode import show

part = Box(10, 10, 10)
show(part)  # Displays in viewer
```

### Inspection

```python
# Get properties
print(f"Volume: {part.volume}")
print(f"Area: {face.area}")
print(f"Length: {edge.length}")

# Get bounding box
bbox = part.bounding_box()
print(f"Size: {bbox.size}")

# Count topology
print(f"Faces: {len(part.faces())}")
print(f"Edges: {len(part.edges())}")
```

## Common Mistakes

### Forgetting to assign operations

❌ **Wrong:**

```python
fillet(part.edges(), 1)  # Returns new object, part unchanged
```

✅ **Correct:**

```python
part = fillet(part.edges(), 1)  # Assign result
```

### Mixing modes incorrectly

❌ **Wrong:**

```python
with BuildPart():
    box = Box(10, 10, 10)
    result = box + Cylinder(5, 15)  # Mixing Builder and Algebra
```

✅ **Correct:**

```python
# Stay in Builder mode
with BuildPart():
    Box(10, 10, 10)
    Cylinder(5, 15, mode=Mode.ADD)
```

### Not understanding selector returns

❌ **Wrong:**

```python
face = part.faces()  # Returns ShapeList, not single face
fillet(face, 1)  # Error: needs edges
```

✅ **Correct:**

```python
faces = part.faces()  # ShapeList
top_face = faces.sort_by(Axis.Z)[-1]  # Single face
edges = top_face.edges()  # Edges of that face
```

### Incorrect import organization

build123d scripts commonly use wildcard imports:

✅ **Correct:**

```python
from build123d import *
```

This is standard practice for build123d despite general Python conventions.

## Performance Considerations

- Use appropriate tolerance for export (smaller = slower)
- Avoid excessive boolean operations (combine where possible)
- Use `make_hull()` instead of multiple boolean unions when applicable
- Cache complex computed shapes
- Consider `make_face()` for complex 2D profiles vs many boolean operations

## Additional Resources

### Reference Files

- **`references/api-quick-reference.md`** - Comprehensive object and operation reference
- **`references/mode-comparison.md`** - Detailed comparison of Builder vs Algebra modes

### Examples

- **`examples/algebra-mode-example.py`** - Complete parametric part in Algebra mode
- **`examples/builder-mode-example.py`** - Complex assembly in Builder mode

### External Documentation

- Official docs: <https://build123d.readthedocs.io/>
- Cheat sheet: <https://build123d.readthedocs.io/en/latest/cheat_sheet.html>
- GitHub: <https://github.com/gumyr/build123d>
- Discord community: <https://discord.com/invite/Bj9AQPsCfx>

## Quick Workflow

To develop with build123d:

1. **Import:** `from build123d import *`
2. **Choose mode:** Algebra for simple, Builder for complex
3. **Create geometry:** Use dimension-appropriate objects (1D/2D/3D)
4. **Apply operations:** Extrude, fillet, chamfer, boolean ops
5. **Select topology:** Use selectors with filtering/sorting
6. **Export:** `export_step()`, `export_stl()`, etc.
7. **Visualize:** Use ocp_vscode for interactive development

Focus on understanding the two modes, mastering selectors, and leveraging the operator-based syntax for clean, readable parametric CAD code.
