---
name: higgsfield-operator
displayName: Higgsfield Operator
description: Master operator guide for Higgsfield AI video generation platform. Covers all 70+ camera presets, 23+ VFX effects, Soul ID character consistency, multi-model integration (Sora 2, Veo 3.1, WAN 2.5, Kling 2.6), Python SDK, and production workflows.
category: design
version: 1.0.0
triggers:
  - higgsfield
  - higgsfield video
  - ai video generation
  - sora 2
  - soul id
  - camera presets
  - vfx effects
  - image to video
  - text to video
  - wan 2.5
  - video ai
  - cinematic ai
  - talking head video
  - lipsync
author: ID8Labs
license: MIT
tags:
  - video
  - ai-video
  - higgsfield
  - sora
  - vfx
  - animation
  - cinematography
  - content-creation
complexity: complex
requiredMcps: []
---

# Higgsfield Operator

Master guide for Higgsfield AI - the multi-model video generation platform with 70+ cinematic camera presets, 23+ VFX effects, and integration with Sora 2, Google Veo 3.1, WAN 2.5, Kling 2.6, and more. This skill covers everything from basic image-to-video generation to advanced production workflows.

## Platform Overview

Higgsfield aggregates 15+ premium AI video models under one platform:
- **OpenAI Sora 2 / Sora 2 Pro** - Text-to-video with multi-scene support
- **Google Veo 3.1** - UGC Builder for talking heads
- **WAN 2.5** - Audio-synced video with camera controls
- **Kling 2.6** - High-fidelity video generation
- **Nano Banana Pro** - Fast generation (unlimited on Ultimate+)

**Key Differentiator:** Unlike single-model tools, Higgsfield layers professional controls (camera simulation, character consistency, lip-sync) on top of best-in-class AI models.

## When to Use This Skill

Use this skill when:
- Creating AI-generated video content (social, ads, content)
- Applying cinematic camera movements to static images
- Adding VFX without green screens or post-production
- Maintaining character consistency across multiple videos (Soul ID)
- Building talking-head videos with lip-sync
- Automating video generation via Python SDK
- Choosing between Higgsfield's integrated models

**Not recommended for:**
- Real-time video editing (use traditional NLEs)
- Video longer than 1 minute (current AI video limits)
- Precise frame-by-frame control (AI generates autonomously)

## Quick Reference

| Action | Method/Tool |
|--------|-------------|
| Image-to-Video | Upload image + select camera preset |
| Text-to-Video | Sora 2 or WAN 2.5 with text prompt |
| Character Consistency | Soul ID (upload 10+ reference photos) |
| Talking Head | UGC Builder (Veo 3.1) + Lipsync Studio |
| VFX Application | Select effect from 23+ presets |
| API Generation | Python SDK `higgsfield-client` |

---

## Core Workflows

### Workflow 1: Image-to-Video with Camera Motion

**Goal:** Transform a static image into a cinematic video clip

**Steps:**
1. Upload high-quality source image (1024x1024+ recommended)
2. Select camera preset from 70+ options
3. Optionally stack up to 3 movements
4. Choose aspect ratio (16:9, 9:16, 1:1)
5. Generate and download

**Camera Preset Categories:**

| Category | Examples | Best For |
|----------|----------|----------|
| **Dolly** | Dolly In, Dolly Out, Dolly Zoom | Product reveals, emphasis |
| **Pan** | Whip Pan, Pan Left/Right | Scene transitions, reveals |
| **Tilt** | Tilt Up/Down, Dutch Tilt | Dramatic reveals, horror |
| **Tracking** | Tracking Shot, Follow Shot | Action, chase scenes |
| **Aerial** | FPV Drone, Crane Shot, Helicopter | Establishing shots |
| **Specialty** | Bullet Time, 360 Rotation, Crash Zoom | Action, stylized content |
| **Stabilized** | Static, Locked Frame | Dialogue, interviews |

**Pro Tip:** Stack movements for complex motion: Crane + Dolly Zoom + Rotation = Christopher Nolan vibes.

---

### Workflow 2: Soul ID Character Consistency

**Goal:** Maintain identical character appearance across multiple videos

**Steps:**
1. Upload 10+ clear reference photos
   - Different angles (front, 3/4, profile)
   - Various expressions
   - Consistent lighting preferred
2. System creates digital twin capturing:
   - Face shape and structure
   - Hair style and color
   - Expression patterns
   - Posture characteristics
3. Select from 50+ style presets (Amalfi Summer, Gorpcore Outdoor, 0.5 Selfie, etc.)
4. Generate videos with consistent character

**Example Prompt with Soul ID:**
```
A young woman walks through a busy Tokyo street at night,
neon lights reflecting off wet pavement.
[Soul ID: @my-character]
Camera: Tracking Shot
```

**Use Cases:**
- Brand ambassadors across campaign
- Character-driven content series
- UGC-style ads with consistent "creator"
- Storytelling with recurring characters

---

### Workflow 3: VFX Effects Application

**Goal:** Add blockbuster VFX to videos without post-production

**Complete VFX Effects List:**

| Category | Effects |
|----------|---------|
| **Explosions** | Building Explosion, Clone Explosion, Head Explosion, Plasma Explosion, Car Explosion |
| **Fire/Heat** | Fire Element, Firelava, Firework, Flame On, Flame Transition, Fire Breath, Set On Fire |
| **Transformations** | Turning Metal, Cyborg, Animalization, Mystification, Gorilla Transfer, Monstrosity |
| **Disintegration** | Disintegration, Datamosh, Morphskin |
| **Superpowers** | Thunder God, Invisible, Luminous Gaze, Levitation, Hero Flight, I Can Fly |
| **Nature** | Earth Element, Earth Wave, Garden Bloom, Nature Bloom, Sakura Petals, Northern Lights |
| **Transitions** | Display Transition, Flying Cam Transition, Smoke Transition, Melt Transition, Seamless Transition |
| **Character** | Black Tears, Glowing Fish, Shadow Smoke, Tentacles, Symbiote, Angel Wings |
| **Environmental** | Aquarium, Flood, Cotton Cloud, Money Rain, Pizza Fall |
| **Style** | Glitch, Point Cloud, Polygon, Portal, Saint Glow, Paint Splash, Powder Explosion |

**Combination Effects (Beta):**
- Action Run + Set on Fire
- Building Explosion + Disintegration
- Car Chasing + Building Explosion
- Crash Zoom In + Face Punch

**Application Steps:**
1. Upload source image or generate video
2. Select VFX effect from library
3. Preview and adjust intensity (if available)
4. Combine with camera movement
5. Generate final output

---

### Workflow 4: Talking Head Videos (UGC Builder)

**Goal:** Create realistic talking-head content for ads and testimonials

**Powered by:** Google Veo 3.1 + Lipsync Studio

**Steps:**
1. Upload character image or use Soul ID
2. Input script text or upload audio
3. Select voice (AI synthesis or voice clone)
4. Apply style preset (professional, casual, energetic)
5. Generate lip-synced video

**Best Practices:**
- Keep clips under 30 seconds for best quality
- Use clear, well-lit face images
- Script natural, conversational language
- Test multiple voice options

---

### Workflow 5: Python SDK Integration

**Goal:** Automate video generation programmatically

**Installation:**
```bash
pip install higgsfield-client
```

**Authentication:**
```bash
# Option 1: Combined key
export HF_KEY="your-api-key:your-api-secret"

# Option 2: Separate keys
export HF_API_KEY="your-api-key"
export HF_API_SECRET="your-api-secret"
```

Get credentials from [Higgsfield Cloud](https://cloud.higgsfield.ai/)

**Synchronous Generation:**
```python
import higgsfield_client as hf

# Upload source image
image_url = hf.upload_file("./my-image.jpg")

# Generate video with camera preset
result = hf.subscribe(
    arguments={
        "image": image_url,
        "camera_preset": "dolly_in",
        "aspect_ratio": "16:9",
        "model": "wan_2.5"
    }
)

print(f"Video URL: {result['output_url']}")
```

**Asynchronous Generation with Polling:**
```python
import higgsfield_client as hf

# Submit request
controller = hf.submit(
    arguments={
        "prompt": "A futuristic city at sunset, flying cars",
        "model": "sora_2",
        "duration": 5
    }
)

# Poll for status
for status in hf.poll_request_status(controller.request_id):
    if isinstance(status, hf.Queued):
        print(f"Queue position: {status.position}")
    elif isinstance(status, hf.InProgress):
        print(f"Progress: {status.progress}%")
    elif isinstance(status, hf.Completed):
        print(f"Done! URL: {status.output_url}")
        break
    elif isinstance(status, hf.Failed):
        print(f"Error: {status.error}")
        break
```

**Webhook Notifications:**
```python
result = hf.submit(
    arguments={...},
    webhook_url="https://your-server.com/webhook"
)
```

**SDK Methods Reference:**

| Method | Description |
|--------|-------------|
| `subscribe(args)` | Submit and wait for completion |
| `submit(args)` | Submit and get controller for tracking |
| `status(request_id)` | Check request status |
| `result(request_id)` | Get completed result |
| `cancel(request_id)` | Cancel queued request |
| `upload(data, content_type)` | Upload raw bytes |
| `upload_file(path)` | Upload from file path |
| `upload_image(pil_image, format)` | Upload PIL Image |

All methods have `_async` variants for async/await usage.

**Status Types:**
- `Queued` - Waiting in queue
- `InProgress` - Currently generating
- `Completed` - Done, output available
- `Failed` - Generation failed
- `NSFW` - Content flagged
- `Cancelled` - User cancelled

---

## Camera Presets Complete Reference

### Basic Movements
| Preset | Motion | Use Case |
|--------|--------|----------|
| Static | No movement | Dialogue, portraits |
| Dolly In | Camera moves toward subject | Emphasis, intimacy |
| Dolly Out | Camera moves away | Reveal environment |
| Dolly Zoom | Zoom opposite of dolly | Vertigo effect |
| Pan Left/Right | Horizontal rotation | Scene scan |
| Tilt Up/Down | Vertical rotation | Reveal height |

### Dynamic Movements
| Preset | Motion | Use Case |
|--------|--------|----------|
| Whip Pan | Fast horizontal snap | Scene transition |
| Crash Zoom | Rapid zoom in | Shock, emphasis |
| Push In | Slow move toward | Building tension |
| Pull Out | Slow move away | Context reveal |
| Arc Shot | Semi-circular movement | Hero shots |
| 360 Rotation | Full circle around subject | Product showcase |

### Aerial/Specialty
| Preset | Motion | Use Case |
|--------|--------|----------|
| FPV Drone | First-person flying | Action, extreme sports |
| Crane Shot | Vertical lift | Establishing shots |
| Helicopter | Aerial sweep | Landscapes |
| Bullet Time | Frozen time orbit | Action freeze |
| Steadicam | Smooth follow | Walking/talking |
| Handheld | Slight shake | Documentary feel |

### Experimental (SOUL)
| Preset | Description |
|--------|-------------|
| Escalator | Moving escalator POV |
| Library | Bookshelf tracking |
| Gallery | Art museum walk |
| Street View | Urban street level |
| Subway | Metro station |
| Mt. Fuji | Mountain vista |
| Sunset Beach | Beach sunset |
| Flight Mode | Airplane window |
| Angel Wings | Ethereal floating |
| CCTV | Security camera |

---

## Pricing & Credits

| Plan | Monthly Cost | Credits | Key Features |
|------|--------------|---------|--------------|
| **Free** | $0 | Daily limit | 720p, watermark, basic presets |
| **Basic** | $9/mo | 150/mo | 1080p, no watermark |
| **Pro** | $29/mo | 600/mo | Faster queue, more models |
| **Ultimate** | $49/mo | 1,200/mo | Unlimited Nano Banana Pro |
| **Creator** | $249/mo | 6,000/mo | Priority rendering |
| **Studio** | Custom | Custom | Team collaboration, API |

**Credit Packs:** One-time purchases valid for 90 days

**Model Credit Costs (approximate):**
| Model | Credits/Generation |
|-------|-------------------|
| Nano Banana | 5-10 |
| WAN 2.5 | 15-25 |
| Kling 2.6 | 20-30 |
| Sora 2 | 30-50 |
| Sora 2 Pro | 50-100 |
| Veo 3.1 | 25-40 |

---

## Best Practices

### Image Quality
- Use 1024x1024 or higher resolution
- Avoid blurry or compressed images
- Good lighting in source = better output
- Centered subjects work best for most presets

### Prompt Engineering (Text-to-Video)
```
Good: "A golden retriever runs through autumn leaves
       in a forest, morning sunlight, slow motion"

Better: "A golden retriever runs joyfully through
        scattered autumn leaves in a sun-dappled forest,
        warm morning light filtering through trees,
        slow motion, cinematic depth of field,
        camera tracking shot"
```

### Soul ID Optimization
- Minimum 10 reference images
- Include full face, 3/4 angle, profile
- Vary expressions (smile, neutral, talking)
- Consistent lighting across images
- Avoid sunglasses, hats (unless character feature)

### VFX Integration
- Match effect intensity to content tone
- Preview before generating full video
- Layer camera movement AFTER effect selection
- Some effects work better on certain subject types

### API Efficiency
- Batch similar requests together
- Use webhooks for long generations
- Cache frequently-used image uploads
- Handle status polling with backoff

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Character looks different | Soul ID needs more references | Add 5+ more varied photos |
| Video is too short | Model/credit limitation | Upgrade plan or use longer model |
| VFX looks artificial | Low source quality | Use higher res source image |
| Generation failed | NSFW detection or model error | Rephrase prompt, change source |
| API timeout | Server load | Retry with exponential backoff |
| Queue position not moving | High demand | Check Higgsfield status page |

---

## Model Selection Guide

| Need | Recommended Model | Why |
|------|-------------------|-----|
| Fastest generation | Nano Banana | 5-10 seconds |
| Best quality | Sora 2 Pro | Highest fidelity |
| Talking heads | Veo 3.1 + UGC Builder | Best lip-sync |
| Audio sync | WAN 2.5 | Native audio support |
| Long form (8+ sec) | Sora 2 | Extended generation |
| Specific style | Kling 2.6 | Style consistency |
| Budget conscious | WAN 2.5 | Good quality/cost ratio |

---

## Integration Examples

### Node.js Wrapper (fetch-based)
```javascript
async function generateVideo(imageUrl, preset) {
  const response = await fetch('https://cloud.higgsfield.ai/api/generate', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${process.env.HF_KEY}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      image: imageUrl,
      camera_preset: preset,
      model: 'wan_2.5'
    })
  });
  return response.json();
}
```

### Next.js API Route
```typescript
// app/api/higgsfield/route.ts
import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  const { imageUrl, preset } = await request.json()

  // Forward to Higgsfield API
  const result = await generateVideo(imageUrl, preset)

  return NextResponse.json(result)
}
```

### Webhook Handler
```typescript
// app/api/higgsfield-webhook/route.ts
export async function POST(request: NextRequest) {
  const event = await request.json()

  if (event.status === 'completed') {
    // Save video URL to database
    await db.videos.update({
      where: { requestId: event.request_id },
      data: {
        outputUrl: event.output_url,
        status: 'ready'
      }
    })
  }

  return NextResponse.json({ received: true })
}
```

---

## Resources

- [Higgsfield Platform](https://higgsfield.ai/)
- [Higgsfield Cloud API](https://cloud.higgsfield.ai/)
- [Python SDK (GitHub)](https://github.com/higgsfield-ai/higgsfield-client)
- [Camera Controls Guide](https://higgsfield.ai/camera-controls)
- [VFX Effects Library](https://higgsfield.ai/effects)
- [Soul ID Documentation](https://higgsfield.ai/blog/sould-id-best-character-consistency)
- [WAN 2.5 Features](https://higgsfield.ai/wan-ai-video)
- [Sora 2 Integration](https://higgsfield.ai/sora-2)

---

*This skill is maintained by ID8Labs. Last updated: 2026-01-19*
