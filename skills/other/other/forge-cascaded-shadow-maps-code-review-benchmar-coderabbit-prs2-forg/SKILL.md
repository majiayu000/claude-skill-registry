---
name: forge-cascaded-shadow-maps
description: Add cascaded shadow maps with PCF soft shadows to an SDL GPU project
---

Add directional-light cascaded shadow maps (CSM) with 3x3 PCF soft shadows
to an SDL3 GPU application.  Based on Lesson 15.

## When to use

- You need directional light shadows covering a large area
- Single shadow maps lack resolution for your scene
- You want soft shadow edges without expensive techniques

## Key API calls

- `SDL_CreateGPUTexture` — shadow map textures (D32_FLOAT, DEPTH_STENCIL_TARGET | SAMPLER)
- `SDL_CreateGPUSampler` — NEAREST filter, CLAMP_TO_EDGE for shadow map sampling
- `SDL_CreateGPUGraphicsPipeline` — shadow pipeline (depth-only, front-face cull, depth bias)
- `SDL_BeginGPURenderPass` / `SDL_EndGPURenderPass` — one pass per cascade (depth only)
- `SDL_BindGPUFragmentSamplers` — bind shadow maps + sampler for scene pass
- `SDL_PushGPUVertexUniformData` / `SDL_PushGPUFragmentUniformData` — per-draw uniforms

## Correct order

1. **Create shadow map textures + sampler** (in `SDL_AppInit`)
2. **Create shadow pipeline** — depth-only, front-face culling, depth bias
3. **Create scene pipeline** — binds shadow maps as fragment samplers
4. **Each frame:**
   a. Compute cascade split depths (logarithmic-linear blend)
   b. Compute light VP matrix per cascade (frustum corners → light-space AABB)
   c. **Shadow pass**: render all casters into each cascade's depth map
   d. **Scene pass**: render with shadow maps bound, fragment shader selects cascade by view-space depth

## Key concepts

1. **Shadow map textures** need `DEPTH_STENCIL_TARGET | SAMPLER` usage flags
2. **Depth-only render pass**: no color targets, only depth attachment
3. **Cascade splits**: logarithmic-linear blend for practical depth ranges
4. **Light VP matrices**: tight orthographic projection from frustum corners
5. **PCF sampling**: 3x3 grid averages shadow/lit for soft edges
6. **Store op MUST be STORE** (not DONT_CARE) for shadow map depth passes

## Pipeline setup

### Shadow pipeline (depth-only)

```c
/* No color targets — depth only */
pipe.target_info.num_color_targets        = 0;
pipe.target_info.has_depth_stencil_target = true;
pipe.target_info.depth_stencil_format     = SDL_GPU_TEXTUREFORMAT_D32_FLOAT;

/* Front-face culling reduces peter-panning */
pipe.rasterizer_state.cull_mode = SDL_GPU_CULLMODE_FRONT;

/* Depth bias reduces shadow acne */
pipe.rasterizer_state.depth_bias_constant_factor = 2;
pipe.rasterizer_state.depth_bias_slope_factor    = 2.0f;
```

### Shadow map texture

```c
SDL_GPUTextureCreateInfo info;
SDL_zero(info);
info.type   = SDL_GPU_TEXTURETYPE_2D;
info.format = SDL_GPU_TEXTUREFORMAT_D32_FLOAT;
info.usage  = SDL_GPU_TEXTUREUSAGE_DEPTH_STENCIL_TARGET |
              SDL_GPU_TEXTUREUSAGE_SAMPLER;  /* key: both flags */
info.width  = 2048;
info.height = 2048;
info.layer_count_or_depth = 1;
info.num_levels           = 1;
```

### Shadow sampler

```c
SDL_GPUSamplerCreateInfo smp;
SDL_zero(smp);
smp.min_filter     = SDL_GPU_FILTER_NEAREST;
smp.mag_filter     = SDL_GPU_FILTER_NEAREST;
smp.address_mode_u = SDL_GPU_SAMPLERADDRESSMODE_CLAMP_TO_EDGE;
smp.address_mode_v = SDL_GPU_SAMPLERADDRESSMODE_CLAMP_TO_EDGE;
```

## Cascade split algorithm

```c
/* Lengyel's logarithmic-linear blend */
for (int i = 0; i < NUM_CASCADES; i++) {
    float p = (float)(i + 1) / (float)NUM_CASCADES;
    float log_split = near * powf(far / near, p);
    float lin_split = near + (far - near) * p;
    splits[i] = lambda * log_split + (1.0f - lambda) * lin_split;
}
```

## Light VP computation per cascade

1. Unproject 8 NDC corners via inverse camera VP
2. Interpolate near/far to get cascade slice corners
3. Compute cascade center, build light view matrix
4. Transform corners to light space, find tight AABB
5. Build orthographic projection from AABB

```c
mat4 light_view = mat4_look_at(light_pos, center, up);
/* Transform corners to light space → compute AABB */
mat4 light_proj = mat4_orthographic(min_x, max_x, min_y, max_y,
                                     -max_z, -min_z);
mat4 light_vp = mat4_multiply(light_proj, light_view);
```

## Shadow pass render loop

```c
for (int ci = 0; ci < NUM_CASCADES; ci++) {
    SDL_GPUDepthStencilTargetInfo depth;
    SDL_zero(depth);
    depth.texture  = shadow_maps[ci];
    depth.load_op  = SDL_GPU_LOADOP_CLEAR;
    depth.store_op = SDL_GPU_STOREOP_STORE;  /* MUST store */
    depth.clear_depth = 1.0f;

    SDL_GPURenderPass *pass = SDL_BeginGPURenderPass(cmd, NULL, 0, &depth);
    SDL_BindGPUGraphicsPipeline(pass, shadow_pipeline);

    /* Draw all shadow casters with light_vp[ci] * model */
    /* ... */

    SDL_EndGPURenderPass(pass);
}
```

## HLSL shadow sampling (fragment shader)

```hlsl
float sample_shadow_pcf(Texture2D shadow_map, SamplerState smp,
                         float2 shadow_uv, float current_depth) {
    float shadow = 0.0;
    [unroll]
    for (int y = -1; y <= 1; y++) {
        [unroll]
        for (int x = -1; x <= 1; x++) {
            float2 offset = float2(x, y) * texel_size;
            float map_depth = shadow_map.Sample(smp, shadow_uv + offset).r;
            shadow += (map_depth >= current_depth - bias) ? 1.0 : 0.0;
        }
    }
    return shadow / 9.0;
}
```

## Common mistakes

- **Forgetting SAMPLER usage flag** on shadow map texture — it will not be
  readable in fragment shaders without it
- **Using DONT_CARE for shadow pass store_op** — depth data is discarded
  and shadow maps will be empty
- **Not flipping Y** when converting NDC to UV: `shadow_uv.y = 1.0 - shadow_uv.y`
- **Missing depth bias** — causes shadow acne (moire self-shadowing pattern)
- **Culling back faces in shadow pass** — should cull FRONT faces instead
  to reduce peter-panning
- **Not expanding Z range** of the light AABB — shadow casters behind the
  frustum slice won't cast shadows into it

## HLSL register map

```text
Vertex uniform slot 0 → register(b0, space1)
Vertex uniform slot 1 → register(b1, space1)
Fragment sampler slot N → register(tN, space2) + register(sN, space2)
Fragment uniform slot 0 → register(b0, space3)
```

## Reference

See: [Lesson 15 — Cascaded Shadow Maps](../../../lessons/gpu/15-cascaded-shadow-maps/)
