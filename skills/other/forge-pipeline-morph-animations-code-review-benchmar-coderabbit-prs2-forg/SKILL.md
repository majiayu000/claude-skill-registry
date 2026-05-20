---
name: forge-pipeline-morph-animations
description: Add morph target (blend shape) animations with pipeline assets to an SDL GPU project using ForgeSceneMorphModel.
---

Add morph target animation support to an SDL GPU project that already uses
`forge_scene.h`. This skill covers loading `.fmesh` files with morph data,
evaluating morph weight animation from `.fanim` channels, CPU-blending
per-vertex deltas, and uploading to GPU storage buffers for vertex shader
displacement.

## Prerequisites

- `forge_scene.h` with `FORGE_SCENE_MODEL_SUPPORT` enabled
- `forge_pipeline.h` for `.fmesh` and `.fanim` loading
- Pipeline-processed assets with `FLAG_MORPHS` set in `.fmesh`
- Compiled morph shaders (`scene_morph.vert.hlsl`, `scene_morph_shadow.vert.hlsl`)

## Asset processing

Process glTF models with morph targets using the pipeline tools:

```bash
forge_mesh_tool model.gltf model.fmesh --verbose
forge_scene_tool model.gltf model.fscene --verbose
forge_anim_tool model.gltf model.fanim --verbose
```

The mesh tool detects morph targets and sets `FLAG_MORPHS` in the `.fmesh`
header. It also disables vertex deduplication (morph deltas reference original
vertex indices). The anim tool preserves `MORPH_WEIGHTS` channels
(`target_path = 3`) with variable component counts.

## Loading a morph model

```c
#define FORGE_SCENE_MODEL_SUPPORT
#define FORGE_SCENE_IMPLEMENTATION
#include "scene/forge_scene.h"

ForgeSceneMorphModel morph_model;

/* fmat_path may be NULL if no materials; fanim_path may be NULL for manual weights */
if (!forge_scene_load_morph_model(&scene, &morph_model,
        fscene_path, fmesh_path, fmat_path, fanim_path, base_dir)) {
    SDL_Log("Failed to load morph model");
    return SDL_APP_FAILURE;
}
```

## Updating morph animation each frame

```c
/* After forge_scene_begin_frame(): */
morph_model.anim_speed = speed_slider_value;

/* Toggle manual_weights to override animation with direct control */
if (morph_model.manual_weights) {
    morph_model.morph_weights[0] = slider_w0;
    morph_model.morph_weights[1] = slider_w1;
}

forge_scene_update_morph_animation(&scene, &morph_model, dt);
```

`forge_scene_update_morph_animation` does three things:

1. Evaluates morph weight channels from `.fanim` (unless `manual_weights` is set)
2. CPU-blends position and normal deltas: `blended[v] += weight * delta[v]`
3. Uploads blended deltas to GPU storage buffers via persistent transfer buffer

## Drawing

```c
mat4 placement = mat4_multiply(
    mat4_translate(vec3_create(x, y, z)),
    mat4_scale_uniform(scale));

/* Shadow pass */
forge_scene_begin_shadow_pass(&scene);
forge_scene_draw_morph_model_shadows(&scene, &morph_model, placement);
forge_scene_end_shadow_pass(&scene);

/* Main pass */
forge_scene_begin_main_pass(&scene);
forge_scene_draw_grid(&scene);
forge_scene_draw_morph_model(&scene, &morph_model, placement);
forge_scene_end_main_pass(&scene);
```

## Cleanup

```c
forge_scene_free_morph_model(&scene, &morph_model);
```

## Shader approach

The morph vertex shader uses the standard 48-byte vertex layout (same as
`scene_model.vert.hlsl`) plus two `StructuredBuffer<float4>` for position
and normal deltas, indexed by `SV_VertexID`. The float4 type ensures a
consistent 16-byte stride across SPIRV and DXIL backends:

```hlsl
StructuredBuffer<float4> morph_pos_deltas : register(t0, space0);
StructuredBuffer<float4> morph_nrm_deltas : register(t1, space0);

float3 morphed_pos = input.position + morph_pos_deltas[input.vertex_id].xyz;
float3 morphed_nrm = normalize(input.normal + morph_nrm_deltas[input.vertex_id].xyz);
```

The shadow variant uses only position deltas (1 storage buffer).

## Reference

- [GPU Lesson 44 — Pipeline Morph Target Animations](../../../lessons/gpu/44-pipeline-morph-animations/)
- [Asset Lesson 13 — Morph Targets](../../../lessons/assets/13-morph-targets/)
- [GPU Lesson 43 — Pipeline Skinned Animations](../../../lessons/gpu/43-pipeline-skinned-animations/) — same CPU-compute + GPU-apply pattern
