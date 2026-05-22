---
name: forge-bloom
description: Add Jimenez dual-filter bloom to an SDL GPU project with HDR rendering. Implements 13-tap downsample with Karis averaging and 9-tap tent-filter upsample with additive blending.
---

Add Jimenez dual-filter bloom (SIGGRAPH 2014) to an SDL GPU project that
already has HDR rendering (floating-point render target + tone mapping).

## Prerequisites

- HDR render target (R16G16B16A16_FLOAT) with COLOR_TARGET + SAMPLER usage
- Tone mapping pass (fullscreen quad, HDR → swapchain)
- Bright HDR values in the scene (emissive objects, specular highlights > 1.0)

## Architecture

### Bloom mip chain

Create 5 half-resolution HDR textures, each with COLOR_TARGET + SAMPLER:

```c
#define BLOOM_MIP_COUNT 5
#define HDR_FORMAT SDL_GPU_TEXTUREFORMAT_R16G16B16A16_FLOAT

/* For 1280x720: 640x360 → 320x180 → 160x90 → 80x45 → 40x22 */
Uint32 w = hdr_width / 2, h = hdr_height / 2;
for (int i = 0; i < BLOOM_MIP_COUNT; i++) {
    bloom_mips[i] = create_texture(device, HDR_FORMAT, w, h,
        SDL_GPU_TEXTUREUSAGE_COLOR_TARGET | SDL_GPU_TEXTUREUSAGE_SAMPLER);
    bloom_widths[i] = w;
    bloom_heights[i] = h;
    w /= 2; h /= 2;
}
```

### Pipelines (3 bloom-specific)

| Pipeline | Vertex | Fragment | Blend | Depth |
|----------|--------|----------|-------|-------|
| downsample | fullscreen.vert (SV_VertexID) | bloom_downsample.frag | None | No |
| upsample | fullscreen.vert (SV_VertexID) | bloom_upsample.frag | **Additive (ONE+ONE)** | No |
| tonemap | fullscreen.vert (SV_VertexID) | tonemap.frag | None | No |

### Upsample blend state (critical)

```c
color_desc.blend_state.enable_blend = true;
color_desc.blend_state.src_color_blendfactor = SDL_GPU_BLENDFACTOR_ONE;
color_desc.blend_state.dst_color_blendfactor = SDL_GPU_BLENDFACTOR_ONE;
color_desc.blend_state.color_blend_op = SDL_GPU_BLENDOP_ADD;
color_desc.blend_state.src_alpha_blendfactor = SDL_GPU_BLENDFACTOR_ONE;
color_desc.blend_state.dst_alpha_blendfactor = SDL_GPU_BLENDFACTOR_ONE;
color_desc.blend_state.alpha_blend_op = SDL_GPU_BLENDOP_ADD;
```

### Bloom sampler

Use LINEAR / CLAMP_TO_EDGE — the bilinear filtering is essential for quality:

```c
sampler_info.min_filter = SDL_GPU_FILTER_LINEAR;
sampler_info.mag_filter = SDL_GPU_FILTER_LINEAR;
sampler_info.address_mode_u = SDL_GPU_SAMPLERADDRESSMODE_CLAMP_TO_EDGE;
sampler_info.address_mode_v = SDL_GPU_SAMPLERADDRESSMODE_CLAMP_TO_EDGE;
```

## Per-frame render passes

```text
1. Scene pass → hdr_target (existing)

2. Bloom downsample (5 passes):
   Pass 0: hdr_target → bloom_mips[0]  (threshold + Karis)
   Pass 1: bloom_mips[0] → bloom_mips[1]  (standard weights)
   Pass 2-4: same pattern

3. Bloom upsample (4 passes, LOAD + additive blend):
   Pass 0: bloom_mips[4] → ADD to bloom_mips[3]
   Pass 1: bloom_mips[3] → ADD to bloom_mips[2]
   Pass 2-3: same pattern

4. Tonemap pass → swapchain
   Sample hdr_target + bloom_mips[0]
   output = tonemap((hdr + bloom * bloom_intensity) * exposure)
```

## Downsample uniforms

```c
typedef struct BloomDownsampleUniforms {
    float texel_size[2];  /* 1/source_width, 1/source_height */
    float threshold;      /* brightness cutoff (first pass only) */
    float use_karis;      /* 1.0 first pass, 0.0 rest */
} BloomDownsampleUniforms;
```

## Upsample uniforms

```c
typedef struct BloomUpsampleUniforms {
    float texel_size[2];  /* 1/source_width, 1/source_height */
    float _pad[2];
} BloomUpsampleUniforms;
```

## Downsample pass loop

```c
for (int i = 0; i < BLOOM_MIP_COUNT; i++) {
    /* Render to bloom_mips[i] with CLEAR */
    /* Source: i==0 ? hdr_target : bloom_mips[i-1] */
    /* Texel size: 1/source dimensions */
    ds_u.use_karis = (i == 0) ? 1.0f : 0.0f;
    ds_u.threshold = bloom_threshold;
}
```

## Upsample pass loop

```c
for (int i = BLOOM_MIP_COUNT - 2; i >= 0; i--) {
    /* Render to bloom_mips[i] with LOAD (preserve existing data) */
    /* Source: bloom_mips[i+1] (smaller mip) */
    /* Additive blend adds upsampled result on top */
}
```

## Key API calls

Each bloom pass is a separate render pass. The key SDL GPU calls per pass:

```c
/* Begin a render pass targeting one bloom mip */
SDL_GPURenderPass *pass = SDL_BeginGPURenderPass(cmd, &color_info, 1, NULL);
SDL_BindGPUGraphicsPipeline(pass, pipeline);          /* downsample or upsample */
SDL_BindGPUFragmentSamplers(pass, 0, &sampler_bind, 1); /* source texture + sampler */
SDL_PushGPUFragmentUniformData(cmd, 0, &uniforms, sizeof(uniforms));
SDL_DrawGPUPrimitives(pass, 3, 1, 0, 0);             /* fullscreen triangle */
SDL_EndGPURenderPass(pass);
```

- **Downsample pass:** `color_info.load_op = SDL_GPU_LOADOP_CLEAR`
- **Upsample pass:** `color_info.load_op = SDL_GPU_LOADOP_LOAD` (preserve
  downsample data; the additive blend state on the pipeline accumulates)
- **Tonemap pass:** Bind both `hdr_target` and `bloom_mips[0]` as fragment
  samplers, combine before tone mapping

## Code template

Minimal copy-ready skeleton for the per-frame bloom passes:

```c
/* ── Downsample: extract bright areas and progressively blur ───────── */
BloomDownsampleUniforms ds_u;
for (int i = 0; i < BLOOM_MIP_COUNT; i++) {
    /* Source is HDR target for first pass, previous mip for the rest */
    SDL_GPUTexture *src = (i == 0) ? hdr_target : bloom_mips[i - 1];
    Uint32 src_w = (i == 0) ? hdr_width : bloom_widths[i - 1];
    Uint32 src_h = (i == 0) ? hdr_height : bloom_heights[i - 1];

    ds_u.texel_size[0] = 1.0f / (float)src_w;
    ds_u.texel_size[1] = 1.0f / (float)src_h;
    ds_u.threshold = bloom_threshold;
    ds_u.use_karis = (i == 0) ? 1.0f : 0.0f;

    /* Render to bloom_mips[i], CLEAR load op */
    SDL_GPUColorTargetInfo color_info;
    SDL_zero(color_info);
    color_info.texture = bloom_mips[i];
    color_info.load_op = SDL_GPU_LOADOP_CLEAR;
    color_info.store_op = SDL_GPU_STOREOP_STORE;

    SDL_GPURenderPass *pass = SDL_BeginGPURenderPass(cmd, &color_info, 1, NULL);
    SDL_BindGPUGraphicsPipeline(pass, downsample_pipeline);
    SDL_GPUTextureSamplerBinding bind = { .texture = src, .sampler = bloom_sampler };
    SDL_BindGPUFragmentSamplers(pass, 0, &bind, 1);
    SDL_PushGPUFragmentUniformData(cmd, 0, &ds_u, sizeof(ds_u));
    SDL_DrawGPUPrimitives(pass, 3, 1, 0, 0);
    SDL_EndGPURenderPass(pass);
}

/* ── Upsample: progressively add back detail with additive blend ───── */
BloomUpsampleUniforms us_u;
for (int i = BLOOM_MIP_COUNT - 2; i >= 0; i--) {
    /* Source is the smaller (i+1) mip */
    us_u.texel_size[0] = 1.0f / (float)bloom_widths[i + 1];
    us_u.texel_size[1] = 1.0f / (float)bloom_heights[i + 1];

    /* Render to bloom_mips[i], LOAD to preserve downsample data */
    SDL_GPUColorTargetInfo color_info;
    SDL_zero(color_info);
    color_info.texture = bloom_mips[i];
    color_info.load_op = SDL_GPU_LOADOP_LOAD;   /* critical: preserve existing data */
    color_info.store_op = SDL_GPU_STOREOP_STORE;

    SDL_GPURenderPass *pass = SDL_BeginGPURenderPass(cmd, &color_info, 1, NULL);
    SDL_BindGPUGraphicsPipeline(pass, upsample_pipeline);  /* has additive blend */
    SDL_GPUTextureSamplerBinding bind = {
        .texture = bloom_mips[i + 1], .sampler = bloom_sampler
    };
    SDL_BindGPUFragmentSamplers(pass, 0, &bind, 1);
    SDL_PushGPUFragmentUniformData(cmd, 0, &us_u, sizeof(us_u));
    SDL_DrawGPUPrimitives(pass, 3, 1, 0, 0);
    SDL_EndGPURenderPass(pass);
}
```

## Common mistakes

1. **CLEAR instead of LOAD on upsample** — The upsample pass MUST use
   `SDL_GPU_LOADOP_LOAD` to preserve the downsample data. CLEAR would
   erase it, losing the multi-scale effect.

2. **Wrong texel size** — The texel size must be `1/source` dimensions,
   not `1/destination`. The shader samples the source texture.

3. **Missing LINEAR sampler** — Using NEAREST for bloom sampling
   produces blocky artifacts. The bilinear filter is part of the
   algorithm's design.

4. **Bloom added after tone mapping** — Bloom must be added to HDR
   values BEFORE tone mapping, so the combined result compresses
   naturally. Adding after tone mapping causes bloom highlights to clip.

5. **Not recreating mip chain on resize** — The bloom mip dimensions
   depend on the window size. Release and recreate on resize.

## Reference

- [GPU Lesson 22 — Bloom](../../../lessons/gpu/22-bloom/)
- Jorge Jimenez, "Next Generation Post Processing in Call of Duty:
  Advanced Warfare," SIGGRAPH 2014
