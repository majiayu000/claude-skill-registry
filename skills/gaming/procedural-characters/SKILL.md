---
name: Procedural Character Generation
description: |
  Generate low-poly characters (300-700 tris) for ZX games using the extrude+scale paradigm.

  **Triggers:** "character mesh", "humanoid mesh", "quadruped mesh", "low-poly character"

  **Before generating:** Check `.studio/visual-style.md` for project style.

  **Load references when:**
  - **COORDINATE SYSTEM** → `references/canonical-coordinates.md` (CRITICAL for bulge/scale/tilt)
  - Python bpy code → `references/bpy-implementation.md`
  - Skeleton hierarchies → `references/skeleton-presets.md`
  - Body part patterns → `references/body-part-patterns.md`
  - Style presets → `references/style-presets.md`
  - Triangle budgets → `references/triangle-budget-guide.md`
  - Example specs → `examples/knight.spec.py`, `examples/spider.spec.py`

  **Related skills:**
  - NORMAL MAPS: `procedural-normal-maps`
  - TEXTURING: `mesh-texturing-workflows`
  - ANIMATIONS: `procedural-animations`
version: 1.4.0
---

# Procedural Character Generation

Generate low-poly characters (PS1/PS2 era, 300-700 tris) using Python specs and Blender bpy.

## Core Concept: Extrude+Scale Paradigm

Characters are defined as `.spec.py` files with:
1. **Skeleton** - Bone hierarchy with world positions
2. **Parts** - Body parts that extrude along bone directions
3. **Steps** - Extrude+scale sequences building each part
4. **Mirroring** - Automatic left/right symmetry

## Character Spec Format

```python
SPEC = {
    "character": {
        "name": "knight_enemy",
        "tri_budget": 400,
        "skeleton": [
            {"bone": "pelvis", "parent": None, "head": [0, 0, 0.9], "tail": [0, 0, 1.0]},
            {"bone": "spine", "parent": "pelvis", "head": [0, 0, 1.0], "tail": [0, 0, 1.3]},
            {"bone": "arm_upper_R", "mirror": "arm_upper_L"},
        ],
        "parts": {
            "torso": {
                "bone": "spine",
                "base": "hexagon(6)",
                "base_radius": 0.12,
                "steps": [
                    {"extrude": 0.05, "scale": 1.15},
                    {"extrude": 0.15, "scale": 1.0},
                ],
                "cap_start": True, "cap_end": False
            },
            "arm_upper_R": {"mirror": "arm_upper_L"}
        }
    }
}
```

## Canonical Coordinate System

**CRITICAL:** Always follow `references/canonical-coordinates.md` (it is the authoritative, code-accurate mapping used by `get_bone_transform()`, including edge-case fallback behavior).

## Step Operations

| Param | Effect |
|-------|--------|
| `extrude` | Distance along bone (+Z) |
| `scale` | Uniform or [width, depth] asymmetric |
| `bulge` | Forward/back push (+/- = forward/back) |
| `tilt` | Rotation in degrees [sideways, forward] |

## Base Shapes

| Shape | Vertices | Tris/Step | Best For |
|-------|----------|-----------|----------|
| `triangle(3)` | 3 | 6 | Hair spikes |
| `square(4)` | 4 | 8 | Mecha, low budget |
| `hexagon(6)` | 6 | 12 | Standard |
| `octagon(8)` | 8 | 16 | Smooth organic |

## Budget Guidelines

| Budget | Bases | Hands |
|--------|-------|-------|
| 300 | square(4) | stub |
| 400 | square/hex | mitten |
| 500 | hexagon(6) | mitten+thumb |
| 700 | hex/oct | 3-finger |

## Joint Seam Rules

Connected parts MUST share same base vertex count:

```python
# CORRECT
"torso": {"base": "hexagon(6)", "cap_end": False},
"head": {"base": "hexagon(6)", "cap_start": False}  # matches

# INCORRECT - won't weld
"torso": {"base": "octagon(8)"},
"head": {"base": "hexagon(6)"}
```

## Workflow

**1. Design Phase (character-designer agent)**
- Determine type, style, budget
- Generate `.spec.py` to `.studio/specs/characters/`

**2. Generation Phase (character_parser.py)**
```bash
blender --background --python character_parser.py -- \
    .studio/specs/characters/knight.spec.py \
    assets/characters/knight.glb
```

## Non-Humanoid Characters

| Creature | Key Difference |
|----------|----------------|
| Quadruped | Horizontal spine, 4 legs, tail |
| Serpent | Chain of segments |
| Spider | 2 body segments, 8 legs |

See `references/skeleton-presets.md` for hierarchies.

## ZX Constraints

| Constraint | Limit |
|------------|-------|
| Max bones per game | 256 |
| Bones per vertex | 4 |
| Texture resolution | 512x512 max |
| Typical character tris | 300-500 |

## Normal Map Support

Add to spec for tangent export:
```python
"use_normal_maps": True
```

See `procedural-normal-maps` skill for texture generation.

## Validation

See `CHARACTER_MODELING_VALIDATION_PLAN.md` for the code-accurate, end-to-end validation strategy (conventions, strict mode, probe specs, and mesh-based checks).
