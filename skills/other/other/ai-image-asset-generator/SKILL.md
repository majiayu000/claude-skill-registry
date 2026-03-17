---
name: ai-image-asset-generator
description: This skill should be used when generating AI image assets for websites, landing pages, or applications. It automatically analyzes page requirements, generates images using Gemini API, removes backgrounds, converts to SVG for interactivity, and places assets in frontend code. Ideal for creating hero images, icons, backgrounds, product mockups, and infographic elements. Use this skill when users need image assets for their web projects.
---

# AI Image Asset Generator Skill

## Overview

Automatically generate production-ready image assets for web applications using Google Gemini API. This skill analyzes page requirements, generates multiple assets in batch, processes them (background removal, SVG conversion), and integrates them into frontend code.

## Core Capabilities

### 1. Smart Asset Analysis

Analyze user requirements to determine needed assets:
- **Hero Images**: Main landing page visuals
- **Icon Sets**: Consistent UI icons
- **Backgrounds**: Abstract patterns, gradients
- **Product Mockups**: Screenshots, device frames
- **Infographic Elements**: Charts, diagrams, data visualizations

### 2. Image Generation with Gemini

Generate images using Google Gemini 2.0 Flash:

```bash
# Single image
node scripts/generate-image.js --prompt "modern airport terminal" --output hero.png

# With style
node scripts/generate-image.js --prompt "airplane icon" --style "minimal flat" --size 512x512

# Batch generation
node scripts/batch-generate.js --config assets-config.json
```

### 3. Image Processing Pipeline

**Background Removal** (`scripts/remove-background.js`):
- Remove backgrounds from generated images
- Create transparent PNGs for overlays
- Batch processing support

**PNG to SVG Conversion** (`scripts/png-to-svg.js`):
- Convert raster images to vector SVG
- Makes assets interactable and scalable
- Preserves colors and details

**Asset Optimization** (`scripts/optimize-assets.js`):
- Compress images without quality loss
- Generate multiple sizes (responsive)
- Convert to WebP for modern browsers

### 4. Frontend Integration

Automatically place assets in code:
- React/Next.js components
- HTML/CSS templates
- Proper import statements
- Lazy loading configuration

## Workflow Decision Tree

### 1. What type of project?
- **Landing Page** → Hero image + icons + background
- **Dashboard** → Icons + charts + UI elements
- **E-commerce** → Product images + icons + badges
- **Portfolio** → Hero + gallery images + decorative elements

### 2. What assets needed?
- **Hero Image** → Use `prompt-templates/landing-hero.txt`
- **Icons** → Use `prompt-templates/icon-set.txt`
- **Backgrounds** → Use `prompt-templates/background-abstract.txt`
- **Product Images** → Use `prompt-templates/product-mockup.txt`
- **Infographics** → Use `prompt-templates/infographic-element.txt`

### 3. Post-processing needed?
- **Transparent background** → Run `remove-background.js`
- **Scalable/Interactive** → Run `png-to-svg.js`
- **Web optimized** → Run `optimize-assets.js`

### 4. Integration method?
- **React** → Use `placement-templates/react-image-component.jsx`
- **Next.js** → Use `placement-templates/next-image-component.tsx`
- **HTML/CSS** → Use `placement-templates/html-css-placement.html`

## Usage Examples

### Example 1: Generate Landing Page Assets

**User**: "Build a landing page for an airport website"

**Generated Assets (19 files total)**:
- 4 Hero Images (1920x1080)
- 2 Background Patterns (1920x1080)
- 5 Icons (256x256)
- 5 Transparent Icons (-nobg.png)
- 3 SVG Vectors (first 3 icons)

**Commands**:
```bash
# Generate all assets in one command
node scripts/batch-generate.js --landing-page "airport website" --output ./generated-assets/airport

# Output structure:
# ./generated-assets/airport/
# ├── hero-main.png
# ├── hero-secondary.png
# ├── hero-feature.png
# ├── hero-cta.png
# ├── background-main.png
# ├── background-secondary.png
# ├── icon-primary.png
# ├── icon-primary-nobg.png
# ├── icon-primary.svg
# ├── icon-secondary.png
# ├── icon-secondary-nobg.png
# ├── icon-secondary.svg
# ├── icon-tertiary.png
# ├── icon-tertiary-nobg.png
# ├── icon-tertiary.svg
# ├── icon-quaternary.png
# ├── icon-quaternary-nobg.png
# ├── icon-quinary.png
# └── icon-quinary-nobg.png
```

### Example 2: Generate Icon Set

**User**: "Create icons for my dashboard"

**Steps**:
1. Determine icon types needed
2. Use consistent style prompt
3. Generate batch with same style parameters
4. Remove backgrounds
5. Convert to SVG for interactivity

**Commands**:
```bash
node scripts/generate-image.js \
  --prompt "dashboard analytics icon, minimal line art, white background" \
  --style "consistent, minimal, monoline" \
  --size 256x256 \
  --output icons/analytics.png
```

### Example 3: Create Hero Image with Processing

**User**: "Generate a hero image for tech startup"

**Steps**:
1. Generate hero image
2. Optimize for web
3. Create responsive sizes
4. Place in Next.js Image component

**Commands**:
```bash
# Generate
node scripts/generate-image.js \
  --prompt "futuristic tech startup office, modern, clean, blue accent lighting" \
  --size 1920x1080 \
  --output hero-main.png

# Optimize and create sizes
node scripts/optimize-assets.js \
  --input hero-main.png \
  --sizes "1920,1280,640" \
  --format webp
```

### Example 4: Full Website Asset Generation

**User**: "I want to build this website" (provides description)

**Automated Flow**:
1. **Analyze**: Parse description, identify all needed assets
2. **Plan**: Create asset list with prompts
3. **Generate**: Batch generate all images via Gemini
4. **Process**: Background removal, SVG conversion as needed
5. **Optimize**: Compress, create responsive sizes
6. **Integrate**: Add to project structure, update imports

## Prompt Engineering Guidelines

### Effective Prompts

```
✅ Good: "Modern minimalist airplane icon, flat design, single color,
         white background, centered, high contrast, suitable for UI"

❌ Bad: "airplane icon"
```

### Style Keywords That Work Well

| Category | Keywords |
|----------|----------|
| **Style** | minimal, flat, 3D, isometric, hand-drawn, realistic |
| **Color** | monochrome, vibrant, pastel, gradient, duotone |
| **Mood** | professional, playful, elegant, bold, subtle |
| **Technical** | high contrast, centered, white background, transparent |

### Consistency Tips

For icon sets, include in every prompt:
- Same style descriptor
- Same color palette reference
- Same background specification
- "Consistent with previous icons in set"

## Best Practices

### Image Generation
- Use detailed, specific prompts
- Include style and technical requirements
- Specify background preference (white/transparent)
- Request appropriate resolution

### Processing
- Always remove backgrounds for icons
- Convert to SVG for scalable UI elements
- Optimize all images before deployment
- Create responsive sizes for hero images

### Integration
- Use Next.js Image component for optimization
- Implement lazy loading for below-fold images
- Add proper alt text for accessibility
- Use WebP format with PNG fallback

## Configuration

### Environment Variables

```bash
GEMINI_API_KEY=your_api_key_here
OUTPUT_DIR=./generated-assets
DEFAULT_SIZE=1024x1024
DEFAULT_STYLE=modern, professional
```

### Default Settings (`config/gemini-config.json`)

```json
{
  "model": "gemini-2.0-flash-exp",
  "generationConfig": {
    "temperature": 0.7,
    "topK": 40,
    "topP": 0.95
  },
  "safetySettings": "balanced"
}
```

### Image Presets (`config/image-presets.json`)

```json
{
  "hero": { "width": 1920, "height": 1080 },
  "icon": { "width": 256, "height": 256 },
  "thumbnail": { "width": 400, "height": 300 },
  "background": { "width": 1920, "height": 1080 }
}
```

## Troubleshooting

### API Errors

**Rate Limited**
→ Wait 60 seconds, use batch-generate with delays
→ Check quota in Google Cloud Console

**Invalid API Key**
→ Verify GEMINI_API_KEY environment variable
→ Check key permissions in Google AI Studio

### Image Quality Issues

**Blurry Output**
→ Increase output size
→ Add "high quality, detailed" to prompt

**Inconsistent Style**
→ Use same style keywords across batch
→ Reference previous images in prompt

**Wrong Subject**
→ Be more specific in prompt
→ Add negative prompts ("not X, without Y")

### Processing Errors

**Background Removal Failed**
→ Ensure image has clear subject/background separation
→ Try with higher contrast original

**SVG Conversion Poor Quality**
→ Use simpler source images for SVG
→ Icons work better than photos for SVG

## Quick Reference

```bash
# Generate single image
node scripts/generate-image.js --prompt "your prompt" --output image.png

# Batch generate
node scripts/batch-generate.js --config config.json

# Remove background
node scripts/remove-background.js --input image.png --output transparent.png

# Convert to SVG
node scripts/png-to-svg.js --input image.png --output vector.svg

# Optimize assets
node scripts/optimize-assets.js --input ./images/ --output ./optimized/

# Analyze page needs
node scripts/analyze-page.js --description "landing page for X"
```

## Resources

### Scripts (`scripts/`)
- `generate-image.js` - Core Gemini API integration
- `remove-background.js` - Background removal with sharp
- `png-to-svg.js` - Vectorization with potrace
- `batch-generate.js` - Batch processing with rate limiting
- `analyze-page.js` - Smart asset requirement analysis
- `optimize-assets.js` - Compression and resizing

### Prompt Templates (`assets/prompt-templates/`)
- `landing-hero.txt` - Hero image prompts
- `icon-set.txt` - UI icon prompts
- `background-abstract.txt` - Background pattern prompts
- `product-mockup.txt` - Product image prompts
- `infographic-element.txt` - Data visualization prompts

### Placement Templates (`assets/placement-templates/`)
- `react-image-component.jsx` - React integration
- `next-image-component.tsx` - Next.js with Image optimization
- `html-css-placement.html` - Vanilla HTML/CSS

### References (`references/`)
- `gemini-api-guide.md` - Complete Gemini API documentation
- `prompt-engineering.md` - Writing effective image prompts
- `image-best-practices.md` - Asset optimization guide
- `placement-guidelines.md` - Frontend integration patterns

## Integration with CI/CD

### GitHub Actions

```yaml
- name: Generate Assets
  run: |
    npm install
    node scripts/batch-generate.js --config production-assets.json
  env:
    GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
```

### Pre-commit Hook

```bash
#!/bin/bash
# Optimize any new images before commit
node scripts/optimize-assets.js --input ./src/assets/ --output ./src/assets/
```
