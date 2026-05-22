---
name: fal-image-to-image
description: Complete fal.ai image-to-image system. PROACTIVELY activate for: (1) FLUX image-to-image transformation, (2) ControlNet (canny, depth, pose), (3) Inpainting with masks, (4) Upscaling (ESRGAN, Clarity), (5) Background removal (BiRefNet, RemBG), (6) Face restoration (GFPGAN, CodeFormer), (7) IP-Adapter style transfer, (8) Strength parameter tuning. Provides: Transformation endpoints, mask formats, ControlNet types, upscaling options. Ensures proper image editing and enhancement workflows.
---

## Quick Reference

| Task | Endpoint | Key Parameter |
|------|----------|---------------|
| Transform | `fal-ai/flux/dev/image-to-image` | `strength: 0-1` |
| Inpaint | `fal-ai/flux/dev/inpainting` | `mask_url` |
| ControlNet | `fal-ai/flux-controlnet-union` | `control_type` |
| Upscale | `fal-ai/clarity-upscaler` | `scale_factor: 2-4` |
| Remove BG | `fal-ai/birefnet` | - |
| Face fix | `fal-ai/codeformer` | `fidelity: 0-1` |

| Strength Value | Effect |
|----------------|--------|
| 0.2-0.3 | Subtle style hint |
| 0.5-0.7 | Moderate transform |
| 0.8-1.0 | Full regeneration |

| ControlNet Type | Use Case |
|-----------------|----------|
| `canny` | Edge guidance |
| `depth` | 3D structure |
| `pose` | Human pose |
| `tile` | Detail enhancement |

## When to Use This Skill

Use for **image editing and transformation**:
- Style transfer while preserving structure
- Inpainting to edit specific regions
- ControlNet for guided generation
- Upscaling low-resolution images
- Removing backgrounds
- Restoring faces in old photos

**Related skills:**
- For text-to-image: see `fal-text-to-image`
- For image-to-video: see `fal-image-to-video`
- For model selection: see `fal-model-guide`

---

# fal.ai Image-to-Image Models

Complete reference for all image transformation, editing, and enhancement models on fal.ai.

## FLUX Image-to-Image

### Basic Image-to-Image
**Endpoint:** `fal-ai/flux/dev/image-to-image`
**Best For:** Style transfer, image transformation

Transform existing images while preserving structure.

```typescript
import { fal } from "@fal-ai/client";

const result = await fal.subscribe("fal-ai/flux/dev/image-to-image", {
  input: {
    prompt: "Transform into a watercolor painting style",
    image_url: "https://example.com/photo.jpg",
    strength: 0.75,  // 0-1, how much to transform
    num_inference_steps: 28,
    guidance_scale: 3.5,
    seed: 42
  }
});

console.log(result.images[0].url);
```

```python
import fal_client

result = fal_client.subscribe(
    "fal-ai/flux/dev/image-to-image",
    arguments={
        "prompt": "Transform into a watercolor painting style",
        "image_url": "https://example.com/photo.jpg",
        "strength": 0.75,
        "num_inference_steps": 28,
        "guidance_scale": 3.5
    }
)
print(result["images"][0]["url"])
```

**Strength Parameter:**
- `0.0`: No change (original image)
- `0.3-0.5`: Subtle changes, style hints
- `0.5-0.7`: Moderate transformation
- `0.7-0.9`: Strong transformation, some original preserved
- `1.0`: Complete regeneration (ignores original)

### FLUX Pro Image-to-Image
**Endpoint:** `fal-ai/flux-pro/v1/image-to-image`
**Best For:** Production quality transformations

```typescript
const result = await fal.subscribe("fal-ai/flux-pro/v1/image-to-image", {
  input: {
    prompt: "Professional headshot, studio lighting",
    image_url: "https://example.com/casual-photo.jpg",
    strength: 0.6,
    guidance_scale: 3.5
  }
});
```

## ControlNet Models

### FLUX ControlNet
**Endpoint:** `fal-ai/flux-controlnet`
**Best For:** Precise structural control

```typescript
const result = await fal.subscribe("fal-ai/flux-controlnet", {
  input: {
    prompt: "A modern house with large windows",
    control_image_url: "https://example.com/architecture-sketch.png",
    controlnet_conditioning_scale: 0.8,
    num_inference_steps: 28,
    guidance_scale: 3.5
  }
});
```

### FLUX ControlNet Union
**Endpoint:** `fal-ai/flux-controlnet-union`
**Best For:** Multiple control types in one model

Supports: canny, depth, pose, tile, blur, gray, low_quality

```typescript
const result = await fal.subscribe("fal-ai/flux-controlnet-union", {
  input: {
    prompt: "A beautiful woman in a red dress",
    control_image_url: "https://example.com/pose-reference.png",
    control_type: "pose",
    controlnet_conditioning_scale: 0.7,
    num_inference_steps: 28
  }
});
```

**Control Types:**
- `canny`: Edge detection guidance
- `depth`: Depth map guidance
- `pose`: Human pose guidance
- `tile`: Detail enhancement
- `blur`: Blur-based control
- `gray`: Grayscale structure
- `low_quality`: Quality enhancement

### SDXL ControlNet
**Endpoint:** `fal-ai/fast-sdxl/controlnet`
**Best For:** SDXL with structural control

```typescript
const result = await fal.subscribe("fal-ai/fast-sdxl/controlnet", {
  input: {
    prompt: "A futuristic cityscape",
    negative_prompt: "blurry, low quality",
    control_image_url: "https://example.com/depth-map.png",
    controlnet_type: "depth",
    controlnet_conditioning_scale: 0.8
  }
});
```

### Canny Edge Detection
**Endpoint:** `fal-ai/flux-controlnet-canny`
**Best For:** Edge-based generation

```typescript
const result = await fal.subscribe("fal-ai/flux-controlnet-canny", {
  input: {
    prompt: "A detailed architectural drawing",
    control_image_url: "https://example.com/building-photo.jpg",
    controlnet_conditioning_scale: 0.9
  }
});
```

### Depth-Based Control
**Endpoint:** `fal-ai/flux-controlnet-depth`
**Best For:** 3D-aware generation

```typescript
const result = await fal.subscribe("fal-ai/flux-controlnet-depth", {
  input: {
    prompt: "A mystical forest scene",
    control_image_url: "https://example.com/depth-map.png",
    controlnet_conditioning_scale: 0.7
  }
});
```

## Inpainting Models

### FLUX Inpainting
**Endpoint:** `fal-ai/flux/dev/inpainting`
**Best For:** Editing specific regions

```typescript
const result = await fal.subscribe("fal-ai/flux/dev/inpainting", {
  input: {
    prompt: "A golden retriever",
    image_url: "https://example.com/photo-with-pet.jpg",
    mask_url: "https://example.com/mask.png",  // White = edit area
    num_inference_steps: 28,
    guidance_scale: 3.5
  }
});
```

```python
result = fal_client.subscribe(
    "fal-ai/flux/dev/inpainting",
    arguments={
        "prompt": "A golden retriever",
        "image_url": "https://example.com/photo.jpg",
        "mask_url": "https://example.com/mask.png"
    }
)
```

**Mask Format:**
- White pixels (255, 255, 255): Areas to edit/regenerate
- Black pixels (0, 0, 0): Areas to preserve

### FLUX Pro Fill
**Endpoint:** `fal-ai/flux-pro/v1/fill`
**Best For:** High-quality inpainting and outpainting

```typescript
const result = await fal.subscribe("fal-ai/flux-pro/v1/fill", {
  input: {
    prompt: "Seamless continuation of the landscape",
    image_url: "https://example.com/partial-image.jpg",
    mask_url: "https://example.com/outpaint-mask.png"
  }
});
```

### SDXL Inpainting
**Endpoint:** `fal-ai/fast-sdxl/inpainting`
**Best For:** SDXL-based region editing

```typescript
const result = await fal.subscribe("fal-ai/fast-sdxl/inpainting", {
  input: {
    prompt: "A beautiful flower arrangement",
    negative_prompt: "ugly, distorted",
    image_url: "https://example.com/vase.jpg",
    mask_url: "https://example.com/vase-mask.png"
  }
});
```

## Upscaling Models

### ESRGAN 4x
**Endpoint:** `fal-ai/esrgan`
**Best For:** Classic 4x upscaling

```typescript
const result = await fal.subscribe("fal-ai/esrgan", {
  input: {
    image_url: "https://example.com/low-res-image.jpg",
    scale: 4  // 2 or 4
  }
});

// Result is 4x the original resolution
console.log(result.image.url);
```

```python
result = fal_client.subscribe(
    "fal-ai/esrgan",
    arguments={
        "image_url": "https://example.com/low-res.jpg",
        "scale": 4
    }
)
print(result["image"]["url"])
```

### Clarity Upscaler
**Endpoint:** `fal-ai/clarity-upscaler`
**Best For:** AI-enhanced upscaling with detail generation

```typescript
const result = await fal.subscribe("fal-ai/clarity-upscaler", {
  input: {
    image_url: "https://example.com/image.jpg",
    scale_factor: 2,  // 1-4
    prompt: "high quality, detailed, sharp",
    creativity: 0.3,  // 0-1, how much to add
    resemblance: 0.8  // 0-1, similarity to original
  }
});
```

**Parameters:**
- `scale_factor`: 1-4, upscale multiplier
- `creativity`: 0-1, how much AI can "imagine" details
- `resemblance`: 0-1, how closely to match original
- `prompt`: Optional guidance for detail generation

### Real-ESRGAN
**Endpoint:** `fal-ai/real-esrgan`
**Best For:** General-purpose upscaling

```typescript
const result = await fal.subscribe("fal-ai/real-esrgan", {
  input: {
    image_url: "https://example.com/image.jpg",
    scale: 4,
    face_enhance: true  // Enhance faces
  }
});
```

### Creative Upscaler
**Endpoint:** `fal-ai/creative-upscaler`
**Best For:** Artistic upscaling with regeneration

```typescript
const result = await fal.subscribe("fal-ai/creative-upscaler", {
  input: {
    image_url: "https://example.com/image.jpg",
    scale: 2,
    prompt: "highly detailed, photorealistic"
  }
});
```

## Background Removal

### BiRefNet
**Endpoint:** `fal-ai/birefnet`
**Best For:** High-quality background removal

```typescript
const result = await fal.subscribe("fal-ai/birefnet", {
  input: {
    image_url: "https://example.com/product-photo.jpg"
  }
});

// Returns image with transparent background
console.log(result.image.url);
```

```python
result = fal_client.subscribe(
    "fal-ai/birefnet",
    arguments={
        "image_url": "https://example.com/photo.jpg"
    }
)
# PNG with transparent background
print(result["image"]["url"])
```

### RemBG
**Endpoint:** `fal-ai/rembg`
**Best For:** Fast background removal

```typescript
const result = await fal.subscribe("fal-ai/rembg", {
  input: {
    image_url: "https://example.com/image.jpg"
  }
});
```

### Background Removal (BRIA)
**Endpoint:** `fal-ai/bria/background-removal`
**Best For:** Commercial-grade background removal

```typescript
const result = await fal.subscribe("fal-ai/bria/background-removal", {
  input: {
    image_url: "https://example.com/image.jpg"
  }
});
```

## Face Enhancement

### GFPGAN
**Endpoint:** `fal-ai/gfpgan`
**Best For:** Face restoration

```typescript
const result = await fal.subscribe("fal-ai/gfpgan", {
  input: {
    image_url: "https://example.com/old-photo.jpg",
    version: "1.4",  // or "1.3"
    scale: 2
  }
});
```

### CodeFormer
**Endpoint:** `fal-ai/codeformer`
**Best For:** Advanced face restoration

```typescript
const result = await fal.subscribe("fal-ai/codeformer", {
  input: {
    image_url: "https://example.com/damaged-photo.jpg",
    fidelity: 0.7  // 0-1, balance quality vs fidelity
  }
});
```

## IP-Adapter (Style Transfer)

### FLUX IP-Adapter
**Endpoint:** `fal-ai/flux-ip-adapter`
**Best For:** Style reference from image

```typescript
const result = await fal.subscribe("fal-ai/flux-ip-adapter", {
  input: {
    prompt: "A modern living room",
    image_url: "https://example.com/style-reference.jpg",
    ip_adapter_scale: 0.7,  // 0-1, style strength
    num_inference_steps: 28
  }
});
```

### IP-Adapter Face ID
**Endpoint:** `fal-ai/flux-ip-adapter-face-id`
**Best For:** Face consistency across generations

```typescript
const result = await fal.subscribe("fal-ai/flux-ip-adapter-face-id", {
  input: {
    prompt: "A portrait in renaissance style",
    face_image_url: "https://example.com/face-reference.jpg",
    ip_adapter_scale: 0.8
  }
});
```

## Image-to-Image Parameter Reference

### Common Parameters

```typescript
interface ImageToImageInput {
  prompt: string;
  image_url: string;

  // Transformation strength
  strength?: number;  // 0-1, how much to change

  // Generation parameters
  num_inference_steps?: number;
  guidance_scale?: number;
  seed?: number;

  // Output
  output_format?: "jpeg" | "png";
}
```

### ControlNet Parameters

```typescript
interface ControlNetInput {
  prompt: string;
  control_image_url: string;
  control_type?: "canny" | "depth" | "pose" | "tile" | "blur" | "gray";
  controlnet_conditioning_scale?: number;  // 0-1

  num_inference_steps?: number;
  guidance_scale?: number;
  seed?: number;
}
```

### Inpainting Parameters

```typescript
interface InpaintingInput {
  prompt: string;
  image_url: string;
  mask_url: string;  // White = edit, Black = preserve

  num_inference_steps?: number;
  guidance_scale?: number;
  seed?: number;
}
```

### Upscaling Parameters

```typescript
interface UpscalingInput {
  image_url: string;
  scale?: number;  // 2 or 4

  // For AI upscalers
  prompt?: string;
  creativity?: number;
  resemblance?: number;
}
```

## Workflow Examples

### Complete Product Photo Pipeline

```typescript
// 1. Remove background
const bgRemoved = await fal.subscribe("fal-ai/birefnet", {
  input: { image_url: originalProductUrl }
});

// 2. Upscale
const upscaled = await fal.subscribe("fal-ai/clarity-upscaler", {
  input: {
    image_url: bgRemoved.image.url,
    scale_factor: 2,
    prompt: "product photography, studio lighting"
  }
});

// 3. Apply style transformation
const styled = await fal.subscribe("fal-ai/flux/dev/image-to-image", {
  input: {
    prompt: "Professional e-commerce product photo, white background, soft shadows",
    image_url: upscaled.image.url,
    strength: 0.3
  }
});
```

### Face Restoration Pipeline

```typescript
// 1. Upscale
const upscaled = await fal.subscribe("fal-ai/real-esrgan", {
  input: {
    image_url: oldPhotoUrl,
    scale: 4,
    face_enhance: false
  }
});

// 2. Restore faces
const restored = await fal.subscribe("fal-ai/codeformer", {
  input: {
    image_url: upscaled.image.url,
    fidelity: 0.7
  }
});
```

### Style Transfer with Structure

```typescript
// Use ControlNet to maintain structure while changing style
const result = await fal.subscribe("fal-ai/flux-controlnet-canny", {
  input: {
    prompt: "oil painting style, impressionist, vibrant colors",
    control_image_url: originalPhotoUrl,
    controlnet_conditioning_scale: 0.9
  }
});
```

## Best Practices

### Strength Guidelines

| Task | Recommended Strength |
|------|---------------------|
| Color correction | 0.2-0.3 |
| Style hint | 0.3-0.5 |
| Style transfer | 0.5-0.7 |
| Reimagining | 0.7-0.9 |
| Full regeneration | 0.9-1.0 |

### ControlNet Scale Guidelines

| Use Case | Recommended Scale |
|----------|-------------------|
| Strict structure | 0.9-1.0 |
| Balanced | 0.7-0.8 |
| Loose guidance | 0.4-0.6 |

### Mask Creation Tips

1. **Clean edges**: Use anti-aliased masks for smooth blending
2. **Feathering**: Slight blur on mask edges reduces artifacts
3. **Coverage**: Include slightly more area than needed
4. **Format**: PNG with white=edit, black=preserve

### File Upload for Large Images

```typescript
// Upload file first for large images
const file = await fetch("local-image.jpg").then(r => r.blob());
const uploadedUrl = await fal.storage.upload(
  new File([file], "image.jpg", { type: "image/jpeg" })
);

// Then use in transformation
const result = await fal.subscribe("fal-ai/flux/dev/image-to-image", {
  input: {
    prompt: "...",
    image_url: uploadedUrl,
    strength: 0.5
  }
});
```
