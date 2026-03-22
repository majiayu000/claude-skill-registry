---
name: forge-pipeline-skinned-animations
description: >
  Add pipeline-based skeletal animation to an SDL GPU project using
  pre-processed .fskin/.fanim assets and ForgeSceneSkinnedModel.
---

Add skeletal animation using pre-processed pipeline assets (`.fmesh` v3,
`.fskin`, `.fanim`) and the `ForgeSceneSkinnedModel` API in `forge_scene.h`.
Joint matrices are computed on the CPU each frame and uploaded to a GPU storage
buffer for vertex-stage skinning. Use this skill when you need animated
characters or creatures with the pipeline asset workflow, or when you need
transform-only animation on non-skinned models.

See [GPU Lesson 43 — Pipeline Skinned Animations](../../../lessons/gpu/43-pipeline-skinned-animations/)
for the full walkthrough. For glTF-based skinning (without the pipeline), see
[GPU Lesson 32 — Skinning Animations](../../../lessons/gpu/32-skinning-animations/).

## Key API calls

| Function | Purpose |
|----------|---------|
| `forge_scene_load_skinned_model()` | Load skinned model from .fscene + .fmesh + .fmat + .fskin + .fanim |
| `forge_scene_update_skinned_animation()` | Advance time, evaluate keyframes, upload joint matrices |
| `forge_scene_draw_skinned_model()` | Draw skinned model in main pass (binds joint storage buffer) |
| `forge_scene_draw_skinned_model_shadows()` | Draw skinned model into shadow map |
| `forge_scene_free_skinned_model()` | Release all GPU + CPU resources |
| `forge_pipeline_anim_apply()` | Evaluate animation channels at time t (for transform-only use) |
| `forge_pipeline_scene_compute_world_transforms()` | Propagate hierarchy after animation |
| `forge_pipeline_compute_joint_matrices()` | Compute joint_matrix[i] = inv(mesh_world) × joint_world × IBM[i] |

## Skinned vertex layout (72 bytes)

```c
/* Pipeline skinned vertex — 72-byte stride */
/* offset  0: float3  position   (12 bytes) */
/* offset 12: float3  normal     (12 bytes) */
/* offset 24: float2  uv         ( 8 bytes) */
/* offset 32: float4  tangent    (16 bytes) */
/* offset 48: uint16×4 joints    ( 8 bytes) */
/* offset 56: float4  weights    (16 bytes) */
```

Vertex attributes (all TEXCOORD semantics):

- Location 0: `FLOAT3` at offset 0 (position)
- Location 1: `FLOAT3` at offset 12 (normal)
- Location 2: `FLOAT2` at offset 24 (uv)
- Location 3: `FLOAT4` at offset 32 (tangent)
- Location 4: `USHORT4` at offset 48 (joints)
- Location 5: `FLOAT4` at offset 56 (weights)

## Loading a skinned model

```c
#define FORGE_PIPELINE_IMPLEMENTATION
#include "pipeline/forge_pipeline.h"

#define FORGE_SCENE_MODEL_SUPPORT
#define FORGE_SCENE_IMPLEMENTATION
#include "scene/forge_scene.h"

ForgeSceneSkinnedModel model;
if (!forge_scene_load_skinned_model(&scene, &model,
        "assets/Model/Model.fscene",
        "assets/Model/Model.fmesh",
        "assets/Model/Model.fmat",
        "assets/Model/Model.fskin",
        "assets/Model/Model.fanim",
        "assets/Model")) {
    SDL_Log("Failed to load skinned model");
    return SDL_APP_FAILURE;
}
```

## Per-frame animation update

```c
/* Set animation parameters */
model.anim_speed = 1.0f;
model.looping = true;

/* Evaluate keyframes, propagate hierarchy, upload joint matrices */
forge_scene_update_skinned_animation(&scene, &model, dt);
```

## Drawing

```c
mat4 placement = mat4_multiply(
    mat4_translate(vec3_create(0, 0, 0)),
    mat4_scale_uniform(1.0f));

/* Shadow pass */
forge_scene_begin_shadow_pass(&scene);
forge_scene_draw_skinned_model_shadows(&scene, &model, placement);
forge_scene_end_shadow_pass(&scene);

/* Main pass */
forge_scene_begin_main_pass(&scene);
forge_scene_draw_skinned_model(&scene, &model, placement);
forge_scene_end_main_pass(&scene);
```

## Shader pattern (vertex)

The skinned vertex shader reads joint matrices from a storage buffer
(`StructuredBuffer`) rather than a uniform buffer, supporting up to 256 joints:

```hlsl
StructuredBuffer<float4x4> joint_mats : register(t0, space0);

float4x4 skin_mat =
    input.weights.x * joint_mats[input.joints.x] +
    input.weights.y * joint_mats[input.joints.y] +
    input.weights.z * joint_mats[input.joints.z] +
    input.weights.w * joint_mats[input.joints.w];

float4 skinned_pos = mul(skin_mat, float4(input.position, 1.0));
float3 skinned_nrm = normalize(mul((float3x3)skin_mat, input.normal));
float3 skinned_tan = normalize(mul((float3x3)skin_mat, input.tangent.xyz));
```

## Transform animation (non-skinned models)

For models with animation but no skin (e.g., a rotating cube), load the
animation separately and apply it manually:

```c
ForgeSceneModel model;
ForgePipelineAnimFile anim;
float anim_time = 0.0f;

if (!forge_scene_load_model(&scene, &model, fscene, fmesh, fmat, base_dir)) {
    SDL_Log("Failed to load model");
    return SDL_APP_FAILURE;
}
if (!forge_pipeline_load_animation(fanim_path, &anim)) {
    SDL_Log("Failed to load animation");
    forge_scene_free_model(&scene, &model);
    return SDL_APP_FAILURE;
}

/* Each frame */
anim_time += dt;
if (anim.clip_count > 0) {
    forge_pipeline_anim_apply(&anim.clips[0],
        model.scene_data.nodes, model.scene_data.node_count,
        anim_time, true);
}
forge_pipeline_scene_compute_world_transforms(
    model.scene_data.nodes, model.scene_data.node_count,
    model.scene_data.roots, model.scene_data.root_count,
    model.scene_data.children, model.scene_data.child_count);

/* Draw with a model-level placement — node animation is applied
 * internally via the scene_data.nodes[*].world_transform values
 * that forge_pipeline_anim_apply() + compute_world_transforms() wrote. */
mat4 placement = mat4_identity();  /* or any model-level transform */
forge_scene_draw_model(&scene, &model, placement);
```

## Pipeline files

| File | Content |
|------|---------|
| `.fmesh` v3 | Skinned vertices (72-byte stride, `FORGE_PIPELINE_FLAG_SKINNED`) |
| `.fskin` | Joint hierarchy, inverse bind matrices, skin-to-node mapping |
| `.fanim` | Keyframe clips with per-channel TRS data |
| `.fscene` | Scene node hierarchy (parents, transforms) |
| `.fmat` | Material definitions (colors, texture references) |

Generate these from glTF source using:

```bash
forge_mesh_tool model.gltf model.fmesh --verbose
forge_scene_tool model.gltf model.fscene --skins --verbose
forge_anim_tool model.gltf model.fanim --verbose
```

## Common mistakes

- **Missing `--skins` flag** — `forge_scene_tool` must be run with `--skins` to
  generate the `.fskin` file. Without it, joint hierarchy data is missing.
- **Pipeline quaternion order** — Pipeline stores quaternions as `[x, y, z, w]`,
  matching glTF. The forge math library uses `quat(w, x, y, z)` with `w` first.
  The pipeline evaluation functions handle this conversion internally.
- **Forgetting shadow skinning** — Use `forge_scene_draw_skinned_model_shadows()`
  for the shadow pass. Using the non-skinned shadow draw produces a static
  bind-pose shadow.
- **Non-skinned model with animation** — Do not use `ForgeSceneSkinnedModel` for
  models without a skin. Instead, load as `ForgeSceneModel` and apply animation
  with `forge_pipeline_anim_apply()` manually.
