---
name: forge-uniforms-and-motion
description: Pass per-frame data to shaders with push uniforms. Use when animating geometry, passing time/matrices/colors to shaders, or setting up uniform buffers in SDL3 GPU.
---

# Uniforms & Motion — Push Uniforms for Per-Frame Data

This skill teaches how to pass data from the CPU to GPU shaders every frame
using SDL3's push uniform API. It builds on the `first-triangle` skill
(vertex buffers, shaders, pipeline).

## When to use

- Passing per-frame data to shaders (time, matrices, colors, parameters)
- Animating geometry on the GPU
- Setting up uniform buffers in a graphics pipeline
- Any draw call that needs data beyond vertex attributes

## Push uniforms vs. GPU uniform buffers

| Method | When to use |
|--------|-------------|
| **Push uniforms** (`SDL_PushGPUVertexUniformData`) | Small data that changes frequently — time, MVP matrices, colors |
| **GPU uniform buffer** (create + upload) | Large or rarely-changing data |

Push uniforms are the simple path: push a pointer to a C struct, SDL copies
it internally. No buffer creation, no transfer buffers, no copy passes.

## Uniform data struct

Define a C struct matching your shader's cbuffer layout:

```c
typedef struct Uniforms {
    float time;     /* elapsed time in seconds                     */
    float aspect;   /* window width / height — for correcting NDC  */
} Uniforms;
```

**std140 layout rules:** vec3 and vec4 fields must be 16-byte aligned. A
single float or a float4 is naturally aligned. If you mix types, add padding.

## HLSL shader convention

SDL GPU maps uniform buffer slots to specific HLSL registers:

| Stage    | Slot 0 register       | Slot 1 register       |
|----------|-----------------------|-----------------------|
| Vertex   | `register(b0, space1)` | `register(b1, space1)` |
| Fragment | `register(b0, space3)` | `register(b1, space3)` |

```hlsl
/* Vertex shader — uniform slot 0 */
cbuffer Uniforms : register(b0, space1)
{
    float time;
    float aspect;
};

VSOutput main(VSInput input)
{
    /* Correct for non-square windows BEFORE rotation so the triangle
     * keeps its shape at every angle.  If done after, the squish
     * would distort the already-rotated coordinates. */
    float2 corrected = float2(input.position.x / aspect, input.position.y);

    float c = cos(time);
    float s = sin(time);

    float2 rotated;
    rotated.x = corrected.x * c - corrected.y * s;
    rotated.y = corrected.x * s + corrected.y * c;

    VSOutput output;
    output.position = float4(rotated, 0.0, 1.0);
    output.color    = float4(input.color, 1.0);
    return output;
}
```

## Shader creation — declaring uniform count

When creating a shader, `num_uniform_buffers` must match the number of
cbuffers your shader code declares:

```c
SDL_GPUShaderCreateInfo info = { 0 };
info.stage               = SDL_GPU_SHADERSTAGE_VERTEX;
info.entrypoint          = "main";
info.num_uniform_buffers = 1;   /* ← must match shader's cbuffer count */
info.num_samplers        = 0;
info.num_storage_textures = 0;
info.num_storage_buffers = 0;
/* ... code, code_size, format ... */

SDL_GPUShader *shader = SDL_CreateGPUShader(device, &info);
```

## Pushing uniform data — each frame

```c
/* 1. Compute your per-frame data */
float elapsed = (float)(SDL_GetTicks() - start_ticks) / 1000.0f;

int w = 0, h = 0;
SDL_GetWindowSizeInPixels(window, &w, &h);

Uniforms uniforms;
uniforms.time   = elapsed;
uniforms.aspect = (h > 0) ? (float)w / (float)h : 1.0f;

/* 2. Acquire command buffer */
SDL_GPUCommandBuffer *cmd = SDL_AcquireGPUCommandBuffer(device);

/* 3. Push BEFORE the render pass */
SDL_PushGPUVertexUniformData(cmd, 0, &uniforms, sizeof(uniforms));

/* 4. Begin render pass and draw as usual */
SDL_GPURenderPass *pass = SDL_BeginGPURenderPass(cmd, &color_target, 1, NULL);
SDL_BindGPUGraphicsPipeline(pass, pipeline);
SDL_BindGPUVertexBuffers(pass, 0, &binding, 1);
SDL_DrawGPUPrimitives(pass, vertex_count, 1, 0, 0);
SDL_EndGPURenderPass(pass);

SDL_SubmitGPUCommandBuffer(cmd);
```

**Key details:**

- Push happens on the **command buffer**, not the render pass
- Push **before** `SDL_BeginGPURenderPass` — SDL latches the data at pass start
- Data is copied internally — your struct can live on the stack
- Slot 0 in the push call matches `b0` in the HLSL register
- Each stage (vertex/fragment) has 4 independent slots (0–3)
- Data persists in a slot until you push new data to it

## Fragment shader uniforms

Same pattern, different function and register space:

```c
SDL_PushGPUFragmentUniformData(cmd, 0, &frag_uniforms, sizeof(frag_uniforms));
```

```hlsl
cbuffer FragUniforms : register(b0, space3)    /* space3 for fragment */
{
    float brightness;
};
```

## Tracking time

```c
/* In app_state */
Uint64 start_ticks;

/* In SDL_AppInit */
state->start_ticks = SDL_GetTicks();

/* In SDL_AppIterate */
float elapsed = (float)(SDL_GetTicks() - state->start_ticks) / 1000.0f;
```

`SDL_GetTicks()` returns milliseconds since `SDL_Init`. Dividing by 1000
gives seconds as a float — ideal for shader math like `sin(time)` and
`cos(time)`.

## Common mistakes

| Mistake | Fix |
|---------|-----|
| `num_uniform_buffers = 0` but shader has a cbuffer | Must match — set to 1 (or however many cbuffers your shader declares) |
| Pushing uniform data *after* `SDL_BeginGPURenderPass` | Push *before* the render pass — SDL latches uniforms at pass start |
| Wrong register space in HLSL | Vertex = `space1`, Fragment = `space3` |
| Forgetting std140 alignment for vec3/vec4 | Pad structs so vec3/vec4 start at 16-byte boundaries |
| Using `SDL_PushGPUVertexUniformData` for fragment data | Use `SDL_PushGPUFragmentUniformData` for fragment stage |
| Not declaring `num_uniform_buffers` on the fragment shader | Each stage declares its own count independently |
| Rotation looks skewed on non-square windows | Pass aspect ratio as uniform, divide x by it **before** rotation |
| Aspect correction applied after rotation | Triangle skews at certain angles — correct *before* rotating so you rotate in uniform space |
| Triangle wobbles instead of spinning in place | Center vertices so centroid is at origin (average of all positions = 0,0) |

## Cleanup

No extra cleanup needed for push uniforms — there are no GPU buffer objects
to release. The only cleanup is the same as Lesson 02 (pipeline, vertex
buffer, window, device).
