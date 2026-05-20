---
name: image-generation
description: "AI-powered image generation and editing using Gemini. Use when Claude needs to: (1) Generate images from text descriptions, (2) Edit existing images with instructions, (3) Create infographics or charts, (4) Generate visual assets for reports/presentations, (5) Work with .png, .jpg, .jpeg, .webp files for editing."
---

# Image Generation & Editing

## Overview
Generate and edit images using Gemini 2.5 Flash Image model via MCP tools.

## Quick Start

### Text-to-Image Generation
```python
result = generate_image(
    prompt="A modern infographic showing renewable energy statistics",
    output_dir="/path/to/work_products/media"
)
```

### Image Editing
```python
result = generate_image(
    prompt="Change the background to a sunset over mountains",
    input_image_path="/path/to/original.png",
    output_dir="/path/to/work_products/media"
)
```

### Preview Generated Image
```python
# Auto-launch viewer after generation
result = generate_image(
    prompt="Blue square with rounded corners",
    preview=True  # Opens Gradio viewer
)

# Or preview any existing image
preview_image("/path/to/image.png")
```

## Available Tools

### `generate_image`
Primary tool for image generation and editing.

**Parameters**:
- `prompt` (required): Text description or edit instruction
- `input_image_path` (optional): Path to source image for editing
- `output_dir` (optional): Output directory (defaults to `work_products/media/`)
- `output_filename` (optional): Custom filename (auto-generated if not provided)
- `preview` (optional): Launch Gradio viewer after generation
- `model_name` (optional): Gemini model to use. Defaults to `gemini-3-pro-image-preview`.
  - Options: `gemini-3-pro-image-preview`, `gemini-2.5-flash-image`.

**Returns**: JSON with `output_path`, `description`, `size_bytes`, and optionally `viewer_url`

### `describe_image`
Get a short description of an image for generating meaningful filenames.

**Parameters**:
- `image_path` (required): Path to image file
- `max_words` (optional): Maximum words in description (default 10)

### `preview_image`
Launch Gradio viewer to display an image.

**Parameters**:
- `image_path` (required): Path to image file
- `port` (optional): Port for Gradio server (default 7860)

## Best Practices

### Prompt Crafting
- **Be specific**: "modern, minimalist infographic with blue gradient"
- **Include style**: "photorealistic", "illustration", "line art", "cartoon"
- **For charts/infographics**: Include data points in the prompt
- **For editing**: Describe what to change AND what to preserve

### Examples

**Infographic**:
```python
generate_image(
    prompt="Infographic showing 3 key statistics: 45% growth, $2.3B market, 120 companies. Modern flat design with blue and green color scheme."
)
```

**Chart**:
```python
generate_image(
    prompt="Clean bar chart comparing renewable energy adoption: Solar 35%, Wind 28%, Hydro 22%. Use professional colors, include labels."
)
```

**Editing**:
```python
generate_image(
    prompt="Add snow to the mountain peaks, keep the sunset colors",
    input_image_path="work_products/media/sunset_mountains.png"
)
```

## Integration with Other Skills

### Reports (`report-creation-expert`)
Generate custom graphics for HTML reports:
```python
# Generate infographic
img_result = generate_image(
    prompt="Infographic about AI market trends",
    output_dir="work_products/media"
)

# Embed in HTML report
html_content = f'''
<img src="file:///{img_result['output_path']}" alt="AI Trends" style="max-width: 100%;">
'''
```

### PowerPoint (`pptx` skill)
Create custom slide backgrounds and visual elements:
- Generate images first, then reference paths in PptxGenJS
- Use `addImage()` to embed generated graphics
- Create infographics for data-heavy slides

### Documents (`docx` skill)
Generate embedded figures and diagrams for Word documents.

## Troubleshooting

### Error: "GEMINI_API_KEY not set"
Ensure `GEMINI_API_KEY` is set in `.env` file.

### Error: "No image data in response"
- Check your prompt is clear and specific
- Ensure Gemini 2.0 Flash model supports the request
- Try simplifying the prompt

### Preview not working
- Gradio viewer script must exist at `.claude/skills/image-generation/scripts/gradio_viewer.py`
- Port 7860 must be available
- Run manually: `python scripts/gradio_viewer.py /path/to/image.png`

## Output Conventions

- **Directory**: `{workspace}/work_products/media/`
- **Filename pattern**: `{description}_{timestamp}.png`
- **Format**: PNG (lossless)
- **Description**: Auto-generated from image analysis

## Dependencies

- `google-genai>=1.56.0` - Gemini API client
- `gradio>=6.2.0` - Optional viewer UI
- `pillow` - Image processing
