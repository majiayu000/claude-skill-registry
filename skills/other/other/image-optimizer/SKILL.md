---
name: optimizing-images
description: Optimizes images and generates responsive markup. Use when the user asks about image formats (WebP, AVIF), srcset, responsive images, Next.js Image, or reducing image file sizes.
---

# Image Optimization Assistant

## When to use this skill

- User asks about image optimization
- User mentions WebP, AVIF, or modern formats
- User wants responsive images or srcset
- User asks about Next.js Image or picture element
- User wants to reduce page weight from images

## Workflow

- [ ] Audit current images
- [ ] Identify optimization opportunities
- [ ] Convert to modern formats
- [ ] Generate responsive markup
- [ ] Implement lazy loading
- [ ] Validate improvements

## Instructions

### Step 1: Audit Current Images

**Find large images:**

```bash
find public -type f \( -name "*.jpg" -o -name "*.png" -o -name "*.gif" \) -size +100k -exec ls -lh {} \;
```

**Check image dimensions:**

```bash
# Requires ImageMagick
find public -type f \( -name "*.jpg" -o -name "*.png" \) -exec identify -format "%f: %wx%h (%b)\n" {} \;
```

**Detect unoptimized in HTML:**

```bash
grep -rn --include="*.tsx" --include="*.html" '<img' src/ | grep -v 'loading='
```

### Step 2: Format Selection

| Format | Use Case                    | Browser Support |
| ------ | --------------------------- | --------------- |
| WebP   | Photos, general use         | 97%+            |
| AVIF   | Best compression, photos    | 92%+            |
| PNG    | Transparency, icons         | 100%            |
| SVG    | Icons, logos, illustrations | 100%            |
| JPEG   | Legacy fallback             | 100%            |

**Compression comparison (typical):**

| Original   | WebP          | AVIF          |
| ---------- | ------------- | ------------- |
| 500KB JPEG | ~300KB (-40%) | ~200KB (-60%) |
| 200KB PNG  | ~80KB (-60%)  | ~50KB (-75%)  |

### Step 3: Convert Images

**Using Sharp (Node.js):**

```bash
npm install sharp
```

```typescript
// scripts/optimize-images.ts
import sharp from "sharp";
import { glob } from "glob";
import path from "path";

const QUALITY = { webp: 80, avif: 65 };
const SIZES = [640, 750, 828, 1080, 1200, 1920];

async function optimizeImage(inputPath: string): Promise<void> {
  const dir = path.dirname(inputPath);
  const name = path.basename(inputPath, path.extname(inputPath));

  for (const width of SIZES) {
    const image = sharp(inputPath).resize(width);

    // WebP
    await image
      .webp({ quality: QUALITY.webp })
      .toFile(path.join(dir, `${name}-${width}.webp`));

    // AVIF
    await image
      .avif({ quality: QUALITY.avif })
      .toFile(path.join(dir, `${name}-${width}.avif`));
  }

  console.log(`Optimized: ${inputPath}`);
}

async function main() {
  const images = await glob("public/images/**/*.{jpg,jpeg,png}");
  await Promise.all(images.map(optimizeImage));
}

main();
```

**Using CLI tools:**

```bash
# WebP conversion
npx @aspect/image-optimize --format webp --quality 80 public/images/*.jpg

# Using cwebp directly
cwebp -q 80 input.jpg -o output.webp

# AVIF with avif-cli
npx avif --input public/images/*.jpg --quality 65
```

### Step 4: Responsive Image Markup

**HTML picture element:**

```html
<picture>
  <!-- AVIF for browsers that support it -->
  <source
    type="image/avif"
    srcset="
      /images/hero-640.avif   640w,
      /images/hero-1080.avif 1080w,
      /images/hero-1920.avif 1920w
    "
    sizes="(max-width: 768px) 100vw, 50vw"
  />
  <!-- WebP fallback -->
  <source
    type="image/webp"
    srcset="
      /images/hero-640.webp   640w,
      /images/hero-1080.webp 1080w,
      /images/hero-1920.webp 1920w
    "
    sizes="(max-width: 768px) 100vw, 50vw"
  />
  <!-- JPEG fallback for old browsers -->
  <img
    src="/images/hero-1080.jpg"
    alt="Hero image description"
    width="1920"
    height="1080"
    loading="lazy"
    decoding="async"
  />
</picture>
```

**Sizes attribute guide:**

| Layout                | Sizes Value                                                |
| --------------------- | ---------------------------------------------------------- |
| Full width            | `100vw`                                                    |
| Half width on desktop | `(min-width: 768px) 50vw, 100vw`                           |
| Fixed width           | `300px`                                                    |
| Grid (3 columns)      | `(min-width: 1024px) 33vw, (min-width: 768px) 50vw, 100vw` |

### Step 5: Framework Integration

**Next.js Image:**

```tsx
import Image from 'next/image';

// Basic usage - automatic optimization
<Image
  src="/images/hero.jpg"
  alt="Hero description"
  width={1920}
  height={1080}
  priority // For above-the-fold images
/>

// Fill container
<div className="relative h-64">
  <Image
    src="/images/hero.jpg"
    alt="Hero description"
    fill
    className="object-cover"
    sizes="(max-width: 768px) 100vw, 50vw"
  />
</div>

// With placeholder blur
import heroImage from '@/public/images/hero.jpg';

<Image
  src={heroImage}
  alt="Hero description"
  placeholder="blur"
  priority
/>
```

**next.config.js for external images:**

```javascript
module.exports = {
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "cdn.example.com",
      },
    ],
    formats: ["image/avif", "image/webp"],
    deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048],
    imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],
  },
};
```

**Nuxt Image:**

```vue
<template>
  <NuxtImg
    src="/images/hero.jpg"
    alt="Hero description"
    width="1920"
    height="1080"
    format="webp"
    loading="lazy"
    sizes="sm:100vw md:50vw lg:33vw"
  />

  <!-- With picture for art direction -->
  <NuxtPicture
    src="/images/hero.jpg"
    alt="Hero description"
    sizes="sm:100vw md:50vw"
    :imgAttrs="{ class: 'rounded-lg' }"
  />
</template>
```

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  modules: ["@nuxt/image"],
  image: {
    format: ["avif", "webp"],
    screens: {
      sm: 640,
      md: 768,
      lg: 1024,
      xl: 1280,
    },
  },
});
```

### Step 6: Lazy Loading

**Native lazy loading:**

```html
<img src="/image.jpg" alt="Description" loading="lazy" decoding="async" />
```

**Intersection Observer (custom):**

```typescript
// hooks/useLazyImage.ts
import { useEffect, useRef, useState } from "react";

export function useLazyImage(src: string) {
  const [isLoaded, setIsLoaded] = useState(false);
  const [isInView, setIsInView] = useState(false);
  const imgRef = useRef<HTMLImageElement>(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsInView(true);
          observer.disconnect();
        }
      },
      { rootMargin: "50px" },
    );

    if (imgRef.current) observer.observe(imgRef.current);
    return () => observer.disconnect();
  }, []);

  return { imgRef, isInView, isLoaded, setIsLoaded };
}
```

**Above-the-fold images (don't lazy load):**

```tsx
// Hero images, LCP candidates
<Image src="/hero.jpg" alt="Hero" priority />

// Or in HTML
<img src="/hero.jpg" alt="Hero" fetchpriority="high" />
```

### Step 7: Responsive Breakpoints

**Calculate optimal breakpoints:**

```typescript
// scripts/calculate-breakpoints.ts
const VIEWPORT_WIDTHS = [320, 375, 414, 768, 1024, 1280, 1440, 1920];
const DEVICE_PIXEL_RATIOS = [1, 2, 3];

function calculateBreakpoints(
  imageWidth: number,
  containerRatio: number = 1, // 1 = full width, 0.5 = half width
): number[] {
  const breakpoints = new Set<number>();

  for (const viewport of VIEWPORT_WIDTHS) {
    for (const dpr of DEVICE_PIXEL_RATIOS) {
      const width = Math.round(viewport * containerRatio * dpr);
      if (width <= imageWidth) {
        breakpoints.add(width);
      }
    }
  }

  return Array.from(breakpoints).sort((a, b) => a - b);
}

// Example: 1920px image at half viewport
console.log(calculateBreakpoints(1920, 0.5));
// [160, 188, 207, 320, 375, 384, 414, 512, 621, 640, 768, 960]
```

### Step 8: Build Pipeline Integration

**Vite plugin:**

```typescript
// vite.config.ts
import { imagetools } from "vite-imagetools";

export default {
  plugins: [
    imagetools({
      defaultDirectives: new URLSearchParams({
        format: "webp;avif;jpg",
        w: "640;1280;1920",
        quality: "80",
      }),
    }),
  ],
};
```

```tsx
// Usage with query params
import heroSrcset from "./hero.jpg?w=640;1280;1920&format=webp&as=srcset";
import heroAvif from "./hero.jpg?w=1280&format=avif";
```

**GitHub Action for optimization:**

```yaml
name: Optimize Images

on:
  pull_request:
    paths:
      - "public/images/**"

jobs:
  optimize:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Optimize images
        uses: calibreapp/image-actions@main
        with:
          githubToken: ${{ secrets.GITHUB_TOKEN }}
          jpegQuality: "80"
          webpQuality: "80"
```

## Optimization Checklist

| Check               | Target                              |
| ------------------- | ----------------------------------- |
| Format              | WebP/AVIF with JPEG fallback        |
| Dimensions          | No larger than 2x display size      |
| File size           | < 200KB for hero, < 100KB for cards |
| Lazy loading        | All images below fold               |
| Explicit dimensions | width/height on all images          |
| Alt text            | Descriptive on all images           |

## Validation

Before completing:

- [ ] Images converted to WebP/AVIF
- [ ] Responsive srcset generated
- [ ] Lazy loading on below-fold images
- [ ] Priority on LCP image
- [ ] Width/height prevent layout shift
- [ ] Total image weight reduced

```bash
# Check image sizes
npx @unlighthouse/cli --site http://localhost:3000

# Lighthouse
npx lighthouse http://localhost:3000 --only-categories=performance
```

## Error Handling

- **Sharp installation fails**: Install build tools; use prebuilt binaries.
- **AVIF encoding slow**: Use lower effort setting or limit to key images.
- **CDN not serving modern formats**: Check Accept header handling and cache config.
- **Layout shift on load**: Always include width/height or aspect-ratio.

## Resources

- [Squoosh](https://squoosh.app/) - Browser-based comparison
- [Sharp Documentation](https://sharp.pixelplumbing.com/)
- [Next.js Image Optimization](https://nextjs.org/docs/app/building-your-application/optimizing/images)
- [web.dev Image Optimization](https://web.dev/learn/images/)
