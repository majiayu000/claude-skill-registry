---
name: image-optimization
description: Optimizes images for web performance using modern formats, responsive techniques, and lazy loading strategies. Use when improving page load times, implementing responsive images, or preparing assets for production deployment.
license: MIT
---

# Image Optimization

Optimize images for web performance with modern formats and responsive techniques.

## Format Selection

| Format | Best For | Compression |
|--------|----------|-------------|
| JPEG | Photos | Lossy, 50-70% reduction |
| PNG | Icons, transparency | Lossless, 10-30% |
| WebP | Modern browsers | 25-35% better than JPEG |
| AVIF | Next-gen | 50% better than JPEG |
| SVG | Logos, icons | Vector, scalable |

## Responsive Images

```html
<picture>
  <source srcset="image.avif" type="image/avif">
  <source srcset="image.webp" type="image/webp">
  <img
    src="image.jpg"
    srcset="image-400.jpg 400w, image-800.jpg 800w, image-1200.jpg 1200w"
    sizes="(max-width: 600px) 100vw, 50vw"
    alt="Description"
    loading="lazy"
    decoding="async"
  >
</picture>
```

## Lazy Loading

```html
<!-- Native lazy loading -->
<img src="image.jpg" loading="lazy" alt="Description">

<!-- With blur placeholder -->
<img
  src="placeholder-blur.jpg"
  data-src="image.jpg"
  class="lazy"
  alt="Description"
>
```

## Build Pipeline (Sharp)

```javascript
const sharp = require('sharp');

async function optimizeImage(input, output) {
  await sharp(input)
    .resize(1200, null, { withoutEnlargement: true })
    .webp({ quality: 80 })
    .toFile(output);
}
```

## Performance Targets

| Asset Type | Target Size |
|------------|-------------|
| Hero image | <200KB |
| Thumbnail | <30KB |
| Total images | <500KB |

## Optimization Checklist

- [ ] Use WebP with JPEG fallback
- [ ] Implement responsive srcset
- [ ] Enable lazy loading for below-fold
- [ ] Compress at quality 70-85
- [ ] Serve from CDN
- [ ] Set proper cache headers
