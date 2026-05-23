---
name: image-generation
description: >
  Generate or edit images with Gemini Pro. Use when user says "generate an image",
  "create a picture", "make me a logo", "edit this image", "remove the background",
  "change the style", "combine these images", "add text to image", "style transfer",
  "make a sticker", "product mockup", or any image creation/manipulation request.
  Handles t2i (text-to-image), i2i (image-to-image editing), and multi-reference composition.
---

# Image Generation

Generate and edit images using Google's Gemini Pro Image API. Requires `GEMINI_API_KEY` environment variable.

## Default Output & Logging

When the user doesn't specify a location, save images to:
```
/Users/samarthgupta/Documents/generated images/
```

Every generated image gets a companion `.md` file with the prompt used (e.g., `logo.png` → `logo.md`).

When gathering parameters (aspect ratio, resolution), offer the option to specify a custom output location.

---

## Core Prompting Principle

**Describe scenes narratively, don't list keywords.** Gemini has deep language understanding—write prompts like prose, not tags.

```
❌ "cat, wizard hat, magical, fantasy, 4k, detailed"

✓ "A fluffy orange tabby sits regally on a velvet cushion, wearing an ornate
   purple wizard hat embroidered with silver stars. Soft candlelight illuminates
   the scene from the left. The mood is whimsical yet dignified."
```

### The Formula

```
[Subject + Adjectives] doing [Action] in [Location/Context].
[Composition/Camera]. [Lighting/Atmosphere]. [Style/Media]. [Constraint].
```

Not every prompt needs every element—match detail to intent.

### Prescriptive vs Open Prompting

**Prescriptive** (user has specific vision): Detailed descriptions, exact specifications
**Open** (exploring/want model creativity): General direction, let model decide details

Both are valid. Ask the user's intent if unclear.

---

## Capability Patterns

### Photorealistic Scenes
Think like a photographer: describe lens, light, moment.
- Specify camera (85mm portrait, 24mm wide), aperture (f/1.8 bokeh, f/11 sharp throughout)
- Describe lighting direction and quality (golden hour from camera-left, three-point softbox)
- Include mood and format (serene, vertical portrait)

### Product Photography
- **Isolation**: Clean white backdrop, soft even lighting, e-commerce ready
- **Lifestyle**: Product in use context, natural setting, aspirational but authentic
- **Hero shots**: Cinematic framing, dramatic lighting, space for text overlay

### Logos & Text
- Put text in quotes: `'Morning Brew Coffee Co'`
- Describe typography: "clean bold sans-serif with generous letter-spacing"
- Specify color scheme, shape constraints, design intent
- Iterate with follow-up edits for refinement

### Stylized Illustration
- Name the style: "kawaii-style sticker", "anime-influenced", "vintage travel poster"
- Describe design language: "bold outlines, flat colors, cel-shading"
- Include format constraints: "white background", "die-cut sticker format"

### Editing Images
- **Acknowledge subject**: "Using the provided image of my cat..."
- **Explicit preservation**: "Keep everything unchanged except..."
- **Realistic integration**: "should look naturally printed on the fabric"
- **Image ordering**: Main image to edit should be **last** in `--input` list

Pattern: Acknowledge → specify change → describe integration → preserve the rest

### Multi-Image Composition
- State output goal first
- Assign elements: "Take X from first image, Y from second"
- Describe integration requirements (lighting match, realistic shadows)
- Supports up to 14 reference images

### Character Consistency
- Use follow-up edits for multiple views of the same character
- Reference distinctive features explicitly in follow-ups
- Include "exact same character" or "maintain all design details"
- Save successful designs as reference for future prompts

---

## Invoking Aesthetics Through Naming

Names invoke aesthetics. The model learned associations for film stocks, cameras, studios, artists, and styles. Instead of describing characteristics, reference the name directly.

```
"Portrait at golden hour, shot on Kodak Portra 400"
→ Warm skin tones, pastel highlights, fine grain

"Studio Ghibli forest scene"
→ Lush nature, soft lighting, whimsical atmosphere

"Fashion editorial, Hasselblad medium format"
→ Exceptional detail, shallow DOF, that medium format look
```

This works for photography, animation, illustration, game art, graphic design, fine art—anything with a recognizable visual identity.

**See [STYLE_REFERENCE.md](STYLE_REFERENCE.md) for comprehensive lexicon of film stocks, cameras, studios, artists, and styles.**

---

## Configuration

### Aspect Ratios
1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9

### Resolutions
- **1K** (~1024px) — default, fast
- **2K** (~2048px) — high quality
- **4K** (~4096px) — maximum detail

**Defaults**: 1K resolution, aspect ratio auto-detected from last reference image (or 1:1 if no images).

---

## Advanced Features

### Google Search Grounding
Enable with `--grounding` flag when real-time data helps:
- Weather visualizations
- Current events infographics
- Real-world data charts

### Semantic Masking
No manual masking needed. Describe changes conversationally:
- "Change the sofa to red leather"
- "Replace the background with a sunset beach"
- "Remove the power lines from the sky"

---

## Script Usage

One unified script handles all modes: t2i, i2i, and multi-reference composition.

```bash
# Text-to-image (t2i)
uv run {baseDir}/scripts/generate.py --prompt "A serene mountain lake at dawn" --output landscape.png

# Image-to-image editing (i2i)
uv run {baseDir}/scripts/generate.py --prompt "Make it sunset colors" --input photo.png --output edited.png

# Multi-reference composition (up to 14 images)
uv run {baseDir}/scripts/generate.py --prompt "Combine the cat from image 1 with the background from image 2" --input cat.png --input background.png --output composite.png

# With options
uv run {baseDir}/scripts/generate.py --prompt "Logo for 'Acme Corp'" --output logo.png --aspect 1:1 --resolution 2K

# With Google Search grounding
uv run {baseDir}/scripts/generate.py --prompt "Current weather in Tokyo visualized" --output weather.png --grounding

# Batch generation (up to 4 images, 2 parallel requests)
uv run {baseDir}/scripts/generate.py --prompt "A cat in different poses" --output cat.png --batch 4
# Outputs: cat-1.png, cat-2.png, cat-3.png, cat-4.png
```

### Script Options

| Flag | Short | Description |
|------|-------|-------------|
| `--prompt` | `-p` | Image description or edit instruction (required) |
| `--output` | `-o` | Output file path (required) |
| `--input` | `-i` | Input image(s) for editing/composition (repeatable, up to 14) |
| `--aspect` | `-a` | Aspect ratio (auto-detects from last reference image, or 1:1) |
| `--resolution` | `-r` | Output resolution: 1K, 2K, or 4K (default: auto-detect or 1K) |
| `--grounding` | `-g` | Enable Google Search grounding |
| `--batch` | `-b` | Generate multiple variations: 1-4 (default: 1, runs 2 parallel max) |

### Auto-Resolution Detection

When editing images, the script automatically detects appropriate resolution from input dimensions:
- Input ≥3000px → 4K output
- Input ≥1500px → 2K output
- Otherwise → 1K output

Override with explicit `--resolution` flag.

### Auto Aspect Ratio Detection

When no `--aspect` flag is provided:
- **With reference images**: Detects from the **last** input image (closest supported ratio)
- **Without reference images (t2i)**: Defaults to 1:1

This matches typical editing workflows where the last image is the canvas being edited.

### Image Optimization

Large input images (>2048px) are automatically resized before sending to the API to prevent timeout errors. The script uses high-quality LANCZOS resampling to preserve detail during downscaling. Original files are never modified.

---

## Recommended Defaults

Unless the user specifies otherwise, use:
- **Resolution**: 2K (good balance of quality and speed)
- **Batch**: 3 (gives variety without overwhelming)

Only use 4K when high detail is explicitly needed (large prints, zoom-in requirements).

---

## Pre-Generation Confirmation

Before running the script, show the user: (1) the exact prompt, (2) input images in order if editing/composing, (3) resolution and aspect ratio. Ask for confirmation before proceeding.

## Quick Checklist

Before generating:
- [ ] Narrative description (not keyword list)?
- [ ] Camera/lighting details for photorealism?
- [ ] Text in quotes, font style described?
- [ ] Aspect ratio appropriate for use case?
- [ ] User preference: prescriptive or open?
