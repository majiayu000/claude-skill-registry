---
name: art-direction-prompt-refiner
description: Transform rough image generation prompts into consistent, effective art direction. Use when getting inconsistent results from AI image generators, need variations matching existing style, or translating vague ideas into precise prompts. Outputs structured prompts, negative prompts, and composition variants.
---

# Art Direction Prompt Refiner (Stil-Regisseur)

Transform rough image generation prompts into consistent, effective art direction.

## When to Use

- Getting inconsistent results from image generators
- Need variations that match existing style
- Translating vague ideas into precise prompts
- Maintaining visual consistency across assets

## Process

### 1. Parse Raw Request

Extract from user's messy prompt:
- **Subject**: What's being depicted
- **Mood**: Emotional tone
- **Style hints**: Any mentioned aesthetics
- **Context**: Where this will be used

### 2. Define Style Anchors

```
Style Framework:
- Medium: [digital art, vector, watercolor, 3D render]
- Rendering: [flat, gradient, realistic, painterly]
- Detail level: [minimal, moderate, intricate]
- Color approach: [limited palette, full color, monochrome]
- Mood keywords: [3-5 consistent terms]
```

### 3. Build Structured Prompt

Template:
```
[SUBJECT], [MEDIUM/STYLE], [RENDERING APPROACH],
[COLOR PALETTE DESCRIPTION], [MOOD/ATMOSPHERE],
[COMPOSITION NOTES], [TECHNICAL SPECS]
```

### 4. Add Negative Prompt

```
Negative: [unwanted elements], [wrong styles],
[technical issues to avoid], [mood conflicts]
```

### 5. Generate Variants

```
Variant A (Center-focused):
"[subject] centered in frame, symmetrical..."

Variant B (Left-heavy):
"[subject] positioned left third, negative space right..."

Variant C (Close-up):
"[subject] close-up detail, cropped view..."

Variant D (Environmental):
"[subject] in full environment, establishing shot..."
```

## Example Transformation

**Raw prompt:**
"ice climber on mountain, looks cool, winter vibes"

**Refined prompt:**
```
Ice climber ascending frozen waterfall on dramatic mountain peak,
flat minimalist vector illustration style,
muted teal and navy color palette (#0c1e2b, #1e3a5f, #64b5f6),
soft gradient shading, night atmosphere with subtle stars,
silhouetted pine trees in foreground for depth,
vertical composition emphasizing height,
transparent or dark navy background for UI integration

Negative: photorealistic, 3D render, outlines, busy details,
bright saturated colors, daylight, grain texture, lens flare
```

## Style Term Reference

### Medium/Style
| Term | Effect |
|------|--------|
| vector illustration | Clean edges, scalable |
| flat design | Minimal shadows, bold shapes |
| soft gradient | Gentle depth, dreamy |
| low poly | Geometric, modern |

### Mood Keywords
| Vibe | Use These |
|------|-----------|
| Calm | serene, peaceful, tranquil, soft |
| Dramatic | epic, intense, powerful, dynamic |
| Cozy | warm, inviting, comfortable |
| Mysterious | ethereal, mystical, enchanted |

### Technical Specs
```
For UI backgrounds:
- "transparent background" or "solid [color] background"
- "[orientation] composition"
- "negative space for text overlay"

For hero images:
- "high resolution"
- "clean edges for masking"
```
