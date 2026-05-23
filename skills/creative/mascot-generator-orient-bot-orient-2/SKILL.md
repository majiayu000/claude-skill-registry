---
name: mascot-generator
description: 'Generate variations of the Orient mascot (border collie dog with blue bandana). Use transparent=true for web/UI images. Use when asked to generate mascot, create avatar variation, make mascot image, mascot with different pose/expression, or any request for mascot customization.'
---

# Mascot Generator

Generate on-the-fly variations of the Orient mascot (Ori the border collie with blue bandana).

## Quick Start

### Generate a mascot with transparent background (recommended for web/UI)

```json
{
  "variation_type": "pose",
  "prompt": "friendly waving pose, clean cartoon style",
  "output_name": "waving",
  "transparent": true
}
```

### Generate a mascot with background (faster, for non-web use)

```json
{
  "variation_type": "seasonal",
  "prompt": "wearing a Santa hat with snowy background",
  "output_name": "winter-holiday"
}
```

## Tool: `ai_first_generate_mascot`

### Parameters

| Parameter        | Required | Description                                                                            |
| ---------------- | -------- | -------------------------------------------------------------------------------------- |
| `variation_type` | Yes      | One of: `pose`, `expression`, `background`, `seasonal`, `accessory`, `style`, `custom` |
| `prompt`         | Yes      | Detailed description of the desired variation                                          |
| `output_name`    | No       | Filename (without extension) for the generated image                                   |
| `transparent`    | No       | **Set to `true` for transparent PNG** (uses OpenAI, requires OPENAI_API_KEY)           |

### The `transparent` Parameter

**IMPORTANT:** This is the key parameter for web/UI mascots.

| `transparent`     | Backend            | Result                    | Use Case                               |
| ----------------- | ------------------ | ------------------------- | -------------------------------------- |
| `true`            | OpenAI gpt-image-1 | PNG with alpha channel    | Landing pages, UI components, overlays |
| `false` (default) | Gemini Nano Banana | PNG with solid background | Marketing materials, social media      |

### Variation Types

**pose** - Different body positions

- "sitting attentively", "waving hello", "running joyfully", "lying down relaxed"

**expression** - Facial expressions

- "thinking deeply", "happy and excited", "surprised", "focused and determined"

**background** - Scene/environment changes (only when `transparent: false`)

- "office setting with monitors", "outdoors in a park", "abstract geometric pattern"

**seasonal** - Holiday and seasonal themes

- "wearing Santa hat with snow", "spring flowers blooming", "Halloween costume"

**accessory** - Add items to the mascot

- "wearing sunglasses", "holding a coffee cup", "with a laptop", "wearing headphones"

**style** - Art style transformations

- "pixel art 8-bit", "watercolor painting", "minimalist line art"

**custom** - Free-form variations

- Any combination or creative prompt

## Usage Examples

### Mascot for landing page hero (transparent)

```json
{
  "variation_type": "pose",
  "prompt": "full body sitting attentively, alert friendly expression, ready to help",
  "output_name": "hero-attentive",
  "transparent": true
}
```

### Mascot for loading state (transparent)

```json
{
  "variation_type": "expression",
  "prompt": "thinking pose with paw on chin, looking upward thoughtfully",
  "output_name": "loading",
  "transparent": true
}
```

### Mascot for error page (transparent)

```json
{
  "variation_type": "expression",
  "prompt": "apologetic expression, slightly worried but helpful look",
  "output_name": "error",
  "transparent": true
}
```

### Mascot for celebration (transparent)

```json
{
  "variation_type": "accessory",
  "prompt": "wearing a party hat, celebrating with happy expression",
  "output_name": "celebration",
  "transparent": true
}
```

### Holiday mascot with background

```json
{
  "variation_type": "seasonal",
  "prompt": "wearing cozy winter sweater and Santa hat, snowy festive background",
  "output_name": "winter-2026"
}
```

## Output

The tool returns:

- `success` - Whether generation succeeded
- `message` - Success/error message
- `path` - Relative URL (e.g., `/mascot/variations/celebration.png`)
- `fullPath` - Absolute file path
- `variationType` - The type used
- `prompt` - The prompt used

Images are saved to `packages/dashboard/frontend/public/mascot/variations/`.

## Requirements

| Feature                 | Required                                             |
| ----------------------- | ---------------------------------------------------- |
| Basic generation        | `GEMINI_API_KEY`                                     |
| Transparent backgrounds | `OPENAI_API_KEY`                                     |
| Base mascot             | `packages/dashboard/frontend/public/mascot/base.png` |

## Best Practices

1. **Always use `transparent: true` for web/UI** - Transparent backgrounds integrate better with any theme
2. **Be specific in prompts** - Include pose, expression, and accessories for best results
3. **Use descriptive names** - Name files by use case (e.g., `loading`, `error`, `celebration`)
4. **Check existing variations** - Before generating, check `/mascot/variations/` for reusable images
5. **Full body for heroes** - Use "full body" in prompt for landing page mascots
6. **Portrait for icons** - Omit "full body" for smaller UI elements

## Web Integration

```tsx
// Transparent background mascot (recommended)
<img
  src="/mascot/variations/hero-attentive.png"
  alt="Ori mascot"
  className="w-64 h-auto object-contain"
/>

// Responsive sizing
<img
  src="/mascot/variations/loading.png"
  alt="Loading..."
  className="w-24 h-24 md:w-32 md:h-32 object-contain"
/>
```

- Use `object-contain` to preserve aspect ratio
- Generated images are 1024x1024 - use CSS for sizing
- Always include descriptive alt text

## Troubleshooting

### Generated image has solid background

- **Cause:** `transparent` parameter not set or set to `false`
- **Fix:** Add `"transparent": true` to your request

### "OPENAI_API_KEY not set" error

- **Cause:** Trying to use `transparent: true` without API key
- **Fix:** Add `OPENAI_API_KEY=sk-...` to your `.env` file

### Image doesn't look like the mascot

- **Cause:** Prompt too vague or too different from base style
- **Fix:** Include "border collie dog with blue bandana, cartoon style" context

### Generation is slow

- OpenAI generation (transparent) takes 15-30 seconds
- Gemini generation (non-transparent) takes 5-10 seconds

## Cross-Platform Usage

This tool works from:

- **WhatsApp/Slack** - "Generate a mascot waving with transparent background"
- **Cursor/Claude Code** - Call `ai_first_generate_mascot` with `transparent: true`
- **Scripts** - Use the MCP tool programmatically

## Common Mascot Variations

| Use Case             | Suggested Prompt                                                                                                                                                                                                                                                                                    | Transparent |
| -------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------- |
| Hero section         | "full body sitting attentively, friendly expression"                                                                                                                                                                                                                                                | Yes         |
| Loading state        | "thinking with paw on chin, looking upward"                                                                                                                                                                                                                                                         | Yes         |
| Error page           | "apologetic expression, slightly worried"                                                                                                                                                                                                                                                           | Yes         |
| Success              | "celebrating with happy expression"                                                                                                                                                                                                                                                                 | Yes         |
| Empty state          | "curious and friendly, looking around"                                                                                                                                                                                                                                                              | Yes         |
| Welcome              | "waving hello cheerfully"                                                                                                                                                                                                                                                                           | Yes         |
| Working              | "wearing headphones like tech support"                                                                                                                                                                                                                                                              | Yes         |
| Holiday              | "wearing Santa hat, snowy background"                                                                                                                                                                                                                                                               | No          |
| **Favicon/Tab icon** | "simple minimalist favicon icon design, just the face/head tightly cropped, bold thick outlines, very simple shapes, high contrast, no fine fur details, focus on recognizable silhouette with bright blue bandana accent, designed to look great at 32x32 pixels, flat design, clean vector style" | No          |

## Favicon / Small Icon Best Practices

When generating mascots for favicons or small tab icons (16x16 to 32x32 pixels):

1. **Use `style` variation type** - This allows for icon-optimized styling
2. **Request simplified design** - Include phrases like "bold thick outlines", "simple shapes", "high contrast"
3. **Tight crop on face** - Specify "just the face/head tightly cropped"
4. **Avoid fine details** - Request "no fine fur details" to prevent muddy appearance
5. **Emphasize silhouette** - Request "focus on recognizable silhouette"
6. **Don't use transparent** - Favicons render better with solid backgrounds

### Example Favicon Generation

```json
{
  "variation_type": "style",
  "prompt": "simple minimalist favicon icon design, just the face/head tightly cropped, bold thick outlines, very simple shapes, high contrast, no fine fur details, focus on recognizable silhouette with bright blue bandana accent, designed to look great at 32x32 pixels, flat design, clean vector style",
  "output_name": "favicon"
}
```
