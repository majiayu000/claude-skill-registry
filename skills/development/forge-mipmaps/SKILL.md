---
name: forge-mipmaps
description: Create mipmapped textures with auto-generated mip levels, configure sampler mipmap modes (trilinear, bilinear, none), and generate procedural textures. Use when someone needs mipmaps, trilinear filtering, LOD control, or procedural texture generation in SDL3 GPU.
---

# Mipmaps — Mip Chain Generation, Trilinear Filtering, and LOD Control

This skill teaches how to create textures with multiple mip levels, auto-generate
mipmaps with `SDL_GenerateMipmapsForGPUTexture`, and configure sampler mipmap
modes for different quality/performance trade-offs. It builds on the
`textures-and-samplers` skill (texture creation, sampler binding).

## When to use

- Creating textures that look correct at any distance (no aliasing)
- Setting up trilinear filtering for smooth mip level transitions
- Generating procedural textures without loading image files
- Controlling LOD behavior with `min_lod`, `max_lod`, and `mip_lod_bias`
- Comparing sampler mipmap modes (trilinear vs bilinear+nearest vs none)

## Key API calls (ordered)

1. `SDL_CreateGPUTexture` — create texture with `num_levels > 1` and `SAMPLER | COLOR_TARGET` usage
2. `SDL_CreateGPUTransferBuffer` — staging buffer for CPU → GPU upload
3. `SDL_MapGPUTransferBuffer` / `SDL_UnmapGPUTransferBuffer` — write pixel data
4. `SDL_BeginGPUCopyPass` / `SDL_UploadToGPUTexture` / `SDL_EndGPUCopyPass` — upload base mip level
5. `SDL_GenerateMipmapsForGPUTexture` — auto-generate all smaller mip levels (outside any pass)
6. `SDL_SubmitGPUCommandBuffer` — submit the upload + mipgen work
7. `SDL_CreateGPUSampler` — configure mipmap filtering mode (trilinear, bilinear+nearest, none)
8. `SDL_BindGPUFragmentSamplers` — bind texture + sampler for drawing

## Code template

Minimal end-to-end sequence: create a mipmapped texture, generate mips, set up a
trilinear sampler, and bind for rendering.

```c
#include "math/forge_math.h"

#define TEX_SIZE      256
#define BYTES_PER_PX  4
#define MAX_LOD       1000.0f  /* allow all mip levels */

/* ── 1. Create texture with mip levels ──────────────────────────────── */
int num_levels = (int)forge_log2f((float)TEX_SIZE) + 1;

SDL_GPUTextureCreateInfo tex_info = { 0 };
tex_info.type                 = SDL_GPU_TEXTURETYPE_2D;
tex_info.format               = SDL_GPU_TEXTUREFORMAT_R8G8B8A8_UNORM_SRGB;
tex_info.usage                = SDL_GPU_TEXTUREUSAGE_SAMPLER |
                                SDL_GPU_TEXTUREUSAGE_COLOR_TARGET;
tex_info.width                = TEX_SIZE;
tex_info.height               = TEX_SIZE;
tex_info.layer_count_or_depth = 1;
tex_info.num_levels           = num_levels;
SDL_GPUTexture *texture = SDL_CreateGPUTexture(device, &tex_info);

/* ── 2. Generate pixel data (procedural or loaded from file) ────────── */
Uint32 total_bytes = TEX_SIZE * TEX_SIZE * BYTES_PER_PX;
Uint8 *pixels = (Uint8 *)SDL_malloc(total_bytes);
/* ... fill pixels ... */

/* ── 3. Upload base level via transfer buffer ───────────────────────── */
SDL_GPUTransferBufferCreateInfo xfer_info = { 0 };
xfer_info.usage = SDL_GPU_TRANSFERBUFFERUSAGE_UPLOAD;
xfer_info.size  = total_bytes;
SDL_GPUTransferBuffer *xfer = SDL_CreateGPUTransferBuffer(device, &xfer_info);
void *mapped = SDL_MapGPUTransferBuffer(device, xfer, false);
SDL_memcpy(mapped, pixels, total_bytes);
SDL_UnmapGPUTransferBuffer(device, xfer);
SDL_free(pixels);

SDL_GPUCommandBuffer *cmd = SDL_AcquireGPUCommandBuffer(device);
SDL_GPUCopyPass *copy = SDL_BeginGPUCopyPass(cmd);

SDL_GPUTextureTransferInfo src = { 0 };
src.transfer_buffer = xfer;
src.pixels_per_row  = TEX_SIZE;
src.rows_per_layer  = TEX_SIZE;

SDL_GPUTextureRegion dst = { 0 };
dst.texture   = texture;
dst.mip_level = 0;
dst.w = TEX_SIZE;  dst.h = TEX_SIZE;  dst.d = 1;

SDL_UploadToGPUTexture(copy, &src, &dst, false);
SDL_EndGPUCopyPass(copy);

/* ── 4. Generate mipmaps — MUST be outside any pass ─────────────────── */
SDL_GenerateMipmapsForGPUTexture(cmd, texture);

SDL_SubmitGPUCommandBuffer(cmd);
SDL_ReleaseGPUTransferBuffer(device, xfer);

/* ── 5. Create trilinear sampler ────────────────────────────────────── */
SDL_GPUSamplerCreateInfo samp_info = { 0 };
samp_info.min_filter     = SDL_GPU_FILTER_LINEAR;
samp_info.mag_filter     = SDL_GPU_FILTER_LINEAR;
samp_info.mipmap_mode    = SDL_GPU_SAMPLERMIPMAPMODE_LINEAR;
samp_info.address_mode_u = SDL_GPU_SAMPLERADDRESSMODE_REPEAT;
samp_info.address_mode_v = SDL_GPU_SAMPLERADDRESSMODE_REPEAT;
samp_info.address_mode_w = SDL_GPU_SAMPLERADDRESSMODE_REPEAT;
samp_info.min_lod        = 0.0f;
samp_info.max_lod        = MAX_LOD;
SDL_GPUSampler *sampler = SDL_CreateGPUSampler(device, &samp_info);

/* ── 6. Bind for rendering (inside a render pass) ───────────────────── */
SDL_GPUTextureSamplerBinding binding = { 0 };
binding.texture = texture;
binding.sampler = sampler;
SDL_BindGPUFragmentSamplers(pass, 0, &binding, 1);
SDL_DrawGPUIndexedPrimitives(pass, index_count, 1, 0, 0, 0);
```

## Creating a mipmapped texture

### Key differences from a non-mipmapped texture

```c
SDL_GPUTextureCreateInfo tex_info = { 0 };
tex_info.type   = SDL_GPU_TEXTURETYPE_2D;
tex_info.format = SDL_GPU_TEXTUREFORMAT_R8G8B8A8_UNORM_SRGB;
tex_info.width  = 256;
tex_info.height = 256;
tex_info.layer_count_or_depth = 1;

/* ── Two critical differences from non-mipmapped textures ──────────── */

/* 1. Usage MUST include COLOR_TARGET for mipmap generation.
 *    The GPU generates mips by rendering into each level. */
tex_info.usage = SDL_GPU_TEXTUREUSAGE_SAMPLER |
                 SDL_GPU_TEXTUREUSAGE_COLOR_TARGET;

/* 2. Multiple mip levels instead of 1.
 *    log2(256) + 1 = 9 levels: 256, 128, 64, 32, 16, 8, 4, 2, 1 */
tex_info.num_levels = (int)forge_log2f((float)tex_info.width) + 1;

SDL_GPUTexture *texture = SDL_CreateGPUTexture(device, &tex_info);
```

### Mip level count formula

```c
#include "math/forge_math.h"

int num_levels = (int)forge_log2f((float)max_dimension) + 1;

/* Examples:
 *   256×256  → 9 levels
 *   512×512  → 10 levels
 *   1024×1024 → 11 levels
 *   2048×2048 → 12 levels
 */
```

For non-square textures, use the larger dimension:

```c
int max_dim = (width > height) ? width : height;
int num_levels = (int)forge_log2f((float)max_dim) + 1;
```

## Generating mipmaps

After uploading the base level (mip 0), call `SDL_GenerateMipmapsForGPUTexture`
**outside any render or copy pass**:

```c
SDL_GPUCommandBuffer *cmd = SDL_AcquireGPUCommandBuffer(device);

/* Upload base level in a copy pass */
SDL_GPUCopyPass *copy = SDL_BeginGPUCopyPass(cmd);
SDL_UploadToGPUTexture(copy, &src, &dst, false);
SDL_EndGPUCopyPass(copy);

/* Generate all other mip levels — MUST be outside any pass */
SDL_GenerateMipmapsForGPUTexture(cmd, texture);

SDL_SubmitGPUCommandBuffer(cmd);
```

The GPU internally renders into each mip level, downsampling from the level
above using a blit operation.

## Sampler mipmap modes

### Trilinear (highest quality)

Blends between two adjacent mip levels for smooth transitions:

```c
SDL_GPUSamplerCreateInfo info = { 0 };
info.min_filter     = SDL_GPU_FILTER_LINEAR;
info.mag_filter     = SDL_GPU_FILTER_LINEAR;
info.mipmap_mode    = SDL_GPU_SAMPLERMIPMAPMODE_LINEAR;  /* blend between mips */
info.address_mode_u = SDL_GPU_SAMPLERADDRESSMODE_REPEAT;
info.address_mode_v = SDL_GPU_SAMPLERADDRESSMODE_REPEAT;
info.address_mode_w = SDL_GPU_SAMPLERADDRESSMODE_REPEAT;
info.min_lod        = 0.0f;
info.max_lod        = 1000.0f;   /* allow all mip levels */
```

### Bilinear + nearest mip (medium quality)

Smooth within a level, but "pops" when switching between levels:

```c
info.mipmap_mode = SDL_GPU_SAMPLERMIPMAPMODE_NEAREST;  /* snap to closest mip */
```

### No mipmaps (force base level)

Causes aliasing at distance — useful for comparison or when you only have
one mip level:

```c
info.min_filter  = SDL_GPU_FILTER_NEAREST;
info.mag_filter  = SDL_GPU_FILTER_NEAREST;
info.mipmap_mode = SDL_GPU_SAMPLERMIPMAPMODE_NEAREST;
info.max_lod     = 0.0f;   /* clamp to level 0 only */
```

## LOD control

| Sampler field | Purpose | Default |
|---------------|---------|---------|
| `min_lod` | Minimum mip level (0 = base) | 0.0 |
| `max_lod` | Maximum mip level | 1000.0 (all) |
| `mip_lod_bias` | Added to computed LOD (positive = blurrier) | 0.0 |

```c
/* Example: restrict to first 3 mip levels */
info.min_lod = 0.0f;
info.max_lod = 2.0f;   /* levels 0, 1, 2 only */

/* Example: bias toward blurrier mips (reduces shimmering) */
info.mip_lod_bias = 0.5f;
```

## Procedural texture generation

Generate textures in code instead of loading from files:

```c
int size = 256;
int tiles = 16;
int tile_size = size / tiles;
Uint8 *pixels = SDL_malloc(size * size * 4);

for (int y = 0; y < size; y++) {
    for (int x = 0; x < size; x++) {
        int tile_x = x / tile_size;
        int tile_y = y / tile_size;
        Uint8 color = ((tile_x + tile_y) % 2 == 0) ? 255 : 0;

        int idx = (y * size + x) * 4;
        pixels[idx + 0] = color;  /* R */
        pixels[idx + 1] = color;  /* G */
        pixels[idx + 2] = color;  /* B */
        pixels[idx + 3] = 255;    /* A */
    }
}

/* Upload pixels via transfer buffer, then SDL_GenerateMipmapsForGPUTexture */
```

No file I/O, no CMake copy steps, no pixel format conversion.

## UV tiling

To make a texture repeat, multiply UVs by a scale factor in the vertex shader:

```hlsl
cbuffer Uniforms : register(b0, space1)
{
    float time;
    float aspect;
    float uv_scale;
    float _pad;        /* pad to 16-byte alignment */
};

output.uv = input.uv * uv_scale;
```

With `REPEAT` address mode, UVs beyond 0–1 wrap around automatically.

## Uniform struct alignment

When adding fields to the uniform buffer, pad to 16-byte alignment:

```c
typedef struct Uniforms {
    float time;       /* 4 bytes */
    float aspect;     /* 4 bytes */
    float uv_scale;   /* 4 bytes */
    float _pad;       /* 4 bytes — pad to 16-byte boundary */
} Uniforms;
```

GPU uniform buffers require 16-byte aligned members. Missing padding causes
subtle data corruption.

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Missing `COLOR_TARGET` usage | `SDL_GenerateMipmapsForGPUTexture` requires `SAMPLER \| COLOR_TARGET` |
| `num_levels = 1` with mipmap sampler | Set `num_levels = (int)forge_log2f(size) + 1` |
| Calling `SDL_GenerateMipmapsForGPUTexture` inside a pass | Must be called outside any render or copy pass |
| `max_lod = 0` with trilinear sampler | GPU can only use level 0 — set `max_lod = 1000.0f` for all levels |
| Uniform buffer not 16-byte aligned | Add `float _pad` fields to fill to 16 bytes |
| Forgetting to upload base level before generating mips | Upload mip 0 first, then call generate |

## Cleanup

Release samplers in reverse order of creation:

```c
for (int i = 0; i < NUM_SAMPLERS; i++)
    SDL_ReleaseGPUSampler(device, samplers[i]);
SDL_ReleaseGPUTexture(device, texture);
```

## Reference

- [GPU Lesson 05 — Mipmaps](../../../lessons/gpu/05-mipmaps/) — full implementation
- [Math Lesson 04 — Mipmaps & LOD](../../../lessons/math/04-mipmaps-and-lod/) — theory
- [textures-and-samplers skill](../forge-textures-and-samplers/SKILL.md) — prerequisite
- `forge_log2f()` in `common/math/forge_math.h` — mip level count
