---
name: image-generator
description: Generate branded images using Google Gemini's image generation API. Supports multiple formats (LinkedIn headers, Medium headers, square concepts, vertical explainers). Reads brand guidelines from the project's BRAND.md file for consistent visual identity.
allowed-tools: Bash, Read, Write, Grep
---

<!--
  Original source: Sandhya Simhan's blog repo
  Generalized for claude-code-quickstart SDK
-->

# Image Generator

Generates professional branded images using Google Gemini's image generation API. Automatically reads brand guidelines from the target project to ensure visual consistency.

## How It Works

1. **Brand Discovery**: Looks for brand guidelines in the project (see Brand Configuration below)
2. **Format Selection**: User chooses image format (LinkedIn, Medium, Square, Vertical)
3. **Prompt Crafting**: Combines user request + brand guidelines + format specs
4. **Generation**: Calls Gemini API to generate the image
5. **Output**: Saves to configured output directory

## Brand Configuration

The skill looks for brand guidelines in this order:
1. `BRAND.md` in project root
2. `.claude/BRAND.md`
3. `docs/BRAND.md`

If no brand file exists, the skill will prompt you to create one (see BRAND_TEMPLATE.md).

### Minimal BRAND.md Example

```markdown
# Brand Guidelines

## Colors
- **Primary:** #0078AA (Teal)
- **Background:** #F4F1EB (Off-white)
- **Accent:** #F69F22 (Yellow)

## Style
- Modern minimalist
- Hand-drawn/illustrated feel
- Generous whitespace

## Tone
- Professional but friendly
- Approachable, not corporate
```

## Image Formats

| Format | Dimensions | Aspect Ratio | Best For |
|--------|------------|--------------|----------|
| LinkedIn | 1200×630 | 16:9 | Social sharing, OG tags, blog headers |
| Medium | 1200×400 | 3:1 | Substack/Medium headers, newsletters |
| Square | 1080×1080 | 1:1 | Instagram, Twitter, concept cards |
| Vertical | 1080×1920 | 9:16 | Stories, mobile-first, Pinterest |

See [IMAGE_FORMATS.md](./IMAGE_FORMATS.md) for detailed layout tips.

## Instructions

When the user requests an image:

### 1. Find Brand Guidelines
```
Read BRAND.md (or alternative locations) to understand:
- Color palette (primary, accent, neutral colors)
- Visual style (minimalist, illustrated, corporate, etc.)
- Emotional tone (friendly, professional, playful, etc.)
- Design elements to include/avoid
```

If no brand file exists, ask if they want to create one or proceed with defaults.

### 2. Determine Format & Output
- Ask which format they need (or default to LinkedIn 1200×630)
- Determine output directory:
  - Default: `assets/images/` or `_assets/images/`
  - Use existing image directory if one exists
  - Or ask user preference

### 3. Gather Requirements
- Blog post topic/title
- Key themes or concepts to visualize
- Specific elements to include
- Level of detail (high-level concept vs detailed)

### 4. Craft Brand-Aligned Prompt

Build a detailed prompt that includes:
- **Exact dimensions** for the chosen format
- **Background color** from brand guidelines
- **Primary and accent colors** from brand palette
- **Visual style** from brand guidelines
- **Composition** appropriate for the format
- **Emotional tone** matching brand voice

**Prompt Template:**
```
Create a [style] image ([dimensions]) for [topic].

Background: Use [background color] as the background.

Visual style: [brand style description]. Use [primary color] as the
primary anchor color with subtle accents of [accent colors]. Include
[design elements from brand].

Composition: [format-specific layout guidance].

Mood: [brand emotional tone]. [Additional mood guidance].
```

### 5. Generate Image

Run the generator script:
```bash
python [skill-path]/generate_image.py \
  --prompt "your detailed prompt" \
  --output "filename.png" \
  --output-dir "assets/images" \
  --image-type linkedin
```

### 6. Provide Output
- Show the generated image path
- Provide markdown snippet: `![Alt text](path/to/image.png)`
- Offer to regenerate with adjustments
- Offer additional formats if needed

## Setup Requirements

### 1. Google Gemini API Key
```bash
export GEMINI_API_KEY="your-api-key-here"
```
Get a key at: https://aistudio.google.com/apikey

### 2. Python Dependencies
```bash
pip install google-genai pillow
```

### 3. Output Directory
The skill will create the output directory if it doesn't exist.

## Tips for Great Images

**Format-Specific:**
- **LinkedIn**: Horizontal flow, leave left/right third for text
- **Medium**: Wide cinematic feel, text at top/bottom
- **Square**: Centered, icon-like clarity, standalone
- **Vertical**: Top-to-bottom flow, can show progression

**General:**
- Clarity over complexity
- Generous whitespace
- Intentional color use (don't use all accent colors at once)
- Match the brand's visual metaphor style

## Example Session

**User**: "Generate a header for my post about API design patterns"

**Skill**:
1. Reads BRAND.md → finds teal primary, illustrated style
2. Asks: "Which format? LinkedIn (default), Medium, Square, or Vertical?"
3. User: "LinkedIn"
4. Asks: "Key visual metaphor? (e.g., building blocks, pipelines, contracts)"
5. User: "Building blocks connecting"
6. Crafts prompt with brand colors + dimensions + metaphor
7. Generates image → saves to `assets/images/api-design-linkedin.png`
8. Returns: `![API Design Patterns](assets/images/api-design-linkedin.png)`
