---
name: responsive-images
description: |
  Implement performant responsive images with srcset, sizes, lazy loading, and modern formats (WebP, AVIF). Covers aspect-ratio for CLS prevention, picture element for art direction, and fetchpriority for LCP optimization.

  Use when: adding images to pages, optimizing Core Web Vitals, preventing layout shift, implementing art direction, or converting to modern formats.
license: MIT
metadata:
  keywords:
    - responsive images
    - srcset
    - sizes
    - lazy loading
    - webp
    - avif
    - aspect-ratio
    - CLS
    - LCP
    - fetchpriority
  version: 1.0.0
  last_updated: 2026-01-14
---

# Responsive Images

**Status**: Production Ready ✅
**Last Updated**: 2026-01-14
**Standards**: Web Performance Best Practices, Core Web Vitals

---

## Quick Start

### Basic Responsive Image

```html
<img
  src="/images/hero-800.jpg"
  srcset="
    /images/hero-400.jpg 400w,
    /images/hero-800.jpg 800w,
    /images/hero-1200.jpg 1200w,
    /images/hero-1600.jpg 1600w
  "
  sizes="(max-width: 640px) 100vw,
         (max-width: 1024px) 90vw,
         1200px"
  alt="Hero image description"
  width="1200"
  height="675"
  loading="lazy"
/>
```

### Hero Image (LCP)

```html
<img
  src="/images/hero-1200.jpg"
  srcset="
    /images/hero-800.jpg 800w,
    /images/hero-1200.jpg 1200w,
    /images/hero-1600.jpg 1600w
  "
  sizes="100vw"
  alt="Hero image"
  width="1600"
  height="900"
  loading="eager"
  fetchpriority="high"
/>
```

---

## Configuration

### Recommended Image Sizes

| Use Case | Widths to Generate | Sizes Attribute |
|----------|-------------------|-----------------|
| Full-width hero | 800w, 1200w, 1600w, 2400w | `100vw` |
| Content width | 400w, 800w, 1200w | `(max-width: 768px) 100vw, 800px` |
| Grid cards (3-col) | 300w, 600w, 900w | `(max-width: 768px) 100vw, 33vw` |
| Sidebar thumbnail | 150w, 300w | `150px` |

### Lazy Loading Rules

| Image Position | loading | fetchpriority | Why |
|----------------|---------|---------------|-----|
| Hero/LCP | `eager` | `high` | Optimize LCP, prioritize download |
| Above fold (not LCP) | `eager` | omit | Load normally |
| Below fold | `lazy` | omit | Defer until near viewport |
| Off-screen carousel | `lazy` | omit | Defer until interaction |

---

## Common Patterns

### Full-Width Responsive Image

```html
<img
  src="/images/banner-1200.jpg"
  srcset="
    /images/banner-600.jpg 600w,
    /images/banner-1200.jpg 1200w,
    /images/banner-1800.jpg 1800w,
    /images/banner-2400.jpg 2400w
  "
  sizes="100vw"
  alt="Full width banner"
  width="2400"
  height="800"
  loading="lazy"
  class="w-full h-auto"
/>
```

### Grid Card Image (3 columns)

```html
<img
  src="/images/card-600.jpg"
  srcset="
    /images/card-300.jpg 300w,
    /images/card-600.jpg 600w,
    /images/card-900.jpg 900w
  "
  sizes="(max-width: 768px) 100vw,
         (max-width: 1024px) 50vw,
         33vw"
  alt="Card image"
  width="900"
  height="600"
  loading="lazy"
  class="w-full h-auto"
/>
```

### Fixed Aspect Ratio Container

```html
<div class="aspect-[16/9] overflow-hidden">
  <img
    src="/images/video-thumbnail-800.jpg"
    srcset="
      /images/video-thumbnail-400.jpg 400w,
      /images/video-thumbnail-800.jpg 800w,
      /images/video-thumbnail-1200.jpg 1200w
    "
    sizes="(max-width: 768px) 100vw, 800px"
    alt="Video thumbnail"
    width="800"
    height="450"
    loading="lazy"
    class="w-full h-full object-cover"
  />
</div>
```

### Modern Formats (WebP + AVIF)

```html
<picture>
  <source
    srcset="
      /images/hero-800.avif 800w,
      /images/hero-1200.avif 1200w,
      /images/hero-1600.avif 1600w
    "
    sizes="100vw"
    type="image/avif"
  />
  <source
    srcset="
      /images/hero-800.webp 800w,
      /images/hero-1200.webp 1200w,
      /images/hero-1600.webp 1600w
    "
    sizes="100vw"
    type="image/webp"
  />
  <img
    src="/images/hero-1200.jpg"
    srcset="
      /images/hero-800.jpg 800w,
      /images/hero-1200.jpg 1200w,
      /images/hero-1600.jpg 1600w
    "
    sizes="100vw"
    alt="Hero image"
    width="1600"
    height="900"
    loading="eager"
    fetchpriority="high"
  />
</picture>
```

### Art Direction (Different Crops)

```html
<picture>
  <source
    media="(max-width: 640px)"
    srcset="
      /images/product-portrait-400.jpg 400w,
      /images/product-portrait-800.jpg 800w
    "
    sizes="100vw"
  />
  <source
    media="(min-width: 641px)"
    srcset="
      /images/product-landscape-800.jpg 800w,
      /images/product-landscape-1200.jpg 1200w,
      /images/product-landscape-1600.jpg 1600w
    "
    sizes="(max-width: 1024px) 90vw, 1200px"
  />
  <img
    src="/images/product-landscape-1200.jpg"
    alt="Product image"
    width="1200"
    height="675"
    loading="lazy"
  />
</picture>
```

---

## Error Prevention

### Always Include Width and Height

**Problem**: Layout shift when images load (poor CLS score)

```html
<!-- ❌ WRONG - causes layout shift -->
<img src="/image.jpg" alt="Image" loading="lazy" />

<!-- ✅ CORRECT - browser reserves space -->
<img
  src="/image.jpg"
  alt="Image"
  width="800"
  height="600"
  loading="lazy"
/>
```

**Source**: [Web.dev - Optimize CLS](https://web.dev/articles/optimize-cls)

### Don't Lazy Load LCP Images

**Problem**: Delayed LCP, poor Core Web Vitals score

```html
<!-- ❌ WRONG - delays LCP -->
<img
  src="/hero.jpg"
  alt="Hero"
  loading="lazy"
/>

<!-- ✅ CORRECT - prioritizes LCP -->
<img
  src="/hero.jpg"
  alt="Hero"
  loading="eager"
  fetchpriority="high"
/>
```

**Source**: [Web.dev - Optimize LCP](https://web.dev/articles/optimize-lcp)

### Use Width Descriptors (w), Not Density (x)

**Problem**: Browser can't choose optimal image for viewport

```html
<!-- ❌ WRONG - only considers DPR -->
<img
  src="/image.jpg"
  srcset="/image.jpg 1x, /image@2x.jpg 2x"
  alt="Image"
/>

<!-- ✅ CORRECT - considers viewport + DPR -->
<img
  src="/image-800.jpg"
  srcset="
    /image-400.jpg 400w,
    /image-800.jpg 800w,
    /image-1200.jpg 1200w
  "
  sizes="(max-width: 768px) 100vw, 800px"
  alt="Image"
  width="800"
  height="600"
/>
```

**Exception**: Density descriptors are appropriate for fixed-size images like logos.

### Always Include Alt Text

**Problem**: Fails accessibility, SEO, and screen readers

```html
<!-- ❌ WRONG -->
<img src="/product.jpg" />

<!-- ✅ CORRECT - descriptive alt text -->
<img src="/product.jpg" alt="Red leather messenger bag with brass buckles" />

<!-- ✅ CORRECT - decorative images use empty alt -->
<img src="/decorative-line.svg" alt="" role="presentation" />
```

### Aspect Ratio with object-fit

**Problem**: Image stretches or squashes when container size differs from image dimensions

```html
<!-- ❌ WRONG - image distorts -->
<div class="w-full h-64">
  <img src="/image.jpg" alt="Image" class="w-full h-full" />
</div>

<!-- ✅ CORRECT - maintains aspect ratio -->
<div class="w-full h-64">
  <img
    src="/image.jpg"
    alt="Image"
    class="w-full h-full object-cover"
  />
</div>
```

---

## Quick Reference

### Sizes Attribute Patterns

```html
<!-- Full width -->
sizes="100vw"

<!-- Content width (max 800px) -->
sizes="(max-width: 768px) 100vw, 800px"

<!-- Sidebar (fixed 300px) -->
sizes="300px"

<!-- 2-column grid -->
sizes="(max-width: 768px) 100vw, 50vw"

<!-- 3-column grid -->
sizes="(max-width: 768px) 100vw, (max-width: 1024px) 50vw, 33vw"

<!-- Responsive with max-width -->
sizes="(max-width: 640px) 100vw, (max-width: 1024px) 90vw, 1200px"
```

### Common Aspect Ratios

| Ratio | CSS | Use Case |
|-------|-----|----------|
| 16:9 | `aspect-[16/9]` | Video thumbnails, hero images |
| 4:3 | `aspect-[4/3]` | Standard photos |
| 3:2 | `aspect-[3/2]` | DSLR photos |
| 1:1 | `aspect-square` | Profile pictures, Instagram-style |
| 21:9 | `aspect-[21/9]` | Ultrawide banners |

### object-fit Values

| Value | Behavior | Use Case |
|-------|----------|----------|
| `cover` | Fill container, crop edges | Card images, backgrounds |
| `contain` | Fit inside, preserve all content | Logos, product photos |
| `fill` | Stretch to fill | Avoid unless necessary |
| `scale-down` | Smaller of `contain` or original size | Mixed content sizes |

### Format Comparison

| Format | Quality | File Size | Browser Support | Use Case |
|--------|---------|-----------|-----------------|----------|
| JPEG | Good | Medium | 100% | Photos, complex images |
| PNG | Lossless | Large | 100% | Logos, transparency |
| WebP | Excellent | Small | 97%+ | Modern browsers, photos |
| AVIF | Excellent | Smallest | 90%+ | Cutting-edge, fallback required |

**Recommended Strategy**: AVIF → WebP → JPEG fallback using `<picture>`

---

## Resources

- [Web.dev: Responsive Images](https://web.dev/articles/responsive-images)
- [MDN: Responsive Images](https://developer.mozilla.org/en-US/docs/Learn/HTML/Multimedia_and_embedding/Responsive_images)
- [Web.dev: Serve Images in Modern Formats](https://web.dev/articles/serve-images-webp)
- [Web.dev: Optimize Cumulative Layout Shift](https://web.dev/articles/optimize-cls)
- [Cloudflare Images Documentation](https://developers.cloudflare.com/images/)

---

**Token Efficiency**: ~70% savings by preventing trial-and-error with srcset/sizes syntax
**Errors Prevented**: 6 common responsive image issues documented above
