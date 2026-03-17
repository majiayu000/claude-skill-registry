---
name: image-processor
description: "Process images with resize, format conversion, and optimization. Use when working with image files, need to resize images, convert formats (PNG/JPG/WebP), or optimize images for web. Not for video processing, image generation, or analysis."
context: fork
agent: general-purpose
skills:
  - file-utils
---

# Image Processor

Resize, convert, and optimize images for web deployment. Supports PNG, JPG, and WebP formats.

## Quick Start

Provide image paths and desired operations. The skill handles resizing, format conversion, and optimization automatically.

## Navigation

| If you need... | Read this section... |
| :------------- | :------------------- |
| Resize images | ## PATTERN: Resize |
| Convert formats | ## PATTERN: Format Conversion |
| Optimize for web | ## PATTERN: Web Optimization |
| Batch processing | ## PATTERN: Batch Processing |
| Output location | ## PATTERN: Output Configuration |

## PATTERN: Resize

Specify target dimensions using pixels or percentage:

```
Input: /path/to/image.jpg
Width: 800
Height: 600
Maintain aspect ratio: true
```

## PATTERN: Format Conversion

Convert between PNG, JPG, and WebP:

```
Input: /path/to/image.png
Output format: webp
Quality: 85
```

## PATTERN: Web Optimization

Automatic optimization for web deployment:

- Lossless compression for graphics
- Progressive JPEG encoding
- WebP with alpha channel support
- Target file size limits

## PATTERN: Batch Processing

Process multiple images with the same settings:

```
Input directory: /path/to/images/
Output directory: /path/to/output/
Operations: [resize, convert, optimize]
Format: webp
```

## PATTERN: Output Configuration

Configure where processed images are saved:

- Same directory as input (overwrite)
- Separate output directory
- Custom filename patterns

---

<critical_constraint>
Process only raster images (PNG, JPG, WebP). Reject vector formats (SVG) and video files.
Always validate input files exist before processing.
Preserve original files unless explicitly requested to overwrite.
</critical_constraint>
