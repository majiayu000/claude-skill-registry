---
name: forge-pipeline-texture-compression
description: Load GPU block-compressed textures (BC7/BC5) through the asset pipeline. Covers basisu encoding, UASTC transcoding, .ftex format, D3D12 alignment, and normal map channel handling.
trigger: Use when someone needs compressed textures, BC7/BC5 loading, VRAM optimization, or asks about .ftex files or texture compression.
---

# forge-pipeline-texture-compression

Load GPU block-compressed textures through `forge_scene.h`. The asset
pipeline compresses textures at build time (basisu → KTX2 → .ftex), and
`forge_scene_load_pipeline_texture()` uploads the pre-transcoded blocks
directly to the GPU — no runtime transcoding or mip generation.

## Compression pipeline

```bash
# Build basisu (once)
cmake --build build --target basisu

# Color textures → BC7 sRGB
basisu -uastc -ktx2 -mipmap -file basecolor.jpg
forge_texture_tool basecolor.ktx2 basecolor.ftex bc7_srgb

# Normal maps → BC5 (requires both flags)
basisu -uastc -ktx2 -mipmap -normal_map -separate_rg_to_color_alpha -file normal.jpg
forge_texture_tool normal.ktx2 normal.ftex bc5_unorm

# Linear textures (metallic-roughness, occlusion) → BC7 linear
basisu -uastc -ktx2 -mipmap -file metallic_roughness.jpg
forge_texture_tool metallic_roughness.ktx2 metallic_roughness.ftex bc7_unorm
```

Both tools are CPU-only — no GPU required. Works on headless servers.

## Format selection

| Texture type | basisu flags | .ftex format | SDL GPU format |
|---|---|---|---|
| Base color | (none) | `bc7_srgb` | `BC7_RGBA_UNORM_SRGB` |
| Emissive | (none) | `bc7_srgb` | `BC7_RGBA_UNORM_SRGB` |
| Normal map | `-normal_map -separate_rg_to_color_alpha` | `bc5_unorm` | `BC5_RG_UNORM` |
| Metallic-roughness | (none) | `bc7_unorm` | `BC7_RGBA_UNORM` |
| Occlusion | (none) | `bc7_unorm` | `BC7_RGBA_UNORM` |

## Normal map encoding — why both flags matter

**`-separate_rg_to_color_alpha`**: The Basis Universal BC5 transcoder reads
channels 0 (R) and 3 (Alpha), not 0 (R) and 1 (G). This flag moves G into
alpha during UASTC encoding so BC5 gets the correct data. Without it, the
Y normal component is lost (all 255).

**`-normal_map`**: Treats input as linear data (not sRGB) and optimizes
UASTC encoding for angular error rather than perceptual color error.

## Sidecar detection

`forge_scene_load_pipeline_texture()` checks for a `.meta.json` sidecar
next to each texture. If the sidecar has a `compression` block pointing to
a `.ftex` file, the compressed path is used. Otherwise, it falls back to
`SDL_LoadSurface` + GPU mipmaps.

Example `.meta.json`:

```json
{
  "source": "basecolor.jpg",
  "output": "basecolor.jpg",
  "output_width": 2048,
  "output_height": 2048,
  "compression": {
    "codec": "uastc",
    "container": "ktx2",
    "compressed_file": "basecolor.ktx2",
    "ratio": 6.32,
    "normal_map": true
  }
}
```

## D3D12 alignment requirement

D3D12 requires 256-byte row pitch alignment and 512-byte mip offset
alignment for texture uploads. `forge_scene_upload_compressed_texture()`
handles this by padding block rows and aligning offsets in the transfer
buffer. Vulkan has no such requirement.

Small BC7/BC5 mips (≤32×32) have row pitches below 256 bytes. Without
padding, SDL's D3D12 backend crashes non-deterministically.

## Usage pattern

```c
#define FORGE_PIPELINE_IMPLEMENTATION
#include "pipeline/forge_pipeline.h"

#define FORGE_SCENE_MODEL_SUPPORT
#define FORGE_SCENE_IMPLEMENTATION
#include "scene/forge_scene.h"

/* Load model — compressed textures are detected automatically */
ForgeSceneModel model;
forge_scene_load_model(&scene, &model,
                       "assets/Model/Model.fscene",
                       "assets/Model/Model.fmesh",
                       "assets/Model/Model.fmat",
                       "assets/Model");

/* Check compression stats */
SDL_Log("Textures: %u/%u compressed, VRAM: %.1f MB (%.1f MB uncompressed)",
        model.vram.compressed_texture_count, model.vram.total_texture_count,
        (float)model.vram.compressed_bytes / (1024.0f * 1024.0f),
        (float)model.vram.uncompressed_bytes / (1024.0f * 1024.0f));
```

## .ftex binary format

```text
Header (32 bytes):
  magic       u32    "FTEX" (0x58455446)
  version     u32    1
  format      u32    1=BC7_SRGB, 2=BC7_UNORM, 3=BC5_UNORM
  width       u32    base mip width
  height      u32    base mip height
  mip_count   u32    number of mip levels
  reserved    u32    0
  reserved    u32    0

Mip entries (16 bytes each × mip_count):
  offset      u32    byte offset from file start
  data_size   u32    compressed block data size
  width       u32    mip level width
  height      u32    mip level height

Block data:
  Contiguous compressed blocks, mip 0 first
```

## Shader compatibility

The fragment shader reconstructs Z from RG for normal maps:

```hlsl
float2 n_rg = normal_tex.Sample(normal_smp, uv).rg * 2.0 - 1.0;
float3 n = float3(n_rg, sqrt(saturate(1.0 - dot(n_rg, n_rg))));
```

This works for both BC5 (RG only) and RGBA8 (ignores B, recomputes Z).

## Common mistakes

- **Missing `-separate_rg_to_color_alpha` for normal maps.** BC5 transcoding
  reads R and Alpha channels, not R and G. Without this flag, the Y normal
  component is all 1.0 and lighting is completely wrong.
- **Missing `-normal_map` for normal maps.** Without it, basisu treats the
  input as sRGB and optimizes for perceptual color error instead of angular
  error. Quality degrades.
- **Unaligned compressed texture uploads on D3D12.** Small mips (≤32×32) have
  row pitches below 256 bytes. Pad block rows to 256-byte alignment and align
  mip offsets to 512 bytes, or SDL's D3D12 backend crashes.
- **Forgetting `pixels_per_row` after padding.** If you pad the transfer
  buffer but don't set `pixels_per_row` on `SDL_GPUTextureTransferInfo`, SDL
  doesn't know the stride and reads garbage.
- **Using BC7 sRGB for linear data.** Metallic-roughness and occlusion
  textures are linear — use `bc7_unorm`, not `bc7_srgb`.

## Reference

- [GPU Lesson 42](../../../lessons/gpu/42-pipeline-texture-compression/) —
  full lesson with debugging walkthrough
- [GPU Lesson 41](../../../lessons/gpu/41-scene-model-loading/) —
  model loading foundation
- `common/scene/forge_scene.h` — `forge_scene_upload_compressed_texture()`
- `common/pipeline/forge_pipeline.h` — `forge_pipeline_load_ftex()`
- `tools/texture/main.c` — `forge_texture_tool` (KTX2 → .ftex)
