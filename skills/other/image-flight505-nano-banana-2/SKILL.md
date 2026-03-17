---
name: image
description: "Generate and edit images using AI models via OpenRouter. Supports Nano Banana Pro (Gemini 3 Pro Image), FLUX, and other image generation models."
allowed-tools: [Read, Write, Edit, Bash]
---

# Nano Banana - Image Generation

## Overview

Generate and edit images using state-of-the-art AI models. Perfect for creating visual assets, concept art, illustrations, and editing existing images.

**Key Features:**
- 🎨 **Multiple Models**: Gemini 3 Pro Image, FLUX Pro, and more
- ✏️ **Image Editing**: Modify existing images with natural language
- 🚀 **Simple API**: One command to generate or edit
- 💾 **Automatic Saving**: Handles file formats automatically

## When to Use This Skill

Use this skill when you need:

- **Visual Assets**: Icons, illustrations, backgrounds
- **Concept Art**: Ideas and visual explorations
- **Marketing Materials**: Product mockups, social media images
- **Photo Editing**: Modify existing images with AI
- **Creative Content**: Artistic images, abstract visuals
- **Presentation Graphics**: Visuals for slides and documents

**Note**: For technical diagrams (architecture, flowcharts, ERD), use the **diagram** skill instead—it includes quality review and iteration.

## Quick Start

```bash
# Generate a new image
python skills/image/scripts/generate_image.py "A beautiful sunset over mountains with orange and purple sky" -o sunset.png

# Edit an existing image
python skills/image/scripts/generate_image.py "Make the sky more dramatic with storm clouds" --input sunset.png -o dramatic_sunset.png

# Use a specific model
python skills/image/scripts/generate_image.py "Abstract geometric art in blue and gold" -m "black-forest-labs/flux.2-pro" -o abstract.png
```

## Available Models

| Model | ID | Capabilities | Best For |
|-------|-----|-------------|----------|
| **Gemini 3 Pro Image** | `google/gemini-3-pro-image-preview` | Generation + Editing | High quality, versatile |
| **FLUX Pro** | `black-forest-labs/flux.2-pro` | Generation + Editing | Fast, artistic |
| **FLUX Flex** | `black-forest-labs/flux.2-flex` | Generation only | Development/testing |

## Usage Examples

### Generate New Images

```bash
# Photorealistic
python generate_image.py "Professional headshot of a business executive in modern office setting" -o headshot.png

# Artistic
python generate_image.py "Watercolor painting of a cozy coffee shop on a rainy day" -o coffee_shop.png

# Abstract
python generate_image.py "Abstract visualization of data flowing through neural networks, blue and cyan colors" -o neural_flow.png

# Product
python generate_image.py "Modern minimalist logo for a tech startup called 'Nexus', clean geometric design" -o logo.png
```

### Edit Existing Images

```bash
# Change colors
python generate_image.py "Change the car color to red" --input car.jpg -o red_car.png

# Add elements
python generate_image.py "Add a rainbow in the sky" --input landscape.jpg -o rainbow_landscape.png

# Remove elements
python generate_image.py "Remove the person from the background" --input photo.jpg -o clean_photo.png

# Style transfer
python generate_image.py "Make this look like a watercolor painting" --input photo.jpg -o watercolor.png
```

### Specify Output Format

```bash
# PNG (default, best for graphics with transparency)
python generate_image.py "Icon of a rocket ship" -o rocket.png

# Output to specific directory
python generate_image.py "Banner image" -o assets/images/banner.png
```

## Configuration

### Environment Variable (Recommended)
```bash
export OPENROUTER_API_KEY='your_api_key_here'
```

### .env File
Create a `.env` file in your project:
```
OPENROUTER_API_KEY=your_api_key_here
```

### Get Your API Key
1. Go to https://openrouter.ai/keys
2. Create a new API key
3. Add credits to your account

## Python API

```python
from skills.image.scripts.generate_image import generate_image

# Generate new image
result = generate_image(
    prompt="A futuristic city at night with neon lights",
    output_path="city.png",
    model="google/gemini-3-pro-image-preview"
)

# Edit existing image
result = generate_image(
    prompt="Add flying cars to the scene",
    output_path="city_with_cars.png",
    input_image="city.png"
)
```

## Tips for Better Images

### Be Descriptive
```bash
# ❌ Too vague
"A dog"

# ✅ Detailed
"A golden retriever puppy playing in autumn leaves, warm afternoon sunlight, shallow depth of field, professional pet photography"
```

### Include Style
```bash
# ✅ Specify artistic style
"A mountain landscape in the style of traditional Japanese ink painting, minimalist, black and white with subtle gray tones"
```

### Specify Composition
```bash
# ✅ Include framing
"Close-up portrait of an owl, centered composition, soft studio lighting, dark background, sharp focus on the eyes"
```

### For Editing, Be Specific
```bash
# ❌ Vague edit
"Make it better"

# ✅ Specific edit
"Increase the contrast, make the colors more vibrant, and add a subtle vignette effect"
```

## Comparison: image vs diagram Skills

| Aspect | `image` Skill | `diagram` Skill |
|--------|--------------|-----------------|
| **Use Case** | Photos, art, illustrations | Technical diagrams |
| **Quality Review** | No | Yes (Gemini 3 Pro) |
| **Iteration** | Single pass | Smart iteration (1-2 passes) |
| **Doc Types** | N/A | 13 document types with thresholds |
| **Image Editing** | Yes | No |
| **Best For** | Creative visuals | Architecture, flowcharts, ERD |

**Rule of thumb**: If it's a technical diagram with boxes, arrows, and labels → use `diagram`. If it's a photo, illustration, or artistic image → use `image`.

## Troubleshooting

### "OPENROUTER_API_KEY not found"
Set the environment variable or create a `.env` file. See Configuration section.

### "Image file not found" (for editing)
Make sure the input image path is correct and the file exists.

### Unexpected Output
- Try a different model
- Add more detail to your prompt
- Be more specific about style, composition, and colors

### Generation Timeout
Large or complex images may take up to 2 minutes. Timeout is set to 120 seconds.

## Cost Considerations

- Gemini 3 Pro Image: ~$2/M input, ~$12/M output tokens
- FLUX Pro: Check OpenRouter for current pricing
- Typical image generation: $0.02-0.10 per image
- Image editing: Similar to generation costs
