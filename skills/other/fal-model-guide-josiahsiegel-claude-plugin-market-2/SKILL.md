---
name: fal-model-guide
description: Complete fal.ai model selection system. PROACTIVELY activate for: (1) Choosing image generation models (FLUX, SDXL), (2) Choosing video models (Kling, Sora, LTX), (3) Choosing audio models (Whisper, ElevenLabs), (4) Model quality vs speed comparison, (5) Cost optimization by model tier, (6) 3D generation models, (7) Model-specific parameters, (8) Development vs production model selection. Provides: Model comparison tables, decision trees, pricing tiers, performance benchmarks. Ensures optimal model selection for quality, speed, and cost.
---

## Quick Reference

| Category | Fast/Cheap | Balanced | Best Quality |
|----------|------------|----------|--------------|
| Image | FLUX Schnell | FLUX.1 Dev | FLUX.2 Pro |
| Video | Runway Turbo | LTX-2 Pro | Kling 2.6 Pro |
| Audio STT | Whisper Turbo | Whisper | Whisper Large v3 |
| Audio TTS | Kokoro | XTTS | ElevenLabs |

| FLUX Model | Endpoint | Steps | Use Case |
|------------|----------|-------|----------|
| FLUX.2 Pro | `fal-ai/flux-2-pro` | 28 | Production |
| FLUX.1 Dev | `fal-ai/flux/dev` | 28 | High quality |
| FLUX Schnell | `fal-ai/flux/schnell` | 4 | Fast iteration |

| Video Model | Duration | Audio | Speed |
|-------------|----------|-------|-------|
| Kling 2.6 Pro | 5-10s | Yes | Slow |
| LTX-2 Pro | 5s | Yes | Medium |
| Runway Turbo | 5-10s | No | Fast |

## When to Use This Skill

Use for **model selection decisions**:
- Comparing FLUX vs SDXL for image generation
- Choosing video models by quality tier
- Optimizing costs with appropriate model selection
- Understanding model-specific parameters
- Building production vs development pipelines

**Related skills:**
- For text-to-image: see `fal-text-to-image`
- For text-to-video: see `fal-text-to-video`
- For audio models: see `fal-audio`

---

# fal.ai Model Selection Guide

Comprehensive guide to selecting the right fal.ai model for your use case.

## Image Generation Models

### FLUX Family

| Model | Endpoint | Best For | Speed | Quality | Cost |
|-------|----------|----------|-------|---------|------|
| FLUX.2 [pro] | `fal-ai/flux-2-pro` | Production, best quality | Medium | Highest | $$$ |
| FLUX.1 [dev] | `fal-ai/flux/dev` | High quality, open-source | Medium | High | $$ |
| FLUX Schnell | `fal-ai/flux/schnell` | Fast iteration | Fast | Good | $ |
| FLUX LoRA | `fal-ai/flux-lora` | Custom trained styles | Medium | High | $$ |
| FLUX Realism | `fal-ai/flux-realism` | Photorealistic images | Medium | High | $$ |

**FLUX.2 Pro** - Latest and best quality
```typescript
const result = await fal.subscribe("fal-ai/flux-2-pro", {
  input: {
    prompt: "Professional product photo of a watch",
    image_size: "square_hd",
    num_inference_steps: 28,
    guidance_scale: 3.5
  }
});
```

**FLUX.1 Dev** - Best open-source option
```typescript
const result = await fal.subscribe("fal-ai/flux/dev", {
  input: {
    prompt: "A serene mountain landscape",
    image_size: "landscape_16_9",
    num_inference_steps: 28
  }
});
```

**FLUX Schnell** - Fast 4-step generation
```typescript
const result = await fal.subscribe("fal-ai/flux/schnell", {
  input: {
    prompt: "Quick concept sketch",
    num_inference_steps: 4  // Optimized for 4 steps
  }
});
```

### Stable Diffusion Models

| Model | Endpoint | Best For |
|-------|----------|----------|
| Fast SDXL | `fal-ai/fast-sdxl` | Speed, lower cost |
| SDXL | `fal-ai/stable-diffusion-xl` | Classic SDXL |
| SD 1.5 | `fal-ai/stable-diffusion-v15` | Legacy compatibility |
| SDXL Turbo | `fal-ai/sdxl-turbo` | Ultra-fast |

```typescript
// Fast SDXL - Good balance of speed and quality
const result = await fal.subscribe("fal-ai/fast-sdxl", {
  input: {
    prompt: "A colorful abstract painting",
    image_size: "square_hd",
    num_inference_steps: 25
  }
});
```

### Specialized Image Models

| Model | Endpoint | Use Case |
|-------|----------|----------|
| Recraft V3 | `fal-ai/recraft-v3` | Design assets, vectors |
| Ideogram | `fal-ai/ideogram` | Text in images |
| Playground v2.5 | `fal-ai/playground-v25` | Creative/artistic |
| Kandinsky 3 | `fal-ai/kandinsky-3` | Russian model |

### Image-to-Image Models

| Model | Endpoint | Use Case |
|-------|----------|----------|
| FLUX i2i | `fal-ai/flux/dev/image-to-image` | Transform images |
| FLUX Inpaint | `fal-ai/flux/dev/inpainting` | Edit regions |
| FLUX ControlNet | `fal-ai/flux/dev/controlnet` | Guided generation |
| IP-Adapter | `fal-ai/ip-adapter-flux` | Style transfer |

```typescript
// Image-to-Image transformation
const result = await fal.subscribe("fal-ai/flux/dev/image-to-image", {
  input: {
    image_url: "https://example.com/photo.jpg",
    prompt: "Transform into watercolor painting style",
    strength: 0.75  // 0-1, how much to change
  }
});

// Inpainting (edit specific regions)
const result = await fal.subscribe("fal-ai/flux/dev/inpainting", {
  input: {
    image_url: "https://example.com/photo.jpg",
    mask_url: "https://example.com/mask.png",
    prompt: "A golden retriever"
  }
});

// ControlNet (structural guidance)
const result = await fal.subscribe("fal-ai/flux/dev/controlnet", {
  input: {
    prompt: "Modern house design",
    control_image_url: "https://example.com/edges.png",
    controlnet_conditioning_scale: 0.8
  }
});
```

## Video Generation Models

### Text-to-Video

| Model | Endpoint | Quality | Duration | Audio | Best For |
|-------|----------|---------|----------|-------|----------|
| Kling 2.6 Pro | `fal-ai/kling-video/v2.6/pro` | Highest | 5-10s | Native | Cinematic |
| Sora 2 | `fal-ai/sora` | Highest | 5-20s | Optional | Advanced |
| LTX-2 Pro | `fal-ai/ltx-video-2-pro` | High | 5s | Yes | Fast HQ |
| Runway Gen-3 | `fal-ai/runway/gen3/turbo` | High | 5-10s | No | Fast |
| Luma | `fal-ai/luma-dream-machine` | Good | 5s | No | Creative |
| CogVideoX | `fal-ai/cogvideox` | Good | 6s | No | Open source |

**Kling 2.6 Pro** - Best overall quality
```typescript
const result = await fal.subscribe("fal-ai/kling-video/v2.6/pro", {
  input: {
    prompt: "A majestic eagle soaring over mountains at golden hour",
    duration: 5,
    aspect_ratio: "16:9",
    negative_prompt: "blurry, distorted",
    cfg_scale: 0.5
  }
});
```

**LTX-2 Pro** - Fast with audio
```typescript
const result = await fal.subscribe("fal-ai/ltx-video-2-pro", {
  input: {
    prompt: "Ocean waves crashing on rocks",
    resolution: "720p",
    enable_audio: true
  }
});
```

### Image-to-Video

| Model | Endpoint | Best For |
|-------|----------|----------|
| MiniMax Hailuo | `fal-ai/minimax/video-01` | Image animation |
| Kling i2v | `fal-ai/kling-video/v2.6/pro/image-to-video` | HQ animation |
| Luma i2v | `fal-ai/luma-dream-machine` | Creative |
| Runway i2v | `fal-ai/runway/gen3/turbo/image-to-video` | Fast |

```typescript
// Animate a still image
const result = await fal.subscribe("fal-ai/minimax/video-01", {
  input: {
    image_url: "https://example.com/portrait.jpg",
    prompt: "Person slowly turns head and smiles",
    prompt_optimizer: true
  }
});
```

### Video-to-Video (Editing)

```typescript
// Edit/transform existing video
const result = await fal.subscribe("fal-ai/kling-video/o1", {
  input: {
    video_url: "https://example.com/video.mp4",
    prompt: "Change to anime style"
  }
});
```

## Audio Models

### Speech-to-Text

| Model | Endpoint | Best For |
|-------|----------|----------|
| Whisper | `fal-ai/whisper` | Accurate transcription |
| Whisper Turbo | `fal-ai/whisper-turbo` | Fast transcription |

```typescript
const result = await fal.subscribe("fal-ai/whisper", {
  input: {
    audio_url: "https://example.com/speech.mp3",
    task: "transcribe",  // or "translate"
    language: "en",
    chunk_level: "segment"
  }
});

console.log(result.text);
console.log(result.chunks);  // With timestamps
```

### Text-to-Speech

| Model | Endpoint | Best For |
|-------|----------|----------|
| Elevenlabs | `fal-ai/elevenlabs` | Premium voices |
| F5-TTS | `fal-ai/f5-tts` | Voice cloning |
| Kokoro | `fal-ai/kokoro` | Multi-language |

```typescript
// Text-to-speech with Elevenlabs
const result = await fal.subscribe("fal-ai/elevenlabs", {
  input: {
    text: "Hello, welcome to our service.",
    voice_id: "voice_id_here"
  }
});
```

## 3D Generation Models

| Model | Endpoint | Use Case |
|-------|----------|----------|
| TripoSR | `fal-ai/triposr` | Image to 3D mesh |
| InstantMesh | `fal-ai/instantmesh` | Fast 3D generation |
| Stable Zero123 | `fal-ai/stable-zero123` | Novel view synthesis |

```typescript
// Generate 3D mesh from image
const result = await fal.subscribe("fal-ai/triposr", {
  input: {
    image_url: "https://example.com/object.jpg"
  }
});

console.log(result.model_mesh.url);  // GLB/OBJ file
```

## Model Selection Decision Tree

```
What do you want to create?
├── Image
│   ├── From text only?
│   │   ├── Need best quality? → FLUX.2 Pro
│   │   ├── Need fast iteration? → FLUX Schnell
│   │   ├── Need open-source? → FLUX.1 Dev
│   │   └── Budget conscious? → Fast SDXL
│   ├── Transform existing image?
│   │   ├── Style transfer → FLUX i2i
│   │   ├── Edit specific region → FLUX Inpainting
│   │   └── Follow structure → FLUX ControlNet
│   └── Need text in image? → Ideogram
│
├── Video
│   ├── From text only?
│   │   ├── Need best quality? → Kling 2.6 Pro
│   │   ├── Need fast preview? → Runway Gen-3 Turbo
│   │   └── Need audio? → LTX-2 Pro or Kling
│   ├── Animate image? → MiniMax Hailuo
│   └── Edit video? → Kling O1
│
├── Audio
│   ├── Speech to text?
│   │   ├── Accurate → Whisper
│   │   └── Fast → Whisper Turbo
│   └── Text to speech? → Elevenlabs / F5-TTS
│
└── 3D
    └── Image to 3D? → TripoSR
```

## Performance Comparison

### Image Generation Speed

| Model | ~Time (1024x1024) |
|-------|-------------------|
| FLUX Schnell | 1-2s |
| Fast SDXL | 2-3s |
| FLUX.1 Dev | 5-8s |
| FLUX.2 Pro | 8-12s |

### Video Generation Speed

| Model | ~Time (5s video) |
|-------|------------------|
| Runway Gen-3 Turbo | 30-60s |
| LTX-2 Pro | 60-90s |
| Kling 2.6 Pro | 120-180s |

## Cost Optimization Strategies

1. **Development Phase**
   - Use FLUX Schnell for prompt iteration
   - Use Fast SDXL for quick tests
   - Use Runway Gen-3 Turbo for video previews

2. **Production Phase**
   - FLUX.2 Pro for final images
   - Kling 2.6 Pro for final videos

3. **Batch Processing**
   - Process during off-peak hours
   - Use appropriate image sizes (don't upscale unnecessarily)
   - Cache results by seed for reproducibility

4. **Resource Efficiency**
   - Generate at target resolution (don't generate larger and downscale)
   - Use webhooks for high-volume (avoid polling overhead)
   - Implement client-side caching

## Model-Specific Tips

### FLUX Tips
- Guidance scale 3-4 works best
- 28 steps is optimal default
- Schnell works best with 4 steps only
- Detailed prompts produce better results

### Video Tips
- Include camera movement in prompts
- Describe action/motion explicitly
- Use negative prompts to avoid artifacts
- Start with shorter duration for testing

### Whisper Tips
- Provide language hint for better accuracy
- Use "translate" task for non-English to English
- chunk_level="segment" gives timestamps

## Explore More Models

Visit https://fal.ai/models for the complete catalog of 600+ models including:
- Face restoration/enhancement
- Background removal
- Upscaling
- Style transfer
- OCR
- Object detection
- And many more specialized models
