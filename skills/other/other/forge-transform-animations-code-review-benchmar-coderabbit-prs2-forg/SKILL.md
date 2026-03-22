---
name: forge-transform-animations
description: >
  Add keyframe animation with glTF loading, quaternion slerp, and path-following
  to an SDL GPU project.
---

Add transform animations to an SDL3 GPU scene using keyframe data loaded from
glTF files and procedural path-following. The technique evaluates keyframe
channels (binary search + interpolation), applies animated transforms to a node
hierarchy, and composes multiple animation layers (data-driven + procedural).
Use this skill when you need animated objects — spinning wheels, walking
characters, vehicles following paths, or any keyframe-driven motion.

See [GPU Lesson 31 — Transform Animations](../../../lessons/gpu/31-transform-animations/)
for the full walkthrough.

## Key API calls

| Function | Purpose |
|----------|---------|
| `forge_gltf_load()` | Load a glTF model with node hierarchy, buffers, and animation data |
| `forge_gltf_anim_apply()` | Evaluate all animation channels at time t — binary search + slerp/lerp |
| `forge_gltf_compute_world_transforms()` | Propagate local transforms through the node hierarchy |
| `quat_slerp(a, b, t)` | Spherical linear interpolation between two quaternions |
| `mat4_multiply(a, b)` | Compose two transforms: apply B first, then A |

## Animation evaluation

`forge_gltf_load()` parses animation data from the glTF file into
`ForgeGltfAnimation` structs in `scene.animations[]`. At runtime,
`forge_gltf_anim_apply()` handles all channel evaluation — binary search
for keyframe intervals, `vec3_lerp` for translation/scale, `quat_slerp`
for rotation, glTF-to-forge quaternion order conversion, and local
transform rebuilds.

```c
#include "gltf/forge_gltf.h"
#include "gltf/forge_gltf_anim.h"

/* Each frame: advance time, evaluate, rebuild hierarchy */
wheel_time += dt * ANIM_SPEED;
if (scene.animation_count > 0) {
    forge_gltf_anim_apply(&scene.animations[0],
                          scene.nodes, scene.node_count,
                          wheel_time, true);  /* true = loop */
}

mat4 identity = mat4_identity();
for (int i = 0; i < scene.root_node_count; i++)
    forge_gltf_compute_world_transforms(&scene,
                                        scene.root_nodes[i], &identity);
```

## Common mistakes

- **Forgetting to call `forge_gltf_compute_world_transforms()` after
  `forge_gltf_anim_apply()`.** The apply function updates node TRS and
  rebuilds local transforms, but world transforms still need propagation
  through the hierarchy.

- **Not wrapping time for looping animations.** Pass `true` for the `loop`
  parameter of `forge_gltf_anim_apply()`, or use `fmodf(t, duration)` if
  managing time manually.

- **Ignoring the Yup2Zup node.** Some models include coordinate system
  conversion nodes. Include them in the hierarchy walk or the model will be
  incorrectly oriented.

## Composing animation layers

The key insight: local transforms compose through the hierarchy. Apply
different animation sources at different levels:

```text
truck_placement (from path animation)
  └── Node 5 "Yup2Zup" (static rotation from glTF)
        └── Node 4 "Truck Body" (mesh)
              ├── Node 1 "Front Axle" (static translation)
              │     └── Node 0 "Wheels" (rotation from keyframes)
              └── Node 3 "Rear Axle" (static translation)
                    └── Node 2 "Wheels" (rotation from keyframes)
```

Each frame: evaluate wheel keyframes → set wheel node rotations →
rebuild hierarchy with path placement as root → render with final world
transforms.
