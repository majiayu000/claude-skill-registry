---
name: solidstart-static-assets
description: "SolidStart static assets: public directory for stable URLs, imports for hashed assets, images, fonts, documents, optimization."
metadata:
  globs:
    - "public/**"
    - "**/*.png"
    - "**/*.jpg"
    - "**/*.svg"
---

# SolidStart Static Assets

Complete guide to managing static assets in SolidStart. Choose between public directory and imports based on your needs.

## Public Directory

Store assets in `/public` for stable, human-readable URLs.

### Structure

```
public/
├── favicon.ico              → /favicon.ico
├── images/
│   ├── logo.png            → /images/logo.png
│   └── background.png      → /images/background.png
├── models/
│   └── player.gltf        → /models/player.gltf
└── documents/
    └── report.pdf          → /documents/report.pdf
```

### Usage

```tsx
function Component() {
  return (
    <>
      <img src="/images/logo.png" alt="Logo" />
      <link rel="icon" href="/favicon.ico" />
      <a href="/documents/report.pdf">Download Report</a>
    </>
  );
}
```

**Benefits:**
- Stable URLs (don't change)
- Human-readable paths
- Easy to reference
- Good for documents, manifests

**Use for:**
- Favicons
- robots.txt, sitemap.xml
- Service workers
- Documents (PDFs, etc.)
- Stable image references

## Importing Assets

Import assets directly for hashed filenames and optimization.

### Basic Import

```tsx
import logo from "./logo.png";

function Component() {
  return <img src={logo} alt="Logo" />;
  // Renders: <img src="/assets/logo.2d8efhg.png" />
}
```

### Multiple Formats

```tsx
import logoPng from "./logo.png";
import logoSvg from "./logo.svg";
import background from "./background.jpg";

function Component() {
  return (
    <>
      <img src={logoPng} alt="PNG Logo" />
      <img src={logoSvg} alt="SVG Logo" />
      <div style={{ backgroundImage: `url(${background})` }} />
    </>
  );
}
```

**Benefits:**
- Hashed filenames (cache busting)
- Automatic optimization
- Tree-shaking unused assets
- Type safety

**Use for:**
- Component-specific images
- Optimized assets
- Cache-busting needed
- Build-time optimization

## Comparison

| Feature | Public Directory | Imports |
|---------|-----------------|---------|
| URL Stability | ✅ Stable | ❌ Hashed |
| Cache Busting | ❌ Manual | ✅ Automatic |
| Optimization | ❌ Manual | ✅ Automatic |
| Type Safety | ❌ No | ✅ Yes |
| Tree Shaking | ❌ No | ✅ Yes |

## Common Patterns

### Images

```tsx
// Public directory
<img src="/images/hero.jpg" alt="Hero" />

// Import
import hero from "./images/hero.jpg";
<img src={hero} alt="Hero" />
```

### Fonts

```tsx
// Public directory
<link rel="stylesheet" href="/fonts/font.css" />

// Import
import font from "./fonts/font.woff2";
```

### Documents

```tsx
// Public directory (preferred for documents)
<a href="/documents/manual.pdf" download>
  Download Manual
</a>
```

### Favicon

```tsx
// Public directory (required)
<link rel="icon" href="/favicon.ico" />
```

### Service Workers

```tsx
// Public directory (required)
if ("serviceWorker" in navigator) {
  navigator.serviceWorker.register("/sw.js");
}
```

## Best Practices

1. **Public directory for:**
   - Stable URLs needed
   - Documents and manifests
   - Service workers
   - Favicons

2. **Imports for:**
   - Component assets
   - Cache busting needed
   - Optimization desired
   - Type safety

3. **Optimize images:**
   - Use appropriate formats
   - Compress before adding
   - Consider WebP for modern browsers

4. **Organize assets:**
   - Group by type (images, fonts, etc.)
   - Use consistent naming
   - Keep public directory clean

## Summary

- **Public directory**: Stable URLs, human-readable
- **Imports**: Hashed filenames, optimized
- **Choose based on**: URL stability vs cache busting
- **Documents**: Prefer public directory
- **Component assets**: Prefer imports

