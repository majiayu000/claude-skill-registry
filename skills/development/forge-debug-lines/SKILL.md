---
name: forge-debug-lines
description: Add immediate-mode debug line drawing to an SDL GPU project. Render colored lines, grids, axes, circles, and wireframe boxes with world-space (depth-tested) and overlay (always-on-top) modes. Use when someone needs diagnostic visualization, debug drawing, or wireframe rendering in SDL3 GPU.
---

# Debug Lines — Immediate-Mode Debug Drawing

This skill adds a lightweight debug drawing system to any SDL GPU project.
It uses `SDL_GPU_PRIMITIVETYPE_LINELIST` with a dynamic vertex buffer updated
every frame via the immediate-mode pattern: reset, accumulate, upload, draw.

## When to use

- Visualizing positions, bounds, directions, or other spatial data
- Drawing coordinate-axis gizmos (RGB = XYZ)
- Rendering wireframe bounding boxes for physics or collision debugging
- Drawing circles to show radii, influence zones, or trigger areas
- Adding an always-visible overlay for diagnostic indicators
- Any per-frame debug visualization that changes based on game state

## Key API calls (ordered)

1. `SDL_CreateGPUGraphicsPipeline` — create two pipelines (depth ON / depth OFF)
   with `SDL_GPU_PRIMITIVETYPE_LINELIST` and `SDL_GPU_CULLMODE_NONE`
2. `SDL_CreateGPUBuffer` — pre-allocate GPU vertex buffer for max vertices
3. `SDL_CreateGPUTransferBuffer` — pre-allocate upload staging buffer
4. `SDL_MapGPUTransferBuffer` / `SDL_UnmapGPUTransferBuffer` — map, copy, unmap each frame
5. `SDL_UploadToGPUBuffer` — copy pass to transfer data to GPU
6. `SDL_PushGPUVertexUniformData` — push VP matrix
7. `SDL_DrawGPUPrimitives` — draw world lines, then overlay lines with first_vertex offset

## Common mistakes

- **Forgetting to reset vertex counts each frame.** The immediate-mode pattern
  requires `world_count = 0; overlay_count = 0;` at the start of every frame,
  otherwise vertices accumulate and the buffer overflows.
- **Using TRIANGLELIST primitive type.** Debug lines use `LINELIST` — every pair
  of vertices is a separate line segment. There are no faces, no indices.
- **Enabling back-face culling.** Lines have no face orientation.  Always use
  `SDL_GPU_CULLMODE_NONE` for line pipelines.
- **Creating separate GPU buffers for world and overlay.** Both can share one
  buffer — use `first_vertex` offset in the draw call to select the region.
- **Forgetting the copy pass before drawing.** The transfer buffer upload
  requires `SDL_BeginGPUCopyPass` / `SDL_UploadToGPUBuffer` /
  `SDL_EndGPUCopyPass` / `SDL_SubmitGPUCommandBuffer` before the render pass.

## Code template

### Vertex format

```c
typedef struct DebugVertex {
    vec3 position;   /* 12 bytes — world-space position */
    vec4 color;      /* 16 bytes — RGBA color           */
} DebugVertex;       /* 28 bytes total                  */

#define DEBUG_VERTEX_PITCH 28
#define MAX_DEBUG_VERTICES 65536
```

### Pipeline creation

```c
/* Vertex layout: position (float3) + color (float4) */
SDL_GPUVertexAttribute attrs[2];
SDL_zero(attrs);
attrs[0].location = 0;
attrs[0].format = SDL_GPU_VERTEXELEMENTFORMAT_FLOAT3;
attrs[0].offset = offsetof(DebugVertex, position);
attrs[1].location = 1;
attrs[1].format = SDL_GPU_VERTEXELEMENTFORMAT_FLOAT4;
attrs[1].offset = offsetof(DebugVertex, color);

SDL_GPUGraphicsPipelineCreateInfo pipe;
SDL_zero(pipe);
pipe.primitive_type = SDL_GPU_PRIMITIVETYPE_LINELIST;
pipe.rasterizer_state.cull_mode = SDL_GPU_CULLMODE_NONE;

/* World-space pipeline: depth test ON */
pipe.depth_stencil_state.enable_depth_test = true;
pipe.depth_stencil_state.enable_depth_write = true;
pipe.depth_stencil_state.compare_op = SDL_GPU_COMPAREOP_LESS_OR_EQUAL;
line_pipeline = SDL_CreateGPUGraphicsPipeline(device, &pipe);

/* Overlay pipeline: depth test OFF */
pipe.depth_stencil_state.enable_depth_test = false;
pipe.depth_stencil_state.enable_depth_write = false;
overlay_pipeline = SDL_CreateGPUGraphicsPipeline(device, &pipe);
```

### Per-frame upload and draw

```c
/* 1. Reset counts */
state->world_count = 0;
state->overlay_count = 0;

/* 2. Accumulate debug shapes */
debug_grid(state, 20, 1.0f, gray);
debug_axes(state, origin, 2.0f, true);   /* overlay */
debug_box_wireframe(state, min, max, orange, false);

/* 3. Upload (map → copy → unmap → copy pass) */
void *mapped = SDL_MapGPUTransferBuffer(device, transfer_buf, true);
SDL_memcpy(mapped, vertices, total * sizeof(DebugVertex));
SDL_UnmapGPUTransferBuffer(device, transfer_buf);
/* ... copy pass to GPU buffer ... */

/* 4. Draw */
if (world_count > 0) {
    SDL_BindGPUGraphicsPipeline(pass, line_pipeline);
    SDL_DrawGPUPrimitives(pass, world_count, 1, 0, 0);
}
if (overlay_count > 0) {
    SDL_BindGPUGraphicsPipeline(pass, overlay_pipeline);
    SDL_DrawGPUPrimitives(pass, overlay_count, 1, world_count, 0);
}
```

### Debug shape helpers

```c
/* Single line segment (2 vertices) */
static void debug_line(state, vec3 start, vec3 end, vec4 color, bool overlay);

/* Ground grid on XZ plane */
static void debug_grid(state, int half_size, float spacing, vec4 color);

/* Coordinate axes: red=X, green=Y, blue=Z (6 vertices) */
static void debug_axes(state, vec3 origin, float size, bool overlay);

/* Circle from line segments (2 × segments vertices) */
static void debug_circle(state, vec3 center, float radius, vec3 normal,
                          vec4 color, int segments, bool overlay);

/* Wireframe AABB (24 vertices = 12 edges) */
static void debug_box_wireframe(state, vec3 min_pt, vec3 max_pt,
                                 vec4 color, bool overlay);
```

### Shader (HLSL)

```hlsl
/* Vertex shader — transform position, pass through color */
cbuffer DebugUniforms : register(b0, space1)
{
    column_major float4x4 view_projection;
};

struct VSInput  { float3 position : TEXCOORD0; float4 color : TEXCOORD1; };
struct VSOutput { float4 clip_pos : SV_Position; float4 color : TEXCOORD0; };

VSOutput main(VSInput input) {
    VSOutput output;
    output.clip_pos = mul(view_projection, float4(input.position, 1.0));
    output.color = input.color;
    return output;
}

/* Fragment shader — pass-through color */
float4 main(PSInput input) : SV_Target { return input.color; }
```

## Lesson reference

See [Lesson 19 — Debug Lines](../../../lessons/gpu/19-debug-lines/) for the
full implementation with detailed comments explaining every step.
