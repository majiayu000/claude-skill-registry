---
name: forge-mesh-loading
description: Load a 3D model from an OBJ file, create a textured mesh with mipmaps, and render with a fly-around camera. Use when someone needs to load geometry from a file, parse OBJ models, or render textured 3D meshes in SDL3 GPU.
---

# Mesh Loading — OBJ Parsing, Textured Rendering, Camera

This skill teaches how to load and render 3D models from Wavefront OBJ files.
It builds on `textures-and-samplers` (Lesson 04), `mipmaps` (Lesson 05),
`depth-and-3d` (Lesson 06), and `camera-and-input` (Lesson 07).

## When to use

- Loading 3D models from OBJ files
- Rendering textured meshes with a camera
- Parsing vertex positions, normals, and UV coordinates from files
- Setting up non-indexed rendering (de-indexed vertices)
- Combining texture loading + mipmaps + depth testing + camera in one app

## Key API calls (ordered)

1. `forge_obj_load(path, &mesh)` — parse OBJ into de-indexed vertex array
2. `SDL_CreateGPUBuffer` + transfer upload — upload vertices to GPU
3. `SDL_LoadSurface` + `SDL_ConvertSurface` — load PNG texture
4. `SDL_CreateGPUTexture` with `SAMPLER | COLOR_TARGET` — mipmapped texture
5. `SDL_GenerateMipmapsForGPUTexture` — auto-generate mip chain
6. `SDL_CreateGPUSampler` — trilinear, REPEAT address mode
7. `SDL_CreateGPUGraphicsPipeline` — 3 vertex attributes, depth test, back-face cull
8. `SDL_BindGPUFragmentSamplers` — bind diffuse texture + sampler
9. `SDL_DrawGPUPrimitives` — non-indexed draw (de-indexed vertices)

## Libraries

```c
#include "obj/forge_obj.h"     /* OBJ parser */
#include "math/forge_math.h"   /* vectors, matrices, quaternions */
```

## Code template

### Loading the mesh

```c
/* Build path relative to executable */
const char *base_path = SDL_GetBasePath();
char obj_path[512];
SDL_snprintf(obj_path, sizeof(obj_path), "%smodels/model.obj", base_path);

ForgeObjMesh mesh;
if (!forge_obj_load(obj_path, &mesh)) {
    SDL_Log("Failed to load model");
    return SDL_APP_FAILURE;
}

/* Upload to GPU vertex buffer via transfer buffer */
Uint32 vertex_data_size = mesh.vertex_count * (Uint32)sizeof(ForgeObjVertex);
/* ... standard transfer buffer pattern from Lesson 02 ... */

Uint32 mesh_vertex_count = mesh.vertex_count;
forge_obj_free(&mesh);  /* CPU-side data no longer needed */
```

### Loading texture with mipmaps

```c
SDL_Surface *surface = SDL_LoadSurface(tex_path);
SDL_Surface *converted = SDL_ConvertSurface(surface, SDL_PIXELFORMAT_ABGR8888);
SDL_DestroySurface(surface);

int num_levels = (int)forge_log2f((float)converted->w) + 1;

SDL_GPUTextureCreateInfo tex_info;
SDL_zero(tex_info);
tex_info.type     = SDL_GPU_TEXTURETYPE_2D;
tex_info.format   = SDL_GPU_TEXTUREFORMAT_R8G8B8A8_UNORM_SRGB;
tex_info.usage    = SDL_GPU_TEXTUREUSAGE_SAMPLER | SDL_GPU_TEXTUREUSAGE_COLOR_TARGET;
tex_info.width    = converted->w;
tex_info.height   = converted->h;
tex_info.num_levels = num_levels;
/* ... upload base level, then: */
SDL_GenerateMipmapsForGPUTexture(cmd, texture);
```

### Vertex layout (3 attributes)

```c
/* ForgeObjVertex: position (float3) + normal (float3) + uv (float2) */

vertex_attributes[0].location = 0;  /* TEXCOORD0 = position */
vertex_attributes[0].format   = SDL_GPU_VERTEXELEMENTFORMAT_FLOAT3;
vertex_attributes[0].offset   = offsetof(ForgeObjVertex, position);

vertex_attributes[1].location = 1;  /* TEXCOORD1 = normal */
vertex_attributes[1].format   = SDL_GPU_VERTEXELEMENTFORMAT_FLOAT3;
vertex_attributes[1].offset   = offsetof(ForgeObjVertex, normal);

vertex_attributes[2].location = 2;  /* TEXCOORD2 = uv */
vertex_attributes[2].format   = SDL_GPU_VERTEXELEMENTFORMAT_FLOAT2;
vertex_attributes[2].offset   = offsetof(ForgeObjVertex, uv);
```

### Rendering (non-indexed)

```c
SDL_BindGPUVertexBuffers(pass, 0, &vertex_binding, 1);

SDL_GPUTextureSamplerBinding tex_binding;
SDL_zero(tex_binding);
tex_binding.texture = diffuse_texture;
tex_binding.sampler = sampler;
SDL_BindGPUFragmentSamplers(pass, 0, &tex_binding, 1);

/* Non-indexed draw — de-indexed vertices, every 3 form a triangle */
SDL_DrawGPUPrimitives(pass, mesh_vertex_count, 1, 0, 0);
```

### HLSL shaders

**Vertex shader:**

```hlsl
cbuffer Uniforms : register(b0, space1) { column_major float4x4 mvp; };

struct VSInput {
    float3 position : TEXCOORD0;
    float3 normal   : TEXCOORD1;
    float2 uv       : TEXCOORD2;
};

struct VSOutput {
    float4 position : SV_Position;
    float2 uv       : TEXCOORD0;
};

VSOutput main(VSInput input) {
    VSOutput output;
    output.position = mul(mvp, float4(input.position, 1.0));
    output.uv = input.uv;
    return output;
}
```

**Fragment shader:**

```hlsl
Texture2D    diffuse_tex : register(t0, space2);
SamplerState smp         : register(s0, space2);

float4 main(float4 pos : SV_Position, float2 uv : TEXCOORD0) : SV_Target {
    return diffuse_tex.Sample(smp, uv);
}
```

## Common mistakes

1. **Forgetting UV flip** — OBJ uses V=0 at bottom; GPU uses V=0 at top.
   The `forge_obj.h` parser handles this automatically (`1.0 - v`).

2. **Using indexed draw for de-indexed mesh** — Use `SDL_DrawGPUPrimitives`,
   not `SDL_DrawGPUIndexedPrimitives`, since vertices are already expanded.

3. **Wrong pixel format** — `SDL_LoadSurface` may return any format.
   Always convert to `SDL_PIXELFORMAT_ABGR8888` for GPU `R8G8B8A8`.

4. **Missing `COLOR_TARGET` usage** — Required for mipmap generation.
   Without it, `SDL_GenerateMipmapsForGPUTexture` silently fails.

5. **Not copying model files in CMake** — The OBJ and texture must be next
   to the executable. Use `add_custom_command(POST_BUILD ...)` to copy them.

6. **Loading JPG** — `SDL_LoadSurface` only supports BMP and PNG.
   Convert JPG textures to PNG first (e.g. with Python Pillow).

## CMakeLists.txt pattern

```cmake
# Copy model files next to executable
add_custom_command(TARGET my-target POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E make_directory
        $<TARGET_FILE_DIR:my-target>/models/model-name
    COMMAND ${CMAKE_COMMAND} -E copy_if_different
        ${CMAKE_CURRENT_SOURCE_DIR}/models/model-name/model.obj
        $<TARGET_FILE_DIR:my-target>/models/model-name/model.obj
    COMMAND ${CMAKE_COMMAND} -E copy_if_different
        ${CMAKE_CURRENT_SOURCE_DIR}/models/model-name/texture.png
        $<TARGET_FILE_DIR:my-target>/models/model-name/texture.png
)
```

## References

- [GPU Lesson 08 — Loading a Mesh](../../../lessons/gpu/08-mesh-loading/)
- [GPU Lesson 04 — Textures & Samplers](../../../lessons/gpu/04-textures-and-samplers/)
- [GPU Lesson 05 — Mipmaps](../../../lessons/gpu/05-mipmaps/)
- [GPU Lesson 07 — Camera & Input](../../../lessons/gpu/07-camera-and-input/)
- [OBJ Parser Library](../../../common/obj/forge_obj.h)
