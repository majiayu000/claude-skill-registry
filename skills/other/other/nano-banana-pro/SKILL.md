---
name: nano-banana-pro
description: Generate and edit high-quality images using Google's Nano Banana Pro (Gemini 3 Pro Image) AI model. Use this skill when working with AI image generation or editing tasks including (1) Creating images from text prompts with professional quality, (2) Editing existing images with natural language instructions, (3) Multi-turn iterative image refinement, (4) Product photography and marketing visuals, (5) Creating infographics and diagrams with text, (6) Photorealistic and artistic image generation, (7) Batch image generation workflows, (8) Testing and troubleshooting Gemini image generation API. Supports up to 4K resolution, multiple aspect ratios, reference images, and advanced prompting techniques for cinema-quality results.
---

# Nano Banana Pro (Gemini 3 Pro Image)

Generate and edit professional-quality images using Google's state-of-the-art Gemini 3 Pro Image model.

## API Configuration

Set your Gemini API key as an environment variable:

```bash
export GEMINI_API_KEY="your-api-key-here"
```

Get your API key at: https://aistudio.google.com/apikey

## Quick Start

### Test API Connection

Before generating images, verify API credentials:

```bash
python scripts/test_connection.py --api-key YOUR_KEY
```

Or set environment variable:

```bash
export GEMINI_API_KEY="your-api-key-here"
python scripts/test_connection.py
```

### Generate Image from Text

```bash
python scripts/generate_image.py "A futuristic cityscape at sunset, neon lights, cyberpunk style"
```

With options:

```bash
python scripts/generate_image.py "Portrait of a cat" \
  --aspect-ratio 9:16 \
  --temperature 0.7 \
  --output ./my_images \
  --filename cat_portrait
```

### Edit Existing Image

```bash
python scripts/edit_image.py "Make the sky more dramatic with storm clouds" input.jpg
```

With options:

```bash
python scripts/edit_image.py "Change car color to red" photo.png \
  --aspect-ratio 16:9 \
  --output ./edited \
  --filename red_car
```

## Core Workflows

### 1. Text-to-Image Generation

**When to use**: Creating images from scratch based on text descriptions.

**Process**:

1. **Craft effective prompt** using best practices from `references/prompting-guide.md`
2. **Run generation script** with appropriate parameters
3. **Review output** and iterate if needed

**Example**:

```bash
# High-quality product photography
python scripts/generate_image.py \
  "High-end product photography of luxury watch on black marble, dramatic single key light from top-left, reflective surface, macro lens, f/5.6, commercial quality, 4K" \
  --aspect-ratio 1:1 \
  --temperature 0.5
```

**Key considerations**:
- Use specific, detailed prompts (see [Prompting Best Practices](#prompting-best-practices))
- Choose appropriate aspect ratio for use case
- Lower temperature (0.3-0.5) for consistency, higher (0.8-1.0) for creativity
- Iterate with multi-turn editing for complex requirements

### 2. Image Editing & Refinement

**When to use**: Modifying existing images with natural language instructions.

**Process**:

1. **Identify specific changes** needed
2. **Use precise editing instructions** with action verbs (Add, Change, Make, Remove, Replace)
3. **Run edit script** with source image
4. **Chain multiple edits** for complex transformations

**Example - Single Edit**:

```bash
python scripts/edit_image.py \
  "Add flying birds in the upper right sky" \
  landscape.jpg \
  --output ./edited
```

**Example - Multi-turn refinement**:

```bash
# Edit 1: Change time of day
python scripts/edit_image.py "Convert to sunset lighting" day_scene.jpg \
  --output ./step1 --filename sunset

# Edit 2: Add elements using output from step 1
python scripts/edit_image.py "Add warm street lamps glowing" ./step1/sunset_image_0_0.jpg \
  --output ./step2 --filename with_lamps

# Edit 3: Fine-tune atmosphere
python scripts/edit_image.py "Make the sky more orange and dramatic" ./step2/with_lamps_image_0_0.jpg \
  --output ./final --filename final
```

**Key considerations**:
- Be specific about which elements to change
- Use positional language ("in the background", "on the left")
- Keep original aspect ratio unless intentionally changing
- Each edit builds on previous result

### 3. Batch Generation

**When to use**: Generating multiple variations or different images in sequence.

**Process**:

Create a shell script or Python wrapper:

```bash
#!/bin/bash
# batch_generate.sh

PROMPTS=(
  "Modern office workspace, minimalist design"
  "Cozy coffee shop interior, warm lighting"
  "Professional meeting room, corporate aesthetic"
)

for i in "${!PROMPTS[@]}"; do
  python scripts/generate_image.py "${PROMPTS[$i]}" \
    --output ./batch_output \
    --filename "scene_$i" \
    --aspect-ratio 16:9

  echo "Generated image $((i+1))/${#PROMPTS[@]}"
  sleep 2  # Rate limiting
done
```

### 4. Reference-Based Generation

**When to use**: Maintaining style consistency or character consistency across images.

**Process**:

1. **Prepare reference images** (up to 14 images)
2. **Create prompt referencing style/character** to maintain
3. **Use Python SDK or API directly** for multi-image upload

**Example using Python**:

```python
from generate_image import NanoBananaProClient
from pathlib import Path
import base64

client = NanoBananaProClient(api_key="YOUR_KEY")

# Read reference images
ref_images = []
for img_path in ["ref1.jpg", "ref2.jpg", "ref3.jpg"]:
    with open(img_path, "rb") as f:
        img_data = base64.b64encode(f.read()).decode()
        ref_images.append({
            "inlineData": {
                "mimeType": "image/jpeg",
                "data": img_data
            }
        })

# Generate with references
# (Requires direct API call with multiple inlineData parts)
```

## Prompting Best Practices

### Essential Structure

Follow this formula for best results:

```
[Subject] + [Style/Medium] + [Lighting Details] + [Camera/Composition] + [Quality Modifiers]
```

**Example**:
```
"Portrait of elderly craftsman | Documentary photography style | Soft window light from left | 85mm lens, f/2.8, shallow DOF | Professional editorial quality, sharp focus on eyes"
```

### Key Principles

1. **Be Specific**: Vague prompts → generic results
   - ❌ "a sunset"
   - ✅ "golden hour sunset over mountain range, vibrant orange and purple clouds, silhouetted pine trees in foreground"

2. **Use Cinematic Language**: Nano Banana Pro responds well to photography terms
   - Lens: "24mm wide-angle" | "85mm portrait" | "200mm telephoto"
   - Lighting: "soft diffused" | "harsh direct" | "backlit with rim lighting"
   - Camera: "low-angle shot" | "overhead view" | "Dutch angle tilt"

3. **Layer Descriptions**: Build depth with atmosphere, materials, mood
   - "Cozy library, warm amber lighting, leather chairs, rain visible through tall windows, steam rising from tea cup on oak table"

4. **Iterate with Multi-Turn**: Start simple, refine progressively
   - Turn 1: "Modern kitchen, white cabinets"
   - Turn 2: "Add marble countertops"
   - Turn 3: "Make the lighting warmer, golden hour through windows"

### Cinematic Digital Painting Style

For **documentary-style digital paintings** with warm golden lighting, painterly brush strokes, and atmospheric depth, see the dedicated style guide:

**[`cinematic-style.md`](cinematic-style.md)** - Complete formula, key elements, examples, and technical notes

Quick reference:
- Warm golden/amber lighting with dramatic rim lighting
- Painterly brush strokes with visible texture
- Soft bokeh depth-of-field for atmospheric background blur
- High contrast (deep blacks + bright highlights)
- Temperature: 0.6 for balanced consistency/creativity

**For complete prompting guide, see**: `references/prompting-guide.md`

## Script Reference

### generate_image.py

Generate images from text prompts.

**Parameters**:
- `prompt` (required): Text description of image
- `--api-key`: API key (or use `GEMINI_API_KEY` env var)
- `--aspect-ratio`: 1:1 | 3:4 | 4:3 | 9:16 | 16:9 (default: 16:9)
- `--temperature`: 0.0-1.0 (default: 0.7)
- `--output`: Output directory (default: ./output)
- `--filename`: Base filename (default: generated)
- `--verbose`: Show full API response

**Common use cases**:
```bash
# Quick generation
python scripts/generate_image.py "red sports car"

# High-quality consistent output
python scripts/generate_image.py "professional headshot" \
  --temperature 0.4 --aspect-ratio 3:4

# Creative exploration
python scripts/generate_image.py "abstract art" --temperature 0.9

# Debug mode
python scripts/generate_image.py "test prompt" --verbose
```

### edit_image.py

Edit existing images with natural language instructions.

**Parameters**:
- `prompt` (required): Edit instruction
- `image` (required): Path to input image
- `--api-key`: API key (or use `GEMINI_API_KEY` env var)
- `--aspect-ratio`: Output aspect ratio
- `--temperature`: Creativity level
- `--output`: Output directory (default: ./output)
- `--filename`: Base filename (default: edited)
- `--verbose`: Show full API response

**Common editing patterns**:
```bash
# Localized changes
python scripts/edit_image.py "Make the car red" photo.jpg

# Atmospheric changes
python scripts/edit_image.py "Convert to night scene" day.jpg

# Add elements
python scripts/edit_image.py "Add mountains in background" landscape.jpg

# Remove elements
python scripts/edit_image.py "Remove person from left side" group.jpg

# Style transforms
python scripts/edit_image.py "Apply vintage film look" modern.jpg
```

### test_connection.py

Test API connectivity and verify credentials.

**Parameters**:
- `--api-key`: API key to test
- `--json`: Output as JSON for scripting

**Usage**:
```bash
# Interactive test
python scripts/test_connection.py --api-key YOUR_KEY

# Automated testing
python scripts/test_connection.py --json | jq '.success'
```

### generate_with_references.py

Generate images using style reference images (up to 14).

**Parameters**:
- `prompt` (required): Text description of image to generate
- `references` (required): One or more reference image paths (up to 14)
- `--api-key`: API key (or use `GEMINI_API_KEY` env var)
- `--aspect-ratio`: 1:1 | 2:3 | 3:2 | 3:4 | 4:3 | 4:5 | 5:4 | 9:16 | 16:9 | 21:9 (default: 1:1)
- `--resolution`: 1K | 2K | 4K (default: 2K)
- `--output`: Output directory (default: ./output)
- `--filename`: Base filename (default: generated)
- `--verbose`: Show detailed output

**Usage**:
```bash
# Generate avatar matching reference style
python scripts/generate_with_references.py \
  "Portrait of elderly craftsman in same artistic style as references" \
  ref1.png ref2.jpg ref3.png \
  --output ./output \
  --filename craftsman

# Character consistency across images
python scripts/generate_with_references.py \
  "Same character in a coffee shop scene" \
  character_ref1.png character_ref2.png \
  --aspect-ratio 16:9 \
  --resolution 2K
```

**Best practices**:
- Include style description in prompt ("same artistic style", "match the lighting")
- Use consistent reference images (same art style, lighting, color palette)
- Reference images can include characters, objects, or style examples
- Up to 14 images: 6 for objects, 5 for character consistency

## Advanced Techniques

### Multi-Resolution Workflow

Generate quick previews, then upscale finals:

```bash
# 1. Quick iteration at 1K (implied by default, fastest)
python scripts/generate_image.py "concept art spaceship" \
  --filename concept_draft

# 2. Review output, refine prompt

# 3. Generate final at higher quality with refined prompt
python scripts/generate_image.py "detailed concept art of sleek sci-fi spaceship, studio lighting, 4K quality, sharp details" \
  --temperature 0.5 \
  --filename concept_final
```

### Temperature Strategies

- **0.3-0.5**: Product photography, technical diagrams, consistency required
- **0.7** (default): Balanced - most use cases
- **0.8-0.9**: Creative exploration, artistic styles, abstract art

### Aspect Ratio Selection

- **1:1** - Social media posts, profile images, icons
- **16:9** - Presentations, YouTube thumbnails, website headers
- **9:16** - Mobile stories, vertical video thumbnails, app screens
- **4:3 / 3:4** - Traditional photography, portrait work
- **4:5** - Instagram posts (use 4:3 as closest)

## Troubleshooting

### Common Issues

1. **API Key Not Working**
   ```bash
   # Verify key format and test
   python scripts/test_connection.py --api-key YOUR_KEY
   ```

2. **Rate Limiting**
   - Free tier: ~100 requests/day, 2-5/minute
   - Add delays between requests: `sleep 2`
   - Implement exponential backoff (see `references/troubleshooting.md`)

3. **Low Quality Output**
   - Use more specific prompts
   - Lower temperature for consistency (0.5)
   - Add quality modifiers: "4K", "professional", "sharp focus"
   - Check input image resolution (editing)

4. **Model Not Found (404)**
   - Verify model name: `gemini-3-pro-image-preview`
   - Check if geo-blocked (Europe/MENA)
   - Try VPN or alternative model

5. **Content Policy Violation**
   - Remove references to violence, explicit content
   - Avoid copyrighted characters
   - Don't reference real public figures without permission
   - Rephrase to be less explicit

**For detailed troubleshooting, see**: `references/troubleshooting.md`

## API Details

### Pricing

- **1K/2K images**: $0.134 per image
- **4K images**: $0.24 per image
- **Image inputs** (editing): $0.0011 per image

### Rate Limits

**Free Tier**:
- ~100 requests/day
- 2-5 requests/minute
- 1 concurrent request

**Paid Tier**:
- Unlimited daily (subject to quota)
- 60 requests/minute
- 10 concurrent requests

### Supported Formats

**Input** (editing): JPEG, PNG, WebP
**Output**: JPEG, PNG (specified via API)

**For complete API reference, see**: `references/api-reference.md`

## Integration Patterns

### Python Integration

```python
from scripts.generate_image import NanoBananaProClient

# Initialize client
client = NanoBananaProClient(api_key="YOUR_KEY")

# Generate image
response = client.generate_image(
    prompt="Professional product photo",
    aspect_ratio="1:1",
    temperature=0.6
)

# Save results
from pathlib import Path
saved = client.save_images_from_response(
    response,
    output_dir=Path("./output"),
    base_filename="product"
)

print(f"Saved to: {saved}")
```

### Bash/Shell Workflows

```bash
#!/bin/bash
# Simple workflow automation

export GEMINI_API_KEY="your-key"

# Generate multiple variations
for style in "modern" "vintage" "minimal"; do
  python scripts/generate_image.py \
    "$style office interior" \
    --filename "office_${style}" \
    --output ./variations
  sleep 2
done

echo "Generated ${#styles[@]} variations"
```

### Error Handling Pattern

```python
import time

def generate_with_retry(prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = client.generate_image(prompt)
            return response
        except Exception as e:
            if "429" in str(e):  # Rate limited
                wait = 2 ** attempt  # Exponential backoff
                print(f"Rate limited, waiting {wait}s...")
                time.sleep(wait)
            else:
                raise
    raise Exception("Max retries exceeded")
```

## Example Use Cases

### Marketing Campaign

```bash
# Generate hero image
python scripts/generate_image.py \
  "Dynamic marketing hero image for tech startup, modern professional team collaborating, bright office space, cinematic color grading, 16:9" \
  --temperature 0.6 \
  --output ./campaign \
  --filename hero

# Generate social media variant
python scripts/edit_image.py \
  "Crop to square focusing on center, increase contrast" \
  ./campaign/hero_image_0_0.jpg \
  --aspect-ratio 1:1 \
  --output ./campaign \
  --filename social
```

### Content Creation

```bash
# Blog header
python scripts/generate_image.py \
  "Blog header for article about sustainable architecture, modern green building with vertical gardens, clear sky, professional editorial photography, 16:9" \
  --filename blog_header

# Thumbnail for video
python scripts/generate_image.py \
  "YouTube thumbnail style, bold composition about productivity tips, vibrant colors, text space on left third, eye-catching" \
  --aspect-ratio 16:9 \
  --filename thumbnail
```

### Product Mockups

```bash
# Product shot
python scripts/generate_image.py \
  "High-end product photography of minimalist desk lamp on marble surface, soft studio lighting from right, black background, commercial quality" \
  --aspect-ratio 1:1 \
  --temperature 0.4 \
  --filename product_main

# Lifestyle context
python scripts/edit_image.py \
  "Place in modern home office setting with laptop and plants" \
  product_main_image_0_0.jpg \
  --filename product_lifestyle
```

## Resources

### Documentation Files

- **Prompting Guide** (`references/prompting-guide.md`): Best practices, examples, techniques
- **API Reference** (`references/api-reference.md`): Complete API documentation, pricing, SDKs
- **Troubleshooting** (`references/troubleshooting.md`): Common issues, solutions, error codes
- **Example Prompts** (`assets/example-prompts.md`): Ready-to-use prompts by category
- **Aldea Avatars** (`references/aldea-avatars.md`): Character templates for Soul Engine personas

### External Links

- **Google AI Studio**: https://aistudio.google.com (get API key, free tier)
- **Official Docs**: https://ai.google.dev/gemini-api/docs
- **Pricing Page**: https://ai.google.dev/gemini-api/docs/pricing
- **Model Info**: https://deepmind.google/models/gemini-image/pro/
- **Vertex AI Console**: https://console.cloud.google.com/vertex-ai (enterprise)

### Getting API Key

1. Visit https://aistudio.google.com
2. Sign in with Google account
3. Click "Get API key" in left sidebar
4. Create new project or select existing
5. Generate API key
6. Store securely (never commit to git)

```bash
# Store in environment
export GEMINI_API_KEY="AIzaSy..."

# Or in .env file (add to .gitignore!)
echo "GEMINI_API_KEY=AIzaSy..." >> .env
```

## Tips & Tricks

1. **Cache results**: Avoid regenerating identical images
2. **Use templates**: Create prompt templates for repeated use cases
3. **Iterate gradually**: Start simple, refine with multi-turn editing
4. **Batch carefully**: Add delays to respect rate limits
5. **Monitor costs**: 4K images cost 2x more than 2K
6. **Test prompts**: Use low temperature for consistency testing
7. **Learn from examples**: Study `assets/example-prompts.md` for patterns
8. **Reference images**: Use up to 14 for style consistency
9. **Quality modifiers**: Always include "professional", "4K", "sharp" for best results
10. **Verbose mode**: Use `--verbose` flag when debugging
