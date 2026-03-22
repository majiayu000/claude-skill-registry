---
name: forge-first-triangle
description: Draw colored geometry with vertex buffers, shaders, and a graphics pipeline using SDL3 GPU API. Use when someone needs to render vertices with per-vertex attributes.
---

# First Triangle — Vertex Buffers, Shaders & Pipeline

This skill teaches how to draw colored geometry with SDL3's GPU API.
It builds on the `forge-sdl-gpu-setup` skill (device, window, swapchain, render loop).

## When to use

- Drawing any geometry (triangles, quads, meshes)
- Setting up vertex buffers with per-vertex attributes
- Creating a graphics pipeline with shaders
- Uploading CPU data to the GPU

## Vertex data pattern

Define a vertex struct matching your shader inputs:

```c
typedef struct Vertex {
    float x, y;      /* position in NDC (float2) → TEXCOORD0 in HLSL */
    float r, g, b;   /* color (float3)           → TEXCOORD1 in HLSL */
} Vertex;
```

**Rule:** The C struct layout must exactly match the vertex attributes you
declare in the pipeline's vertex input state.

**Coordinate spaces:** For the first triangle lesson, positions are provided
directly in **NDC** (Normalized Device Coordinates), which is clip space with
w = 1. The range is [-1, 1] for x and y. Later lessons introduce model-view-projection
matrices to transform from model space. See `lessons/math/02-coordinate-spaces`
for the complete transformation pipeline.

## Shader conventions

SDL GPU uses HLSL semantics for vertex inputs:

| Vertex attribute location | HLSL semantic |
|--------------------------|---------------|
| 0                        | TEXCOORD0     |
| 1                        | TEXCOORD1     |
| 2                        | TEXCOORD2     |
| N                        | TEXCOORD{N}   |

Output position uses `SV_Position`. Fragment shader output uses `SV_Target`.

**Shader resource counts** must be declared when creating a shader object:
`num_samplers`, `num_storage_textures`, `num_storage_buffers`, `num_uniform_buffers`.

## Shader compilation

Write HLSL source, compile to SPIRV and DXIL with `dxc`:

```bash
# SPIRV (Vulkan) — requires Vulkan SDK
dxc -spirv -T vs_6_0 -E main shader.vert.hlsl -Fo shader.vert.spv
dxc -spirv -T ps_6_0 -E main shader.frag.hlsl -Fo shader.frag.spv

# DXIL (D3D12)
dxc -T vs_6_0 -E main shader.vert.hlsl -Fo shader.vert.dxil
dxc -T ps_6_0 -E main shader.frag.hlsl -Fo shader.frag.dxil
```

Embed compiled bytecodes as C byte arrays in header files, then pick the
right format at runtime based on `SDL_GetGPUShaderFormats(device)`.

## Creating shaders — correct order

```c
SDL_GPUShaderCreateInfo info = { 0 };
info.code      = bytecode;           /* SPIRV or DXIL bytes */
info.code_size = bytecode_size;
info.entrypoint = "main";
info.format    = SDL_GPU_SHADERFORMAT_SPIRV;  /* or DXIL */
info.stage     = SDL_GPU_SHADERSTAGE_VERTEX;  /* or FRAGMENT */
info.num_samplers        = 0;
info.num_storage_textures = 0;
info.num_storage_buffers = 0;
info.num_uniform_buffers = 0;

SDL_GPUShader *shader = SDL_CreateGPUShader(device, &info);
```

## Graphics pipeline — correct order

```c
/* 1. Vertex buffer description (stride, input rate) */
SDL_GPUVertexBufferDescription vbuf_desc = { 0 };
vbuf_desc.slot       = 0;
vbuf_desc.pitch      = sizeof(Vertex);
vbuf_desc.input_rate = SDL_GPU_VERTEXINPUTRATE_VERTEX;

/* 2. Vertex attributes (location, format, offset) */
SDL_GPUVertexAttribute attrs[2] = { 0 };
attrs[0].location = 0;  attrs[0].format = SDL_GPU_VERTEXELEMENTFORMAT_FLOAT2;
attrs[0].offset   = offsetof(Vertex, x);
attrs[1].location = 1;  attrs[1].format = SDL_GPU_VERTEXELEMENTFORMAT_FLOAT3;
attrs[1].offset   = offsetof(Vertex, r);

/* 3. Pipeline create info */
SDL_GPUGraphicsPipelineCreateInfo pipe_info = { 0 };
pipe_info.vertex_shader   = vert_shader;
pipe_info.fragment_shader = frag_shader;
pipe_info.vertex_input_state.vertex_buffer_descriptions = &vbuf_desc;
pipe_info.vertex_input_state.num_vertex_buffers         = 1;
pipe_info.vertex_input_state.vertex_attributes          = attrs;
pipe_info.vertex_input_state.num_vertex_attributes      = 2;
pipe_info.primitive_type = SDL_GPU_PRIMITIVETYPE_TRIANGLELIST;
pipe_info.rasterizer_state.fill_mode  = SDL_GPU_FILLMODE_FILL;
pipe_info.rasterizer_state.cull_mode  = SDL_GPU_CULLMODE_NONE;
pipe_info.rasterizer_state.front_face = SDL_GPU_FRONTFACE_COUNTER_CLOCKWISE;

/* 4. Color target must match swapchain format */
SDL_GPUColorTargetDescription ct = { 0 };
ct.format = SDL_GetGPUSwapchainTextureFormat(device, window);
pipe_info.target_info.color_target_descriptions = &ct;
pipe_info.target_info.num_color_targets         = 1;

SDL_GPUGraphicsPipeline *pipeline = SDL_CreateGPUGraphicsPipeline(device, &pipe_info);

/* 5. Release shader objects — pipeline keeps its own copy */
SDL_ReleaseGPUShader(device, frag_shader);
SDL_ReleaseGPUShader(device, vert_shader);
```

## GPU buffer upload pattern

```c
/* 1. Create GPU buffer */
SDL_GPUBufferCreateInfo buf = { 0 };
buf.usage = SDL_GPU_BUFFERUSAGE_VERTEX;
buf.size  = data_size;
SDL_GPUBuffer *gpu_buf = SDL_CreateGPUBuffer(device, &buf);

/* 2. Create transfer buffer (staging) */
SDL_GPUTransferBufferCreateInfo tbuf = { 0 };
tbuf.usage = SDL_GPU_TRANSFERBUFFERUSAGE_UPLOAD;
tbuf.size  = data_size;
SDL_GPUTransferBuffer *transfer = SDL_CreateGPUTransferBuffer(device, &tbuf);

/* 3. Map, copy, unmap */
void *mapped = SDL_MapGPUTransferBuffer(device, transfer, false);
SDL_memcpy(mapped, source_data, data_size);
SDL_UnmapGPUTransferBuffer(device, transfer);

/* 4. Copy pass: transfer → GPU buffer */
SDL_GPUCommandBuffer *cmd = SDL_AcquireGPUCommandBuffer(device);
SDL_GPUCopyPass *copy = SDL_BeginGPUCopyPass(cmd);
SDL_GPUTransferBufferLocation src = { .transfer_buffer = transfer };
SDL_GPUBufferRegion dst = { .buffer = gpu_buf, .size = data_size };
SDL_UploadToGPUBuffer(copy, &src, &dst, false);
SDL_EndGPUCopyPass(copy);
SDL_SubmitGPUCommandBuffer(cmd);

/* 5. Release staging buffer */
SDL_ReleaseGPUTransferBuffer(device, transfer);
```

## Drawing — inside a render pass

```c
SDL_BindGPUGraphicsPipeline(pass, pipeline);

SDL_GPUBufferBinding binding = { .buffer = vertex_buffer };
SDL_BindGPUVertexBuffers(pass, 0, &binding, 1);

SDL_DrawGPUPrimitives(pass, vertex_count, 1, 0, 0);
```

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Vertex struct doesn't match shader inputs | Ensure `offsetof` values match attribute offsets exactly |
| Wrong `num_uniform_buffers` in shader create info | Must match the number your shader actually uses (0 if none) |
| Forgetting to release shaders after pipeline creation | Call `SDL_ReleaseGPUShader` — pipeline keeps its own copy |
| Using `malloc` instead of `SDL_calloc` | SDL functions expect SDL allocators |
| Color target format doesn't match swapchain | Use `SDL_GetGPUSwapchainTextureFormat(device, window)` |
| Forgetting `SDL_zero()` on create info structs | Uninitialized fields cause undefined behavior |
| Not releasing the transfer buffer after upload | Leaks CPU-visible memory every init |

## Cleanup order (reverse of creation)

```c
SDL_ReleaseGPUBuffer(device, vertex_buffer);
SDL_ReleaseGPUGraphicsPipeline(device, pipeline);
SDL_ReleaseWindowFromGPUDevice(device, window);
SDL_DestroyWindow(window);
SDL_DestroyGPUDevice(device);
```
