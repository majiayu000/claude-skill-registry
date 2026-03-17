---
name: PhotoRealisticArt
description: |
  Generate stunning photorealistic images using advanced AI models. Covers portrait photography,
  landscapes, product shots, architecture, and cinematic scenes. Includes prompting techniques
  for lighting, composition, and camera settings.

  USE WHEN user says 'photorealistic', 'photo realistic', 'realistic image', 'stunning photo',
  'cinematic', 'portrait photo', 'product photography', 'landscape photo', 'hyper realistic',
  'professional photo', or needs high-quality realistic image generation.
---

# PhotoRealisticArt Skill

Generate **stunning photorealistic images** using AI. Optimized prompting techniques for maximum realism.

## Output Location

```
ALL GENERATED IMAGES GO TO ~/Downloads/ FIRST
Preview in Finder/Preview before final placement
Only copy to project directories after review
```

## Workflow Routing

Route based on subject matter:

- Portrait/headshot/person -> `Workflows/Portrait.md`
- Landscape/nature/scenic -> `Workflows/Landscape.md`
- Product/commercial/studio -> `Workflows/Product.md`
- Architecture/interior/real estate -> `Workflows/Architecture.md`
- Cinematic/movie still/dramatic -> `Workflows/Cinematic.md`

---

## Recommended Models

| Model | Best For | Quality |
|-------|----------|---------|
| **nano-banana-pro** | General photorealism, portraits | Excellent |
| **gpt-image-1** | Complex scenes, text in images | Very Good |
| **flux** | Artistic photorealism | Good |

**Default:** `nano-banana-pro` (Gemini 3 Pro) - best photorealistic quality

---

## Image Generation

```bash
bun run ~/.claude/skills/Art/Tools/Generate.ts \
  --model nano-banana-pro \
  --prompt "[PHOTOREALISTIC PROMPT]" \
  --size 2K \
  --aspect-ratio 16:9 \
  --output ~/Downloads/photo.png
```

**Reference images for consistency:**
```bash
bun run ~/.claude/skills/Art/Tools/Generate.ts \
  --model nano-banana-pro \
  --prompt "Same person from reference, now in business attire..." \
  --reference-image ~/Downloads/ref1.jpg \
  --reference-image ~/Downloads/ref2.jpg \
  --size 2K --aspect-ratio 3:4
```

---

## Photorealism Prompt Formula

```
[SHOT TYPE], [SUBJECT], [ACTION/POSE], [ENVIRONMENT],
[LIGHTING], [CAMERA], [MOOD], [QUALITY KEYWORDS]
```

### Quality Keywords (Always Include)

```
photorealistic, ultra detailed, 8K UHD, RAW photo,
sharp focus, professional photography, masterpiece
```

### Shot Types

| Type | Description | Use Case |
|------|-------------|----------|
| Close-up | Tight framing on face/detail | Beauty, emotion |
| Medium shot | Waist up | Portraits, editorial |
| Full body | Head to toe | Fashion, lifestyle |
| Wide shot | Subject + environment | Context, scenes |
| Macro | Extreme close-up | Products, textures |
| Aerial | Drone/bird's eye | Landscapes, architecture |

### Lighting Setups

| Lighting | Effect | Keywords |
|----------|--------|----------|
| Golden hour | Warm, flattering | golden hour, warm sunlight, soft shadows |
| Blue hour | Cool, moody | blue hour, twilight, ambient glow |
| Studio | Clean, professional | studio lighting, softbox, three-point lighting |
| Natural | Authentic, candid | natural light, window light, diffused daylight |
| Dramatic | High contrast | chiaroscuro, dramatic shadows, rim lighting |
| Neon | Cyberpunk, urban | neon lights, city glow, colorful reflections |

### Camera Settings (Adds Realism)

| Setting | Effect | Example |
|---------|--------|---------|
| Aperture | Depth of field | f/1.4 shallow DOF, f/8 sharp throughout |
| Focal length | Perspective | 85mm portrait, 24mm wide, 200mm telephoto |
| Shutter | Motion | 1/1000 frozen action, 1/30 motion blur |
| ISO | Grain | ISO 100 clean, ISO 3200 film grain |

---

## Quick Reference Prompts

### Portrait (Headshot)
```
Close-up portrait of [SUBJECT], natural expression, soft smile,
studio lighting with softbox, shallow depth of field f/1.8,
85mm lens, neutral background, professional headshot,
photorealistic, ultra detailed, 8K UHD, RAW photo
```

### Landscape
```
Wide shot panoramic landscape, [LOCATION/SCENE],
golden hour lighting, dramatic clouds,
shot on Sony A7R IV, 24mm f/8, deep focus,
photorealistic, ultra detailed, 8K UHD, nature photography
```

### Product
```
Commercial product photography, [PRODUCT] on white seamless,
studio lighting, soft shadows, macro detail,
shot on medium format Hasselblad, sharp focus throughout,
photorealistic, ultra detailed, professional advertising
```

### Cinematic
```
Cinematic still from [GENRE] film, [SUBJECT/SCENE],
anamorphic lens flare, film grain, color graded,
35mm film, shallow DOF, dramatic lighting,
photorealistic, movie quality, masterpiece
```

---

## Common Aspect Ratios

| Ratio | Use Case | Command |
|-------|----------|---------|
| 16:9 | Cinematic, landscape | `--aspect-ratio 16:9` |
| 3:2 | Standard photo | `--aspect-ratio 3:2` |
| 4:3 | Medium format feel | `--aspect-ratio 4:3` |
| 1:1 | Social media, portrait | `--aspect-ratio 1:1` |
| 9:16 | Mobile, stories | `--aspect-ratio 9:16` |
| 21:9 | Ultra-wide cinematic | `--aspect-ratio 21:9` |

---

## Negative Prompt Concepts

Avoid these in your prompts (or explicitly negate them):

```
AVOID: cartoon, anime, illustration, drawing, painting,
artificial, CGI, 3D render, plastic, waxy skin,
over-saturated, over-processed, HDR artifacts,
blurry, out of focus, distorted, deformed
```

---

## Examples

**Example 1: Executive Portrait**
```
User: "Create a professional headshot of a CEO"
-> Uses Portrait workflow
-> Prompt: "Close-up portrait of confident middle-aged businessman,
   silver hair, tailored navy suit, subtle smile,
   studio lighting with softbox and rim light,
   shallow DOF f/2.0, 85mm lens, corporate office bokeh background,
   photorealistic, ultra detailed, 8K UHD, professional headshot"
-> Output: ~/Downloads/ceo-portrait.png
```

**Example 2: Travel Photography**
```
User: "Stunning photo of Santorini at sunset"
-> Uses Landscape workflow
-> Prompt: "Wide shot of Santorini Greece white buildings with blue domes,
   overlooking Aegean Sea, golden hour sunset,
   warm orange and pink sky, dramatic clouds,
   shot on Sony A7R IV 24mm f/11, deep focus,
   photorealistic, ultra detailed, 8K UHD, travel photography"
-> Output: ~/Downloads/santorini.png
```

**Example 3: Product Shot**
```
User: "Product photo of luxury watch"
-> Uses Product workflow
-> Prompt: "Commercial product photography, luxury Swiss chronograph watch,
   brushed steel case, leather strap, on black velvet,
   dramatic studio lighting highlighting reflections,
   macro detail on dial and hands, shot on Hasselblad,
   photorealistic, ultra detailed, professional advertising"
-> Output: ~/Downloads/watch-product.png
```

---

## Extended Documentation

For advanced techniques and detailed workflows:
`read ~/.claude/skills/PhotoRealisticArt/CLAUDE.md`
