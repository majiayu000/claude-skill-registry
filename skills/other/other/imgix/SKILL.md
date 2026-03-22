---
name: imgix
description: >-
  Optimize and transform images with imgix. Use when serving responsive images,
  implementing image CDN, adding real-time transformations, or optimizing
  Core Web Vitals with image delivery.
license: Apache-2.0
compatibility: 'Any web app, React, Next.js'
metadata:
  author: terminal-skills
  version: 1.0.0
  category: content
  tags: [imgix, images, cdn, optimization, responsive]
---

# imgix

## Overview

imgix is a real-time image processing CDN. Point it at your image storage (S3, GCS, web folder), and it serves optimized, transformed images via URL parameters. No pre-processing needed — transformations happen on request and are cached globally.

## Instructions

### Step 1: URL API

```typescript
// lib/imgix.ts — Image URL builder
import ImgixClient from '@imgix/js-core'

const client = new ImgixClient({
  domain: 'myapp.imgix.net',
  secureURLToken: process.env.IMGIX_TOKEN,    // sign URLs to prevent abuse
})

// Responsive image with auto format/quality
const url = client.buildURL('photos/hero.jpg', {
  w: 1200,
  h: 630,
  fit: 'crop',
  auto: 'format,compress',    // WebP/AVIF + quality optimization
  crop: 'faces',               // crop around detected faces
})

// Generate srcset for responsive images
const srcset = client.buildSrcSet('photos/hero.jpg', {
  auto: 'format,compress',
  fit: 'crop',
  ar: '16:9',
})
```

### Step 2: React Component

```tsx
import Imgix from 'react-imgix'

function ProductImage({ path, alt }: { path: string; alt: string }) {
  return (
    <Imgix
      src={`https://myapp.imgix.net/${path}`}
      sizes="(max-width: 768px) 100vw, 50vw"
      imgixParams={{
        auto: 'format,compress',
        fit: 'crop',
        ar: '1:1',
      }}
      htmlAttributes={{ alt, loading: 'lazy' }}
    />
  )
}
```

### Step 3: Video Thumbnails

```typescript
// Extract video thumbnails via URL
const thumbnail = client.buildURL('videos/demo.mp4', {
  fm: 'jpg',
  frame: 1,          // extract frame at 1 second
  w: 640,
  h: 360,
  fit: 'crop',
})
```

## Guidelines

- `auto=format,compress` delivers WebP/AVIF with optimal quality — always include it.
- Sign URLs with secureURLToken in production — prevents parameter tampering.
- imgix doesn't store images — it proxies from your origin (S3, GCS, HTTP).
- Use `buildSrcSet()` for responsive images — generates proper `srcset` with widths.
- Pricing: based on origin images accessed per month, not transformations.
