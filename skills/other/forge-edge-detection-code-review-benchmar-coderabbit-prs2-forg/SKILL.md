---
name: forge-edge-detection
description: >
  Add Sobel edge detection on G-buffer data (depth + normals via MRT),
  stencil-based X-ray vision with depth_fail_op, and Fresnel ghost
  silhouettes with additive blending to an SDL GPU project.
triggers:
  - edge detection
  - sobel filter
  - x-ray vision
  - ghost silhouette
  - post-process outline
  - depth_fail_op
  - fresnel outline
---

# Edge Detection

Add post-process edge detection, stencil X-ray vision, and Fresnel ghost
silhouettes to an SDL GPU project. Uses G-buffer MRT output (depth + normals)
for Sobel edge detection, `depth_fail_op` for occluded-object marking, and
additive blending for translucent ghost rendering.

Based on [GPU Lesson 36](../../../lessons/gpu/36-edge-detection/).

## When to use

- You want post-process outlines from depth/normal discontinuities
- You need X-ray vision to reveal occluded objects behind walls
- You want ghostly translucent silhouettes for hidden geometry
- You need an alternative to L34's stencil-expansion outlines

## Pipeline overview (6 pipelines)

1. **Shadow pipeline** — Depth-only pass for shadow mapping
2. **Scene pipeline (MRT)** — Renders lit scene to two color targets:
   color (RT0) and view-space normals (RT1), plus depth-stencil
3. **Grid pipeline (MRT)** — Same MRT layout for the floor grid
4. **Edge composite pipeline** — Full-screen quad, samples depth + normal
   textures, runs Sobel filter, composites edges onto the scene
5. **X-ray mark pipeline** — Draws occluded objects with `depth_fail_op =
   INCREMENT_AND_WRAP`, `color_write_mask = 0`, writing only to stencil
   where fragments fail the depth test
6. **Ghost pipeline** — Draws the same objects again with stencil test
   `NOT_EQUAL` ref=0 and additive blending for Fresnel ghost silhouettes

## G-buffer setup (MRT)

The scene pass renders to two color targets simultaneously:

```c
/* RT0: scene color (RGBA8) */
/* RT1: view-space normals (RGBA16_FLOAT or RGBA8_SNORM) */
SDL_GPUColorTargetInfo color_targets[2] = {
    { .texture = scene_color_tex, .load_op = SDL_GPU_LOADOP_CLEAR },
    { .texture = normal_tex,      .load_op = SDL_GPU_LOADOP_CLEAR },
};
```

The fragment shader outputs to both targets:

```hlsl
struct PSOutput {
    float4 color  : SV_Target0;
    float4 normal : SV_Target1;
};
```

Pipeline must declare two color target descriptions to match.

## Sobel edge detection

Sample depth and normal textures in a 3x3 neighborhood. Apply Sobel
operators (horizontal Gx and vertical Gy kernels) separately to depth
and to each normal component. Combine magnitudes:

```hlsl
/* Sobel kernels */
/* Gx = [-1 0 1; -2 0 2; -1 0 1] */
/* Gy = [-1 -2 -1; 0 0 0; 1 2 1] */

float depth_edge = sqrt(gx_depth * gx_depth + gy_depth * gy_depth);
float normal_edge = sqrt(gx_nx*gx_nx + gy_nx*gy_nx
                       + gx_ny*gx_ny + gy_ny*gy_ny
                       + gx_nz*gx_nz + gy_nz*gy_nz);

float edge = saturate(depth_edge * depth_scale + normal_edge * normal_scale);
```

Threshold and composite: `final_color = lerp(scene_color, edge_color, edge)`.

## X-ray mark technique (depth_fail_op)

The key insight: `depth_fail_op` fires when a fragment is behind existing
geometry. By drawing the target object with this operation, we mark exactly
the pixels where it is occluded.

```c
/* X-ray mark pipeline stencil state */
SDL_GPUStencilOpState xray_stencil = {
    .fail_op       = SDL_GPU_STENCILOP_KEEP,
    .pass_op       = SDL_GPU_STENCILOP_KEEP,           /* visible parts: no mark */
    .depth_fail_op = SDL_GPU_STENCILOP_INCREMENT_AND_WRAP, /* occluded: mark */
    .compare_op    = SDL_GPU_COMPAREOP_ALWAYS,
};
```

Color write mask = 0 and depth write = false. This pass is invisible — it
only writes stencil values where the object is hidden behind other geometry.

## Ghost silhouette technique

After the X-ray mark pass, draw the object again with:

- Stencil test: `compare_op = NOT_EQUAL`, reference = 0 (draw only where marked)
- Additive blending: `src_color_blendfactor = ONE`, `dst = ONE`
- Fresnel-based opacity: brighter at edges where `dot(N, V)` is low

```hlsl
/* Fresnel ghost effect */
float fresnel = 1.0 - saturate(dot(normal, view_dir));
fresnel = pow(fresnel, fresnel_power);
return float4(ghost_color * fresnel * intensity, 0.0);
```

The additive blend makes the ghost glow through geometry without needing
alpha sorting.

## Clearing stencil

Clear stencil alongside depth at the start of the render pass:

```c
SDL_GPUDepthStencilTargetInfo ds_target = {
    .texture          = depth_stencil_texture,
    .load_op          = SDL_GPU_LOADOP_CLEAR,
    .store_op         = SDL_GPU_STOREOP_STORE,
    .clear_depth      = 1.0f,
    .clear_stencil    = 0,
    .stencil_load_op  = SDL_GPU_LOADOP_CLEAR,
    .stencil_store_op = SDL_GPU_STOREOP_STORE,
};
```

## Key patterns

| Pattern | Value |
|---------|-------|
| `depth_fail_op` | `SDL_GPU_STENCILOP_INCREMENT_AND_WRAP` |
| X-ray mark `color_write_mask` | `0` (invisible pass) |
| X-ray mark `depth_write` | `false` |
| Ghost stencil `compare_op` | `SDL_GPU_COMPAREOP_NOT_EQUAL` |
| Ghost stencil `reference` | `0` |
| Ghost blend | Additive (`SRC=ONE`, `DST=ONE`) |
| MRT count | 2 (color + normals) |

## Key API calls

- `SDL_BeginGPURenderPass(cmd, color_targets, 2, &ds)` — MRT with 2 color targets
- `SDL_SetGPUStencilReference(pass, ref)` — set stencil compare reference value
- `SDL_DrawGPUPrimitives(pass, 3, 1, 0, 0)` — fullscreen triangle (no vertex buffer)
- `SDL_GPU_STENCILOP_INCREMENT_AND_WRAP` — depth_fail_op for X-ray marking
- `SDL_GPU_COMPAREOP_NOT_EQUAL` — stencil test for ghost pass (ref=0, pass where >0)
- `SDL_GPU_BLENDFACTOR_ONE` (src + dst) — additive blending for ghost glow
- `SDL_GPUTextureSupportsFormat` — negotiate D24S8 with SAMPLER usage

## Common mistakes

- **Forgetting MRT pipeline color target count** — The pipeline must declare
  the same number of color target descriptions as render pass color targets.
  Mismatched counts cause validation errors or undefined behavior.
- **Wrong depth_fail_op direction** — `depth_fail_op` fires when the fragment
  is behind existing depth. Make sure the scene depth is already established
  before the X-ray mark pass.
- **Not disabling depth writes for X-ray mark** — If the mark pass writes
  depth, it corrupts the depth buffer and prevents the ghost pass from
  rendering correctly.
- **Missing stencil clear** — Stale stencil values from the previous frame
  cause ghost artifacts everywhere. Always clear stencil at pass start.
- **Sobel on linear depth vs hyperbolic depth** — Raw depth buffer values
  are hyperbolic (non-linear). For better edge detection, linearize depth
  first or adjust the depth scale threshold.

## Cross-references

- [GPU Lesson 36 — Edge Detection](../../../lessons/gpu/36-edge-detection/)
  for the full walkthrough
- [GPU Lesson 34 — Stencil Testing](../../../lessons/gpu/34-stencil-testing/)
  for stencil buffer fundamentals and stencil-expansion outlines
- [GPU Lesson 27 — SSAO](../../../lessons/gpu/27-ssao/)
  for G-buffer and view-space normal techniques
- [GPU Lesson 15 — Shadow Maps](../../../lessons/gpu/15-cascaded-shadow-maps/)
  for depth-only render passes
- [GPU Lesson 16 — Blending](../../../lessons/gpu/16-blending/)
  for blend state configuration (additive blending)
