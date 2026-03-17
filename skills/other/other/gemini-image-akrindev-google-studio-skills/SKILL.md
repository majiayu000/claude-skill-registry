---
name: gemini-image
description: Generate images using Google Gemini and Imagen models via scripts/. Use for AI image generation, text-to-image, creating visuals from prompts, generating multiple images, custom aspect ratios, and high-resolution output up to 4K. Triggers on "generate image", "create image", "imagen", "text to image", "AI art", "nano banana".
license: MIT
version: 1.0.0
keywords: image generation, imagen, gemini-3-pro, gemini-2.5, text-to-image, AI art, nano banana, 4K resolution, aspect ratio
---

# Gemini Image Generation

Generate high-quality images from text prompts using Google's Gemini and Imagen models through executable scripts.

## When to Use This Skill

Use this skill when you need to:
- Create visual content from text descriptions
- Generate multiple image variations
- Create images at specific resolutions (1K, 2K, 4K)
- Produce images for different aspect ratios (social media, banners, etc.)
- Generate photorealistic images or artistic visuals
- Create images with person generation controls
- Batch generate multiple images at once
- Combine with text generation for complete content creation

## Available Scripts

### scripts/generate_image.py
**Purpose**: Generate images using Gemini 3 Pro Image or Imagen 4 models

**When to use**:
- Any image generation task
- Multiple image generation (1-4 per request)
- Custom resolution and aspect ratio needs
- Professional asset creation
- Photorealistic or artistic image generation

**Key parameters**:
| Parameter | Description | Example |
|-----------|-------------|---------|
| `prompt` | Text description (required) | `"A futuristic city at sunset"` |
| `--model`, `-m` | Model to use | `gemini-3-pro-image-preview` |
| `--output-dir`, `-o` | Output directory for images | `images/` |
| `--name`, `-n` | Base name for output files | `artwork` |
| `--no-timestamp` | Disable auto timestamp | Flag |
| `--aspect`, `-a` | Aspect ratio | `16:9` |
| `--size`, `-s` | Resolution | `2K` or `4K` |
| `--num` | Number of images (1-4) | `4` |
| `--person` | Person generation policy | `allow_adult` |

**Output**: List of saved PNG file paths

## Workflows

### Workflow 1: Basic Image Generation
```bash
python scripts/generate_image.py "A futuristic city at sunset with flying cars"
```
- Best for: Quick image generation, prototypes
- Model: `gemini-3-pro-image-preview` (default, highest quality)
- Output: `images/generated_image_YYYYMMDD_HHMMSS.png`

### Workflow 2: Social Media (Instagram, Facebook)
```bash
python scripts/generate_image.py "Minimalist coffee shop interior" --aspect 1:1 --size 2K --name coffee-shop
```
- Best for: Instagram posts, profile pictures
- Aspect: 1:1 (square format)
- Resolution: 2K (2048x2048)
- Output: `images/coffee-shop_YYYYMMDD_HHMMSS.png`

### Workflow 3: YouTube Thumbnails (16:9)
```bash
python scripts/generate_image.py "Tech gadget review thumbnail with vibrant colors" --aspect 16:9 --size 2K --name thumbnail
```
- Best for: YouTube, video thumbnails
- Aspect: 16:9 (widescreen)
- Resolution: 2K (2752x1536)
- Output: `images/thumbnail_YYYYMMDD_HHMMSS.png`

### Workflow 4: Multiple Variations
```bash
python scripts/generate_image.py "Abstract geometric patterns in blue and gold" --num 4 --name abstract
```
- Best for: A/B testing, design options
- Generates: 4 distinct variations
- Output: `images/abstract_YYYYMMDD_HHMMSS_0.png`, `images/abstract_YYYYMMDD_HHMMSS_1.png`, etc.

### Workflow 5: Custom Output Directory
```bash
python scripts/generate_image.py "Detailed architectural rendering of modern museum" --aspect 16:9 --size 4K --output-dir ./professional/ --name museum
```
- Best for: Print materials, high-end assets, organized projects
- Model: `gemini-3-pro-image-preview` only (for 4K)
- Resolution: 4K (5504x3072 for 16:9)
- Directory created automatically if it doesn't exist

### Workflow 6: Photorealistic Images (Imagen 4)
```bash
python scripts/generate_image.py "Robot holding a red skateboard in urban setting" --model imagen-4.0-generate-001 --aspect 16:9 --size 2K --num 2 --name robot-skate
```
- Best for: Realistic photos, product shots
- Model: `imagen-4.0-generate-001` (photorealistic)
- Notes: English prompts only
- Max 4 images per request

### Workflow 7: Blog Post Featured Image
```bash
python scripts/generate_image.py "Serene mountain lake at sunrise with reflections" --aspect 16:9 --size 2K --output-dir ./blog-images/ --name featured-image
```
- Best for: Blog headers, article images
- Combines well with: gemini-text for blog content generation

### Workflow 8: Content Creation Pipeline (Text + Image)
```bash
# 1. Generate content (gemini-text skill)
python skills/gemini-text/scripts/generate.py "Write a product description for smart home device"

# 2. Generate product image (this skill)
python scripts/generate_image.py "Sleek modern smart home device on white background" --aspect 4:3 --size 2K --name product

# 3. Create social media post
```
- Best for: E-commerce, marketing campaigns
- Combines with: gemini-text, gemini-batch for batch production

### Workflow 9: Disable Timestamp
```bash
python scripts/generate_image.py "Fixed filename image" --name my-image --no-timestamp
```
- Best for: When you want complete control over filename
- Output: `images/my-image.png` (no timestamp)
- Use when: Generating files for specific naming schemes or automated pipelines

## Parameters Reference

### Model Selection

| Model | Nickname | Quality | Max Size | Best For |
|-------|----------|---------|----------|----------|
| `gemini-3-pro-image-preview` | Nano Banana Pro | Highest | 4K | Professional assets, advanced text rendering |
| `gemini-2.5-flash-image` | Nano Banana | Good | 2K | High-volume, low-latency |
| `imagen-4.0-generate-001` | Imagen 4 | Photorealistic | 2K | Realistic photos, product shots |

### Aspect Ratios

| Ratio | Use Case | 1K Size | 2K Size |
|-------|----------|----------|----------|
| 1:1 | Instagram, avatars | 1024x1024 | 2048x2048 |
| 16:9 | YouTube, presentations | 1376x768 | 2752x1536 |
| 9:16 | Instagram Stories, TikTok | 768x1376 | 1536x2752 |
| 4:3 | Traditional displays | 1024x768 | 2048x1536 |
| 3:4 | Portrait orientation | 768x1024 | 1536x2048 |
| 21:9 | Ultrawide | - | 5504x2400 |

Note: 4K resolution only available with `gemini-3-pro-image-preview`

### Resolution Guide

| Size | Use Case | Best Model |
|------|----------|-------------|
| 1K (1024px) | Web thumbnails, previews | Any model |
| 2K (2048px) | Standard web, social media | Any model |
| 4K (4096px) | Print, high-end assets | gemini-3-pro only |

### Person Generation Policy

| Policy | Description | Restrictions |
|---------|-------------|----------------|
| `dont_allow` | No people in images | None |
| `allow_adult` | Adults only | Recommended default |
| `allow_all` | All ages | Restricted in EU, UK, CH, MENA |

## Output Interpretation

### File Naming
- Default format: `{name}_YYYYMMDD_HHMMSS.png` (auto timestamp)
- Single image example: `artwork_20260130_031643.png`
- Multiple images: `{name}_YYYYMMDD_HHMMSS_0.png`, `{name}_YYYYMMDD_HHMMSS_1.png`, etc.
- Without timestamp (`--no-timestamp`): `{name}.png`
- Script prints: "Saved: /path/to/file.png"

### Image Quality
- All images include SynthID watermark for authenticity
- PNG format for lossless quality
- Can be converted to JPEG/WEBP if needed
- 4K images are significantly larger file sizes

### Error Messages
- "Model not available": Check model name spelling
- "Unsupported size": Verify size/model combination
- "Aspect ratio error": Use supported ratios for selected model

## Common Issues

### "google-genai or pillow not installed"
```bash
pip install google-genai pillow
```

### "Image generation failed"
- Check prompt length (too verbose can fail)
- Try simpler, more focused prompts
- Verify model availability in your region
- Check API quota limits

### "Unsupported aspect ratio"
- Check if ratio is supported by selected model
- Imagen 4 has fewer ratio options than Gemini
- Use 16:9 or 1:1 for best compatibility

### "4K not supported"
- 4K only works with `gemini-3-pro-image-preview`
- Use `--size 2K` for other models
- Try `--model gemini-3-pro-image-preview --size 4K`

### "Imagen prompt language error"
- Imagen models support English prompts only
- Use `gemini-3-pro-image-preview` for other languages
- Translate prompt to English for Imagen

### File too large for storage
- Use `--size 1K` for smaller files
- Compress images after generation
- Convert PNG to JPEG for web use

## Best Practices

### Prompt Engineering
- Be specific and descriptive
- Include style descriptors (e.g., "photorealistic", "digital art")
- Mention lighting, mood, and composition
- Use analogies for complex concepts
- Avoid negative prompts (describe what you want, not what to avoid)

### Model Selection
- Use `gemini-3-pro-image-preview` for: High quality, text rendering, 4K
- Use `gemini-2.5-flash-image` for: Speed, high volume
- Use `imagen-4.0-generate-001` for: Photorealism, product shots

### Performance Optimization
- Generate multiple images at once with `--num`
- Use lower resolution for previews
- Batch requests for high-volume needs (gemini-batch skill)
- Cache results for repeated requests

### Quality Tips
- Use 2K resolution for most web uses
- 4K only when maximum detail is needed
- Combine specific prompts with style guidance
- Test prompts with `--num 1` before generating batches

### Cost Management
- Use flash models for cost efficiency
- 4K generation costs significantly more
- Batch multiple requests when possible
- Generate at 1K for testing, 2K/4K for final

## Related Skills

- **gemini-text**: Generate text content alongside images
- **gemini-tts**: Create audio for image-based content
- **gemini-batch**: Process multiple image requests efficiently
- **gemini-embeddings**: Generate image embeddings for similarity search

## Quick Reference

```bash
# Basic
python scripts/generate_image.py "Your prompt"

# Social media (1:1)
python scripts/generate_image.py "Prompt" --aspect 1:1 --size 2K --name social-post

# YouTube thumbnail (16:9)
python scripts/generate_image.py "Prompt" --aspect 16:9 --size 2K --name thumbnail

# 4K high quality
python scripts/generate_image.py "Prompt" --aspect 16:9 --size 4K --name high-res

# Multiple variations
python scripts/generate_image.py "Prompt" --num 4 --name variations

# Custom directory
python scripts/generate_image.py "Prompt" --output-dir ./my-images/ --name custom

# Photorealistic
python scripts/generate_image.py "Prompt" --model imagen-4.0-generate-001 --aspect 16:9 --size 2K --name photo

# No timestamp
python scripts/generate_image.py "Prompt" --name fixed-name --no-timestamp
```

## Reference

- See `references/` for model documentation (if available)
- Get API key: https://aistudio.google.com/apikey
- Documentation: https://ai.google.dev/gemini-api/docs/image-generation
- SynthID: https://deepmind.google/technologies/synthid/
