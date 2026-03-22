---
name: forge-textures-and-samplers
description: Load images, create GPU textures and samplers, draw textured geometry with index buffers. Use when someone needs to map an image onto geometry, set up texture filtering, or use index buffers in SDL3 GPU.
---

# Textures & Samplers — Image Loading, GPU Upload, and Texture Mapping

This skill teaches how to load images from disk, upload them to the GPU as
textures, create samplers, and draw textured geometry using index buffers.
It builds on the `uniforms-and-motion` skill (push uniforms, animation) and
the `first-triangle` skill (vertex buffers, pipeline).

## When to use

- Loading and displaying images/textures in SDL3 GPU
- Setting up texture filtering (linear, nearest) and address modes (repeat, clamp)
- Drawing quads or other geometry with UV-mapped textures
- Using index buffers to avoid duplicate vertices
- Getting correct sRGB color handling for textures

## Texture loading and upload

### Step 1: Load from disk

```c
SDL_Surface *surface = SDL_LoadSurface(path);  /* handles BMP and PNG */
```

### Step 2: Convert to RGBA8

```c
SDL_Surface *converted = SDL_ConvertSurface(surface, SDL_PIXELFORMAT_ABGR8888);
SDL_DestroySurface(surface);
```

**Pixel format mapping:** SDL `ABGR8888` = GPU `R8G8B8A8` (SDL names bits
MSB→LSB, GPU names bytes in memory order).

### Step 3: Create GPU texture

```c
SDL_GPUTextureCreateInfo tex_info = { 0 };
tex_info.type                 = SDL_GPU_TEXTURETYPE_2D;
tex_info.format               = SDL_GPU_TEXTUREFORMAT_R8G8B8A8_UNORM_SRGB;
tex_info.usage                = SDL_GPU_TEXTUREUSAGE_SAMPLER;
tex_info.width                = converted->w;
tex_info.height               = converted->h;
tex_info.layer_count_or_depth = 1;
tex_info.num_levels           = 1;

SDL_GPUTexture *texture = SDL_CreateGPUTexture(device, &tex_info);
```

Use `_SRGB` format for textures with sRGB color data (most photographs and
hand-painted textures). The GPU auto-converts sRGB→linear when sampling.

### Step 4: Upload via transfer buffer

```c
Uint32 bytes_per_row = (Uint32)tex_w * 4;
Uint32 total_bytes   = bytes_per_row * (Uint32)tex_h;

/* Create and fill transfer buffer */
SDL_GPUTransferBufferCreateInfo xfer_info = { 0 };
xfer_info.usage = SDL_GPU_TRANSFERBUFFERUSAGE_UPLOAD;
xfer_info.size  = total_bytes;

SDL_GPUTransferBuffer *transfer = SDL_CreateGPUTransferBuffer(device, &xfer_info);
void *mapped = SDL_MapGPUTransferBuffer(device, transfer, false);

/* Copy row-by-row to handle surface pitch padding */
const Uint8 *src = (const Uint8 *)converted->pixels;
Uint8 *dst = (Uint8 *)mapped;
for (int y = 0; y < tex_h; y++) {
    SDL_memcpy(dst + y * bytes_per_row, src + y * converted->pitch, bytes_per_row);
}
SDL_UnmapGPUTransferBuffer(device, transfer);

/* Issue GPU upload command */
SDL_GPUCommandBuffer *cmd = SDL_AcquireGPUCommandBuffer(device);
SDL_GPUCopyPass *copy = SDL_BeginGPUCopyPass(cmd);

SDL_GPUTextureTransferInfo tex_src = { 0 };
tex_src.transfer_buffer = transfer;
tex_src.pixels_per_row  = tex_w;
tex_src.rows_per_layer  = tex_h;

SDL_GPUTextureRegion tex_dst = { 0 };
tex_dst.texture = texture;
tex_dst.w       = tex_w;
tex_dst.h       = tex_h;
tex_dst.d       = 1;

SDL_UploadToGPUTexture(copy, &tex_src, &tex_dst, false);
SDL_EndGPUCopyPass(copy);
SDL_SubmitGPUCommandBuffer(cmd);

SDL_ReleaseGPUTransferBuffer(device, transfer);
SDL_DestroySurface(converted);
```

## Sampler creation

```c
SDL_GPUSamplerCreateInfo sampler_info = { 0 };
sampler_info.min_filter     = SDL_GPU_FILTER_LINEAR;      /* smooth scaling down */
sampler_info.mag_filter     = SDL_GPU_FILTER_LINEAR;      /* smooth scaling up   */
sampler_info.mipmap_mode    = SDL_GPU_SAMPLERMIPMAPMODE_LINEAR;
sampler_info.address_mode_u = SDL_GPU_SAMPLERADDRESSMODE_REPEAT;  /* tile U */
sampler_info.address_mode_v = SDL_GPU_SAMPLERADDRESSMODE_REPEAT;  /* tile V */
sampler_info.address_mode_w = SDL_GPU_SAMPLERADDRESSMODE_REPEAT;

SDL_GPUSampler *sampler = SDL_CreateGPUSampler(device, &sampler_info);
```

**Filter options:** `LINEAR` (smooth) or `NEAREST` (pixelated/pixel-art).
**Address modes:** `REPEAT` (tile), `CLAMP_TO_EDGE`, `MIRRORED_REPEAT`.

## Vertex format with UVs

```c
typedef struct Vertex {
    vec2 position;   /* NDC position   — TEXCOORD0 */
    vec2 uv;         /* texture coord  — TEXCOORD1 */
} Vertex;
```

UV origin is at top-left: (0,0) = top-left, (1,1) = bottom-right.

## Index buffer

```c
/* Create index buffer */
SDL_GPUBufferCreateInfo ibuf_info = { 0 };
ibuf_info.usage = SDL_GPU_BUFFERUSAGE_INDEX;
ibuf_info.size  = sizeof(indices);
SDL_GPUBuffer *index_buffer = SDL_CreateGPUBuffer(device, &ibuf_info);

/* Upload (same transfer pattern as vertex buffer) */

/* Bind during render */
SDL_GPUBufferBinding index_binding = { 0 };
index_binding.buffer = index_buffer;
SDL_BindGPUIndexBuffer(pass, &index_binding, SDL_GPU_INDEXELEMENTSIZE_16BIT);

/* Draw */
SDL_DrawGPUIndexedPrimitives(pass, index_count, 1, 0, 0, 0);
```

Use `SDL_GPU_INDEXELEMENTSIZE_16BIT` for `Uint16` indices (up to 65535 vertices)
or `SDL_GPU_INDEXELEMENTSIZE_32BIT` for `Uint32` indices.

## HLSL fragment shader

```hlsl
Texture2D    tex : register(t0, space2);   /* fragment texture slot 0 */
SamplerState smp : register(s0, space2);   /* fragment sampler slot 0 */

float4 main(PSInput input) : SV_Target
{
    return tex.Sample(smp, input.uv);
}
```

**Register convention for fragment-stage resources:**

| Resource | Register |
|----------|----------|
| Texture slot N | `register(tN, space2)` |
| Sampler slot N | `register(sN, space2)` |

## Binding texture + sampler at draw time

```c
SDL_GPUTextureSamplerBinding binding = { 0 };
binding.texture = texture;
binding.sampler = sampler;
SDL_BindGPUFragmentSamplers(pass, 0, &binding, 1);
```

The first `0` is the first slot. The `1` is the count. For multiple textures,
pass an array of bindings.

## Shader creation — declaring sampler count

```c
/* Fragment shader with 1 texture+sampler pair */
info.num_samplers = 1;   /* ← must match number of Texture2D/SamplerState pairs */
```

## sRGB color pipeline

For correct colors end-to-end:

1. **Texture:** `R8G8B8A8_UNORM_SRGB` (sRGB→linear on sample)
2. **Shader:** math in linear space
3. **Swapchain:** `SDR_LINEAR` composition (linear→sRGB on write)

Without `_SRGB` formats, colors appear washed out (gamma applied twice).

## CMake — copying textures

```cmake
# Copy texture files next to executable for runtime loading
add_custom_command(TARGET my-target POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E make_directory
        $<TARGET_FILE_DIR:my-target>/textures
    COMMAND ${CMAKE_COMMAND} -E copy_if_different
        ${CMAKE_CURRENT_SOURCE_DIR}/textures/my_texture.png
        $<TARGET_FILE_DIR:my-target>/textures/my_texture.png
)
```

## Common mistakes

| Mistake | Fix |
|---------|-----|
| `num_samplers = 0` but shader has Texture2D + SamplerState | Must match — set to 1 (or however many texture+sampler pairs) |
| Wrong pixel format conversion | Use `SDL_PIXELFORMAT_ABGR8888` for GPU `R8G8B8A8` format |
| Texture looks washed out | Use `_SRGB` texture format (`R8G8B8A8_UNORM_SRGB`) |
| Texture not found at runtime | Use CMake POST_BUILD to copy texture next to executable |
| Wrong register space for fragment textures | Fragment textures/samplers use `space2` |
| Surface pitch != width * bpp | Copy row-by-row to strip padding |
| Using `SDL_GPU_INDEXELEMENTSIZE_32BIT` with `Uint16` indices | Match element size to your index type |
| Forgetting to bind index buffer before `SDL_DrawGPUIndexedPrimitives` | Bind with `SDL_BindGPUIndexBuffer` before drawing |

## Cleanup

Release in reverse order of creation:

```c
SDL_ReleaseGPUSampler(device, sampler);
SDL_ReleaseGPUTexture(device, texture);
SDL_ReleaseGPUBuffer(device, index_buffer);
SDL_ReleaseGPUBuffer(device, vertex_buffer);
SDL_ReleaseGPUGraphicsPipeline(device, pipeline);
```

## Code template — end-to-end workflow

Minimal scaffold showing the full texture + index buffer workflow in order:

```c
/* ── 1. Load and convert image ──────────────────────────────────────── */
SDL_Surface *surface   = SDL_LoadSurface("textures/my_texture.png");
SDL_Surface *converted = SDL_ConvertSurface(surface, SDL_PIXELFORMAT_ABGR8888);
SDL_DestroySurface(surface);

/* ── 2. Create GPU texture ──────────────────────────────────────────── */
SDL_GPUTextureCreateInfo tex_info = { 0 };
tex_info.type   = SDL_GPU_TEXTURETYPE_2D;
tex_info.format = SDL_GPU_TEXTUREFORMAT_R8G8B8A8_UNORM_SRGB;
tex_info.usage  = SDL_GPU_TEXTUREUSAGE_SAMPLER;
tex_info.width  = converted->w;
tex_info.height = converted->h;
tex_info.layer_count_or_depth = 1;
tex_info.num_levels           = 1;
SDL_GPUTexture *texture = SDL_CreateGPUTexture(device, &tex_info);

/* ── 3. Upload pixels via transfer buffer ───────────────────────────── */
Uint32 bytes_per_row = (Uint32)converted->w * 4;
Uint32 total_bytes   = bytes_per_row * (Uint32)converted->h;

SDL_GPUTransferBufferCreateInfo xfer_info = { 0 };
xfer_info.usage = SDL_GPU_TRANSFERBUFFERUSAGE_UPLOAD;
xfer_info.size  = total_bytes;
SDL_GPUTransferBuffer *transfer = SDL_CreateGPUTransferBuffer(device, &xfer_info);

Uint8 *mapped = SDL_MapGPUTransferBuffer(device, transfer, false);
for (int y = 0; y < converted->h; y++)
    SDL_memcpy(mapped + y * bytes_per_row,
               (Uint8 *)converted->pixels + y * converted->pitch,
               bytes_per_row);
SDL_UnmapGPUTransferBuffer(device, transfer);

SDL_GPUCommandBuffer *cmd  = SDL_AcquireGPUCommandBuffer(device);
SDL_GPUCopyPass      *copy = SDL_BeginGPUCopyPass(cmd);

SDL_GPUTextureTransferInfo src = { .transfer_buffer = transfer,
    .pixels_per_row = converted->w, .rows_per_layer = converted->h };
SDL_GPUTextureRegion dst = { .texture = texture,
    .w = converted->w, .h = converted->h, .d = 1 };
SDL_UploadToGPUTexture(copy, &src, &dst, false);

SDL_EndGPUCopyPass(copy);
SDL_SubmitGPUCommandBuffer(cmd);
SDL_ReleaseGPUTransferBuffer(device, transfer);
SDL_DestroySurface(converted);

/* ── 4. Create sampler ──────────────────────────────────────────────── */
SDL_GPUSamplerCreateInfo smp_info = { 0 };
smp_info.min_filter     = SDL_GPU_FILTER_LINEAR;
smp_info.mag_filter     = SDL_GPU_FILTER_LINEAR;
smp_info.address_mode_u = SDL_GPU_SAMPLERADDRESSMODE_REPEAT;
smp_info.address_mode_v = SDL_GPU_SAMPLERADDRESSMODE_REPEAT;
SDL_GPUSampler *sampler = SDL_CreateGPUSampler(device, &smp_info);

/* ── 5. Create index buffer and upload ──────────────────────────────── */
Uint16 indices[] = { 0, 1, 2, 2, 3, 0 };

SDL_GPUBufferCreateInfo ibuf_info = { 0 };
ibuf_info.usage = SDL_GPU_BUFFERUSAGE_INDEX;
ibuf_info.size  = sizeof(indices);
SDL_GPUBuffer *index_buffer = SDL_CreateGPUBuffer(device, &ibuf_info);
/* ... upload via transfer buffer (same pattern as vertex data) ... */

/* ── 6. In render loop: bind and draw ───────────────────────────────── */
SDL_GPUTextureSamplerBinding tex_bind = { .texture = texture, .sampler = sampler };
SDL_BindGPUFragmentSamplers(pass, 0, &tex_bind, 1);

SDL_GPUBufferBinding idx_bind = { .buffer = index_buffer };
SDL_BindGPUIndexBuffer(pass, &idx_bind, SDL_GPU_INDEXELEMENTSIZE_16BIT);

SDL_DrawGPUIndexedPrimitives(pass, 6, 1, 0, 0, 0);
```
