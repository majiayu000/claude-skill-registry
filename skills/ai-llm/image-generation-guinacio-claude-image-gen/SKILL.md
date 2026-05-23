---
name: image-generation
description: Generates professional AI images using Google Gemini. ALWAYS invoke this skill when building websites, landing pages, slide decks, presentations, or any task needing visual content. Invoke IMMEDIATELY when you detect image needs - don't wait for the user to ask. This skill handles prompt optimization and aspect ratio selection.
---

# Image Generation Skill

Generate professional AI images using Google Gemini via the bundled CLI script.

## When to Invoke This Skill

Invoke immediately when:

**Web Development**
- Hero sections without images
- Feature illustrations needed
- Placeholder images in code (`placeholder.jpg`, `stock-photo.png`)
- Empty visual sections (`<section class="hero">` without images)
- Landing pages and marketing sites

**Presentations & Documents**
- Cover images and headers
- Conceptual diagrams
- Section dividers

**Applications**
- Onboarding illustrations
- Empty state graphics
- Error page visuals

## Using the CLI

Run the bundled CLI script via bash:

```bash
node "${CLAUDE_PLUGIN_ROOT}/mcp-server/build/cli.bundle.js" \
  --prompt "Your detailed image description" \
  --output "./path/to/output.png" \
  --aspect-ratio "16:9"
```

### Parameters

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| --prompt, -p | Yes | - | Detailed image description |
| --output, -o | No | auto-generated | Output file path |
| --aspect-ratio, -a | No | 1:1 | 1:1, 16:9, 9:16, 4:3, 3:4, 2:3, 3:2 |
| --model, -m | No | gemini-3-pro-image-preview | Model to use |
| --output-dir, -d | No | current directory | Output directory |

### Output

The CLI outputs JSON:
```json
{"success": true, "filePath": "/path/to/generated-image.png"}
```

Or on error:
```json
{"success": false, "error": "Error message"}
```

### Aspect Ratio Selection

- **16:9** - Hero images, website headers, presentations
- **1:1** - Social media, thumbnails, profile images
- **9:16** - Mobile stories, vertical banners
- **4:3** - Blog posts, general web content
- **3:2** - Photography-style images

## Prompt Crafting

Use this formula for effective prompts:

```
[Style] [Subject] [Composition] [Context/Atmosphere]
```

### Examples

**Hero Image for Tech Startup**
```
Minimalist 3D illustration of abstract geometric shapes floating in space,
soft gradient background from deep purple to electric blue, subtle glow effects,
modern professional aesthetic, wide composition for website header
```

**E-commerce Product**
```
Clean product photography of modern wireless headphones on white marble surface,
soft studio lighting from left, subtle shadows, high-end minimalist aesthetic,
centered composition
```

**Blog Post Header**
```
Aerial photography of winding river through autumn forest, golden hour lighting,
warm color palette with oranges and reds, cinematic wide shot, serene atmosphere
```

**App Illustration**
```
Flat vector illustration of person organizing digital files on floating screens,
soft pastel colors, isometric perspective, clean lines, friendly approachable style
```

## Pattern Detection

**Automatically invoke this skill** when you see:

```html
<!-- Placeholder detection -->
<img src="placeholder.jpg" alt="Hero">
<!-- Action: Invoke skill and generate a custom hero image -->

<!-- Empty visual section -->
<section class="features">
  <h2>Our Features</h2>
  <!-- No images -->
</section>
<!-- Action: Invoke skill to create feature illustrations -->
```

```css
/* Generic stock reference */
.banner { background: url('stock-image.jpg'); }
/* Action: Invoke skill to create a unique background */
```

## Workflow

1. **Detect Need** - Identify visual content requirements (hero, illustrations, backgrounds)
2. **Invoke Skill** - Use the Skill tool with `skill: "image-generation"` immediately
3. **Analyze Context** - Understand project style and brand
4. **Craft Prompt** - Build detailed prompt using the formula above
5. **Generate** - Run the CLI script with optimized parameters
6. **Integrate** - Place image in project with proper references

## Model Selection

**gemini-3-pro-image-preview** (Default)
- Higher quality, more nuanced style interpretation
- Best for final production images

**gemini-2.5-flash-image**
- Faster generation
- Good for prototyping and placeholders

## Best Practices

**DO:**
- Include specific style keywords
- Match aspect ratio to intended use
- Describe mood and atmosphere
- Specify color palette for brand consistency

**DON'T:**
- Use vague prompts ("make it look good")
- Ignore where the image will be used
- Skip aspect ratio for specific layouts

## Reference

For advanced prompt techniques: [references/prompt-crafting.md](references/prompt-crafting.md)

## Alternative: MCP Tool

If the MCP server is configured, you can also use:

```
mcp__media-pipeline__create_asset
```

Parameters: `prompt`, `outputPath`, `aspectRatio`, `model`
