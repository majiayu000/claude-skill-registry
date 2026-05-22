---
name: og-hero-image
description: |
  Generate premium open-graph hero images for brands using AI.
  Use when: creating social sharing images, website headers, marketing collateral.
  Keywords: og image, open graph, hero image, social header, brand image
argument-hint: "[brand name or project path]"
---

# /og-hero-image

Generate a premium open-graph hero image for a brand.

## What This Does

1. Gather brand context (name, colors, tagline)
2. Generate prompt with brand values
3. Invoke Gemini image generation
4. Output 16:9 hero image ready for social sharing

## Prerequisites

Requires Gemini API access via the gemini-imagegen skill:
- `GEMINI_API_KEY` environment variable set
- Python 3.9+ with `google-genai` package

## Process

### 1. Gather Brand Context

**If project path provided:**
```bash
# Check for brand profile
cat brand-profile.yaml 2>/dev/null || cat .brand.yaml 2>/dev/null

# Check for existing colors in tailwind config
grep -A20 "colors:" tailwind.config.ts 2>/dev/null

# Check package.json for project name
jq -r '.name' package.json 2>/dev/null
```

**If no context found, ask:**
```
AskUserQuestion:
"What's the brand name and primary color palette?"
```

**Required context:**
- Brand name
- Primary brand color(s)
- Short headline (3-6 words) - or generate one

### 2. Generate Image

Use the gemini-imagegen skill:

```bash
~/.claude/skills/gemini-imagegen/scripts/generate_image.py \
  "[FULL PROMPT]" \
  "og-hero-[brand].png" \
  --aspect-ratio 16:9
```

**Full prompt template:**

```
Create a premium open-graph hero image for [BRAND]:

A wide horizontal layout (16:9 ratio) designed for social sharing, website headers, and marketing collateral. This is a high-end designer mockup presentation suitable for a branding portfolio or product launch. The focus is on clarity, balance, negative space and visual confidence.

LAYOUT STRUCTURE:

The composition is split into two clear zones with generous breathing room between them.

LEFT ZONE:
The [BRAND] logo and brand name are placed in the top-left corner. The logo is sized appropriately for the format, not too large, not too small. It reads clearly but doesn't dominate.

Below the logo, a single large headline is set in a clean, modern sans-serif typeface. The headline is short, typically 3-6 words maximum. It is confident, left-aligned, and sits comfortably within the left third of the canvas. The text color is derived from the brand palette.

RIGHT ZONE:
One floating, rounded rectangular panel suggesting a product interface, dashboard, or app screen. The panel has subtle depth, either through a soft drop shadow or slight elevation effect. The contents of the panel are suggestive rather than detailed, hinting at functionality without clutter.

The panel is angled very slightly or presented straight-on depending on what feels most balanced. It floats naturally in the composition, grounded by its shadow but with clear separation from the background.

NEGATIVE SPACE:
Strong use of negative space throughout. The background is clean and uncluttered. There is clear visual breathing room between the left text block and the right interface panel. Nothing feels cramped or crowded.

COLOR & STYLE:
Colors are drawn directly from the [BRAND] palette: [COLORS]. The background can be a brand color, white, off-white, or a subtle gradient that complements the brand.

The overall style is flat or near-flat. No heavy gradients, no glossy effects, no 3D renders. Shadows are subtle and serve only to create gentle depth. Typography is modern, confident, and legible at small sizes.

MOOD & FEEL:
Clean SaaS homepage hero. Quiet confidence. The image should feel premium, polished and intentional. Every element is placed with purpose. The overall impression is of a company that knows what it's doing.

WHAT TO AVOID:
No stock photo elements. No people. No complex illustrations. No decorative graphics or patterns. No multiple interface panels. No visual noise. No text other than the headline and brand name. No borders or frames around the image.

OUTPUT:
A single 16:9 image with no watermarks, no mockup frames, and no external branding. Ready to use as an open-graph image, social header, or presentation slide.

HEADLINE: "[HEADLINE]"
```

### 3. Review & Iterate

If the image doesn't meet quality bar:
- Adjust headline wording
- Specify color placement more precisely
- Regenerate with refined prompt

Use multi-turn chat for refinements:
```bash
~/.claude/skills/gemini-imagegen/scripts/multi_turn_chat.py
```

### 4. Output

Place image in standard location:
```
public/og-image.png          # Next.js default
public/images/og-hero.png    # Alternative
```

Update metadata if needed:
```typescript
// app/layout.tsx
export const metadata = {
  openGraph: {
    images: ['/og-image.png'],
  },
};
```

## Example Usage

**For Volume (fitness app):**
```
Brand: Volume
Colors: Deep green (#1a4d2e), warm cream (#f5f0e8)
Headline: "Track your fitness journey"

→ Generates: og-hero-volume.png (16:9, ~1200x630px)
```

**For Brainstory (journaling app):**
```
Brand: Brainstory
Colors: Warm amber (#d4a574), deep charcoal (#2d2d2d)
Headline: "Capture your thoughts"

→ Generates: og-hero-brainstory.png
```

## Quick Reference

```bash
# Generate with defaults
/og-hero-image volume

# With explicit values
/og-hero-image --brand "Volume" --colors "#1a4d2e, #f5f0e8" --headline "Track your fitness journey"
```

## Related Skills

- `gemini-imagegen` - Underlying image generation
- `brand-builder` - Creates brand-profile.yaml
- `seo-baseline` - Ensures OG tags are set correctly
