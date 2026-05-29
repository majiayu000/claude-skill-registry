---
name: brand-illustrator
description: Generate Builder Methods hand-drawn line art illustrations (icons, scenes, periphery) with a single accent color (Coral/Teal/Indigo/Amber). Use for blog headers, thumbnails, course graphics, social posts, and on-brand UI/tech metaphors.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
---

# Builder Methods Brand Illustrator

Generate hand-drawn line illustrations that match the Builder Methods visual identity:
warm off-white canvas, confident black ink lines, and one bold accent color.

This Skill is designed to be *reusable* and *procedural*:
- you gather requirements
- you propose three on-brand concepts
- you get a selection
- you generate final image(s) consistently using our style + color system

## What this Skill produces

- **Icon**: 1 primary object, isolated, quick punctuation.
- **Scene**: 2–4 objects, suggested environment, hero/header moments.
- **Periphery**: 1–3 objects, used as corner/edge elements or decorative supports.

See `references/visual-world.md` for the world + constraints and `references/style.md` for rendering rules.

## Requirements

- **Python 3.8+** for running the generation script
- **google-genai package**: `pip install google-genai`
- **GEMINI_API_KEY environment variable**: Set your Google Gemini API key as `GEMINI_API_KEY` (alternatively `GOOGLE_API_KEY` or `GENAI_API_KEY`)

Get an API key from: https://ai.google.dev/

## Quick Start

1. **Create a project folder** (recommended) in `projects/` with today's date and a short slug.

   Example:
   ```bash
   mkdir -p projects/2026-01-13-blog-hero
   ```

2. **Gather requirements** — use the AskUserQuestion tool for each missing piece *one at a time*.
   Required inputs:
   - **Content context**: topic + the core idea (insight), or paste article/transcript
   - **Visual context**: where the illustration will live (page screenshot, layout notes), or “n/a”
   - **Accent color**: `coral` | `teal` | `indigo` | `amber`
   - **Image type**: `icon` | `scene` | `periphery`
   - **Dimensions** (px): width × height

   Defaults:
   - scene: **1200×630**
   - icon: **512×512**
   - periphery: **500×500**

3. **Generate 3 concept options** using `references/idea-mapping.md`:
   - Present **Option A / B / C**
   - Each option includes: connection type, category (Builder’s World / Metaphor / Digital Artifact),
     object list, and why it fits the content.
   - Keep options meaningfully different (object choice, metaphor, or mood), but all on-brand.

4. **Get user choice** — use AskUserQuestion and let them pick A/B/C (or “Other” for feedback).

5. **Document the project** — create `project.md` inside the project folder with:
   - requirements
   - A/B/C concepts
   - chosen direction
   - final prompt + parameters
   - output filenames

6. **Craft prompt and generate** once a concept is approved, saving outputs to the project folder.

   Example:
   ```bash
   python3 scripts/generate.py \
     --prompt "A worn leather notebook open to a page with handwritten wireframe sketches" \
     --color coral \
     --type scene \
     --width 1200 \
     --height 630 \
     --output projects/2026-01-13-blog-hero/illustration-v1.png
   ```

## Color System

See `references/colors.md` for all hex values (single source of truth).

**Available accent colors:** Coral, Teal, Indigo, Amber

### Rules
- Use **ONE** accent color per illustration.
- Most of the image is **warm off-white background** with **confident black lines**.
- Accent color should fill **~20–30%** of the illustration.
- Shadow/depth color is used **sparingly** (**~5–10%**), mostly as grounding.

## Style Requirements (non-negotiable)

These are enforced by prompt + review. See `references/style.md` for full details.

- Hand-drawn ink line art; no photorealism, no 3D, no gradients
- Restrained compositions: focus objects over scenery
- Suggest environment with a few cues; do not render full rooms
- Leave negative space for text overlays when used as a hero image

## Concepting Guidance

Use the mapping doc to ensure every illustration is connected to the content:
- `references/idea-mapping.md` — connection types, object lists, metaphors, quick reference by meaning
- `references/visual-world.md` — what “belongs” in the Builder Methods world
- `references/prompts.md` — prompt templates and proven patterns

## Safety / Brand Guardrails

- Avoid trademarks/logos/brand names on devices, mugs, screens, or apparel.
- Avoid depicting real identifiable people.
- Keep UI/terminal content generic (nonsense code is fine; no secrets).
- No violence, gore, or sensitive themes—Builder Methods illustrations should feel calm and inviting.

## Project Documentation Template

Copy into `projects/<date>-<slug>/project.md`:

```md
# Project: <slug>

## Requirements
- Content context:
- Core idea:
- Visual context:
- Accent color:
- Image type:
- Dimensions:

## Concepts
### Option A
- Connection type:
- Category:
- Objects:
- Rationale:

### Option B
...

### Option C
...

## Selected Direction
- Chosen option:
- Notes / tweaks:

## Final Prompt
```text
<final prompt here>
```

## Generation Params
- color:
- type:
- width:
- height:
- output:

## Outputs
- illustration-v1.png
- illustration-v2.png
```
