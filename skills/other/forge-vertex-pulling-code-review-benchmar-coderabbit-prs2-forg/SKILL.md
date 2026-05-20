---
name: forge-vertex-pulling
description: >
  Add vertex pulling (programmable vertex fetch) to an SDL GPU project.
  Replace fixed-function vertex input with storage buffer reads in the
  vertex shader using SV_VertexID and StructuredBuffer.
triggers:
  - vertex pulling
  - storage buffer vertex
  - programmable vertex fetch
  - bindless vertex
  - SV_VertexID fetch
  - remove vertex attributes
  - flexible vertex format
---

# Vertex Pulling with SDL3 GPU

Replace the fixed-function vertex input assembler with manual storage buffer
reads in the vertex shader. The pipeline declares zero vertex attributes and
the shader fetches vertex data from a `StructuredBuffer` using `SV_VertexID`.

Based on [GPU Lesson 33 — Vertex Pulling](../../../lessons/gpu/33-vertex-pulling/).

## When to use

- Meshes with different vertex layouts sharing one pipeline
- Compute shaders writing vertex data for the vertex shader to read
- Compressed or packed vertex formats decoded in the shader
- GPU-driven rendering with indirect draw calls
- Reducing pipeline state complexity and pipeline object count

## HLSL pattern

### Vertex shader (pulled)

```hlsl
struct PulledVertex
{
    float3 position;
    float3 normal;
    float2 uv;
};

/* Vertex storage buffer: register(t0, space0) for DXIL vertex shaders.
 * Slot index follows sampled textures and storage textures (if any). */
StructuredBuffer<PulledVertex> vertex_buffer : register(t0, space0);

cbuffer SceneUniforms : register(b0, space1)
{
    column_major float4x4 mvp;
    column_major float4x4 model;
};

struct VSOutput
{
    float4 clip_pos  : SV_Position;
    float3 world_pos : TEXCOORD0;
    float3 world_nrm : TEXCOORD1;
    float2 uv        : TEXCOORD2;
};

VSOutput main(uint vertex_id : SV_VertexID)
{
    VSOutput output;
    PulledVertex v = vertex_buffer[vertex_id];

    float4 world = mul(model, float4(v.position, 1.0));
    output.clip_pos  = mul(mvp, float4(v.position, 1.0));
    output.world_pos = world.xyz;
    output.world_nrm = normalize(mul((float3x3)model, v.normal));
    output.uv        = v.uv;
    return output;
}
```

### Fragment shader

No changes needed — fragment shaders work identically regardless of whether
vertex data came from the input assembler or a storage buffer.

## C-side pattern

### 1. Define the vertex struct (must match HLSL)

```c
typedef struct PulledVertex {
    vec3 position;   /* 12 bytes */
    vec3 normal;     /* 12 bytes */
    vec2 uv;         /*  8 bytes */
} PulledVertex;      /* 32 bytes */
```

### 2. Upload as storage buffer (not vertex buffer)

```c
/* The only CPU-side difference: buffer usage flag */
SDL_GPUBuffer *storage_buf = upload_gpu_buffer(
    device,
    SDL_GPU_BUFFERUSAGE_GRAPHICS_STORAGE_READ,  /* NOT VERTEX */
    vertex_data,
    vertex_count * sizeof(PulledVertex));
```

### 3. Create shader with storage buffer count

```c
/* Vertex shader: declare 1 storage buffer */
SDL_GPUShaderCreateInfo info;
SDL_zero(info);
info.stage               = SDL_GPU_SHADERSTAGE_VERTEX;
info.num_samplers        = 0;
info.num_storage_buffers = 1;   /* <-- vertex data storage buffer */
info.num_uniform_buffers = 1;
/* ... format, code, entrypoint ... */
```

### 4. Create pipeline with empty vertex input

```c
/* No vertex buffer descriptions, no vertex attributes */
SDL_GPUVertexInputState vis;
SDL_zero(vis);
/* vis.num_vertex_buffers    = 0;  already zero */
/* vis.num_vertex_attributes = 0;  already zero */

SDL_GPUGraphicsPipelineCreateInfo pi;
SDL_zero(pi);
pi.vertex_input_state = vis;
/* ... rest of pipeline setup ... */
```

### 5. Bind and draw

```c
/* Bind storage buffer instead of vertex buffer */
SDL_GPUBuffer *bufs[1] = { storage_buf };
SDL_BindGPUVertexStorageBuffers(pass, 0, bufs, 1);

/* Index buffer binding is unchanged */
SDL_GPUBufferBinding ib = { index_buffer, 0 };
SDL_BindGPUIndexBuffer(pass, &ib, index_type);
SDL_DrawGPUIndexedPrimitives(pass, index_count, 1, 0, 0, 0);
```

## SDL GPU register mapping

For **DXIL** vertex shaders, resources are bound in this order at `space0`:

1. Sampled textures (`t0..tN`)
2. Storage textures (`tN+1..`)
3. Storage buffers (`tN+M+1..`)

With zero sampled/storage textures, the first storage buffer is `t0, space0`.

For **SPIR-V** vertex shaders, storage buffers go in descriptor set 0 after
sampled and storage textures.

## Combining with other techniques

- **Compute → Vertex**: Use `SDL_GPU_BUFFERUSAGE_GRAPHICS_STORAGE_READ |
  SDL_GPU_BUFFERUSAGE_COMPUTE_STORAGE_WRITE` so a compute shader can write
  the buffer and the vertex shader can read it.

- **Indirect drawing** (Lesson 38): Vertex pulling pairs naturally with
  indirect draws for fully GPU-driven rendering.

- **Multiple vertex formats**: One pipeline can render meshes with different
  vertex layouts by defining multiple `StructuredBuffer` structs or using
  a `ByteAddressBuffer` with manual offset calculations.

## Common mistakes

| Mistake | Fix |
|---|---|
| Using `SDL_GPU_BUFFERUSAGE_VERTEX` | Use `SDL_GPU_BUFFERUSAGE_GRAPHICS_STORAGE_READ` |
| Forgetting `num_storage_buffers = 1` on shader | Set it in `SDL_GPUShaderCreateInfo` |
| Calling `SDL_BindGPUVertexBuffers` | Use `SDL_BindGPUVertexStorageBuffers` |
| Mismatched C/HLSL struct layout | Ensure identical field order and sizes |
| Leaving vertex attributes in pipeline | Set `num_vertex_buffers = 0`, `num_vertex_attributes = 0` |
