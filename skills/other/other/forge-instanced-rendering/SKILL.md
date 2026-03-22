---
name: forge-instanced-rendering
description: Draw many copies of a mesh efficiently with per-instance vertex buffers. Use when rendering forests, particle systems, city blocks, or any scene with repeated geometry in SDL3 GPU.
---

Set up instanced rendering with per-instance transforms passed through vertex
attributes. One draw call renders all instances of a mesh.

## When to use

- Drawing **many copies** of the same mesh at different positions/rotations
- CPU draw-call overhead is a concern (10+ instances of the same mesh)
- Particles, vegetation, crowds, buildings, or any repeated geometry

## Core pattern

### 1. Instance data structure

Each instance gets a model matrix (64 bytes = 4 × float4 columns):

```c
typedef struct InstanceData {
    mat4 model;   /* 4 × vec4 columns, 64 bytes total */
} InstanceData;
```

### 2. Pipeline with two vertex buffer slots

Declare per-vertex AND per-instance buffer slots:

```c
SDL_GPUVertexBufferDescription vb_descs[2];

/* Slot 0: per-vertex mesh data */
vb_descs[0].slot       = 0;
vb_descs[0].pitch      = sizeof(YourVertex);
vb_descs[0].input_rate = SDL_GPU_VERTEXINPUTRATE_VERTEX;

/* Slot 1: per-instance transform data */
vb_descs[1].slot       = 1;
vb_descs[1].pitch      = sizeof(InstanceData);  /* 64 bytes */
vb_descs[1].input_rate = SDL_GPU_VERTEXINPUTRATE_INSTANCE;
```

### 3. Vertex attributes (7 total)

```c
SDL_GPUVertexAttribute attrs[7];

/* Per-vertex (slot 0) */
attrs[0] = { .location=0, .buffer_slot=0, .format=FLOAT3, .offset=offsetof(V, position) };
attrs[1] = { .location=1, .buffer_slot=0, .format=FLOAT3, .offset=offsetof(V, normal) };
attrs[2] = { .location=2, .buffer_slot=0, .format=FLOAT2, .offset=offsetof(V, uv) };

/* Per-instance (slot 1) — mat4 split into 4 columns */
attrs[3] = { .location=3, .buffer_slot=1, .format=FLOAT4, .offset=0 };   /* col 0 */
attrs[4] = { .location=4, .buffer_slot=1, .format=FLOAT4, .offset=16 };  /* col 1 */
attrs[5] = { .location=5, .buffer_slot=1, .format=FLOAT4, .offset=32 };  /* col 2 */
attrs[6] = { .location=6, .buffer_slot=1, .format=FLOAT4, .offset=48 };  /* col 3 */
```

### 4. Vertex shader — reconstruct matrix from columns

```hlsl
cbuffer VertUniforms : register(b0, space1) {
    column_major float4x4 vp;
};

struct VSInput {
    float3 position : TEXCOORD0;  /* per-vertex */
    float3 normal   : TEXCOORD1;
    float2 uv       : TEXCOORD2;
    float4 model_c0 : TEXCOORD3;  /* per-instance */
    float4 model_c1 : TEXCOORD4;
    float4 model_c2 : TEXCOORD5;
    float4 model_c3 : TEXCOORD6;
};

struct VSOutput {
    float4 clip_pos   : SV_Position; /* clip-space position */
    float2 uv         : TEXCOORD0;   /* texture coordinates */
    float3 world_norm : TEXCOORD1;   /* world-space normal  */
    float3 world_pos  : TEXCOORD2;   /* world-space position */
};

VSOutput main(VSInput input) {
    VSOutput output;

    /* Reconstruct column-major model matrix.
     * float4x4() takes ROWS, so transpose to get columns. */
    float4x4 model = transpose(float4x4(
        input.model_c0, input.model_c1,
        input.model_c2, input.model_c3));

    float4 wp = mul(model, float4(input.position, 1.0));
    output.clip_pos = mul(vp, wp);
    output.world_pos = wp.xyz;

    /* Normal transform: adjugate transpose (works for all matrices) */
    float3x3 m = (float3x3)model;
    float3x3 adj_t;
    adj_t[0] = cross(m[1], m[2]);
    adj_t[1] = cross(m[2], m[0]);
    adj_t[2] = cross(m[0], m[1]);
    output.world_norm = mul(adj_t, input.normal);

    output.uv = input.uv;

    return output;
}
```

### 5. Generate and upload instance transforms

```c
InstanceData instances[MAX_INSTANCES];
for (int i = 0; i < count; i++) {
    mat4 t = mat4_translate(positions[i]);
    mat4 r = mat4_rotate_y(angles[i]);
    mat4 s = mat4_scale(scales[i]);
    instances[i].model = mat4_multiply(t, mat4_multiply(r, s));
}

SDL_GPUBuffer *instance_buffer = upload_gpu_buffer(
    device, SDL_GPU_BUFFERUSAGE_VERTEX,
    instances, count * sizeof(InstanceData));
```

### 6. Render — bind both buffers, draw instanced

```c
SDL_GPUBufferBinding vb[2];
vb[0].buffer = mesh->vertex_buffer;     /* per-vertex */
vb[1].buffer = model->instance_buffer;  /* per-instance */
SDL_BindGPUVertexBuffers(pass, 0, vb, 2);

/* Bind index buffer */
SDL_GPUBufferBinding ib = { .buffer = mesh->index_buffer };
SDL_BindGPUIndexBuffer(pass, &ib, index_type);

/* THE instanced draw — instance_count is the key */
SDL_DrawGPUIndexedPrimitives(pass, index_count, instance_count, 0, 0, 0);
```

## Common mistakes

1. **Setting `instance_step_rate` to non-zero** — SDL3 GPU requires
   `instance_step_rate = 0` for all vertex buffer descriptions. The
   `VERTEXINPUTRATE_INSTANCE` input rate alone controls per-instance
   advancement.

2. **Wrong matrix reconstruction** — HLSL `float4x4(a,b,c,d)` treats arguments
   as ROWS. If your data is column-major (like forge_math.h), you must
   `transpose()` the result.

3. **Using the wrong buffer usage** — instance buffers use
   `SDL_GPU_BUFFERUSAGE_VERTEX`, not a special "instance" flag. The input rate
   on the pipeline description is what distinguishes per-vertex from
   per-instance.

4. **Not checking SDL return values** — every `SDL_CreateGPU*` and
   `SDL_SubmitGPUCommandBuffer` returns a value. Log the function name +
   `SDL_GetError()` on failure.

## Uniform layout

The instanced pipeline only pushes the VP matrix as a vertex uniform (64 bytes).
The model matrix comes from the instance buffer. Fragment uniforms (material +
lighting) are pushed per-material, same as non-instanced rendering.

## Performance notes

- Instanced rendering reduces **CPU overhead** (fewer draw calls, fewer uniform
  pushes), not GPU work. The GPU still processes the same number of triangles.
- One instanced draw call can replace hundreds of individual draw calls.
- For dynamic instances (moving objects), re-upload the instance buffer each
  frame using the transfer buffer pattern.
- Multiple different meshes can share the same instanced pipeline — just bind
  different vertex/instance buffers per mesh.

## Reference

- **Lesson**: [GPU Lesson 13 — Instanced Rendering](../../../lessons/gpu/13-instanced-rendering/)
- **Math**: mat4_translate, mat4_rotate_y, mat4_scale, mat4_multiply from forge_math.h
