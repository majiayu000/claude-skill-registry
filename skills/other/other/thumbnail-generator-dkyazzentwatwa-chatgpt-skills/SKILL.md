---
name: thumbnail-generator
description: Generate thumbnails from images with smart cropping, multiple sizes, and batch processing. Ideal for web galleries, social media, and app icons.
---

# Thumbnail Generator

Create optimized thumbnails with smart cropping, multiple output sizes, and batch processing.

## Features

- **Smart Cropping**: Center, face-aware, or edge-detection based
- **Multiple Sizes**: Generate multiple thumbnail sizes at once
- **Presets**: Web, social media, app icon presets
- **Batch Processing**: Process entire folders
- **Quality Control**: Optimize file size vs quality
- **Formats**: JPEG, PNG, WebP output

## Quick Start

```python
from thumbnail_gen import ThumbnailGenerator

gen = ThumbnailGenerator()
gen.load("photo.jpg")

# Create single thumbnail
gen.resize(200, 200).save("thumb.jpg")

# Create multiple sizes
gen.generate_sizes([
    (100, 100),
    (200, 200),
    (400, 400)
], output_dir="./thumbs/")
```

## CLI Usage

```bash
# Single thumbnail
python thumbnail_gen.py --input photo.jpg --size 200x200 --output thumb.jpg

# Multiple sizes
python thumbnail_gen.py --input photo.jpg --sizes 100x100,200x200,400x400 --output ./thumbs/

# Batch process folder
python thumbnail_gen.py --input ./photos/ --size 200x200 --output ./thumbs/

# Use preset
python thumbnail_gen.py --input photo.jpg --preset social --output ./thumbs/

# Smart crop
python thumbnail_gen.py --input photo.jpg --size 200x200 --crop smart --output thumb.jpg

# WebP output
python thumbnail_gen.py --input photo.jpg --size 200x200 --format webp --output thumb.webp
```

## API Reference

### ThumbnailGenerator Class

```python
class ThumbnailGenerator:
    def __init__(self)

    # Loading
    def load(self, filepath: str) -> 'ThumbnailGenerator'

    # Resizing
    def resize(self, width: int, height: int,
              crop: str = "fit") -> 'ThumbnailGenerator'
    def resize_width(self, width: int) -> 'ThumbnailGenerator'
    def resize_height(self, height: int) -> 'ThumbnailGenerator'

    # Cropping
    def crop_center(self, width: int, height: int) -> 'ThumbnailGenerator'
    def crop_smart(self, width: int, height: int) -> 'ThumbnailGenerator'
    def crop_position(self, width: int, height: int,
                     position: str = "center") -> 'ThumbnailGenerator'

    # Output
    def save(self, output: str, quality: int = 85,
            format: str = None) -> str
    def to_bytes(self, format: str = "JPEG", quality: int = 85) -> bytes

    # Batch operations
    def generate_sizes(self, sizes: list, output_dir: str,
                      prefix: str = None) -> list
    def process_folder(self, input_dir: str, output_dir: str,
                      width: int, height: int, recursive: bool = False) -> list

    # Presets
    def apply_preset(self, preset: str, output_dir: str) -> list
```

## Resize Modes

### Fit (Default)
Resize to fit within bounds, maintaining aspect ratio:

```python
gen.resize(200, 200, crop="fit")
# Result: Image fits within 200x200, may have letterboxing
```

### Fill
Resize to fill bounds, cropping excess:

```python
gen.resize(200, 200, crop="fill")
# Result: Exactly 200x200, some content may be cropped
```

### Stretch
Resize to exact dimensions (distorts aspect ratio):

```python
gen.resize(200, 200, crop="stretch")
# Result: Exactly 200x200, may be distorted
```

## Smart Cropping

Automatically detect the most interesting part of the image:

```python
gen.load("photo.jpg")
gen.crop_smart(200, 200)
gen.save("thumb.jpg")
```

Uses edge detection to find areas of interest.

### Crop Positions

```python
# Predefined positions
gen.crop_position(200, 200, position="center")
gen.crop_position(200, 200, position="top")
gen.crop_position(200, 200, position="bottom")
gen.crop_position(200, 200, position="left")
gen.crop_position(200, 200, position="right")
gen.crop_position(200, 200, position="top-left")
gen.crop_position(200, 200, position="top-right")
gen.crop_position(200, 200, position="bottom-left")
gen.crop_position(200, 200, position="bottom-right")
```

## Presets

### Web Preset

```python
gen.apply_preset("web", "./output/")

# Generates:
# - thumb_small.jpg (150x150)
# - thumb_medium.jpg (300x300)
# - thumb_large.jpg (600x600)
```

### Social Media Preset

```python
gen.apply_preset("social", "./output/")

# Generates:
# - instagram_square.jpg (1080x1080)
# - instagram_portrait.jpg (1080x1350)
# - instagram_landscape.jpg (1080x566)
# - twitter.jpg (1200x675)
# - facebook.jpg (1200x630)
# - linkedin.jpg (1200x627)
```

### App Icons Preset

```python
gen.apply_preset("icons", "./output/")

# Generates:
# - icon_16.png (16x16)
# - icon_32.png (32x32)
# - icon_48.png (48x48)
# - icon_64.png (64x64)
# - icon_128.png (128x128)
# - icon_256.png (256x256)
# - icon_512.png (512x512)
```

### Favicon Preset

```python
gen.apply_preset("favicon", "./output/")

# Generates:
# - favicon_16.png (16x16)
# - favicon_32.png (32x32)
# - apple_touch.png (180x180)
# - android_192.png (192x192)
# - android_512.png (512x512)
```

## Multiple Sizes

Generate multiple thumbnail sizes at once:

```python
gen.load("photo.jpg")
files = gen.generate_sizes(
    sizes=[(100, 100), (200, 200), (400, 400), (800, 800)],
    output_dir="./thumbs/",
    prefix="product"
)

# Creates:
# - product_100x100.jpg
# - product_200x200.jpg
# - product_400x400.jpg
# - product_800x800.jpg
```

## Batch Processing

Process entire folders:

```python
gen = ThumbnailGenerator()
results = gen.process_folder(
    input_dir="./photos/",
    output_dir="./thumbnails/",
    width=200,
    height=200,
    recursive=True
)

print(f"Processed {len(results)} images")
```

## Quality and Format

### Quality Settings

```python
# High quality (larger file)
gen.save("thumb.jpg", quality=95)

# Balanced (default)
gen.save("thumb.jpg", quality=85)

# Web optimized (smaller file)
gen.save("thumb.jpg", quality=70)
```

### Output Formats

```python
# JPEG (best for photos)
gen.save("thumb.jpg", format="JPEG")

# PNG (best for graphics/transparency)
gen.save("thumb.png", format="PNG")

# WebP (modern, smaller files)
gen.save("thumb.webp", format="WEBP", quality=80)
```

## Output Structure

```python
result = gen.generate_sizes(
    sizes=[(100, 100), (200, 200)],
    output_dir="./thumbs/"
)

# Returns:
[
    {
        "size": "100x100",
        "path": "./thumbs/image_100x100.jpg",
        "file_size": 5432
    },
    {
        "size": "200x200",
        "path": "./thumbs/image_200x200.jpg",
        "file_size": 15234
    }
]
```

## Example Workflows

### E-commerce Product Images

```python
gen = ThumbnailGenerator()
gen.load("product.jpg")

# Generate product thumbnails
gen.generate_sizes(
    sizes=[
        (80, 80),    # Cart thumbnail
        (200, 200),  # Category listing
        (400, 400),  # Product page
        (800, 800)   # Zoom view
    ],
    output_dir="./product_images/",
    prefix="sku_12345"
)
```

### Gallery Thumbnails

```python
gen = ThumbnailGenerator()
results = gen.process_folder(
    input_dir="./gallery/",
    output_dir="./gallery/thumbs/",
    width=300,
    height=200
)
```

### Social Media Batch

```python
gen = ThumbnailGenerator()

for image in Path("./photos/").glob("*.jpg"):
    gen.load(str(image))
    gen.apply_preset("social", f"./social/{image.stem}/")
```

## Dependencies

- pillow>=10.0.0
- numpy>=1.24.0
