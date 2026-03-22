---
name: forge-stencil-testing
description: >
  Add stencil buffer testing to an SDL GPU project. Configure depth-stencil
  textures with stencil bits, set up stencil state on pipelines, and use
  stencil operations for portals, outlines, and per-pixel masking.
triggers:
  - stencil
  - portal effect
  - object outline
  - stencil mask
  - stencil buffer
  - per-pixel masking
---

# Stencil Testing

Add stencil buffer support to an SDL GPU project. This skill covers
depth-stencil texture format selection, pipeline stencil state configuration,
and common stencil techniques (portals, outlines, debug visualization).

Based on [GPU Lesson 34](../../../lessons/gpu/34-stencil-testing/).

## When to use

- You need per-pixel masking to control where fragments are drawn
- You want a portal or window showing a different scene
- You want object outlines for selection or highlighting
- You need to combine multiple rendering effects with per-pixel control

## Depth-stencil texture format

The depth-stencil texture **must** include stencil bits. Use
`SDL_GPU_TEXTUREFORMAT_D24_UNORM_S8_UINT` (24-bit depth + 8-bit stencil)
as the primary choice, with `SDL_GPU_TEXTUREFORMAT_D32_FLOAT_S8_UINT` as
fallback.

```c
/* Check for D24_UNORM_S8_UINT support first */
SDL_GPUTextureFormat depth_stencil_fmt;
if (SDL_GPUTextureSupportsFormat(device,
        SDL_GPU_TEXTUREFORMAT_D24_UNORM_S8_UINT,
        SDL_GPU_TEXTURETYPE_2D,
        SDL_GPU_TEXTUREUSAGE_DEPTH_STENCIL_TARGET)) {
    depth_stencil_fmt = SDL_GPU_TEXTUREFORMAT_D24_UNORM_S8_UINT;
} else {
    depth_stencil_fmt = SDL_GPU_TEXTUREFORMAT_D32_FLOAT_S8_UINT;
}
```

Without the `_S8_UINT` suffix, there is no stencil buffer and all stencil
operations silently do nothing.

## Pipeline stencil state

Stencil testing is configured on the pipeline, not in shaders:

```c
SDL_GPUGraphicsPipelineCreateInfo pi = { /* ... */ };
pi.depth_stencil_state.enable_stencil_test = true;
pi.depth_stencil_state.front_stencil_state = (SDL_GPUStencilOpState){
    .fail_op      = SDL_GPU_STENCILOP_KEEP,
    .pass_op      = SDL_GPU_STENCILOP_REPLACE,
    .depth_fail_op = SDL_GPU_STENCILOP_KEEP,
    .compare_op   = SDL_GPU_COMPAREOP_ALWAYS,
};
pi.depth_stencil_state.back_stencil_state =
    pi.depth_stencil_state.front_stencil_state;
pi.depth_stencil_state.compare_mask = 0xFF;
pi.depth_stencil_state.write_mask   = 0xFF;
```

The reference value is set per-draw call:

```c
SDL_SetGPUStencilReference(render_pass, reference_value);
```

## Portal technique (4 passes)

1. **Main world pass** — Draw regular scene geometry first:
   - Stencil test disabled, normal depth write
   - Establishes depth so the mask respects occlusion

2. **Mask pipeline** — Write stencil, no color/depth:
   - `compare_op = ALWAYS`, `pass_op = REPLACE`, ref = 1
   - Color write mask = 0, depth write = false
   - Draw an invisible quad filling the portal opening
   - Depth test still active — mask only writes where no closer geometry exists

3. **Portal world pipeline** — Draw inside portal only:
   - `compare_op = EQUAL`, ref = 1, `pass_op = KEEP`
   - Draw alternate-world objects (only pass where stencil == 1)

4. **Frame pipeline** — Draw portal frame geometry:
   - Stencil test disabled or `compare_op = ALWAYS`
   - Normal color + depth writes

## Outline technique (2 pipelines)

1. **Outline write** — Draw object normally, writing stencil:
   - `compare_op = ALWAYS`, `pass_op = REPLACE`, ref = 2
   - Normal rendering + stencil write

2. **Outline draw** — Draw scaled-up object where stencil != ref:
   - `compare_op = NOT_EQUAL`, ref = 2
   - Scale object 3-5% larger, output solid outline color
   - Only the border ring passes (interior rejected by stencil)

Scale for outlines:

```c
mat4 outline_model = mat4_multiply(
    mat4_translate(object_position),
    mat4_multiply(
        mat4_scale_uniform(1.04f),
        mat4_translate(vec3_negate(object_position))
    )
);
```

## Clearing stencil

Clear stencil alongside depth when beginning the render pass:

```c
SDL_GPUDepthStencilTargetInfo ds_target = {
    .texture       = depth_stencil_texture,
    .load_op       = SDL_GPU_LOADOP_CLEAR,
    .store_op      = SDL_GPU_STOREOP_STORE,
    .clear_depth   = 1.0f,
    .clear_stencil = 0,
    .stencil_load_op  = SDL_GPU_LOADOP_CLEAR,
    .stencil_store_op = SDL_GPU_STOREOP_STORE,
};
```

## Disabling color writes (for mask pipeline)

```c
SDL_GPUColorTargetDescription ctd = {
    .format = swapchain_format,
    .blend_state = {
        .color_write_mask = 0,  /* write nothing to color */
    },
};
```

## Key API calls

- `SDL_GPUTextureSupportsFormat()` — check depth-stencil format support
- `SDL_CreateGPUTexture()` with `D24_UNORM_S8_UINT` — create depth-stencil target
- `SDL_GPUStencilOpState` — configure compare_op, pass_op, fail_op, depth_fail_op
- `SDL_SetGPUStencilReference()` — set per-draw stencil reference value
- `SDL_GPUGraphicsPipelineCreateInfo.depth_stencil_state` — embed stencil config in pipeline

## Common mistakes

- **Missing `_S8_UINT` suffix** — Using `D24_UNORM` or `D32_FLOAT` without
  `_S8_UINT` creates a texture with no stencil bits. All stencil operations
  silently do nothing.
- **Forgetting to clear stencil** — Set `stencil_load_op = SDL_GPU_LOADOP_CLEAR`
  and `clear_stencil = 0` on the depth-stencil target info. Without this,
  stale stencil values from the previous frame cause artifacts.
- **Wrong draw order** — Main-world occluders must render before the portal
  mask so the depth buffer is established. The mask then only writes stencil
  where no closer geometry exists. Outline writes must happen after the main
  world so the outline reference value does not collide with the portal reference.
- **Not disabling depth writes for mask** — The mask quad must not write depth,
  or it will occlude objects drawn behind it in the portal world.
- **Forgetting to set both front and back stencil** — If back-face culling is
  off, both `front_stencil_state` and `back_stencil_state` must be configured.

## Ready-to-use template

```c
/* Minimal stencil mask + conditional draw setup */

/* 1. Create depth-stencil texture with stencil bits */
SDL_GPUTextureFormat ds_fmt = SDL_GPU_TEXTUREFORMAT_D24_UNORM_S8_UINT;
/* ... create texture with ds_fmt ... */

/* 2. Mask pipeline: write stencil, no color/depth */
SDL_GPUStencilOpState mask_stencil = {
    .fail_op    = SDL_GPU_STENCILOP_KEEP,
    .pass_op    = SDL_GPU_STENCILOP_REPLACE,
    .depth_fail_op = SDL_GPU_STENCILOP_KEEP,
    .compare_op = SDL_GPU_COMPAREOP_ALWAYS,
};
/* pi.depth_stencil_state.enable_stencil_test = true; */
/* pi.depth_stencil_state.front/back = mask_stencil; */
/* color_write_mask = 0, depth_write = false */

/* 3. Conditional pipeline: draw only where stencil matches */
SDL_GPUStencilOpState cond_stencil = {
    .fail_op    = SDL_GPU_STENCILOP_KEEP,
    .pass_op    = SDL_GPU_STENCILOP_KEEP,
    .depth_fail_op = SDL_GPU_STENCILOP_KEEP,
    .compare_op = SDL_GPU_COMPAREOP_EQUAL, /* or NOT_EQUAL */
};

/* 4. At draw time */
SDL_SetGPUStencilReference(render_pass, 1);
/* Draw mask geometry with mask pipeline */
/* Draw scene with conditional pipeline */
```

## Stencil operations reference

| Operation | Effect |
|-----------|--------|
| KEEP | Leave stencil unchanged |
| ZERO | Set to 0 |
| REPLACE | Set to reference value |
| INCREMENT_AND_CLAMP | Increment, clamp to 255 |
| DECREMENT_AND_CLAMP | Decrement, clamp to 0 |
| INVERT | Bitwise NOT |
| INCREMENT_AND_WRAP | Increment, wrap 255 to 0 |
| DECREMENT_AND_WRAP | Decrement, wrap 0 to 255 |

## Cross-references

- [GPU Lesson 34 — Portals & Outlines](../../../lessons/gpu/34-stencil-testing/)
  for the full walkthrough
- [GPU Lesson 06 — Depth & 3D](../../../lessons/gpu/06-depth-and-3d/)
  for depth buffer fundamentals
- [GPU Lesson 15 — Cascaded Shadow Maps](../../../lessons/gpu/15-cascaded-shadow-maps/)
  for depth-only render passes
