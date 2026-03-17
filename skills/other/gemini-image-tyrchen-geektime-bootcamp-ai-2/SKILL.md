---
name: gemini-image
description: Reference guide for using google-genai Python library to generate images with gemini-3-pro-image-preview model. Use this skill when building new projects that need Gemini image generation capabilities, to understand the correct API patterns, configuration options, and best practices.
---

# Gemini Image Generation Guide

Reference for generating images with Google's `gemini-3-pro-image-preview` model.

## Language References

Load the appropriate reference based on the project's language:

| Language | Reference File         |
|----------|------------------------|
| Python   | `references/python.md` |

**Instructions:** When implementing Gemini image generation, read the corresponding language reference file for complete code patterns and examples.

---

## Model Information

| Property             | Value                        |
|----------------------|------------------------------|
| Model ID             | `gemini-3-pro-image-preview` |
| Cost                 | ~$0.134 per image (2K)       |
| Max Reference Images | 5+ (high fidelity)           |
| Resolutions          | 1K, 2K, 4K                   |

## Supported Aspect Ratios

| Ratio  | Use Case                   |
|--------|----------------------------|
| `1:1`  | Square, social media posts |
| `2:3`  | Portrait photos            |
| `3:2`  | Landscape photos           |
| `3:4`  | Portrait, mobile screens   |
| `4:3`  | Standard display           |
| `4:5`  | Instagram portrait         |
| `5:4`  | Large format               |
| `9:16` | Vertical video, stories    |
| `16:9` | Widescreen, presentations  |
| `21:9` | Ultra-wide, cinematic      |

## Image Sizes

| Size | Resolution | Use Case                      |
|------|------------|-------------------------------|
| `1K` | ~1024px    | Thumbnails, previews          |
| `2K` | ~2048px    | Standard output (recommended) |
| `4K` | ~4096px    | High-quality prints           |

**Important:** Use uppercase "K" (not "1k", "2k", "4k").

---

## Environment Setup

```bash
export GOOGLE_API_KEY='your-api-key-here'
```

---

## Core Capabilities

### 1. Text-to-Image Generation

Generate images from text descriptions with configurable aspect ratio and resolution.

### 2. Style Transfer with Reference Images

Pass reference images to maintain consistent style across generations. Supports up to 5+ images for high fidelity.

### 3. Image Editing

Modify existing images based on text instructions (add/remove elements, style changes).

### 4. Batch Generation

Generate multiple style candidates or variations.

---

## Prompt Engineering Tips

### Be Descriptive

```
Bad:  "cat, sunset"
Good: "A fluffy orange tabby cat sitting on a wooden fence,
       watching a vibrant sunset over rolling hills.
       Warm golden and pink light illuminates the scene.
       Photorealistic style with soft focus background."
```

### Specify Visual Elements

- **Lighting:** "soft morning light", "dramatic side lighting", "golden hour"
- **Style:** "oil painting", "watercolor", "3D render", "photorealistic"
- **Mood:** "serene", "dramatic", "whimsical", "mysterious"
- **Composition:** "close-up portrait", "wide landscape", "bird's eye view"
- **Camera:** "35mm lens", "shallow depth of field", "wide angle"

### For Style Transfer

When using reference images, be explicit about what to transfer:

- "Match the color palette and brushstroke style of the reference"
- "Keep the artistic mood and lighting from the reference image"

---

## Common Issues

| Issue                | Solution                                                    |
|----------------------|-------------------------------------------------------------|
| "No image generated" | Check prompt for content policy violations; simplify prompt |
| "Invalid image_size" | Use uppercase: `"1K"`, `"2K"`, `"4K"`                       |
| "API key not found"  | Set `GOOGLE_API_KEY` environment variable                   |
| Rate limits          | Add delays between requests; use exponential backoff        |

---

## Pricing Comparison

| Model                      | Cost per Image |
|----------------------------|----------------|
| gemini-3-pro-image-preview | ~$0.134        |
| gemini-2.5-flash-image     | ~$0.039        |
