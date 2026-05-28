---
name: imgix
description: Optimizes and transforms images with Imgix CDN using URL-based API. Use when serving responsive images, applying real-time transformations, and optimizing delivery without processing overhead.
---

# Imgix

Real-time image processing and CDN delivery via URL parameters. No server-side processing needed - transformations happen at the edge.

## Quick Start

### URL Structure

```
https://your-source.imgix.net/path/to/image.jpg?w=400&h=300&fit=crop
```

Components:
- **Source**: Your imgix subdomain
- **Path**: Image path in your origin (S3, GCS, web folder)
- **Parameters**: Transformation query string

### Basic Example

```javascript
const imgixDomain = 'your-source.imgix.net';

function imgixUrl(path, params = {}) {
  const url = new URL(`https://${imgixDomain}${path}`);
  Object.entries(params).forEach(([key, value]) => {
    url.searchParams.set(key, value);
  });
  return url.toString();
}

// Usage
const url = imgixUrl('/products/shoe.jpg', {
  w: 400,
  h: 300,
  fit: 'crop',
  auto: 'format,compress',
});
// https://your-source.imgix.net/products/shoe.jpg?w=400&h=300&fit=crop&auto=format%2Ccompress
```

## Core Parameters

### Sizing

```
?w=400           # Width
?h=300           # Height
?w=400&h=300     # Both (may crop/letterbox based on fit)
?ar=16:9&w=800   # Aspect ratio with width
```

### Fit Modes

```
?fit=clip        # Resize to fit, no crop (default)
?fit=crop        # Resize and crop to exact size
?fit=fill        # Resize to fit, fill with background
?fit=fillmax     # Like fill, never upscale
?fit=max         # Resize to fit, never upscale
?fit=min         # Resize, at least one dimension matches
?fit=scale       # Stretch to exact size (distorts)
?fit=clamp       # Like clip, never upscale
?fit=facearea    # Crop to detected face
```

### Crop & Focus

```
?crop=faces      # Crop to faces
?crop=entropy    # Crop to high-detail area
?crop=edges      # Crop to edges
?crop=top        # Crop from top
?crop=bottom,left # Crop from bottom-left

# Focal point (0-1 coordinates)
?fp-x=0.3&fp-y=0.7&fit=crop

# Face detection + crop
?fit=facearea&facepad=1.5
```

## Auto Optimization

```
?auto=format     # Best format for browser (WebP, AVIF)
?auto=compress   # Optimal compression
?auto=format,compress  # Both (recommended)
```

This automatically:
- Serves WebP to Chrome/Firefox, AVIF where supported
- Applies optimal compression per format
- Maintains quality while reducing file size

## Quality & Format

```
?q=75            # Quality 1-100 (default varies by format)
?fm=webp         # Force WebP format
?fm=avif         # Force AVIF format
?fm=jpg          # Force JPEG
?fm=png          # Force PNG
?lossless=true   # Lossless compression (PNG, WebP)
```

## Effects & Adjustments

### Color

```
?bri=20          # Brightness (-100 to 100)
?con=30          # Contrast (-100 to 100)
?sat=50          # Saturation (-100 to 100)
?hue=180         # Hue rotation (0-359)
?gam=1.5         # Gamma (0-10)
?exp=10          # Exposure (-100 to 100)
?vib=20          # Vibrance (-100 to 100)
```

### Filters

```
?blur=50         # Gaussian blur (0-2000)
?sharp=10        # Sharpen (0-100)
?sepia=80        # Sepia tone (0-100)
?monochrome=blue # Monochrome with tint
?htn=0           # Halftone
?px=10           # Pixelate
```

### Stylize

```
?duotone=000000,663399  # Duotone (shadow,highlight)
?blend=663399&bm=multiply  # Color blend
```

## Watermarks & Overlays

```
# Image overlay
?mark=watermark.png&mark-w=100&mark-align=bottom,right&mark-pad=10

# Text overlay
?txt=Hello%20World&txt-size=24&txt-color=ffffff&txt-align=center
?txt=Copyright&txt-font=Helvetica&txt-pad=20

# Blend modes
?blend=overlay.png&bm=multiply&ba=center,middle
```

## Responsive Images

### srcset Generation

```javascript
function generateSrcset(path, sizes = [400, 800, 1200, 1600]) {
  return sizes
    .map((w) => `${imgixUrl(path, { w, auto: 'format,compress' })} ${w}w`)
    .join(', ');
}

// Usage in React
function ResponsiveImage({ src, alt, sizes }) {
  return (
    <img
      src={imgixUrl(src, { w: 800, auto: 'format,compress' })}
      srcSet={generateSrcset(src)}
      sizes={sizes}
      alt={alt}
    />
  );
}
```

### With Device Pixel Ratio

```
?w=400&dpr=2     # 800px actual, for 2x displays
?w=400&dpr=3     # 1200px actual, for 3x displays
```

```javascript
function generateDprSrcset(path, width) {
  return [1, 1.5, 2, 3]
    .map((dpr) => `${imgixUrl(path, { w: width, dpr, auto: 'format,compress' })} ${dpr}x`)
    .join(', ');
}
```

## JavaScript SDK

```bash
npm install @imgix/js-core
```

```javascript
import ImgixClient from '@imgix/js-core';

const client = new ImgixClient({
  domain: 'your-source.imgix.net',
  secureURLToken: 'your-token',  // Optional, for signed URLs
});

// Build URL
const url = client.buildURL('/image.jpg', {
  w: 400,
  h: 300,
  fit: 'crop',
  auto: 'format,compress',
});

// Generate srcset
const srcset = client.buildSrcSet('/image.jpg', {
  auto: 'format,compress',
}, {
  widths: [400, 800, 1200, 1600],
});
```

## React SDK

```bash
npm install @imgix/react
```

```jsx
import Imgix from '@imgix/react';

function ProductImage({ path }) {
  return (
    <Imgix
      src={`https://your-source.imgix.net${path}`}
      sizes="(min-width: 1024px) 50vw, 100vw"
      imgixParams={{
        fit: 'crop',
        ar: '16:9',
        auto: 'format,compress',
      }}
      htmlAttributes={{
        alt: 'Product image',
        loading: 'lazy',
      }}
    />
  );
}
```

### With Background Image

```jsx
import { Background } from '@imgix/react';

function Hero({ imagePath }) {
  return (
    <Background
      src={`https://your-source.imgix.net${imagePath}`}
      imgixParams={{ auto: 'format,compress', fit: 'crop' }}
      className="hero-section"
    >
      <h1>Welcome</h1>
    </Background>
  );
}
```

## Next.js Integration

### Custom Loader

```javascript
// next.config.js
module.exports = {
  images: {
    loader: 'custom',
    loaderFile: './imgix-loader.js',
  },
};
```

```javascript
// imgix-loader.js
export default function imgixLoader({ src, width, quality }) {
  const url = new URL(`https://your-source.imgix.net${src}`);
  url.searchParams.set('w', width.toString());
  url.searchParams.set('q', (quality || 75).toString());
  url.searchParams.set('auto', 'format,compress');
  return url.toString();
}
```

```jsx
import Image from 'next/image';

function ProductImage({ src }) {
  return (
    <Image
      src={src}
      width={800}
      height={600}
      alt="Product"
    />
  );
}
```

## Common URL Patterns

### Thumbnail
```
?w=150&h=150&fit=crop&crop=faces&auto=format,compress
```

### Hero Image
```
?w=1920&h=600&fit=crop&crop=entropy&auto=format,compress&q=80
```

### Avatar
```
?w=100&h=100&fit=facearea&facepad=2&mask=ellipse&auto=format,compress
```

### Card Image
```
?w=400&h=300&fit=crop&ar=4:3&auto=format,compress
```

### Product Gallery
```
?w=800&fit=max&auto=format,compress&bg=ffffff
```

### Blurred Placeholder (LQIP)
```
?w=20&blur=200&auto=format,compress&q=30
```

## Signed URLs

For private images or to prevent URL tampering:

```javascript
import ImgixClient from '@imgix/js-core';

const client = new ImgixClient({
  domain: 'your-source.imgix.net',
  secureURLToken: process.env.IMGIX_SECURE_TOKEN,
});

// Signed URL
const signedUrl = client.buildURL('/private/image.jpg', {
  w: 400,
  auto: 'format,compress',
});
```

## Performance Tips

1. **Always use `auto=format,compress`** - Let imgix choose best format
2. **Specify width** - Don't serve larger than needed
3. **Use srcset** - Serve appropriate sizes for device
4. **Consider DPR** - Use `dpr` for high-density displays
5. **Set cache headers** - Images are CDN-cached
6. **Use LQIP** - Low-quality placeholders for perceived performance

## Pricing Note

Imgix charges based on:
- Master images (origin images accessed)
- Unique transformations cached
- Bandwidth delivered

Use consistent transformation parameters to maximize cache hits.
