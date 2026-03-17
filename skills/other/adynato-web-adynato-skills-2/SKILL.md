---
name: adynato-web
description: Web development conventions for Adynato projects. Covers image optimization with img4web, asset management, component patterns, styling, and performance best practices. Use when building or modifying web applications, adding images/assets, or creating UI components.
---

# Web Development Skill

Use this skill for all Adynato web projects and frontend development.

## Image & Asset Management

### Always Use img4web

When adding images or visual assets to any Adynato project, use [adynato/img4web](https://github.com/adynato/img4web).

```bash
# Install globally
npm install -g @adynato/img4web

# Or use npx
npx @adynato/img4web <input> [options]
```

### When to Use img4web

- Adding any new image to a project
- Processing user-uploaded images
- Optimizing existing unoptimized images
- Converting images to modern formats (WebP, AVIF)
- Generating responsive image sets

### img4web Usage

```bash
# Basic optimization
npx @adynato/img4web ./src/images

# With specific output formats
npx @adynato/img4web ./image.png --formats webp,avif

# Generate responsive sizes
npx @adynato/img4web ./hero.jpg --sizes 640,1024,1920

# Watch mode during development
npx @adynato/img4web ./src/images --watch
```

### Image Requirements

| Use Case | Max Width | Formats | Quality |
|----------|-----------|---------|---------|
| Hero/Banner | 1920px | WebP, AVIF, fallback JPG | 80-85 |
| Content Images | 1200px | WebP, AVIF | 80 |
| Thumbnails | 400px | WebP | 75 |
| Icons/Logos | Original | SVG preferred, else PNG | Lossless |
| OG Images | 1200x630 | PNG or JPG | 90 |

### Image Component Pattern

Always use responsive images with modern format fallbacks:

```tsx
// Next.js
import Image from 'next/image'

<Image
  src="/images/hero.webp"
  alt="Descriptive alt text"
  width={1920}
  height={1080}
  priority // for above-fold images
  placeholder="blur"
  blurDataURL={blurDataUrl}
/>
```

```html
<!-- Plain HTML with picture element -->
<picture>
  <source srcset="/images/hero.avif" type="image/avif">
  <source srcset="/images/hero.webp" type="image/webp">
  <img src="/images/hero.jpg" alt="Descriptive alt text" loading="lazy">
</picture>
```

## Asset Organization

```
public/
├── images/
│   ├── blog/
│   │   └── [post-slug]/
│   │       ├── cover.webp
│   │       ├── cover.avif
│   │       └── *.webp
│   ├── og/
│   │   └── [page-slug].png
│   ├── icons/
│   │   └── *.svg
│   └── hero/
│       └── *.webp
├── fonts/
│   └── *.woff2
└── videos/
    └── *.mp4
```

## Component Patterns

### File Naming

- Components: `PascalCase.tsx` (e.g., `Button.tsx`, `NavBar.tsx`)
- Utilities: `camelCase.ts` (e.g., `formatDate.ts`)
- Hooks: `useCamelCase.ts` (e.g., `useAuth.ts`)
- Types: `types.ts` or `[feature].types.ts`

### Component Structure

```tsx
// components/Button.tsx
import { type ReactNode } from 'react'

interface ButtonProps {
  children: ReactNode
  variant?: 'primary' | 'secondary'
  onClick?: () => void
}

export function Button({ children, variant = 'primary', onClick }: ButtonProps) {
  return (
    <button
      className={`btn btn-${variant}`}
      onClick={onClick}
    >
      {children}
    </button>
  )
}
```

### Export Pattern

Prefer named exports over default exports:

```tsx
// Good
export function Button() { ... }
export function Input() { ... }

// Avoid
export default function Button() { ... }
```

## Performance Checklist

Before deploying any web project:

- [ ] All images processed through img4web
- [ ] Images use WebP/AVIF with fallbacks
- [ ] Above-fold images have `priority` or `fetchpriority="high"`
- [ ] Below-fold images have `loading="lazy"`
- [ ] Fonts are self-hosted as WOFF2
- [ ] Critical CSS is inlined
- [ ] JavaScript is code-split appropriately
- [ ] No layout shift (CLS) issues

## Styling

### Preferred Stack

1. **Tailwind CSS** - utility-first styling
2. **CSS Modules** - when component-scoped styles needed
3. **CSS Variables** - for theming and dynamic values

### Tailwind Conventions

```tsx
// Use consistent ordering: layout, spacing, sizing, typography, colors, effects
<div className="flex items-center gap-4 p-4 w-full text-sm text-gray-700 bg-white rounded-lg shadow-md">
```

### Dark Mode

Always support dark mode:

```tsx
<div className="bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100">
```
