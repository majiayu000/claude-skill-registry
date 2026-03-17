---
name: fal-text-to-image
description: Complete fal.ai text-to-image system. PROACTIVELY activate for: (1) FLUX.1/2 Pro/Dev/Schnell generation, (2) SDXL and Fast SDXL, (3) Image size presets (square_hd, landscape_16_9), (4) Guidance scale and inference steps, (5) LoRA model application, (6) Seed for reproducibility, (7) Batch generation (num_images), (8) Ideogram for text in images, (9) Recraft for design assets. Provides: Model endpoints, parameter reference, prompt engineering, quality vs speed trade-offs. Ensures optimal text-to-image generation.
---

## Quick Reference

| Model | Endpoint | Speed | Quality | Cost |
|-------|----------|-------|---------|------|
| FLUX.2 Pro | `fal-ai/flux-2-pro` | Medium | Highest | $$$ |
| FLUX.1 Dev | `fal-ai/flux/dev` | Medium | High | $$ |
| FLUX Schnell | `fal-ai/flux/schnell` | Fast | Good | $ |
| Fast SDXL | `fal-ai/fast-sdxl` | Fast | Good | $ |

| Image Size | Preset | Dimensions |
|------------|--------|------------|
| Square HD | `square_hd` | 1024x1024 |
| Landscape | `landscape_16_9` | 1024x576 |
| Portrait | `portrait_16_9` | 576x1024 |
| Custom | `{ width, height }` | Any |

| Parameter | FLUX Default | SDXL Default |
|-----------|--------------|--------------|
| `guidance_scale` | 3.5 | 7.5 |
| `num_inference_steps` | 28 | 25 |
| `num_images` | 1 | 1 |

## When to Use This Skill

Use for **text-to-image generation**:
- Generating images from text prompts
- Choosing between FLUX and SDXL models
- Configuring image sizes and quality parameters
- Using LoRA models for custom styles
- Batch generating multiple images

**Related skills:**
- For image editing: see `fal-image-to-image`
- For model comparison: see `fal-model-guide`
- For API integration: see `fal-api-reference`

---

# fal.ai Text-to-Image Models

Complete reference for all text-to-image generation models on fal.ai.

## FLUX Models

### FLUX.1 [dev]
**Endpoint:** `fal-ai/flux/dev`
**Pricing:** $0.025/megapixel
**Best For:** High-quality open-source generation

The 12B parameter FLUX.1 model offers excellent quality with open-source accessibility.

```typescript
import { fal } from "@fal-ai/client";

const result = await fal.subscribe("fal-ai/flux/dev", {
  input: {
    prompt: "A serene Japanese garden with cherry blossoms, koi pond, wooden bridge, soft morning light",
    image_size: "landscape_16_9",
    num_inference_steps: 28,
    guidance_scale: 3.5,
    num_images: 1,
    seed: 42,
    enable_safety_checker: true,
    output_format: "jpeg"
  }
});

console.log(result.images[0].url);
```

```python
import fal_client

result = fal_client.subscribe(
    "fal-ai/flux/dev",
    arguments={
        "prompt": "A serene Japanese garden with cherry blossoms",
        "image_size": "landscape_16_9",
        "num_inference_steps": 28,
        "guidance_scale": 3.5,
        "num_images": 1,
        "seed": 42,
        "enable_safety_checker": True,
        "output_format": "jpeg"
    }
)
print(result["images"][0]["url"])
```

### FLUX Schnell
**Endpoint:** `fal-ai/flux/schnell`
**Pricing:** Lower cost per image
**Best For:** Fast iteration, previews, 4-step generation

Optimized for speed with only 4 inference steps required.

```typescript
const result = await fal.subscribe("fal-ai/flux/schnell", {
  input: {
    prompt: "A colorful abstract painting",
    image_size: "square_hd",
    num_inference_steps: 4,  // Optimized for 4 steps
    num_images: 1
  }
});
```

### FLUX Pro
**Endpoint:** `fal-ai/flux-pro`
**Pricing:** Premium
**Best For:** Production workloads

```typescript
const result = await fal.subscribe("fal-ai/flux-pro", {
  input: {
    prompt: "Professional product photography of a luxury watch",
    image_size: "square_hd",
    num_inference_steps: 28,
    guidance_scale: 3.5
  }
});
```

### FLUX.2 [pro]
**Endpoint:** `fal-ai/flux-2-pro`
**Pricing:** $0.03/megapixel
**Best For:** Highest quality, automatic prompt enhancement

The latest FLUX model with built-in prompt optimization.

```typescript
const result = await fal.subscribe("fal-ai/flux-2-pro", {
  input: {
    prompt: "A majestic lion in the savanna at golden hour",
    image_size: "landscape_16_9",
    num_inference_steps: 28,
    guidance_scale: 3.5,
    // FLUX 2 Pro features
    safety_tolerance: "2",  // 1-6, higher = more permissive
    raw: false  // Set true to disable prompt enhancement
  }
});
```

**FLUX.2 Pro Specific Parameters:**
- `safety_tolerance`: 1-6, controls content filtering sensitivity
- `raw`: Boolean, set to `true` to disable automatic prompt enhancement

### FLUX LoRA
**Endpoint:** `fal-ai/flux-lora`
**Best For:** Custom trained styles and subjects

Apply custom LoRA models to FLUX generation.

```typescript
const result = await fal.subscribe("fal-ai/flux-lora", {
  input: {
    prompt: "A portrait in the style of <lora_trigger>",
    loras: [
      {
        path: "https://huggingface.co/user/lora-model/resolve/main/lora.safetensors",
        scale: 0.8
      }
    ],
    image_size: "portrait_4_3",
    num_inference_steps: 28,
    guidance_scale: 3.5
  }
});
```

**LoRA Parameters:**
- `loras`: Array of LoRA configurations
  - `path`: URL to LoRA weights (.safetensors)
  - `scale`: 0-1, strength of LoRA effect

### FLUX Realism
**Endpoint:** `fal-ai/flux-realism`
**Best For:** Photorealistic images

```typescript
const result = await fal.subscribe("fal-ai/flux-realism", {
  input: {
    prompt: "A photorealistic portrait of a young woman, natural lighting, 85mm lens",
    image_size: "portrait_4_3",
    num_inference_steps: 28
  }
});
```

### FLUX Fill (Outpainting)
**Endpoint:** `fal-ai/flux-pro/v1/fill`
**Best For:** Extending images beyond boundaries

```typescript
const result = await fal.subscribe("fal-ai/flux-pro/v1/fill", {
  input: {
    prompt: "Continue the landscape with mountains",
    image_url: "https://example.com/partial-image.jpg",
    mask_url: "https://example.com/outpaint-mask.png"
  }
});
```

## Stable Diffusion Models

### Fast SDXL
**Endpoint:** `fal-ai/fast-sdxl`
**Best For:** Speed and cost efficiency

```typescript
const result = await fal.subscribe("fal-ai/fast-sdxl", {
  input: {
    prompt: "A fantasy castle on a cliff, dramatic lighting",
    negative_prompt: "blurry, low quality, distorted",
    image_size: "landscape_16_9",
    num_inference_steps: 25,
    guidance_scale: 7.5,
    num_images: 1,
    seed: 42
  }
});
```

**SDXL-Specific Parameters:**
- `negative_prompt`: What to avoid in generation
- Higher `guidance_scale` (7-12) works better for SDXL

### Stable Diffusion 3 Medium
**Endpoint:** `fal-ai/stable-diffusion-v3-medium`
**Best For:** SD3 architecture, good text rendering

```typescript
const result = await fal.subscribe("fal-ai/stable-diffusion-v3-medium", {
  input: {
    prompt: "A sign that says 'Hello World' in neon lights",
    negative_prompt: "blurry, distorted text",
    image_size: "square_hd",
    num_inference_steps: 28,
    guidance_scale: 7.0
  }
});
```

### SDXL Turbo
**Endpoint:** `fal-ai/sdxl-turbo`
**Best For:** Ultra-fast, single-step generation

```typescript
const result = await fal.subscribe("fal-ai/sdxl-turbo", {
  input: {
    prompt: "A cute robot",
    num_inference_steps: 1,  // Single step!
    guidance_scale: 0  // No guidance needed
  }
});
```

### SDXL Lightning
**Endpoint:** `fal-ai/fast-lightning-sdxl`
**Best For:** Fast 4-step SDXL

```typescript
const result = await fal.subscribe("fal-ai/fast-lightning-sdxl", {
  input: {
    prompt: "A beautiful sunset",
    num_inference_steps: 4,
    guidance_scale: 1.5
  }
});
```

## Specialized Models

### Recraft V3
**Endpoint:** `fal-ai/recraft-v3`
**Best For:** Design assets, illustrations, vector-style

```typescript
const result = await fal.subscribe("fal-ai/recraft-v3", {
  input: {
    prompt: "A minimalist logo for a tech startup, clean lines",
    image_size: "square_hd",
    style: "digital_illustration"  // or "realistic_image", "vector_illustration"
  }
});
```

**Recraft Styles:**
- `realistic_image`
- `digital_illustration`
- `vector_illustration`
- `icon`

### Ideogram
**Endpoint:** `fal-ai/ideogram`
**Best For:** Text in images, typography

```typescript
const result = await fal.subscribe("fal-ai/ideogram", {
  input: {
    prompt: "A vintage poster with the text 'JAZZ FESTIVAL' in art deco style",
    aspect_ratio: "portrait_4_3"
  }
});
```

### Playground v2.5
**Endpoint:** `fal-ai/playground-v25`
**Best For:** Creative, artistic images

```typescript
const result = await fal.subscribe("fal-ai/playground-v25", {
  input: {
    prompt: "A surreal dreamscape with floating islands",
    image_size: "landscape_16_9",
    guidance_scale: 3.0
  }
});
```

### AuraFlow
**Endpoint:** `fal-ai/aura-flow`
**Best For:** Open-source flow-based model

```typescript
const result = await fal.subscribe("fal-ai/aura-flow", {
  input: {
    prompt: "A magical forest with bioluminescent plants",
    num_inference_steps: 28,
    guidance_scale: 3.5
  }
});
```

### Kolors
**Endpoint:** `fal-ai/kolors`
**Best For:** Artistic, colorful generations

```typescript
const result = await fal.subscribe("fal-ai/kolors", {
  input: {
    prompt: "A vibrant street market in Morocco",
    image_size: "landscape_4_3"
  }
});
```

## Common Parameters Reference

### Image Size Options

| Preset | Dimensions | Aspect Ratio |
|--------|------------|--------------|
| `square` | 512x512 | 1:1 |
| `square_hd` | 1024x1024 | 1:1 |
| `portrait_4_3` | 768x1024 | 3:4 |
| `portrait_16_9` | 576x1024 | 9:16 |
| `landscape_4_3` | 1024x768 | 4:3 |
| `landscape_16_9` | 1024x576 | 16:9 |

**Custom Dimensions:**
```typescript
image_size: { width: 1920, height: 1080 }
```

### Complete Parameter Reference

```typescript
interface TextToImageInput {
  // Required
  prompt: string;

  // Image dimensions
  image_size?:
    | "square" | "square_hd"
    | "portrait_4_3" | "portrait_16_9"
    | "landscape_4_3" | "landscape_16_9"
    | { width: number; height: number };

  // Generation parameters
  num_inference_steps?: number;  // 1-50, default varies by model
  guidance_scale?: number;       // 1-20, default: 3.5 (FLUX) or 7.5 (SDXL)
  num_images?: number;           // 1-4, default: 1
  seed?: number;                 // For reproducibility

  // Output options
  output_format?: "jpeg" | "png";
  enable_safety_checker?: boolean;

  // SDXL-specific
  negative_prompt?: string;

  // FLUX 2 Pro specific
  safety_tolerance?: string;     // "1" to "6"
  raw?: boolean;                 // Disable prompt enhancement

  // LoRA specific
  loras?: Array<{
    path: string;
    scale: number;
  }>;
}
```

### Response Structure

```typescript
interface TextToImageOutput {
  images: Array<{
    url: string;
    width: number;
    height: number;
    content_type: string;
  }>;
  seed: number;
  prompt: string;
  has_nsfw_concepts?: boolean[];
  timings?: {
    inference: number;
  };
}
```

## Model Selection Guide

| Use Case | Recommended Model | Why |
|----------|-------------------|-----|
| Best quality | `fal-ai/flux-2-pro` | Latest model, prompt enhancement |
| Open source | `fal-ai/flux/dev` | 12B params, high quality |
| Fast iteration | `fal-ai/flux/schnell` | 4-step generation |
| Budget | `fal-ai/fast-sdxl` | Lower cost per image |
| Ultra-fast | `fal-ai/sdxl-turbo` | Single step |
| Custom styles | `fal-ai/flux-lora` | LoRA support |
| Text in images | `fal-ai/ideogram` | Typography focus |
| Design assets | `fal-ai/recraft-v3` | Vector-style output |
| Photorealistic | `fal-ai/flux-realism` | Realism optimized |

## Best Practices

### Prompt Engineering

**For FLUX models:**
- Be descriptive and specific
- Include style, lighting, composition
- FLUX 2 Pro auto-enhances prompts (use `raw: true` to disable)
- Guidance scale 3-4 works best

**For SDXL models:**
- Use negative prompts
- Higher guidance (7-12) for better prompt adherence
- Include quality keywords: "high quality, detailed, 8k"

### Quality vs Speed Trade-offs

```typescript
// Quality priority
const quality = await fal.subscribe("fal-ai/flux-2-pro", {
  input: {
    prompt: "...",
    num_inference_steps: 28,
    guidance_scale: 3.5
  }
});

// Speed priority
const fast = await fal.subscribe("fal-ai/flux/schnell", {
  input: {
    prompt: "...",
    num_inference_steps: 4
  }
});

// Balance
const balanced = await fal.subscribe("fal-ai/flux/dev", {
  input: {
    prompt: "...",
    num_inference_steps: 20,
    guidance_scale: 3.5
  }
});
```

### Batch Generation

```typescript
// Generate multiple variations
const result = await fal.subscribe("fal-ai/flux/dev", {
  input: {
    prompt: "A beautiful landscape",
    num_images: 4,
    seed: 42  // Same seed = similar outputs
  }
});

// Access all images
result.images.forEach((img, i) => {
  console.log(`Image ${i + 1}: ${img.url}`);
});
```

### Reproducibility

```typescript
// Use seed for reproducible results
const seed = 12345;

const result1 = await fal.subscribe("fal-ai/flux/dev", {
  input: { prompt: "A cat", seed }
});

const result2 = await fal.subscribe("fal-ai/flux/dev", {
  input: { prompt: "A cat", seed }
});

// result1 and result2 will be identical
```
