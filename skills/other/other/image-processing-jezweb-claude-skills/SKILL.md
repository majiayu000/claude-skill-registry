---
name: image-processing
description: "Process images for web development — resize, crop, trim whitespace, convert formats (PNG/WebP/JPG), optimise file size, generate thumbnails, create OG card images. Uses Pillow (Python) — no ImageMagick needed. Trigger with 'resize image', 'convert to webp', 'trim logo', 'optimise images', 'make thumbnail', 'create OG image', 'crop whitespace', 'process image', or 'image too large'."
compatibility: claude-code-only
---

# Image Processing

Process images for web development. Generate a Pillow script adapted to the user's environment and specific needs.

## Prerequisites

Pillow is usually pre-installed. If not:

```bash
pip install Pillow
```

If Pillow is unavailable, use alternatives:

| Alternative | Platform | Install | Best for |
|-------------|----------|---------|----------|
| `sips` | macOS (built-in) | None | Resize, convert (no trim/OG) |
| `sharp` | Node.js | `npm install sharp` | Full feature set, high performance |
| `ffmpeg` | Cross-platform | `brew install ffmpeg` | Resize, convert |

```bash
# macOS sips examples
sips --resampleWidth 1920 input.jpg --out resized.jpg
sips --setProperty format webp input.jpg --out output.webp
```

## Output Format Guide

| Use case | Format | Why |
|----------|--------|-----|
| Photos, hero images | WebP | Best compression, wide browser support |
| Logos, icons (need transparency) | PNG | Lossless, supports alpha |
| Fallback for older browsers | JPG | Universal support |
| Thumbnails | WebP or JPG | Small file size priority |
| OG cards | PNG | Social platforms handle PNG best |

## Core Patterns

### Save with Format-Specific Quality

Different formats need different save parameters. Always handle RGBA-to-JPG compositing — JPG does not support transparency, so composite onto a white background first.

```python
from PIL import Image
import os

def save_image(img, output_path, quality=None):
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    kwargs = {}
    ext = output_path.lower().rsplit(".", 1)[-1]

    if ext == "webp":
        kwargs = {"quality": quality or 85, "method": 6}
    elif ext in ("jpg", "jpeg"):
        kwargs = {"quality": quality or 90, "optimize": True}
        # RGBA → RGB: composite onto white background
        if img.mode == "RGBA":
            bg = Image.new("RGB", img.size, (255, 255, 255))
            bg.paste(img, mask=img.split()[3])
            img = bg
    elif ext == "png":
        kwargs = {"optimize": True}

    img.save(output_path, **kwargs)
```

### Resize with Aspect Ratio

When only width or height is given, calculate the other from aspect ratio. Use `Image.LANCZOS` for high-quality downscaling.

```python
def resize_image(img, width=None, height=None):
    if width and height:
        return img.resize((width, height), Image.LANCZOS)
    elif width:
        ratio = width / img.width
        return img.resize((width, int(img.height * ratio)), Image.LANCZOS)
    elif height:
        ratio = height / img.height
        return img.resize((int(img.width * ratio), height), Image.LANCZOS)
    return img
```

### Trim Whitespace (Auto-Crop)

Remove surrounding whitespace from logos and icons. Convert to RGBA first, then use `getbbox()` to find content bounds.

```python
img = Image.open(input_path)
if img.mode != "RGBA":
    img = img.convert("RGBA")
bbox = img.getbbox()  # Bounding box of non-zero pixels
if bbox:
    img = img.crop(bbox)
```

### Thumbnail

Fit within max dimensions while maintaining aspect ratio:

```python
img.thumbnail((size, size), Image.LANCZOS)
```

### Optimise for Web

Resize + compress in one step. Convert to WebP for best compression. Typical settings: width 1920, quality 85.

### Cross-Platform Font Discovery

System font paths differ by OS. Try multiple paths, fall back to Pillow's default. On Linux, `fc-list` can discover fonts dynamically.

```python
from PIL import ImageFont

def get_font(size):
    font_paths = [
        # macOS
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/SFNSText.ttf",
        # Linux
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        # Windows
        "C:/Windows/Fonts/arial.ttf",
    ]
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()
```

### OG Card Generation (1200x630)

Composite text on a background image or solid colour. Apply semi-transparent overlay for text readability. Centre text horizontally.

```python
from PIL import Image, ImageDraw, ImageFont

width, height = 1200, 630

# Background: image or solid colour
if background_path:
    img = Image.open(background_path).resize((width, height), Image.LANCZOS)
else:
    img = Image.new("RGB", (width, height), bg_color or "#1a1a2e")

# Semi-transparent overlay for text readability
overlay = Image.new("RGBA", (width, height), (0, 0, 0, 128))
img = img.convert("RGBA")
img = Image.alpha_composite(img, overlay)

draw = ImageDraw.Draw(img)
font_title = get_font(48)
font_sub = get_font(24)

# Centre title
if title:
    bbox = draw.textbbox((0, 0), title, font=font_title)
    tw = bbox[2] - bbox[0]
    draw.text(((width - tw) // 2, height // 2 - 60), title, fill="white", font=font_title)

img = img.convert("RGB")
```

## Common Workflows

### Logo Cleanup (client-supplied JPG with white background)

1. Trim whitespace
2. Convert to PNG (for transparency)
3. Create favicon-sized version (thumbnail at 512px)

### Prepare Hero Image for Production

Resize to max width 1920, convert to WebP, compress at quality 85.

### Batch Process

For multiple images, generate a single script that loops over all files rather than processing one at a time.

## Pipeline with Gemini Image Gen

Generate images with the gemini-image-gen skill, then process them:

1. Generate with Gemini (raw PNG output)
2. User picks favourite
3. Optimise: resize to target width, convert to WebP, compress
