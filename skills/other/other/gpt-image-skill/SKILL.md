---
name: gpt-image-skill
description: 'Generate or edit images using OpenAI GPT Image API (gpt-image-2, gpt-image-1, etc). Triggers: "gpt image", "openai image", "generate image with openai", "draw image", "create image", "image generation", "AI drawing", "图片生成", "AI绘图", "生成图片", "画图". Use this skill whenever the user wants to generate or edit images and mentions OpenAI, GPT, or when OPENAI_API_KEY is available.'
allowed-tools: Read, Write, Glob, Grep, Task, Bash(cat:*), Bash(ls:*), Bash(tree:*), Bash(python3:*)
---

# GPT Image Skill

Generate or edit images using OpenAI's GPT Image models through a bundled Python script.

## Requirements

1. **OPENAI_API_KEY**: Must be configured in `~/.gpt-image.env` or `export OPENAI_API_KEY=<your-key>`
2. **OPENAI_API_BASE** (optional): Custom API base URL for compatible endpoints (e.g. Azure OpenAI, proxies). Set in `~/.gpt-image.env` or export it.
3. **Python3 with dependencies**: openai, Pillow. Install via `python3 -m pip install -r ./requirements.txt` if not installed yet.
4. **Executable**: `./gpt_image.py`

## Instructions

### For image generation

1. Ask the user for:
   - What they want to create (the prompt)
   - Desired size (optional, defaults to 1024x1024)
   - Output filename (optional, auto-generates UUID-based name if not specified)
   - Model preference (optional, defaults to gpt-image-2)
   - Quality (optional, defaults to auto)
   - Number of images (optional, defaults to 1)

2. Run the script:

   ```bash
   python3 ./gpt_image.py --prompt "description of image" --output "filename.png"
   ```

3. Show the user the saved image path when complete.

### For image editing

1. Ask the user for:
   - Input image file(s) to edit (up to 3)
   - What changes they want (the prompt)
   - Output filename (optional)

2. Run with input images:

   ```bash
   python3 ./gpt_image.py edit --prompt "editing instructions" --input image1.png image2.png --output "edited.png"
   ```

## Available Options

### Models (--model)

- `gpt-image-2` (default) — Latest model with strong instruction following, text rendering, and broad world knowledge
- `gpt-image-1.5` — Mid-tier model
- `gpt-image-1` — First-generation GPT image model
- `gpt-image-1-mini` — Lightweight, faster generation

### Sizes (--size)

- `1024x1024` (default) — Square
- `1024x1536` — Portrait (2:3)
- `1536x1024` — Landscape (3:2)
- `auto` — Let the model decide

### Quality (--quality)

- `auto` (default) — Model decides optimal quality
- `high` — Higher detail, slower
- `medium` — Balanced
- `low` — Fastest

### Output Format (--format)

- `png` (default) — Lossless
- `jpeg` — Smaller file size
- `webp` — Modern format, good compression

### Background (--background)

- `auto` (default) — Model decides
- `transparent` — Transparent background (png/webp only)
- `opaque` — Solid background

### Other Options

- `--n <count>` — Number of images to generate (default: 1)
- `--output <filename>` — Output filename (default: auto-generated)

## Examples

### Generate a simple image

```bash
python3 ./gpt_image.py --prompt "A serene mountain landscape at sunset with a lake"
```

### Generate with specific size and output

```bash
python3 ./gpt_image.py \
  --prompt "Modern minimalist logo for a tech startup" \
  --size 1024x1024 \
  --quality high \
  --output "logo.png"
```

### Generate landscape image

```bash
python3 ./gpt_image.py \
  --prompt "Futuristic cityscape with flying cars" \
  --size 1536x1024 \
  --output "cityscape.png"
```

### Generate with transparent background

```bash
python3 ./gpt_image.py \
  --prompt "A cute cartoon cat mascot" \
  --background transparent \
  --format png \
  --output "mascot.png"
```

### Generate multiple images

```bash
python3 ./gpt_image.py \
  --prompt "Abstract art in the style of Kandinsky" \
  --n 3 \
  --output "art.png"
```

### Edit existing images

```bash
python3 ./gpt_image.py edit \
  --prompt "Add a rainbow in the sky" \
  --input photo.png \
  --output "photo-with-rainbow.png"
```

### Combine multiple reference images

```bash
python3 ./gpt_image.py edit \
  --prompt "Create a gift basket containing all items shown" \
  --input item1.png item2.png item3.png \
  --output "gift-basket.png"
```

### Use a different model

```bash
python3 ./gpt_image.py \
  --prompt "Detailed portrait of a cat in watercolor style" \
  --model gpt-image-1 \
  --output "cat-portrait.png"
```

## Error Handling

If the script fails:

- Check that `OPENAI_API_KEY` is exported
- If using a custom endpoint, verify `OPENAI_API_BASE` is correct
- Verify input image files exist and are readable (for editing)
- Ensure the output directory is writable
- Check that the model name is valid

## Best Practices

1. Be descriptive in prompts — include style, mood, colors, composition details
2. For logos/icons, use square size (1024x1024) with transparent background
3. For social media, use portrait (1024x1536) for stories or square for posts
4. For wallpapers/headers, use landscape (1536x1024)
5. Use `high` quality for final output, `auto` for quick iterations
6. GPT Image models excel at text rendering — include text in prompts when needed
7. For editing, provide clear instructions about what to change and what to keep
