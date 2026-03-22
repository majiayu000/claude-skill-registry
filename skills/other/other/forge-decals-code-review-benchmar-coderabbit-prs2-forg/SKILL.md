---
name: forge-decals
description: >
  Add deferred decal projection to an SDL GPU project. Render projected decals
  onto scene geometry using depth reconstruction, inverse view-projection
  transforms, local-space bounds checking, soft-edge fading, G-buffer
  normals, Blinn-Phong lighting, and shadow map sampling.
triggers:
  - decal
  - decal projection
  - deferred decal
  - projected texture
  - bullet hole
  - surface marking
  - depth reconstruction
---

# Deferred Decal Projection

Add projected decals to an SDL GPU project. This skill covers three-pass
rendering (shadow, scene, decals), depth texture sampling, inverse
view-projection reconstruction, local-space projection with bounds rejection,
procedural decal textures, soft-edge fading, G-buffer surface normals,
Blinn-Phong lighting, and shadow map sampling on decals.

## When to use

- You need to project textures onto arbitrary scene geometry (bullet holes,
  paint splashes, tire marks, blast marks)
- You want surface markings that conform to complex geometry without modifying
  the underlying mesh
- You need runtime-placed decals that do not require UV mapping on the target
  surface
- You want layered surface detail without baking it into scene textures

## Three-pass rendering architecture

Deferred decals require the scene depth to be available as a sampleable texture
during the decal pass. This means the rendering is split into three passes:

1. **Shadow pass** -- Render shadow casters into a depth-only shadow map
2. **Scene pass** -- Render the full scene (lit geometry, grid, sky) into both
   a color target and a depth-stencil target
3. **Decal pass** -- For each decal, draw its bounding box using the scene
   depth texture to reconstruct world positions and project the decal

The scene pass depth texture is reused as a sampler input in the decal pass.
This is the key constraint that drives the pipeline configuration.

## Depth texture with dual usage

The scene depth texture **must** be created with both `DEPTH_STENCIL_TARGET`
and `SAMPLER` usage flags so it can serve as a render target in the scene pass
and a sampled texture in the decal pass:

```c
SDL_GPUTextureCreateInfo depth_ci = {
    .type   = SDL_GPU_TEXTURETYPE_2D,
    .format = depth_stencil_fmt,  /* D24_UNORM_S8_UINT or D32_FLOAT_S8_UINT */
    .width  = window_w,
    .height = window_h,
    .layer_count_or_depth = 1,
    .num_levels = 1,
    .usage = SDL_GPU_TEXTUREUSAGE_DEPTH_STENCIL_TARGET
           | SDL_GPU_TEXTUREUSAGE_SAMPLER,
};
SDL_GPUTexture *scene_depth = SDL_CreateGPUTexture(device, &depth_ci);
```

Without `SDL_GPU_TEXTUREUSAGE_SAMPLER`, binding this texture as a fragment
sampler in the decal pass will fail or produce undefined results.

## Pipeline configurations

| Pipeline | Cull mode | Depth test | Depth write | Blend | Purpose |
|----------|-----------|------------|-------------|-------|---------|
| Shadow | `BACK` | Yes (`LESS`) | Yes | None | Depth-only shadow map |
| Scene | `BACK` | Yes (`LESS`) | Yes | None | Color + depth for lit geometry |
| Grid | `NONE` | Yes (`LESS_OR_EQUAL`) | Yes | None | Ground grid contributing to scene depth |
| Decal | `FRONT` | No | No | Alpha blend | Projected decal volumes |

## Decal pipeline configuration

The decal pipeline has several non-obvious settings:

```c
SDL_GPUGraphicsPipelineCreateInfo decal_pi = { /* ... */ };

/* Cull FRONT faces -- the camera is often inside the decal box,
   so we render back faces to guarantee visible fragments */
decal_pi.rasterizer_state.cull_mode = SDL_GPU_CULLMODE_FRONT;

/* No depth test or write -- decals float on top of scene geometry,
   depth rejection is handled manually in the fragment shader */
decal_pi.depth_stencil_state.enable_depth_test  = false;
decal_pi.depth_stencil_state.enable_depth_write = false;

/* Alpha blending for soft edges and transparency */
decal_pi.target_info.color_target_descriptions[0].blend_state = (SDL_GPUColorTargetBlendState){
    .enable_blend = true,
    .src_color_blendfactor = SDL_GPU_BLENDFACTOR_SRC_ALPHA,
    .dst_color_blendfactor = SDL_GPU_BLENDFACTOR_ONE_MINUS_SRC_ALPHA,
    .color_blend_op        = SDL_GPU_BLENDOP_ADD,
    .src_alpha_blendfactor = SDL_GPU_BLENDFACTOR_ONE,
    .dst_alpha_blendfactor = SDL_GPU_BLENDFACTOR_ZERO,
    .alpha_blend_op         = SDL_GPU_BLENDOP_ADD,
    .color_write_mask       = 0xF,
};
```

**Why `CULL_FRONT`:** When the camera enters the decal volume (which happens
frequently for close-up decals), front-face culling ensures the back faces of
the box are still rasterized. With back-face culling, the decal would vanish
when the camera gets close.

## Decal fragment shader: depth reconstruction

The core technique reconstructs world-space position from the depth buffer,
then transforms it into the decal's local space to determine UV coordinates
and bounds rejection.

```hlsl
/* Fragment shader pseudocode */

/* 1. Sample scene depth at this fragment's screen position */
float2 screen_uv = frag_pos.xy / viewport_size;
float depth = depth_texture.Sample(depth_sampler, screen_uv);

/* 2. Reconstruct clip-space position */
float4 clip_pos = float4(
    screen_uv.x *  2.0 - 1.0,
    screen_uv.y * -2.0 + 1.0,  /* flip Y for Vulkan/SDL conventions */
    depth,
    1.0
);

/* 3. Transform to world space via inverse view-projection */
float4 world_pos = mul(inv_view_proj, clip_pos);
world_pos /= world_pos.w;  /* perspective divide */

/* 4. Transform to decal local space via inverse decal model matrix */
float4 local_pos = mul(inv_decal_model, world_pos);

/* 5. Bounds check: reject if outside the unit cube [-0.5, 0.5] */
if (abs(local_pos.x) > 0.5 ||
    abs(local_pos.y) > 0.5 ||
    abs(local_pos.z) > 0.5) {
    discard;
}

/* 6. Compute UV from local XZ (top-down projection) */
float2 decal_uv = local_pos.xz + 0.5;
```

## Inverse view-projection matrix

The inverse VP matrix must be passed as a uniform to the decal fragment shader.
Compute it on the CPU each frame:

```c
mat4 vp     = mat4_multiply(proj, view);
mat4 inv_vp = mat4_inverse(vp);
```

Pass `inv_vp` alongside the inverse decal model matrix in the decal's fragment
uniform buffer.

## Procedural decal textures

For simple decal shapes (circles, rings, crosshairs, blast marks), generate
textures procedurally on the CPU and upload once:

```c
/* Example: circular decal with soft edge */
for (int y = 0; y < size; y++) {
    for (int x = 0; x < size; x++) {
        float u = (x + 0.5f) / size * 2.0f - 1.0f;
        float v = (y + 0.5f) / size * 2.0f - 1.0f;
        float dist = sqrtf(u * u + v * v);

        uint8_t r = 255, g = 50, b = 20;
        /* Soft circular falloff */
        float alpha = 1.0f - smoothstep(0.7f, 1.0f, dist);
        pixels[(y * size + x) * 4 + 0] = r;
        pixels[(y * size + x) * 4 + 1] = g;
        pixels[(y * size + x) * 4 + 2] = b;
        pixels[(y * size + x) * 4 + 3] = (uint8_t)(alpha * 255);
    }
}
```

## Soft edge fade with smoothstep

Decals look best when their edges fade out rather than ending abruptly at the
bounds of the projection volume. Apply smoothstep to the distance from the
center in the fragment shader:

```hlsl
/* Soft fade at decal boundaries */
float fade_x = 1.0 - smoothstep(0.4, 0.5, abs(local_pos.x));
float fade_z = 1.0 - smoothstep(0.4, 0.5, abs(local_pos.z));
float fade_y = 1.0 - smoothstep(0.4, 0.5, abs(local_pos.y));
float edge_fade = fade_x * fade_z * fade_y;

float4 decal_color = decal_texture.Sample(decal_sampler, decal_uv);
decal_color.a *= edge_fade;
```

The smoothstep range `(0.4, 0.5)` controls the fade width. A narrower range
(e.g., `0.45, 0.5`) produces a sharper edge; a wider range (e.g., `0.3, 0.5`)
produces a softer gradient.

## Normal G-buffer for decal lighting

Decals need surface normals for lighting. The scene and grid fragment shaders
write world-space normals to a second color target (`SV_Target1`), encoded
into an RGBA8 texture as `n * 0.5 + 0.5`. The decal shader samples this
texture and decodes:

```hlsl
float3 N = normalize(normal_tex.Sample(normal_smp, screen_uv).xyz * 2.0 - 1.0);
```

This gives the same smooth per-vertex interpolated normals as the scene's own
lighting. With the normal available, apply the same Blinn-Phong model as the
scene shader:

```hlsl
float3 lit = decal_color.rgb * ambient;
float3 L = normalize(-light_dir);
float NdotL = max(dot(N, L), 0.0);
float3 H = normalize(L + normalize(eye_pos - world_pos));
float spec = specular_str * pow(max(dot(N, H), 0.0), shininess);
float shadow = sample_shadow(world_pos);  /* project into light VP, PCF sample */
lit += (decal_color.rgb * NdotL + spec) * light_intensity * light_color * shadow;
```

The decal fragment shader needs these additional uniforms and samplers:

- **Uniform**: `light_vp` (mat4), `eye_pos`, `light_dir`, `light_color`,
  `light_intensity`, `ambient`, `shininess`, `specular_str`
- **Sampler slot 2**: shadow depth texture + nearest-clamp sampler
- **Sampler slot 3**: scene normal texture + nearest-clamp sampler

The scene and grid pipelines must have 2 color targets (swapchain + normal
G-buffer). Create the normal texture with `COLOR_TARGET | SAMPLER` usage.

Update the shader creation to declare 4 fragment samplers:

```c
SDL_GPUShader *decal_frag = create_shader(device,
    SDL_GPU_SHADERSTAGE_FRAGMENT,
    decal_frag_spirv, sizeof(decal_frag_spirv),
    decal_frag_dxil, sizeof(decal_frag_dxil),
    4, 0, 1);  /* 4 samplers: scene depth, decal texture, shadow map, normals */
```

## Decal volume geometry

Each decal is rendered as a unit cube `[-0.5, 0.5]^3` transformed by the
decal's model matrix (position, rotation, scale). The cube does not need UVs
or normals -- the fragment shader derives everything from depth reconstruction.

```c
/* Decal model matrix: position + orientation + scale */
mat4 decal_model = mat4_multiply(
    mat4_translate(decal_position),
    mat4_multiply(
        mat4_rotate_y(decal_angle),
        mat4_scale(decal_width, decal_height, decal_depth)
    )
);
mat4 inv_decal_model = mat4_inverse(decal_model);
```

## Render pass structure

The decal pass reuses the scene color target but does **not** attach a
depth-stencil target (depth test is disabled). The scene depth is bound as a
fragment sampler instead:

```c
/* Scene pass: render to color + normal G-buffer + depth */
SDL_GPUColorTargetInfo color_targets[2] = {
    { .texture = scene_color, /* ... */ },
    { .texture = scene_normal, .load_op = SDL_GPU_LOADOP_CLEAR,
      .store_op = SDL_GPU_STOREOP_STORE, /* ... */ },
};
SDL_GPUDepthStencilTargetInfo ds_target = { .texture = scene_depth, /* ... */ };
SDL_GPURenderPass *scene_pass = SDL_BeginGPURenderPass(
    cmd, color_targets, 2, &ds_target);
/* ... draw scene ... */
SDL_EndGPURenderPass(scene_pass);

/* Decal pass: render to color only, sample depth */
SDL_GPUColorTargetInfo decal_color_target = {
    .texture  = scene_color,
    .load_op  = SDL_GPU_LOADOP_LOAD,   /* preserve scene color */
    .store_op = SDL_GPU_STOREOP_STORE,
};
SDL_GPURenderPass *decal_pass = SDL_BeginGPURenderPass(
    cmd, &decal_color_target, 1, NULL);  /* no depth-stencil target */

/* Bind scene depth as a fragment sampler */
SDL_GPUTextureSamplerBinding depth_binding = {
    .texture = scene_depth,
    .sampler = depth_sampler,
};
SDL_BindGPUFragmentSamplers(decal_pass, 0, &depth_binding, 1);

/* Draw each decal box */
for (int i = 0; i < num_decals; i++) {
    /* Push decal uniforms (inv_vp, inv_model, color, viewport) */
    /* Bind decal texture sampler */
    /* Draw cube (36 indices) */
}
SDL_EndGPURenderPass(decal_pass);
```

## Key API calls

- `SDL_CreateGPUTexture()` with `DEPTH_STENCIL_TARGET | SAMPLER` -- dual-use
  depth texture for scene rendering and decal sampling
- `SDL_BindGPUFragmentSamplers()` -- bind scene depth as input to decal shader
- `SDL_GPU_CULLMODE_FRONT` -- ensures decal box is visible when camera is inside
- `SDL_BeginGPURenderPass()` with `NULL` depth target -- decal pass has no
  depth attachment

## Common mistakes

- **Depth texture missing `SAMPLER` usage** -- Creating the depth texture
  without `SDL_GPU_TEXTUREUSAGE_SAMPLER` prevents it from being bound as a
  fragment sampler in the decal pass. The texture must have both
  `DEPTH_STENCIL_TARGET` and `SAMPLER` flags.
- **Using back-face culling on decals** -- With `CULL_BACK`, the decal
  disappears when the camera enters the volume. Use `CULL_FRONT` so the back
  faces are always rendered.
- **Enabling depth test on the decal pipeline** -- Depth testing rejects decal
  fragments that are behind the scene geometry. Since the decal box is an
  arbitrary volume, its fragments have no meaningful depth relationship to the
  scene. Depth rejection is handled manually via the reconstructed position and
  bounds check.
- **Forgetting the perspective divide** -- After multiplying by `inv_view_proj`,
  the result is in homogeneous coordinates. Dividing by `w` is required to get
  correct world-space positions.
- **Wrong Y-axis flip** -- SDL GPU / Vulkan uses top-left origin with Y pointing
  down. The clip-space Y must be flipped (`y * -2.0 + 1.0`) when reconstructing
  from screen UV.
- **Decal pass writing depth** -- If the decal pipeline writes depth, it
  corrupts the depth buffer for subsequent passes or post-processing. Always
  disable depth writes.

## Cross-references

- [GPU Lesson 06 -- Depth & 3D](../../../lessons/gpu/06-depth-and-3d/)
  for depth buffer fundamentals
- [GPU Lesson 15 -- Shadow Maps](../../../lessons/gpu/15-cascaded-shadow-maps/)
  for depth-only render passes and shadow mapping
- [GPU Lesson 34 — Stencil Testing](../../../lessons/gpu/34-stencil-testing/)
  for stencil-based per-pixel masking techniques
- [Math Library](../../../common/math/)
  for `mat4_inverse`, `mat4_multiply`, and other transform utilities
