---
name: forge-blending
description: Add alpha blending, alpha testing, or additive blending to an SDL GPU project. Configure blend state, sort transparent objects, and set up clip/discard for cutout transparency.
---

Add transparency and blending to an SDL3 GPU application. Based on Lesson 16.

## When to use

- You need transparent or semi-transparent surfaces (glass, windows, UI)
- You need cutout transparency (foliage, fences, decals)
- You need luminous additive effects (fire, lasers, particle trails)
- You need to render glTF models with BLEND or MASK alpha modes

## Key API calls

- `SDL_CreateGPUGraphicsPipeline` — blend state in `SDL_GPUColorTargetBlendState`
- `SDL_GPU_BLENDFACTOR_SRC_ALPHA` / `SDL_GPU_BLENDFACTOR_ONE_MINUS_SRC_ALPHA` — standard blend
- `SDL_GPU_BLENDFACTOR_ONE` — additive blend (dst factor) or premultiplied (src factor)
- `SDL_GPU_BLENDOP_ADD` — most common blend operation
- `clip()` in HLSL — discard fragments below an alpha threshold

## Correct order

1. **Create pipelines** (in `SDL_AppInit`)
   - Opaque pipeline: no blend, depth write ON
   - Alpha-test pipeline: no blend, depth write ON, fragment shader uses `clip()`
   - Standard blend pipeline: blend enabled, depth write OFF
   - Additive pipeline: blend enabled (ONE dst factor), depth write OFF
2. **Each frame — draw in this order:**
   a. Opaque geometry (any order) — fills the depth buffer
   b. Alpha-tested geometry (any order) — clip/discard, writes depth for visible pixels
   c. Alpha-blended geometry (sorted back-to-front) — reads but does not write depth
   d. Additive geometry (any order) — commutative, no sorting needed

## Key concepts

1. **Depth write OFF** for all blended pipelines — semi-transparent surfaces must not occlude geometry behind them
2. **Depth test ON** for blended pipelines — transparent surfaces still appear behind opaque ones
3. **Back-to-front sorting** required for standard alpha blend (not for additive)
4. **Same shader works** for opaque and blended — the difference is pipeline config
5. **Alpha test** uses a different shader (with `clip()`) but no blend state
6. **Cull mode NONE** for transparent surfaces — both sides are often visible

## Pipeline setup

### Standard alpha blend

```c
SDL_GPUColorTargetDescription color_target;
SDL_zero(color_target);
color_target.format = swapchain_format;
color_target.blend_state.enable_blend = true;

/* Color: src * srcAlpha + dst * (1 - srcAlpha) */
color_target.blend_state.src_color_blendfactor = SDL_GPU_BLENDFACTOR_SRC_ALPHA;
color_target.blend_state.dst_color_blendfactor = SDL_GPU_BLENDFACTOR_ONE_MINUS_SRC_ALPHA;
color_target.blend_state.color_blend_op = SDL_GPU_BLENDOP_ADD;

/* Alpha: src * 1 + dst * (1 - srcAlpha) */
color_target.blend_state.src_alpha_blendfactor = SDL_GPU_BLENDFACTOR_ONE;
color_target.blend_state.dst_alpha_blendfactor = SDL_GPU_BLENDFACTOR_ONE_MINUS_SRC_ALPHA;
color_target.blend_state.alpha_blend_op = SDL_GPU_BLENDOP_ADD;

color_target.blend_state.color_write_mask =
    SDL_GPU_COLORCOMPONENT_R | SDL_GPU_COLORCOMPONENT_G |
    SDL_GPU_COLORCOMPONENT_B | SDL_GPU_COLORCOMPONENT_A;

/* CRITICAL: depth write must be OFF */
pipe.depth_stencil_state.enable_depth_test = true;
pipe.depth_stencil_state.enable_depth_write = false;  /* <-- key difference */
pipe.depth_stencil_state.compare_op = SDL_GPU_COMPAREOP_LESS_OR_EQUAL;
```

### Additive blend

```c
/* Only the blend factors differ from standard blend */
color_target.blend_state.src_color_blendfactor = SDL_GPU_BLENDFACTOR_SRC_ALPHA;
color_target.blend_state.dst_color_blendfactor = SDL_GPU_BLENDFACTOR_ONE;  /* additive */
color_target.blend_state.color_blend_op = SDL_GPU_BLENDOP_ADD;

/* Alpha: preserve existing */
color_target.blend_state.src_alpha_blendfactor = SDL_GPU_BLENDFACTOR_ZERO;
color_target.blend_state.dst_alpha_blendfactor = SDL_GPU_BLENDFACTOR_ONE;
```

### Premultiplied alpha

```c
/* src factor is ONE (not SRC_ALPHA) because RGB already includes alpha */
color_target.blend_state.src_color_blendfactor = SDL_GPU_BLENDFACTOR_ONE;
color_target.blend_state.dst_color_blendfactor = SDL_GPU_BLENDFACTOR_ONE_MINUS_SRC_ALPHA;
```

## Alpha test shader (HLSL)

```hlsl
float4 main(PSInput input) : SV_Target
{
    float4 texel = diffuse_tex.Sample(diffuse_smp, input.uv);
    float4 color = texel * base_color;
    clip(color.a - alpha_cutoff);  /* discard if alpha < cutoff */
    return color;
}
```

## Back-to-front sorting

Sort by the **nearest point on each object's world-space AABB** to the
camera, not the object center. Center-distance sorting fails when two
transparent objects share the same node position (e.g., a flat plane inside
a glass box). The AABB nearest-point distance correctly distinguishes them
because the box's front face is closer to the camera than the interior plane.

```c
/* Compute mesh-local AABB once during upload (min/max of vertex positions).
 * Each frame, transform it to world space with Arvo's method, then sort. */
vec3 w_min, w_max;
transform_aabb(&node->world_transform, prim->aabb_min, prim->aabb_max,
               &w_min, &w_max);

/* Clamp camera position to AABB to find nearest point */
float nx = clamp(cam.x, w_min.x, w_max.x);
float ny = clamp(cam.y, w_min.y, w_max.y);
float nz = clamp(cam.z, w_min.z, w_max.z);
float dist = vec3_length(vec3_sub(vec3_create(nx, ny, nz), cam));

/* Sort descending by distance (farthest nearest-point first) */
SDL_qsort(draws, count, sizeof(BlendDraw), compare_back_to_front);
```

## Using glTF alpha modes

The glTF parser (`forge_gltf.h`) exposes `alpha_mode`, `alpha_cutoff`, and
`double_sided` on each `ForgeGltfMaterial`. Use these to select the correct
pipeline per primitive:

```c
/* Create one pipeline per alpha mode, then select at draw time: */
switch (gpu_materials[prim->material_index].alpha_mode) {
    case FORGE_GLTF_ALPHA_OPAQUE: SDL_BindGPUGraphicsPipeline(pass, opaque_pipeline); break;
    case FORGE_GLTF_ALPHA_MASK:   SDL_BindGPUGraphicsPipeline(pass, alpha_test_pipeline); break;
    case FORGE_GLTF_ALPHA_BLEND:  SDL_BindGPUGraphicsPipeline(pass, blend_pipeline); break;
}
```

**Never extract individual assets from a glTF model.** Always load the complete
model with `forge_gltf_load()` and use its transforms, materials, and textures
to drive the scene.

## Code template

A minimal SDL3 GPU program that sets up four pipelines (opaque, alpha test,
standard blend, additive blend) and draws geometry in the correct order.
Copy into an existing SDL GPU project and adapt to your scene.

```c
/* ── 1. Create pipelines (in SDL_AppInit) ─────────────────────────── */

SDL_GPUTextureFormat swapchain_format =
    SDL_GetGPUSwapchainTextureFormat(device, window);

/* Shared vertex layout (position + normal + uv) */
SDL_GPUVertexBufferDescription vb_desc;
SDL_zero(vb_desc);
vb_desc.slot = 0;
vb_desc.pitch = sizeof(MyVertex);
vb_desc.input_rate = SDL_GPU_VERTEXINPUTRATE_VERTEX;
vb_desc.instance_step_rate = 0;

/* --- 1a. Opaque pipeline: no blend, depth write ON --- */
{
    SDL_GPUColorTargetDescription ctd;
    SDL_zero(ctd);
    ctd.format = swapchain_format;

    SDL_GPUGraphicsPipelineCreateInfo pipe;
    SDL_zero(pipe);
    pipe.vertex_shader = scene_vs;
    pipe.fragment_shader = scene_fs;
    pipe.vertex_input_state.vertex_buffer_descriptions = &vb_desc;
    pipe.vertex_input_state.num_vertex_buffers = 1;
    pipe.vertex_input_state.vertex_attributes = attrs;
    pipe.vertex_input_state.num_vertex_attributes = attr_count;
    pipe.primitive_type = SDL_GPU_PRIMITIVETYPE_TRIANGLELIST;
    pipe.rasterizer_state.fill_mode = SDL_GPU_FILLMODE_FILL;
    pipe.rasterizer_state.cull_mode = SDL_GPU_CULLMODE_BACK;
    pipe.depth_stencil_state.enable_depth_test = true;
    pipe.depth_stencil_state.enable_depth_write = true;
    pipe.depth_stencil_state.compare_op = SDL_GPU_COMPAREOP_LESS_OR_EQUAL;
    pipe.target_info.color_target_descriptions = &ctd;
    pipe.target_info.num_color_targets = 1;
    pipe.target_info.has_depth_stencil_target = true;
    pipe.target_info.depth_stencil_format = SDL_GPU_TEXTUREFORMAT_D32_FLOAT;

    opaque_pipeline = SDL_CreateGPUGraphicsPipeline(device, &pipe);
}

/* --- 1b. Alpha test pipeline: no blend, depth write ON, clip() shader --- */
{
    SDL_GPUColorTargetDescription ctd;
    SDL_zero(ctd);
    ctd.format = swapchain_format;

    SDL_GPUGraphicsPipelineCreateInfo pipe;
    SDL_zero(pipe);
    pipe.vertex_shader = scene_vs;
    pipe.fragment_shader = alpha_test_fs;  /* uses clip() */
    pipe.vertex_input_state.vertex_buffer_descriptions = &vb_desc;
    pipe.vertex_input_state.num_vertex_buffers = 1;
    pipe.vertex_input_state.vertex_attributes = attrs;
    pipe.vertex_input_state.num_vertex_attributes = attr_count;
    pipe.primitive_type = SDL_GPU_PRIMITIVETYPE_TRIANGLELIST;
    pipe.rasterizer_state.fill_mode = SDL_GPU_FILLMODE_FILL;
    pipe.rasterizer_state.cull_mode = SDL_GPU_CULLMODE_NONE; /* often double-sided */
    pipe.depth_stencil_state.enable_depth_test = true;
    pipe.depth_stencil_state.enable_depth_write = true;      /* survivors are opaque */
    pipe.depth_stencil_state.compare_op = SDL_GPU_COMPAREOP_LESS_OR_EQUAL;
    pipe.target_info.color_target_descriptions = &ctd;
    pipe.target_info.num_color_targets = 1;
    pipe.target_info.has_depth_stencil_target = true;
    pipe.target_info.depth_stencil_format = SDL_GPU_TEXTUREFORMAT_D32_FLOAT;

    alpha_test_pipeline = SDL_CreateGPUGraphicsPipeline(device, &pipe);
}

/* --- 1c. Standard alpha blend pipeline: blend ON, depth write OFF --- */
{
    SDL_GPUColorTargetDescription ctd;
    SDL_zero(ctd);
    ctd.format = swapchain_format;
    ctd.blend_state.enable_blend = true;
    /* Color: src * srcAlpha + dst * (1 - srcAlpha) */
    ctd.blend_state.src_color_blendfactor = SDL_GPU_BLENDFACTOR_SRC_ALPHA;
    ctd.blend_state.dst_color_blendfactor = SDL_GPU_BLENDFACTOR_ONE_MINUS_SRC_ALPHA;
    ctd.blend_state.color_blend_op = SDL_GPU_BLENDOP_ADD;
    /* Alpha: src * 1 + dst * (1 - srcAlpha) */
    ctd.blend_state.src_alpha_blendfactor = SDL_GPU_BLENDFACTOR_ONE;
    ctd.blend_state.dst_alpha_blendfactor = SDL_GPU_BLENDFACTOR_ONE_MINUS_SRC_ALPHA;
    ctd.blend_state.alpha_blend_op = SDL_GPU_BLENDOP_ADD;
    ctd.blend_state.color_write_mask =
        SDL_GPU_COLORCOMPONENT_R | SDL_GPU_COLORCOMPONENT_G |
        SDL_GPU_COLORCOMPONENT_B | SDL_GPU_COLORCOMPONENT_A;

    SDL_GPUGraphicsPipelineCreateInfo pipe;
    SDL_zero(pipe);
    pipe.vertex_shader = scene_vs;
    pipe.fragment_shader = scene_fs;      /* same shader as opaque */
    pipe.vertex_input_state.vertex_buffer_descriptions = &vb_desc;
    pipe.vertex_input_state.num_vertex_buffers = 1;
    pipe.vertex_input_state.vertex_attributes = attrs;
    pipe.vertex_input_state.num_vertex_attributes = attr_count;
    pipe.primitive_type = SDL_GPU_PRIMITIVETYPE_TRIANGLELIST;
    pipe.rasterizer_state.fill_mode = SDL_GPU_FILLMODE_FILL;
    pipe.rasterizer_state.cull_mode = SDL_GPU_CULLMODE_NONE; /* both sides visible */
    pipe.depth_stencil_state.enable_depth_test = true;
    pipe.depth_stencil_state.enable_depth_write = false;     /* CRITICAL: OFF */
    pipe.depth_stencil_state.compare_op = SDL_GPU_COMPAREOP_LESS_OR_EQUAL;
    pipe.target_info.color_target_descriptions = &ctd;
    pipe.target_info.num_color_targets = 1;
    pipe.target_info.has_depth_stencil_target = true;
    pipe.target_info.depth_stencil_format = SDL_GPU_TEXTUREFORMAT_D32_FLOAT;

    blend_pipeline = SDL_CreateGPUGraphicsPipeline(device, &pipe);
}

/* --- 1d. Additive blend pipeline: ONE dst factor, depth write OFF --- */
{
    SDL_GPUColorTargetDescription ctd;
    SDL_zero(ctd);
    ctd.format = swapchain_format;
    ctd.blend_state.enable_blend = true;
    /* Color: src * srcAlpha + dst * ONE (additive) */
    ctd.blend_state.src_color_blendfactor = SDL_GPU_BLENDFACTOR_SRC_ALPHA;
    ctd.blend_state.dst_color_blendfactor = SDL_GPU_BLENDFACTOR_ONE;
    ctd.blend_state.color_blend_op = SDL_GPU_BLENDOP_ADD;
    /* Alpha: preserve destination */
    ctd.blend_state.src_alpha_blendfactor = SDL_GPU_BLENDFACTOR_ZERO;
    ctd.blend_state.dst_alpha_blendfactor = SDL_GPU_BLENDFACTOR_ONE;
    ctd.blend_state.alpha_blend_op = SDL_GPU_BLENDOP_ADD;
    ctd.blend_state.color_write_mask =
        SDL_GPU_COLORCOMPONENT_R | SDL_GPU_COLORCOMPONENT_G |
        SDL_GPU_COLORCOMPONENT_B | SDL_GPU_COLORCOMPONENT_A;

    SDL_GPUGraphicsPipelineCreateInfo pipe;
    SDL_zero(pipe);
    pipe.vertex_shader = scene_vs;
    pipe.fragment_shader = scene_fs;
    pipe.vertex_input_state.vertex_buffer_descriptions = &vb_desc;
    pipe.vertex_input_state.num_vertex_buffers = 1;
    pipe.vertex_input_state.vertex_attributes = attrs;
    pipe.vertex_input_state.num_vertex_attributes = attr_count;
    pipe.primitive_type = SDL_GPU_PRIMITIVETYPE_TRIANGLELIST;
    pipe.rasterizer_state.fill_mode = SDL_GPU_FILLMODE_FILL;
    pipe.rasterizer_state.cull_mode = SDL_GPU_CULLMODE_NONE;
    pipe.depth_stencil_state.enable_depth_test = true;
    pipe.depth_stencil_state.enable_depth_write = false;     /* OFF for all blended */
    pipe.depth_stencil_state.compare_op = SDL_GPU_COMPAREOP_LESS_OR_EQUAL;
    pipe.target_info.color_target_descriptions = &ctd;
    pipe.target_info.num_color_targets = 1;
    pipe.target_info.has_depth_stencil_target = true;
    pipe.target_info.depth_stencil_format = SDL_GPU_TEXTUREFORMAT_D32_FLOAT;

    additive_pipeline = SDL_CreateGPUGraphicsPipeline(device, &pipe);
}

/* Release shaders — pipelines keep their own copy */
SDL_ReleaseGPUShader(device, alpha_test_fs);
SDL_ReleaseGPUShader(device, scene_fs);
SDL_ReleaseGPUShader(device, scene_vs);
```

### Alpha test fragment shader (HLSL)

```hlsl
/* alpha_test.frag.hlsl — discard fragments below alpha cutoff */

Texture2D    diffuse_tex : register(t0, space2);
SamplerState diffuse_smp : register(s0, space2);

cbuffer FragUniforms : register(b0, space3) {
    float4 base_color;
    float  alpha_cutoff;
    float  has_texture;
};

struct PSInput {
    float4 position : SV_Position;
    float2 uv       : TEXCOORD2;
};

float4 main(PSInput input) : SV_Target {
    float4 texel = has_texture > 0.5
        ? diffuse_tex.Sample(diffuse_smp, input.uv)
        : float4(1, 1, 1, 1);
    float4 color = texel * base_color;
    clip(color.a - alpha_cutoff);  /* discard if alpha < cutoff */
    return color;
}
```

### Draw loop (in SDL_AppIterate)

```c
/* ── 2. Draw in strict order: opaque → alpha test → blend → additive ── */

SDL_GPURenderPass *pass = SDL_BeginGPURenderPass(
    cmd, &color_target, 1, &depth_target);

/* --- 2a. Opaque geometry (any order) --- */
SDL_BindGPUGraphicsPipeline(pass, opaque_pipeline);
for (int i = 0; i < opaque_count; i++) {
    draw_mesh(pass, cmd, &opaque_meshes[i], &vp);
}

/* --- 2b. Alpha-tested geometry (any order) --- */
SDL_BindGPUGraphicsPipeline(pass, alpha_test_pipeline);
for (int i = 0; i < mask_count; i++) {
    draw_mesh(pass, cmd, &mask_meshes[i], &vp);
}

/* --- 2c. Alpha-blended geometry (sorted back-to-front) --- */
/* Sort by nearest AABB distance to camera (farthest first) */
for (int i = 0; i < blend_count; i++) {
    vec3 w_min, w_max;
    transform_aabb(&blend_meshes[i].world_transform,
                   blend_meshes[i].aabb_min, blend_meshes[i].aabb_max,
                   &w_min, &w_max);
    float nx = forge_clampf(cam_pos.x, w_min.x, w_max.x);
    float ny = forge_clampf(cam_pos.y, w_min.y, w_max.y);
    float nz = forge_clampf(cam_pos.z, w_min.z, w_max.z);
    blend_meshes[i].sort_dist = vec3_length(
        vec3_sub(vec3_create(nx, ny, nz), cam_pos));
}
SDL_qsort(blend_meshes, blend_count, sizeof(BlendDraw),
           compare_back_to_front);

SDL_BindGPUGraphicsPipeline(pass, blend_pipeline);
for (int i = 0; i < blend_count; i++) {
    draw_mesh(pass, cmd, &blend_meshes[i], &vp);
}

/* --- 2d. Additive geometry (any order — commutative) --- */
SDL_BindGPUGraphicsPipeline(pass, additive_pipeline);
for (int i = 0; i < additive_count; i++) {
    draw_mesh(pass, cmd, &additive_meshes[i], &vp);
}

SDL_EndGPURenderPass(pass);
```

## Common mistakes

1. **Forgetting to disable depth write** for blended pipelines — transparent surfaces block everything behind them
2. **Not sorting** alpha-blended objects — produces incorrect visual results (artifacts depend on draw order)
3. **Sorting by center distance instead of AABB nearest point** — fails when objects share the same node position (e.g., a plane inside a box). Use the nearest point on the world-space AABB for correct ordering
4. **Using alpha blend where alpha test suffices** — alpha test is faster (no sorting, writes depth) and correct for binary transparency
5. **Sorting additive objects** — unnecessary; additive blending is commutative
6. **Drawing transparent objects before opaque** — transparent objects need the depth buffer filled by opaque geometry first
7. **Using `SRC_ALPHA` for premultiplied textures** — premultiplied textures need `ONE` as the source factor
8. **Extracting assets from a glTF à la carte** — always load the complete model and use its scene data
