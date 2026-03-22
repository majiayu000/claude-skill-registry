---
name: forge-gobo-spotlight
description: Add a projected-texture (gobo/cookie) spotlight with cone falloff, shadow map, and pattern projection to an SDL GPU project
---

Add a spotlight with inner/outer cone angles, projected gobo texture, and a
single 2D shadow map. The spotlight's view-projection matrix serves triple
duty — shadow mapping, gobo UV projection, and cone masking. Based on
[GPU Lesson 24](../../../lessons/gpu/24-gobo-spotlight/).

## When to use

- You need a focused light source with a defined cone (not omnidirectional)
- You want to project a pattern (window, foliage, abstract) through a light
- You need shadows from a spotlight (simpler than point light cube maps)
- You are building theatrical, cinematic, or stage-style lighting
- You already have an HDR rendering pipeline and Blinn-Phong lighting

## Key API calls

- `SDL_CreateGPUTexture` — shadow depth map (D32_FLOAT, 2D, `SAMPLER | DEPTH_STENCIL_TARGET`)
- `SDL_CreateGPUTexture` — gobo texture (R8G8B8A8_UNORM, 2D, `SAMPLER`)
- `SDL_CreateGPUSampler` — NEAREST + CLAMP for shadow, LINEAR + CLAMP for gobo
- `SDL_CreateGPUGraphicsPipeline` — shadow pipeline (depth-only, no color targets)
- `SDL_BeginGPURenderPass` — shadow pass with depth-only attachment
- `SDL_BindGPUFragmentSamplers` — bind diffuse + shadow + gobo textures in scene pass

## Correct order

1. **Define spotlight parameters** — position, target, inner/outer cone angles, color, intensity
2. **Compute light view-projection** — `mat4_look_at(pos, target, up)` + `mat4_perspective(2 * outer_angle, 1.0, near, far)`
3. **Create shadow depth texture** — D32_FLOAT, same resolution for shadow map (e.g. 1024x1024)
4. **Create shadow sampler** — NEAREST filter, CLAMP_TO_EDGE
5. **Load gobo texture** — grayscale PNG as UNORM (not sRGB), LINEAR sampler, CLAMP_TO_EDGE
6. **Create shadow pipeline** — vertex shader transforms by light_mvp, empty fragment shader, depth-only
7. **Create scene pipeline** — increase `num_samplers` to include shadow + gobo (e.g. 3 total)
8. **Each frame:**
   a. Shadow pass: render shadow casters from spotlight's perspective (depth-only)
   b. Scene pass: bind shadow map + gobo texture, fragment shader applies cone + gobo + shadow

## Key concepts

1. **Spotlight cone**: `smoothstep(cos_outer, cos_inner, cos_angle)` — cosine decreases with angle, so outer < inner
2. **Gobo projection**: light_vp transforms world pos → clip → NDC → UV for gobo texture sampling
3. **Triple-duty matrix**: the same light_vp handles shadow mapping, gobo UV mapping, and cone bounds
4. **Single 2D shadow map**: a spotlight's perspective frustum captures everything in one pass (unlike cube maps for point lights)
5. **UNORM gobo texture**: the gobo is a linear attenuation mask, not a color — use UNORM to avoid sRGB gamma
6. **Cone masking via UV bounds**: fragments projecting outside [0,1] UV get zero light via `step()` functions

## Common mistakes

- **Using sRGB format for the gobo texture** — the gobo is a light attenuation mask sampled linearly. sRGB applies an unwanted gamma curve. Use `R8G8B8A8_UNORM`.
- **Wrong smoothstep parameter order** — cosine is decreasing, so `smoothstep(cos_outer, cos_inner, ...)` with outer < inner. Swapping them inverts the cone.
- **Forgetting the Y-flip in UV remapping** — texture V increases downward; NDC Y increases upward. Always flip: `gobo_uv.y = 1.0 - gobo_uv.y`.
- **Shadow acne from insufficient bias** — add a small constant bias (0.002) when comparing depths in the shadow test.
- **Including the light source model as a shadow caster** — the searchlight/lamp model sits at the light position and would block its own light. Exclude it from the shadow pass.
- **FOV not matching outer cone angle** — the shadow/projection FOV must be `2 * outer_angle` to cover the full spotlight cone. Too narrow clips shadows; too wide wastes resolution.

## Spotlight definition

```c
#define SPOT_INNER_DEG  20.0f   /* full-intensity inner cone half-angle */
#define SPOT_OUTER_DEG  30.0f   /* falloff-to-zero outer cone half-angle */
#define SPOT_INTENSITY  5.0f    /* HDR brightness */
#define SPOT_NEAR       0.5f
#define SPOT_FAR        30.0f
#define SHADOW_MAP_SIZE 1024

/* Compute spotlight view-projection (static light). */
vec3 spot_pos    = vec3_create(6.0f, 5.0f, 4.0f);
vec3 spot_target = vec3_create(0.0f, 0.0f, 0.0f);
vec3 spot_up     = vec3_create(0.0f, 1.0f, 0.0f);

mat4 light_view = mat4_look_at(spot_pos, spot_target, spot_up);
float outer_rad = SPOT_OUTER_DEG * FORGE_DEG2RAD;
mat4 light_proj = mat4_perspective(2.0f * outer_rad, 1.0f, SPOT_NEAR, SPOT_FAR);
mat4 light_vp   = mat4_multiply(light_proj, light_view);
vec3 spot_dir   = vec3_normalize(vec3_sub(spot_target, spot_pos));
```

## Shadow depth texture

```c
SDL_GPUTextureCreateInfo ti;
SDL_zero(ti);
ti.type                 = SDL_GPU_TEXTURETYPE_2D;
ti.format               = SDL_GPU_TEXTUREFORMAT_D32_FLOAT;
ti.width                = SHADOW_MAP_SIZE;
ti.height               = SHADOW_MAP_SIZE;
ti.layer_count_or_depth = 1;
ti.num_levels           = 1;
ti.usage                = SDL_GPU_TEXTUREUSAGE_SAMPLER
                        | SDL_GPU_TEXTUREUSAGE_DEPTH_STENCIL_TARGET;

SDL_GPUTexture *shadow_depth = SDL_CreateGPUTexture(device, &ti);
```

## Gobo texture loading

```c
/* Use UNORM (not sRGB) — the gobo is a linear attenuation mask. */
SDL_GPUTextureCreateInfo tex_info;
SDL_zero(tex_info);
tex_info.type                = SDL_GPU_TEXTURETYPE_2D;
tex_info.format              = SDL_GPU_TEXTUREFORMAT_R8G8B8A8_UNORM;
tex_info.width               = w;
tex_info.height              = h;
tex_info.layer_count_or_depth = 1;
tex_info.num_levels          = 1;
tex_info.usage               = SDL_GPU_TEXTUREUSAGE_SAMPLER;

/* Gobo sampler — linear filtering for smooth projection, clamp to edge. */
SDL_GPUSamplerCreateInfo si;
SDL_zero(si);
si.min_filter     = SDL_GPU_FILTER_LINEAR;
si.mag_filter     = SDL_GPU_FILTER_LINEAR;
si.address_mode_u = SDL_GPU_SAMPLERADDRESSMODE_CLAMP_TO_EDGE;
si.address_mode_v = SDL_GPU_SAMPLERADDRESSMODE_CLAMP_TO_EDGE;
si.address_mode_w = SDL_GPU_SAMPLERADDRESSMODE_CLAMP_TO_EDGE;
```

## Fragment shader — spotlight with gobo and shadow

```hlsl
/* Direction from spotlight to fragment. */
float3 to_frag = world_pos - spot_pos;
float  dist    = length(to_frag);
float3 L_frag  = to_frag / dist;

/* Cone falloff. */
float cos_angle = dot(L_frag, normalize(spot_dir));
float cone = smoothstep(cos_outer, cos_inner, cos_angle);

if (cone > 0.0)
{
    /* Transform fragment into spotlight clip space. */
    float4 light_clip = mul(light_vp, float4(world_pos, 1.0));
    float3 light_ndc  = light_clip.xyz / light_clip.w;

    /* Gobo texture projection — remap NDC to UV space. */
    float2 gobo_uv = light_ndc.xy * 0.5 + 0.5;
    gobo_uv.y = 1.0 - gobo_uv.y;

    /* Cone masking — clamp to spotlight bounds. */
    float in_bounds = step(0.0, gobo_uv.x) * step(gobo_uv.x, 1.0) *
                      step(0.0, gobo_uv.y) * step(gobo_uv.y, 1.0);

    /* Sample gobo pattern (grayscale). */
    float gobo = gobo_tex.Sample(gobo_smp, gobo_uv).r;

    /* Shadow test with PCF. */
    float shadow = sample_shadow(light_ndc, texel_size);

    /* Blinn-Phong from spotlight. */
    float3 L = normalize(spot_pos - world_pos);
    float NdotL = max(dot(N, L), 0.0);
    float3 H = normalize(L + V);
    float NdotH = max(dot(N, H), 0.0);

    /* Quadratic attenuation. */
    float atten = 1.0 / (1.0 + 0.09 * dist + 0.032 * dist * dist);

    total_light += (albedo * NdotL + spec) * cone * gobo * shadow *
                   in_bounds * atten * spot_intensity * spot_color;
}
```

## Shadow pass — depth-only render

```c
/* Shadow pipeline: no color targets, depth-only. */
SDL_GPUDepthStencilTargetInfo shadow_depth_info;
SDL_zero(shadow_depth_info);
shadow_depth_info.texture     = shadow_depth_texture;
shadow_depth_info.load_op     = SDL_GPU_LOADOP_CLEAR;
shadow_depth_info.store_op    = SDL_GPU_STOREOP_STORE;
shadow_depth_info.clear_depth = 1.0f;

SDL_GPURenderPass *shadow_pass = SDL_BeginGPURenderPass(
    cmd, NULL, 0, &shadow_depth_info);
SDL_BindGPUGraphicsPipeline(shadow_pass, shadow_pipeline);

/* Draw shadow casters (exclude the light source model). */
draw_model_shadow(shadow_pass, cmd, &truck, &truck_mat, &light_vp);
for (int i = 0; i < BOX_COUNT; i++) {
    draw_model_shadow(shadow_pass, cmd, &box, &box_mat[i], &light_vp);
}

SDL_EndGPURenderPass(shadow_pass);
```

## Scene pass texture bindings

```c
/* Bind 3 samplers: diffuse, shadow depth, gobo pattern. */
SDL_GPUTextureSamplerBinding tex_binds[3];
tex_binds[0] = (SDL_GPUTextureSamplerBinding){
    .texture = diffuse_tex, .sampler = sampler };
tex_binds[1] = (SDL_GPUTextureSamplerBinding){
    .texture = shadow_depth_texture, .sampler = shadow_sampler };
tex_binds[2] = (SDL_GPUTextureSamplerBinding){
    .texture = gobo_texture, .sampler = gobo_sampler };
SDL_BindGPUFragmentSamplers(pass, 0, tex_binds, 3);
```
