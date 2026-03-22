---
name: forge-particle-system
description: Add a GPU-driven particle system with compute shader simulation, billboard rendering, texture atlas animation, and blending modes to an SDL GPU project.
---

# GPU Particle System — Compute Simulation + Billboard Rendering

This skill adds a compute-shader-driven particle system to an SDL GPU project.
Particles live entirely on the GPU — the CPU only uploads simulation parameters
and a spawn budget each frame.

## When to use

- Fire, smoke, sparks, explosions, magic effects, weather
- Any scenario needing thousands of animated sprites at interactive frame rates
- When particle behavior is simple enough for GPU parallelism (no complex
  inter-particle dependencies)

## Architecture

```text
CPU each frame:
  1. Upload spawn count (4 bytes) to counter buffer via copy pass
  2. Push SimUniforms (dt, gravity, drag, emitter params)
  3. Dispatch compute shader
  4. Draw MAX_PARTICLES * 6 primitives (vertex pulling, no VB)
```

### Particle struct (64 bytes, float4-aligned)

```hlsl
struct Particle {
    float4 pos_lifetime;   // xyz=position, w=lifetime remaining
    float4 vel_size;       // xyz=velocity, w=billboard size
    float4 color;          // rgba
    float4 max_life_type;  // x=max_lifetime, y=type, z=original_size
};
```

### GPU buffer setup

```c
/* Dual usage: compute writes, vertex shader reads */
buf_info.usage = SDL_GPU_BUFFERUSAGE_COMPUTE_STORAGE_WRITE
               | SDL_GPU_BUFFERUSAGE_GRAPHICS_STORAGE_READ;
```

### Compute shader register layout

```hlsl
RWStructuredBuffer<Particle> particles     : register(u0, space1);
RWStructuredBuffer<int>      spawn_counter : register(u1, space1);
cbuffer SimUniforms                        : register(b0, space2);
```

### Atomic spawn recycling

Dead particles attempt to claim spawn slots atomically:

```hlsl
if (p.pos_lifetime.w <= 0.0) {
    int prev;
    InterlockedAdd(spawn_counter[0], -1, prev);
    if (prev > 0) {
        p = spawn_particle(idx, emitter_type);
    }
}
```

### Billboard vertex shader (vertex pulling)

```hlsl
StructuredBuffer<Particle> particles : register(t0, space0);
cbuffer BillboardUniforms            : register(b0, space1);

// 6 vertices per particle, 2 triangles
uint particle_idx = SV_VertexID / 6;
uint corner_idx   = SV_VertexID % 6;

// Camera-facing quad
float3 offset = cam_right * corner.x * size + cam_up * corner.y * size;
float3 world_pos = particle.pos + offset;
```

### Fragment shader

```hlsl
Texture2D    atlas_tex : register(t0, space2);
SamplerState atlas_smp : register(s0, space2);
```

### Blending pipelines

**Additive** (fire, sparks — order-independent):

```c
ctd.blend_state.src_color_blendfactor = SDL_GPU_BLENDFACTOR_SRC_ALPHA;
ctd.blend_state.dst_color_blendfactor = SDL_GPU_BLENDFACTOR_ONE;
```

**Alpha** (smoke, clouds — needs sorting for correctness):

```c
ctd.blend_state.src_color_blendfactor = SDL_GPU_BLENDFACTOR_SRC_ALPHA;
ctd.blend_state.dst_color_blendfactor = SDL_GPU_BLENDFACTOR_ONE_MINUS_SRC_ALPHA;
```

Both: depth test ON, depth write OFF, cull mode NONE.

### Atlas UV calculation

```hlsl
float age_ratio = 1.0 - (lifetime / max_lifetime);
age_ratio = clamp(age_ratio, 0.0, 0.999);  // keep frame in [0, 15]
uint frame = (uint)(age_ratio * 16.0);  // 4x4 atlas
uint row = frame / 4;
uint col = frame % 4;
float2 uv = (float2(col, row) + corner_uv) * 0.25;
```

## Frame flow with forge_scene.h

```c
forge_scene_begin_frame(s);

// 1. Copy pass: reset spawn counter
SDL_GPUCopyPass *copy = SDL_BeginGPUCopyPass(cmd);
SDL_UploadToGPUBuffer(copy, &src, &dst, false);
SDL_EndGPUCopyPass(copy);

// 2. Compute pass: simulate + emit
SDL_PushGPUComputeUniformData(cmd, 0, &sim, sizeof(sim));
SDL_GPUComputePass *compute = SDL_BeginGPUComputePass(cmd, NULL, 0, rw, 2);
SDL_BindGPUComputePipeline(compute, sim_pipeline);
SDL_DispatchGPUCompute(compute, groups, 1, 1);
SDL_EndGPUComputePass(compute);

// 3. Shadow + main pass
forge_scene_begin_shadow_pass(s);
forge_scene_end_shadow_pass(s);
forge_scene_begin_main_pass(s);
forge_scene_draw_grid(s);

// 4. Draw particles (vertex pulling)
SDL_BindGPUGraphicsPipeline(pass, particle_pipeline);
SDL_BindGPUVertexStorageBuffers(pass, 0, &particle_buffer, 1);
SDL_BindGPUFragmentSamplers(pass, 0, &atlas_bind, 1);
SDL_PushGPUVertexUniformData(cmd, 0, &bb, sizeof(bb));
SDL_DrawGPUPrimitives(pass, MAX_PARTICLES * 6, 1, 0, 0);

forge_scene_end_main_pass(s);
```

## Common mistakes

- **Vertex shader uniform in wrong register space**: Vertex uniforms use
  `register(b0, space1)`, not `space2`. Fragment samplers use `space2`.
  Mixing these up causes D3D12 pipeline creation failure.
- **StructuredBuffer float3 stride mismatch**: DXIL uses 12-byte stride for
  float3, SPIRV uses 16. Always use float4 fields and read `.xyz`.
- **Depth write ON for transparent particles**: Particles with blending must
  disable depth write, otherwise they occlude each other based on draw order.
- **Forgetting to reset the spawn counter**: The counter must be uploaded via
  copy pass each frame. Without reset, the counter stays at 0 (or negative)
  and no particles spawn after the first frame.
- **cycle=true on particle buffer**: Using `cycle=true` on the RW binding
  allocates a new (undefined) buffer each frame, losing all particle state.
  Use `cycle=false` to preserve particle data between frames.

## Reference

- **Lesson**: [GPU Lesson 46 — Particle Animations](../../../lessons/gpu/46-particle-animations/)
- **Compute shaders**: [GPU Lesson 11](../../../lessons/gpu/11-compute-shaders/)
- **Vertex pulling**: [GPU Lesson 33](../../../lessons/gpu/33-vertex-pulling/)
- **Blending**: [GPU Lesson 16](../../../lessons/gpu/16-blending/)
- **Physics concepts**: [Physics Lesson 01](../../../lessons/physics/01-point-particles/)
