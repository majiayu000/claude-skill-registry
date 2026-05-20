---
name: nano-banana
description: "AI image generation using Nano Banana PRO (Gemini 3 Pro Image) and Nano Banana (Gemini 2.5 Flash Image). Use this skill when: (1) Generating images from text prompts, (2) Editing existing images, (3) Creating professional visual assets like infographics, logos, product shots, stickers, (4) Working with character consistency across multiple images, (5) Creating images with accurate text rendering, (6) Any task requiring AI-generated visuals. Triggers on: 'generate image', 'create image', 'make a picture', 'design a logo', 'create infographic', 'AI image', 'nano banana', or any image generation request."
---

# Nano Banana PRO Image Generation

Generate professional AI images using Google's Nano Banana models via the Gemini API.

## Prerequisites

- API key must be set as `GEMINI_API_KEY` environment variable
- Uses curl for all API calls (no SDK required)

## Model Selection

| Model | Identifier | Best For |
|-------|------------|----------|
| **Nano Banana PRO** | `gemini-3-pro-image-preview` | Professional assets, text rendering, infographics, 4K output, complex multi-turn editing |
| **Nano Banana** | `gemini-2.5-flash-image` | Fast generation, simple edits, lower cost |

**Default to PRO** for quality work. Use Flash for rapid iterations or simple tasks.

## CRITICAL: Prompt Engineering First

**BEFORE calling the API, always craft an effective prompt.** Read [`references/prompting-guide.md`](references/prompting-guide.md) for comprehensive prompting strategies. Key principles:

### The Golden Rules

1. **Describe scenes, don't list keywords** - Write narrative descriptions, not tag soup
2. **Use natural language** - Full sentences with proper grammar
3. **Be specific** - Define subject, setting, lighting, mood, materials
4. **Provide context** - The "why" helps the model make better artistic decisions
5. **Edit, don't re-roll** - If 80% correct, ask for specific changes

### The ICS Framework (Quick Reference)

For any image, specify:
- **I**mage type: What kind of visual (photo, infographic, logo, sticker, etc.)
- **C**ontent: Specific elements, data, or information to include
- **S**tyle: Visual style, color palette, artistic approach

## API Reference

### Text-to-Image Generation

```bash
curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{
      "parts": [{"text": "YOUR_PROMPT_HERE"}]
    }],
    "generationConfig": {
      "responseModalities": ["TEXT", "IMAGE"],
      "imageConfig": {
        "aspectRatio": "16:9",
        "imageSize": "2K"
      }
    }
  }'
```

### Image Editing (with input image)

```bash
curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{
      "parts": [
        {"text": "YOUR_EDIT_INSTRUCTION"},
        {"inline_data": {"mime_type": "image/png", "data": "BASE64_IMAGE_DATA"}}
      ]
    }],
    "generationConfig": {
      "responseModalities": ["TEXT", "IMAGE"]
    }
  }'
```

### Configuration Options

| Parameter | Values | Notes |
|-----------|--------|-------|
| `aspectRatio` | `1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9` | Match use case |
| `imageSize` | `1K`, `2K`, `4K` | Use uppercase K; PRO model only for 4K |

### Google Search Grounding (Real-time Data)

Add `"tools": [{"google_search": {}}]` to generate images based on current information:

```bash
curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{"parts": [{"text": "Create an infographic of current tech stock prices"}]}],
    "tools": [{"google_search": {}}],
    "generationConfig": {
      "responseModalities": ["TEXT", "IMAGE"],
      "imageConfig": {"aspectRatio": "16:9"}
    }
  }'
```

## Workflow

### Step 1: Craft the Prompt

Use the ICS framework and prompting guide. Examples:

**Photorealistic:**
```
A photorealistic close-up portrait of an elderly Japanese ceramicist with deep wrinkles and a warm smile, inspecting a tea bowl. Soft golden hour light from a window. 85mm lens, shallow depth of field. Serene mood.
```

**Infographic:**
```
Create a clean, modern infographic explaining photosynthesis as a recipe. Show "ingredients" (sunlight, water, CO2) and "finished dish" (energy). Style like a colorful kids' cookbook page.
```

**Product Shot:**
```
High-resolution studio photograph of a matte black ceramic coffee mug on polished concrete. Three-point softbox lighting, 45-degree angle, sharp focus on rising steam. Square format.
```

### Step 2: Generate Image

Use `scripts/generate-image.sh` or call API directly:

```bash
./scripts/generate-image.sh "Your prompt here" output.png --ratio 16:9 --size 2K
```

### Step 3: Process Response

The API returns base64-encoded image data. Extract and decode:

```bash
# Response contains: {"candidates":[{"content":{"parts":[{"inlineData":{"mimeType":"image/png","data":"BASE64..."}}]}}]}
# Extract with jq and decode:
cat response.json | jq -r '.candidates[0].content.parts[] | select(.inlineData) | .inlineData.data' | base64 -d > image.png
```

## Common Use Cases

### Landing Pages & Ads
- Use 16:9 or 21:9 for hero images
- Specify brand colors, modern/minimal style
- Include text requirements in prompt

### Logos & Icons
- Use 1:1 aspect ratio
- Request "minimalist", "clean lines", "vector-style"
- Specify color scheme explicitly

### Product Photography
- Describe lighting setup (softbox, natural, studio)
- Mention surface/background materials
- Include camera angle and lens type

### Infographics
- Define data to visualize
- Specify style (corporate, playful, technical)
- Request clear text and labeled sections

### Stickers & Illustrations
- Request "bold outlines", "kawaii", "cel-shading"
- Specify "white background" or "transparent background"
- Define color palette

### Character Consistency (Multiple Images)
- PRO supports up to 14 reference images
- Explicitly state: "Keep facial features exactly the same as Image 1"
- Describe expression/pose changes while maintaining identity

## Scripts

See [`scripts/generate-image.sh`](scripts/generate-image.sh) for a ready-to-use generation script.

## Detailed Prompting Guide

For advanced techniques including:
- Photorealistic scene templates
- Text rendering best practices  
- Sequential art and storyboarding
- Dimensional translation (2D↔3D)
- Search grounding for real-time data

Read [`references/prompting-guide.md`](references/prompting-guide.md).
