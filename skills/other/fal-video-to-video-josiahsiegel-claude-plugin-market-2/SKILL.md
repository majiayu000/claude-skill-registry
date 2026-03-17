---
name: fal-video-to-video
description: Complete fal.ai video-to-video system. PROACTIVELY activate for: (1) Kling O1 video editing, (2) Sora Remix transformation, (3) Video upscaling, (4) Frame interpolation, (5) Style transfer (anime, painting), (6) Object replacement/removal, (7) Color correction, (8) Video enhancement pipelines. Provides: Edit types (general/style/object), upscaling options, style keywords, enhancement workflows. Ensures consistent video transformation without flickering.
---

## Quick Reference

| Task | Endpoint | Key Parameter |
|------|----------|---------------|
| Style/Edit | `fal-ai/kling-video/o1/video-to-video/edit` | `edit_type` |
| Remix | `fal-ai/sora/remix` | `prompt` |
| Upscale | `fal-ai/video-upscaler` | `scale: 2,4` |
| Interpolate | `fal-ai/frame-interpolation` | `target_fps` |

| Edit Type | Use Case |
|-----------|----------|
| `general` | Color, lighting, quality |
| `style` | Anime, painting, noir |
| `object` | Replace/remove elements |

| Style Keyword | Effect |
|---------------|--------|
| "anime style" | Japanese animation |
| "oil painting" | Textured brushstrokes |
| "noir" | High contrast B&W |
| "cyberpunk" | Neon futuristic |

| Upscale | Size Impact |
|---------|-------------|
| 2x | 4x file size |
| 4x | 16x file size |

## When to Use This Skill

Use for **video editing and transformation**:
- Applying style transfer to videos
- Upscaling low-resolution videos
- Increasing frame rate for smooth motion
- Replacing or removing objects
- Enhancing video quality

**Related skills:**
- For text-to-video: see `fal-text-to-video`
- For image-to-video: see `fal-image-to-video`
- For model selection: see `fal-model-guide`

---

# fal.ai Video-to-Video Models

Complete reference for video editing, transformation, and upscaling models on fal.ai.

## Kling O1 Video Editing

### Kling O1 Video-to-Video Edit
**Endpoint:** `fal-ai/kling-video/o1/video-to-video/edit`
**Best For:** Comprehensive video editing and transformation

```typescript
import { fal } from "@fal-ai/client";

const result = await fal.subscribe("fal-ai/kling-video/o1/video-to-video/edit", {
  input: {
    prompt: "Transform into an anime style with vibrant colors",
    video_url: "https://example.com/original-video.mp4",
    edit_type: "style",
    negative_prompt: "blurry, distorted, low quality"
  }
});

console.log(result.video.url);
```

```python
import fal_client

result = fal_client.subscribe(
    "fal-ai/kling-video/o1/video-to-video/edit",
    arguments={
        "prompt": "Transform into anime style",
        "video_url": "https://example.com/video.mp4",
        "edit_type": "style"
    }
)
print(result["video"]["url"])
```

**Edit Types:**

| Type | Description | Use Case |
|------|-------------|----------|
| `general` | General purpose editing | Any transformation |
| `style` | Style transfer | Artistic effects |
| `object` | Object replacement/editing | Change specific elements |

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `prompt` | string | Editing instruction |
| `video_url` | string | Source video URL |
| `edit_type` | string | "general", "style", "object" |
| `negative_prompt` | string | What to avoid |

### Kling O1 Examples

**Style Transfer:**
```typescript
const result = await fal.subscribe("fal-ai/kling-video/o1/video-to-video/edit", {
  input: {
    prompt: "Transform into a watercolor painting style with soft brushstrokes",
    video_url: sourceVideoUrl,
    edit_type: "style",
    negative_prompt: "harsh edges, digital artifacts"
  }
});
```

**Object Editing:**
```typescript
const result = await fal.subscribe("fal-ai/kling-video/o1/video-to-video/edit", {
  input: {
    prompt: "Change the red car to a blue sports car",
    video_url: sourceVideoUrl,
    edit_type: "object"
  }
});
```

**General Transformation:**
```typescript
const result = await fal.subscribe("fal-ai/kling-video/o1/video-to-video/edit", {
  input: {
    prompt: "Make it look like a sunny summer day instead of overcast",
    video_url: sourceVideoUrl,
    edit_type: "general"
  }
});
```

## Sora 2 Remix

### Sora Remix (Video Transformation)
**Endpoint:** `fal-ai/sora/remix`
**Best For:** Creative video remixing and transformation

```typescript
const result = await fal.subscribe("fal-ai/sora/remix", {
  input: {
    prompt: "Transform this into a cinematic sci-fi scene with futuristic elements",
    video_url: "https://example.com/original.mp4",
    aspect_ratio: "16:9"
  }
});

console.log(result.video.url);
```

**Sora Remix Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `prompt` | string | Transformation description |
| `video_url` | string | Source video URL |
| `aspect_ratio` | string | "16:9", "9:16", "1:1" |

## Video Upscaling

### Video Upscaler
**Endpoint:** `fal-ai/video-upscaler`
**Best For:** Enhance video resolution

```typescript
const result = await fal.subscribe("fal-ai/video-upscaler", {
  input: {
    video_url: "https://example.com/low-res-video.mp4",
    scale: 2  // 2x or 4x upscale
  }
});

console.log(result.video.url);
```

```python
result = fal_client.subscribe(
    "fal-ai/video-upscaler",
    arguments={
        "video_url": "https://example.com/video.mp4",
        "scale": 2
    }
)
```

**Parameters:**

| Parameter | Type | Values | Description |
|-----------|------|--------|-------------|
| `video_url` | string | - | Source video URL |
| `scale` | number | 2, 4 | Upscale factor |

### TopazVideoAI (if available)
**Endpoint:** `fal-ai/topaz-video-ai`
**Best For:** Professional video enhancement

```typescript
const result = await fal.subscribe("fal-ai/topaz-video-ai", {
  input: {
    video_url: "https://example.com/video.mp4",
    enhancement_type: "upscale",
    target_resolution: "4k"
  }
});
```

## Video Frame Interpolation

### Frame Interpolation
**Endpoint:** `fal-ai/frame-interpolation`
**Best For:** Smooth motion, increase frame rate

```typescript
const result = await fal.subscribe("fal-ai/frame-interpolation", {
  input: {
    video_url: "https://example.com/24fps-video.mp4",
    target_fps: 60,
    interpolation_mode: "smooth"
  }
});
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `video_url` | string | Source video |
| `target_fps` | number | Target frame rate (30, 60, 120) |
| `interpolation_mode` | string | "smooth", "natural" |

## Video Style Transfer

### General Style Transfer Pipeline

```typescript
// Apply artistic style to video
async function applyVideoStyle(videoUrl: string, style: string) {
  const result = await fal.subscribe("fal-ai/kling-video/o1/video-to-video/edit", {
    input: {
      prompt: `Transform into ${style} style`,
      video_url: videoUrl,
      edit_type: "style"
    }
  });
  return result.video.url;
}

// Usage
const animeVideo = await applyVideoStyle(originalVideo, "anime");
const oilPaintingVideo = await applyVideoStyle(originalVideo, "oil painting");
const pixelArtVideo = await applyVideoStyle(originalVideo, "pixel art");
```

### Style Keywords

| Style | Prompt Example |
|-------|----------------|
| Anime | "Japanese anime style, cel shading" |
| Watercolor | "Soft watercolor painting with flowing colors" |
| Oil Painting | "Classical oil painting, textured brushstrokes" |
| Pixel Art | "8-bit pixel art retro game style" |
| Noir | "Black and white film noir, high contrast" |
| Cyberpunk | "Neon cyberpunk aesthetic, futuristic" |
| Sketch | "Hand-drawn pencil sketch style" |
| Comic | "Comic book style with bold outlines" |

## Video Enhancement Techniques

### Denoising
```typescript
const result = await fal.subscribe("fal-ai/kling-video/o1/video-to-video/edit", {
  input: {
    prompt: "Clean and enhance video quality, reduce noise and grain",
    video_url: noisyVideoUrl,
    edit_type: "general",
    negative_prompt: "grainy, noisy, artifacts"
  }
});
```

### Color Correction
```typescript
const result = await fal.subscribe("fal-ai/kling-video/o1/video-to-video/edit", {
  input: {
    prompt: "Enhance colors to be more vibrant and natural, improve contrast",
    video_url: flatVideoUrl,
    edit_type: "general"
  }
});
```

### Lighting Enhancement
```typescript
const result = await fal.subscribe("fal-ai/kling-video/o1/video-to-video/edit", {
  input: {
    prompt: "Improve lighting, add warm golden hour glow",
    video_url: darkVideoUrl,
    edit_type: "general"
  }
});
```

## Video Object Editing

### Object Replacement
```typescript
const result = await fal.subscribe("fal-ai/kling-video/o1/video-to-video/edit", {
  input: {
    prompt: "Replace the bicycle with a motorcycle",
    video_url: sourceVideoUrl,
    edit_type: "object"
  }
});
```

### Object Removal
```typescript
const result = await fal.subscribe("fal-ai/kling-video/o1/video-to-video/edit", {
  input: {
    prompt: "Remove the person in the background, fill with natural scenery",
    video_url: sourceVideoUrl,
    edit_type: "object"
  }
});
```

### Object Addition
```typescript
const result = await fal.subscribe("fal-ai/kling-video/o1/video-to-video/edit", {
  input: {
    prompt: "Add falling snow throughout the scene",
    video_url: sourceVideoUrl,
    edit_type: "object"
  }
});
```

## Complete Parameter Reference

```typescript
interface VideoToVideoInput {
  // Required
  video_url: string;

  // For editing models
  prompt?: string;
  edit_type?: "general" | "style" | "object";
  negative_prompt?: string;

  // For upscaling
  scale?: number;  // 2 or 4

  // For frame interpolation
  target_fps?: number;
  interpolation_mode?: string;

  // Output
  aspect_ratio?: string;
}
```

## Workflow Examples

### Complete Video Enhancement Pipeline

```typescript
async function enhanceVideo(sourceUrl: string) {
  // 1. Upscale resolution
  const upscaled = await fal.subscribe("fal-ai/video-upscaler", {
    input: {
      video_url: sourceUrl,
      scale: 2
    }
  });

  // 2. Enhance quality
  const enhanced = await fal.subscribe("fal-ai/kling-video/o1/video-to-video/edit", {
    input: {
      prompt: "Enhance video quality, improve sharpness and colors",
      video_url: upscaled.video.url,
      edit_type: "general"
    }
  });

  // 3. Smooth motion (optional)
  const smoothed = await fal.subscribe("fal-ai/frame-interpolation", {
    input: {
      video_url: enhanced.video.url,
      target_fps: 60
    }
  });

  return smoothed.video.url;
}
```

### Style Transfer Workflow

```typescript
async function styleTransferVideo(
  sourceUrl: string,
  targetStyle: string
) {
  // Apply style transformation
  const styled = await fal.subscribe("fal-ai/kling-video/o1/video-to-video/edit", {
    input: {
      prompt: `Transform into ${targetStyle} style, maintain motion consistency`,
      video_url: sourceUrl,
      edit_type: "style",
      negative_prompt: "flickering, inconsistent, artifacts"
    }
  });

  return styled.video.url;
}

// Usage
const animeVersion = await styleTransferVideo(original, "anime");
const paintingVersion = await styleTransferVideo(original, "impressionist oil painting");
```

### Batch Video Processing

```typescript
async function processVideosBatch(
  videos: string[],
  transformation: string
) {
  const results = await Promise.all(
    videos.map(video =>
      fal.subscribe("fal-ai/kling-video/o1/video-to-video/edit", {
        input: {
          prompt: transformation,
          video_url: video,
          edit_type: "general"
        }
      })
    )
  );

  return results.map(r => r.video.url);
}
```

## Model Comparison

| Model | Editing | Style | Upscale | Speed |
|-------|---------|-------|---------|-------|
| Kling O1 | Full | Full | No | Medium |
| Sora Remix | Limited | Full | No | Slow |
| Video Upscaler | No | No | Full | Fast |

## Best Practices

### For Style Transfer
1. **Be consistent** - Use specific style descriptions
2. **Avoid flickering** - Add "consistent" to negative prompt
3. **Test on clips** - Process short segments first
4. **Maintain identity** - Don't over-transform

### For Object Editing
1. **Be specific** - Name exact objects to change
2. **Provide context** - Describe replacement clearly
3. **Consider motion** - Ensure edits work with movement
4. **Check boundaries** - Object edges should blend naturally

### For Upscaling
1. **Source quality matters** - Clean input = better output
2. **Don't over-upscale** - 2x usually sufficient
3. **Consider file size** - Higher res = larger files
4. **Test first** - Preview with short clip

### For General Enhancement
1. **Incremental changes** - Don't try to fix everything at once
2. **Preserve intent** - Keep original mood/style
3. **Check artifacts** - Look for introduced errors
4. **Iterate** - Multiple passes may be needed

## Common Issues and Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| Flickering | Inconsistent frames | Add "consistent, stable" to prompt |
| Color shifts | Over-aggressive editing | Use gentler prompts |
| Lost details | Too much transformation | Reduce edit intensity |
| Artifacts | Compression issues | Use higher quality source |
| Motion blur | Frame interpolation | Use "natural" mode |

## File Size Considerations

| Operation | Size Impact |
|-----------|-------------|
| 2x Upscale | 4x larger |
| 4x Upscale | 16x larger |
| Frame interpolation | 2-4x larger |
| Style transfer | Similar size |

Always consider storage and bandwidth when processing videos.
