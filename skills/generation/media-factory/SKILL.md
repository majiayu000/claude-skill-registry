---
name: media-factory
description: AI-powered media production pipeline using Nano Banana Pro (images), KLING AI (video/transitions), and ElevenLabs (voiceover). Use when creating video content, product demos, social media assets, or any multimedia production.
version: 1.0.0
mcps: [firecrawl, perplexity]
subagents: [nana-image-generator]
skills: [terminal-ui-design]
---

# ID8 MEDIA FACTORY - AI Production Pipeline

## Purpose

Orchestrate AI-powered multimedia production using three specialized tools:
- **Nano Banana Pro** (fal.ai) → Image generation
- **KLING AI** → Video generation & transitions
- **ElevenLabs** → Voiceover & audio

**Philosophy:** Assemble, don't animate. Generate high-quality assets, then compose them into polished content.

---

## When to Use

- Creating product demos or explainer videos
- Generating social media video content
- Building marketing assets (ads, promos)
- Producing educational content
- Creating podcast/video intros and outros
- Generating b-roll or background footage
- Building visual storytelling content
- Product launch videos
- Any multimedia content requiring images + video + audio

---

## The Three Pillars

### 🖼️ Nano Banana Pro (Images)
**Provider:** fal.ai (`fal-ai/nano-banana-pro`)
**Purpose:** Generate high-quality still images from text prompts

| Feature | Value |
|---------|-------|
| Model | Gemini 3 Pro Image (Nano Banana 2) |
| Resolutions | 1K, 2K, 4K |
| Aspect Ratios | 21:9, 16:9, 3:2, 4:3, 5:4, 1:1, 4:5, 3:4, 2:3, 9:16 |
| Formats | PNG, JPEG, WebP |
| Web Search | Can use live web data for current topics |

**Best For:**
- Hero images, thumbnails
- Character/product shots
- Background scenes
- Storyboard frames
- Social media graphics

### 🎬 KLING AI (Video)
**Provider:** KLING AI / AI/ML API
**Purpose:** Generate video from text or images, create transitions

| Feature | Value |
|---------|-------|
| Text-to-Video | v1, v1.6, v2, v2.1 (standard/pro/master) |
| Image-to-Video | v1, v1.6, v2, v2.1 (standard/pro/master) |
| Effects | v1.6-standard/effects, v1.6-pro/effects |
| Resolution | Up to 1080p |
| Frame Rate | 30 fps |
| Duration | 5-10 seconds per generation |

**Best For:**
- Animating still images
- Creating transitions between scenes
- Generating b-roll footage
- Motion graphics
- Product animations

### 🎙️ ElevenLabs (Voice)
**Provider:** ElevenLabs API
**Purpose:** Generate natural voiceovers and audio

| Feature | Value |
|---------|-------|
| Models | eleven_multilingual_v2 (default), eleven_turbo_v2_5 |
| Languages | 32+ supported |
| Voices | 1000s of pre-made + custom voice cloning |
| Formats | mp3_44100_128, pcm_44100, etc. |
| Features | Pronunciation dictionaries, voice settings |

**Best For:**
- Narration and voiceovers
- Character voices
- Podcast intros
- Product demo audio
- Multilingual content

---

## Production Workflows

### Workflow 1: Image → Video → Audio (Standard)

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  NANO BANANA    │────▶│    KLING AI     │────▶│   ELEVENLABS    │
│  Generate       │     │  Animate        │     │   Narrate       │
│  Still Images   │     │  Images to      │     │   Final         │
│                 │     │  Video          │     │   Video         │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

**Steps:**
1. Write prompts for each scene/shot
2. Generate images with Nano Banana Pro
3. Feed images to KLING for animation
4. Write script for voiceover
5. Generate audio with ElevenLabs
6. Composite in video editor (CapCut, DaVinci, Premiere)

### Workflow 2: Script-First (Narrative)

```
┌─────────────────┐
│   SCRIPT        │
│   Write story   │
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌───────┐  ┌───────────┐
│ELEVEN │  │NANO BANANA│
│LABS   │  │Scene imgs │
└───┬───┘  └─────┬─────┘
    │            │
    │      ┌─────┴─────┐
    │      ▼           │
    │  ┌───────┐       │
    │  │KLING  │       │
    │  │Animate│       │
    │  └───┬───┘       │
    │      │           │
    └──────┴───────────┘
           │
           ▼
    ┌─────────────┐
    │  COMPOSITE  │
    │  Final Edit │
    └─────────────┘
```

### Workflow 3: Product Demo

```
Product Photos → KLING (animate) → KLING (transitions) → ElevenLabs (VO)
```

---

## Commands

### `/media-factory plan <concept>`

Create a production plan for multimedia content.

**Output:**
- Scene breakdown
- Image prompts (for Nano Banana)
- Video direction (for KLING)
- Script draft (for ElevenLabs)
- Estimated assets and timeline

### `/media-factory image <prompt>`

Generate an image using Nano Banana Pro.

**Parameters:**
- `--aspect` - Aspect ratio (default: 16:9)
- `--resolution` - 1K, 2K, or 4K (default: 1K)
- `--count` - Number of variations (default: 1)
- `--format` - png, jpeg, webp (default: png)

### `/media-factory video <prompt-or-image>`

Generate video using KLING AI.

**Parameters:**
- `--model` - v2.1-master, v1.6-pro, etc.
- `--mode` - text-to-video or image-to-video
- `--duration` - 5 or 10 seconds

### `/media-factory voice <script>`

Generate voiceover using ElevenLabs.

**Parameters:**
- `--voice` - Voice ID or name
- `--model` - eleven_multilingual_v2, eleven_turbo_v2_5
- `--format` - mp3_44100_128, pcm_44100, etc.

### `/media-factory storyboard <concept>`

Generate a complete storyboard with images for each scene.

---

## API Reference

### Nano Banana Pro (fal.ai)

**Endpoint:** `fal-ai/nano-banana-pro`

```javascript
import { fal } from "@fal-ai/client";

const result = await fal.subscribe("fal-ai/nano-banana-pro", {
  input: {
    prompt: "A product shot of a sleek black smartwatch on a marble surface, soft studio lighting, commercial photography",
    num_images: 1,
    aspect_ratio: "16:9",
    resolution: "2K",
    output_format: "png"
  }
});

console.log(result.data.images[0].url);
```

**Input Schema:**
| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| prompt | string | ✓ | - | Text description of image |
| num_images | integer | | 1 | Number of images to generate |
| aspect_ratio | enum | | 1:1 | 21:9, 16:9, 3:2, 4:3, 5:4, 1:1, 4:5, 3:4, 2:3, 9:16 |
| resolution | enum | | 1K | 1K, 2K, 4K |
| output_format | enum | | png | jpeg, png, webp |
| enable_web_search | boolean | | false | Use live web data |

**Environment:**
```bash
export FAL_KEY="your-fal-api-key"
```

---

### KLING AI

**Text-to-Video:**
```javascript
const response = await fetch("https://api.klingai.com/v1/videos/text-to-video", {
  method: "POST",
  headers: {
    "Authorization": `Bearer ${KLING_API_KEY}`,
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    model: "v2.1-master",
    prompt: "A camera slowly pans across a modern office space, morning light streaming through windows",
    duration: 5,
    aspect_ratio: "16:9"
  })
});
```

**Image-to-Video:**
```javascript
const response = await fetch("https://api.klingai.com/v1/videos/image-to-video", {
  method: "POST",
  headers: {
    "Authorization": `Bearer ${KLING_API_KEY}`,
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    model: "v2.1-master",
    image_url: "https://storage.example.com/my-image.png",
    prompt: "The subject slowly turns to face the camera, subtle wind moving their hair",
    duration: 5
  })
});
```

**Models Available:**
| Model | Type | Quality | Speed |
|-------|------|---------|-------|
| v2.1-master | Both | Highest | Slow |
| v2.1-pro | Both | High | Medium |
| v2.1-standard | Both | Good | Fast |
| v1.6-pro | Both | High | Medium |
| v1.6-standard | Both | Good | Fast |
| v1.6-standard/effects | I2V | Special FX | Fast |

---

### ElevenLabs

**Text-to-Speech:**
```javascript
const response = await fetch(
  `https://api.elevenlabs.io/v1/text-to-speech/${voiceId}`,
  {
    method: "POST",
    headers: {
      "xi-api-key": ELEVENLABS_API_KEY,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      text: "Welcome to our product demo. Today we'll show you how our solution transforms your workflow.",
      model_id: "eleven_multilingual_v2",
      voice_settings: {
        stability: 0.5,
        similarity_boost: 0.75,
        style: 0.0,
        use_speaker_boost: true
      }
    })
  }
);

// Response is audio stream (mp3 by default)
const audioBuffer = await response.arrayBuffer();
```

**Query Parameters:**
| Param | Default | Description |
|-------|---------|-------------|
| output_format | mp3_44100_128 | Audio format |
| optimize_streaming_latency | 0 | 0-4, higher = faster but lower quality |

**Voice Settings:**
| Setting | Range | Description |
|---------|-------|-------------|
| stability | 0-1 | Lower = more expressive, Higher = more consistent |
| similarity_boost | 0-1 | How closely to match the original voice |
| style | 0-1 | Style exaggeration (v2 models only) |
| use_speaker_boost | bool | Enhance speaker clarity |

**Environment:**
```bash
export ELEVENLABS_API_KEY="your-elevenlabs-key"
```

---

## Prompt Engineering

### For Nano Banana Pro (Images)

**Structure:** `[Subject] + [Setting] + [Style] + [Technical]`

**Examples:**
```
Product shot of a minimalist desk lamp on a wooden table, soft natural lighting, commercial photography, 4K resolution

A cyberpunk street market at night, neon signs reflecting on wet pavement, cinematic composition, moody atmosphere

Professional headshot of a confident business woman, studio lighting, neutral background, corporate style
```

### For KLING AI (Video)

**Structure:** `[Camera Movement] + [Subject Action] + [Environment] + [Mood]`

**Examples:**
```
Camera slowly pushes in on a coffee cup as steam rises, morning kitchen setting, warm and cozy atmosphere

Drone shot ascending over a mountain lake at sunrise, mist rolling across the water, epic and serene

Subject walks toward camera through a busy city street, shallow depth of field, dynamic and urban
```

### For ElevenLabs (Voice)

**Script Best Practices:**
- Use natural punctuation for pacing
- Add `...` for longer pauses
- Use `CAPS` sparingly for emphasis
- Include pronunciation hints: `[Nanotechnology: nan-oh-tek-nol-oh-jee]`
- Write conversationally, not formally

---

## Production Checklist

Before starting any media production:

- [ ] **Concept defined**: Clear vision of final output
- [ ] **Script drafted**: Narration or dialogue written
- [ ] **Storyboard created**: Scene-by-scene breakdown
- [ ] **Aspect ratios consistent**: All assets match target format
- [ ] **Voice selected**: ElevenLabs voice chosen and tested
- [ ] **API keys configured**: FAL_KEY, KLING_API_KEY, ELEVENLABS_API_KEY

Before compositing:

- [ ] **Images generated**: All Nano Banana assets ready
- [ ] **Videos rendered**: All KLING clips complete
- [ ] **Audio recorded**: All ElevenLabs VO exported
- [ ] **Music selected**: Background music sourced (if needed)
- [ ] **Timing mapped**: Script synced to visual timeline

---

## Asset Organization

```
project-name/
├── 01-planning/
│   ├── concept.md
│   ├── script.md
│   └── storyboard.md
├── 02-images/
│   ├── scene-01-hero.png
│   ├── scene-02-product.png
│   └── scene-03-cta.png
├── 03-videos/
│   ├── scene-01-animated.mp4
│   ├── scene-02-animated.mp4
│   └── transition-01.mp4
├── 04-audio/
│   ├── voiceover-full.mp3
│   ├── voiceover-scene-01.mp3
│   └── background-music.mp3
├── 05-exports/
│   ├── final-1080p.mp4
│   ├── final-4k.mp4
│   └── social-cuts/
└── project-notes.md
```

---

## Cost Estimation

| Tool | Pricing Model | Approximate Cost |
|------|---------------|------------------|
| Nano Banana Pro | Per image | ~$0.04-0.10 per 1K image |
| KLING AI | Per second | ~$0.05-0.20 per 5s clip |
| ElevenLabs | Per character | ~$0.30 per 1K characters |

**Example 60-second video:**
- 10 images × $0.08 = $0.80
- 6 video clips × $0.15 = $0.90
- 1000 character script × $0.30 = $0.30
- **Total: ~$2.00**

---

## Integration with ID8 Pipeline

### When to Invoke

During these pipeline stages:
- **Stage 9 (Launch Prep)**: Create launch videos, product demos
- **Stage 10 (Ship)**: Marketing assets, social content
- **Stage 11 (Listen & Iterate)**: Testimonial videos, update announcements

### Handoff

After completing media production:

1. **Save outputs:**
   - Assets → project `assets/media/` directory
   - Production notes → `docs/MEDIA_PRODUCTION.md`

2. **Log to tracker:**
   ```
   /tracker log {project-slug} "MEDIA: Produced {asset-type}. {count} images, {count} videos, {duration}s VO."
   ```

3. **Quality check:**
   - Preview all assets
   - Verify audio sync
   - Check resolution and format

---

## Tool Integration

### MCP Tools

**firecrawl:**
- Research competitor video styles
- Scrape reference content for inspiration

**perplexity:**
- Research trending video formats
- Find voice style references

### Subagents

**nana-image-generator:**
- Batch image generation with optimized prompts
- Style consistency across image sets

---

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| KLING video too static | Add more motion direction in prompt |
| ElevenLabs pacing too fast | Add punctuation, commas, ellipses |
| Nano Banana style inconsistent | Include style keywords in every prompt |
| Video transitions jarring | Use KLING effects mode for smoother cuts |
| Audio doesn't match timing | Generate VO in segments, not full script |

### Quality Optimization

**For sharper images:**
- Use 2K or 4K resolution
- Include "sharp focus" or "high detail" in prompt
- Export as PNG (lossless)

**For smoother video:**
- Use v2.1-master model
- Keep prompts focused on single action
- Generate 10s clips for more natural motion

**For natural voice:**
- Set stability to 0.4-0.6
- Use eleven_multilingual_v2 model
- Include natural punctuation in script

---

## Anti-Patterns

| Avoid | Why | Do Instead |
|-------|-----|------------|
| Generating video from text directly | Less control over visuals | Generate image first, then animate |
| Long VO in single generation | Pacing issues, errors compound | Generate in segments (30s max) |
| Inconsistent aspect ratios | Compositing nightmare | Lock ratio at start of project |
| Skipping storyboard | Waste of API credits | Plan shots before generating |
| Using default voice settings | Generic sound | Tune stability and style per project |

---

*Media Factory v1.0.0 - Added 2025-12-29*
