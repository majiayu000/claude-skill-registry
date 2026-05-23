---
name: Procedural Animation Generation
description: |
  Create animations for ZX game assets using Blender bpy.

  **Triggers:** "animate mesh", "walk cycle", "skeletal animation", "rig character", "keyframe", "spinning pickup"

  **Before animating:** Check `.studio/direction/visual.md` for animation feel.

  **Workflow:**
  - `animation-describer` agent → Produces `.spec.py` in `.studio/specs/animations/`
  - `python .studio/generate.py --only animations` → Interprets specs in Blender

  **Load references when:**
  - **COORDINATE SYSTEM** → `procedural-characters → references/canonical-coordinates.md` (CRITICAL)
  - Animation spec format → `references/animation-spec-format.md`
  - Animation parser → `.studio/parsers/animation.py`
  - IK setup → `references/ik-utilities.md`
  - Object animation → `references/object-animation.md`
  - Armature/rigs → `references/armature-creation.md`
  - Walk/attack cycles → `references/keyframe-patterns.md`
  - Export settings → `references/gltf-export.md`
  - ZX limits → `references/zx-constraints.md`

  **Related skills:**
  - MESH GENERATION: `procedural-meshes`
  - CHARACTER RIGS: `procedural-characters`
version: 5.0.0
---

# Procedural Animation Generation

Create animated 3D objects using Blender's Python API in headless mode.

## Prerequisites

Blender 3.0+ in PATH: `blender --version`

## Animation Type Decision

| Does mesh deform? | Approach |
|-------------------|----------|
| No (spinning, bobbing) | Object animation |
| Yes (bending, stretching) | Skeletal animation |

## Animation Approach Quick Reference

| Animation | Approach | Why |
|-----------|----------|-----|
| Walk/run | IK feet + FK upper | Foot placement |
| Idle/breathing | FK only | No contact |
| Sword swings | FK only | Rotational arcs |
| Climbing | IK hands + feet | Goal positions |
| Spinning pickups | Object animation | No deformation |

## Animation Spec Pipeline

```
animation-describer agent → .spec.py → generate.py → .glb
```

**Why this architecture:**
- No PyYAML dependency (Python literals)
- Parser is deterministic, reusable
- Skeleton-agnostic (any armature)
- Explicit rotations (degrees)
- Unified with other asset types

## Animation Spec Format

```python
# .studio/specs/animations/knight_walk.spec.py
ANIMATION = {
    "animation": {
        "name": "knight_walk",
        "input_armature": "assets/characters/knight.glb",
        "duration_frames": 60,
        "fps": 60,
        "loop": True,

        # Declarative rig setup (IK, constraints, presets)
        "rig_setup": {
            "presets": {"humanoid_legs": True},  # Auto IK chains
            "constraints": [
                {"bone": "leg_lower_L", "type": "hinge", "axis": "X", "limits": [0, 160]},
            ],
        },

        "poses": {...},
        "phases": [
            {
                "name": "step",
                "frames": [0, 15],
                "pose": "right_forward",
                "ik_targets": {
                    "ik_foot_R": [{"frame": 0, "location": [0.09, 0.25, 0]}],
                },
            },
        ],
    }
}
```

See `references/animation-spec-format.md` for complete spec.

## Declarative Rig Setup

The `rig_setup` section provides professional rigging features:

| Feature | Description |
|---------|-------------|
| `presets` | Quick setup: `humanoid_legs`, `humanoid_arms`, `spider_legs`, `quadruped_legs` |
| `ik_chains` | Explicit IK chains for any bone count |
| `constraints` | Intent-based: `hinge`, `ball`, `planar` |
| `aim_constraints` | Look-at/aim for head tracking |

**Presets expand to full IK chain definitions** - just enable and animate!

```python
"rig_setup": {
    "presets": {"spider_legs": True},  # Creates 8 IK chains with poles
    "ik_chains": [  # Or explicit chains for tails/hair
        {"name": "tail", "bones": ["tail_1", "tail_2", "tail_3"], "target": {"name": "ik_tail"}},
    ],
}
```

Everything bakes to FK before export - no game engine IK needed.

## IK Target Naming Convention

**Standard:** `ik_{end_bone}` - named after the bone the IK controls.

| Chain | IK Target | Pole Vector |
|-------|-----------|-------------|
| Leg | `ik_foot_L`, `ik_foot_R` | `pole_knee_L`, `pole_knee_R` |
| Arm | `ik_hand_L`, `ik_hand_R` | `pole_elbow_L`, `pole_elbow_R` |
| Tail | `ik_tail_tip` | (none for single-chain) |
| Spider leg | `ik_leg_front_L`, `ik_leg_mid_front_R`, etc. | `pole_front_L`, etc. |

**Presets auto-create these names** - just reference them in `ik_targets`:

```python
"ik_targets": {
    "ik_foot_L": [{"frame": 0, "location": [-0.08, 0.2, 0]}],  # humanoid_legs preset
    "ik_hand_R": [{"frame": 0, "location": [0.3, 0.5, 1.2]}],  # humanoid_arms preset
}
```

**For custom chains**, use `ik_{chain_name}_tip`:
```python
"ik_chains": [
    {"name": "tail", "bones": ["tail_1", "tail_2"], "target": {"name": "ik_tail_tip"}},
]
```

See `references/preset-reference.md` for full preset bone requirements.

## Validation

The parser validates animation specs at multiple stages:

### Bone Validation (Pre-Generation)
- **Spec-to-spec:** Checked before Blender work (catches early)
- **Runtime GLB:** Checked when loading armature (safety net)

Missing bones cause hard errors with detailed messages:
```
AnimationValidationError: Spec references bones not in armature 'knight':

Missing bones:
  - arm_twist_L (referenced in: rig_setup.twist_bones[0].target)
  - toe_L (referenced in: preset 'humanoid_legs')

Available bones (14):
  arm_lower_L, arm_lower_R, arm_upper_L, arm_upper_R, ...
```

### Motion Validation (Post-Bake)

After IK is baked to FK, the parser validates hinge joint motion:

1. **Calibration**: Determines flexion axis/sign from rest geometry
2. **Frame-by-frame check**: Detects hyperextension/overflexion
3. **Report generation**: Produces `.validation.json` alongside `.glb`

```json
{
  "version": "2026-01-08",
  "armature": "knight",
  "status": "pass",
  "hinges": {
    "leg_lower_L": {"axis": "X", "flexion_sign": "+", "range_deg": [0, 160], "violations": []}
  }
}
```

**Strict mode** fails on violations:
```bash
blender --background --python animation.py -- spec.spec.py in.glb out.glb --strict
```

Or in spec:
```python
"conventions": {"version": "2026-01-08", "strict": True}
```

## Rotation Convention

| Term | Axis | Example |
|------|------|---------|
| **pitch** | X | Nodding, elbow bend |
| **yaw** | Y | Twisting, turning |
| **roll** | Z | Tilting, side-bend |

All values in degrees. See `procedural-characters → references/canonical-coordinates.md` for full reference.

## Object Animation (Simple)

```python
import bpy, math

obj = bpy.context.active_object
obj.rotation_euler = (0, 0, 0)
obj.keyframe_insert(data_path="rotation_euler", frame=1)
obj.rotation_euler = (0, 0, math.radians(360))
obj.keyframe_insert(data_path="rotation_euler", frame=60)

for fc in obj.animation_data.action.fcurves:
    for kp in fc.keyframe_points:
        kp.interpolation = 'LINEAR'
```

See `references/object-animation.md` for bobbing, doors, etc.

## ZX Constraints

| Constraint | Limit |
|------------|-------|
| Bones per mesh | ~30 max |
| Keyframes | Keep minimal |
| Actions per mesh | 1-4 clips |

See `references/zx-constraints.md` for optimization.

## Export

```python
bpy.ops.export_scene.gltf(
    filepath="output.glb",
    export_format='GLB',
    export_animations=True,
    export_animation_mode='ACTIONS',
    export_skins=True,
    export_all_influences=False,  # Max 4 bones/vertex
)
```

## Running the Parser

Via unified generator:
```bash
python .studio/generate.py --only animations
```

Standalone (for debugging):
```bash
blender --background --python .studio/parsers/animation.py -- \
    .studio/specs/animations/knight_idle.spec.py \
    assets/characters/knight.glb \
    assets/animations/knight_idle.glb
```

## File Organization

```
.studio/
├── generate.py                    # Unified generator
├── parsers/
│   └── animation.py               # Animation parser
└── specs/
    └── animations/
        ├── knight_idle.spec.py
        ├── knight_walk.spec.py
        └── knight_attack.spec.py

assets/
└── animations/
    ├── knight_idle.glb
    └── knight_walk.glb
```
