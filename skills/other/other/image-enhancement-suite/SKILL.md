---
name: image-enhancement-suite
description: "Batch image processing: resize, crop, watermark, color correction, format conversion, compression. Quality presets for web, print, and social media."
---

# Image Enhancement Suite

Professional image processing toolkit that handles common image tasks without requiring Photoshop or similar software. Process single images or entire folders with consistent, high-quality results.

## Core Capabilities

- **Resize & Crop**: Smart resizing with aspect ratio preservation, crop to specific dimensions
- **Watermark**: Add text or image watermarks with positioning and opacity control
- **Color Correction**: Brightness, contrast, saturation, sharpness adjustments
- **Format Conversion**: Convert between PNG, JPEG, WebP, BMP, TIFF, GIF
- **Compression**: Optimize file size with quality presets
- **Filters**: Apply preset filters (grayscale, sepia, vintage, blur, sharpen)
- **Batch Processing**: Process multiple images with same settings

## Quick Start

```python
from scripts.image_enhancer import ImageEnhancer

# Single image processing
enhancer = ImageEnhancer("photo.jpg")
enhancer.resize(width=800).sharpen(0.5).save("photo_enhanced.jpg")

# Batch processing
from scripts.image_enhancer import batch_process
batch_process(
    input_dir="raw_photos/",
    output_dir="processed/",
    operations=[
        ("resize", {"width": 1200}),
        ("watermark", {"text": "© 2024"}),
        ("compress", {"quality": 85})
    ]
)
```

## Operations Reference

### Resize

```python
# By width (maintain aspect ratio)
enhancer.resize(width=800)

# By height (maintain aspect ratio)
enhancer.resize(height=600)

# Exact dimensions (may distort)
enhancer.resize(width=800, height=600, maintain_aspect=False)

# Fit within bounds
enhancer.resize(max_width=1200, max_height=800)

# Scale by percentage
enhancer.resize(scale=0.5)  # 50%
```

### Crop

```python
# Crop to specific dimensions from center
enhancer.crop(width=800, height=600)

# Crop with position
enhancer.crop(width=800, height=600, position='top-left')
# Positions: 'center', 'top-left', 'top-right', 'bottom-left', 'bottom-right'

# Crop to exact coordinates (left, top, right, bottom)
enhancer.crop(box=(100, 100, 900, 700))

# Smart crop (content-aware)
enhancer.smart_crop(width=800, height=600)
```

### Watermark

```python
# Text watermark
enhancer.watermark(
    text="© 2024 Company",
    position='bottom-right',
    opacity=0.5,
    font_size=24,
    color='white'
)

# Image watermark
enhancer.watermark(
    image="logo.png",
    position='bottom-right',
    opacity=0.3,
    scale=0.2  # 20% of main image width
)

# Tiled watermark
enhancer.watermark(
    text="DRAFT",
    tiled=True,
    opacity=0.1,
    rotation=45
)
```

### Color Adjustments

```python
# Individual adjustments (range: -1.0 to 1.0, 0 = no change)
enhancer.brightness(0.2)    # +20% brightness
enhancer.contrast(0.3)      # +30% contrast
enhancer.saturation(-0.2)   # -20% saturation
enhancer.sharpen(0.5)       # Sharpen

# Combined adjustment
enhancer.adjust(
    brightness=0.1,
    contrast=0.2,
    saturation=0.1,
    sharpen=0.3
)

# Auto-enhance
enhancer.auto_enhance()
```

### Filters

```python
# Apply preset filters
enhancer.filter('grayscale')
enhancer.filter('sepia')
enhancer.filter('vintage')
enhancer.filter('blur')
enhancer.filter('sharpen')
enhancer.filter('edge_enhance')
enhancer.filter('emboss')

# Custom blur
enhancer.blur(radius=2)

# Gaussian blur
enhancer.gaussian_blur(radius=3)
```

### Format Conversion

```python
# Convert to different format
enhancer.save("output.png")   # Auto-detect from extension
enhancer.save("output.webp")
enhancer.save("output.jpg")

# Explicit format
enhancer.convert('PNG').save("output.png")
enhancer.convert('WEBP').save("output.webp")
```

### Compression

```python
# JPEG quality (1-100)
enhancer.compress(quality=85).save("compressed.jpg")

# WebP with quality
enhancer.save("output.webp", quality=80)

# PNG optimization
enhancer.optimize_png().save("optimized.png")

# Target file size
enhancer.compress_to_size(max_kb=500).save("sized.jpg")
```

## Quality Presets

```python
# Web optimized
enhancer.preset('web')  # 1200px max, 85 quality, WebP

# Social media
enhancer.preset('instagram')  # 1080x1080, optimized
enhancer.preset('twitter')    # 1200x675
enhancer.preset('facebook')   # 1200x630
enhancer.preset('linkedin')   # 1200x627

# Print quality
enhancer.preset('print_4x6')   # 1800x1200, 300dpi
enhancer.preset('print_8x10')  # 3000x2400, 300dpi

# Thumbnail
enhancer.preset('thumbnail')   # 150x150, center crop
enhancer.preset('preview')     # 400px max, 70 quality
```

## Batch Processing

### Process Directory

```python
from scripts.image_enhancer import batch_process

# Apply same operations to all images
results = batch_process(
    input_dir="photos/",
    output_dir="processed/",
    operations=[
        ("resize", {"width": 1200}),
        ("watermark", {"text": "© 2024", "position": "bottom-right"}),
        ("compress", {"quality": 85})
    ],
    formats=['jpg', 'png'],  # Only process these formats
    recursive=True           # Include subdirectories
)

print(f"Processed: {results['success']} images")
print(f"Failed: {results['failed']} images")
```

### Rename Pattern

```python
batch_process(
    input_dir="photos/",
    output_dir="processed/",
    operations=[("resize", {"width": 800})],
    rename_pattern="{name}_web_{index:03d}"
)
# Output: photo_web_001.jpg, photo_web_002.jpg, ...
```

### Generate Multiple Sizes

```python
from scripts.image_enhancer import generate_sizes

# Create multiple sizes from one image
sizes = generate_sizes(
    "hero.jpg",
    output_dir="responsive/",
    widths=[320, 640, 1024, 1920],
    format='webp'
)
# Output: hero_320.webp, hero_640.webp, etc.
```

## Icon Generation

```python
from scripts.image_enhancer import generate_icons

# Generate favicon and app icons from single image
icons = generate_icons(
    "logo.png",
    output_dir="icons/",
    sizes=[16, 32, 48, 64, 128, 256, 512]
)
```

## Metadata Operations

```python
# Read EXIF data
metadata = enhancer.get_metadata()
print(metadata['camera'])
print(metadata['date_taken'])
print(metadata['gps'])

# Strip metadata (privacy)
enhancer.strip_metadata()

# Preserve specific metadata
enhancer.strip_metadata(keep=['copyright', 'artist'])
```

## CLI Usage

```bash
# Single file
python image_enhancer.py input.jpg -o output.jpg --resize 800 --quality 85

# Batch processing
python image_enhancer.py photos/ -o processed/ --resize 1200 --watermark "© 2024"

# Apply preset
python image_enhancer.py photo.jpg --preset instagram

# Generate icons
python image_enhancer.py logo.png --icons icons/
```

## Supported Formats

| Format | Read | Write | Notes |
|--------|------|-------|-------|
| JPEG | Yes | Yes | Lossy, best for photos |
| PNG | Yes | Yes | Lossless, supports transparency |
| WebP | Yes | Yes | Modern format, good compression |
| GIF | Yes | Yes | Animation support |
| BMP | Yes | Yes | Uncompressed |
| TIFF | Yes | Yes | High quality, large files |
| ICO | Yes | Yes | Icon format |
| HEIC | Yes | No | iPhone photos (read only) |

## Error Handling

```python
from scripts.image_enhancer import ImageEnhancer, ImageError

try:
    enhancer = ImageEnhancer("photo.jpg")
    enhancer.resize(width=800).save("output.jpg")
except ImageError as e:
    print(f"Image error: {e}")
except FileNotFoundError:
    print("Image file not found")
```

## Configuration

```python
enhancer = ImageEnhancer("photo.jpg")

# Global settings
enhancer.config.update({
    'default_quality': 85,
    'default_format': 'webp',
    'preserve_metadata': False,
    'color_profile': 'sRGB',
    'dpi': 72
})
```

## Performance Tips

1. **Large batches**: Use `batch_process()` with `parallel=True`
2. **Memory**: Process one image at a time for very large files
3. **Speed**: WebP encoding is slower but produces smaller files
4. **Quality**: Start at 85 quality, reduce if file size is critical

## Dependencies

```
pillow>=10.0.0
opencv-python>=4.8.0
numpy>=1.24.0
```
