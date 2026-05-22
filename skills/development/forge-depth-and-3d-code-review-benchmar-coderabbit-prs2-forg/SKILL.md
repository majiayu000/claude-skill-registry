---
name: forge-depth-and-3d
description: Set up depth buffer, 3D MVP pipeline, back-face culling, and window resize handling. Use when someone needs to render 3D geometry with correct depth ordering, perspective projection, or a view camera in SDL3 GPU.
---

# Depth Buffer & 3D Transforms — MVP Pipeline, Depth Testing, and Culling

This skill teaches how to render 3D geometry with the full Model-View-Projection
pipeline, depth testing, back-face culling, and window resize handling. It builds
on the `uniforms-and-motion` skill (push uniforms) and `first-triangle` skill
(vertex buffers, pipelines).

## When to use

- Rendering 3D geometry (cubes, meshes, scenes)
- Setting up perspective projection with a camera
- Enabling depth testing so closer surfaces draw over farther ones
- Adding back-face culling for closed meshes
- Handling window resize for depth textures
- Transitioning from 2D (float2) to 3D (float3) vertex positions

## Key API calls (ordered)

1. `SDL_CreateGPUTexture` — create depth texture with `DEPTH_STENCIL_TARGET` usage
2. `SDL_CreateGPUGraphicsPipeline` — with depth stencil state and back-face culling
3. `mat4_look_at` / `mat4_perspective` / `mat4_multiply` — build MVP matrix per frame
4. `SDL_PushGPUVertexUniformData` — push MVP matrix to vertex shader
5. `SDL_BeginGPURenderPass` — with both color target AND depth target
6. `SDL_DrawGPUIndexedPrimitives` — draw 3D geometry

## Code template

### Depth texture creation

```c
static SDL_GPUTexture *create_depth_texture(SDL_GPUDevice *device,
                                             Uint32 w, Uint32 h)
{
    SDL_GPUTextureCreateInfo info;
    SDL_zero(info);
    info.type                 = SDL_GPU_TEXTURETYPE_2D;
    info.format               = SDL_GPU_TEXTUREFORMAT_D16_UNORM;
    info.usage                = SDL_GPU_TEXTUREUSAGE_DEPTH_STENCIL_TARGET;
    info.width                = w;
    info.height               = h;
    info.layer_count_or_depth = 1;
    info.num_levels           = 1;

    SDL_GPUTexture *texture = SDL_CreateGPUTexture(device, &info);
    if (!texture) {
        SDL_Log("Failed to create depth texture: %s", SDL_GetError());
    }
    return texture;
}
```

### Pipeline setup with depth and culling

```c
SDL_GPUGraphicsPipelineCreateInfo pipeline_info;
SDL_zero(pipeline_info);

/* ... vertex input, shaders, etc. ... */

/* Back-face culling — skip faces pointing away from camera */
pipeline_info.rasterizer_state.cull_mode  = SDL_GPU_CULLMODE_BACK;
pipeline_info.rasterizer_state.front_face = SDL_GPU_FRONTFACE_COUNTER_CLOCKWISE;

/* Depth testing — closer fragments win */
pipeline_info.depth_stencil_state.enable_depth_test  = true;
pipeline_info.depth_stencil_state.enable_depth_write = true;
pipeline_info.depth_stencil_state.compare_op         = SDL_GPU_COMPAREOP_LESS_OR_EQUAL;

/* Color target */
SDL_GPUColorTargetDescription color_desc;
SDL_zero(color_desc);
color_desc.format = SDL_GetGPUSwapchainTextureFormat(device, window);
pipeline_info.target_info.color_target_descriptions = &color_desc;
pipeline_info.target_info.num_color_targets         = 1;

/* Depth target — MUST declare format in pipeline */
pipeline_info.target_info.has_depth_stencil_target = true;
pipeline_info.target_info.depth_stencil_format     = SDL_GPU_TEXTUREFORMAT_D16_UNORM;
```

### MVP matrix computation

```c
#include "math/forge_math.h"

/* Model: position and orient the object */
mat4 model = mat4_multiply(
    mat4_translate(vec3_create(0.0f, 0.0f, 0.0f)),
    mat4_multiply(mat4_rotate_y(angle_y), mat4_rotate_x(angle_x))
);

/* View: position and orient the camera */
mat4 view = mat4_look_at(
    vec3_create(0.0f, 1.5f, 3.0f),  /* eye position    */
    vec3_create(0.0f, 0.0f, 0.0f),  /* look-at target  */
    vec3_create(0.0f, 1.0f, 0.0f)   /* world up        */
);

/* Projection: perspective with correct aspect ratio */
float fov    = 60.0f * FORGE_DEG2RAD;
float aspect = (float)window_w / (float)window_h;
mat4 proj    = mat4_perspective(fov, aspect, 0.1f, 100.0f);

/* Compose: MVP = Projection * View * Model */
mat4 mvp = mat4_multiply(mat4_multiply(proj, view), model);
```

### Render pass with depth target

```c
SDL_GPUColorTargetInfo color_target;
SDL_zero(color_target);
color_target.texture     = swapchain;
color_target.load_op     = SDL_GPU_LOADOP_CLEAR;
color_target.store_op    = SDL_GPU_STOREOP_STORE;
color_target.clear_color = (SDL_FColor){ 0.02f, 0.02f, 0.04f, 1.0f };

SDL_GPUDepthStencilTargetInfo depth_target;
SDL_zero(depth_target);
depth_target.texture          = depth_texture;
depth_target.load_op          = SDL_GPU_LOADOP_CLEAR;
depth_target.store_op         = SDL_GPU_STOREOP_DONT_CARE;
depth_target.stencil_load_op  = SDL_GPU_LOADOP_DONT_CARE;
depth_target.stencil_store_op = SDL_GPU_STOREOP_DONT_CARE;
depth_target.clear_depth      = 1.0f;  /* far plane */

SDL_GPURenderPass *pass = SDL_BeginGPURenderPass(
    cmd, &color_target, 1, &depth_target);
```

### Window resize handling

```c
/* Check each frame — recreate depth texture if window size changed */
int w, h;
SDL_GetWindowSizeInPixels(window, &w, &h);

if ((Uint32)w != depth_width || (Uint32)h != depth_height) {
    SDL_ReleaseGPUTexture(device, depth_texture);
    depth_texture = create_depth_texture(device, (Uint32)w, (Uint32)h);
    depth_width   = (Uint32)w;
    depth_height  = (Uint32)h;
}
```

### Vertex shader (HLSL)

```hlsl
cbuffer Uniforms : register(b0, space1)
{
    column_major float4x4 mvp;
};

struct VSInput
{
    float3 position : TEXCOORD0;
    float3 color    : TEXCOORD1;
};

struct VSOutput
{
    float4 position : SV_Position;
    float4 color    : TEXCOORD0;
};

VSOutput main(VSInput input)
{
    VSOutput output;
    output.position = mul(mvp, float4(input.position, 1.0));
    output.color    = float4(input.color, 1.0);
    return output;
}
```

## Vertex format for 3D

```c
typedef struct Vertex {
    vec3 position;   /* 3D model-space position (FLOAT3) */
    vec3 color;      /* RGB per-vertex color    (FLOAT3) */
} Vertex;

/* Vertex attributes */
attrs[0].format = SDL_GPU_VERTEXELEMENTFORMAT_FLOAT3;  /* position */
attrs[0].offset = offsetof(Vertex, position);
attrs[1].format = SDL_GPU_VERTEXELEMENTFORMAT_FLOAT3;  /* color */
attrs[1].offset = offsetof(Vertex, color);
```

## Uniform struct

```c
typedef struct Uniforms {
    mat4 mvp;   /* 64 bytes — naturally 16-byte aligned */
} Uniforms;
```

A single `mat4` is exactly 64 bytes and naturally 16-byte aligned, so no
padding is needed (unlike the `time + aspect + pad` structs from earlier lessons).

## HLSL column-major compatibility

forge_math.h stores matrices column-major. HLSL defaults to `column_major` for
`float4x4`. Use `mul(mvp, float4(pos, 1.0))` — no transpose needed.

If you accidentally see an inside-out or mirrored cube, check:

1. Matrix storage order matches shader declaration
2. `mul(matrix, vector)` not `mul(vector, matrix)`
3. Winding order matches `front_face` setting

## Depth format choices

| Format | Bits | Precision | Use case |
|--------|------|-----------|----------|
| `D16_UNORM` | 16 | Low | Simple scenes, universally supported |
| `D24_UNORM` | 24 | Medium | Most 3D games |
| `D32_FLOAT` | 32 | High | Large worlds, reverse-Z |

For learning and simple scenes, `D16_UNORM` is sufficient and universally
supported.

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Cube looks inside-out | Enable depth testing (`enable_depth_test = true`) |
| No depth target in pipeline | Set `has_depth_stencil_target = true` and `depth_stencil_format` |
| Crash on window resize | Recreate depth texture when window size changes |
| Cube appears mirrored | Check `mul(mvp, vertex)` order matches column-major storage |
| Back faces visible | Set `cull_mode = CULLMODE_BACK` with correct `front_face` |
| Depth buffer not clearing | Set `load_op = LOADOP_CLEAR` and `clear_depth = 1.0f` |
| Missing perspective | Use `mat4_perspective` not `mat4_orthographic` |

## Cleanup

```c
SDL_ReleaseGPUTexture(device, depth_texture);
SDL_ReleaseGPUBuffer(device, index_buffer);
SDL_ReleaseGPUBuffer(device, vertex_buffer);
SDL_ReleaseGPUGraphicsPipeline(device, pipeline);
```

## Reference

- [GPU Lesson 06 — Depth Buffer & 3D Transforms](../../../lessons/gpu/06-depth-and-3d/) — full implementation
- [Math Lesson 05 — Matrices](../../../lessons/math/05-matrices/) — transform theory
- [uniforms-and-motion skill](../forge-uniforms-and-motion/SKILL.md) — push uniforms
- [first-triangle skill](../forge-first-triangle/SKILL.md) — vertex buffers, pipelines
- `mat4_perspective()`, `mat4_look_at()` in `common/math/forge_math.h`
