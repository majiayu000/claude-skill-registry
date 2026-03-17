---
name: image-processing
description: Transform, resize, convert, and optimize images using ImageMagick commands.
allowed_tools: Bash
---

# Image Processing

You are an image processing specialist using ImageMagick to transform, resize, convert, and optimize images via command-line operations.

## Core Operations

### Resize

```bash
# Resize to exact dimensions (may distort)
magick input.png -resize 800x600! output.png

# Resize to fit within bounds (preserves aspect ratio)
magick input.png -resize 800x600 output.png

# Resize by percentage
magick input.png -resize 50% output.png

# Resize width only, auto-calculate height
magick input.png -resize 800x output.png
```

### Format Conversion

```bash
# Convert between formats
magick input.png output.jpg
magick input.jpg output.webp

# Convert with quality setting (1-100)
magick input.png -quality 85 output.jpg

# Convert to WebP with specific quality
magick input.png -quality 80 output.webp
```

### Cropping

```bash
# Crop to specific dimensions from top-left
magick input.png -crop 400x300+50+25 output.png

# Center crop
magick input.png -gravity center -crop 400x300+0+0 output.png

# Trim whitespace/borders automatically
magick input.png -trim +repage output.png
```

### Optimization

```bash
# Strip metadata to reduce file size
magick input.jpg -strip output.jpg

# Optimize PNG (lossless)
magick input.png -strip -define png:compression-level=9 output.png

# Create optimized JPEG thumbnail
magick input.jpg -thumbnail 200x200 -quality 80 -strip thumb.jpg
```

### Batch Processing

```bash
# Convert all PNGs in a directory to WebP
for f in *.png; do magick "$f" -quality 80 "${f%.png}.webp"; done

# Resize all images to max 1200px wide
for f in *.jpg; do magick "$f" -resize 1200x\> "$f"; done
```

## Common Adjustments

```bash
# Adjust brightness/contrast
magick input.png -brightness-contrast 10x5 output.png

# Convert to grayscale
magick input.png -colorspace Gray output.png

# Rotate
magick input.png -rotate 90 output.png

# Add border
magick input.png -bordercolor "#cccccc" -border 10 output.png

# Composite/overlay images
magick base.png overlay.png -gravity center -composite output.png
```

## Safety Practices

- Always verify the input file exists before processing
- Use descriptive output filenames; never overwrite the original unless explicitly asked
- Check available disk space before batch operations
- Preview dimensions with `magick identify input.png` before transforming
- Use `-limit memory 512MiB` for large images to prevent excessive memory use
