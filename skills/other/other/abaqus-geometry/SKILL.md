---
name: abaqus-geometry
description: Create and manipulate Abaqus geometry - parts, sketches, extrusions, CAD import. Use for any geometry creation task including box, cylinder, or STEP/IGES import.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash(abaqus:*)
---

# Abaqus Geometry Skill

Create parts, assemblies, and import CAD files for finite element analysis.

## When to Use This Skill

**Route here when user mentions:**
- "create a box/beam/plate/bracket"
- "draw geometry", "make a cylinder/tube"
- "import STEP/IGES file"
- "extrude", "revolve", "create assembly"
- "position the parts", "build a component"

**Route elsewhere:**
- Meshing the geometry -> `/abaqus-mesh`
- Defining materials/sections -> `/abaqus-material`
- Applying loads or BCs -> `/abaqus-load`, `/abaqus-bc`
- Full analysis workflow -> `/abaqus-static-analysis`

## Key Decisions

### 1. How to Create Geometry?

| Shape | Approach |
|-------|----------|
| Box, plate, beam | Sketch rectangle + extrude |
| Cylinder, tube | Sketch circle + extrude |
| Pipe, disc, shaft | Sketch profile + revolve |
| Complex/existing | Import STEP/IGES |
| Quick prototype | Primitives |

**Decision guidance:**
- Simple prismatic shape? -> Sketch + extrude
- Axisymmetric part? -> Sketch + revolve
- Existing CAD model? -> Import STEP file

### 2. Where to Place Origin?

| Origin Location | When to Use |
|-----------------|-------------|
| Corner (0,0,0) | Asymmetric parts, easier coordinate math |
| Center (0,0,0) | Symmetric parts, rotation about center |

### 3. Part vs Instance Coordinates

| Context | Use |
|---------|-----|
| Geometry creation, section assignment | Part coordinates |
| BCs, loads, sets, finding faces | Instance/assembly coordinates |

**Important:** After creating an instance, use `instance.faces.findAt()` not `part.faces.findAt()`.

## What to Ask User

If unclear, ask:
- **Shape type?** Box, cylinder, imported CAD?
- **Dimensions?** Length, width, height in mm
- **Origin location?** Corner or center?
- **Import file available?** Path to STEP/IGES?
- **Features needed?** Holes, fillets, chamfers?

## Workflow

### Step 1: Create Model and Part

Create the model container, then a 3D deformable part.

### Step 2: Define Geometry

Choose approach based on shape:
- **Sketch + Extrude:** Draw 2D profile, extrude to 3D
- **Sketch + Revolve:** Draw profile, revolve around axis (360 degrees for full solid)
- **CAD Import:** Open STEP/IGES, create part from geometry file

### Step 3: Add Features (Optional)

Add secondary features if needed:
- Cut holes using cut extrude
- Round edges with fillet
- Partition cells for BC/load regions

### Step 4: Create Assembly Instance

Create root assembly with Cartesian datum, then create instance from part.

### Step 5: Create Sets and Surfaces

Create named sets/surfaces on **instance** (not part) for:
- BC regions
- Load application surfaces
- Design regions (for optimization)

## Finding Entities

Two methods to locate faces/edges:
1. **findAt()** - Exact coordinates (point must be ON the entity)
2. **getByBoundingBox()** - Tolerant box search (better for automation)

Combine multiple entities with `+` operator.

## Common Pitfalls

| Problem | Cause | Solution |
|---------|-------|----------|
| "Sketch is not closed" | Gap in sketch entities | Ensure lines connect to form closed loop |
| "Cannot find face at coordinates" | Point not exactly on face | Use bounding box or verify coordinates |
| "Part has no cells" | Sketch not extruded | Call BaseSolidExtrude or similar |
| "Instance already exists" | Duplicate name | Use unique name or delete existing |

## Validation Checklist

Before proceeding to mesh/analysis:
- [ ] Part created with correct dimensions
- [ ] Geometry is watertight (no gaps)
- [ ] Instance created in assembly
- [ ] Sets created on **instance** for BC/load regions
- [ ] Partitions added if needed for region selection

## Units

All dimensions use consistent units (mm-tonne-s-N-MPa):
- Length: mm
- Coordinates: mm

## Code Patterns

For API syntax and code examples, see:
- [API Quick Reference](references/api-quick-ref.md)
- [Common Patterns](references/common-patterns.md)
- [Troubleshooting Guide](references/troubleshooting.md)
