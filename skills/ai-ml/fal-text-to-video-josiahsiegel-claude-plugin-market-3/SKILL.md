---
name: fal-text-to-video
description: Complete fal.ai text-to-video system. PROACTIVELY activate for: (1) Kling 2.0/2.5/2.6 Pro video generation, (2) Sora 2 for creative videos, (3) LTX Video with audio, (4) Runway Gen-3 Turbo for fast iteration, (5) Luma Dream Machine, (6) Video duration and aspect ratio, (7) Motion prompt engineering, (8) Camera movement keywords. Provides: Model endpoints, quality tiers, prompt structure, duration options. Ensures cinematic video generation with proper motion description.
---

## Quick Reference

| Model | Endpoint | Duration | Audio | Speed |
|-------|----------|----------|-------|-------|
| Kling 2.6 Pro | `fal-ai/kling-video/v2.6/pro/text-to-video` | 5-10s | Yes | Slow |
| Sora 2 | `fal-ai/sora` | 5-20s | Optional | Slow |
| LTX-2 Pro | `fal-ai/ltx-2-pro` | 5s | Yes | Medium |
| Runway Turbo | `fal-ai/runway-gen3/turbo/text-to-video` | 5-10s | No | Fast |
| Luma | `fal-ai/luma-dream-machine` | 5s | No | Medium |

| Aspect Ratio | Value | Use Case |
|--------------|-------|----------|
| Landscape | `"16:9"` | Standard video |
| Portrait | `"9:16"` | Social/mobile |
| Square | `"1:1"` | Social posts |

| Prompt Structure | Example |
|------------------|---------|
| Subject + Action | "A woman walks" |
| + Setting | "through a forest" |
| + Style | "cinematic lighting" |
| + Camera | "tracking shot" |

## When to Use This Skill

Use for **text-to-video generation**:
- Creating videos from text descriptions
- Choosing models by quality/speed tier
- Crafting motion-oriented prompts
- Generating videos with native audio
- Preview workflow (fast) → Final (quality)

**Related skills:**
- For image-to-video: see `fal-image-to-video`
- For video editing: see `fal-video-to-video`
- For model comparison: see `fal-model-guide`

---

# fal.ai Text-to-Video Models

Complete reference for all text-to-video generation models on fal.ai.

## Kling Video Models

### Kling 2.0 Standard
**Endpoint:** `fal-ai/kling-video/v2.0/text-to-video`
**Best For:** Good quality, cost-effective

```typescript
import { fal } from "@fal-ai/client";

const result = await fal.subscribe("fal-ai/kling-video/v2.0/text-to-video", {
  input: {
    prompt: "A majestic eagle soaring over snow-capped mountains at golden hour, cinematic lighting",
    duration: "5",  // "5" or "10" seconds
    aspect_ratio: "16:9",
    negative_prompt: "blurry, distorted, low quality"
  }
});

console.log(result.video.url);
```

```python
import fal_client

result = fal_client.subscribe(
    "fal-ai/kling-video/v2.0/text-to-video",
    arguments={
        "prompt": "A majestic eagle soaring over mountains",
        "duration": "5",
        "aspect_ratio": "16:9",
        "negative_prompt": "blurry, distorted"
    }
)
print(result["video"]["url"])
```

### Kling 2.5 Pro
**Endpoint:** `fal-ai/kling-video/v2.5/pro/text-to-video`
**Best For:** Professional quality videos

```typescript
const result = await fal.subscribe("fal-ai/kling-video/v2.5/pro/text-to-video", {
  input: {
    prompt: "A luxury car driving through a mountain road, drone shot, cinematic",
    duration: "5",
    aspect_ratio: "16:9",
    negative_prompt: "shaky, amateur, blurry"
  }
});
```

### Kling 2.6 Pro (Latest)
**Endpoint:** `fal-ai/kling-video/v2.6/pro/text-to-video`
**Best For:** Highest quality with native audio generation

The latest Kling model with built-in audio generation.

```typescript
const result = await fal.subscribe("fal-ai/kling-video/v2.6/pro/text-to-video", {
  input: {
    prompt: "Ocean waves crashing on rocky cliffs at sunset, seagulls flying, ambient sounds",
    duration: "5",
    aspect_ratio: "16:9",
    negative_prompt: "static, boring, low quality"
  }
});

console.log(result.video.url);
console.log(result.audio?.url);  // Native audio included
```

**Kling Parameters:**

| Parameter | Type | Values | Description |
|-----------|------|--------|-------------|
| `prompt` | string | - | Video description |
| `duration` | string | "5", "10" | Duration in seconds |
| `aspect_ratio` | string | "16:9", "9:16", "1:1" | Video dimensions |
| `negative_prompt` | string | - | What to avoid |

## Sora 2

### Sora (OpenAI)
**Endpoint:** `fal-ai/sora`
**Best For:** Advanced, creative video generation

```typescript
const result = await fal.subscribe("fal-ai/sora", {
  input: {
    prompt: "A stylish woman walks down a Tokyo street filled with warm glowing neon and animated city signage. She wears a black leather jacket, a long red dress, and black boots. She carries a black purse. She wears sunglasses and red lipstick. She walks confidently. The street is damp and reflective, creating a mirror effect of the colorful lights.",
    duration: 10,
    aspect_ratio: "16:9",
    resolution: "1080p"
  }
});

console.log(result.video.url);
```

**Sora Parameters:**

| Parameter | Type | Values | Description |
|-----------|------|--------|-------------|
| `prompt` | string | - | Detailed video description |
| `duration` | number | 5-20 | Duration in seconds |
| `aspect_ratio` | string | "16:9", "9:16", "1:1" | Video dimensions |
| `resolution` | string | "720p", "1080p" | Output resolution |

## LTX Video Models

### LTX Video (Original)
**Endpoint:** `fal-ai/ltx-video`
**Best For:** Fast, efficient generation

```typescript
const result = await fal.subscribe("fal-ai/ltx-video", {
  input: {
    prompt: "A beautiful sunset over the ocean with gentle waves",
    negative_prompt: "low quality, blurry, distorted",
    num_inference_steps: 30,
    guidance_scale: 7.5,
    aspect_ratio: "16:9"
  }
});
```

### LTX Video v2
**Endpoint:** `fal-ai/ltx-video/v2`
**Best For:** Improved quality over v1

```typescript
const result = await fal.subscribe("fal-ai/ltx-video/v2", {
  input: {
    prompt: "A futuristic city with flying cars and neon lights",
    negative_prompt: "ugly, distorted",
    num_inference_steps: 35,
    guidance_scale: 7.0,
    resolution: "720p"
  }
});
```

### LTX-2 Pro
**Endpoint:** `fal-ai/ltx-2-pro`
**Best For:** High fidelity with audio support

```typescript
const result = await fal.subscribe("fal-ai/ltx-2-pro", {
  input: {
    prompt: "A jazz band performing in a dimly lit club, smooth music, intimate atmosphere",
    negative_prompt: "worst quality, inconsistent motion, blurry",
    num_inference_steps: 30,
    guidance_scale: 3.5,
    resolution: "720p",
    enable_audio: true  // Generate matching audio
  }
});

console.log(result.video.url);
console.log(result.audio?.url);  // Audio track if enabled
```

**LTX Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `prompt` | string | - | Video description |
| `negative_prompt` | string | - | What to avoid |
| `num_inference_steps` | number | 30 | Quality steps |
| `guidance_scale` | number | 7.5 | Prompt adherence |
| `resolution` | string | "720p" | "720p" or "480p" |
| `aspect_ratio` | string | "16:9" | Video dimensions |
| `enable_audio` | boolean | false | Generate audio (LTX-2 Pro) |

## Wan Video

### Wan v2.1 1.3B
**Endpoint:** `fal-ai/wan/v2.1/1.3b/text-to-video`
**Best For:** Lightweight, fast generation

```typescript
const result = await fal.subscribe("fal-ai/wan/v2.1/1.3b/text-to-video", {
  input: {
    prompt: "A cat playing with a ball of yarn, cute, playful",
    num_frames: 81,  // Number of frames
    resolution: "480p"
  }
});
```

### Wan v2.1 14B
**Endpoint:** `fal-ai/wan/v2.1/14b/text-to-video`
**Best For:** Higher quality, larger model

```typescript
const result = await fal.subscribe("fal-ai/wan/v2.1/14b/text-to-video", {
  input: {
    prompt: "A professional chef preparing sushi, precise movements, high-end restaurant",
    num_frames: 81,
    resolution: "720p"
  }
});
```

## MiniMax Video

### MiniMax Text-to-Video
**Endpoint:** `fal-ai/minimax-video/text-to-video`
**Best For:** Balanced quality and speed

```typescript
const result = await fal.subscribe("fal-ai/minimax-video/text-to-video", {
  input: {
    prompt: "A butterfly emerging from a cocoon, macro shot, nature documentary style",
    prompt_optimizer: true  // Enhance prompt automatically
  }
});
```

**MiniMax Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `prompt` | string | Video description |
| `prompt_optimizer` | boolean | Auto-enhance prompt |

## Runway Gen-3

### Runway Gen-3 Turbo
**Endpoint:** `fal-ai/runway-gen3/turbo/text-to-video`
**Best For:** Fast iteration, previews

```typescript
const result = await fal.subscribe("fal-ai/runway-gen3/turbo/text-to-video", {
  input: {
    prompt: "A dancer performing ballet in an empty theater, spotlight, graceful movements",
    duration: 5,
    ratio: "16:9"
  }
});
```

**Runway Parameters:**

| Parameter | Type | Values | Description |
|-----------|------|--------|-------------|
| `prompt` | string | - | Video description |
| `duration` | number | 5, 10 | Seconds |
| `ratio` | string | "16:9", "9:16", "1:1" | Aspect ratio |

## Luma Dream Machine

### Luma Text-to-Video
**Endpoint:** `fal-ai/luma-dream-machine`
**Best For:** Creative, artistic videos

```typescript
const result = await fal.subscribe("fal-ai/luma-dream-machine", {
  input: {
    prompt: "A magical forest with glowing mushrooms and fireflies at night",
    aspect_ratio: "16:9",
    loop: false
  }
});
```

**Luma Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `prompt` | string | Video description |
| `aspect_ratio` | string | "16:9", "9:16", "1:1" |
| `loop` | boolean | Create looping video |

## CogVideoX

### CogVideoX Text-to-Video
**Endpoint:** `fal-ai/cogvideox`
**Best For:** Open-source alternative

```typescript
const result = await fal.subscribe("fal-ai/cogvideox", {
  input: {
    prompt: "A timelapse of a flower blooming, from bud to full bloom",
    num_inference_steps: 50,
    guidance_scale: 6.0
  }
});
```

### CogVideoX-5B
**Endpoint:** `fal-ai/cogvideox-5b`
**Best For:** Higher quality open-source

```typescript
const result = await fal.subscribe("fal-ai/cogvideox-5b", {
  input: {
    prompt: "An astronaut floating in space with Earth in the background",
    num_inference_steps: 50,
    guidance_scale: 6.0,
    num_frames: 49
  }
});
```

## HunyuanVideo

### Hunyuan Video
**Endpoint:** `fal-ai/hunyuan-video`
**Best For:** Chinese model, good quality

```typescript
const result = await fal.subscribe("fal-ai/hunyuan-video", {
  input: {
    prompt: "A traditional Chinese dragon dance during festival celebration",
    num_inference_steps: 50,
    guidance_scale: 6.0
  }
});
```

## Model Comparison

### Quality Rankings

| Tier | Models | Quality | Speed | Cost |
|------|--------|---------|-------|------|
| Premium | Kling 2.6 Pro, Sora 2 | Highest | Slow | $$$ |
| Professional | Kling 2.5 Pro, LTX-2 Pro | High | Medium | $$ |
| Standard | Kling 2.0, Runway Turbo | Good | Fast | $ |
| Budget | LTX v1, CogVideoX | Acceptable | Fast | $ |

### Feature Comparison

| Model | Audio | Duration | Resolution | Best Use |
|-------|-------|----------|------------|----------|
| Kling 2.6 Pro | Native | 5-10s | 1080p | Cinematic |
| Sora 2 | Optional | 5-20s | 1080p | Creative |
| LTX-2 Pro | Yes | 5s | 720p | Fast HQ |
| Runway Turbo | No | 5-10s | 720p | Iteration |
| MiniMax | No | 6s | 720p | Balanced |
| Luma | No | 5s | 720p | Artistic |

### Speed Comparison (approximate)

| Model | ~Generation Time (5s video) |
|-------|-----------------------------|
| Runway Gen-3 Turbo | 30-60s |
| LTX Video | 45-90s |
| MiniMax | 60-120s |
| Kling 2.5 Pro | 120-180s |
| Kling 2.6 Pro | 150-240s |
| Sora 2 | 180-300s |

## Prompt Engineering for Video

### Structure Your Prompts

```
[Subject] + [Action] + [Setting] + [Style] + [Camera/Technical]
```

**Examples:**

```typescript
// Good: Specific, action-oriented
"A golden retriever running through autumn leaves in a forest, slow motion, cinematic, warm lighting, tracking shot"

// Bad: Vague, static
"A dog in a forest"
```

### Motion Keywords

| Keyword | Effect |
|---------|--------|
| "walking", "running", "jumping" | Subject movement |
| "slow motion", "timelapse" | Speed modification |
| "tracking shot", "pan", "zoom" | Camera movement |
| "floating", "flying", "falling" | Spatial movement |
| "dancing", "spinning", "waving" | Rhythmic movement |

### Style Keywords

| Keyword | Effect |
|---------|--------|
| "cinematic" | Movie-like quality |
| "documentary" | Realistic style |
| "anime" | Animated style |
| "noir" | Dark, contrasty |
| "vibrant" | Saturated colors |

### Camera Movements

| Term | Description |
|------|-------------|
| "tracking shot" | Camera follows subject |
| "pan left/right" | Horizontal camera sweep |
| "tilt up/down" | Vertical camera sweep |
| "zoom in/out" | Focal length change |
| "drone shot" | Aerial perspective |
| "POV shot" | First-person view |
| "dolly shot" | Camera moves on track |

## Complete Parameter Reference

```typescript
interface TextToVideoInput {
  // Required
  prompt: string;

  // Duration (varies by model)
  duration?: number | string;  // seconds

  // Dimensions
  aspect_ratio?: "16:9" | "9:16" | "1:1" | "4:3" | "21:9";
  resolution?: "480p" | "720p" | "1080p";

  // Quality control
  negative_prompt?: string;
  num_inference_steps?: number;
  guidance_scale?: number;

  // Reproducibility
  seed?: number;

  // Model-specific
  prompt_optimizer?: boolean;  // MiniMax
  enable_audio?: boolean;      // LTX-2 Pro, Kling 2.6
  loop?: boolean;              // Luma
  num_frames?: number;         // Wan, CogVideoX
}
```

## Workflow Examples

### Production Workflow

```typescript
// 1. Fast preview with Runway Turbo
const preview = await fal.subscribe("fal-ai/runway-gen3/turbo/text-to-video", {
  input: {
    prompt: "A woman walking through a rainy city street at night",
    duration: 5,
    ratio: "16:9"
  }
});

console.log("Preview:", preview.video.url);
// Review and refine prompt...

// 2. Final render with Kling Pro
const final = await fal.subscribe("fal-ai/kling-video/v2.6/pro/text-to-video", {
  input: {
    prompt: "A stylish woman walking confidently through a rainy Tokyo street at night, neon reflections on wet pavement, cinematic lighting, slow motion, tracking shot",
    duration: "10",
    aspect_ratio: "16:9"
  }
});

console.log("Final:", final.video.url);
```

### Batch Generation

```typescript
const prompts = [
  "A sunrise over mountains",
  "A sunset over the ocean",
  "A storm rolling in"
];

const videos = await Promise.all(
  prompts.map(prompt =>
    fal.subscribe("fal-ai/ltx-video", {
      input: { prompt, aspect_ratio: "16:9" }
    })
  )
);

videos.forEach((v, i) => console.log(`Video ${i + 1}: ${v.video.url}`));
```

## Best Practices

1. **Use `subscribe()` not `run()`** - Video generation takes time
2. **Start with previews** - Use faster models to iterate on prompts
3. **Be specific about motion** - Describe what moves and how
4. **Include camera direction** - Guide the visual perspective
5. **Use negative prompts** - Avoid common artifacts
6. **Match model to need** - Don't use premium for tests
7. **Include audio keywords** - For models that support audio generation
