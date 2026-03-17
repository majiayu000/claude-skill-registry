---
name: fal-image-to-video
description: Complete fal.ai image-to-video system. PROACTIVELY activate for: (1) Kling 2.5/2.6 Pro image animation, (2) MiniMax Hailuo with prompt optimizer, (3) LTX image-to-video, (4) Runway Gen-3 Turbo, (5) Luma Dream Machine with loop, (6) Stable Video Diffusion, (7) Motion description prompts, (8) Portrait/product animation workflows. Provides: Model endpoints, motion keywords, animation techniques, workflow examples. Ensures natural image animation with proper motion description.
---

## Quick Reference

| Model | Endpoint | Audio | Loop | Best For |
|-------|----------|-------|------|----------|
| Kling 2.6 Pro | `fal-ai/kling-video/v2.6/pro/image-to-video` | Yes | No | Cinematic |
| MiniMax | `fal-ai/minimax-video/image-to-video` | No | No | Reliable |
| Luma | `fal-ai/luma-dream-machine` | No | Yes | Creative |
| SVD | `fal-ai/stable-video-diffusion` | No | No | Fast test |

| Motion Type | Keywords | Example |
|-------------|----------|---------|
| Character | walks, turns, smiles | "She slowly turns her head" |
| Nature | sways, flows, falls | "Leaves flutter in the wind" |
| Camera | pans, zooms, tracks | "Camera slowly pans right" |

| Use Case | Recommended Model |
|----------|-------------------|
| Portraits | Kling 2.5/2.6 Pro |
| Products | MiniMax (optimizer) |
| Landscapes | Luma (loop) |
| Fast testing | SVD, Runway Turbo |

## When to Use This Skill

Use for **image animation**:
- Animating still portraits with natural motion
- Creating product showcase videos
- Generating ambient loop videos
- Adding subtle motion to landscapes
- Preview workflow before final render

**Related skills:**
- For text-to-video: see `fal-text-to-video`
- For video editing: see `fal-video-to-video`
- For text-to-image first: see `fal-text-to-image`

---

# fal.ai Image-to-Video Models

Complete reference for all image animation and image-to-video models on fal.ai.

## Kling Image-to-Video

### Kling 2.0 Image-to-Video
**Endpoint:** `fal-ai/kling-video/v2.0/image-to-video`
**Best For:** Standard image animation

```typescript
import { fal } from "@fal-ai/client";

const result = await fal.subscribe("fal-ai/kling-video/v2.0/image-to-video", {
  input: {
    prompt: "The person slowly turns their head and smiles warmly",
    image_url: "https://example.com/portrait.jpg",
    duration: "5",
    aspect_ratio: "16:9"
  }
});

console.log(result.video.url);
```

```python
import fal_client

result = fal_client.subscribe(
    "fal-ai/kling-video/v2.0/image-to-video",
    arguments={
        "prompt": "The person slowly turns their head and smiles",
        "image_url": "https://example.com/portrait.jpg",
        "duration": "5",
        "aspect_ratio": "16:9"
    }
)
print(result["video"]["url"])
```

### Kling 2.5 Pro Image-to-Video
**Endpoint:** `fal-ai/kling-video/v2.5/pro/image-to-video`
**Best For:** Professional quality animation

```typescript
const result = await fal.subscribe("fal-ai/kling-video/v2.5/pro/image-to-video", {
  input: {
    prompt: "The car drives forward along the mountain road, camera follows",
    image_url: "https://example.com/car-scene.jpg",
    duration: "5",
    aspect_ratio: "16:9",
    negative_prompt: "static, frozen, distorted"
  }
});
```

### Kling 2.6 Pro Image-to-Video (Latest)
**Endpoint:** `fal-ai/kling-video/v2.6/pro/image-to-video`
**Best For:** Highest quality with native audio

```typescript
const result = await fal.subscribe("fal-ai/kling-video/v2.6/pro/image-to-video", {
  input: {
    prompt: "The waterfall cascades down with a gentle roar, birds fly past",
    image_url: "https://example.com/waterfall.jpg",
    duration: "5",
    aspect_ratio: "16:9"
  }
});

console.log(result.video.url);
console.log(result.audio?.url);  // Native audio
```

**Kling Parameters:**

| Parameter | Type | Values | Description |
|-----------|------|--------|-------------|
| `prompt` | string | - | Motion description |
| `image_url` | string | - | Source image URL |
| `duration` | string | "5", "10" | Duration in seconds |
| `aspect_ratio` | string | "16:9", "9:16", "1:1" | Output dimensions |
| `negative_prompt` | string | - | What to avoid |

## MiniMax Image-to-Video

### MiniMax Hailuo
**Endpoint:** `fal-ai/minimax-video/image-to-video`
**Best For:** Reliable image animation with prompt optimization

```typescript
const result = await fal.subscribe("fal-ai/minimax-video/image-to-video", {
  input: {
    prompt: "The cat stretches and yawns, then walks forward",
    image_url: "https://example.com/sleeping-cat.jpg",
    prompt_optimizer: true  // Auto-enhance prompt
  }
});
```

```python
result = fal_client.subscribe(
    "fal-ai/minimax-video/image-to-video",
    arguments={
        "prompt": "The cat stretches and yawns",
        "image_url": "https://example.com/cat.jpg",
        "prompt_optimizer": True
    }
)
```

**MiniMax Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `prompt` | string | Motion description |
| `image_url` | string | Source image URL |
| `prompt_optimizer` | boolean | Auto-enhance prompt |

## LTX Image-to-Video

### LTX Video Image-to-Video
**Endpoint:** `fal-ai/ltx-video/image-to-video`
**Best For:** Fast image animation

```typescript
const result = await fal.subscribe("fal-ai/ltx-video/image-to-video", {
  input: {
    prompt: "The flowers sway gently in the breeze",
    image_url: "https://example.com/flower-field.jpg",
    negative_prompt: "static, frozen",
    num_inference_steps: 30,
    guidance_scale: 7.5
  }
});
```

### LTX Video v2 Image-to-Video
**Endpoint:** `fal-ai/ltx-video/v2/image-to-video`
**Best For:** Improved quality animation

```typescript
const result = await fal.subscribe("fal-ai/ltx-video/v2/image-to-video", {
  input: {
    prompt: "Smoke rises and swirls from the chimney",
    image_url: "https://example.com/cabin.jpg",
    num_inference_steps: 35,
    guidance_scale: 7.0
  }
});
```

**LTX Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `prompt` | string | - | Motion description |
| `image_url` | string | - | Source image |
| `negative_prompt` | string | - | What to avoid |
| `num_inference_steps` | number | 30 | Quality steps |
| `guidance_scale` | number | 7.5 | Prompt adherence |

## Runway Gen-3 Image-to-Video

### Runway Gen-3 Turbo
**Endpoint:** `fal-ai/runway-gen3/turbo/image-to-video`
**Best For:** Fast iteration, previews

```typescript
const result = await fal.subscribe("fal-ai/runway-gen3/turbo/image-to-video", {
  input: {
    prompt: "The model walks confidently down the runway",
    image_url: "https://example.com/fashion-shot.jpg",
    duration: 5
  }
});
```

**Runway Parameters:**

| Parameter | Type | Values | Description |
|-----------|------|--------|-------------|
| `prompt` | string | - | Motion description |
| `image_url` | string | - | Source image |
| `duration` | number | 5, 10 | Seconds |

## Luma Dream Machine

### Luma Image-to-Video
**Endpoint:** `fal-ai/luma-dream-machine`
**Best For:** Creative, artistic animation

```typescript
const result = await fal.subscribe("fal-ai/luma-dream-machine", {
  input: {
    prompt: "The magical portal opens with swirling energy",
    image_url: "https://example.com/fantasy-scene.jpg",
    aspect_ratio: "16:9",
    loop: true  // Create seamless loop
  }
});
```

```python
result = fal_client.subscribe(
    "fal-ai/luma-dream-machine",
    arguments={
        "prompt": "The portal opens with swirling energy",
        "image_url": "https://example.com/scene.jpg",
        "aspect_ratio": "16:9",
        "loop": True
    }
)
```

**Luma Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `prompt` | string | Motion description |
| `image_url` | string | Source image |
| `aspect_ratio` | string | "16:9", "9:16", "1:1" |
| `loop` | boolean | Create looping video |

## Wan Image-to-Video

### Wan v2.1 Image-to-Video
**Endpoint:** `fal-ai/wan/v2.1/1.3b/image-to-video`
**Best For:** Lightweight animation

```typescript
const result = await fal.subscribe("fal-ai/wan/v2.1/1.3b/image-to-video", {
  input: {
    prompt: "The leaves flutter and fall from the tree",
    image_url: "https://example.com/autumn-tree.jpg",
    num_frames: 81
  }
});
```

## Stable Video Diffusion

### SVD Image-to-Video
**Endpoint:** `fal-ai/stable-video-diffusion`
**Best For:** Open-source image animation

```typescript
const result = await fal.subscribe("fal-ai/stable-video-diffusion", {
  input: {
    image_url: "https://example.com/landscape.jpg",
    motion_bucket_id: 127,  // 0-255, higher = more motion
    fps: 7,
    num_frames: 25
  }
});
```

**SVD Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `image_url` | string | - | Source image |
| `motion_bucket_id` | number | 127 | Motion intensity (0-255) |
| `fps` | number | 7 | Frames per second |
| `num_frames` | number | 25 | Total frames |
| `seed` | number | - | For reproducibility |

### SVD XT
**Endpoint:** `fal-ai/stable-video-diffusion-xt`
**Best For:** Extended video length

```typescript
const result = await fal.subscribe("fal-ai/stable-video-diffusion-xt", {
  input: {
    image_url: "https://example.com/scene.jpg",
    motion_bucket_id: 127,
    num_frames: 25,
    fps: 6
  }
});
```

## CogVideoX Image-to-Video

### CogVideoX-5B Image-to-Video
**Endpoint:** `fal-ai/cogvideox-5b/image-to-video`
**Best For:** Open-source alternative

```typescript
const result = await fal.subscribe("fal-ai/cogvideox-5b/image-to-video", {
  input: {
    prompt: "The astronaut waves to the camera",
    image_url: "https://example.com/astronaut.jpg",
    num_inference_steps: 50,
    guidance_scale: 6.0
  }
});
```

## Model Comparison

### Quality Ranking

| Tier | Models | Quality | Speed |
|------|--------|---------|-------|
| Premium | Kling 2.6 Pro | Highest | Slow |
| Professional | Kling 2.5 Pro, Runway | High | Medium |
| Standard | MiniMax, LTX v2 | Good | Fast |
| Budget | SVD, CogVideoX | Acceptable | Fast |

### Feature Comparison

| Model | Audio | Duration | Loop | Best For |
|-------|-------|----------|------|----------|
| Kling 2.6 Pro | Yes | 5-10s | No | Cinematic |
| Kling 2.5 Pro | No | 5-10s | No | Professional |
| MiniMax | No | 6s | No | Reliable |
| Runway Turbo | No | 5-10s | No | Fast |
| Luma | No | 5s | Yes | Creative |
| SVD | No | 3-4s | No | Open source |

## Prompt Engineering for Image Animation

### Motion Description Structure

```
[Subject action] + [Motion quality] + [Camera movement] + [Atmosphere]
```

**Examples:**

```typescript
// Good: Specific motion
"The woman slowly turns her head to the right and smiles, gentle breeze moves her hair"

// Bad: Vague
"The woman moves"
```

### Motion Types

| Type | Keywords | Example |
|------|----------|---------|
| Character | "walks", "runs", "dances", "gestures" | "She waves hello" |
| Nature | "sways", "flows", "rustles", "falls" | "Leaves fall gently" |
| Mechanical | "rotates", "spins", "moves", "opens" | "The door opens slowly" |
| Atmospheric | "drifts", "swirls", "rises", "disperses" | "Fog drifts across" |

### Camera Motion Keywords

| Keyword | Effect |
|---------|--------|
| "camera slowly pans" | Horizontal sweep |
| "slight zoom in" | Gradual zoom |
| "tracking shot" | Follows subject |
| "static camera" | No camera movement |
| "subtle camera shake" | Handheld feel |

### Quality Modifiers

- "smooth motion"
- "natural movement"
- "fluid animation"
- "subtle motion"
- "cinematic"

## Complete Parameter Reference

```typescript
interface ImageToVideoInput {
  // Required
  prompt: string;
  image_url: string;

  // Duration (varies by model)
  duration?: number | string;

  // Dimensions
  aspect_ratio?: "16:9" | "9:16" | "1:1";

  // Quality
  negative_prompt?: string;
  num_inference_steps?: number;
  guidance_scale?: number;

  // Model-specific
  prompt_optimizer?: boolean;  // MiniMax
  loop?: boolean;              // Luma
  motion_bucket_id?: number;   // SVD (0-255)
  fps?: number;                // SVD
  num_frames?: number;         // SVD, Wan

  // Reproducibility
  seed?: number;
}
```

## Workflow Examples

### Portrait Animation Pipeline

```typescript
// 1. Generate a portrait image
const portrait = await fal.subscribe("fal-ai/flux/dev", {
  input: {
    prompt: "Professional headshot of a business woman, neutral expression, studio lighting",
    image_size: "portrait_4_3"
  }
});

// 2. Animate the portrait
const video = await fal.subscribe("fal-ai/kling-video/v2.5/pro/image-to-video", {
  input: {
    prompt: "She slowly turns her head, makes eye contact with camera, and gives a warm professional smile",
    image_url: portrait.images[0].url,
    duration: "5",
    aspect_ratio: "16:9"
  }
});

console.log(video.video.url);
```

### Product Showcase

```typescript
// Animate product image
const result = await fal.subscribe("fal-ai/minimax-video/image-to-video", {
  input: {
    prompt: "The camera slowly rotates around the product, highlighting details, studio lighting",
    image_url: "https://example.com/product-shot.jpg",
    prompt_optimizer: true
  }
});
```

### Nature Scene

```typescript
// Create ambient nature video
const result = await fal.subscribe("fal-ai/luma-dream-machine", {
  input: {
    prompt: "Gentle breeze moves through the grass, clouds drift slowly overhead, peaceful ambient motion",
    image_url: "https://example.com/landscape.jpg",
    aspect_ratio: "16:9",
    loop: true  // Perfect for background video
  }
});
```

### Fast Preview Workflow

```typescript
// Quick preview with faster model
const preview = await fal.subscribe("fal-ai/stable-video-diffusion", {
  input: {
    image_url: sourceImage,
    motion_bucket_id: 100
  }
});

console.log("Preview:", preview.video.url);

// If satisfied, use higher quality model
const final = await fal.subscribe("fal-ai/kling-video/v2.6/pro/image-to-video", {
  input: {
    prompt: "Refined motion description based on preview",
    image_url: sourceImage,
    duration: "5"
  }
});
```

## Best Practices

### Image Preparation

1. **High Resolution**: Use high-quality source images
2. **Clear Subject**: Ensure main subject is clearly visible
3. **Proper Framing**: Leave room for motion
4. **Consistent Lighting**: Avoid harsh shadows

### Prompt Tips

1. **Describe the motion**, not the static scene
2. **Be specific** about direction (left, right, forward)
3. **Include speed** (slowly, quickly, gradually)
4. **Match motion to image** content

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Static output | Vague prompt | Add specific motion verbs |
| Distorted faces | Fast motion | Use "subtle", "gentle" |
| Inconsistent motion | Complex scene | Focus on one element |
| Cut-off motion | Short duration | Extend duration if available |

### Model Selection

| Use Case | Recommended Model |
|----------|-------------------|
| Portraits | Kling 2.5/2.6 Pro |
| Products | MiniMax (prompt optimizer) |
| Landscapes | Luma (loop option) |
| Fast testing | SVD, Runway Turbo |
| With audio | Kling 2.6 Pro |
