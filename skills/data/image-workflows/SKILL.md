---
name: image-workflows
description: Create and execute image workflows using floimg. Use when the user needs
  to generate AI images, transform existing images (resize, caption, filters), or
  create multi-step pipelines. Also handles chart
---

---
name: image-workflows
description: Create and execute image workflows using floimg. Use when the user needs to generate AI images, transform existing images (resize, caption, filters), or create multi-step pipelines. Also handles charts, diagrams, QR codes, and screenshots. Trigger words: image, picture, photo, illustration, hero, thumbnail, resize, transform, caption, watermark, generate, AI, DALL-E, chart, diagram, QR, screenshot.
allowed-tools: mcp__floimg__generate_image, mcp__floimg__transform_image, mcp__floimg__save_image, mcp__floimg__run_pipeline, mcp__floimg__analyze_image, Bash
---

# Image Workflows Skill

This skill enables you to create and execute image workflows using floimg—the composable workflow engine with two core differentiators:

1. **Deterministic Transforms**: AI image modification is probabilistic—DALL-E generates new images, inpainting runs diffusion. FloImg applies deterministic transforms: adjust hue mathematically, resize to exact dimensions. The image stays intact except for exactly what you requested.

2. **A Unified API**: FloImg models image manipulation as a series of composable steps. This functional approach consolidates the patchwork of tools and SDKs into one abstraction layer—portable across SDK, CLI, visual builder, and MCP.

## Architecture: CLI Simple, MCP Complex

floimg uses a hybrid approach:

| Task Type                                  | Method        | Works Immediately? |
| ------------------------------------------ | ------------- | ------------------ |
| Complex (AI images, multi-step, iteration) | MCP           | After restart      |
| Simple (QR, chart, diagram, screenshot)    | CLI via `npx` | Yes                |

## When to Use This Skill

Activate this skill when the user:

- Wants to generate AI images (DALL-E, etc.) with professional finishing
- Needs to transform images (resize, add caption, adjust colors, apply filters)
- Wants iterative refinement ("make it more vibrant", "add a caption")
- Wants to save images to cloud storage (S3, R2, Tigris)
- Describes a multi-step image workflow (generate → transform → save)
- Also: charts, diagrams, QR codes, screenshots

## Simple Tasks (Use CLI)

For one-shot operations, use the floimg CLI:

```bash
# Resize an image
npx -y @teamflojo/floimg resize hero.png 1200x630 -o ./og-image.png

# Convert format
npx -y @teamflojo/floimg convert image.png -o image.webp

# Add caption
npx -y @teamflojo/floimg caption image.png "© 2025 Acme" -o ./watermarked.png

# AI image (requires OPENAI_API_KEY)
npx -y @teamflojo/floimg generate --generator openai --prompt "..." -o ./image.png

# Also: charts, diagrams, QR, screenshots
npx -y @teamflojo/floimg qr "https://example.com" -o ./qr.png
npx -y @teamflojo/floimg chart bar --labels "Q1,Q2,Q3" --values "10,20,30" -o ./chart.png
```

These work immediately with no configuration.

## Complex Tasks (Use MCP)

For multi-step workflows, iteration, and transforms, use MCP tools:

### Available MCP Tools

- `generate_image` - Generate with intent-based routing
- `transform_image` - Apply transforms to existing images
- `save_image` - Save to filesystem or cloud
- `run_pipeline` - Execute multi-step workflows
- `analyze_image` - AI vision analysis

### If MCP is not available

For complex workflows, inform the user:
"Multi-step image workflows work best with MCP. Restart Claude Code once to enable the floimg MCP server for session state and iteration."

## Why Session State Matters

This is FloImg's core advantage over raw LLM + DALL-E:

| Task                  | Without FloImg                           | With FloImg MCP                 |
| --------------------- | ---------------------------------------- | ------------------------------- |
| "Create a hero image" | Generates image                          | Generates + stores as `img_001` |
| "Make it 1200x630"    | Re-generates entirely (different image!) | Resizes exact pixels            |
| "Make it bluer"       | Start over                               | Adjusts hue on existing image   |

**The key insight**: When you say "make it more vibrant," FloImg adjusts the existing image—it doesn't re-generate a new one. AI handles creation. FloImg handles precision.

## Generator Selection Guide

| User Intent                   | Generator  | Method                      |
| ----------------------------- | ---------- | --------------------------- |
| Photo/illustration/hero/scene | openai     | MCP `generate_image` or CLI |
| Product mockup, creative      | openai     | MCP for iteration           |
| Bar/line/pie chart            | quickchart | CLI `chart TYPE`            |
| Flowchart/sequence/diagram    | mermaid    | CLI `diagram "CODE"`        |
| QR code/barcode               | qr         | CLI `qr "TEXT"`             |
| Webpage screenshot            | screenshot | CLI `screenshot "URL"`      |

## Workflow Patterns

### Pattern 1: AI Image with Transforms (MCP preferred)

```
User: "Create a hero image for my blog, resize to 1200x630, add my tagline"

1. generate_image({ intent: "hero image for tech blog about AI" }) → imageId
2. transform_image({ imageId, operation: "resize", params: { width: 1200, height: 630 } })
3. transform_image({ imageId, operation: "addCaption", params: { text: "AI for Everyone" } })
4. save_image({ imageId, destination: "./hero.png" })
```

### Pattern 2: Iterative Refinement (MCP required)

```
User: "Create a hero image for my blog"
→ generate_image(...) → imageId: "img_001"

User: "Make it more vibrant"
→ transform_image({ imageId: "img_001", operation: "modulate", params: { saturation: 1.3 } })

User: "Add a caption"
→ transform_image({ imageId: "img_002", operation: "addCaption", params: { text: "..." } })
```

**Session state is crucial here**: Each transform references the previous result by imageId. No file uploads, no re-generation—just precise refinements.

### Pattern 3: Full Pipeline (MCP)

```
User: "Create a hero image, resize for social, add caption, upload to S3"

run_pipeline({
  steps: [
    { generate: { intent: "hero image..." } },
    { transform: { operation: "resize", params: { width: 1200, height: 630 } } },
    { transform: { operation: "addCaption", params: { text: "...", position: "bottom" } } },
    { save: { destination: "s3://bucket/hero.png" } }
  ]
})
```

## Best Practices

1. **AI workflows → MCP**: Generate + transform + iterate benefits from session state
2. **Simple generators → CLI**: `/floimg:qr`, `/floimg:chart` for one-shot output
3. **Use imageId for chaining**: Reference previous images without file juggling
4. **Resize last**: Apply quality-degrading transforms before final resize
5. **Choose right format**: PNG for photos, WebP for web, SVG for diagrams

For detailed API reference, see [reference.md](reference.md).
For common workflow examples, see [examples.md](examples.md).
