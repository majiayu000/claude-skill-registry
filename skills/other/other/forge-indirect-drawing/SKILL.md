---
name: forge-indirect-drawing
description: >
  Add GPU-driven indirect drawing with compute-based frustum culling to an SDL
  GPU project. A compute shader tests bounding spheres against frustum planes
  and writes indirect draw commands — the CPU never decides what to draw.
  Uses SDL_DrawGPUIndexedPrimitivesIndirect with per-object storage buffers
  and the first_instance offset pattern for portable instance identification.
triggers:
  - indirect drawing
  - indirect draw
  - frustum culling
  - compute culling
  - GPU-driven rendering
  - DrawGPUIndexedPrimitivesIndirect
  - indirect buffer
  - visibility culling
  - bounding sphere culling
---

# Indirect Drawing with Compute Frustum Culling

Add GPU-driven rendering to an SDL GPU project where a compute shader performs
frustum culling and writes indirect draw commands. The CPU uploads object data
once; the GPU decides what to draw every frame.

Based on [GPU Lesson 38](../../../lessons/gpu/38-indirect-drawing/).

## When to use

- You have many instances of the same mesh and want the GPU to cull invisible ones
- You want to eliminate per-object CPU draw decisions entirely
- You need frustum culling without CPU-side bounding volume tests
- You want a debug visualization showing which objects are visible vs. culled

## Core data structures

### ObjectGPUData storage buffer

Each object's transform, color, bounding sphere, and draw arguments are packed
into a single struct stored in a GPU storage buffer. Both the compute shader
(for culling) and the vertex shader (for rendering) read from this buffer.

```c
/* Must match the HLSL ObjectData struct exactly.
 * Total: 112 bytes per object, 16-byte aligned. */
typedef struct ObjectGPUData {
    mat4     model;              /* offset  0: 64 bytes — model-to-world transform */
    float    color[4];           /* offset 64: 16 bytes — base color (RGBA) */
    float    bounding_sphere[4]; /* offset 80: 16 bytes — xyz=center(world), w=radius */
    Uint32   num_indices;        /* offset 96: 4 bytes  — index count for this object */
    Uint32   first_index;        /* offset 100: 4 bytes — first index in shared index buffer */
    Sint32   vertex_offset;      /* offset 104: 4 bytes — added to each index */
    Uint32   _pad;               /* offset 108: 4 bytes — align to 16 bytes */
} ObjectGPUData;                 /* 112 bytes */
```

### IndirectCommand (matches SDL_GPUIndexedIndirectDrawCommand)

```c
/* 20 bytes per command — 5 x uint32. Written by the compute shader. */
struct IndirectCommand {
    uint num_indices;
    uint num_instances;   /* 1 = visible, 0 = culled (hardware no-op) */
    uint first_index;
    int  vertex_offset;
    uint first_instance;  /* = object index, used for storage buffer lookup */
};
```

### CullUniforms

```c
typedef struct CullUniforms {
    float  frustum_planes[6][4];  /* 6 planes, each (nx, ny, nz, d) */
    Uint32 num_objects;
    Uint32 enable_culling;        /* 1 = cull, 0 = draw everything */
    float  _pad[2];               /* 16-byte alignment */
} CullUniforms;
```

## Buffer creation and usage flags

Each buffer requires specific usage flags to allow cross-pipeline access:

```c
/* Object data — read by compute (culling) and vertex shader (transforms) */
object_data_buf = upload_gpu_buffer(device,
    SDL_GPU_BUFFERUSAGE_COMPUTE_STORAGE_READ |
    SDL_GPU_BUFFERUSAGE_GRAPHICS_STORAGE_READ,
    objects, num_objects * sizeof(ObjectGPUData));

/* Indirect draw commands — written by compute, consumed by indirect draw */
SDL_GPUBufferCreateInfo bi;
SDL_zero(bi);
bi.usage = SDL_GPU_BUFFERUSAGE_INDIRECT |
           SDL_GPU_BUFFERUSAGE_COMPUTE_STORAGE_WRITE;
bi.size  = num_objects * 20;  /* 5 x uint32 per command */
indirect_buf = SDL_CreateGPUBuffer(device, &bi);

/* Visibility flags — written by compute, read by debug fragment shader */
SDL_zero(bi);
bi.usage = SDL_GPU_BUFFERUSAGE_COMPUTE_STORAGE_WRITE |
           SDL_GPU_BUFFERUSAGE_GRAPHICS_STORAGE_READ;
bi.size  = num_objects * sizeof(Uint32);
visibility_buf = SDL_CreateGPUBuffer(device, &bi);

/* Instance ID buffer — [0, 1, 2, ..., N-1] as a vertex buffer */
Uint32 ids[NUM_OBJECTS];
for (int i = 0; i < NUM_OBJECTS; i++) ids[i] = (Uint32)i;
instance_id_buf = upload_gpu_buffer(device,
    SDL_GPU_BUFFERUSAGE_VERTEX,
    ids, sizeof(ids));
```

## Instance ID vertex buffer pattern

`SV_InstanceID` does not consistently include `first_instance` across all GPU
backends. The portable alternative is a vertex buffer containing `[0, 1, ..., N-1]`
bound at `INSTANCE` input rate. Each indirect draw command sets `first_instance`
to the object index, so the instance attribute value equals the object index
regardless of backend.

### Vertex input state

```c
SDL_GPUVertexAttribute attrs[4];
SDL_zero(attrs);

/* Per-vertex: position (float3), location 0 */
attrs[0].location    = 0;
attrs[0].buffer_slot = 0;
attrs[0].format      = SDL_GPU_VERTEXELEMENTFORMAT_FLOAT3;
attrs[0].offset      = offsetof(SceneVertex, position);

/* Per-vertex: normal (float3), location 1 */
attrs[1].location    = 1;
attrs[1].buffer_slot = 0;
attrs[1].format      = SDL_GPU_VERTEXELEMENTFORMAT_FLOAT3;
attrs[1].offset      = offsetof(SceneVertex, normal);

/* Per-vertex: UV (float2), location 2 */
attrs[2].location    = 2;
attrs[2].buffer_slot = 0;
attrs[2].format      = SDL_GPU_VERTEXELEMENTFORMAT_FLOAT2;
attrs[2].offset      = offsetof(SceneVertex, uv);

/* Per-instance: object ID (uint32), location 3 */
attrs[3].location    = 3;
attrs[3].buffer_slot = 1;
attrs[3].format      = SDL_GPU_VERTEXELEMENTFORMAT_UINT;
attrs[3].offset      = 0;

SDL_GPUVertexBufferDescription vb_descs[2];
SDL_zero(vb_descs);
vb_descs[0].slot               = 0;
vb_descs[0].pitch              = sizeof(SceneVertex);
vb_descs[0].input_rate         = SDL_GPU_VERTEXINPUTRATE_VERTEX;
vb_descs[0].instance_step_rate = 0;
vb_descs[1].slot               = 1;
vb_descs[1].pitch              = sizeof(Uint32);
vb_descs[1].input_rate         = SDL_GPU_VERTEXINPUTRATE_INSTANCE;
vb_descs[1].instance_step_rate = 0;  /* MUST be 0 in SDL3 GPU */
```

## Compute cull shader

The compute shader reads object data, tests each bounding sphere against the
six frustum planes, and writes the indirect draw command. Culled objects get
`num_instances = 0` — a hardware no-op the GPU skips at zero cost.

```hlsl
struct ObjectData {
    float4x4 model;
    float4   color;
    float4   bounding_sphere;  /* xyz=center(world), w=radius */
    uint     num_indices;
    uint     first_index;
    int      vertex_offset;
    uint     _pad;
};

struct IndirectCommand {
    uint num_indices;
    uint num_instances;
    uint first_index;
    int  vertex_offset;
    uint first_instance;
};

StructuredBuffer<ObjectData>        objects           : register(t0, space0);
RWStructuredBuffer<IndirectCommand> indirect_commands : register(u0, space1);
RWStructuredBuffer<uint>            visibility        : register(u1, space1);

cbuffer CullUniforms : register(b0, space2) {
    float4 frustum_planes[6];
    uint   num_objects;
    uint   enable_culling;
    float2 _pad;
};

bool sphere_vs_frustum(float3 center, float radius) {
    [unroll]
    for (int i = 0; i < 6; i++) {
        float dist = dot(center, frustum_planes[i].xyz) + frustum_planes[i].w;
        if (dist < -radius)
            return false;
    }
    return true;
}

[numthreads(64, 1, 1)]
void main(uint3 tid : SV_DispatchThreadID) {
    uint idx = tid.x;
    if (idx >= num_objects) return;

    ObjectData obj = objects[idx];
    float3 center = obj.bounding_sphere.xyz;
    float  radius = obj.bounding_sphere.w;

    bool visible = (enable_culling == 0) || sphere_vs_frustum(center, radius);

    IndirectCommand cmd;
    cmd.num_indices    = obj.num_indices;
    cmd.num_instances  = visible ? 1 : 0;
    cmd.first_index    = obj.first_index;
    cmd.vertex_offset  = obj.vertex_offset;
    cmd.first_instance = idx;  /* object index for storage buffer lookup */

    indirect_commands[idx] = cmd;
    visibility[idx]        = visible ? 1 : 0;
}
```

## Vertex shader with storage buffer lookup

The vertex shader reads per-object transforms from a `StructuredBuffer` using
the `object_id` attribute passed via the instance vertex buffer:

```hlsl
struct ObjectTransform {
    column_major float4x4 model;
    float4   color;
    float4   bounding_sphere;
    uint     num_indices;
    uint     first_index;
    int      vertex_offset;
    uint     _pad;
};

StructuredBuffer<ObjectTransform> object_data : register(t0, space0);

cbuffer VertUniforms : register(b0, space1) {
    column_major float4x4 vp;
    column_major float4x4 light_vp;
};

struct VSInput {
    float3 position  : TEXCOORD0;
    float3 normal    : TEXCOORD1;
    float2 uv        : TEXCOORD2;
    uint   object_id : TEXCOORD3;  /* from instance vertex buffer */
};

VSOutput main(VSInput input) {
    VSOutput output;
    ObjectTransform obj = object_data[input.object_id];
    float4 world = mul(obj.model, float4(input.position, 1.0));
    output.clip_pos  = mul(vp, world);
    output.world_pos = world.xyz;
    output.color     = obj.color;
    /* ... normal transform, shadow coords, etc. ... */
    return output;
}
```

## Gribb-Hartmann frustum plane extraction

Extract 6 frustum planes from the view-projection matrix. Each plane is
`(nx, ny, nz, d)` where `dot(pos, n) + d` gives the signed distance.

**Vulkan [0,1] depth convention:** The near plane is `row2` alone, not
`row3 + row2` as in OpenGL's `[-1, 1]` depth range. Getting this wrong causes
the near plane to be positioned incorrectly, culling objects that should be
visible.

```c
static void extract_frustum_planes(mat4 vp, float planes[6][4])
{
    float m[16];
    SDL_memcpy(m, &vp, sizeof(m));

    /* Left:   row3 + row0 */
    planes[0][0] = m[3]  + m[0];
    planes[0][1] = m[7]  + m[4];
    planes[0][2] = m[11] + m[8];
    planes[0][3] = m[15] + m[12];

    /* Right:  row3 - row0 */
    planes[1][0] = m[3]  - m[0];
    planes[1][1] = m[7]  - m[4];
    planes[1][2] = m[11] - m[8];
    planes[1][3] = m[15] - m[12];

    /* Bottom: row3 + row1 */
    planes[2][0] = m[3]  + m[1];
    planes[2][1] = m[7]  + m[5];
    planes[2][2] = m[11] + m[9];
    planes[2][3] = m[15] + m[13];

    /* Top:    row3 - row1 */
    planes[3][0] = m[3]  - m[1];
    planes[3][1] = m[7]  - m[5];
    planes[3][2] = m[11] - m[9];
    planes[3][3] = m[15] - m[13];

    /* Near:   row2 only (Vulkan [0,1] depth — NOT row3+row2) */
    planes[4][0] = m[2];
    planes[4][1] = m[6];
    planes[4][2] = m[10];
    planes[4][3] = m[14];

    /* Far:    row3 - row2 */
    planes[5][0] = m[3]  - m[2];
    planes[5][1] = m[7]  - m[6];
    planes[5][2] = m[11] - m[10];
    planes[5][3] = m[15] - m[14];

    /* Normalize each plane for correct sphere-vs-plane distances */
    for (int i = 0; i < 6; i++) {
        float len = SDL_sqrtf(planes[i][0] * planes[i][0] +
                          planes[i][1] * planes[i][1] +
                          planes[i][2] * planes[i][2]);
        if (len > 0.0001f) {
            planes[i][0] /= len;
            planes[i][1] /= len;
            planes[i][2] /= len;
            planes[i][3] /= len;
        }
    }
}
```

## Compute dispatch

The compute pass runs before any render passes. It reads object data, writes
indirect commands and visibility flags:

```c
/* Fill cull uniforms on the CPU */
CullUniforms cull_uniforms;
SDL_zero(cull_uniforms);
cull_uniforms.num_objects    = NUM_OBJECTS;
cull_uniforms.enable_culling = culling_enabled ? 1 : 0;
extract_frustum_planes(cam_vp, cull_uniforms.frustum_planes);

SDL_PushGPUComputeUniformData(cmd, 0, &cull_uniforms, sizeof(cull_uniforms));

/* Bind read-write storage buffers for the compute pass */
SDL_GPUStorageBufferReadWriteBinding rw_bindings[2];
SDL_zero(rw_bindings);
rw_bindings[0].buffer = indirect_buf;
rw_bindings[0].cycle  = true;
rw_bindings[1].buffer = visibility_buf;
rw_bindings[1].cycle  = true;

SDL_GPUComputePass *compute = SDL_BeginGPUComputePass(
    cmd, NULL, 0, rw_bindings, 2);
if (compute) {
    SDL_BindGPUComputePipeline(compute, cull_pipeline);

    /* Object data as read-only storage buffer */
    SDL_GPUBuffer *ro_buf = object_data_buf;
    SDL_BindGPUComputeStorageBuffers(compute, 0, &ro_buf, 1);

    Uint32 groups = (NUM_OBJECTS + WORKGROUP_SIZE - 1) / WORKGROUP_SIZE;
    SDL_DispatchGPUCompute(compute, groups, 1, 1);

    SDL_EndGPUComputePass(compute);
}
```

## Indirect draw call

After the compute pass fills the indirect buffer, the render pass consumes it.
Bind the mesh vertex buffer in slot 0 and the instance ID buffer in slot 1,
then issue a single indirect draw call for all objects:

```c
SDL_BindGPUGraphicsPipeline(pass, indirect_pipeline);

/* Push uniforms */
VertUniforms vu = { .vp = cam_vp, .light_vp = light_vp };
SDL_PushGPUVertexUniformData(cmd, 0, &vu, sizeof(vu));

/* Bind object data as vertex storage buffer */
SDL_GPUBuffer *obj_buf = object_data_buf;
SDL_BindGPUVertexStorageBuffers(pass, 0, &obj_buf, 1);

/* Bind mesh vertex buffer (slot 0) + instance ID buffer (slot 1) */
SDL_GPUBufferBinding vb[2];
SDL_zero(vb);
vb[0].buffer = mesh_vertex_buffer;
vb[1].buffer = instance_id_buf;
SDL_BindGPUVertexBuffers(pass, 0, vb, 2);

/* Bind index buffer */
SDL_GPUBufferBinding ib;
SDL_zero(ib);
ib.buffer = mesh_index_buffer;
SDL_BindGPUIndexBuffer(pass, &ib, SDL_GPU_INDEXELEMENTSIZE_16BIT);

/* THE KEY CALL: GPU reads NUM_OBJECTS draw commands from the indirect
 * buffer. Culled objects have num_instances=0 — hardware skips them
 * at zero cost, no CPU round-trip needed. */
SDL_DrawGPUIndexedPrimitivesIndirect(pass, indirect_buf, 0, NUM_OBJECTS);
```

## Compute pipeline creation

```c
#define WORKGROUP_SIZE 64

SDL_GPUComputePipelineCreateInfo comp_ci;
SDL_zero(comp_ci);
comp_ci.code                            = cull_shader_bytecode;
comp_ci.code_size                       = cull_shader_size;
comp_ci.entrypoint                      = "main";
comp_ci.format                          = shader_format;
comp_ci.num_samplers                    = 0;
comp_ci.num_readonly_storage_textures   = 0;
comp_ci.num_readonly_storage_buffers    = 1;  /* object data */
comp_ci.num_readwrite_storage_textures  = 0;
comp_ci.num_readwrite_storage_buffers   = 2;  /* indirect commands + visibility */
comp_ci.num_uniform_buffers             = 1;  /* frustum planes + flags */
comp_ci.threadcount_x                   = WORKGROUP_SIZE;
comp_ci.threadcount_y                   = 1;
comp_ci.threadcount_z                   = 1;

SDL_GPUComputePipeline *cull_pipeline =
    SDL_CreateGPUComputePipeline(device, &comp_ci);
```

## Key API calls

- `SDL_DrawGPUIndexedPrimitivesIndirect()` — reads an array of indexed draw
  commands from a GPU buffer. Each command is 20 bytes (5 x uint32).
- `SDL_BeginGPUComputePass()` — starts a compute pass with read-write storage
  buffer bindings for the indirect and visibility buffers.
- `SDL_BindGPUComputeStorageBuffers()` — binds read-only storage buffers to
  compute shader slots.
- `SDL_DispatchGPUCompute()` — launches compute workgroups. Use
  `(num_objects + WORKGROUP_SIZE - 1) / WORKGROUP_SIZE` groups.
- `SDL_BindGPUVertexStorageBuffers()` — binds the object data storage buffer
  for the vertex shader to read per-instance transforms.

## Common mistakes

- **Using `SV_InstanceID` instead of the instance vertex buffer** —
  `SV_InstanceID` does not include `first_instance` on all backends (notably
  Vulkan). The instance ID buffer with `first_instance` offset is the portable
  solution.
- **Setting `instance_step_rate = 1`** — In SDL3 GPU, `instance_step_rate`
  must be 0 for all vertex buffer descriptions. Set `input_rate` to
  `SDL_GPU_VERTEXINPUTRATE_INSTANCE` instead. A non-zero step rate triggers an
  assertion failure in `SDL_CreateGPUGraphicsPipeline`.
- **Using OpenGL near plane extraction** — OpenGL uses `[-1, 1]` depth, so
  the near plane is `row3 + row2`. SDL GPU uses Vulkan's `[0, 1]` depth, so
  the near plane is `row2` alone. Getting this wrong places the near plane at
  the wrong distance and culls visible objects.
- **Forgetting to normalize frustum planes** — The sphere-vs-plane test
  `dot(center, n) + d` only produces correct world-space distances if the
  plane normal has unit length. Un-normalized planes cause incorrect culling at
  oblique angles.
- **Missing INDIRECT usage flag** — The indirect draw buffer must have
  `SDL_GPU_BUFFERUSAGE_INDIRECT` in addition to
  `SDL_GPU_BUFFERUSAGE_COMPUTE_STORAGE_WRITE`. Without it, the buffer cannot
  be used as an indirect draw source.
- **Missing GRAPHICS_STORAGE_READ on object data** — The object data buffer
  needs both `COMPUTE_STORAGE_READ` (for the cull shader) and
  `GRAPHICS_STORAGE_READ` (for the vertex shader). Missing the graphics flag
  prevents the vertex shader from reading transforms.
- **Not cycling read-write buffers** — Set `cycle = true` on the compute
  pass read-write bindings to allow the GPU to double-buffer. Without cycling,
  the compute and render passes may contend on the same memory.

## Cross-references

- [GPU Lesson 38 — Indirect Drawing](../../../lessons/gpu/38-indirect-drawing/)
  for the full walkthrough with dual-camera split-screen debug visualization
- [GPU Lesson 13 — Instanced Rendering](../../../lessons/gpu/13-instanced-rendering/)
  for the basic instanced rendering pattern that indirect drawing extends
- [GPU Lesson 11 — Compute Shaders](../../../lessons/gpu/11-compute-shaders/)
  for compute pipeline fundamentals
- [Math Lesson 05 — Matrices](../../../lessons/math/05-matrices/) for the
  view-projection matrix that frustum planes are extracted from
