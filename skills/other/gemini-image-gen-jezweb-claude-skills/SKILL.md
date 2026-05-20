---
name: gemini-image-gen
description: "Generate images using Google's Gemini API — hero backgrounds, OG images, placeholder photos, textures, and style-matched variants. Uses free-tier models for drafts, paid for finals. No dependencies beyond Python 3. Trigger with 'generate image', 'gemini image', 'make a hero background', 'create placeholder photo', 'generate OG image', 'AI image', or 'need an image for'."
compatibility: claude-code-only
---

# Gemini Image Generator

Generate contextual images for web projects using the Gemini API. Produces hero backgrounds, OG cards, placeholder photos, textures, and style-matched variants.

## Setup

**API Key**: Set `GEMINI_API_KEY` as an environment variable. Get a key from https://aistudio.google.com/apikey if you don't have one.

```bash
export GEMINI_API_KEY="your-key-here"
```

## Workflow

### Step 1: Understand What's Needed

Gather from the user or project context:
- **What**: hero background, product photo, texture, OG image, placeholder
- **Style**: warm/cool/minimal/luxurious/bold — check project's colour palette (input.css, tailwind config)
- **Dimensions**: hero (1920x1080), OG (1200x630), square (1024x1024), custom
- **Count**: single image or multiple variants to choose from

### Step 2: Build the Prompt

Use concrete photography parameters, not abstract adjectives. Read [references/prompting-guide.md](references/prompting-guide.md) for the full framework.

**Quick rules**:
- Narrate like directing a photographer
- Use camera specs: "85mm f/1.8", "wide angle 24mm"
- Use colour anchors from the project palette: "warm terracotta (#C66A52) and cream (#F5F0EB) tones"
- Use lighting descriptions: "golden-hour light from the left, 4500K"
- Always end with: "No text, no watermarks, no logos, no hands"

### Step 3: Generate

Generate a Python script (no dependencies beyond stdlib) that calls the Gemini API. The script should:

1. Read `GEMINI_API_KEY` from environment
2. POST to `https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent`
3. Include `"responseModalities": ["TEXT", "IMAGE"]` in generationConfig
4. Parse the response: extract `inlineData.data` (base64) from candidate parts
5. Decode base64 and save as PNG
6. Support multiple variants (generate N times, save as `name-1.png`, `name-2.png`)

For style matching with a reference image, include the reference as an `inlineData` part before the text prompt, and use temperature 0.7 (instead of 1.0).

See [references/api-pattern.md](references/api-pattern.md) for the full implementation pattern including error handling and response parsing.

**Critical**: Never pass prompts via curl + bash arguments — shell escaping breaks on apostrophes. Always use Python's `json.dumps()` or write the prompt to a file first.

### Step 4: Post-Process (Optional)

Use the **image-processing** skill for resizing, format conversion, or optimisation.

### Step 5: Present to User

Show the generated images for review. Read the image files to display them inline if possible, otherwise describe what was generated and let the user open them.

## Presets

Starting prompts — enhance with project-specific context (colours, mood, subject):

| Preset | Base Prompt |
|--------|-------------|
| `hero-background` | "Wide atmospheric background, soft-focus, [colour tones], [mood], landscape 1920x1080" |
| `og-image` | "Clean branded card background, [brand colours], subtle gradient, 1200x630" |
| `placeholder-photo` | "Professional stock-style photo of [subject], natural lighting, warm tones" |
| `texture-pattern` | "Subtle repeating texture, [material], seamless tile, muted [colour]" |
| `product-shot` | "Product photography, [item] on [surface], soft studio lighting, clean background" |

## Model Selection

| Use case | Model | Cost |
|----------|-------|------|
| Drafts, quick placeholders | `gemini-2.5-flash-image` | Free (~500/day) |
| Final client assets | `gemini-3-pro-image-preview` | ~$0.04/image |
| Style-matched variants | `gemini-3-pro-image-preview` + reference image | ~$0.04/image |

Verify current model IDs if errors occur — they change frequently.

## Reference Files

| When | Read |
|------|------|
| Building effective prompts | [references/prompting-guide.md](references/prompting-guide.md) |
| API implementation details | [references/api-pattern.md](references/api-pattern.md) |
