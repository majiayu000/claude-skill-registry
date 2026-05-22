---
name: api-ai-claude-vision
description: Image understanding and document analysis with Claude's multimodal capabilities -- image input formats, PDF processing, multi-image patterns, structured extraction, and token cost estimation
---

# Claude Vision Patterns

> **Quick Guide:** Use `type: "image"` content blocks for images (base64, URL, or file_id) and `type: "document"` content blocks for PDFs. Supported image formats: JPEG, PNG, GIF, WebP. Images before text in the content array improves results. Token cost formula: `tokens = (width * height) / 750`. Images are auto-resized if the long edge exceeds 1568px or exceeds ~1600 tokens. PDFs use `type: "document"` with `media_type: "application/pdf"`. No OCR library needed -- Claude reads text directly from images and PDFs.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use `type: "image"` for images and `type: "document"` for PDFs -- they are different content block types)**

**(You MUST place images and documents BEFORE text in the content array -- Claude performs better with visual content first)**

**(You MUST always provide `max_tokens` in every request -- it is required and has no default)**

**(You MUST iterate over `response.content` blocks -- never assume a single text block in the response)**

**(You MUST use named constants for max_tokens, token budgets, and pixel limits -- no magic numbers)**

</critical_requirements>

---

**Auto-detection:** Claude vision, image analysis, image input, base64 image, URL image, type image, type document, media_type image/jpeg, media_type image/png, image/webp, image/gif, application/pdf, PDF processing, document extraction, multimodal, multi-image, image comparison, chart analysis, screenshot analysis, image understanding, visual content, vision API

**When to use:**

- Sending images to Claude for analysis, description, or data extraction
- Processing PDF documents for text extraction, chart analysis, or summarization
- Comparing multiple images in a single request
- Extracting structured data from screenshots, receipts, charts, or forms
- Building document processing pipelines with Claude
- Estimating token costs for image-heavy workloads

**Key patterns covered:**

- Image input via base64, URL, and Files API
- PDF document input and processing
- Multi-image requests and comparison patterns
- Image + text prompting best practices
- Token cost estimation and image sizing
- Structured data extraction from visual content
- Multi-turn vision conversations
- Prompt caching with images and PDFs

**When NOT to use:**

- General Claude API usage without images or documents -- use the Anthropic SDK skill instead
- Image generation or editing -- Claude is understanding-only, it cannot create or modify images
- Identifying specific people in images -- Claude refuses to name people (Anthropic policy)
- Medical diagnostic imaging (CTs, MRIs) -- not designed for clinical diagnosis

---

## Examples Index

- [Core: Image & PDF Input](examples/core.md) -- Base64, URL, file_id, PDF input, multi-image, token estimation
- [Extraction & Prompting](examples/extraction.md) -- Structured extraction, comparison, prompting best practices, caching
- [Quick API Reference](reference.md) -- Content block types, supported formats, size limits, token formula

---

<philosophy>

## Philosophy

Claude's vision capabilities treat images and documents as **first-class content blocks** alongside text. There is no separate "vision API" -- you add image or document blocks to the same Messages API you already use for text.

**Core principles:**

1. **Images are content blocks, not attachments** -- Images and PDFs are content blocks in the `messages` array, interleaved with text. They are not uploaded separately or referenced by URL-only.
2. **Image-first ordering** -- Place images before text in the content array. This mirrors how `documents first, query last` improves text prompts. Claude processes visual content better when it sees the image before the question.
3. **No OCR needed** -- Claude reads text directly from images and PDFs. You do not need to pre-extract text with an OCR library. For PDFs, Claude processes both the extracted text and a rendered image of each page.
4. **Token costs scale with pixels** -- Image tokens are proportional to resolution: `tokens = (width * height) / 750`. Downsizing images before sending saves tokens without losing meaningful detail for most use cases.
5. **PDFs are dual-processed** -- Each PDF page is converted to an image AND has its text extracted. Claude sees both, giving it access to visual layout and textual content.

**When to use vision:**

- Analyzing screenshots, photos, charts, diagrams, or infographics
- Extracting data from forms, receipts, invoices, or tables
- Processing PDF documents for summarization, extraction, or analysis
- Comparing multiple images (before/after, A/B testing, design review)
- Understanding visual context that text alone cannot capture

**When NOT to use:**

- Pure text tasks with no visual component -- vision adds unnecessary token cost
- Tasks requiring pixel-perfect spatial precision -- Claude's spatial reasoning is approximate
- Identifying specific people -- Claude refuses to name individuals (Anthropic policy)
- Replacing professional medical imaging analysis (CTs, MRIs, X-rays)

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Base64 Image Input

Read a local file, encode to base64, send as `type: "image"` content block. Image block before text block.

```typescript
// Image block first, text prompt second, iterate response content blocks
content: [
  {
    type: "image",
    source: { type: "base64", media_type: "image/png", data: imageData },
  },
  { type: "text", text: "Describe what you see in this image." },
];
```

**Why good:** Image before text improves results, explicit media_type, structured content blocks

```typescript
// BAD: base64 as text string -- Claude cannot interpret raw base64
content: "What's in this image? " + imageData;
```

**Why bad:** Passing base64 as text string instead of image content block, Claude cannot interpret raw base64 text as an image

**See:** [examples/core.md](examples/core.md) for full runnable examples with base64, URL, and Files API

---

### Pattern 2: URL vs Base64 vs Files API

Three source types for images. Choose based on where your image lives.

```typescript
// URL source -- simplest, smallest payload
source: { type: "url", url: "https://example.com/chart.png" }

// Base64 source -- local files
source: { type: "base64", media_type: "image/jpeg", data: base64String }

// Files API source (beta) -- upload once, reuse across requests
source: { type: "file", file_id: "file_abc123" }
```

**When to use:** URL for hosted images, base64 for local files, Files API for multi-turn or repeated use

**See:** [examples/core.md](examples/core.md) for full examples of each source type

---

### Pattern 3: PDF Document Input

PDFs use `type: "document"` -- different from `type: "image"`. This is the most common mistake.

```typescript
// Correct: type "document" for PDFs
{ type: "document", source: { type: "base64", media_type: "application/pdf", data: pdfData } }

// WRONG: type "image" for PDFs -- causes API errors
{ type: "image", source: { type: "base64", media_type: "application/pdf", data: pdfData } }
```

**Why good:** `type: "document"` enables dual processing (text extraction + page rendering)

**Why bad:** Using `type: "image"` for PDFs causes API errors. PDFs require `type: "document"`.

**See:** [examples/core.md](examples/core.md) for base64 and URL PDF examples, [examples/extraction.md](examples/extraction.md) for PDF caching

---

### Pattern 4: Multiple Images with Labels

Label images with text blocks so Claude can reference them clearly.

```typescript
content: [
  { type: "text", text: "Image 1:" },
  {
    type: "image",
    source: { type: "base64", media_type: "image/jpeg", data: image1 },
  },
  { type: "text", text: "Image 2:" },
  {
    type: "image",
    source: { type: "base64", media_type: "image/jpeg", data: image2 },
  },
  {
    type: "text",
    text: "Compare these two images and describe the differences.",
  },
];
```

**Why good:** Labels let Claude reference specific images unambiguously

**Why bad (without labels):** Claude may confuse which image is which when no labels are provided

**See:** [examples/core.md](examples/core.md) for full multi-image example

---

### Pattern 5: Token Cost Estimation

Token formula: `tokens = (width * height) / 750`. Auto-resize triggers at 1568px long edge or ~1.15 megapixels.

```typescript
const TOKENS_PER_PIXEL_DIVISOR = 750;
const MAX_LONG_EDGE_PX = 1568;
const MAX_MEGAPIXELS = 1.15;

function estimateImageTokens(width: number, height: number): number {
  let w = width,
    h = height;
  const longEdge = Math.max(w, h);
  const mp = (w * h) / 1_000_000;
  if (longEdge > MAX_LONG_EDGE_PX || mp > MAX_MEGAPIXELS) {
    const scale = Math.min(
      MAX_LONG_EDGE_PX / longEdge,
      Math.sqrt(MAX_MEGAPIXELS / mp),
    );
    w = Math.round(width * scale);
    h = Math.round(height * scale);
  }
  return Math.ceil((w * h) / TOKENS_PER_PIXEL_DIVISOR);
}
// 200x200: ~54 tokens | 1000x1000: ~1334 | 4000x3000: ~1590 (auto-resized)
```

**Why good:** Named constants, accounts for auto-resize, documents the formula

**See:** [reference.md](reference.md) for the complete size/token/cost table, [examples/core.md](examples/core.md) for `countTokens()` usage

---

### Pattern 6: Structured Data Extraction

Combine vision with `messages.parse()` and Zod schemas for typed extraction.

```typescript
import { zodOutputFormat } from "@anthropic-ai/sdk/helpers/zod";
import { z } from "zod";

const ReceiptData = z.object({
  merchant: z.string(),
  date: z.string(),
  items: z.array(
    z.object({ name: z.string(), quantity: z.number(), price: z.number() }),
  ),
  total: z.number(),
  currency: z.string(),
});

const response = await client.messages.parse({
  model: "claude-sonnet-4-6",
  max_tokens: MAX_TOKENS,
  messages: [
    {
      role: "user",
      content: [
        {
          type: "image",
          source: {
            type: "base64",
            media_type: "image/jpeg",
            data: receiptImage,
          },
        },
        {
          type: "text",
          text: "Extract all receipt information from this image.",
        },
      ],
    },
  ],
  output_config: { format: zodOutputFormat(ReceiptData) },
});

const receipt = response.parsed_output; // fully typed
```

**Why good:** Zod schema for type-safe extraction, `messages.parse()` for auto-validation, image before text

**See:** [examples/extraction.md](examples/extraction.md) for chart extraction, form extraction, multi-document extraction, PDF caching

</patterns>

---

<performance>

## Performance Optimization

### Image Sizing Strategy

```
Image resolution vs token cost:
200x200   -> ~54 tokens    ($0.00016/image at Sonnet 4.6 pricing)
1000x1000 -> ~1334 tokens  ($0.004/image)
1092x1092 -> ~1590 tokens  ($0.0048/image) -- max 1:1 without auto-resize
4000x3000 -> ~1590 tokens  (auto-resized to fit 1568px long edge)
```

- **Pre-resize images** to no more than 1568px on the long edge and 1.15 megapixels to avoid auto-resize latency
- **Small images** under 200px on any edge may degrade output quality
- **Images over 8000x8000px** are rejected outright
- **20+ images** in one request limits each image to 2000x2000px max

### Cost Reduction Techniques

- **Resize before sending** -- A 4000x3000 image is auto-resized to the same tokens as 1092x1092, but adds latency. Pre-resize to save time.
- **Use URL sources** when images are already hosted -- avoids encoding overhead and reduces request payload size
- **Use the Files API** for images used across multiple requests -- upload once, reference by `file_id`
- **Cache PDFs** with `cache_control: { type: "ephemeral" }` when asking multiple questions about the same document
- **Use token counting** (`client.messages.countTokens()`) before expensive requests to estimate costs

### PDF Token Costs

- Text extraction: ~1,500-3,000 tokens per page depending on density
- Image rendering: Each page also incurs image token costs (same formula)
- Total per page: text tokens + image tokens (dual processing)

</performance>

---

<decision_framework>

## Decision Framework

### Image Source Type

```
Where is your image?
+-- Local file        -> Base64 encode with readFileSync().toString("base64")
+-- Public URL        -> Use type: "url" source (simplest, smallest payload)
+-- Already uploaded  -> Use type: "file" source with file_id (Files API, beta)
+-- Multiple requests -> Upload once via Files API, reuse file_id
```

### Image vs Document Block

```
What type of file?
+-- JPEG, PNG, GIF, WebP -> type: "image"
+-- PDF                  -> type: "document" with media_type: "application/pdf"
+-- Other formats        -> Convert to a supported format first
```

### Token Budget for max_tokens

```
What kind of analysis?
+-- Brief description    -> 256-512 max_tokens
+-- Detailed analysis    -> 1024-2048 max_tokens
+-- Document summarization -> 2048-4096 max_tokens
+-- Structured extraction  -> 1024 max_tokens (JSON output is compact)
```

</decision_framework>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Using `type: "image"` for PDFs -- PDFs require `type: "document"` with `media_type: "application/pdf"`
- Passing base64 data as a text string instead of an image content block -- Claude cannot interpret raw base64 text
- Not providing `max_tokens` -- required on every request, no default
- Images larger than 8000x8000px -- rejected by the API
- API file size limit is 5MB per image (10MB on claude.ai)

**Medium Priority Issues:**

- Placing text before images in the content array -- Claude performs better with images first
- Not labeling multiple images -- Claude may confuse which image is which without "Image 1:", "Image 2:" labels
- Sending full-resolution images when a smaller version would suffice -- wastes tokens and adds latency from auto-resizing
- Using base64 for publicly available images -- URL source is simpler and reduces payload
- Not using `cache_control` when asking multiple questions about the same PDF -- each request re-processes the full document

**Common Mistakes:**

- Expecting Claude to generate or edit images -- it is understanding-only
- Using vision for tasks requiring precise spatial reasoning (exact pixel coordinates, analog clock reading) -- Claude's spatial abilities are approximate
- Relying on Claude to identify specific people -- it refuses to name individuals per Anthropic policy
- Assuming exact object counts -- Claude gives approximate counts, especially for many small objects
- Forgetting that PDF pages are dual-processed (text + image) -- token costs are higher than text-only

**Gotchas & Edge Cases:**

- Images under 200px on any edge may produce lower quality analysis
- When sending 20+ images in a single request, each image is limited to 2000x2000px max
- API supports up to 600 images per request (100 for 200k context window models), but request size limits (32MB) are often reached first
- Claude does not read image EXIF metadata -- orientation, camera info, GPS data are not accessible
- PDFs with passwords or encryption are not supported -- only standard PDFs
- The Files API for images and documents is currently in beta (`betas: ["files-api-2025-04-14"]`)
- Multi-turn vision conversations do not require re-sending the image -- it persists in conversation history
- For PDFs, dense pages with complex tables or heavy graphics can fill the context window before reaching the 600-page limit

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use `type: "image"` for images and `type: "document"` for PDFs -- they are different content block types)**

**(You MUST place images and documents BEFORE text in the content array -- Claude performs better with visual content first)**

**(You MUST always provide `max_tokens` in every request -- it is required and has no default)**

**(You MUST iterate over `response.content` blocks -- never assume a single text block in the response)**

**(You MUST use named constants for max_tokens, token budgets, and pixel limits -- no magic numbers)**

**Failure to follow these rules will produce API errors, degraded vision quality, unexpected token costs, or runtime crashes from untyped content blocks.**

</critical_reminders>
