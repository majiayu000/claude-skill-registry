---
name: forge-environment-mapping
description: >
  Add cube map environment mapping with a skybox and reflective surfaces.
  Use when someone needs a 360-degree background, reflection mapping, or
  cube map textures in SDL3 GPU.
---

# Environment Mapping — SDL3 GPU Skill

Add a cube map skybox and environment reflections to a 3D scene.

## When to use this skill

- Rendering a 360-degree background (space, sky, indoor environment)
- Adding reflections to metallic or glossy surfaces
- Working with `SDL_GPU_TEXTURETYPE_CUBE` textures
- Combining multiple graphics pipelines in one render pass

## Cube map texture creation

```c
/* Create a cube map texture with 6 faces. */
SDL_GPUTextureCreateInfo tex_info;
SDL_zero(tex_info);
tex_info.type                 = SDL_GPU_TEXTURETYPE_CUBE;
tex_info.format               = SDL_GPU_TEXTUREFORMAT_R8G8B8A8_UNORM_SRGB;
tex_info.usage                = SDL_GPU_TEXTUREUSAGE_SAMPLER;
tex_info.width                = face_size;
tex_info.height               = face_size;
tex_info.layer_count_or_depth = 6;  /* MUST be 6 for cube maps */
tex_info.num_levels           = 1;

SDL_GPUTexture *cubemap = SDL_CreateGPUTexture(device, &tex_info);

/* Upload each face as a separate layer (0=+X, 1=-X, 2=+Y, 3=-Y, 4=+Z, 5=-Z). */
for (int face = 0; face < 6; face++) {
    /* Load face image, convert to ABGR8888, map transfer buffer... */

    SDL_GPUTextureRegion dst;
    SDL_zero(dst);
    dst.texture = cubemap;
    dst.layer   = (Uint32)face;  /* Face index = layer index */
    dst.w       = face_size;
    dst.h       = face_size;
    dst.d       = 1;

    SDL_UploadToGPUTexture(copy_pass, &src, &dst, false);
}
```

## Skybox rendering pattern

### Vertex shader — depth = 1.0

```hlsl
cbuffer VertUniforms : register(b0, space1)
{
    column_major float4x4 vp_no_translation;
};

struct VSOutput
{
    float4 clip_pos  : SV_Position;
    float3 direction : TEXCOORD0;
};

VSOutput main(VSInput input)
{
    VSOutput output;
    output.direction = input.position;

    float4 pos = mul(vp_no_translation, float4(input.position, 1.0));
    output.clip_pos = pos.xyww;  /* z = w → depth = 1.0 after divide */

    return output;
}
```

### Fragment shader — sample cube map

```hlsl
TextureCube  skybox_tex : register(t0, space2);
SamplerState smp        : register(s0, space2);

float4 main(PSInput input) : SV_Target
{
    return skybox_tex.Sample(smp, input.direction);
}
```

### Pipeline settings

```c
/* Cull FRONT faces — we're inside the cube. */
pipe_info.rasterizer_state.cull_mode = SDL_GPU_CULLMODE_FRONT;

/* Depth test LESS_OR_EQUAL to pass at depth=1.0.
 * Depth write DISABLED — skybox should never occlude anything. */
pipe_info.depth_stencil_state.enable_depth_test  = true;
pipe_info.depth_stencil_state.enable_depth_write = false;
pipe_info.depth_stencil_state.compare_op = SDL_GPU_COMPAREOP_LESS_OR_EQUAL;
```

### Rotation-only view matrix

```c
/* Strip translation so the skybox always surrounds the camera. */
mat4 view_rot = view;
view_rot.m[12] = 0.0f;
view_rot.m[13] = 0.0f;
view_rot.m[14] = 0.0f;
mat4 vp_sky = mat4_multiply(proj, view_rot);
```

## Reflection mapping pattern

### Fragment shader with reflections

```hlsl
TextureCube env_tex : register(t1, space2);

/* Compute reflection direction */
float3 V = normalize(eye_pos.xyz - world_pos);
float3 R = reflect(-V, N);
float3 env_color = env_tex.Sample(env_smp, R).rgb;

/* Blend diffuse with environment reflection */
float3 blended = lerp(surface_color.rgb, env_color, reflectivity);
```

## Render order

1. Clear depth to 1.0
2. Draw skybox (depth write off, passes at depth=1.0)
3. Draw objects (depth write on, depth < 1.0 always passes)

## Common mistakes

1. **Forgetting `layer_count_or_depth = 6`** — cube maps require exactly 6 layers.
   Without this, texture creation fails silently or renders black.

2. **Wrong face order** — `SDL_GPUCubeMapFace` enum order is +X, -X, +Y, -Y, +Z, -Z.
   Mixing up faces produces seams or incorrect reflections.

3. **Depth write enabled on skybox** — the skybox writes depth=1.0 everywhere,
   occluding all subsequent geometry.  Always disable depth write for the skybox.

4. **Using full view matrix for skybox** — includes camera translation, causing
   visible parallax when moving.  Strip translation columns (m[12], m[13], m[14]).

5. **Wrong cull mode for skybox** — the camera is inside the cube, so front faces
   point inward (toward the camera).  Cull front faces, not back faces.

6. **Not negating V in reflect()** — `reflect()` expects the incident vector pointing
   toward the surface.  The view direction V points away from the surface, so pass
   `-V`.

## File layout

```text
shaders/
├── skybox.vert.hlsl      # Unit cube → clip space with depth=1.0
├── skybox.frag.hlsl      # Sample TextureCube
├── object.vert.hlsl      # Standard MVP + model (same as lighting)
└── object.frag.hlsl      # Blinn-Phong + reflect() + cube map sample
```

## References

- [Lesson 14 — Environment Mapping](../../../lessons/gpu/14-environment-mapping/)
- [Lesson 10 — Basic Lighting](../../../lessons/gpu/10-basic-lighting/) (Blinn-Phong)
- [Math Lesson 01 — Vectors](../../../lessons/math/01-vectors/) (dot product, reflection)
