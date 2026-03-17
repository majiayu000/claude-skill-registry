---
name: nano-banana-placeholders
description: Generates on-brand frontend placeholder images (hero, cards, avatars, etc.) using Google's Nano Banana (Gemini image models) via google-genai.
---

# Nano Banana Placeholders

Use this skill to generate clean, consistent placeholder images while building a website—so layouts look real before final creative is ready.

## When to use this skill

- You are building a website/app and need **temporary images** for:
  - Hero sections (16:9, 21:9)
  - Feature blocks / blog thumbnails (3:2, 4:3)
  - Product cards (1:1, 4:5)
  - Team avatars (1:1)
  - Mobile story/cover assets (9:16)
- You want placeholders that are **visually coherent** (same palette, lighting, style) across a full UI.
- You want the placeholders to be **safe by default**: no logos, no brand marks, no recognizable people, no text.

## Output standards

- **No text** in images (placeholders should not contain typography).
- **No logos / trademarks / brand lookalikes**.
- **No recognizable faces** (use silhouettes or abstract avatars if needed).
- Prefer **simple composition** and **low distraction** (soft gradients, subtle grain, minimal detail).
- Save assets into a predictable folder, e.g. `public/placeholders/` or `assets/placeholders/`.
- Maintain a small JSON manifest for easy wiring in frontend code.

## Model selection

Choose the model by intent:

1. Speed / bulk placeholders (default)

- Model: `gemini-2.5-flash-image` (Nano Banana)
- Use for: most card images, blog thumbnails, generic b-roll

2. Higher-fidelity hero or “marketing-looking” assets

- Model: `gemini-3-pro-image-preview` (Nano Banana Pro)
- Use for: hero banners, premium landing pages, images that need more controlled composition
- Consider `image_size="2K"` for hero assets

## Aspect ratio mapping (use one of these)

Common web ratios you’ll use:

- Avatar: `1:1`
- Blog thumbnail: `3:2` or `4:3`
- Product portrait: `4:5` or `3:4`
- Phone cover / story: `9:16`
- Hero: `16:9` or `21:9`

Set it with `image_config.aspect_ratio`.

## Prompting system (repeatable + consistent)

### Step 1 — Define the “Placeholder Spec”

For each image, write a short spec:

- `id`: unique name (e.g., `hero-home`, `card-feature-01`)
- `ratio`: `16:9`, `1:1`, etc.
- `category`: hero | card | avatar | product | background
- `subject`: what it should roughly depict (generic, non-branded)
- `style_preset`: choose one (below)
- `palette`: 2–4 colors or a vibe (e.g., “cool neutrals, soft blues”)
- `notes`: optional composition constraints (e.g., “empty space on left for headline”)

### Step 2 — Use a style preset (pick ONE)

**A. Abstract Gradient (default, safest)**

- “soft abstract gradient, subtle grain, modern, minimal”

**B. Minimal 3D Objects**

- “simple geometric 3D shapes, matte finish, studio light, no text”

**C. Flat Vector Illustration**

- “clean vector illustration, minimal details, modern SaaS style, no text”

**D. Generic Product Photography**

- “unbranded product-like object, neutral background, soft shadow, studio lighting”

### Step 3 — Build the final prompt (template)

Use this exact structure to keep outputs consistent:

- What it is + where used
- Ratio + composition requirement
- Style + palette
- Hard constraints (no text/logos/faces)
- Background cleanliness

**Prompt template:**

"Generate a modern placeholder image for a [CATEGORY] used on a website.
Aspect ratio: [RATIO].
Subject: [SUBJECT] (generic, unbranded).
Style: [STYLE_PRESET]. Palette: [PALETTE].
Composition: [NOTES].
Constraints: no text, no logos, no trademarks, no recognizable faces, no watermarks besides SynthID.
Background: clean, minimal, suitable for UI."

### Examples

**Hero (16:9)**
"Generate a modern placeholder image for a hero banner used on a SaaS landing page.
Aspect ratio: 16:9.
Subject: abstract sense of 'growth' using soft flowing shapes (generic, unbranded).
Style: soft abstract gradient, subtle grain, modern, minimal. Palette: cool neutrals with soft blue accents.
Composition: leave ~35% clean negative space on the left for headline text overlay.
Constraints: no text, no logos, no trademarks, no recognizable faces.
Background: clean and minimal."

**Avatar (1:1)**
"Generate a modern placeholder image for a user avatar in a web app.
Aspect ratio: 1:1.
Subject: abstract profile silhouette icon, friendly and minimal (generic, unbranded).
Style: clean vector illustration, minimal details. Palette: neutral gray with a single accent color.
Composition: centered.
Constraints: no text, no logos, no trademarks, no recognizable faces."

## How to use the generation script

### Step 1 — Dependencies

Ensure you have the required dependency:

- `pip install google-genai`

### Step 2 — Run the script

Use the provided script in the skill's `scripts` directory to generate images based on your prompt:

```bash
python .agent/skills/frontend-design/scripts/generate_images.py "Your prompt here" "output_filename"
```

The script uses a built-in API key for convenience, but will respect `GEMINI_API_KEY` if set in the environment.

### Step 3 — Integrate in Frontend

The script will save images in the current directory (or specified path). Move them to your project's `public/` or `assets/` folder and update your code.

### Step 4 — Generate a manifest (Optional)

If generating multiple assets, create a `manifest.json` in your images folder for easy reference:

```json
{
  "id": "hero-home",
  "ratio": "16:9",
  "file": "/assets/hero-home.png",
  "alt": "Abstract placeholder hero image."
}
```
