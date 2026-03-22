---
name: forge-compute-shaders
description: Set up a compute pipeline with storage textures, dispatch groups, and a compute-then-render pattern. Use when someone needs GPU compute, image processing, procedural generation, particle simulation, or post-processing in SDL3 GPU.
---

# Compute Shaders — GPU Compute with SDL3

This skill teaches how to create and dispatch compute shaders using SDL3 GPU.
It covers the compute pipeline, storage textures, dispatch groups, and the
compute-then-render pattern where a compute pass writes to a texture and a
render pass displays it.

## When to use

- Running general-purpose computation on the GPU (not tied to rendering)
- Image processing or post-processing (blur, tone mapping, histograms)
- Procedural texture or noise generation
- Particle simulation or physics computation
- Any scenario where you need random-access write to a texture or buffer

## Key API calls (ordered)

1. `SDL_CreateGPUTexture` — with `COMPUTE_STORAGE_WRITE | SAMPLER` usage
2. `SDL_CreateGPUComputePipeline` — embeds shader code directly (no separate shader object)
3. `SDL_PushGPUComputeUniformData` — push per-frame data (time, resolution)
4. `SDL_BeginGPUComputePass` — binds RW storage textures and buffers
5. `SDL_BindGPUComputePipeline` — bind the pipeline
6. `SDL_DispatchGPUCompute` — launch workgroups
7. `SDL_EndGPUComputePass`
8. `SDL_BeginGPURenderPass` — render pass samples the same texture
9. `SDL_BindGPUFragmentSamplers` — bind compute output as sampled texture

## Compute pipeline creation

The compute pipeline embeds the shader code directly — no separate
`SDL_CreateGPUShader` step. The `threadcount` values must match
`[numthreads()]` in the HLSL.

```c
SDL_GPUComputePipelineCreateInfo info;
SDL_zero(info);
info.entrypoint                     = "main";
info.code                           = shader_code;
info.code_size                      = shader_size;
info.format                         = shader_format;
info.num_readwrite_storage_textures = 1;   /* RWTexture2D outputs */
info.num_uniform_buffers            = 1;   /* cbuffer with time etc. */
info.threadcount_x                  = 8;   /* must match HLSL */
info.threadcount_y                  = 8;
info.threadcount_z                  = 1;

SDL_GPUComputePipeline *pipeline =
    SDL_CreateGPUComputePipeline(device, &info);
```

## Register layout (DXIL — compute shaders)

Compute shaders use different register spaces than vertex/fragment shaders:

| Resource | Register | Space |
|----------|----------|-------|
| Sampled textures, read-only storage textures/buffers | `t[n]` | `space0` |
| Read-write storage textures, read-write storage buffers | `u[n]` | `space1` |
| Uniform buffers | `b[n]` | `space2` |

For SPIR-V, use descriptor sets 0, 1, 2 in the same order.

## Storage texture creation

The texture must have both `COMPUTE_STORAGE_WRITE` (for the compute shader)
and `SAMPLER` (for the render pass) usage flags:

```c
SDL_GPUTextureCreateInfo tex_info;
SDL_zero(tex_info);
tex_info.type                 = SDL_GPU_TEXTURETYPE_2D;
tex_info.format               = SDL_GPU_TEXTUREFORMAT_R8G8B8A8_UNORM;
tex_info.usage                = SDL_GPU_TEXTUREUSAGE_COMPUTE_STORAGE_WRITE |
                                SDL_GPU_TEXTUREUSAGE_SAMPLER;
tex_info.width                = width;
tex_info.height               = height;
tex_info.layer_count_or_depth = 1;
tex_info.num_levels           = 1;
```

Use `R8G8B8A8_UNORM` (not `_SRGB`) when compute writes raw linear values.
Let the sRGB swapchain handle gamma conversion.

## Compute-then-render pattern

Each frame: compute pass writes to texture, render pass samples it.
SDL3 synchronizes automatically between passes on the same command buffer.

```c
/* Push compute uniforms BEFORE the pass */
SDL_PushGPUComputeUniformData(cmd, 0, &uniforms, sizeof(uniforms));

/* ── Compute pass ────────────────────────────── */
SDL_GPUStorageTextureReadWriteBinding storage_binding;
SDL_zero(storage_binding);
storage_binding.texture = texture;
storage_binding.cycle   = true;    /* frame pipelining */

SDL_GPUComputePass *compute_pass = SDL_BeginGPUComputePass(
    cmd,
    &storage_binding, 1,   /* RW storage textures */
    NULL, 0                /* RW storage buffers  */
);

SDL_BindGPUComputePipeline(compute_pass, compute_pipeline);

/* Ceiling division for dispatch groups */
Uint32 groups_x = (width  + 7) / 8;
Uint32 groups_y = (height + 7) / 8;
SDL_DispatchGPUCompute(compute_pass, groups_x, groups_y, 1);

SDL_EndGPUComputePass(compute_pass);

/* ── Render pass ─────────────────────────────── */
/* Same texture, now bound as a sampled texture */
SDL_GPUTextureSamplerBinding tex_binding;
tex_binding.texture = texture;   /* same texture! */
tex_binding.sampler = sampler;

SDL_BindGPUFragmentSamplers(render_pass, 0, &tex_binding, 1);
SDL_DrawGPUPrimitives(render_pass, 3, 1, 0, 0);  /* fullscreen tri */
```

## Dispatch group calculation

Dispatch groups must cover every pixel. Use ceiling division:

```c
Uint32 groups_x = (tex_width  + WORKGROUP_SIZE - 1) / WORKGROUP_SIZE;
Uint32 groups_y = (tex_height + WORKGROUP_SIZE - 1) / WORKGROUP_SIZE;
```

The HLSL shader must bounds-check `SV_DispatchThreadID` to handle overshoot:

```hlsl
[numthreads(8, 8, 1)]
void main(uint3 id : SV_DispatchThreadID)
{
    if (id.x >= (uint)width || id.y >= (uint)height)
        return;
    // ... write pixel
}
```

## Fullscreen triangle (no vertex buffer)

Draw 3 vertices from `SV_VertexID` — no vertex buffer needed. The triangle
overshoots the screen and is clipped to fill it exactly:

```hlsl
struct VSOutput {
    float4 position : SV_Position;
    float2 uv       : TEXCOORD0;
};

VSOutput main(uint id : SV_VertexID)
{
    VSOutput output;
    float2 pos;
    pos.x = (float)((id & 1u) << 1) - 1.0;
    pos.y = (float)((id & 2u))       - 1.0;
    output.position = float4(pos.x * 2.0 + 1.0,
                              pos.y * 2.0 + 1.0,
                              0.0, 1.0);
    output.uv = float2((output.position.x + 1.0) * 0.5,
                         1.0 - (output.position.y + 1.0) * 0.5);
    return output;
}
```

Graphics pipeline needs zero vertex attributes:

```c
gfx_info.vertex_input_state.num_vertex_buffers    = 0;
gfx_info.vertex_input_state.num_vertex_attributes = 0;
```

## Common mistakes

| Mistake | Fix |
|---------|-----|
| `threadcount` in create info doesn't match HLSL `[numthreads()]` | Must be identical — 8,8,1 in both |
| Forgot bounds check in compute shader | Dispatch may overshoot texture size |
| Using `_SRGB` texture format with compute | Use `_UNORM`; let the sRGB swapchain convert |
| Forgot `COMPUTE_STORAGE_WRITE` usage flag | Texture won't bind as RW in compute pass |
| Using vertex shader register spaces for compute | Compute uses `space0/1/2`, not the graphics layout |
| Not pushing uniforms before `BeginGPUComputePass` | Uniforms must be pushed before the pass |

## Related lessons

- [Lesson 11 — Compute Shaders](../../../lessons/gpu/11-compute-shaders/) — full tutorial
- [Lesson 03 — Uniforms & Motion](../../../lessons/gpu/03-uniforms-and-motion/) — push uniforms
- [Lesson 04 — Textures & Samplers](../../../lessons/gpu/04-textures-and-samplers/) — texture binding
