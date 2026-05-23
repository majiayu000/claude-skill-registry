---
name: Procedural Mesh Generation (Blender bpy)
description: |
  Generate 3D meshes for ZX games using Blender bpy in headless mode.

  **Triggers:** "generate mesh", "3D model", "low-poly", "blender script", "hard surface", "organic mesh", "metaballs", "UV unwrap", "export glb".

  **Before generating:** Check `.studio/visual-style.md` for project style specs.

  **Load references when:**
  - Basic shapes, primitives → `references/bpy-primitives.md`
  - Modifiers (bevel, mirror, array) → `references/bpy-modifiers.md`
  - Organic shapes, metaballs, skin → `references/bpy-organic-workflows.md`
  - UV, normals, cleanup, export → `references/bpy-post-processing.md`
  - Tangent export for normal maps → `references/bpy-tangent-export.md`
  - Project structure, multiple assets → `generator-patterns` skill

  **Related skills:**
  - NORMAL MAPS: `procedural-normal-maps` (requires tangent export)
  - CHARACTERS: `procedural-characters` (extrude+scale paradigm)
  - TEXTURING: `mesh-texturing-workflows`
  - ANIMATION: `procedural-animations`
version: 1.4.0
---

# Procedural Mesh Generation

Generate game-ready 3D meshes with proper UVs and normals for Nethercore ZX.

## Prerequisites

Blender 3.0+ must be installed and in PATH:

```bash
blender --version
```

Run mesh generation via: `blender --background --python .studio/generate.py -- --only meshes`

## Spec-Based Workflow

Write one mesh spec per file under `.studio/specs/meshes/`:

```python
# .studio/specs/meshes/barrel.spec.py
MESH = {
    "mesh": {
        "name": "barrel",
        "primitive": "cylinder",
        "params": {"radius": 0.45, "depth": 1.1, "vertices": 24},
        "modifiers": [{"type": "bevel", "width": 0.02, "segments": 2}],
        "uv": {"mode": "smart_project", "angle_limit": 66.0},
        "export": {"tangents": True},
    }
}
```

Generate with:

```bash
blender --background --python .studio/generate.py -- --only meshes
```

## Workflow Selection

| Mesh Type | Workflow | Reference |
|-----------|----------|-----------|
| Props, weapons, vehicles, architecture | Polygon modeling (primitives + modifiers) | `bpy-primitives.md`, `bpy-modifiers.md` |
| Blobby shapes (slimes, eggs) | Metaballs | `bpy-organic-workflows.md#metaballs` |
| Creatures from skeleton | Skin modifier | `bpy-organic-workflows.md#skin-modifier` |
| Complex smooth blends | SDF pipeline | `bpy-organic-workflows.md#sdf-pipeline` |

## Hard Surface Quick Reference

**Core Primitives:**
- `bpy.ops.mesh.primitive_cube_add()` - Crates, boxes
- `bpy.ops.mesh.primitive_cylinder_add()` - Barrels, pillars
- `bpy.ops.mesh.primitive_uv_sphere_add()` - Spheres, domes
- `bpy.ops.mesh.primitive_cone_add()` - Spikes, cones
- `bpy.ops.mesh.primitive_torus_add()` - Rings, wheels

**Key Modifiers:** MIRROR, BEVEL, SOLIDIFY, ARRAY, BOOLEAN, DECIMATE

See `references/bpy-modifiers.md` for detailed modifier patterns.

## Console Constraints

| Use Case | Triangle Budget | Bones (if animated) |
|----------|-----------------|---------------------|
| Swarm entities | 50-150 | - |
| Props | 50-300 | - |
| Characters | 200-500 | 16-24 |
| Vehicles | 300-800 | - |
| Hero/close-up | 500-2000 | 32-48 |

**Texture resolution:** Power-of-2 only (64, 128, 256, 512)

## Required Post-Processing

Every mesh MUST have before export:
1. **UV unwrap** - `smart_project` or `cube_project`
2. **Normals** - `shade_smooth` + `use_auto_smooth`
3. **Cleanup** - `remove_doubles`, `delete_loose`
4. **Triangulate** - `quads_convert_to_tris`
5. **Export** - GLB with `export_normals=True`

See `references/bpy-post-processing.md` for implementation.

## File Organization

One mesh spec per file:

```
.studio/specs/meshes/
├── barrel.spec.py
└── crate.spec.py

generated/meshes/
├── barrel.glb
└── crate.glb
```

## nether.toml Integration

```toml
[build]
script = "blender --background --python .studio/generate.py -- --only meshes && cargo build -p game --target wasm32-unknown-unknown --release"

[[assets.meshes]]
id = "barrel"
path = "../generated/meshes/barrel.glb"
```

## Tangent Export (for Normal Maps)

If using normal maps, enable tangents:

```python
mesh.calc_tangents()  # Requires UVs
bpy.ops.export_scene.gltf(
    filepath="output.glb",
    export_tangents=True
)
```

See `references/bpy-tangent-export.md` for complete workflow.

## Quality Checklist

- [ ] Triangle count within budget
- [ ] UVs unwrapped (no overlapping)
- [ ] Normals consistent (no inverted faces)
- [ ] No loose geometry
- [ ] Triangulated
- [ ] Correct scale (1 unit = 1 meter)
- [ ] Origin at logical point
- [ ] Tangents if using normal maps
