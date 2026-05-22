---
name: forge-ui-rendering
description: Render the forge-gpu immediate-mode UI system on the GPU with a single draw call, font atlas texture, alpha blending, and dynamic buffer streaming. Based on Lesson 28.
---

Render the CPU-side immediate-mode UI (forge_ui_ctx.h, forge_ui_window.h) using
the SDL GPU API. Based on GPU Lesson 28.

## When to use

- You have a ForgeUiContext producing vertex/index arrays and need to draw them
- You need to render text glyphs from a font atlas with alpha blending
- You need a single-draw-call 2D UI pipeline with dynamic buffer streaming
- You want to integrate the UI track output into a GPU application

## Key API calls

- `SDL_CreateGPUTexture` with `SDL_GPU_TEXTUREFORMAT_R8_UNORM` — single-channel atlas
- `SDL_CreateGPUSampler` — linear filter, clamp-to-edge for atlas
- `SDL_CreateGPUGraphicsPipeline` — alpha blend, no depth, cull none
- `SDL_CreateGPUTransferBuffer` / `SDL_MapGPUTransferBuffer` — per-frame upload
- `SDL_UploadToGPUBuffer` — copy vertex + index data via copy pass
- `SDL_PushGPUVertexUniformData` — orthographic projection matrix
- `SDL_DrawGPUIndexedPrimitives` — single batched draw call
- `forge_ui_ctx_begin` / `forge_ui_ctx_end` — UI declaration phase
- `forge_ui_wctx_begin` / `forge_ui_wctx_end` — window z-order sorting

## Correct order

1. **Init (once)**
   a. Load font with `forge_ui_ttf_load`, build atlas with `forge_ui_atlas_build`
   b. Upload atlas pixels to R8_UNORM GPU texture via transfer buffer + copy pass
   c. Create sampler (linear, clamp-to-edge)
   d. Create vertex and fragment shaders from compiled HLSL bytecode
   e. Create pipeline: alpha blend enabled, no depth, cull none, 4x FLOAT2 vertex attrs
   f. Pre-allocate vertex and index GPU buffers (power-of-two sizes)
   g. Init ForgeUiContext and ForgeUiWindowContext

2. **Each frame**
   a. Query window size and mouse state
   b. `forge_ui_ctx_begin` — start UI declaration
   c. Declare windows and widgets (labels, buttons, checkboxes, sliders, text input)
   d. `forge_ui_wctx_end` / `forge_ui_ctx_end` — finalize vertex/index arrays
   e. Resize GPU buffers if needed (power-of-two growth)
   f. Create single transfer buffer, map, copy vertex+index data, unmap
   g. Copy pass: upload vertex data at offset 0, index data after
   h. Release transfer buffer
   i. Acquire swapchain, begin render pass (clear)
   j. Bind pipeline, vertex buffer, index buffer, atlas texture+sampler
   k. Push orthographic projection uniform
   l. `SDL_DrawGPUIndexedPrimitives` — one call for all UI
   m. End render pass, submit command buffer

## Key concepts

1. **ForgeUiVertex is 32 bytes** — 8 floats: pos(2), uv(2), color(4). Pipeline reads as 4x FLOAT2.
2. **White-pixel technique** — solid rects use UVs pointing to a white region in the atlas where coverage = 1.0, so the fragment shader works for both text and solid geometry.
3. **R8_UNORM atlas** — single-channel texture saves 4x memory vs RGBA8. Fragment shader reads `.r` as coverage.
4. **Orthographic projection** — maps [0..W, 0..H] pixels to [-1..+1] clip space with Y flipped for top-left origin. Rebuilt every frame for automatic resize handling.
5. **No depth buffer** — 2D UI uses painter's algorithm via z_order sorting in the window context.
6. **No backface culling** — UI quads may have either winding order.
7. **Single draw call** — all widgets batched into one vertex/index stream by the UI context.

## Theme colors

The forge-gpu project uses a dark blue-gray palette defined in
`scripts/forge_diagrams/_common.py`. All UI colors follow this theme. The
key property: dark surfaces carry a strong blue tint (B/R ratio ~1.8) that
tapers toward neutral at brighter levels (~1.07 for text).

### Reference palette (sRGB)

| Role | Hex | RGBA float | Used for |
|------|-----|------------|----------|
| Background | `#1a1a2e` | (0.10, 0.10, 0.18, 1.0) | Clear color |
| Surface | `#252545` | (0.14, 0.14, 0.27, 1.0) | Panel/window BG |
| Grid | `#2a2a4a` | (0.16, 0.16, 0.29, 1.0) | Title bar BG |
| Accent cyan | `#4fc3f7` | (0.31, 0.76, 0.97, 1.0) | Active/focused states, cursors, borders |
| Accent orange | `#ff7043` | (1.00, 0.44, 0.26, 1.0) | Secondary highlights |
| Accent green | `#66bb6a` | (0.40, 0.73, 0.42, 1.0) | Tertiary highlights |
| Accent purple | `#ab47bc` | (0.67, 0.28, 0.74, 1.0) | Special elements |
| Warn yellow | `#ffd54f` | (1.00, 0.84, 0.31, 1.0) | Warnings, annotations |
| Text | `#e0e0f0` | (0.88, 0.88, 0.94, 1.0) | Primary text, labels |
| Dim text | `#8888aa` | (0.53, 0.53, 0.67, 1.0) | Secondary/info text |

### Deriving new colors

When adding new UI elements, derive colors from the theme by maintaining
the blue tint ratio for the brightness level:

- **Dark** (0.10–0.20 R/G): set B ≈ R × 1.7–1.8
- **Medium** (0.20–0.40 R/G): set B ≈ R × 1.5–1.6
- **Bright** (0.40–0.60 R/G): set B ≈ R × 1.3–1.4
- **Near-white** (0.80+ R/G): set B ≈ R × 1.05–1.15

The default widget colors in `forge_ui_ctx.h` and `forge_ui_window.h`
already follow this theme. The clear color and label colors are set per
lesson (see `main.c` `CLEAR_R/G/B` and `TITLE_LABEL_R/G/B` defines).

## Common mistakes

1. **Using RGBA8 for the atlas** — wastes 4x GPU memory and requires CPU-side pixel expansion. Use R8_UNORM.
2. **Forgetting to flip Y in the projection** — without `-2.0f / height`, the UI renders upside down.
3. **Not checking SDL_SubmitGPUCommandBuffer return** — must check on every path, including error paths after swapchain acquisition.
4. **Leaking the transfer buffer** — release it after the copy pass ends, not after submit.
5. **Not handling the minimized window case** — when swapchain texture is NULL, submit the command buffer and return.
6. **Fixed-size buffers** — if the UI grows beyond initial capacity, you must resize. Use power-of-two growth.
7. **Depth testing with alpha blending** — depth test would discard semi-transparent fragments. Disable it for 2D UI.

## Template

```c
#define SDL_MAIN_USE_CALLBACKS 1
#include "ui/forge_ui.h"
#include "ui/forge_ui_ctx.h"
#include "ui/forge_ui_window.h"
#include "math/forge_math.h"
#include <SDL3/SDL.h>
#include <SDL3/SDL_main.h>

/* Include compiled shader headers */
#include "shaders/compiled/ui_vert_spirv.h"
#include "shaders/compiled/ui_vert_dxil.h"
#include "shaders/compiled/ui_frag_spirv.h"
#include "shaders/compiled/ui_frag_dxil.h"

typedef struct UiUniforms {
    mat4 projection;  /* orthographic pixel-to-NDC mapping */
} UiUniforms;

typedef struct app_state {
    SDL_Window    *window;
    SDL_GPUDevice *device;
    SDL_GPUGraphicsPipeline *pipeline;
    SDL_GPUTexture *atlas_texture;   /* R8_UNORM font atlas */
    SDL_GPUSampler *atlas_sampler;   /* linear, clamp-to-edge */
    SDL_GPUBuffer  *vertex_buffer;
    SDL_GPUBuffer  *index_buffer;
    Uint32 vertex_buffer_size;
    Uint32 index_buffer_size;
    ForgeUiFont     font;
    ForgeUiFontAtlas atlas;
    ForgeUiContext   ui_ctx;
    ForgeUiWindowContext ui_wctx;
    /* ... widget state ... */
} app_state;

/* Orthographic projection: top-left origin, y-down */
static mat4 ui_ortho_projection(float width, float height)
{
    mat4 m = mat4_identity();
    m.m[0]  =  2.0f / width;
    m.m[5]  = -2.0f / height;
    m.m[12] = -1.0f;
    m.m[13] =  1.0f;
    return m;
}
```
