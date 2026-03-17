---
name: image-gen
description: Generate website images with Gemini 3 Native Image Generation. Covers hero banners, service cards, infographics with legible text, and multi-turn editing. Includes Australian-specific imagery patterns. Use when stock photos don't fit, need text in images, or require consistent style across assets. Prevents 5 documented errors.
license: MIT
metadata:
  last_verified: "2026-01-21"
---

# Image Generation Skill

Generate and edit website images using Gemini Native Image Generation.

## ⚠️ Critical: SDK Migration Required

**IMPORTANT**: The `@google/generative-ai` package is deprecated as of November 30, 2025. All new projects must use `@google/genai`.

**Migration Required**:
```typescript
// ❌ OLD (deprecated, support ended Nov 30, 2025)
import { GoogleGenerativeAI } from "@google/generative-ai";
const genAI = new GoogleGenerativeAI(API_KEY);

// ✅ NEW (required)
import { GoogleGenAI } from "@google/genai";
const ai = new GoogleGenAI({ apiKey: API_KEY });
```

**Source**: [GitHub Repository Migration Notice](https://github.com/google-gemini/deprecated-generative-ai-js)

## Models

| Model | ID | Status | Best For |
|-------|-----|--------|----------|
| **Gemini 3 Pro Image** | `gemini-3-pro-image-preview` | Preview (Nov 20, 2025) | 4K, complex prompts, text |
| **Gemini 2.5 Flash Image** | `gemini-2.5-flash-image` | GA (Oct 2, 2025) | Fast iteration, general use |
| **Imagen 4.0** | `imagen-4.0-generate-001` | GA (Aug 14, 2025) | Alternative platform |

**Deprecated Models** (do not use):
- `gemini-2.0-flash-exp-image-generation` - Shut down Nov 11, 2025
- `gemini-2.0-flash-preview-image-generation` - Shut down Nov 11, 2025
- `gemini-2.5-flash-image-preview` - Scheduled shutdown Jan 15, 2026

**Source**: [Google AI Changelog](https://ai.google.dev/gemini-api/docs/changelog)

## Capabilities

| Feature | Supported |
|---------|-----------|
| Generate from text | ✅ |
| Edit existing images | ✅ |
| Change aspect ratio | ✅ |
| Widen/extend images | ✅ |
| Style transfer | ✅ |
| Change colours | ✅ |
| Add/remove elements | ✅ |
| Text in images | ✅ (legible!) |
| Multiple reference images | ✅ (up to 14: max 5 humans, 9 objects) |
| 4K resolution | ✅ (Pro only) |

**Note**: Exceeding 5 human reference images causes unpredictable character consistency. Keep human images ≤ 5 for reliable results.

## Aspect Ratios

```
1:1   | 2:3  | 3:2  | 3:4  | 4:3
4:5   | 5:4  | 9:16 | 16:9 | 21:9
```

## Resolutions (Pro only)

| Size | 1:1 | 16:9 | 4:3 |
|------|-----|------|-----|
| 1K | 1024x1024 | 1376x768 | 1184x880 |
| 2K | 2048x2048 | 2752x1536 | 2368x1760 |
| 4K | 4096x4096 | 5504x3072 | 4736x3520 |

## Quick Start

```typescript
import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });

// Generate new image
const response = await ai.models.generateContent({
  model: "gemini-2.5-flash-image",
  contents: "A professional plumber in hi-vis working in modern Australian home",
  config: {
    responseModalities: ["TEXT", "IMAGE"],  // BOTH required - cannot use ["IMAGE"] alone
    imageGenerationConfig: {
      aspectRatio: "16:9",
    },
  },
});

// Extract image
for (const part of response.candidates[0].content.parts) {
  if (part.inlineData) {
    const buffer = Buffer.from(part.inlineData.data, "base64");
    fs.writeFileSync("hero.png", buffer);
  }
}
```

**Important**: `responseModalities` must include both `["TEXT", "IMAGE"]`. Using `["IMAGE"]` alone may fail or produce unexpected results.

## Model Selection

| Requirement | Use |
|-------------|-----|
| Fast iteration | Gemini 2.5 Flash Image |
| 4K resolution | Gemini 3 Pro Image Preview |
| Text in images | Gemini 3 Pro (94% legibility at 4K) |
| Simple edits | Gemini 2.5 Flash Image |
| Complex compositions | Gemini 3 Pro Image Preview |
| Infographics/diagrams | Gemini 3 Pro Image Preview |

**Text Rendering Benchmarks** (4K resolution):
- Gemini 3 Pro Image: 94% legible text
- DALL-E 3: 78% legible text
- Midjourney: Decorative pseudo-text only

## When to Use

**Use Gemini Image Gen when:**
- Stock photos don't fit brand/context
- Need Australian-specific imagery
- Need text in images (infographics, diagrams)
- Need consistent style across multiple images
- Need to edit/modify existing images
- Client has no photos of their work

**Don't use when:**
- Client has good photos of actual work
- Real team photos needed (discuss first)
- Product shots (use real products)
- Legal/compliance concerns

## Known Issues Prevention

This skill prevents **5** documented issues:

### Issue #1: Resolution Parameter Case Sensitivity
**Error**: Request fails with invalid parameter error
**Source**: [Google AI Image Generation Docs](https://ai.google.dev/gemini-api/docs/image-generation)
**Why It Happens**: Resolution values are case-sensitive and must use uppercase 'K'.
**Prevention**: Always use `"4K"`, `"2K"`, `"1K"` - never lowercase `"4k"`.

```typescript
// ❌ WRONG - causes request failure
config: { imageGenerationConfig: { resolution: "4k" } }

// ✅ CORRECT - uppercase required
config: { imageGenerationConfig: { resolution: "4K" } }
```

### Issue #2: Aspect Ratio May Be Ignored (Sept 2025+)
**Error**: Returns 1:1 square image despite requesting 16:9 or other ratios
**Source**: [Google Support Thread](https://support.google.com/gemini/thread/371311134/)
**Why It Happens**: Backend update in September 2025 affected Gemini 2.5 Flash Image model's aspect ratio handling.
**Prevention**: Use Gemini 3 Pro Image Preview for reliable aspect ratio control, or generate 1:1 and use multi-turn editing to extend.

```typescript
// May ignore aspectRatio on Gemini 2.5 Flash Image
model: "gemini-2.5-flash-image",
config: { imageGenerationConfig: { aspectRatio: "16:9" } }

// More reliable for aspect ratio control
model: "gemini-3-pro-image-preview",
config: { imageGenerationConfig: { aspectRatio: "16:9" } }
```

**Status**: Google confirmed working on fix (Sept 2025).

### Issue #3: Exceeding 5 Human Reference Images
**Error**: Unpredictable character consistency in generated images
**Source**: [Google AI Image Generation Docs](https://ai.google.dev/gemini-api/docs/image-generation)
**Why It Happens**: Gemini 3 Pro Image supports up to 14 reference images total, but only 5 can be human images for character consistency.
**Prevention**: Limit human images to 5 or fewer. Use remaining slots (up to 14 total) for objects/scenes.

```typescript
// ❌ WRONG - 7 human images exceeds limit
const humanImages = [img1, img2, img3, img4, img5, img6, img7];
const prompt = [
  { text: "Generate consistent characters" },
  ...humanImages.map(img => ({ inlineData: { data: img, mimeType: "image/png" }})),
];

// ✅ CORRECT - max 5 human images
const humanImages = images.slice(0, 5);  // Limit to 5
const objectImages = images.slice(5, 14);  // Up to 9 more for objects
const prompt = [
  { text: "Generate consistent characters" },
  ...humanImages.map(img => ({ inlineData: { data: img, mimeType: "image/png" }})),
  ...objectImages.map(img => ({ inlineData: { data: img, mimeType: "image/png" }})),
];
```

### Issue #4: SynthID Watermark Cannot Be Disabled
**Error**: N/A (documented limitation)
**Source**: [Google AI Image Generation Docs](https://ai.google.dev/gemini-api/docs/image-generation)
**Why It Happens**: All generated images automatically include a SynthID watermark for content authenticity tracking.
**Prevention**: Be aware of this limitation for commercial use cases. Watermark cannot be disabled by developers.

### Issue #5: Google Search Grounding Excludes Image Results
**Error**: Generated images don't reflect visual search results, only text
**Source**: [Google AI Image Generation Docs](https://ai.google.dev/gemini-api/docs/image-generation)
**Why It Happens**: When using Google Search tool with image generation, "image-based search results are not passed to the generation model."
**Prevention**: Only text-based search results inform the visual output. Don't expect the model to reference images from search results.

```typescript
// Google Search tool enabled
const response = await ai.models.generateContent({
  model: "gemini-3-pro-image-preview",
  contents: "Generate image of latest iPhone design",
  tools: [{ googleSearch: {} }],
  config: { responseModalities: ["TEXT", "IMAGE"] },
});
// Result: Only text search results used, not image results from web search
```

## Pricing

**Current Pricing** (as of November 2025):
- **Gemini 2.5 Flash Image**: ~$0.008 per image
  - Input: 258 tokens per image
  - Output: 1290 tokens per image
  - Rate: $30.00 per 1M output tokens

**Note**: The `generateImages` API (Imagen models) does not return `usageMetadata` in responses. Track costs manually based on pricing above.

**Source**: [Google Developers Blog - Gemini 2.5 Flash Image](https://developers.googleblog.com/introducing-gemini-2-5-flash-image/)

## Reference Files

- `references/prompting.md` - Effective prompt patterns
- `references/website-images.md` - Hero, service, background templates
- `references/editing.md` - Multi-turn editing patterns
- `references/local-imagery.md` - Australian-specific details
- `references/integration.md` - API code examples

---

**Last verified**: 2026-01-21 | **Skill version**: 2.0.0 | **Changes**: Added SDK migration notice (critical), updated to current model names (gemini-3-pro-image-preview, gemini-2.5-flash-image), added 5 Known Issues (resolution case sensitivity, aspect ratio bug, reference image limits, SynthID watermark, Google Search grounding), added pricing section, added text rendering benchmarks.
