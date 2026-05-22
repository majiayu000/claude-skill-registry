---
name: forge-procedural-sky
description: Add a physically-based procedural sky with atmospheric scattering (Rayleigh, Mie, ozone) to an SDL GPU project using per-pixel ray marching with LUT-accelerated transmittance and multi-scattering
user_invokable: true
---

# Procedural Sky (Hillaire)

Add a physically-based atmospheric sky to an SDL GPU project. Implements
Sebastien Hillaire's atmospheric model (EGSR 2020) with LUT-accelerated
transmittance and multi-scattering, producing correct sky colors at any
time of day.

## When to use

- Outdoor scenes that need a dynamic sky background
- Time-of-day systems (sunrise, noon, sunset, twilight, night)
- Replacing static skybox textures with physically correct skies
- Scenes where the sun position changes dynamically
- Any project needing atmospheric scattering (aerial perspective)

## Architecture

### Render pipeline

6 pipelines: 2 compute (one-time) + 4 graphics (per frame).

**One-time compute passes (at startup):**

1. **Transmittance LUT** (256×64) — compute shader, 40-step march/texel
2. **Multi-scattering LUT** (32×32) — compute shader, 64 dirs × 20 steps

**Per-frame render passes:**

1. **Sky pass** — Fullscreen quad, atmosphere ray march + LUT sampling → HDR
2. **Bloom downsample** (5×) — 13-tap Jimenez with Karis → mip chain
3. **Bloom upsample** (4×) — 9-tap tent, additive blend → mip 0
4. **Tonemap pass** — HDR + bloom → swapchain (ACES filmic)

### Key shaders

#### transmittance_lut.comp.hlsl

Compute shader generating the transmittance LUT. Uses Bruneton non-linear
UV mapping that concentrates precision near the horizon.

```hlsl
/* Register layout (compute spaces) */
RWTexture2D<float4> output_tex : register(u0, space1);  /* RW output */

/* LUT dimensions are compile-time constants — no uniform buffer needed. */
static const float LUT_WIDTH  = 256.0;
static const float LUT_HEIGHT = 64.0;

[numthreads(8, 8, 1)]
void main(uint3 id : SV_DispatchThreadID) { ... }
```

#### multiscatter_lut.comp.hlsl

Compute shader generating the multi-scattering LUT. Reads the
transmittance LUT and integrates over 64 sphere directions.

```hlsl
/* Register layout (compute spaces) */
Texture2D<float4> transmittance_lut : register(t0, space0);  /* sampled */
SamplerState      trans_sampler     : register(s0, space0);
RWTexture2D<float4> output_tex : register(u0, space1);       /* RW output */

/* LUT dimensions are compile-time constants — no uniform buffer needed. */
static const float LUT_WIDTH  = 32.0;
static const float LUT_HEIGHT = 32.0;

[numthreads(8, 8, 1)]
void main(uint3 id : SV_DispatchThreadID) { ... }
```

#### sky.frag.hlsl

All atmosphere constants are `static const` in the shader. Uniforms
are camera position, sun direction, and march step count. LUT textures
are bound as fragment samplers.

Core functions (implement in this order):

```hlsl
/* 1. Ray-sphere test — find atmosphere entry/exit */
bool ray_sphere_intersect(float3 ro, float3 rd, float radius,
                          out float t_near, out float t_far);

/* 2. Phase functions — angular scattering distribution */
float rayleigh_phase(float cos_theta);      /* (3/16pi)(1+cos^2 theta) */
float mie_phase_hg(float cos_theta, float g); /* Henyey-Greenstein g=0.8 */

/* 3. Medium sampling — density at altitude */
MediumSample sample_medium(float3 pos);     /* returns scatter + extinction */

/* 4. LUT sampling — O(1) transmittance lookup */
float3 sample_transmittance(float view_height, float cos_zenith);

/* 5. LUT sampling — multi-scattering lookup */
float3 sample_multiscatter(float altitude, float cos_sun_zenith);

/* 6. Main march — outer loop with LUT-accelerated sampling */
float3 atmosphere(float3 ray_origin, float3 ray_dir,
                  out float3 transmittance);

/* 7. Sun disc — rendered on top with limb darkening */
float3 sun_disc(float3 ray_dir, float3 sun_dir, float3 transmittance);
```

### Atmosphere constants (Hillaire EGSR 2020, Table 1)

```hlsl
static const float R_GROUND = 6360.0;  /* Earth radius (km) */
static const float R_ATMO   = 6460.0;  /* atmosphere top (km) */

/* Rayleigh — molecular scattering, wavelength-dependent */
static const float3 RAYLEIGH_SCATTER = float3(5.802e-3, 13.558e-3, 33.1e-3);
static const float  RAYLEIGH_H = 8.0;  /* scale height (km) */

/* Mie — aerosol scattering, nearly white */
static const float MIE_SCATTER = 3.996e-3;
static const float MIE_ABSORB  = 0.444e-3;
static const float MIE_H       = 1.2;
static const float MIE_G       = 0.8;  /* forward-peak asymmetry */

/* Ozone — absorption only (no scattering) */
static const float3 OZONE_ABSORB = float3(0.650e-3, 1.881e-3, 0.085e-3);
static const float  OZONE_CENTER = 25.0;  /* peak altitude (km) */
static const float  OZONE_WIDTH  = 15.0;  /* tent half-width (km) */
```

### Vertex shader: ray matrix reconstruction

```hlsl
cbuffer SkyVertUniforms : register(b0, space1) {
    float4x4 ray_matrix; /* maps NDC to world-space directions */
};

/* Map NDC to world-space ray direction via the ray matrix */
float4 world_pos = mul(ray_matrix, float4(ndc.x, ndc.y, 1.0, 1.0));
output.view_ray = world_pos.xyz / world_pos.w;
```

### Fragment shader: LUT bindings

```hlsl
/* LUT textures bound as fragment samplers (space2) */
Texture2D<float4> transmittance_lut : register(t0, space2);
SamplerState      trans_sampler     : register(s0, space2);
Texture2D<float4> multiscatter_lut  : register(t1, space2);
SamplerState      ms_sampler        : register(s1, space2);

/* Uniforms (space3) */
cbuffer SkyFragUniforms : register(b0, space3) {
    float3 cam_pos_km;
    float  sun_intensity;
    float3 sun_dir;
    int    num_steps;
    float2 resolution;
    float2 _pad;
};
```

### C-side uniform structures

```c
/* Sky vertex: ray matrix mapping NDC to world-space directions (64 bytes).
 * Built from camera basis vectors scaled by FOV/aspect — avoids precision
 * loss from inverse VP at planet-centric coordinates (~6360 km). */
typedef struct SkyVertUniforms {
    mat4 ray_matrix;
} SkyVertUniforms;

/* Sky fragment: camera + sun + march params (48 bytes) */
typedef struct SkyFragUniforms {
    float cam_pos_km[3];
    float sun_intensity;     /* default: 20.0 */
    float sun_dir[3];
    int   num_steps;         /* default: 32 */
    float resolution[2];
    float _pad[2];
} SkyFragUniforms;

/* No uniform struct needed for compute shaders — LUT dimensions are
 * compile-time constants in the HLSL (static const). */
```

### Compute pipeline creation

```c
/* Create compute pipeline (same pattern as lesson 11).
 * No uniform buffers — LUT dimensions are compile-time constants. */
state->transmittance_compute = create_compute_pipeline(
    device,
    transmittance_lut_comp_spirv, sizeof(transmittance_lut_comp_spirv),
    transmittance_lut_comp_dxil, sizeof(transmittance_lut_comp_dxil),
    0, 1, 0,  /* 0 samplers, 1 RW texture, 0 uniform buffers */
    8, 8, 1); /* workgroup size matches [numthreads(8,8,1)] */

state->multiscatter_compute = create_compute_pipeline(
    device,
    multiscatter_lut_comp_spirv, sizeof(multiscatter_lut_comp_spirv),
    multiscatter_lut_comp_dxil, sizeof(multiscatter_lut_comp_dxil),
    1, 1, 0,  /* 1 sampler (transmittance LUT), 1 RW texture, 0 uniforms */
    8, 8, 1);
```

### LUT texture creation

```c
SDL_GPUTextureCreateInfo tex_info;
SDL_zero(tex_info);
tex_info.type = SDL_GPU_TEXTURETYPE_2D;
tex_info.format = SDL_GPU_TEXTUREFORMAT_R16G16B16A16_FLOAT;
tex_info.layer_count_or_depth = 1;
tex_info.num_levels = 1;
tex_info.usage = SDL_GPU_TEXTUREUSAGE_COMPUTE_STORAGE_WRITE
               | SDL_GPU_TEXTUREUSAGE_SAMPLER;

tex_info.width = 256;
tex_info.height = 64;
state->transmittance_lut = SDL_CreateGPUTexture(device, &tex_info);

tex_info.width = 32;
tex_info.height = 32;
state->multiscatter_lut = SDL_CreateGPUTexture(device, &tex_info);
```

### One-time LUT dispatch

```c
/* Two separate compute passes — SDL GPU does NOT synchronize
 * reads/writes within a single compute pass. */

/* Pass 1: Transmittance */
SDL_GPUStorageTextureReadWriteBinding storage;
storage.texture = state->transmittance_lut;
SDL_GPUComputePass *pass = SDL_BeginGPUComputePass(cmd, &storage, 1, NULL, 0);
SDL_BindGPUComputePipeline(pass, state->transmittance_compute);
SDL_DispatchGPUCompute(pass, 256/8, 64/8, 1);
SDL_EndGPUComputePass(pass);

/* Pass 2: Multi-scattering (reads transmittance LUT) */
storage.texture = state->multiscatter_lut;
pass = SDL_BeginGPUComputePass(cmd, &storage, 1, NULL, 0);
SDL_BindGPUComputePipeline(pass, state->multiscatter_compute);
SDL_GPUTextureSamplerBinding sampler_binding = {
    .texture = state->transmittance_lut,
    .sampler = state->lut_sampler
};
SDL_BindGPUComputeSamplers(pass, 0, &sampler_binding, 1);
SDL_DispatchGPUCompute(pass, 32/8, 32/8, 1);
SDL_EndGPUComputePass(pass);

SDL_SubmitGPUCommandBuffer(cmd);
SDL_WaitForGPUIdle(device);  /* LUTs must be ready before first frame */
```

### LUT sampling in fragment shader

```c
/* Bind LUT textures before the sky draw call */
SDL_GPUTextureSamplerBinding lut_bindings[2];
lut_bindings[0] = { .texture = transmittance_lut, .sampler = lut_sampler };
lut_bindings[1] = { .texture = multiscatter_lut,  .sampler = lut_sampler };
SDL_BindGPUFragmentSamplers(pass, 0, lut_bindings, 2);
```

### Sun direction from angles

```c
/* elevation: radians above horizon (0=horizon, pi/2=zenith)
 * azimuth: radians from east (increases CCW viewed from above) */
static vec3 sun_direction_from_angles(float elevation, float azimuth) {
    float cos_el = SDL_cosf(elevation);
    vec3 dir;
    dir.x = cos_el * SDL_cosf(azimuth);
    dir.y = SDL_sinf(elevation);
    dir.z = cos_el * SDL_sinf(azimuth);
    return dir;
}
```

### Camera setup

Planet-centric coordinates in km. Camera starts at surface:

```c
#define CAM_START_Y 6360.001f  /* 1 meter above sea level */
#define CAM_SPEED   0.2f       /* km/s base speed */
#define NEAR_PLANE  0.0001f    /* 0.1 meters in km */
#define FAR_PLANE   1000.0f    /* 1000 km */
```

## Key API calls

| Function | Purpose |
|----------|---------|
| `SDL_CreateGPUTexture` | HDR target, LUT textures (COMPUTE\_STORAGE\_WRITE + SAMPLER) |
| `SDL_CreateGPUSampler` | Linear/clamp samplers for HDR, bloom, and LUTs |
| `SDL_CreateGPUComputePipeline` | 2 compute pipelines (transmittance, multiscatter) |
| `SDL_CreateGPUGraphicsPipeline` | 4 graphics pipelines (sky, downsample, upsample, tonemap) |
| `SDL_BeginGPUComputePass` | Bind RW storage textures for compute dispatch |
| `SDL_BindGPUComputePipeline` | Bind compute pipeline before dispatch |
| `SDL_BindGPUComputeSamplers` | Bind transmittance LUT for multiscatter pass |
| `SDL_DispatchGPUCompute` | Launch compute workgroups |
| `SDL_PushGPUVertexUniformData` | Push ray matrix to sky vertex shader |
| `SDL_PushGPUFragmentUniformData` | Push sky params, bloom params, tonemap params |
| `SDL_BindGPUFragmentSamplers` | Bind LUT textures, bloom/HDR textures |
| `SDL_DrawGPUPrimitives` | Fullscreen quad (6 verts, no vertex buffer) |
| `quat_right`, `quat_up`, `quat_forward` | Camera basis vectors for ray matrix |
| `quat_from_euler` | Camera orientation from yaw/pitch |

## Bloom pipeline (reused from Lesson 22)

The sky needs HDR + bloom because the sun disc emits values far
exceeding 1.0. See the [bloom skill](../forge-bloom/SKILL.md) for full
bloom downsample/upsample implementation details.

Key adaptation for sky: the bloom threshold catches the bright sun
disc and creates a natural glow halo.

## Common mistakes

1. **Inverse VP fails at planet-centric coordinates** — Do NOT use the
   inverse view-projection matrix to reconstruct ray directions. The camera
   is at `(0, 6360.001, 0)` km — the subtraction `world_pos - cam_pos`
   in the fragment shader loses all float32 precision (`6360.0 - 6360.001`
   has only ~7 significant digits). Use a ray matrix built from camera
   basis vectors instead. The fragment shader then just calls
   `normalize(input.view_ray)` — no position subtraction needed.

2. **Wrong coordinate system** — All constants are in km. If you place the
   camera at `(0, 0, 0)` instead of `(0, 6360.001, 0)`, it's inside the
   planet. The camera Y must be ≥ R_GROUND.

3. **Missing HDR render target** — Rendering the sky directly to the LDR
   swapchain clips all values above 1.0, losing the sun disc and any
   bloom. Always render to R16G16B16A16_FLOAT first.

4. **Bloom upsample without additive blend** — The upsample pipeline must
   use ONE+ONE additive blending with LOADOP_LOAD. Without this, each
   upsample pass overwrites the downsample data instead of accumulating.

5. **Sun disc too bright without bloom** — The sun outputs
   `sun_intensity * 10.0`, which is 200× the sky brightness. Without
   bloom and tone mapping, this appears as a hard white circle with no
   soft glow.

6. **Sun disc visible below the horizon** — The `sun_disc()` function must
   check if the planet occludes the sun. Before rendering the disc, test
   `ray_sphere_intersect(cam_pos, sun_dir, R_GROUND)` — if the ray hits
   the ground with `t_near > 0`, suppress the disc. The atmosphere ray
   march handles this naturally (inner march returns zero when it hits
   the ground), but the sun disc is rendered separately and needs its own
   occlusion test.

7. **Ray matrix not updated on resize** — If the window resizes, the
   aspect ratio changes. The ray matrix must be recomputed every frame
   from the current window dimensions.

8. **Compute passes must be separate for synchronization** — SDL GPU does
   NOT implicitly synchronize reads and writes within a single compute
   pass. The multi-scattering pass reads the transmittance LUT, so it
   must be a separate `SDL_BeginGPUComputePass` / `SDL_EndGPUComputePass`
   from the transmittance write pass. SDL does synchronize between passes
   on the same command buffer.

9. **Compute samplers use space0, not space2** — In compute shaders,
   sampled textures go in `t[n], space0` and samplers in `s[n], space0`.
   This is different from fragment shaders which may use higher spaces.
   RW storage textures use `u[n], space1` and uniforms use `b[n], space2`.

10. **LUT texture needs both COMPUTE\_STORAGE\_WRITE and SAMPLER** — The
    compute shader writes to it (storage), then the fragment shader reads
    from it (sampler). Both usage flags must be set at creation time.

11. **Missing earth shadow** — At each sample point in the atmosphere
    march, test whether the planet blocks sunlight with
    `ray_sphere_intersect(pos, sun_dir, R_GROUND)`. Without this, points
    in the planet's shadow still contribute inscattered light, washing out
    warm Rayleigh sunset colors with incorrect cold blue light. Apply
    `earth_shadow` only to the single-scatter term; multi-scatter is not
    shadowed in the fragment shader (it's pre-integrated in the LUT).
    Add `horizon_fade = saturate(cos_sun_zenith * 10.0 + 0.5)` to smooth
    the terminator boundary.

12. **Multi-scatter LUT must include earth shadow** — The 64-direction
    inner march in the multi-scatter compute shader also needs the earth
    shadow test. Without it, the LUT stores non-zero values for
    below-horizon sun angles. The symptom is warm sunset colors that
    appear only after the sun sets and persist indefinitely.

13. **Transmittance LUT forward/inverse mapping mismatch** — The forward
    mapping (params → UV, used for lookups) must be the exact mathematical
    inverse of the reverse mapping (UV → params, used in the compute
    shader). Do NOT clip the ray distance `d` to the ground intersection
    in the forward mapping — always use the atmosphere sphere distance.
    Below-horizon sun directions are handled by earth shadow, not by the
    transmittance parameterization.

## Reference implementation

- [Lesson 26 main.c](../../../lessons/gpu/26-procedural-sky/main.c)
- [sky.frag.hlsl](../../../lessons/gpu/26-procedural-sky/shaders/sky.frag.hlsl)
- [transmittance_lut.comp.hlsl](../../../lessons/gpu/26-procedural-sky/shaders/transmittance_lut.comp.hlsl)
- [multiscatter_lut.comp.hlsl](../../../lessons/gpu/26-procedural-sky/shaders/multiscatter_lut.comp.hlsl)
- [Lesson 22 — Bloom](../../../lessons/gpu/22-bloom/) — HDR + bloom pipeline
- [Lesson 11 — Compute Shaders](../../../lessons/gpu/11-compute-shaders/) —
  Compute pipeline fundamentals
- Hillaire, S. (2020). *A Scalable and Production-Ready Sky and
  Atmosphere Rendering Technique.* EGSR 2020.
