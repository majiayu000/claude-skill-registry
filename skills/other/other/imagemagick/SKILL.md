---
name: imagemagick
description: Guide for using ImageMagick command-line tools to perform advanced image processing tasks including format conversion, resizing, cropping, effects, transformations, and batch operations. Use when manipulating images programmatically via shell commands.
license: MIT
version: 1.0.0
---

# ImageMagick Skill

ImageMagick is a comprehensive, free, open-source software suite for creating, editing, converting, and manipulating images in over 250 formats. This skill covers command-line usage of ImageMagick tools for programmatic image processing.

## When to Use This Skill

Use this skill when:
- Converting images between formats (PNG, JPEG, WebP, GIF, etc.)
- Resizing, cropping, or transforming images
- Applying effects, filters, or adjustments to images
- Creating thumbnails or image previews
- Batch processing multiple images
- Compositing or combining images
- Adding watermarks, borders, or text to images
- Optimizing images for web or print

## Core Concepts

### Primary Commands

ImageMagick provides several command-line tools:

- **magick**: Modern unified command for all operations (ImageMagick v7+)
- **convert**: Legacy command for image conversion and manipulation (still widely used)
- **mogrify**: Modify images in-place (batch processing)
- **identify**: Display image metadata and properties
- **montage**: Create image composites and contact sheets
- **composite**: Overlay images

**Note**: In ImageMagick v7+, `magick` is the recommended command. Legacy `convert` syntax: `convert input.png output.jpg` becomes `magick input.png output.jpg`

### Command Structure

Basic syntax:
```bash
magick [input-options] input-file [operations] [output-options] output-file
```

Operations are applied **left to right** in the order specified.

### Geometry Specifications

ImageMagick uses geometry strings for dimensions:

- `100x100` - Resize to fit within 100×100 (maintains aspect ratio)
- `100x100!` - Force exact size (ignores aspect ratio)
- `100x100^` - Fill 100×100 (may crop, maintains aspect ratio)
- `100x` - Resize to width 100 (auto height)
- `x100` - Resize to height 100 (auto width)
- `50%` - Scale to 50% of original
- `100x100+10+20` - 100×100 region at offset (10, 20)

## Installation

**macOS:**
```bash
brew install imagemagick
```

**Ubuntu/Debian:**
```bash
sudo apt-get install imagemagick
```

**Verify installation:**
```bash
magick -version
# or
convert -version
```

## Common Operations

### Format Conversion

Convert between image formats:

```bash
# PNG to JPEG
magick input.png output.jpg

# JPEG to WebP
magick input.jpg output.webp

# Multiple formats
magick input.png output.jpg output.webp output.gif

# Set JPEG quality (0-100)
magick input.png -quality 85 output.jpg

# Convert with compression
magick input.png -quality 90 -strip output.jpg
```

### Resizing

Resize images while maintaining aspect ratio:

```bash
# Resize to fit within 800×600
magick input.jpg -resize 800x600 output.jpg

# Resize to specific width (auto height)
magick input.jpg -resize 800x output.jpg

# Resize to specific height (auto width)
magick input.jpg -resize x600 output.jpg

# Resize to exact dimensions (ignores aspect ratio)
magick input.jpg -resize 800x600! output.jpg

# Scale by percentage
magick input.jpg -resize 50% output.jpg

# Resize only if larger (shrink only)
magick input.jpg -resize 800x600\> output.jpg

# Resize only if smaller (enlarge only)
magick input.jpg -resize 800x600\< output.jpg
```

### Cropping

Extract portions of images:

```bash
# Crop 400×400 pixels starting at (100, 100)
magick input.jpg -crop 400x400+100+100 output.jpg

# Crop from center
magick input.jpg -gravity center -crop 400x400+0+0 output.jpg

# Remove virtual canvas after crop
magick input.jpg -crop 400x400+100+100 +repage output.jpg

# Crop to aspect ratio from center
magick input.jpg -gravity center -crop 16:9 output.jpg
```

### Resize + Crop (Thumbnail Generation)

Common pattern for creating square thumbnails:

```bash
# Resize to fill 100×100, then crop from center
magick input.jpg -resize 100x100^ -gravity center -extent 100x100 output.jpg

# Alternative using crop
magick input.jpg -resize 275x275^ -gravity center -crop 275x275+0+0 +repage output.jpg

# Create thumbnail with specific background
magick input.jpg -resize 100x100 -background white -gravity center -extent 100x100 output.jpg
```

### Effects and Filters

Apply visual effects:

```bash
# Blur
magick input.jpg -blur 0x8 output.jpg

# Gaussian blur with radius 5, sigma 3
magick input.jpg -gaussian-blur 5x3 output.jpg

# Sharpen
magick input.jpg -sharpen 0x1 output.jpg

# Grayscale
magick input.jpg -colorspace Gray output.jpg

# Sepia tone
magick input.jpg -sepia-tone 80% output.jpg

# Negate (invert colors)
magick input.jpg -negate output.jpg

# Edge detection
magick input.jpg -edge 3 output.jpg

# Emboss
magick input.jpg -emboss 2 output.jpg

# Oil painting effect
magick input.jpg -paint 4 output.jpg

# Charcoal drawing
magick input.jpg -charcoal 2 output.jpg
```

### Adjustments

Modify brightness, contrast, and colors:

```bash
# Adjust brightness (+/- 0-100)
magick input.jpg -brightness-contrast 10x0 output.jpg

# Adjust contrast
magick input.jpg -brightness-contrast 0x20 output.jpg

# Both brightness and contrast
magick input.jpg -brightness-contrast 10x20 output.jpg

# Adjust saturation
magick input.jpg -modulate 100,150,100 output.jpg

# Adjust hue
magick input.jpg -modulate 100,100,120 output.jpg

# Auto level (normalize contrast)
magick input.jpg -auto-level output.jpg

# Auto gamma correction
magick input.jpg -auto-gamma output.jpg

# Normalize (stretch histogram)
magick input.jpg -normalize output.jpg
```

### Rotation and Flipping

Transform image orientation:

```bash
# Rotate 90 degrees clockwise
magick input.jpg -rotate 90 output.jpg

# Rotate 180 degrees
magick input.jpg -rotate 180 output.jpg

# Rotate counter-clockwise
magick input.jpg -rotate -90 output.jpg

# Rotate with background color
magick input.jpg -background white -rotate 45 output.jpg

# Flip vertically
magick input.jpg -flip output.jpg

# Flip horizontally (mirror)
magick input.jpg -flop output.jpg

# Auto-orient based on EXIF
magick input.jpg -auto-orient output.jpg
```

### Borders and Frames

Add borders to images:

```bash
# Add 10px black border
magick input.jpg -border 10x10 output.jpg

# Add border with specific color
magick input.jpg -bordercolor red -border 10x10 output.jpg

# Add frame effect
magick input.jpg -mattecolor gray -frame 10x10+5+5 output.jpg

# Add shadow effect
magick input.jpg \( +clone -background black -shadow 80x3+5+5 \) \
  +swap -background white -layers merge +repage output.jpg
```

### Text and Watermarks

Add text overlays:

```bash
# Add simple text
magick input.jpg -pointsize 30 -fill white -annotate +10+30 "Hello" output.jpg

# Add text with positioning
magick input.jpg -gravity south -pointsize 20 -fill white \
  -annotate +0+10 "Copyright 2025" output.jpg

# Add text with background
magick input.jpg -gravity center -pointsize 40 -fill white \
  -undercolor black -annotate +0+0 "Watermark" output.jpg

# Add semi-transparent watermark
magick input.jpg \( -background none -fill "rgba(255,255,255,0.5)" \
  -pointsize 50 label:"DRAFT" \) -gravity center -compose over -composite output.jpg
```

### Compositing

Combine multiple images:

```bash
# Overlay watermark on image
magick input.jpg watermark.png -gravity southeast -composite output.jpg

# Overlay with transparency
magick input.jpg watermark.png -gravity center \
  -compose over -composite output.jpg

# Tile pattern
magick input.jpg pattern.png -compose over -tile -composite output.jpg

# Side-by-side images
magick input1.jpg input2.jpg +append output.jpg

# Stack images vertically
magick input1.jpg input2.jpg -append output.jpg
```

### Format-Specific Options

Optimize for different formats:

```bash
# JPEG with quality and strip metadata
magick input.png -quality 85 -strip output.jpg

# Progressive JPEG
magick input.png -quality 85 -interlace Plane output.jpg

# PNG with compression level (0-9)
magick input.jpg -quality 95 output.png

# WebP with quality
magick input.jpg -quality 80 output.webp

# WebP lossless
magick input.png -define webp:lossless=true output.webp

# GIF with optimization
magick input.png -colors 256 output.gif

# Transparent background PNG
magick input.jpg -transparent white output.png
```

## Batch Processing

### Using mogrify

Modify multiple files in-place:

```bash
# Convert all JPEGs to PNG in current directory
mogrify -format png *.jpg

# Resize all images in directory
mogrify -resize 800x600 *.jpg

# Apply to output directory (preserves originals)
mogrify -path ./output -resize 800x600 *.jpg

# Batch thumbnail generation
mogrify -path ./thumbnails -resize 275x275^ -gravity center \
  -crop 275x275+0+0 +repage *.jpg

# Batch format conversion with quality
mogrify -path ./optimized -format jpg -quality 85 -strip *.png
```

### Using shell loops

For more complex batch operations:

```bash
# Convert with custom naming
for img in *.jpg; do
  magick "$img" -resize 800x600 "resized_$img"
done

# Multi-step processing
for img in *.jpg; do
  magick "$img" -resize 1920x1080^ -gravity center \
    -crop 1920x1080+0+0 +repage -quality 85 "processed_$img"
done

# Different output format
for img in *.png; do
  magick "$img" -quality 90 "${img%.png}.jpg"
done
```

## Image Information

### Using identify

Get image metadata:

```bash
# Basic info
identify image.jpg

# Detailed information
identify -verbose image.jpg

# Format only
identify -format "%f: %wx%h %b\n" image.jpg

# Specific attributes
identify -format "%f: %wx%h, %[colorspace], %[type]\n" image.jpg

# File size
identify -format "%f: %b\n" image.jpg

# Multiple images
identify *.jpg
```

### Common format strings

- `%f` - filename
- `%w` - width
- `%h` - height
- `%b` - file size
- `%[colorspace]` - colorspace
- `%[type]` - image type
- `%[channels]` - number of channels
- `%[depth]` - bit depth

## Advanced Techniques

### Creating Contact Sheets

Use montage:

```bash
# Basic grid
montage *.jpg -geometry 200x200+2+2 contact-sheet.jpg

# With labels
montage *.jpg -geometry 200x200+2+2 -label '%f' contact-sheet.jpg

# Custom layout (3 columns)
montage *.jpg -tile 3x -geometry 200x200+5+5 contact-sheet.jpg
```

### Animated GIFs

Create animations:

```bash
# Create GIF from images
magick -delay 100 -loop 0 frame*.png animated.gif

# Optimize GIF
magick animated.gif -fuzz 5% -layers Optimize optimized.gif

# Extract frames from GIF
magick animated.gif frame_%03d.png
```

### Complex Pipelines

Chain multiple operations:

```bash
# Resize, crop, add border, adjust brightness
magick input.jpg \
  -resize 1000x1000^ \
  -gravity center \
  -crop 1000x1000+0+0 +repage \
  -bordercolor black -border 5x5 \
  -brightness-contrast 5x10 \
  -quality 90 \
  output.jpg

# Create thumbnail with watermark
magick input.jpg \
  -resize 400x400^ \
  -gravity center \
  -extent 400x400 \
  \( watermark.png -resize 100x100 \) \
  -gravity southeast -geometry +10+10 \
  -composite \
  output.jpg
```

## Performance Optimization

### Memory and Speed

```bash
# Limit memory usage (useful for large images)
magick -limit memory 2GB -limit map 4GB input.jpg -resize 50% output.jpg

# Set thread count
magick -limit thread 4 input.jpg -resize 50% output.jpg

# Use streaming for large files
magick -define stream:buffer-size=0 huge.jpg -resize 50% output.jpg
```

### Quality vs Size Trade-offs

```bash
# High quality (larger file)
magick input.jpg -quality 95 output.jpg

# Balanced (recommended for web)
magick input.jpg -quality 85 -strip output.jpg

# Lower quality (smaller file)
magick input.jpg -quality 70 -sampling-factor 4:2:0 -strip output.jpg

# Progressive JPEG (better for web)
magick input.jpg -quality 85 -interlace Plane -strip output.jpg
```

## Common Patterns

### Avatar/Profile Picture Generation

```bash
# Square thumbnail from any aspect ratio
magick input.jpg -resize 200x200^ -gravity center -extent 200x200 avatar.jpg

# Circular avatar (PNG with transparency)
magick input.jpg -resize 200x200^ -gravity center -extent 200x200 \
  \( +clone -threshold -1 -negate -fill white -draw "circle 100,100 100,0" \) \
  -alpha off -compose copy_opacity -composite avatar.png
```

### Responsive Images

```bash
# Generate multiple sizes
for size in 320 640 1024 1920; do
  magick input.jpg -resize ${size}x -quality 85 "output-${size}w.jpg"
done
```

### Watermarking

```bash
# Bottom-right watermark
magick input.jpg watermark.png -gravity southeast \
  -geometry +10+10 -composite output.jpg

# Tiled watermark
magick input.jpg \( watermark.png -alpha set -channel A \
  -evaluate multiply 0.3 +channel \) -tile -composite output.jpg
```

## Error Handling

Common issues and solutions:

**File not found:**
```bash
# Check file exists
[ -f input.jpg ] && magick input.jpg output.png || echo "File not found"
```

**Invalid geometry:**
```bash
# Validate dimensions first
identify -format "%wx%h" input.jpg
```

**Memory errors:**
```bash
# Limit resources
magick -limit memory 1GB -limit map 2GB input.jpg output.png
```

## Best Practices

1. **Always use `-strip`** to remove metadata (reduces file size)
2. **Set appropriate quality** (85 for JPEG is good balance)
3. **Use `+repage`** after crop to reset virtual canvas
4. **Quote file paths** with spaces: `"my image.jpg"`
5. **Test on sample** before batch processing
6. **Backup originals** when using mogrify
7. **Use `-auto-orient`** to respect EXIF orientation
8. **Progressive JPEGs** for web (use `-interlace Plane`)
9. **Limit memory** for large batches to prevent crashes
10. **Check output** after complex operations

## Troubleshooting

### Policy Restrictions

Some systems restrict ImageMagick operations for security:

```bash
# Check policy
identify -list policy

# Edit policy file (if needed)
sudo nano /etc/ImageMagick-6/policy.xml
# or
sudo nano /etc/ImageMagick-7/policy.xml
```

### Common Errors

**"convert: not authorized"**
- ImageMagick security policy blocking operation
- Edit policy.xml to allow specific formats/operations

**"convert: no decode delegate"**
- Missing format support library
- Install additional libraries (libjpeg, libpng, libwebp, etc.)

**"convert: memory allocation failed"**
- Image too large or insufficient memory
- Use `-limit` flags or process in smaller chunks

## Resources

- Official Documentation: https://imagemagick.org/
- Command-line Options: https://imagemagick.org/script/command-line-options.php
- Examples: https://imagemagick.org/Usage/
- Format Support: https://imagemagick.org/script/formats.php

## Command Reference Quick Guide

**Format Conversion:**
```bash
magick input.ext output.ext
```

**Resize:**
```bash
magick input.jpg -resize WIDTHxHEIGHT output.jpg
```

**Crop:**
```bash
magick input.jpg -crop WIDTHxHEIGHT+X+Y output.jpg
```

**Thumbnail:**
```bash
magick input.jpg -resize 100x100^ -gravity center -extent 100x100 thumb.jpg
```

**Effects:**
```bash
magick input.jpg -blur 0x8 output.jpg
```

**Batch:**
```bash
mogrify -resize 800x600 *.jpg
```

**Info:**
```bash
identify -verbose image.jpg
```
