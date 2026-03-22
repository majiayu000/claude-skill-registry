---
name: forge-3d-picking
description: >
  Add GPU-based 3D object picking to an SDL GPU project. Implement color-ID
  picking with offscreen render targets, stencil-ID picking with per-object
  reference values, GPU-to-CPU readback with transfer buffers, and stencil
  outline selection highlighting.
triggers:
  - 3d picking
  - object picking
  - object selection
  - color picking
  - click to select
  - GPU readback
  - mouse picking
  - ray picking
  - select object
---

# 3D Picking

Add GPU-based object picking to an SDL GPU project. This skill covers two
picking methods (color-ID and stencil-ID), GPU-to-CPU data transfer with
`SDL_DownloadFromGPUTexture`, transfer buffer readback, and stencil outline
selection highlighting.

Based on [GPU Lesson 37](../../../lessons/gpu/37-3d-picking/).

## When to use

- You need to identify which object the user clicked on in a 3D scene
- You want pixel-perfect selection without CPU-side ray casting
- You need to highlight selected objects with a visible outline
- You want to read data back from the GPU to the CPU

## Color-ID picking pipeline

Color-ID picking renders each object with a unique flat color to an offscreen
texture, then reads back the single pixel under the cursor to identify the
object. This is the recommended approach — it is portable, supports up to
65,535 objects, and the RGBA readback has a consistent byte layout across all
GPU backends.

### Index-to-color encoding

```c
/* Convert object index to a unique RGB color.
 * Index 0 maps to ID 1 (background is (0,0,0) = no object). */
static void index_to_color(int index, float *r, float *g, float *b)
{
    int id = index + 1;
    *r = (float)((id >> 0) & 0xFF) / 255.0f;
    *g = (float)((id >> 8) & 0xFF) / 255.0f;
    *b = 0.0f;
}

/* Decode a read-back pixel back to an object index. Returns -1 for background. */
static int color_to_index(Uint8 r, Uint8 g, Uint8 b)
{
    (void)b;
    int id = (int)r | ((int)g << 8);
    if (id == 0) return -1;
    return id - 1;
}
```

### Offscreen render target

Create an `R8G8B8A8_UNORM` texture as the color-ID render target. Do **not** use
the swapchain format — you need a known pixel layout for reliable CPU readback.
Also create a separate depth buffer for occlusion:

```c
/* Color-ID offscreen target */
SDL_GPUTextureCreateInfo ci;
SDL_zero(ci);
ci.type   = SDL_GPU_TEXTURETYPE_2D;
ci.format = SDL_GPU_TEXTUREFORMAT_R8G8B8A8_UNORM;
ci.width  = window_w;
ci.height = window_h;
ci.layer_count_or_depth = 1;
ci.num_levels = 1;
ci.usage  = SDL_GPU_TEXTUREUSAGE_COLOR_TARGET;
SDL_GPUTexture *id_texture = SDL_CreateGPUTexture(device, &ci);

/* ID pass depth buffer — separate from the main scene depth */
SDL_GPUTextureCreateInfo depth_ci;
SDL_zero(depth_ci);
depth_ci.type   = SDL_GPU_TEXTURETYPE_2D;
depth_ci.format = depth_stencil_fmt;  /* D24_UNORM_S8_UINT or D32_FLOAT_S8_UINT */
depth_ci.width  = window_w;
depth_ci.height = window_h;
depth_ci.layer_count_or_depth = 1;
depth_ci.num_levels = 1;
depth_ci.usage  = SDL_GPU_TEXTUREUSAGE_DEPTH_STENCIL_TARGET;
SDL_GPUTexture *id_depth = SDL_CreateGPUTexture(device, &depth_ci);
```

### ID pass shaders

The vertex shader only needs MVP — no lighting outputs:

```hlsl
cbuffer IdVertUniforms : register(b0, space1)
{
    column_major float4x4 mvp;
};

struct VSInput
{
    float3 position : TEXCOORD0;
    float3 normal   : TEXCOORD1;  /* unused — must match vertex layout */
};

float4 main(VSInput input) : SV_Position
{
    return mul(mvp, float4(input.position, 1.0));
}
```

The fragment shader outputs the flat ID color:

```hlsl
cbuffer IdFragUniforms : register(b0, space3)
{
    float4 id_color;
};

float4 main(float4 pos : SV_Position) : SV_Target
{
    return id_color;
}
```

### ID pipeline configuration

```c
SDL_GPUColorTargetDescription ct;
SDL_zero(ct);
ct.format = SDL_GPU_TEXTUREFORMAT_R8G8B8A8_UNORM;

SDL_GPUGraphicsPipelineCreateInfo pi;
SDL_zero(pi);
pi.vertex_shader   = id_pass_vert;
pi.fragment_shader = id_pass_frag;
pi.vertex_input_state = scene_vis;  /* same vertex layout as scene */
pi.primitive_type = SDL_GPU_PRIMITIVETYPE_TRIANGLELIST;

pi.rasterizer_state.fill_mode = SDL_GPU_FILLMODE_FILL;
pi.rasterizer_state.cull_mode = SDL_GPU_CULLMODE_BACK;
pi.rasterizer_state.front_face = SDL_GPU_FRONTFACE_COUNTER_CLOCKWISE;

pi.depth_stencil_state.compare_op = SDL_GPU_COMPAREOP_LESS;
pi.depth_stencil_state.enable_depth_test  = true;
pi.depth_stencil_state.enable_depth_write = true;
pi.depth_stencil_state.enable_stencil_test = false;

pi.target_info.color_target_descriptions = &ct;
pi.target_info.num_color_targets = 1;
pi.target_info.depth_stencil_format = depth_stencil_fmt;
pi.target_info.has_depth_stencil_target = true;
```

### ID pass execution

Only run the ID pass on click frames to avoid wasting GPU time:

```c
if (pick_pending && picking_method == PICK_COLOR_ID) {
    SDL_GPUColorTargetInfo id_color_target;
    SDL_zero(id_color_target);
    id_color_target.texture  = id_texture;
    id_color_target.load_op  = SDL_GPU_LOADOP_CLEAR;
    id_color_target.store_op = SDL_GPU_STOREOP_STORE;
    /* Clear to (0,0,0,0) — decodes to "no object" */

    SDL_GPUDepthStencilTargetInfo id_ds;
    SDL_zero(id_ds);
    id_ds.texture     = id_depth;
    id_ds.clear_depth = 1.0f;
    id_ds.load_op     = SDL_GPU_LOADOP_CLEAR;
    id_ds.store_op    = SDL_GPU_STOREOP_DONT_CARE;
    id_ds.cycle       = true;

    SDL_GPURenderPass *pass = SDL_BeginGPURenderPass(
        cmd, &id_color_target, 1, &id_ds);
    SDL_BindGPUGraphicsPipeline(pass, id_pipeline);

    for (int i = 0; i < object_count; i++) {
        mat4 mvp = mat4_multiply(cam_vp, object_models[i]);

        IdVertUniforms vu = { .mvp = mvp };
        SDL_PushGPUVertexUniformData(cmd, 0, &vu, sizeof(vu));

        float id_r, id_g, id_b;
        index_to_color(i, &id_r, &id_g, &id_b);
        IdFragUniforms fu = {{ id_r, id_g, id_b, 1.0f }};
        SDL_PushGPUFragmentUniformData(cmd, 0, &fu, sizeof(fu));

        /* Bind and draw object geometry */
        SDL_DrawGPUIndexedPrimitives(pass, idx_count, 1, 0, 0, 0);
    }
    SDL_EndGPURenderPass(pass);
}
```

## GPU readback with SDL_DownloadFromGPUTexture

### Transfer buffer for readback

Create a `DOWNLOAD` transfer buffer once at init. For color-ID picking (RGBA8),
4 bytes suffices. For stencil-ID picking, `D32_FLOAT_S8_UINT` needs 8 bytes per
pixel. Use `SDL_CalculateGPUTextureFormatSize` to size correctly for either:

```c
SDL_GPUTransferBufferCreateInfo xfer_ci;
SDL_zero(xfer_ci);
xfer_ci.usage = SDL_GPU_TRANSFERBUFFERUSAGE_DOWNLOAD;
/* Size for the larger format to support both color-ID and stencil-ID */
Uint32 color_bpp = SDL_CalculateGPUTextureFormatSize(SDL_GPU_TEXTUREFORMAT_R8G8B8A8_UNORM, 1, 1, 1);
Uint32 ds_bpp    = SDL_CalculateGPUTextureFormatSize(ds_format, 1, 1, 1);
xfer_ci.size     = (color_bpp > ds_bpp) ? color_bpp : ds_bpp;
SDL_GPUTransferBuffer *pick_readback = SDL_CreateGPUTransferBuffer(device, &xfer_ci);
```

### Copy pass

Download a single pixel from the source texture into the transfer buffer:

```c
SDL_GPUCopyPass *copy = SDL_BeginGPUCopyPass(cmd);

SDL_GPUTextureRegion src_region;
SDL_zero(src_region);
src_region.texture = id_texture;  /* or depth-stencil for stencil-ID */
src_region.x = (Uint32)pick_x;
src_region.y = (Uint32)pick_y;
src_region.w = 1;
src_region.h = 1;
src_region.d = 1;

SDL_GPUTextureTransferInfo dst_info;
SDL_zero(dst_info);
dst_info.transfer_buffer = pick_readback;
dst_info.offset = 0;

SDL_DownloadFromGPUTexture(copy, &src_region, &dst_info);
SDL_EndGPUCopyPass(copy);
```

### Wait, map, and decode

After submitting the command buffer, wait for GPU completion before reading:

```c
if (!SDL_SubmitGPUCommandBuffer(cmd)) {
    SDL_Log("SDL_SubmitGPUCommandBuffer failed: %s", SDL_GetError());
    return;
}
if (!SDL_WaitForGPUIdle(device)) {
    SDL_Log("SDL_WaitForGPUIdle failed: %s", SDL_GetError());
    return;
}

void *pixel_data = SDL_MapGPUTransferBuffer(device, pick_readback, false);
if (pixel_data) {
    Uint8 *bytes = (Uint8 *)pixel_data;
    int picked = color_to_index(bytes[0], bytes[1], bytes[2]);
    selected_object = (picked >= 0 && picked < object_count) ? picked : -1;
    SDL_UnmapGPUTransferBuffer(device, pick_readback);
}
```

## Stencil-ID picking

An alternative that reuses the scene stencil buffer. Limited to 255 objects
and has backend-dependent byte layout, but requires no extra render pass.

### Pipeline setup

```c
pi.depth_stencil_state.enable_stencil_test = true;
pi.depth_stencil_state.front_stencil_state = (SDL_GPUStencilOpState){
    .fail_op       = SDL_GPU_STENCILOP_KEEP,
    .pass_op       = SDL_GPU_STENCILOP_REPLACE,
    .depth_fail_op = SDL_GPU_STENCILOP_KEEP,
    .compare_op    = SDL_GPU_COMPAREOP_ALWAYS,
};
pi.depth_stencil_state.back_stencil_state =
    pi.depth_stencil_state.front_stencil_state;
pi.depth_stencil_state.write_mask   = 0xFF;
pi.depth_stencil_state.compare_mask = 0xFF;
```

### Per-object stencil reference

```c
for (int i = 0; i < object_count; i++) {
    SDL_SetGPUStencilReference(pass, (Uint8)(i + 1));
    /* ... draw object i ... */
}
```

### D24S8 readback

Download from the depth-stencil texture instead of the ID texture. The stencil
byte position varies by GPU vendor:

```c
Uint8 stencil = bytes[3];
int picked = (int)stencil - 1;
if (picked < 0 || picked >= object_count) {
    stencil = bytes[0];  /* fallback for reversed byte order */
    picked = (int)stencil - 1;
}
```

## Selection outline with stencil

Highlight the selected object using the two-pass stencil outline technique from
[Lesson 34](../../../lessons/gpu/34-stencil-testing/):

### Outline write pipeline

```c
/* Pass 1: draw selected object, write stencil marker */
pi.depth_stencil_state.enable_stencil_test = true;
pi.depth_stencil_state.front_stencil_state = (SDL_GPUStencilOpState){
    .fail_op       = SDL_GPU_STENCILOP_KEEP,
    .pass_op       = SDL_GPU_STENCILOP_REPLACE,
    .depth_fail_op = SDL_GPU_STENCILOP_KEEP,
    .compare_op    = SDL_GPU_COMPAREOP_ALWAYS,
};
pi.depth_stencil_state.back_stencil_state =
    pi.depth_stencil_state.front_stencil_state;
pi.depth_stencil_state.write_mask   = 0xFF;
pi.depth_stencil_state.compare_mask = 0xFF;
```

### Outline draw pipeline

```c
/* Pass 2: draw scaled-up object where stencil != marker */
pi.depth_stencil_state.enable_depth_test  = false;
pi.depth_stencil_state.enable_depth_write = false;
pi.depth_stencil_state.enable_stencil_test = true;
pi.depth_stencil_state.front_stencil_state = (SDL_GPUStencilOpState){
    .fail_op       = SDL_GPU_STENCILOP_KEEP,
    .pass_op       = SDL_GPU_STENCILOP_KEEP,
    .depth_fail_op = SDL_GPU_STENCILOP_KEEP,
    .compare_op    = SDL_GPU_COMPAREOP_NOT_EQUAL,
};
pi.depth_stencil_state.back_stencil_state =
    pi.depth_stencil_state.front_stencil_state;
pi.depth_stencil_state.write_mask   = 0x00;  /* don't modify stencil */
pi.depth_stencil_state.compare_mask = 0xFF;
pi.rasterizer_state.cull_mode = SDL_GPU_CULLMODE_NONE;
```

### Outline rendering

```c
#define STENCIL_OUTLINE  200  /* high value to avoid picking collisions */
#define OUTLINE_SCALE    1.04f

/* Outline pass: LOAD color + depth, CLEAR stencil */
SDL_GPUColorTargetInfo outline_color = {
    .texture  = swapchain_tex,
    .load_op  = SDL_GPU_LOADOP_LOAD,
    .store_op = SDL_GPU_STOREOP_STORE,
};
SDL_GPUDepthStencilTargetInfo outline_ds = {
    .texture          = main_depth,
    .load_op          = SDL_GPU_LOADOP_LOAD,
    .store_op         = SDL_GPU_STOREOP_DONT_CARE,
    .stencil_load_op  = SDL_GPU_LOADOP_CLEAR,
    .stencil_store_op = SDL_GPU_STOREOP_DONT_CARE,
    .clear_stencil    = 0,
};

SDL_GPURenderPass *pass = SDL_BeginGPURenderPass(
    cmd, &outline_color, 1, &outline_ds);

/* Step 1: draw object normally, write stencil marker */
SDL_BindGPUGraphicsPipeline(pass, outline_write_pipeline);
SDL_SetGPUStencilReference(pass, STENCIL_OUTLINE);
/* ... push uniforms, draw selected object ... */

/* Step 2: draw scaled-up object with NOT_EQUAL stencil */
SDL_BindGPUGraphicsPipeline(pass, outline_draw_pipeline);
SDL_SetGPUStencilReference(pass, STENCIL_OUTLINE);

mat4 outline_model = mat4_multiply(
    mat4_translate(object_position),
    mat4_scale_uniform(object_scale * OUTLINE_SCALE));
/* ... push outline uniforms (solid color), draw ... */

SDL_EndGPURenderPass(pass);
```

## Key API calls

- `SDL_CreateGPUTransferBuffer()` with `DOWNLOAD` usage — CPU-readable staging
  buffer for GPU-to-CPU data transfer
- `SDL_DownloadFromGPUTexture()` — copy a texture region into a transfer buffer
  (runs inside a copy pass)
- `SDL_WaitForGPUIdle()` — block until all submitted GPU work completes
- `SDL_MapGPUTransferBuffer()` / `SDL_UnmapGPUTransferBuffer()` — access the
  downloaded pixel data on the CPU
- `SDL_SetGPUStencilReference()` — set per-draw stencil reference value for
  stencil-ID picking and outline rendering

## Common mistakes

- **Using the swapchain format for the ID texture** — The swapchain format
  varies by platform and may be sRGB, which distorts the ID color encoding.
  Always use `R8G8B8A8_UNORM` for the ID texture.
- **Missing depth buffer on the ID pass** — Without its own depth buffer, the
  ID pass renders all objects without occlusion. Background objects overdraw
  foreground objects, producing incorrect pick results.
- **Reading transfer buffer before GPU completion** — The download is
  asynchronous. Reading the transfer buffer before `SDL_WaitForGPUIdle` (or
  fence completion) returns stale or garbage data.
- **Forgetting to clear stencil for the outline pass** — If the outline pass
  reuses stencil values from the scene pass (stencil-ID mode), the outline
  comparison will fail. Clear stencil at the start of the outline render pass.
- **Stencil reference collision** — If the outline marker value (e.g., 200)
  overlaps with stencil-ID object indices (1-N), the outline will not render
  correctly for those objects. Use a high marker value well above your object
  count.
- **Running the ID pass every frame** — The ID pass re-renders the entire scene.
  Running it every frame doubles the draw call count. Only run it on click frames
  unless you specifically need hover detection.

## Cross-references

- [GPU Lesson 37 — 3D Picking](../../../lessons/gpu/37-3d-picking/)
  for the full walkthrough
- [GPU Lesson 34 — Stencil Testing](../../../lessons/gpu/34-stencil-testing/)
  for the stencil outline technique
- [GPU Lesson 36 — Edge Detection](../../../lessons/gpu/36-edge-detection/)
  for alternative stencil patterns
- [GPU Lesson 06 — Depth & 3D](../../../lessons/gpu/06-depth-and-3d/)
  for depth buffer fundamentals
