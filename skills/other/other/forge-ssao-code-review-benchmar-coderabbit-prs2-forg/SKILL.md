---
name: forge-ssao
description: Add screen-space ambient occlusion (SSAO) to an SDL3 GPU application
argument-hint: (no arguments needed)
---

# SSAO — Screen-Space Ambient Occlusion

Add hemisphere-kernel SSAO with blur and composite passes to an existing
SDL3 GPU application. Based on the John Chapman / LearnOpenGL approach.

## When to use

- You want contact shadows in crevices, corners, and where objects meet
- You have a depth buffer and can add a view-normal G-buffer pass
- You want a screen-space effect that works with any geometry

## How it works

SSAO requires 3 additional render passes after your main geometry pass:

1. **SSAO pass** — samples the depth buffer in a hemisphere around each
   pixel's surface normal; outputs a single-channel AO factor
2. **Blur pass** — 4x4 box blur smooths the noise tile pattern
3. **Composite pass** — multiplies scene color by the AO factor

The geometry pass must output view-space normals as a second render target
(MRT), and the depth buffer must be readable as a sampler.

## Key API calls

### Render targets needed

```c
/* Scene depth — readable as sampler for SSAO reconstruction */
ti.format = SDL_GPU_TEXTUREFORMAT_D32_FLOAT;
ti.usage  = SDL_GPU_TEXTUREUSAGE_DEPTH_STENCIL_TARGET |
            SDL_GPU_TEXTUREUSAGE_SAMPLER;

/* View normals — MRT target 1 from geometry pass */
ti.format = SDL_GPU_TEXTUREFORMAT_R16G16B16A16_FLOAT;
ti.usage  = SDL_GPU_TEXTUREUSAGE_COLOR_TARGET |
            SDL_GPU_TEXTUREUSAGE_SAMPLER;

/* SSAO raw + blurred — single channel AO factor */
ti.format = SDL_GPU_TEXTUREFORMAT_R8_UNORM;
ti.usage  = SDL_GPU_TEXTUREUSAGE_COLOR_TARGET |
            SDL_GPU_TEXTUREUSAGE_SAMPLER;
```

### Pipeline setup

Set `num_color_targets = 2` on the MRT geometry pipeline (color + normals).
The three fullscreen-quad pipelines (SSAO, blur, composite) use no vertex
buffer and no depth test — see existing pipeline patterns from earlier lessons.

### SSAO kernel generation

```c
/* 64 hemisphere samples with quadratic falloff */
for (int i = 0; i < 64; i++) {
    /* Random direction in hemisphere (+Z up) */
    float x = random_signed(), y = random_signed(), z = random_01();
    normalize(&x, &y, &z);

    /* Concentrate samples near the surface */
    float t = (float)i / 64.0f;
    float scale = 0.1f + 0.9f * t * t;
    kernel[i] = {x * scale, y * scale, z * scale, 0};
}
```

### Depth reconstruction (HLSL)

```hlsl
float3 view_pos_from_depth(float2 uv, float depth) {
    float2 ndc_xy = uv * 2.0 - 1.0;
    ndc_xy.y = -ndc_xy.y;
    float4 clip = float4(ndc_xy, depth, 1.0);
    float4 view = mul(inv_projection, clip);
    return view.xyz / view.w;
}
```

### MRT fragment shader output (HLSL)

```hlsl
struct PSOutput {
    float4 color       : SV_Target0;  /* lit scene color */
    float4 view_normal : SV_Target1;  /* view-space normal */
};
```

## Step-by-step integration

1. **Add view-normal output** to your geometry pass vertex shader (transform
   normal by view matrix) and fragment shader (output as SV_Target1)

2. **Change depth texture usage** to include `SDL_GPU_TEXTUREUSAGE_SAMPLER`
   so the SSAO pass can read it

3. **Create SSAO render targets** — `ssao_raw` and `ssao_blurred` (R8_UNORM)

4. **Create noise texture** — 4x4, R32G32B32A32_FLOAT, random unit XY vectors,
   REPEAT wrapping

5. **Generate SSAO kernel** — 64 hemisphere samples at init time

6. **Add 3 fullscreen-quad pipelines** — SSAO, blur, composite (no vertex
   buffer, no depth test)

7. **Render 3 additional passes** after your geometry pass:
   - SSAO: bind normals + depth + noise, push kernel + matrices
   - Blur: bind raw SSAO, push texel size
   - Composite: bind scene color + blurred AO, push display mode

## Common issues

- **Black screen** — check that depth texture has SAMPLER usage flag
- **All white AO** — verify `inv_projection` is correct; check depth
  reconstruction flips Y correctly
- **Visible 4x4 pattern** — ensure blur pass runs; check noise texture
  uses REPEAT wrapping
- **Self-occlusion (dark flat surfaces)** — increase `bias` parameter
- **AO halo around objects** — decrease `radius` or add range check with
  `smoothstep(0, 1, radius / abs(frag_z - stored_z))`

## Reference

See [Lesson 27 — SSAO](../../../lessons/gpu/27-ssao/) for the complete
implementation with 5 render passes, shadow mapping, and view mode switching.
