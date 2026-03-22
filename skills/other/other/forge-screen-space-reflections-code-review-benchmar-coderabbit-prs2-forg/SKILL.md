---
name: forge-screen-space-reflections
description: >
  Add screen-space reflections (SSR) with ray marching to an SDL GPU project.
  Use when someone needs realistic reflections on surfaces without expensive
  cube maps or environment probes, working with deferred rendering.
---

# Screen-Space Reflections — SDL3 GPU Skill

Implement realistic reflections by ray marching through screen space, sampling
depth and normal data to compute accurate reflection rays.

## When to use this skill

- Adding reflections to wet surfaces, mirrors, or polished floors
- Building a deferred rendering pipeline with multiple render targets (MRT)
- Avoiding the cost of cube maps or reflective capture probes
- Combining shadow mapping with reflective surfaces
- Creating a G-buffer (geometry buffer) to decouple lighting from reflections

## G-buffer texture creation

Create the main textures for deferred rendering:

```c
/* 1. Color + reflectivity (R8G8B8A8) */
SDL_GPUTextureCreateInfo color_info;
SDL_zero(color_info);
color_info.type   = SDL_GPU_TEXTURETYPE_2D;
color_info.format = SDL_GPU_TEXTUREFORMAT_R8G8B8A8_UNORM;
color_info.usage  = SDL_GPU_TEXTUREUSAGE_COLOR_TARGET | SDL_GPU_TEXTUREUSAGE_SAMPLER;
color_info.width  = width;
color_info.height = height;
SDL_GPUTexture *color_tex = SDL_CreateGPUTexture(device, &color_info);

/* 2. Normals (R16G16B16A16_FLOAT for precision) */
SDL_GPUTextureCreateInfo normal_info;
SDL_zero(normal_info);
normal_info.type   = SDL_GPU_TEXTURETYPE_2D;
normal_info.format = SDL_GPU_TEXTUREFORMAT_R16G16B16A16_FLOAT;
normal_info.usage  = SDL_GPU_TEXTUREUSAGE_COLOR_TARGET | SDL_GPU_TEXTUREUSAGE_SAMPLER;
normal_info.width  = width;
normal_info.height = height;
SDL_GPUTexture *normal_tex = SDL_CreateGPUTexture(device, &normal_info);

/* 3. World position (R16G16B16A16_FLOAT for SSR ray marching) */
SDL_GPUTextureCreateInfo pos_info;
SDL_zero(pos_info);
pos_info.type   = SDL_GPU_TEXTURETYPE_2D;
pos_info.format = SDL_GPU_TEXTUREFORMAT_R16G16B16A16_FLOAT;
pos_info.usage  = SDL_GPU_TEXTUREUSAGE_COLOR_TARGET | SDL_GPU_TEXTUREUSAGE_SAMPLER;
pos_info.width  = width;
pos_info.height = height;
SDL_GPUTexture *pos_tex = SDL_CreateGPUTexture(device, &pos_info);

/* 4. Depth (D32_FLOAT for precision) */
SDL_GPUTextureCreateInfo depth_info;
SDL_zero(depth_info);
depth_info.type   = SDL_GPU_TEXTURETYPE_2D;
depth_info.format = SDL_GPU_TEXTUREFORMAT_D32_FLOAT;
depth_info.usage  = SDL_GPU_TEXTUREUSAGE_DEPTH_STENCIL_TARGET | SDL_GPU_TEXTUREUSAGE_SAMPLER;
depth_info.width  = width;
depth_info.height = height;
SDL_GPUTexture *depth_tex = SDL_CreateGPUTexture(device, &depth_info);

/* 5. SSR output (R8G8B8A8 for reflection color) */
SDL_GPUTextureCreateInfo ssr_info;
SDL_zero(ssr_info);
ssr_info.type   = SDL_GPU_TEXTURETYPE_2D;
ssr_info.format = SDL_GPU_TEXTUREFORMAT_R8G8B8A8_UNORM;
ssr_info.usage  = SDL_GPU_TEXTUREUSAGE_COLOR_TARGET | SDL_GPU_TEXTUREUSAGE_SAMPLER;
ssr_info.width  = width;
ssr_info.height = height;
SDL_GPUTexture *ssr_tex = SDL_CreateGPUTexture(device, &ssr_info);
```

## Render pass order

### 1. Shadow pass (standard depth pass)

Render depth from light viewpoint to shadow map. Used in G-buffer pass for
shadow computation.

### 2. G-buffer pass (MRT: color, normals, world position)

```c
/* Create colorful render pass with 3 color targets + depth */
SDL_GPURenderPass *render_pass = SDL_BeginGPURenderPass(
    cmd_buf,
    NULL,  /* No color targets for this example, using targets array */
    0,
    depth_tex,
    &(SDL_GPUColorTargetInfo) {
        .texture = color_tex,
        .load_op = SDL_GPU_LOADOP_CLEAR,
        .store_op = SDL_GPU_STOREOP_STORE,
        .clear_color = { 0.0f, 0.0f, 0.0f, 1.0f }
    }
);

/* Bind normal, position, color targets */
SDL_GPUColorTargetInfo targets[3] = {
    {
        .texture = color_tex,
        .load_op = SDL_GPU_LOADOP_CLEAR,
        .store_op = SDL_GPU_STOREOP_STORE,
        .clear_color = { 0.0f, 0.0f, 0.0f, 1.0f }
    },
    {
        .texture = normal_tex,
        .load_op = SDL_GPU_LOADOP_CLEAR,
        .store_op = SDL_GPU_STOREOP_STORE,
        .clear_color = { 0.5f, 0.5f, 1.0f, 0.0f }  /* Default normal */
    },
    {
        .texture = pos_tex,
        .load_op = SDL_GPU_LOADOP_CLEAR,
        .store_op = SDL_GPU_STOREOP_STORE,
        .clear_color = { 0.0f, 0.0f, 0.0f, 0.0f }
    }
};

SDL_GPURenderPass *render_pass = SDL_BeginGPURenderPass(
    cmd_buf,
    targets,
    3,  /* 3 color targets */
    depth_tex,
    NULL  /* No depth target info needed here */
);

/* Bind G-buffer pipeline and render geometry */
SDL_BindGPUGraphicsPipeline(render_pass, gbuffer_pipe);
SDL_DrawGPUPrimitives(render_pass, vertex_count, 1, 0, 0);

SDL_EndGPURenderPass(render_pass);
```

### 3. SSR ray march pass (fullscreen quad)

```c
/* SSR uniform buffer structure */
typedef struct {
    mat4 proj;                  /* Projection matrix */
    mat4 proj_inv;              /* Inverse projection */
    mat4 view;                  /* View matrix */
    vec3 camera_pos;            /* Camera position in world space */
    float max_distance;         /* Max ray march distance */
    vec3 padding1;
    float max_steps;            /* Ray march step count */
    float step_size;            /* Initial step size */
    float thickness;            /* Thickness for depth test tolerance */
    float fade_distance;        /* Distance to fade edge reflections */
    float edge_fade;            /* Edge fade factor for screen borders */
} SSRUniforms;

SSRUniforms ssr_uniforms = {
    .proj = proj,
    .proj_inv = mat4_inverse(proj),
    .view = view,
    .camera_pos = camera_pos,
    .max_distance = 100.0f,
    .max_steps = 64.0f,
    .step_size = 0.5f,
    .thickness = 0.1f,
    .fade_distance = 50.0f,
    .edge_fade = 0.1f
};

SDL_GPURenderPass *ssr_pass = SDL_BeginGPURenderPass(
    cmd_buf,
    &(SDL_GPUColorTargetInfo) {
        .texture = ssr_tex,
        .load_op = SDL_GPU_LOADOP_CLEAR,
        .store_op = SDL_GPU_STOREOP_STORE,
        .clear_color = { 0.0f, 0.0f, 0.0f, 0.0f }
    },
    1,
    NULL
);

SDL_BindGPUGraphicsPipeline(ssr_pass, ssr_pipe);

/* Bind G-buffer textures */
SDL_BindGPUFragmentSamplers(
    ssr_pass,
    &(SDL_GPUTextureSamplerBinding) {
        .texture = color_tex,
        .sampler = sampler
    },
    0,
    1
);
SDL_BindGPUFragmentSamplers(
    ssr_pass,
    &(SDL_GPUTextureSamplerBinding) {
        .texture = normal_tex,
        .sampler = sampler
    },
    1,
    1
);
SDL_BindGPUFragmentSamplers(
    ssr_pass,
    &(SDL_GPUTextureSamplerBinding) {
        .texture = pos_tex,
        .sampler = sampler
    },
    2,
    1
);
SDL_BindGPUFragmentSamplers(
    ssr_pass,
    &(SDL_GPUTextureSamplerBinding) {
        .texture = depth_tex,
        .sampler = sampler
    },
    3,
    1
);

/* Push SSR uniforms */
SDL_PushGPUFragmentUniformData(cmd_buf, 0, &ssr_uniforms, sizeof(SSRUniforms));

/* Draw fullscreen quad */
SDL_DrawGPUPrimitives(ssr_pass, 6, 1, 0, 0);  /* 2 triangles = 6 vertices */

SDL_EndGPURenderPass(ssr_pass);
```

### 4. Composite pass (blend SSR with scene)

```c
SDL_GPURenderPass *composite_pass = SDL_BeginGPURenderPass(
    cmd_buf,
    &(SDL_GPUColorTargetInfo) {
        .texture = backbuffer,
        .load_op = SDL_GPU_LOADOP_CLEAR,
        .store_op = SDL_GPU_STOREOP_STORE,
        .clear_color = { 0.0f, 0.0f, 0.0f, 1.0f }
    },
    1,
    NULL
);

SDL_BindGPUGraphicsPipeline(composite_pass, composite_pipe);

/* Bind color and SSR textures */
SDL_BindGPUFragmentSamplers(
    composite_pass,
    &(SDL_GPUTextureSamplerBinding) {
        .texture = color_tex,
        .sampler = sampler
    },
    0,
    1
);
SDL_BindGPUFragmentSamplers(
    composite_pass,
    &(SDL_GPUTextureSamplerBinding) {
        .texture = ssr_tex,
        .sampler = sampler
    },
    1,
    1
);

/* Draw fullscreen quad */
SDL_DrawGPUPrimitives(composite_pass, 6, 1, 0, 0);

SDL_EndGPURenderPass(composite_pass);
```

## G-buffer vertex shader

Output world position and normal to textures:

```hlsl
cbuffer VertUniforms : register(b0, space1)
{
    column_major float4x4 model;
    column_major float4x4 view;
    column_major float4x4 proj;
};

struct VSInput
{
    float3 position : POSITION;
    float3 normal   : NORMAL;
};

struct VSOutput
{
    float4 clip_pos : SV_Position;
    float3 world_pos : TEXCOORD0;
    float3 world_normal : TEXCOORD1;
};

VSOutput main(VSInput input)
{
    VSOutput output;

    float4 world_pos = mul(float4(input.position, 1.0), model);
    output.world_pos = world_pos.xyz;

    float3 world_normal = mul(input.normal, (float3x3)model);
    output.world_normal = normalize(world_normal);

    float4 view_pos = mul(world_pos, view);
    output.clip_pos = mul(view_pos, proj);

    return output;
}
```

## G-buffer fragment shader

Output to 3 color targets:

```hlsl
Texture2D shadow_map : register(t4, space2);
SamplerState smp : register(s0, space2);

cbuffer LightUniforms : register(b0, space0)
{
    float3 light_dir;
    float pad1;
    float3 light_color;
    float pad2;
    float3 ambient;
    float pad3;
    column_major float4x4 light_vp;
};

struct PSOutput
{
    float4 color : SV_Target0;      /* Diffuse + reflectivity */
    float4 normal : SV_Target1;     /* World normal */
    float4 position : SV_Target2;   /* World position */
};

PSOutput main(VSOutput input)
{
    PSOutput output;

    /* Diffuse color */
    float3 base_color = float3(0.8, 0.8, 0.8);

    /* Compute shadow (simplified) */
    float4 light_space = mul(float4(input.world_pos, 1.0), light_vp);
    float2 shadow_uv = light_space.xy / light_space.w * 0.5 + 0.5;
    float depth = shadow_map.Sample(smp, shadow_uv).r;
    float shadow = (light_space.z > depth + 0.001) ? 0.5 : 1.0;

    /* Blinn-Phong diffuse */
    float diffuse = max(dot(input.world_normal, light_dir), 0.0);
    float3 lit = base_color * light_color * diffuse * shadow;

    /* Output to targets */
    output.color = float4(lit, 0.5);           /* Alpha = reflectivity */
    output.normal = float4(input.world_normal, 0.0);
    output.position = float4(input.world_pos, 1.0);

    return output;
}
```

## SSR ray march shader (fragment)

Sample G-buffer and march reflection rays:

```hlsl
Texture2D color_tex : register(t0, space2);
Texture2D normal_tex : register(t1, space2);
Texture2D pos_tex : register(t2, space2);
Texture2D depth_tex : register(t3, space2);
SamplerState smp : register(s0, space2);

cbuffer SSRUniforms : register(b0, space0)
{
    column_major float4x4 proj;
    column_major float4x4 proj_inv;
    column_major float4x4 view;
    float3 camera_pos;
    float max_distance;
    float3 padding1;
    float max_steps;
    float step_size;
    float thickness;
    float fade_distance;
    float edge_fade;
};

float4 main(float4 clip_pos : SV_Position, float2 uv : TEXCOORD0) : SV_Target
{
    /* Sample G-buffer at this pixel */
    float3 base_color = color_tex.Sample(smp, uv).rgb;
    float reflectivity = color_tex.Sample(smp, uv).a;
    float3 normal = normal_tex.Sample(smp, uv).rgb;
    float3 world_pos = pos_tex.Sample(smp, uv).rgb;

    if (reflectivity < 0.01) {
        return float4(0.0, 0.0, 0.0, 0.0);  /* Not reflective */
    }

    /* Compute reflection direction */
    float3 V = normalize(camera_pos - world_pos);
    float3 R = reflect(-V, normal);

    /* Ray march in screen space */
    float4 ray_origin = mul(float4(world_pos, 1.0), view);
    ray_origin = mul(ray_origin, proj);
    float2 screen_origin = ray_origin.xy / ray_origin.w * 0.5 + 0.5;

    float3 ray_end = world_pos + R * max_distance;
    float4 ray_end_screen = mul(float4(ray_end, 1.0), view);
    ray_end_screen = mul(ray_end_screen, proj);
    float2 screen_end = ray_end_screen.xy / ray_end_screen.w * 0.5 + 0.5;

    float2 ray_dir = (screen_end - screen_origin) / max_steps;

    float3 reflection = float3(0.0, 0.0, 0.0);
    float hit_count = 0.0;

    for (float step = 1.0; step < max_steps; step += 1.0) {
        float2 screen_sample = screen_origin + ray_dir * step;

        /* Clamp to screen bounds with fade */
        float edge_fade_factor = 1.0;
        if (screen_sample.x < edge_fade || screen_sample.x > 1.0 - edge_fade) {
            edge_fade_factor *= 1.0 - abs(screen_sample.x - clamp(screen_sample.x, edge_fade, 1.0 - edge_fade)) / edge_fade;
        }
        if (screen_sample.y < edge_fade || screen_sample.y > 1.0 - edge_fade) {
            edge_fade_factor *= 1.0 - abs(screen_sample.y - clamp(screen_sample.y, edge_fade, 1.0 - edge_fade)) / edge_fade;
        }

        if (edge_fade_factor < 0.01) break;

        /* Reconstruct where the ray is at this step in world space */
        float3 ray_world = world_pos + R * (step * step_size);
        float3 sampled_pos = pos_tex.Sample(smp, screen_sample).rgb;

        /* Compare sampled surface against current ray position */
        float distance_to_surface = length(sampled_pos - ray_world);
        if (distance_to_surface < thickness) {
            reflection = color_tex.Sample(smp, screen_sample).rgb;
            hit_count = 1.0;
            break;
        }

        if (length(ray_world - world_pos) > fade_distance) break;
    }

    return float4(reflection * hit_count, hit_count);
}
```

## Composite shader (blend scene + SSR)

```hlsl
Texture2D scene : register(t0, space2);
Texture2D ssr : register(t1, space2);
SamplerState smp : register(s0, space2);

float4 main(float2 uv : TEXCOORD0) : SV_Target
{
    float4 scene_color = scene.Sample(smp, uv);
    float4 ssr_color = ssr.Sample(smp, uv);

    /* Blend reflections where hit_count > 0 */
    return lerp(scene_color, ssr_color, ssr_color.a * 0.5);
}
```

## Common mistakes

1. **Missing world position in G-buffer** — SSR requires world-space position
   to compute ray direction and check depth. Without it, ray marching fails.
   Always output `float4(world_pos, 1.0)` as the third MRT target.

2. **Swapping texture binding slots** — G-buffer pass outputs to targets 0, 1, 2
   but the SSR pass must sample them at slots 0, 1, 2 in the same order.
   Mismatch causes black or inverted reflections.

3. **Forgetting reflectivity in G-buffer** — Store reflectivity in the alpha
   channel of the color target. Without it, non-reflective surfaces show
   unwanted reflections.

4. **Mismatched uniform struct layout** — The C struct field order must match
   the HLSL `cbuffer` layout exactly. Add explicit `float _pad[N]` fields to
   align `float3` members to 16-byte boundaries, and use
   `static_assert(sizeof(MyUniforms) == EXPECTED)` to catch layout mismatches
   at compile time.

5. **No edge fadeout** — Reflections at screen borders sample invalid data.
   Always apply a fade factor based on distance from screen edges.

6. **Ray march direction in wrong space** — Ray origin and direction must be
   computed consistently in either clip space or NDC. Mixing spaces produces
   diagonal artifacts.

7. **Depth precision** — Use `D32_FLOAT` for depth, not `D24_S8`. The extra
   precision prevents z-fighting in depth comparisons.

8. **Not normalizing normals in G-buffer** — Bilinear interpolation of normals
   produces non-unit vectors. Always `normalize()` sampled normals in SSR shader.

## File layout

```text
shaders/
├── gbuffer.vert.hlsl       # Output world position, normal, MVP
├── gbuffer.frag.hlsl       # Output to 3 targets (color, normal, position)
├── ssr.vert.hlsl           # Fullscreen quad vertex shader
├── ssr.frag.hlsl           # Ray march reflection rays
├── composite.vert.hlsl     # Fullscreen quad vertex shader
└── composite.frag.hlsl     # Blend scene + SSR
```

## Math functions used

- `mat4_inverse()` — compute inverse projection for ray reconstruction
- `vec3_normalize()` — normalize surface normals sampled from G-buffer
- `vec3_reflect()` — compute reflection direction

See [Math Lesson 01 — Vectors](../../../lessons/math/01-vectors/) for reflection formula.

## References

- [Lesson 29 — Screen-Space Reflections](../../../lessons/gpu/29-screen-space-reflections/)
- [Lesson 27 — SSAO](../../../lessons/gpu/27-ssao/) (G-buffer, depth reconstruction)
- [Lesson 15 — Cascaded Shadow Maps](../../../lessons/gpu/15-cascaded-shadow-maps/) (depth precision)
- [Lesson 10 — Basic Lighting](../../../lessons/gpu/10-basic-lighting/) (Blinn-Phong diffuse)
- [Math Lesson 01 — Vectors](../../../lessons/math/01-vectors/) (reflection, dot product)
