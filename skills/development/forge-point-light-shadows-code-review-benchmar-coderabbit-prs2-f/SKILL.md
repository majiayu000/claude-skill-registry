---
name: forge-point-light-shadows
description: Add omnidirectional point light shadows with cube map depth textures to an SDL GPU project
---

Add omnidirectional shadow mapping for point lights using cube map textures.
Each point light renders the scene into a 6-face cube map storing linear depth,
then the fragment shader samples the cube map with a direction vector to
determine shadow coverage. Based on Lesson 23.

## When to use

- You need shadows from point lights (not directional)
- Shadows must work in all directions around a light source
- You have an HDR rendering pipeline and want to integrate shadow mapping
- You are extending a scene that already has Blinn-Phong or similar lighting

## Key API calls

- `SDL_CreateGPUTexture` — cube map textures (`TEXTURETYPE_CUBE`, R32_FLOAT, 6 layers, `COLOR_TARGET | SAMPLER`)
- `SDL_CreateGPUTexture` — shared depth buffer (D32_FLOAT, `DEPTH_STENCIL_TARGET`)
- `SDL_CreateGPUSampler` — NEAREST filter, CLAMP_TO_EDGE for shadow sampling
- `SDL_CreateGPUGraphicsPipeline` — shadow pipeline (R32_FLOAT color target + D32_FLOAT depth)
- `SDL_BeginGPURenderPass` — one pass per cube face, `layer_or_depth_plane` selects the face
- `SDL_BindGPUFragmentSamplers` — bind shadow cube maps for scene pass sampling

## Correct order

1. **Create shadow cube maps** — one `TEXTURETYPE_CUBE` R32_FLOAT texture per light
2. **Create shared depth buffer** — one D32_FLOAT 2D texture (reused across faces/lights)
3. **Create shadow sampler** — NEAREST, CLAMP_TO_EDGE
4. **Create shadow pipeline** — vertex + fragment shaders, CULLMODE_NONE, R32_FLOAT color + D32_FLOAT depth
5. **Create scene pipeline** — increase `num_samplers` to include shadow cube maps
6. **Each frame:**
   a. For each active light, compute 6 face view-projection matrices (90-degree FOV)
   b. For each face, render shadow casters into the cube face (set `layer_or_depth_plane`)
   c. Render scene with shadow cube maps bound as fragment samplers
   d. Fragment shader samples cube map with `world_pos - light_pos` direction

## Key concepts

1. **R32_FLOAT color targets** store linear depth (`distance / far_plane`) — uniform precision across range
2. **Cube face view-projection**: `mat4_look_at(light_pos, light_pos + dir, up)` with 90-degree perspective
3. **Y-flip compensation**: negate `projection.m[5]` because SDL3 GPU uses negative viewport height
4. **Shadow lookup**: `TextureCube.Sample(sampler, light_to_frag)` selects the correct face automatically
5. **Bias**: small constant (0.002) prevents shadow acne without causing Peter Panning
6. **Shared depth buffer**: one D32_FLOAT texture handles rasterization for all faces/lights

## Common mistakes

- **Forgetting the Y-flip** — SDL3 GPU normalizes viewport behavior across backends, which inverts cube face orientation. Negate `projection.m[5]` in the shadow projection.
- **Using hardware depth instead of linear depth** — z/w depth is non-linear and causes inconsistent shadow comparisons across cube faces. Store `distance / far_plane` explicitly.
- **Too much shadow bias** — bias > 0.01 causes visible shadow detachment (Peter Panning). Start with 0.002 and tune.
- **Front-face culling with non-watertight meshes** — front-face culling reduces Peter Panning for closed meshes but fails with glTF models that have open edges. Use `CULLMODE_NONE` for safety.
- **Forgetting to clear cube faces** — clear R32_FLOAT faces to 1.0 (max depth = fully lit) so unrendered areas produce no shadows.
- **Wrong sampler slot count** — the scene pipeline `num_samplers` must include both diffuse and all shadow cube maps (e.g., 5 for diffuse + 4 shadows).

## Shadow cube map creation

```c
#define SHADOW_MAP_SIZE   512
#define SHADOW_MAP_FORMAT SDL_GPU_TEXTUREFORMAT_R32_FLOAT
#define CUBE_FACE_COUNT   6

SDL_GPUTextureCreateInfo info;
SDL_zero(info);
info.type                  = SDL_GPU_TEXTURETYPE_CUBE;
info.format                = SHADOW_MAP_FORMAT;
info.width                 = SHADOW_MAP_SIZE;
info.height                = SHADOW_MAP_SIZE;
info.layer_count_or_depth  = CUBE_FACE_COUNT;
info.num_levels            = 1;
info.usage                 = SDL_GPU_TEXTUREUSAGE_COLOR_TARGET
                           | SDL_GPU_TEXTUREUSAGE_SAMPLER;

SDL_GPUTexture *shadow_cube = SDL_CreateGPUTexture(device, &info);
```

## Cube face view-projection matrices

```c
static void build_cube_face_vp(vec3 light_pos, mat4 out_vp[6]) {
    const vec3 look_dirs[6] = {
        { 1, 0, 0}, {-1, 0, 0}, {0, 1, 0},
        {0,-1, 0},  { 0, 0, 1}, {0, 0,-1},
    };
    const vec3 up_dirs[6] = {
        {0,-1, 0}, {0,-1, 0}, {0, 0, 1},
        {0, 0,-1}, {0,-1, 0}, {0,-1, 0},
    };

    mat4 proj = mat4_perspective(PI/2, 1.0f, 0.1f, 25.0f);
    proj.m[5] = -proj.m[5]; /* SDL3 GPU Y-flip compensation */

    for (int face = 0; face < 6; face++) {
        vec3 target = vec3_add(light_pos, look_dirs[face]);
        mat4 view = mat4_look_at(light_pos, target, up_dirs[face]);
        out_vp[face] = mat4_multiply(proj, view);
    }
}
```

## Shadow render pass (per face)

```c
SDL_GPUColorTargetInfo color_target;
SDL_zero(color_target);
color_target.texture               = shadow_cube;
color_target.layer_or_depth_plane  = (Uint32)face;
color_target.load_op               = SDL_GPU_LOADOP_CLEAR;
color_target.store_op              = SDL_GPU_STOREOP_STORE;
color_target.clear_color.r         = 1.0f; /* max depth = fully lit */

SDL_GPUDepthStencilTargetInfo depth_target;
SDL_zero(depth_target);
depth_target.texture     = shadow_depth;
depth_target.load_op     = SDL_GPU_LOADOP_CLEAR;
depth_target.store_op    = SDL_GPU_STOREOP_DONT_CARE;
depth_target.clear_depth = 1.0f;

SDL_GPURenderPass *pass = SDL_BeginGPURenderPass(cmd, &color_target, 1, &depth_target);
SDL_BindGPUGraphicsPipeline(pass, shadow_pipeline);
/* draw shadow casters */
SDL_EndGPURenderPass(pass);
```

## Shadow fragment shader

```hlsl
cbuffer FragUniforms : register(b0, space3)
{
    float3 light_pos;
    float  far_plane;
};

float4 main(float4 clip_pos : SV_Position,
            float3 world_pos : TEXCOORD0) : SV_Target
{
    float dist = length(world_pos - light_pos);
    return float4(dist / far_plane, 0.0, 0.0, 1.0);
}
```

## Shadow sampling in scene shader

```hlsl
float sample_shadow(int light_index, float3 light_to_frag)
{
    float current_depth = length(light_to_frag) / shadow_far_plane;
    float bias = 0.002;
    float stored_depth = shadow_cube.Sample(shadow_smp, light_to_frag).r;
    return (current_depth - bias > stored_depth) ? 0.0 : 1.0;
}

/* In lighting loop: */
float3 light_to_frag = world_pos - lights[i].position;
float shadow = sample_shadow(i, light_to_frag);
total_light += (diffuse + spec) * shadow * attenuation * intensity * color;
```

## Shadow pipeline setup

```c
/* Rasterizer: no culling (works with non-watertight meshes) */
pipe.rasterizer_state.cull_mode = SDL_GPU_CULLMODE_NONE;

/* Color target: R32_FLOAT for linear depth */
pipe.target_info.num_color_targets             = 1;
pipe.target_info.color_target_descriptions[0].format = SDL_GPU_TEXTUREFORMAT_R32_FLOAT;

/* Depth target: D32_FLOAT for rasterization */
pipe.target_info.has_depth_stencil_target = true;
pipe.target_info.depth_stencil_format     = SDL_GPU_TEXTUREFORMAT_D32_FLOAT;

/* Depth test enabled, write enabled */
pipe.depth_stencil_state.compare_op          = SDL_GPU_COMPAREOP_LESS;
pipe.depth_stencil_state.enable_depth_test   = true;
pipe.depth_stencil_state.enable_depth_write  = true;
```

## Reference

- **Lesson**: [GPU Lesson 23 — Point Light Shadows](../../../lessons/gpu/23-point-light-shadows/)
- **Cascaded shadows**: [GPU Lesson 15](../../../lessons/gpu/15-cascaded-shadow-maps/) — directional light shadow mapping
- **HDR prerequisite**: [GPU Lesson 21](../../../lessons/gpu/21-hdr-tone-mapping/) — floating-point render targets
- **Math**: [Lesson 06 — Projections](../../../lessons/math/06-projections/), [Lesson 09 — View Matrix](../../../lessons/math/09-view-matrix/)
