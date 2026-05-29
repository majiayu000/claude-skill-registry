---
name: optimizing-images
description: Optimizes images for web using compression, modern formats (WebP, AVIF), and responsive techniques. Use when reducing page weight, improving load times, or implementing responsive images. Triggers include "image optimization", "compress images", "WebP", or "srcset".
allowed-tools: Bash, Read, Glob
---

# Image Optimization

## Overview

Images typically comprise 50% of page weight. Optimization dramatically improves performance, especially on mobile networks.

## When to Use

- Website optimization
- Responsive image implementation
- Performance improvement
- Mobile experience enhancement
- Before deployment

## Instructions

### 1. **Image Compression & Formats**

```yaml
Format Selection:

JPEG:
  Best for: Photographs, complex images
  Compression: Lossy (quality 70-85)
  Size: ~50-70% reduction
  Tools: ImageMagick, TinyJPEG
  Command: convert image.jpg -quality 75 optimized.jpg

PNG:
  Best for: Icons, screenshots, transparent images
  Compression: Lossless
  Size: 10-30% reduction
  Tools: PNGQuant, OptiPNG
  Command: optipng -o3 image.png

WebP:
  Best for: Modern browsers (90% support)
  Compression: 25-35% better than JPEG/PNG
  Fallback: Use <picture> element
  Tools: cwebp
  Command: cwebp -q 75 image.jpg -o image.webp

SVG:
  Best for: Icons, logos, simple graphics
  Compression: Minify XML
  Scalable: Works at any size
  Tools: SVGO
  Command: svgo image.svg --output optimized.svg

---

Compression Levels:

Conservative (95% quality):
  JPEG: 85-90 quality
  PNG: Lossless
  Use: High-value images

Moderate (90% quality):
  JPEG: 75-80 quality
  PNG: Quantized to 256 colors
  Use: General images

Aggressive (80% quality):
  JPEG: 60-70 quality
  PNG: Reduced colors
  Use: Thumbnails, backgrounds
```

### 2. **Responsive Images**

```html
<!-- Responsive image techniques -->

<!-- srcset: Let browser choose -->
<img
  src="image.jpg"
  srcset="
    small.jpg 480w,
    medium.jpg 768w,
    large.jpg 1200w
  "
  sizes="
    (max-width: 480px) 100vw,
    (max-width: 768px) 90vw,
    80vw
  "
  alt="Description"
/>

<!-- picture: Format selection -->
<picture>
  <source srcset="image.webp" type="image/webp">
  <source srcset="image.jpg" type="image/jpeg">
  <img src="image.jpg" alt="Description">
</picture>

<!-- Lazy loading -->
<img
  src="placeholder.jpg"
  loading="lazy"
  alt="Description"
/>
```

### 3. **Optimization Process**

```yaml
Workflow:

1. Preparation
  - Export at correct size (don't scale in HTML)
  - Use appropriate format
  - Batch process similar images

2. Compression
  - Lossy: TinyJPEG/TinyPNG
  - Lossless: ImageMagick
  - Target: <100KB for main images
  - Thumbnails: <20KB

3. Format Conversion
  - WebP with JPEG fallback
  - Consider PNG for transparency
  - SVG for scalable graphics

4. Implementation
  - Use srcset for responsive
  - Lazy load below-fold
  - Optimize critical images first
  - Monitor file sizes in CI/CD

5. Validation
  - Check file sizes in DevTools
  - Test on slow networks
  - Verify quality acceptable
  - Measure performance impact

---

Quick Wins:

Remove EXIF data (saves 20-50KB):
  identify -verbose image.jpg | rg -i exif
  convert image.jpg -strip image-clean.jpg

Convert to WebP (25-35% smaller):
  cwebp -q 75 *.jpg

Batch compress with ImageMagick:
  mogrify -quality 75 -resize 1920x1080 *.jpg

Expected Results:
  - Homepage: 850KB → 300KB images
  - Performance: 3s → 1.5s load time
  - Mobile: Significant improvement on 3G
```

### 4. **Monitoring & Best Practices**

```yaml
Performance Targets:

Hero Image: <200KB
Thumbnail: <30KB
Icon: <5KB
Total images: <500KB
Target gzipped: <300KB

Tools:
  - ImageOptim (Mac)
  - ImageMagick (CLI)
  - TinyJPEG/TinyPNG (web)
  - Squoosh (web)
  - Lighthouse (audit)

Checklist:
  [ ] All images optimized
  [ ] WebP with fallback
  [ ] Responsive srcset
  [ ] Lazy loading implemented
  [ ] Correct format per image
  [ ] File size <100KB each
  [ ] Benchmarks established
  [ ] Monitoring in place
  [ ] Documented process

Tips:
  - Optimize before uploading
  - Use CDN with image optimization
  - Consider Image CDN (Imgix, Cloudinary)
  - Batch process during build
  - Monitor image additions
  - Test real devices on 3G
```

## Key Points

- JPEG for photos, PNG for graphics, SVG for icons
- WebP saves 25-35% vs JPEG/PNG
- Responsive images adapt to device
- Lazy loading defers off-screen images
- Remove EXIF and metadata
- Batch optimize before deployment
- Monitor image file sizes
- Measure performance impact
- Set strict targets per image type
- Use image CDN for global optimization
