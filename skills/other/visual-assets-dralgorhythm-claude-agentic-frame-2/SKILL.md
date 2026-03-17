---
name: visual-assets
description: Create and manage visual assets. Use when creating graphics, icons, or images. Covers asset formats and optimization.
allowed-tools: Read, Write, Bash, Glob, Grep
---

# Visual Assets

## Asset Types

### Icons
- **SVG**: Scalable, small file size, CSS styling
- **Icon fonts**: Easy to use, limited styling
- **PNG sprites**: Legacy, larger files

### Images
- **JPEG**: Photos, complex images
- **PNG**: Transparency, screenshots
- **WebP**: Modern, smaller files
- **AVIF**: Newest, best compression

### Graphics
- **SVG**: Illustrations, logos, charts
- **Lottie**: Animations, complex motion

## Optimization

### Image Compression
```bash
# WebP conversion
cwebp -q 80 input.png -o output.webp

# AVIF conversion
avifenc input.png output.avif

# PNG optimization
pngquant --quality=65-80 input.png
```

### Responsive Images
```html
<picture>
  <source srcset="image.avif" type="image/avif">
  <source srcset="image.webp" type="image/webp">
  <img src="image.jpg" alt="Description"
       srcset="image-400.jpg 400w,
               image-800.jpg 800w,
               image-1200.jpg 1200w"
       sizes="(max-width: 600px) 100vw, 50vw">
</picture>
```

### SVG Optimization
```bash
# SVGO optimization
svgo input.svg -o output.svg
```

## Icon Guidelines

- Consistent stroke width
- Consistent sizing (24x24, 20x20)
- Optical alignment
- Clear at small sizes

## File Organization

```
assets/
├── icons/
│   ├── ui/
│   └── brand/
├── images/
│   ├── originals/
│   └── optimized/
└── illustrations/
```

## Performance Tips

1. Lazy load below-fold images
2. Use appropriate format for content
3. Serve responsive sizes
4. Consider CDN delivery
5. Set cache headers
