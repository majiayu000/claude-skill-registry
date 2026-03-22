---
name: forge-hdr-tone-mapping
description: >
  Add HDR rendering and tone mapping to an SDL GPU project. Render to a
  floating-point render target, then tone map to the swapchain with Reinhard
  or ACES filmic operators. Includes exposure control and fullscreen blit pass.
---

# HDR Tone Mapping Skill

Adds a two-pass HDR rendering pipeline to any SDL3 GPU scene. Derived from
Lesson 21.

## When to use

- Scene lighting produces values above 1.0 (bright specular highlights,
  multiple lights, emissive surfaces)
- Highlights are clamping to flat white and losing detail
- You want filmic color grading (ACES) instead of raw linear output
- You need a post-processing pass architecture (foundation for bloom, SSAO)

## HDR render target setup

Create a floating-point texture with both render and sample usage:

```c
#define HDR_FORMAT SDL_GPU_TEXTUREFORMAT_R16G16B16A16_FLOAT

SDL_GPUTextureCreateInfo hdr_info;
SDL_zero(hdr_info);
hdr_info.type                 = SDL_GPU_TEXTURETYPE_2D;
hdr_info.format               = HDR_FORMAT;
hdr_info.width                = width;
hdr_info.height               = height;
hdr_info.layer_count_or_depth = 1;
hdr_info.num_levels           = 1;
hdr_info.usage = SDL_GPU_TEXTUREUSAGE_COLOR_TARGET   /* render to it */
               | SDL_GPU_TEXTUREUSAGE_SAMPLER;        /* sample from it */

SDL_GPUTexture *hdr_target = SDL_CreateGPUTexture(device, &hdr_info);
```

`COLOR_TARGET` lets the scene pass render into it. `SAMPLER` lets the tone
map pass read from it. Both flags are required.

## Tone map fragment shader (HLSL)

```hlsl
Texture2D    hdr_texture : register(t0, space0);
SamplerState hdr_sampler : register(s0, space0);

cbuffer TonemapUniforms : register(b0, space3) {
    float exposure;
    uint  tonemap_mode;   /* 0 = clamp, 1 = Reinhard, 2 = ACES */
    float2 _pad;
};

/* Reinhard: simple, maps 0->0, inf->1 */
float3 reinhard(float3 c) { return c / (c + 1.0); }

/* ACES filmic: S-curve with lifted shadows, rich highlights */
float3 aces(float3 c) {
    return saturate((c * (2.51 * c + 0.03)) /
                    (c * (2.43 * c + 0.59) + 0.14));
}

float4 main(float2 uv : TEXCOORD0) : SV_Target {
    float3 hdr = hdr_texture.Sample(hdr_sampler, uv).rgb;
    hdr *= exposure;

    float3 ldr;
    if      (tonemap_mode == 1) ldr = reinhard(hdr);
    else if (tonemap_mode == 2) ldr = aces(hdr);
    else                        ldr = saturate(hdr);

    return float4(ldr, 1.0);
}
```

## Fullscreen blit vertex shader (no vertex buffer)

```hlsl
struct VS_Output {
    float4 clip_pos : SV_Position;
    float2 uv       : TEXCOORD0;
};

VS_Output main(uint vertex_id : SV_VertexID) {
    VS_Output output;
    /* Generate 6 vertices (2 triangles) covering the screen */
    float2 uv;
    uv.x = (vertex_id == 1 || vertex_id == 4 || vertex_id == 5) ? 1.0 : 0.0;
    uv.y = (vertex_id == 2 || vertex_id == 3 || vertex_id == 5) ? 1.0 : 0.0;
    output.clip_pos = float4(uv.x * 2.0 - 1.0, -(uv.y * 2.0 - 1.0), 0.0, 1.0);
    output.uv = uv;
    return output;
}
```

No vertex buffer, no index buffer. Draw with `SDL_DrawGPUPrimitives(pass, 6, 1, 0, 0)`.

## Two-pass rendering pattern (C)

```c
/* ── Pass 1: Scene → HDR buffer ──────────────────────────────── */
SDL_GPUColorTargetInfo scene_ct;
SDL_zero(scene_ct);
scene_ct.texture     = hdr_target;
scene_ct.load_op     = SDL_GPU_LOADOP_CLEAR;
scene_ct.store_op    = SDL_GPU_STOREOP_STORE;
scene_ct.clear_color = (SDL_FColor){ 0.01f, 0.01f, 0.03f, 1.0f };

SDL_GPURenderPass *scene_pass =
    SDL_BeginGPURenderPass(cmd, &scene_ct, 1, &depth_target);
/* ... bind scene pipeline, draw geometry ... */
SDL_EndGPURenderPass(scene_pass);

/* ── Pass 2: Tone map → swapchain ────────────────────────────── */
SDL_GPUColorTargetInfo tone_ct;
SDL_zero(tone_ct);
tone_ct.texture  = swapchain_texture;
tone_ct.load_op  = SDL_GPU_LOADOP_DONT_CARE;
tone_ct.store_op = SDL_GPU_STOREOP_STORE;

SDL_GPURenderPass *tone_pass =
    SDL_BeginGPURenderPass(cmd, &tone_ct, 1, NULL);
SDL_BindGPUGraphicsPipeline(tone_pass, tonemap_pipeline);

/* Bind the HDR buffer as a texture for sampling */
SDL_GPUTextureSamplerBinding hdr_binding = {
    .texture = hdr_target,
    .sampler = hdr_sampler
};
SDL_BindGPUFragmentSamplers(tone_pass, 0, &hdr_binding, 1);

/* Push tone map uniforms */
struct { float exposure; Uint32 mode; float pad[2]; } tu;
tu.exposure = exposure_value;
tu.mode     = tonemap_mode;
SDL_PushGPUFragmentUniformData(cmd, 0, &tu, sizeof(tu));

SDL_DrawGPUPrimitives(tone_pass, 6, 1, 0, 0);
SDL_EndGPURenderPass(tone_pass);
```

## Tone map pipeline setup

The tone map pipeline has no vertex input and no depth test:

```c
SDL_GPUGraphicsPipelineCreateInfo tone_info;
SDL_zero(tone_info);
tone_info.vertex_shader   = tonemap_vert;
tone_info.fragment_shader = tonemap_frag;
tone_info.primitive_type  = SDL_GPU_PRIMITIVETYPE_TRIANGLELIST;

/* No vertex input — positions generated from SV_VertexID */
tone_info.vertex_input_state.num_vertex_attributes = 0;
tone_info.vertex_input_state.num_vertex_buffers    = 0;

/* No depth test — fullscreen quad always draws */
tone_info.depth_stencil_state.enable_depth_test  = false;
tone_info.depth_stencil_state.enable_depth_write = false;

/* Target the sRGB swapchain format (query after SetGPUSwapchainParameters) */
SDL_GPUColorTargetDescription tone_ct_desc;
SDL_zero(tone_ct_desc);
tone_ct_desc.format = swapchain_format;
tone_info.target_info.num_color_targets          = 1;
tone_info.target_info.color_target_descriptions  = &tone_ct_desc;
tone_info.target_info.has_depth_stencil_target   = false;
```

## sRGB swapchain (automatic gamma correction)

```c
SDL_SetGPUSwapchainParameters(device, window,
    SDL_GPU_SWAPCHAINCOMPOSITION_SDR_LINEAR,
    SDL_GPU_PRESENTMODE_VSYNC);
```

`SDR_LINEAR` gives a `B8G8R8A8_UNORM_SRGB` format. The GPU automatically
converts linear values to sRGB on write. No manual `pow(color, 1.0/2.2)`
needed in the shader.

## Typical parameter values

| Parameter | Value | Notes |
|-----------|-------|-------|
| exposure | 1.0 | Default; increase to brighten, decrease to darken |
| light_intensity | 3.0 | Multiplier on diffuse+specular to create HDR values |
| tonemap_mode | 2 (ACES) | Best for most scenes; Reinhard for softer look |

## Key rules

1. **Scene pipeline targets HDR format.** The scene graphics pipeline's color
   target must use `R16G16B16A16_FLOAT`, not the swapchain format. The tone
   map pipeline targets the swapchain format.

2. **Don't clamp lighting in the scene shader.** The whole point of HDR is to
   preserve values above 1.0. Remove any `saturate()` or `min()` on the final
   lighting result in the scene fragment shader.

3. **Push uniforms use the command buffer.** `SDL_PushGPUVertexUniformData`
   and `SDL_PushGPUFragmentUniformData` take `SDL_GPUCommandBuffer*`, not
   `SDL_GPURenderPass*`. Bind/draw calls use the render pass.

4. **Recreate HDR target on resize.** When the window resizes, release and
   recreate the HDR texture to match the new dimensions.

5. **Exposure before tone mapping.** Multiply HDR values by exposure before
   applying the tone mapping operator, not after.

## Common mistakes

- **Using swapchain format for scene pipeline** — values above 1.0 get
  clamped, defeating the purpose of HDR.
- **Forgetting SAMPLER usage on HDR texture** — the tone map pass can't
  sample from a texture that only has COLOR_TARGET usage.
- **Manual gamma in the shader** — with an sRGB swapchain, adding
  `pow(color, 1/2.2)` applies gamma twice, making the image washed out.
- **Passing render pass to push uniform functions** — causes a type mismatch
  compile error. Push uniforms use the command buffer.
- **Not matching HDR target size to window** — after resize, the tone map
  pass samples a stale smaller texture, leaving black borders.

## Reference

- [Lesson 21 — HDR Tone Mapping](../../../lessons/gpu/21-hdr-tone-mapping/)
- [Scene shader](../../../lessons/gpu/21-hdr-tone-mapping/shaders/scene.frag.hlsl)
- [Tone map shader](../../../lessons/gpu/21-hdr-tone-mapping/shaders/tonemap.frag.hlsl)
- [Math Lesson 11 — Color Spaces](../../../lessons/math/11-color-spaces/)
