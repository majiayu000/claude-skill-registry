---
name: Image Files
description: Image manipulation using ImageMagick command-line tools for resizing, converting, optimizing, and batch processing
---

# Image Files

## Instructions

When helping users work with image files, follow these guidelines:

1. **Tool Availability**: ImageMagick is installed and available on the system path. Use `magick` command (modern syntax) or legacy commands (`convert`, `identify`, `mogrify`)
If it is not on the path look in C:\Program Files\ImageMagick-7.1.2-Q16-HDRI

2. **Modern vs Legacy Syntax**:
   - **Modern** (ImageMagick 7+): `magick convert input.jpg output.png`
   - **Legacy** (ImageMagick 6): `convert input.jpg output.png`
   - Try modern syntax first, fall back to legacy if command not found

3. **Common Operations**:
   - **Resize**: Use `-resize` with geometry (e.g., `800x600`, `50%`, `800x`)
   - **Convert Format**: Change file extension (e.g., `.jpg` to `.png`)
   - **Quality**: Use `-quality` for JPEG compression (1-100)
   - **Strip Metadata**: Use `-strip` to remove EXIF data
   - **Batch Processing**: Use `mogrify` for in-place edits or shell loops for batch conversions

4. **Preserve Aspect Ratio**: Use geometry without `!` suffix (e.g., `800x600` not `800x600!`)

5. **Output Paths**: Always specify full output path to avoid overwriting originals

6. **Format Support**: Common formats include JPG, PNG, GIF, BMP, TIFF, WebP, PDF

7. **Error Handling**: Check file exists before processing, verify output was created

8. **Performance**: For batch operations, process files in parallel if system has multiple cores

## Examples

### Example 1: Resize Single Image
```
User: Resize this image to 800px wide, maintaining aspect ratio

Claude: I'll use ImageMagick to resize the image:
- Preserve aspect ratio with 800x geometry
- Keep original format
- Save to new filename to preserve original

magick convert input.jpg -resize 800x output.jpg
```

### Example 2: Batch Convert and Optimize
```
User: Convert all PNG files to JPEG and reduce file size

Claude: I'll batch convert PNG to JPEG with optimization:
- Strip metadata with -strip
- Set quality to 85 (good balance)
- Process all PNG files in directory

for file in *.png; do magick convert "$file" -strip -quality 85 "${file%.png}.jpg"; done
```

### Example 3: Generate Thumbnails
```
User: Create thumbnails for all images in a folder

Claude: I'll generate thumbnails:
- Resize to 200x200 (constrained, maintain aspect)
- Save with _thumb suffix
- Preserve format

for img in *.jpg; do magick convert "$img" -resize 200x200 "thumbs/${img%.jpg}_thumb.jpg"; done
```

### Example 4: Get Image Information
```
User: What are the dimensions of this image?

Claude: I'll use identify to get image details:

magick identify input.jpg
# or: identify input.jpg
```

---

# Reference Implementation Details

Common ImageMagick operations and patterns.

## Basic Operations

### Resize Images

**Maintain Aspect Ratio**:
```bash
# Resize to width of 800px (height auto)
magick convert input.jpg -resize 800x output.jpg

# Resize to height of 600px (width auto)
magick convert input.jpg -resize x600 output.jpg

# Resize to fit within 800x600 box
magick convert input.jpg -resize 800x600 output.jpg

# Resize to 50% of original
magick convert input.jpg -resize 50% output.jpg
```

**Force Exact Dimensions** (distorts if needed):
```bash
magick convert input.jpg -resize 800x600! output.jpg
```

**Resize and Crop to Exact Dimensions**:
```bash
# Crop to center after resize
magick convert input.jpg -resize 800x600^ -gravity center -extent 800x600 output.jpg
```

### Convert Formats

```bash
# JPG to PNG
magick convert input.jpg output.png

# PNG to JPG with quality
magick convert input.png -quality 90 output.jpg

# Multiple formats
magick convert input.tiff output.jpg output.png

# PDF to images (one per page)
magick convert document.pdf page-%03d.jpg
```

### Optimize Images

**JPEG Optimization**:
```bash
# Reduce quality (85 is good balance)
magick convert input.jpg -quality 85 output.jpg

# Strip metadata and optimize
magick convert input.jpg -strip -quality 85 output.jpg

# Progressive JPEG
magick convert input.jpg -interlace Plane -quality 85 output.jpg
```

**PNG Optimization**:
```bash
# Basic PNG optimization
magick convert input.png -strip output.png

# Reduce PNG colors (for smaller file)
magick convert input.png -colors 256 output.png
```

### Crop and Trim

```bash
# Crop to specific region (width x height + x_offset + y_offset)
magick convert input.jpg -crop 800x600+100+50 output.jpg

# Auto-trim whitespace
magick convert input.jpg -trim output.jpg

# Add border
magick convert input.jpg -border 10x10 -bordercolor white output.jpg
```

### Image Information

```bash
# Basic info (format, dimensions, size)
magick identify input.jpg

# Verbose info (all metadata)
magick identify -verbose input.jpg

# Just dimensions
magick identify -format "%wx%h" input.jpg
```

## Batch Operations

### Batch Resize

**Using mogrify (in-place modification)**:
```bash
# DANGEROUS: Overwrites originals!
magick mogrify -resize 800x *.jpg

# Safer: Output to different directory
mkdir resized
magick mogrify -path resized -resize 800x *.jpg
```

**Using loop (safer)**:
```bash
# Bash loop for batch resize
mkdir output
for img in *.jpg; do
  magick convert "$img" -resize 800x "output/$img"
done

# PowerShell loop
mkdir output
Get-ChildItem *.jpg | ForEach-Object {
  magick convert $_.Name -resize 800x "output/$($_.Name)"
}
```

### Batch Convert Format

```bash
# Convert all PNG to JPG
for file in *.png; do
  magick convert "$file" -quality 90 "${file%.png}.jpg"
done

# Convert all to WebP
for file in *.jpg; do
  magick convert "$file" -quality 90 "${file%.jpg}.webp"
done
```

### Batch Optimize

```bash
# Optimize all JPEGs in place (with backup)
mkdir originals
for img in *.jpg; do
  cp "$img" "originals/$img"
  magick convert "$img" -strip -quality 85 "$img"
done
```

### Parallel Processing

```bash
# Process files in parallel (requires GNU parallel)
ls *.jpg | parallel magick convert {} -resize 800x output/{}

# Or using xargs (Unix/Linux)
ls *.jpg | xargs -P 4 -I {} magick convert {} -resize 800x output/{}
```

## Advanced Operations

### Watermarking

```bash
# Add text watermark
magick convert input.jpg \
  -gravity southeast \
  -pointsize 24 \
  -fill white \
  -annotate +10+10 'Copyright 2025' \
  output.jpg

# Add image watermark
magick convert input.jpg watermark.png \
  -gravity southeast \
  -geometry +10+10 \
  -composite \
  output.jpg
```

### Image Composition

```bash
# Combine images horizontally
magick convert img1.jpg img2.jpg +append output.jpg

# Combine images vertically
magick convert img1.jpg img2.jpg -append output.jpg

# Create montage/grid
magick montage *.jpg -tile 3x3 -geometry +5+5 grid.jpg
```

### Effects and Filters

```bash
# Convert to grayscale
magick convert input.jpg -colorspace Gray output.jpg

# Blur
magick convert input.jpg -blur 0x8 output.jpg

# Sharpen
magick convert input.jpg -sharpen 0x1 output.jpg

# Rotate
magick convert input.jpg -rotate 90 output.jpg

# Flip/Flop
magick convert input.jpg -flip output.jpg    # vertical flip
magick convert input.jpg -flop output.jpg    # horizontal flip

# Sepia tone
magick convert input.jpg -sepia-tone 80% output.jpg
```

### Background Removal

```bash
# Remove white background (make transparent)
magick convert input.jpg -fuzz 10% -transparent white output.png

# Replace background color
magick convert input.jpg -fuzz 10% -fill blue -opaque white output.jpg
```

## Useful Patterns

### Create Thumbnails with Prefix/Suffix

```bash
# Add _thumb suffix
for img in *.jpg; do
  magick convert "$img" -resize 200x200 "${img%.jpg}_thumb.jpg"
done

# Add thumb_ prefix
for img in *.jpg; do
  magick convert "$img" -resize 200x200 "thumb_$img"
done
```

### Maintain Directory Structure

```bash
# Recursively process images, maintaining directory structure
find . -name "*.jpg" -type f | while read file; do
  dir=$(dirname "$file")
  name=$(basename "$file")
  mkdir -p "output/$dir"
  magick convert "$file" -resize 800x "output/$dir/$name"
done
```

### Progressive Quality Outputs

```bash
# Generate multiple quality versions
for quality in 95 85 75 60; do
  magick convert input.jpg -quality $quality "output_q${quality}.jpg"
done
```

### Generate Responsive Image Sizes

```bash
# Create common responsive sizes
for width in 320 640 768 1024 1920; do
  magick convert input.jpg -resize ${width}x "responsive/image_${width}w.jpg"
done
```

## Error Handling and Validation

### Check File Exists

```bash
if [ -f "input.jpg" ]; then
  magick convert input.jpg -resize 800x output.jpg
else
  echo "Error: input.jpg not found"
fi
```

### Verify Output Created

```bash
magick convert input.jpg -resize 800x output.jpg
if [ -f "output.jpg" ]; then
  echo "Success: output.jpg created"
else
  echo "Error: conversion failed"
fi
```

### Handle Spaces in Filenames

```bash
# Always quote variables
for img in *.jpg; do
  magick convert "$img" -resize 800x "output/$img"
done
```

## Format-Specific Options

### JPEG

```bash
# Quality (1-100, default 92)
-quality 85

# Sampling factor (4:2:0 for smaller files)
-sampling-factor 4:2:0

# Progressive
-interlace Plane

# Strip metadata
-strip
```

### PNG

```bash
# Compression level (0-9, higher = smaller but slower)
-quality 95  # PNG quality is compression level

# Bit depth
-depth 8

# Remove alpha channel
-alpha off
```

### WebP

```bash
# WebP quality
-quality 90

# Lossless WebP
-define webp:lossless=true
```

## Common Use Cases

### Prepare Images for Web

```bash
# Optimize for web: resize, strip metadata, optimize quality
magick convert input.jpg \
  -resize 1920x \
  -strip \
  -quality 85 \
  -sampling-factor 4:2:0 \
  -interlace Plane \
  output.jpg
```

### Convert Screenshots to Optimized Format

```bash
# PNG screenshots to optimized JPEG
for png in *.png; do
  magick convert "$png" -strip -quality 90 "${png%.png}.jpg"
done
```

### Create Social Media Images

```bash
# Facebook/Twitter cover (1200x630)
magick convert input.jpg \
  -resize 1200x630^ \
  -gravity center \
  -extent 1200x630 \
  social_cover.jpg

# Instagram square (1080x1080)
magick convert input.jpg \
  -resize 1080x1080^ \
  -gravity center \
  -extent 1080x1080 \
  instagram.jpg
```

## Troubleshooting

### ImageMagick Not Found

```bash
# Check if installed
magick --version
convert --version

# Windows: Check PATH environment variable
# Linux: sudo apt-get install imagemagick
# macOS: brew install imagemagick
```

### Permission Denied

```bash
# Check file permissions
ls -l input.jpg

# Make readable
chmod 644 input.jpg
```

### Out of Memory

```bash
# Limit memory usage
magick convert input.jpg -limit memory 1GB -resize 800x output.jpg

# Process in smaller batches
```

### Policy Errors (PDF, etc.)

```bash
# Edit ImageMagick policy.xml
# Location: /etc/ImageMagick-7/policy.xml
# Remove or comment out restrictive policies for PDF, PS, etc.
```

## Command Reference

### Core Commands

- `magick convert` - Convert and modify images
- `magick identify` - Display image information
- `magick mogrify` - Modify images in place
- `magick montage` - Create composite images
- `magick compare` - Compare two images

### Legacy Commands (ImageMagick 6)

- `convert` - Same as `magick convert`
- `identify` - Same as `magick identify`
- `mogrify` - Same as `magick mogrify`
- `montage` - Same as `magick montage`
- `compare` - Same as `magick compare`

## Best Practices

1. **Always backup originals** before batch operations
2. **Use descriptive output names** to avoid confusion
3. **Quote filenames** to handle spaces and special characters
4. **Test commands** on single file before batch processing
5. **Create output directories** before processing
6. **Use appropriate quality settings** (85 is usually good for JPEGs)
7. **Strip metadata** to reduce file size (unless needed)
8. **Maintain aspect ratio** unless explicitly distorting
9. **Use modern syntax** (`magick convert`) for future compatibility
10. **Check command success** before continuing in scripts
