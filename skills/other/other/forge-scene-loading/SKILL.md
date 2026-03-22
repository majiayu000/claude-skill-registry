---
name: forge-scene-loading
description: Load and render a glTF 2.0 scene with multi-material meshes, scene hierarchy, indexed drawing, and cJSON parsing. Use when someone needs to load complex 3D scenes, parse glTF files, render multi-material models, or set up indexed rendering in SDL3 GPU.
---

# Scene Loading — glTF Parsing, Multi-Material, Indexed Rendering

This skill teaches how to load and render glTF 2.0 scenes with multiple meshes,
materials, and a node hierarchy. It builds on `mesh-loading` (Lesson 08) and
adds scene graphs, indexed drawing, and multi-material support.

## When to use

- Loading 3D scenes from glTF files
- Rendering multi-material meshes (textured + solid color in one draw)
- Parsing JSON scene descriptions with cJSON
- Setting up indexed rendering with `SDL_DrawGPUIndexedPrimitives`
- Building and traversing a scene hierarchy (parent-child transforms)
- Working with quaternion-based transforms in glTF

## Key API calls (ordered)

1. `forge_gltf_load(path, &scene)` — parse glTF JSON + binary into CPU data
2. `SDL_CreateGPUBuffer` + transfer upload — upload vertex + index buffers
3. `SDL_LoadSurface` + `SDL_ConvertSurface` — load texture images
4. `SDL_CreateGPUTexture` with `SAMPLER | COLOR_TARGET` — mipmapped textures
5. `SDL_GenerateMipmapsForGPUTexture` — auto-generate mip chain
6. `SDL_CreateGPUSampler` — trilinear, REPEAT address mode
7. `SDL_CreateGPUGraphicsPipeline` — 3 vertex attributes, depth test, back-face cull
8. `SDL_PushGPUVertexUniformData` — push per-primitive MVP matrix
9. `SDL_PushGPUFragmentUniformData` — push base_color + has_texture flag
10. `SDL_BindGPUFragmentSamplers` — bind material texture + sampler
11. `SDL_BindGPUIndexBuffer` — bind primitive index buffer
12. `SDL_DrawGPUIndexedPrimitives` — indexed draw per primitive

## Libraries

```c
#include "gltf/forge_gltf.h"    /* glTF parser (depends on cJSON) */
#include "math/forge_math.h"    /* vectors, matrices, quaternions */
#include "cJSON.h"              /* JSON parser (third_party/cJSON/) */
```

## Code template

### Loading the scene

```c
/* Build path relative to executable */
const char *base_path = SDL_GetBasePath();
char gltf_path[512];
SDL_snprintf(gltf_path, sizeof(gltf_path), "%sassets/model.gltf", base_path);

ForgeGltfScene scene;
if (!forge_gltf_load(gltf_path, &scene)) {
    SDL_Log("Failed to load scene");
    return SDL_APP_FAILURE;
}

/* scene.nodes[], scene.meshes[], scene.primitives[], scene.materials[] */
/* scene.root_nodes[] lists the scene's root node indices */
```

### Uploading to GPU

```c
/* For each primitive: upload vertex + index buffers */
for (int i = 0; i < scene.primitive_count; i++) {
    ForgeGltfPrimitive *prim = &scene.primitives[i];

    Uint32 vb_size = prim->vertex_count * (Uint32)sizeof(ForgeGltfVertex);
    gpu_prims[i].vertex_buffer = upload_gpu_buffer(
        device, SDL_GPU_BUFFERUSAGE_VERTEX, prim->vertices, vb_size);

    Uint32 ib_size = prim->index_count * prim->index_stride;
    gpu_prims[i].index_buffer = upload_gpu_buffer(
        device, SDL_GPU_BUFFERUSAGE_INDEX, prim->indices, ib_size);

    gpu_prims[i].index_type = (prim->index_stride == 2)
        ? SDL_GPU_INDEXELEMENTSIZE_16BIT
        : SDL_GPU_INDEXELEMENTSIZE_32BIT;
}

/* For each material: load texture from path */
for (int i = 0; i < scene.material_count; i++) {
    if (scene.materials[i].has_texture) {
        gpu_mats[i].texture = load_texture(device, scene.materials[i].texture_path);
    }
}
```

### Fragment shader (multi-material)

```hlsl
cbuffer FragUniforms : register(b0, space3) {
    float4 base_color;
    uint   has_texture;
    uint3  _pad;
};

Texture2D    diffuse_tex : register(t0, space2);
SamplerState smp         : register(s0, space2);

float4 main(PSInput input) : SV_Target {
    if (has_texture)
        return diffuse_tex.Sample(smp, input.uv) * base_color;
    else
        return base_color;
}
```

### Rendering the scene

```c
/* Iterate all nodes with meshes */
for (int ni = 0; ni < scene.node_count; ni++) {
    ForgeGltfNode *node = &scene.nodes[ni];
    if (node->mesh_index < 0) continue;

    /* MVP = projection * view * node.world_transform */
    mat4 mvp = mat4_multiply(vp, node->world_transform);
    SDL_PushGPUVertexUniformData(cmd, 0, &mvp, sizeof(mvp));

    ForgeGltfMesh *mesh = &scene.meshes[node->mesh_index];
    for (int pi = 0; pi < mesh->primitive_count; pi++) {
        int idx = mesh->first_primitive + pi;
        GpuPrimitive *prim = &gpu_prims[idx];

        /* Push material uniforms */
        FragUniforms fu;
        fu.base_color = gpu_mats[prim->material_index].base_color;
        fu.has_texture = gpu_mats[prim->material_index].has_texture;
        SDL_PushGPUFragmentUniformData(cmd, 0, &fu, sizeof(fu));

        /* Bind texture + sampler */
        SDL_GPUTextureSamplerBinding tex_bind = { .texture = tex, .sampler = sampler };
        SDL_BindGPUFragmentSamplers(pass, 0, &tex_bind, 1);

        /* Bind vertex + index buffers and draw */
        SDL_GPUBufferBinding vb = { .buffer = prim->vertex_buffer };
        SDL_BindGPUVertexBuffers(pass, 0, &vb, 1);

        SDL_GPUBufferBinding ib = { .buffer = prim->index_buffer };
        SDL_BindGPUIndexBuffer(pass, &ib, prim->index_type);

        SDL_DrawGPUIndexedPrimitives(pass, prim->index_count, 1, 0, 0, 0);
    }
}
```

### CMakeLists.txt pattern

```cmake
add_executable(my-app WIN32
    main.c
    ${CMAKE_SOURCE_DIR}/third_party/cJSON/cJSON.c)
target_include_directories(my-app PRIVATE
    ${FORGE_COMMON_DIR}
    ${CMAKE_SOURCE_DIR}/third_party/cJSON)
target_link_libraries(my-app PRIVATE SDL3::SDL3
    $<$<NOT:$<C_COMPILER_ID:MSVC>>:m>)

# Copy glTF assets next to executable
add_custom_command(TARGET my-app POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_directory
        ${CMAKE_CURRENT_SOURCE_DIR}/assets/ModelName
        $<TARGET_FILE_DIR:my-app>/assets/ModelName
)
```

## Important rule

**Never extract individual assets from a glTF model à la carte.** Always copy
the complete model (`.gltf`, `.bin`, and all referenced textures) into the
lesson's `assets/` directory and load it with `forge_gltf_load()`. The model's
node transforms, materials, and textures should drive the scene — do not
cherry-pick textures or meshes and build a hand-coded scene around them.

## Common mistakes

1. **glTF quaternion order** — glTF stores quaternions as `[x, y, z, w]`, but
   `forge_math.h` uses `quat_create(w, x, y, z)`. The parser handles this
   conversion, but watch out if parsing manually.

2. **Shared textures** — Multiple materials can reference the same image.
   Track loaded textures to avoid loading the same file twice and to prevent
   double-free when releasing GPU resources.

3. **1x1 white placeholder texture** — Always bind a valid texture to the
   fragment sampler, even for materials without textures. Create a 1x1 white
   texture at init and bind it as the default.

4. **Index element size** — glTF uses both uint16 (componentType 5123) and
   uint32 (componentType 5125) indices. Match the `SDL_GPUIndexElementSize`
   to the primitive's index stride.

5. **Missing `COLOR_TARGET` usage** — Required for mipmap generation.
   Without it, `SDL_GenerateMipmapsForGPUTexture` silently fails.

6. **Not copying assets in CMake** — The .gltf, .bin, and texture files must
   be next to the executable. Use `copy_directory` in a post-build step.

7. **Transform accumulation order** — World transform is
   `parent_world * local_transform`, not the other way around. Local transform
   is `T * R * S` (translation first in multiplication order).

## References

- [GPU Lesson 09 — Loading a Scene](../../../lessons/gpu/09-scene-loading/)
- [GPU Lesson 08 — Loading a Mesh](../../../lessons/gpu/08-mesh-loading/)
- [Math Lesson 08 — Orientation](../../../lessons/math/08-orientation/) (quaternions)
- [Math Lesson 09 — View Matrix](../../../lessons/math/09-view-matrix/)
- [glTF Parser Library](../../../common/gltf/forge_gltf.h)
- [glTF 2.0 Specification](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html)
