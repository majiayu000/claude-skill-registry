---
name: image-gen
description: >
  Generate images using the brand's visual identity and Gemini API. Reads
  brand/creative-kit.md for visual style, crafts narrative prompts, and produces
  images via Nano Banana Pro (gemini-3-pro-image-preview). Supports on-brand
  and freestyle modes. Use when the user needs a blog header, social graphic,
  product shot, hero image, banner, thumbnail, or any generated image. Also use
  proactively when building content that would benefit from visuals. Triggers on
  "generate image", "create image", "make me an image", "blog header", "social
  graphic", "product shot", "hero image", "banner", "thumbnail", "I need an
  image", "visual for", or any request for generated artwork. Even if they just
  say "image" or "picture for this" — this is the skill.
reads:
  - brand/voice-profile.md
  - brand/positioning.md
  - brand/creative-kit.md
  - brand/landscape.md
writes:
  - brand/assets.md
depends-on: []
triggers:
  - generate image
  - create image
  - blog header
  - social graphic
  - product shot
  - need an image
  - make me an image
  - visual for
  - hero image
  - banner
  - thumbnail
allowed-tools:
  - Bash(python3 *)
---

# /image-gen — On-Brand Image Generation

Describe what you need. Get an image that looks like your brand made it.

This skill reads your visual brand identity from `brand/creative-kit.md`, crafts a narrative prompt that bakes in your style constraints, and generates the image via Gemini API. No brand style defined yet? It still works — just at a lower enhancement level. Run `/visual-style` first for the best results.

---

## On Activation

1. Check `GEMINI_API_KEY` environment variable.
   - If missing: "Image generation requires a Gemini API key. Set GEMINI_API_KEY in your environment. Get one at ai.google.dev."
   - Do not proceed without it.

2. Read brand files in priority order:
   - `brand/creative-kit.md` — look for `## Visual Brand Style` section
   - `brand/voice-profile.md` — personality informs image tone
   - `brand/positioning.md` — angles inform visual metaphors
   - `brand/landscape.md` — Claims Blacklist (don't generate imagery that visually implies blacklisted claims)

3. Determine enhancement level:

| Level | Context available | Image quality |
|-------|------------------|---------------|
| L0 | No brand files | Good generic images — uses discovery questions + prompt craft |
| L1 | voice-profile.md | Personality-aligned — playful brand gets warm/bright images |
| L2 | + creative-kit.md colors/typography | Color-constrained — palette woven into prompts |
| L3 | + Visual Brand Style section | Fully on-brand — style anchors, lighting, mood, composition all applied |

---

## Phase 1: Discovery

Use AskUserQuestion. Ask one at a time. Skip questions the user already answered in their request.

**Question 1: Purpose**
"What's this image for?"
- Blog header / article illustration
- Social media post (which platform?)
- Product shot / marketing asset
- Hero image / landing page
- Presentation / slide deck
- Something else (describe it)

This determines aspect ratio:

| Use case | Default ratio | Resolution |
|----------|---------------|------------|
| Blog header | 16:9 | 2K |
| Social square | 1:1 | 2K |
| Social story | 9:16 | 2K |
| Hero / banner | 21:9 | 2K |
| Product shot | 4:3 | 4K |
| Thumbnail | 16:9 | 1K |

**Question 2: Feeling**
"What should someone feel when they see this?"
(Free text — this drives the prompt's emotional anchor)

**Question 3: Style override** (only if L3 brand style exists)
"Use your on-brand style, or something different?"
- On-brand (default) — applies Visual Brand Style from creative-kit.md
- Different — describe the style you want instead

If user picks "different," their description overrides the brand style for this image only.

**Skip discovery when:** The user's request is specific enough. "Generate a 16:9 blog header showing a glowing terminal on a dark background, warm rim lighting" — don't ask what they want, they just told you.

---

## Phase 2: Prompt Crafting (Nano Banana Prompt Engineering)

You are an expert Nano Banana prompt engineer. Your job is to turn the user's brief into a single, high-quality prompt for Nano Banana 2 (or Pro), a "thinking" image model used for professional asset production.

**Core principle: brief a senior art director, don't list keywords.** Write natural language in full sentences. Never use "tag soup" like "dog, park, 4k, realistic."

### The 10 Rules

**1. General style.** Be specific and descriptive about subject, setting, composition, camera/viewpoint, lighting, mood, materials, and textures. Full sentences, not comma lists.

**2. Context and purpose.** Always encode the purpose and audience (YouTube thumbnail, app icon, hero banner, tweet graphic, 4K wallpaper). Let purpose guide style, polish level, and framing.

**3. Text and infographics.** If text must appear, put it clearly in quotes in the prompt. Ask for legible, clean typography and specify style (bold sans-serif, monospace, handwritten). For data, ask the model to compress into infographics, diagrams, or whiteboards.

**4. Character and brand consistency.** When reference images exist, explicitly refer to them: "Keep the person's facial features exactly the same as Image 1." Allow changes in pose, expression, angle while preserving identity.

**5. Grounding and realism.** For real data, locations, or products, tell the model to rely on up-to-date factual knowledge. Encourage coherent details consistent with physics.

**6. Editing and restoration.** For edits to existing images, give semantic instructions: "remove," "replace," "add," "restore," "change the season." Maintain original structure, only change what's intended.

**7. Dimensional and structural control.** For floor plans, schematics, wireframes, grids, tell the model to follow that layout closely. For 2D↔3D, describe how the new representation should look while preserving key relationships.

**8. Resolution, detail, and format.** Specify resolution ("high detail suitable for 4K wallpaper," "clean 16:9 thumbnail"). Call out micro details and textures when needed (brushed steel, cracked paint, mossy stone).

**9. Narrative and sequences.** For multiple images, describe the story arc, emotional beats, what stays consistent across images. Specify count, format, and identity/style consistency.

**10. Output rules.** Do not ask follow-up questions about the prompt. Resolve small ambiguities with sensible professional defaults. Output a single flowing narrative prompt.

### Prompt Structure

Build the narrative in this order, woven into flowing prose:

1. **Purpose and format** — what this is for, aspect ratio, resolution
2. **Scene** — what's happening, where, environment
3. **Subject** — detailed description with textures, materials, poses
4. **Composition** — framing, focal point, depth of field, negative space
5. **Lighting** — source, quality, color temperature, interaction with materials
6. **Mood** — emotional tone, atmosphere
7. **Text** — any text in quotes with typography specification
8. **Technical** — camera/lens for photorealistic, style reference for illustrated

### Brand Constraints (L3)

When Visual Brand Style exists, weave constraints INTO the narrative — don't add as a separate block:

- Primary Aesthetic → sets overall style direction
- Lighting → overrides generic lighting with brand-specific lighting
- Backgrounds → constrains background treatment
- Composition → constrains layout/framing
- Mood → anchors emotional tone
- Avoid → explicit exclusions baked into prompt
- Reference Prompts → use as structural templates, adapting subject matter

See [references/prompt-patterns.md](references/prompt-patterns.md) for proven patterns.
See [references/visual-metaphors.md](references/visual-metaphors.md) for concept-to-metaphor mapping.

---

## Phase 3: Generate

### Gemini API Call

```python
import os
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

response = client.models.generate_content(
    model="gemini-3.1-flash-image-preview",
    contents=["<narrative prompt>"],
    config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE'],
        image_config=types.ImageConfig(
            aspect_ratio="<ratio>",
            image_size="<resolution>",
        ),
    ),
)

for part in response.parts:
    if part.text:
        print(part.text)
    elif part.inline_data:
        image = part.as_image()
        image.save("output.png")
```

**Default to `gemini-3.1-flash-image-preview` (Nano Banana 2).** Launched Feb 26, 2026. Pro quality at Flash speed/pricing. 4K support, up to 14 reference images for style consistency. Use `gemini-3-pro-image-preview` (Nano Banana Pro) only when text-heavy infographics or premium quality justify the higher cost.

### Save and Log

1. Save image to project directory (e.g., `images/`, `assets/`, or wherever the project keeps visuals)
2. Append to `brand/assets.md`:
   ```
   | <date> | image | <file-path> | image-gen | <1-line description of what was generated> |
   ```

---

## Phase 4: Iterate

After generating, show the image and offer:

"Image generated. Want me to:"
1. Adjust the lighting or mood
2. Change the composition or framing
3. Try a completely different approach
4. Generate more variations
5. Ship it

For adjustments, use Gemini's multi-turn chat API for iterative refinement — pass the previous image + adjustment prompt.

```python
chat = client.chats.create(model="gemini-3-pro-image-preview")
response = chat.send_message("Make the lighting warmer and add more negative space on the left for text")
```

---

## Image Editing

When the user provides an existing image to modify:

```python
from PIL import Image

img = Image.open("input.png")
response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=["<edit instruction>", img],
    config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE'],
    ),
)
```

Supports: style transfer, background replacement, object removal, color grading, text overlay.

---

## Claims Blacklist Awareness

If `brand/landscape.md` exists, check the Claims Blacklist before generating:
- Don't generate imagery that visually implies "the only X" if that claim is blacklisted
- Don't generate competitor comparisons that misrepresent the competitive landscape
- When in doubt, describe the concept to the user and ask if it implies a blacklisted claim

---

## Anti-Patterns

| Anti-pattern | Why it fails | Instead |
|-------------|-------------|---------|
| Listing comma-separated keywords | "professional, modern, tech, blue, minimal" produces generic AI art | Write a narrative: "A single glowing terminal on a dark slate desk, soft amber rim lighting catching the screen edges" |
| Ignoring aspect ratio | Generating 1:1 for a blog header means the user has to crop, losing composition | Always ask where the image goes FIRST — ratio determines everything |
| Overriding brand style silently | User defined a visual brand identity for consistency — ignoring it defeats the purpose | Default to brand style. Only override when user explicitly asks for something different |
| Generating without purpose | "A nice image" produces nothing distinctive | Every image needs a purpose (blog header, social, hero) and a feeling (trust, excitement, calm) |
| Saving as JPEG when PNG needed | Gemini returns JPEG by default — transparency and quality loss | Always convert to PNG with `image.save("output.png", format="PNG")` |
| Skipping the assets log | Future agents won't know what images exist, leading to duplicate generation | Always append to brand/assets.md after generating |

---

## Related Skills

- **/visual-style** — builds the Visual Brand Style section this skill reads
- **/creative** — produces multi-mode creative briefs (not pixels). Route here for ad concepts and video scripts
- **/paper-marketing** — designs in Paper MCP. Route here for carousels, slideshows, and social graphics designed as HTML
- **/app-store-screenshots** — specialized screenshot generator for App Store listings
