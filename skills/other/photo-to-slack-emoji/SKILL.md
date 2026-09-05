---
name: photo-to-slack-emoji
description: "Convert photos into Slack-optimized custom emojis using Nano Banana Pro (Gemini 3 Pro Image) with automatic subject identification, style transformation, and image editing. 64KB/128px compliant. Triggers on: slack emoji, photo to emoji, convert to emoji, edit emoji, emoji maker."
---

# Photo to Slack Emoji Converter & Image Editor

Transform any photo into a classic Slack-optimized emoji using Google's **Nano Banana Pro (Gemini 3 Pro Image)** model with automatic subject identification and style transformation. **NEW:** Edit existing images with natural language prompts!

## When to Use This Skill

Use this skill when:
- Converting photos into Slack custom emojis
- **Editing existing images/emojis** (add hats, change colors, add accessories, etc.)
- Creating icon-style representations of people, pets, objects, or concepts
- Need automatic subject identification and isolation
- Transforming photos to match classic emoji aesthetics (flat, simple, expressive)
- Ensuring Slack's strict 64KB file size and dimension requirements are met

## Overview

This skill combines:
1. **Google Nano Banana Pro (Gemini 3 Pro Image)** - AI-powered subject identification, style transformation, **and image editing** with superior quality
2. **Slack Emoji Validators** - Ensures compliance with Slack's 64KB limit and optimal dimensions
3. **Automatic Optimization** - Color quantization, compression, and size validation

## Two Main Workflows

### 1. Photo-to-Emoji Conversion (Original)
```
Photo Input → Gemini Identifies Subject → Transform to Emoji Style → Optimize for Slack → Validate
```

### 2. Image Editing (NEW!)
```
Existing Image → Natural Language Edit Prompt → Gemini Edits Image → Optimize (optional) → Save
```

## How It Works

```
Photo Input → Gemini Identifies Subject → Transform to Emoji Style → Optimize for Slack → Validate
```

### Workflow Steps:
1. **Upload photo** - Provide path to source image
2. **AI identifies subject** - Gemini's visual reasoning determines the main subject
3. **Style transformation** - Converts to emoji/icon/sticker style with descriptive prompt
4. **Optimization** - Reduces to 128x128, limits colors to 32-48, compresses to <64KB
5. **Validation** - Confirms Slack requirements are met

## Quick Start

### Basic Photo-to-Emoji Usage

```python
from core.photo_to_emoji import convert_photo_to_emoji

# Convert a photo to a Slack emoji
convert_photo_to_emoji(
    input_path="~/Downloads/my_cat.jpg",
    output_path="~/Desktop/cat_emoji.png",
    style="classic_emoji",
    description="happy cat face"  # Optional: helps guide transformation
)
```

### NEW: Image Editing Usage

**IMPORTANT: Never override existing generated images.** Always use a different output filename to preserve the original. Iterative editing works best when you can compare versions.

```bash
# Command line (easiest way)
python edit_image.py input.jpg output.png "add a party hat"
python edit_image.py cat_emoji.png cat_with_sunglasses.png "add cool sunglasses" --optimize

# WRONG: Don't overwrite the original
# python edit_image.py cat_emoji.png cat_emoji.png "edit" ❌

# CORRECT: Use a new filename
# python edit_image.py cat_emoji.png cat_emoji_edited.png "edit" ✅

# Python API
from core.gemini_client import GeminiImageClient

client = GeminiImageClient()

# Edit an existing image
with open("cat_emoji.png", "rb") as f:
    image_data = f.read()

edited_data = client.edit_image(
    image_data=image_data,
    mime_type="image/png",
    edit_prompt="add a party hat to the cat"
)

# Always save to a NEW filename
with open("cat_with_hat.png", "wb") as f:
    f.write(edited_data)
```

### Advanced Usage with Custom Styles

```python
convert_photo_to_emoji(
    input_path="~/Downloads/portrait.jpg",
    output_path="~/Desktop/person_emoji.png",
    style="flat_icon",
    description="friendly person waving",
    custom_prompt="Transform this photo into a simple, flat design icon with bold outlines, minimal details, solid colors, and a white background. Focus on the subject's key features and expression."
)
```

## Available Styles

### 1. **classic_emoji** (Recommended for most use cases)
- Round, expressive, classic emoji aesthetic
- Simplified features with bold outlines
- High contrast, vibrant colors
- Perfect for faces, animals, and expressive subjects

**Example prompt template:**
```
Transform this photo into a classic emoji style: round shape, simplified features,
bold outlines, expressive and friendly, vibrant yellow/warm tones, minimal shading,
white or transparent background. Focus on the subject's main expression.
```

### 2. **flat_icon**
- Minimalist, flat design
- Simple geometric shapes
- Solid colors without gradients
- Best for objects, logos, symbols

**Example prompt template:**
```
Transform this photo into a flat, minimalist icon: simple geometric shapes,
solid colors, no gradients, bold clean outlines, modern flat design aesthetic,
white background. Capture the essence of the subject with minimal detail.
```

### 3. **kawaii_sticker**
- Cute, playful, Japanese kawaii aesthetic
- Rounded features, large eyes
- Pastel or vibrant colors
- Best for animals, characters, food

**Example prompt template:**
```
Transform this photo into a kawaii-style sticker: cute and playful, rounded features,
large expressive eyes, simple cel-shading, vibrant color palette, bold clean outlines,
white background. Make it adorable and friendly.
```

### 4. **pixel_art**
- Retro 8-bit/16-bit pixel art style
- Chunky pixels, limited color palette
- Nostalgic gaming aesthetic
- Best for characters, objects, icons

**Example prompt template:**
```
Transform this photo into pixel art: 16x16 or 32x32 pixel style, retro 8-bit aesthetic,
limited color palette (8-16 colors), chunky pixels, clear subject outline,
simple shading, transparent or solid background.
```

### 5. **custom**
- Provide your own transformation prompt
- Full control over style description
- Use for unique or specific aesthetic needs

## API Configuration

### Setting up Google Gemini API Key

You'll need a Google Gemini API key to use this skill.

1. **Get API Key**: Visit [Google AI Studio](https://aistudio.google.com/apikey)
2. **Set Environment Variable**:
   ```bash
   export GEMINI_API_KEY="your-api-key-here"
   ```
3. **Or provide directly** in code:
   ```python
   convert_photo_to_emoji(
       input_path="photo.jpg",
       output_path="emoji.png",
       api_key="your-api-key-here"
   )
   ```

### API Costs

Google Gemini 2.5 Flash Image pricing:
- **$30 per 1 million output tokens**
- **Each image = 1290 tokens** (flat rate up to 1024x1024px)
- **~$0.039 per image generated**

*Very cost-effective for emoji creation!*

## Slack Requirements

### Emoji Specifications (Strict)
- **Max file size**: 64KB (strict enforcement)
- **Optimal dimensions**: 128x128 pixels
- **Recommended colors**: 32-48 colors maximum
- **Format**: PNG with transparency support

### Validation

The skill automatically validates and optimizes for these requirements:

```python
from core.validators import validate_slack_emoji

# After conversion, validate
is_valid, report = validate_slack_emoji("emoji.png")

if is_valid:
    print("✅ Ready to upload to Slack!")
else:
    print(f"❌ Issues: {report}")
```

## Examples

### Example 1: Pet Photo to Emoji

```python
# Convert a dog photo to a happy emoji
convert_photo_to_emoji(
    input_path="~/Photos/my_dog.jpg",
    output_path="~/Desktop/happy_dog_emoji.png",
    style="classic_emoji",
    description="happy golden retriever smiling"
)
```

**Result**: A round, simplified emoji-style dog face with expressive eyes and a big smile.

### Example 2: Person Portrait to Icon

```python
# Convert a headshot to a professional icon
convert_photo_to_emoji(
    input_path="~/Photos/headshot.jpg",
    output_path="~/Desktop/person_icon.png",
    style="flat_icon",
    description="professional person with glasses"
)
```

**Result**: A minimalist, flat design icon representation of the person.

### Example 3: Food Photo to Kawaii Sticker

```python
# Convert a pizza photo to cute sticker
convert_photo_to_emoji(
    input_path="~/Photos/pizza.jpg",
    output_path="~/Desktop/kawaii_pizza.png",
    style="kawaii_sticker",
    description="cute pizza slice with happy face"
)
```

**Result**: A kawaii-style pizza slice with adorable features.

### Example 4: Batch Conversion

```python
from core.photo_to_emoji import batch_convert

# Convert multiple photos at once
photos = [
    {"input": "cat.jpg", "output": "cat_emoji.png", "description": "happy cat"},
    {"input": "dog.jpg", "output": "dog_emoji.png", "description": "excited dog"},
    {"input": "bird.jpg", "output": "bird_emoji.png", "description": "singing bird"}
]

results = batch_convert(photos, style="classic_emoji")
```

## Advanced Features

### Custom Prompts

For maximum control, provide your own transformation prompt:

```python
convert_photo_to_emoji(
    input_path="photo.jpg",
    output_path="emoji.png",
    style="custom",
    custom_prompt="""
    Transform this photo into a vintage cartoon style from the 1930s:
    thick black outlines, limited color palette (black, white, red, yellow),
    exaggerated features, bouncy and animated appearance, white background.
    """
)
```

### Size Optimization Strategies

If your emoji exceeds 64KB after conversion:

```python
from core.optimizer import aggressive_optimize

# Try aggressive optimization
aggressive_optimize(
    input_path="emoji.png",
    output_path="emoji_optimized.png",
    target_size_kb=60,  # Leave buffer below 64KB
    strategies=["reduce_colors", "reduce_dimensions", "compress_png"]
)
```

### Preview Before Upload

```python
from core.preview import preview_emoji

# Preview how it will look in Slack
preview_emoji("emoji.png", sizes=[16, 32, 64, 128])
```

Shows how the emoji appears at different sizes (Slack displays emojis at various scales).

## Troubleshooting

### Issue: File size exceeds 64KB

**Solutions**:
1. Use fewer colors: `max_colors=32` instead of 48
2. Simplify the style: "flat_icon" compresses better than "kawaii_sticker"
3. Reduce detail in description: Less detail = simpler image = smaller file
4. Use aggressive optimization (see Advanced Features)

### Issue: Subject not identified correctly

**Solutions**:
1. Provide more specific `description` parameter
2. Crop photo to focus on main subject before conversion
3. Use better-lit, clearer source photo
4. Try a custom prompt with explicit subject description

### Issue: Style doesn't match expectation

**Solutions**:
1. Try different style presets (flat_icon vs classic_emoji)
2. Use `custom_prompt` for precise control
3. Add more descriptive terms to `description` parameter
4. Review style examples in `/templates/style_examples.md`

### Issue: API authentication fails

**Solutions**:
1. Verify `GEMINI_API_KEY` environment variable is set
2. Check API key is valid at [Google AI Studio](https://aistudio.google.com/apikey)
3. Ensure no extra spaces or quotes in API key
4. Try providing `api_key` parameter directly

## File Structure

```
~/.claude/skills/photo-to-slack-emoji/
├── skill.md                    # This file
├── core/
│   ├── photo_to_emoji.py      # Main conversion logic
│   ├── gemini_client.py       # Gemini API wrapper
│   ├── optimizer.py           # Image optimization utilities
│   ├── validators.py          # Slack requirement validators
│   └── preview.py             # Preview utilities
├── templates/
│   ├── style_prompts.json     # Pre-defined style templates
│   └── style_examples.md      # Visual style guide
└── references/
    ├── gemini-api-docs.md     # Gemini API documentation
    └── slack-emoji-specs.md   # Slack emoji specifications
```

## Dependencies

```bash
# Required packages
pip install pillow google-genai requests

# Optional for advanced features
pip install imageio numpy
```

## Best Practices

1. **Start with high-quality photos** - Better input = better output
2. **Use descriptive filenames** - Helps with organization in Slack
3. **NEVER override existing generated images** - Always save edits to new filenames to preserve originals
4. **Test at multiple sizes** - Preview before uploading to ensure clarity
5. **Keep it simple** - Simpler styles compress better and meet size limits
6. **Provide context** - Use the `description` parameter to guide transformation
7. **Batch process** - Convert multiple photos at once for efficiency
8. **Iterative editing** - Make small edits and save each version with descriptive names (e.g., `cat_v1.png`, `cat_v2_hat.png`, `cat_v3_final.png`)

## Limitations

- **API rate limits** - Google Gemini has rate limits (check your quota)
- **Subject complexity** - Very complex subjects may not simplify well
- **Background removal** - Gemini does its best, but manual editing may improve results
- **Transparent backgrounds** - Not always perfect; may need manual cleanup
- **Text in photos** - May not preserve text accurately in emoji transformation

## Related Skills

- **slack-gif-creator** - Create animated GIFs for Slack
- **canvas-design** - Design custom graphics from scratch
- **firecrawl-mcp** - Scrape emoji images from web for reference

## What's Next

After creating your emoji:

1. **Upload to Slack**:
   - Go to Slack workspace settings
   - Click "Customize" → "Emoji"
   - Upload your PNG file
   - Give it a memorable name like `:my_cat:` or `:happy_dog:`

2. **Share with team**:
   - Emojis are available to entire workspace
   - Use in messages, reactions, and status updates

3. **Create variations**:
   - Try different styles for the same photo
   - Experiment with descriptions for different expressions
   - Build an emoji library for your team

## Feedback & Support

This skill uses:
- **Google Gemini 2.5 Flash Image** (aka Nano Banana) - [Documentation](https://ai.google.dev/gemini-api/docs/image-generation)
- **Slack Emoji Guidelines** - [Slack Help Center](https://slack.com/help/articles/206870177-Add-custom-emoji)

For issues or suggestions, check the skill's GitHub repository or the Claude Code skills directory.
