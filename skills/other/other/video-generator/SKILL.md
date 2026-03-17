---
name: video-generator
description: Generate AI videos with synchronized audio using Google's Veo 3.1 API. Use this skill when content needs short-form video — social clips, promotional teasers, ambient backgrounds, or creative visual storytelling. Follows an iterative workflow — storyboard the concept, craft the prompt with audio cues, generate via API, then refine.
---

# Video Generator

Generate professional short-form videos with native audio using Google's Veo 3.1 API via the same Gemini API key used for image generation.

## Prerequisites & Setup

### API Key

Uses the same key as the image-prompt-generator skill. If you already have `GEMINI_API_KEY` set, you're ready.

If not:

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated key

```bash
export GEMINI_API_KEY=your_api_key_here
```

### Install Dependencies

```bash
pip install google-genai
```

No additional dependencies beyond what the image skill already requires.

### Available Models

| Model | API Name | Best For |
|-------|----------|----------|
| **Standard** | `veo-3.1-generate-preview` | Quality, audio fidelity, final assets |
| **Fast** | `veo-3.1-fast-generate-preview` | Drafts, iteration, quick previews |

### Video Parameters

| Parameter | Options | Default |
|-----------|---------|---------|
| **Duration** | 4, 6, or 8 seconds | 8s |
| **Resolution** | 720p, 1080p, 4K | 720p |
| **Aspect Ratio** | 16:9, 9:16 | 16:9 |
| **Count** | 1-4 variations | 1 |

### Latency

Video generation is async — expect 11 seconds to 6 minutes depending on server load. The script polls automatically and saves when ready.

---

## Workflow Overview

1. **Define the Concept** — What story does the video tell in 4-8 seconds?
2. **Storyboard the Shot** — Camera, motion, subject, environment
3. **Add Audio Direction** — Dialogue, sound effects, ambient sound
4. **Generate Video** — Run via API
5. **Iterate** — Adjust prompt based on results

## Prompt Rules (From Research)

Before diving into the workflow, internalize these rules from extensive testing across Veo, Runway, and Sora:

1. **150-300 characters is the sweet spot.** Under 100 = generic. Over 400 = the model drops elements unpredictably.
2. **One shot = one action.** Don't pack multiple scene changes or style shifts into one prompt. One camera move + one subject action.
3. **Describe what you want, not what you don't want.** Use the `--negative` flag for exclusions, not the main prompt.
4. **Treat audio as a separate layer.** Write audio cues in their own sentences, not mixed into visual descriptions.
5. **Use colon syntax for dialogue.** `A man says: "Hello!"` prevents subtitle artifacts. Without the colon, text may appear on screen.
6. **Keep dialogue under 7 words per line.** Longer speech causes lip-sync drift or rushed garbling.
7. **Start simple, then layer.** Begin with a basic prompt, evaluate, then add one variable at a time.
8. **Slow camera movements win.** Fast pans and spins break output. Use tight framing for perceived speed.

See `references/prompt-engineering-research.md` for the complete research.

---

## Step 1: Define the Concept

A good video prompt answers three questions:

- **What's happening?** (action/motion)
- **Where?** (environment/setting)
- **What does it sound like?** (audio landscape)

Unlike images, video is *temporal*. Think in terms of movement and change, not a static composition.

**Good concepts for 8-second clips:**

| Use Case | Example Concept |
|----------|----------------|
| Social teaser | A hand flipping through pages of a book, stopping on a highlighted passage |
| Ambient background | Rain falling on a window with city lights blurring behind it |
| Product reveal | Camera slowly orbits a product on a table, warm studio lighting |
| Podcast promo | A microphone in a cozy studio, coffee steam rising, morning light |
| Newsletter visual | A typewriter striking keys, with the sound of each keystroke |

## Step 2: Storyboard the Shot

Structure your prompt with cinematic language. Veo responds well to film terminology:

### Camera Language

| Term | Effect |
|------|--------|
| **Wide shot** | Shows full environment, establishes context |
| **Close-up** | Tight on a subject, emphasizes detail |
| **Tracking shot** | Camera follows subject movement |
| **Dolly in/out** | Camera moves toward or away from subject |
| **Static shot** | Locked camera, subject moves within frame |
| **Slow pan** | Camera rotates horizontally across scene |
| **Overhead / bird's eye** | Looking straight down |
| **Low angle** | Looking up at subject, adds drama |

### Motion Description

Be explicit about what moves and how:

| Don't | Do |
|-------|-----|
| "A dog in a park" | "A golden retriever runs toward camera through tall grass, ears bouncing" |
| "City at night" | "Camera slowly dollies through a neon-lit Tokyo alley as rain puddles reflect signs" |
| "Ocean" | "A single wave forms, curls, and crashes onto wet sand in slow motion" |

### Lighting & Atmosphere

| Term | Mood |
|------|------|
| Golden hour | Warm, nostalgic, cinematic |
| Overcast | Soft, even, contemplative |
| Neon / artificial | Urban, energetic, modern |
| Candlelight | Intimate, quiet |
| Hard shadows | Dramatic, high contrast |

## Step 3: Add Audio Direction

Veo 3.1 generates synchronized audio natively. This is a major differentiator — use it.

### Three Types of Audio Cues

**1. Dialogue** — Use colon syntax before quotes (prevents subtitle artifacts):
```
A barista says: "Here you go!" as she slides a latte across the counter.
```
Keep lines under 7 words for clean lip-sync. One sentence max per 8-second clip.

**2. Sound Effects** — Describe specific sounds:
```
The sound of a match striking, then a candle flame flickering to life.
```

**3. Ambient Sound** — Set the sonic environment:
```
Birds chirping in the background, distant traffic hum, morning atmosphere.
```

### Audio Tips

- Be specific: "the crunch of gravel underfoot" beats "footstep sounds"
- Layer audio: combine ambient + specific sounds for depth
- Match audio to motion: "a door creaks open" timed with the visual action
- Dialogue should be short — 1-2 sentences max for 8 seconds

## Step 4: Craft the Full Prompt

### Prompt Structure (5-Element Priority)

Structure prompts in this order of priority — you don't need all five every time:

1. **Shot Specification** — camera work, framing, movement
2. **Setting & Atmosphere** — location, time, weather, lighting
3. **Subject & Action** — who/what, described in beats
4. **Audio Layer** — dialogue, SFX, ambient (separate sentences)
5. **Style/Grade** — artistic treatment, lens, color

```
[Shot type + camera movement]. [Setting and lighting]. [Subject doing action].
[Audio: what you hear]. [Style/grade].
```

### Example Prompts

**Podcast promo (16:9):**
```
A close-up tracking shot of a vintage microphone in a warmly lit podcast studio.
Steam rises slowly from a coffee mug beside it. Morning sunlight filters through
blinds, casting soft stripes across the desk. The sound of a quiet room — a clock
ticking, the faint hum of equipment. Cinematic, intimate, inviting.
```

**Social teaser — vertical (9:16):**
```
A hand reaches into frame and opens a leather-bound journal on a wooden desk.
The pages flutter briefly before settling on a page covered in handwritten notes.
A pen is set down beside the book. The sound of pages rustling, a pen clicking,
and soft ambient music. Warm overhead lighting, shallow depth of field.
```

**Newsletter header — ambient loop (16:9):**
```
A static wide shot of rain falling on a large window. Behind the glass, a blurred
cityscape with warm lights. Water droplets slide slowly down the pane. The sound of
steady rain and distant muffled city noise. Moody, contemplative, cozy.
```

**Product reveal (16:9):**
```
Camera slowly orbits a pair of wireless headphones placed on a dark marble surface.
Dramatic studio lighting with a single warm key light from the left. The headphones
cast a sharp shadow. Subtle electronic ambient music. Premium, minimal, modern.
```

## Step 5: Generate via API

### Running the Script

```bash
# Basic generation (8s, 720p, 16:9)
python scripts/generate_video.py "Your prompt here"

# Fast draft for iteration
python scripts/generate_video.py "Your prompt here" --model fast

# High quality vertical video for social
python scripts/generate_video.py "Your prompt" --aspect 9:16 --resolution 1080p

# Multiple variations to choose from
python scripts/generate_video.py "Your prompt" --count 2 --output ./videos

# Short clip with specific settings
python scripts/generate_video.py "Your prompt" --duration 4 --resolution 4k --name "hero-clip"

# Exclude unwanted elements
python scripts/generate_video.py "Your prompt" --negative "text overlays, watermarks, blurry"
```

**Options:**

| Flag | Values | Default | Notes |
|------|--------|---------|-------|
| `--model` | `standard`, `fast` | `standard` | Fast for drafts, standard for finals |
| `--aspect` | `16:9`, `9:16` | `16:9` | Vertical for Reels/TikTok/Shorts |
| `--resolution` | `720p`, `1080p`, `4k` | `720p` | Use 1080p+ for final assets |
| `--duration` | `4`, `6`, `8` | `8` | Shorter = faster generation |
| `--negative` | text | none | Describe what to avoid |
| `--count` | `1`-`4` | `1` | Generate variations |
| `--output` | path | `.` | Save directory |
| `--name` | text | none | Filename prefix |

**Output:** MP4 files with timestamp-based filenames.

## Step 6: Iterate

After reviewing generated video:

- **Motion wrong?** Be more explicit about direction, speed, and sequence
- **Audio off?** Add or refine audio cues — the model needs clear direction
- **Too much happening?** Simplify. One clear action per clip works best
- **Style drift?** Add a negative prompt to exclude unwanted aesthetics
- **Wrong mood?** Adjust lighting and atmosphere descriptors

### Iteration Strategy

1. Start with `--model fast` and `--duration 4` for quick drafts
2. Refine the prompt through 2-3 fast iterations
3. Switch to `--model standard` with full duration/resolution for the final take
4. Generate 2 variations of the final prompt and pick the best

---

## Negative Prompt Guide

Use `--negative` to steer away from common problems:

| Problem | Negative Prompt |
|---------|-----------------|
| Text/watermarks appearing | "text, watermarks, logos, subtitles" |
| Uncanny faces | "distorted faces, morphing features" |
| Jittery motion | "jerky motion, flickering, stuttering" |
| Over-saturated look | "oversaturated, HDR, neon colors" |
| Stock footage feel | "generic, corporate, stock footage aesthetic" |

---

## Prompting Principles

### Think in Shots, Not Scenes

8 seconds is one shot. Don't try to cram a narrative arc — describe a single continuous moment.

| Don't | Do |
|-------|-----|
| "A chef makes a meal from scratch and serves it" | "A chef's hands julienne carrots on a wooden cutting board, knife moving rhythmically" |
| "A day at the beach from sunrise to sunset" | "Waves gently lap at bare feet on sand, golden hour light, camera at ground level" |

### Be Specific About Motion

Vague motion descriptions produce vague results. Describe *what moves*, *how fast*, and *in which direction*.

### Layer Your Audio

Don't just describe one sound — create a soundscape:
```
The crackling of a vinyl record playing soft jazz,
a distant car horn outside the window,
the quiet clink of an ice cube in a glass.
```

### Use Negative Prompts Proactively

Always include `--negative "text, watermarks"` at minimum. The model occasionally generates unwanted text overlays.

---

## Use Cases by Content Type

### Social Media (9:16, 4-8s)

Short, punchy, loop-friendly. Favor close-ups and strong motion.

```bash
python scripts/generate_video.py "Close-up of coffee being poured into a ceramic mug, steam rising, warm morning light. The sound of liquid pouring and a soft sigh." \
  --aspect 9:16 --duration 4 --resolution 1080p
```

### Podcast/Newsletter Headers (16:9, 8s)

Ambient, atmospheric. Favor wide shots and subtle motion.

```bash
python scripts/generate_video.py "A vintage radio on a wooden shelf, dial slowly turning. Warm tungsten light. Soft static transitioning into faint music." \
  --resolution 1080p --name "podcast-header"
```

### Product/Brand (16:9, 6-8s)

Clean, controlled, premium feel. Studio lighting, slow orbits.

```bash
python scripts/generate_video.py "Camera slowly orbits a leather notebook on a dark wood desk. Single warm key light. The sound of pages turning gently." \
  --resolution 4k --duration 6 --negative "text, watermarks, busy background"
```

---

## Multi-Clip Consistency

When generating multiple clips for a project (e.g. a social series, product launch, or multi-shot sequence):

### Lock Your Constants

Create a consistency block and repeat it verbatim across all prompts:

```
CHARACTER: A woman in her thirties with short silver hair and a black turtleneck
PALETTE: amber, cream, walnut brown, deep olive
LIGHTING: Soft key light from camera right, warm tungsten
STYLE: Cinematic, shallow depth of field, warm film grain
NEGATIVE: no subtitles, no on-screen text, no watermarks
```

### Frame Chaining

For sequential shots, use the last frame of clip N as the reference image for clip N+1. This preserves subject orientation, lighting continuity, and motion vectors.

### Consistency Checklist

- [ ] Same character description, word for word — never paraphrase between shots
- [ ] Same palette anchors (3-5 named colors)
- [ ] Same lighting direction and quality
- [ ] Same aspect ratio and resolution
- [ ] Same style/grade language
- [ ] "No subtitles, no on-screen text" included
- [ ] Simple wardrobe — solid colors and notable anchors (red jacket, silver pendant) are more consistent than busy patterns

---

## Related Skills

- **image-prompt-generator** — Static images with the same API key and similar workflow
- **youtube-title-creator** — Pair video content with optimized titles
- **social-content-creation** — Use videos in platform-optimized posts

---

*For prompt engineering research and advanced techniques, see `references/prompt-engineering-research.md`*
