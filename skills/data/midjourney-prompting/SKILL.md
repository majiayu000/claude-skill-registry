---
name: midjourney-prompting
description: Craft effective Midjourney V7 prompts for any style — photography, illustration,
  anime, or artistic. Provides frameworks (7-Element, F.O.C.A.L.), parameter reference
  (--ar, --stylize, --sref, --cref),
---

---
name: midjourney-prompting
description: Craft effective Midjourney V7 prompts for any style — photography, illustration, anime, or artistic. Provides frameworks (7-Element, F.O.C.A.L.), parameter reference (--ar, --stylize, --sref, --cref), lighting/camera terminology, and V7-specific optimization. Auto-activates when writing Midjourney prompts, discussing MJ parameters, or creating AI image prompts. Triggers: Midjourney, MJ prompt, --ar, --stylize, --sref, style reference, character reference, image generation prompt.
---

# Midjourney V7 Prompting Guide

## Quick Reference: Prompt Structure

A Midjourney prompt has up to four parts:

```
/imagine [description] [image URLs] [parameters]
```

**Key Principle**: Short, specific prompts work best. Describe what you want to SEE, not abstract concepts.

---

## The 7-Element Framework

Build complete prompts systematically:

| Element | Question | Examples |
|---------|----------|----------|
| **Subject** | Who/what is in the image? | A weathered fisherman, a cyberpunk samurai |
| **Medium** | What art form? | Oil painting, photograph, 3D render |
| **Environment** | Where is this? | Stormy harbor, neon-lit alley, misty forest |
| **Lighting** | How is it lit? | Golden hour, dramatic backlighting, soft diffused |
| **Color** | What palette? | Muted blues, warm earth tones, high contrast |
| **Mood** | What feeling? | Melancholic, triumphant, eerie |
| **Composition** | How is it framed? | Rule of thirds, centered, wide shot |

**Example**:
```
A weathered fisherman, oil painting, stormy harbor at dawn,
dramatic backlighting, muted blues and grays, melancholic,
rule of thirds composition --ar 3:2
```

---

## Essential Parameters

| Parameter | Purpose | Values | Default |
|-----------|---------|--------|---------|
| `--ar` | Aspect ratio | Any ratio (16:9, 2:3, 1:1) | 1:1 |
| `--stylize` / `--s` | Artistic interpretation | 0-1000 | 100 |
| `--chaos` / `--c` | Variation between grid images | 0-100 | 0 |
| `--weird` / `--w` | Unusual aesthetics | 0-3000 | 0 |
| `--no` | Exclude elements | Words (comma-separated) | - |
| `--seed` | Reproducibility | 0-4294967295 | Random |
| `--style raw` | Less MJ beautification | - | Off |
| `--tile` | Seamless patterns | - | Off |

### Reference Parameters

| Parameter | Purpose | Weight Control |
|-----------|---------|----------------|
| `--sref [URL or code]` | Copy style from image | `--sw 0-1000` (default 100) |
| `--cref [URL]` | Copy character from image | `--cw 0-100` (default 100) |
| `--iw` | Image prompt weight | 0-3 (default 1) |

See [reference/parameters.md](reference/parameters.md) for complete details.

---

## Aspect Ratio Guide

| Ratio | Best For | Feel |
|-------|----------|------|
| 1:1 | Instagram, avatars | Balanced |
| 3:2 | Classic photography | Natural |
| 2:3 | Portrait orientation | Vertical focus |
| 16:9 | Widescreen, presentations | Cinematic |
| 21:9 | Ultra-wide, panoramic | Epic |
| 9:16 | Phone wallpapers, stories | Vertical social |

---

## Common Prompt Types

### Photorealistic Portrait

```
[Age] [ethnicity if relevant] [gender] [action/pose], [clothing],
[environment], [lighting type], [camera] [lens] [aperture],
[film stock if desired] --ar [ratio] --style raw
```

**Example**:
```
30-year-old woman with freckles and auburn hair, wearing cream
linen shirt, sitting in sun-drenched cafe, soft window light,
Canon EOS R5, 85mm lens, f/1.8, Kodak Portra 400 --ar 2:3 --style raw
```

### Illustration/Art

```
[Subject] in the style of [artist/medium], [environment],
[lighting], [mood] --ar [ratio] --stylize [value]
```

**Example**:
```
A mystical forest spirit, digital illustration in the style of Loish,
enchanted woodland, dappled sunlight, ethereal and mysterious
--ar 2:3 --stylize 250
```

### Anime/Manga (Niji Mode)

```
[Subject], [action/pose], [environment], [style notes] --niji 6
```

**Example**:
```
A fierce warrior princess, dynamic action pose, cherry blossom
battlefield, dramatic lighting, detailed armor --niji 6
```

---

## Style Reference (--sref)

Copy visual style from an image:

```
A mountain landscape --sref [image_URL]
```

**Using SREF codes** (numeric style codes):
```
A portrait of a warrior --sref 5000
```

**Random styles** (discover new aesthetics):
```
A cityscape --sref random
```

**Multiple style references with weights**:
```
A scene --sref URL1::2 URL2::1
```

**Style weight** (`--sw`): Higher = stronger style influence (0-1000, default 100)

---

## Character Reference (--cref)

Maintain character consistency across images:

```
A knight in a forest --cref [character_image_URL]
```

**Character weight** (`--cw`):
- `--cw 100` (default): Face, hair, AND clothing
- `--cw 50`: Moderate consistency
- `--cw 0`: Face only (different hair/clothes allowed)

**Best Practice**: Works best with Midjourney-generated characters. Real photos may produce distortions.

---

## Multi-Prompts & Weights

Use `::` to separate concepts for independent interpretation:

```
space ship    → sci-fi spaceship
space:: ship  → a boat in outer space
```

**Weighted prompts**:
```
forest::3 cabin::1 river::1    // Forest dominates
```

**Negative weights** (equivalent to --no):
```
flowers::-0.5
```

---

## V7 Key Features

V7 is Midjourney's latest and most capable model:

- **Superior prompt understanding** — More accurate interpretation of complex prompts
- **Better coherence** — Improved hands, bodies, and object relationships
- **Richer textures and details** — Higher quality output by default
- **Draft Mode** — 10x faster, half cost for exploration (`--draft`)
- **Personalization ON by default** — V7 applies learned preferences automatically
- **Omni Reference** — Enhanced reference capabilities

---

## V7 Best Practices

### DO

- Be specific with visual details
- Use natural language clearly
- Include time of day, weather, specific elements
- Place important elements early in prompt
- Use `--style raw` for photorealism and precise control
- Use `--draft` for quick exploration iterations
- Leverage V7's improved coherence for complex scenes

### DON'T (Junk Words to Avoid)

V7 produces high quality by default — these waste tokens:
- 4k, 6k, 8k, 16k, ultra 4k
- Octane, unreal, v-ray, lumion
- HDR, high-resolution
- Award-winning, photorealistic (unless specifically needed)

---

## Negative Prompts (--no)

**Correct usage**:
```
still life painting --no fruit, shadows, bright colors
```

**Critical warnings**:
- "don't" and "without" DO NOT work — use `--no` instead
- `--no modern clothing` = "no modern" AND "no clothing" (words interpreted separately)

---

## Text in Images

```
A storefront sign that says "BAKERY"
```

**Tips** (V7 handles text better than previous versions):
- Use double quotes only (single quotes don't work)
- Keep text SHORT (5 words or fewer)
- Include context: "sign that says", "text reading"
- Use `--style raw` for better accuracy
- Lower `--stylize` helps text clarity

---

## Common Mistakes

| Mistake | Problem | Solution |
|---------|---------|----------|
| Vague prompts | Unpredictable results | Be specific about subject, setting, style |
| Using "don't/without" | Words ignored or reversed | Use `--no` parameter |
| Prompt overload | Confused output | Keep under ~40 words |
| Too many --no items | Contradictory exclusions | Limit to essential exclusions |
| Ignoring --style raw | Over-stylized photos | Use raw for photorealism |
| Not saving seeds | Can't reproduce results | Note seeds for favorites |

---

## Key Principles

### The Specificity Principle
More specific = more control. Vague prompts let Midjourney decide; specific prompts give you your vision.

### The Subtraction Principle
Adding more words doesn't always help. Use `/shorten` to identify essential terms.

### The Reference Power Law
`--sref` and `--cref` provide more consistent control than text descriptions alone.

### The Iteration Mindset
First generation = starting point. Use variations, remix, vary region to refine.

---

## Photography Reference

For detailed camera settings, lighting terminology, and film stocks, see [reference/photography.md](reference/photography.md).

---

## Quick Templates

**Product shot**:
```
[Product] on [surface], [lighting], professional product photography,
clean background --ar 1:1 --style raw
```

**Landscape**:
```
[Scene], [time of day], [weather], [mood], wide angle,
[camera/film if desired] --ar 16:9
```

**Character design**:
```
[Character description], [pose], [outfit], [art style],
full body shot --ar 2:3
```

**Abstract/artistic**:
```
[Concept], [artistic style], [color palette], [texture],
[mood] --ar 1:1 --stylize 500
```
