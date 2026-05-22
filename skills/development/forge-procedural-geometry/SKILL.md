---
name: forge-procedural-geometry
description: Generate procedural 3D geometry using forge_shapes.h — parametric surfaces (sphere, icosphere, cylinder, cone, torus, plane, cube, capsule) with struct-of-arrays layout for GPU upload
---

Generate and render procedural geometry using the `forge_shapes.h` header-only
library. Shapes are unit-scale, centred at origin, Y-up, CCW winding.

## Include pattern

One `.c` file defines the implementation; all others get declarations only:

```c
/* In exactly ONE .c file: */
#define FORGE_SHAPES_IMPLEMENTATION
#include "shapes/forge_shapes.h"

/* In all other files: */
#include "shapes/forge_shapes.h"
```

## Generate and upload a shape

```c
/* Generate a 32-slice, 16-stack UV sphere */
ForgeShape sphere = forge_shapes_sphere(32, 16);

/* Create GPU buffers for struct-of-arrays layout */
SDL_GPUBuffer *pos_buf = upload_gpu_buffer(device,
    sphere.positions, sphere.vertex_count * sizeof(vec3));
SDL_GPUBuffer *nor_buf = upload_gpu_buffer(device,
    sphere.normals,   sphere.vertex_count * sizeof(vec3));
SDL_GPUBuffer *idx_buf = upload_gpu_buffer_index(device,
    sphere.indices,   sphere.index_count * sizeof(uint32_t));

/* Free CPU-side data after upload */
int index_count = sphere.index_count;
forge_shapes_free(&sphere);
```

## Bind and draw (struct-of-arrays)

```c
/* Bind position buffer at vertex slot 0 */
SDL_GPUBufferBinding pos_bind = { .buffer = pos_buf, .offset = 0 };
SDL_BindGPUVertexBuffers(rpass, 0, &pos_bind, 1);

/* Bind normal buffer at vertex slot 1 */
SDL_GPUBufferBinding nor_bind = { .buffer = nor_buf, .offset = 0 };
SDL_BindGPUVertexBuffers(rpass, 1, &nor_bind, 1);

/* Bind index buffer */
SDL_GPUBufferBinding idx_bind = { .buffer = idx_buf, .offset = 0 };
SDL_BindGPUIndexBuffer(rpass, &idx_bind, SDL_GPU_INDEXELEMENTSIZE_32BIT);

/* Draw */
SDL_DrawGPUIndexedPrimitives(rpass, index_count, 1, 0, 0, 0);
```

## Pipeline vertex attributes

Configure two vertex buffer slots matching the struct-of-arrays layout:

```c
SDL_GPUVertexBufferDescription vbufs[] = {
    { .slot = 0, .pitch = sizeof(vec3), .input_rate = SDL_GPU_VERTEXINPUTRATE_VERTEX },
    { .slot = 1, .pitch = sizeof(vec3), .input_rate = SDL_GPU_VERTEXINPUTRATE_VERTEX },
};
SDL_GPUVertexAttribute attrs[] = {
    { .location = 0, .buffer_slot = 0, .format = SDL_GPU_VERTEXELEMENTFORMAT_FLOAT3, .offset = 0 },
    { .location = 1, .buffer_slot = 1, .format = SDL_GPU_VERTEXELEMENTFORMAT_FLOAT3, .offset = 0 },
};
```

## Multiple shapes in one scene

```c
/* Generate all shapes */
ForgeShape shapes[] = {
    forge_shapes_sphere(32, 16),
    forge_shapes_torus(24, 12, 1.0f, 0.4f),
    forge_shapes_plane(4, 4),
};
int shape_count = sizeof(shapes) / sizeof(shapes[0]);

/* Upload each to GPU, store buffers and counts */
for (int i = 0; i < shape_count; i++) {
    upload_shape_to_gpu(device, &shapes[i], &gpu_shapes[i]);
    forge_shapes_free(&shapes[i]);
}

/* In render loop: draw each with its own model matrix */
for (int i = 0; i < shape_count; i++) {
    set_push_uniforms(rpass, model_matrices[i]);
    bind_and_draw(rpass, &gpu_shapes[i]);
}
```

## Available generators

| Function | Description | Default params |
|---|---|---|
| `forge_shapes_sphere(slices, stacks)` | UV sphere, radius 1 | 32, 16 |
| `forge_shapes_icosphere(subdivisions)` | Even triangle distribution | 2 |
| `forge_shapes_cylinder(slices, stacks)` | No caps, height 2 | 32, 1 |
| `forge_shapes_cone(slices, stacks)` | Apex at Y=+1, no base | 32, 1 |
| `forge_shapes_torus(slices, stacks, major, tube)` | Donut in XZ plane | 32, 16, 1.0, 0.4 |
| `forge_shapes_plane(slices, stacks)` | XZ plane, Y=0 | 4, 4 |
| `forge_shapes_cube(slices, stacks)` | 6 faces, per-face normals | 1, 1 |
| `forge_shapes_capsule(slices, stacks, cap_stacks, half_h)` | Cylinder + hemisphere caps | 32, 4, 4, 1.0 |

## Common mistakes

1. **Forgetting to free** — always call `forge_shapes_free()` after GPU upload
2. **Wrong vertex slot** — positions go to slot 0, normals to slot 1; swapping
   them produces garbled lighting
3. **Using interleaved vertex layout** — `ForgeShape` uses struct-of-arrays;
   bind separate buffers per attribute, not one interleaved buffer
4. **Missing seam at U=0/U=1** — the sphere has `(slices+1)` columns to handle
   the texture seam; this is intentional, not a bug

## References

- Library: [`common/shapes/forge_shapes.h`](../../../common/shapes/forge_shapes.h)
- API docs: [`common/shapes/README.md`](../../../common/shapes/README.md)
- Lesson: [`lessons/assets/04-procedural-geometry/`](../../../lessons/assets/04-procedural-geometry/)
- Tests: [`tests/shapes/test_shapes.c`](../../../tests/shapes/test_shapes.c)
