---
name: creating-share-images
description: >-
  Create OpenGraph and Twitter share images for Next.js applications using
  next/og ImageResponse. Generates dynamic social preview cards with gradients,
  SVG icons, and proper dimensions. Use when building OG images, Twitter cards,
  social previews, meta images, or share images for webapps.
---

# Creating Share Images for Next.js

Generate dynamic OpenGraph (1200x630) and Twitter (1200x600) images using `next/og` ImageResponse.

## Quick Start

Create `app/opengraph-image.tsx`:

```tsx
import { ImageResponse } from "next/og";

export const runtime = "edge";
export const alt = "Page Title - Site Description";
export const size = { width: 1200, height: 630 };
export const contentType = "image/png";

export default async function Image() {
  return new ImageResponse(
    (
      <div style={{
        height: "100%",
        width: "100%",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        background: "linear-gradient(145deg, #0a0a12 0%, #0f1218 50%, #0a0a12 100%)",
        fontFamily: "system-ui, -apple-system, sans-serif",
      }}>
        <h1 style={{ fontSize: 64, color: "#ffffff", margin: 0 }}>
          Page Title
        </h1>
      </div>
    ),
    { ...size }
  );
}
```

## File Naming Convention

| File | Purpose | Dimensions |
|------|---------|------------|
| `opengraph-image.tsx` | Facebook, LinkedIn, iMessage | 1200×630 |
| `twitter-image.tsx` | Twitter/X cards | 1200×600 |

Place in route directory (e.g., `app/about/opengraph-image.tsx` for `/about`).

## Design Patterns

### Gradient Backgrounds

```tsx
background: "linear-gradient(145deg, #0a0a12 0%, #0f1218 35%, #121620 65%, #0a0a12 100%)"
```

### Glowing Orbs (Depth Effect)

```tsx
<div style={{
  position: "absolute",
  top: -150,
  left: -100,
  width: 500,
  height: 500,
  borderRadius: "50%",
  background: "radial-gradient(circle, rgba(34,211,238,0.15) 0%, transparent 60%)",
  display: "flex",
}} />
```

### Gradient Text

```tsx
<h1 style={{
  fontSize: 62,
  fontWeight: 800,
  background: "linear-gradient(135deg, #ffffff 0%, #e2e8f0 50%, #94a3b8 100%)",
  backgroundClip: "text",
  color: "transparent",
  display: "flex",
}}>Title</h1>
```

### SVG Icons with Gradients

```tsx
<svg width="200" height="200" viewBox="0 0 100 100" fill="none"
  style={{ filter: "drop-shadow(0 0 24px rgba(34,211,238,0.35))" }}>
  <defs>
    <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stopColor="#22d3ee" />
      <stop offset="100%" stopColor="#a855f7" />
    </linearGradient>
  </defs>
  <circle cx="50" cy="50" r="45" stroke="url(#grad)" strokeWidth="2" fill="none" />
</svg>
```

## Critical Rules

1. **Always use `display: "flex"`** on every element (Satori requirement)
2. **No `gap` on containers without `display: "flex"`**
3. **Use inline styles only** - no CSS classes or external stylesheets
4. **All text must be wrapped in elements** with explicit styling
5. **SVG must use `viewBox`** and explicit dimensions
6. **Filter property only on SVG root** - not on child elements

## Color Palette by Section Type

| Section | Primary | Secondary | Accent |
|---------|---------|-----------|--------|
| Homepage | `#3b82f6` blue | `#8b5cf6` purple | `#06b6d4` cyan |
| About | `#10b981` emerald | `#14b8a6` teal | `#22c55e` green |
| Projects | `#f97316` orange | `#f59e0b` amber | `#f43f5e` rose |
| Writing | `#ec4899` pink | `#f472b6` rose | `#6366f1` indigo |
| Tools/TLDR | `#22d3ee` cyan | `#a855f7` purple | `#f472b6` pink |

## Badge/Tag Pattern

```tsx
<div style={{
  display: "flex",
  padding: "7px 14px",
  borderRadius: 8,
  background: "rgba(34,211,238,0.15)",
  border: "1px solid rgba(34,211,238,0.3)",
}}>
  <span style={{ color: "#22d3ee", fontWeight: 600, display: "flex" }}>
    Label
  </span>
</div>
```

## Bottom Gradient Accent

```tsx
<div style={{
  position: "absolute",
  bottom: 0,
  left: 0,
  right: 0,
  height: 4,
  background: "linear-gradient(90deg, transparent 0%, #22d3ee 25%, #a855f7 50%, #f472b6 75%, transparent 100%)",
  display: "flex",
}} />
```

## Testing

After creating images, run `bun run build` (or `npm run build`) to verify routes register as dynamic:

```
Route (app)                    Size     First Load JS
├ ƒ /opengraph-image          0 B      0 B
├ ƒ /twitter-image            0 B      0 B
```

The `ƒ` indicates dynamic (edge) functions.

## Common Issues

| Issue | Solution |
|-------|----------|
| Text not rendering | Add `display: "flex"` to text wrapper |
| Layout broken | Ensure all containers have `display: "flex"` |
| Colors wrong | Use hex colors, not CSS variables |
| SVG not showing | Add explicit width/height attributes |
| Gradient text invisible | Need both `backgroundClip: "text"` AND `color: "transparent"` |

## Extended Patterns

See [patterns.md](references/patterns.md) for complete examples including:
- Flywheel diagrams
- Document/writing visuals
- Code window icons
- Network/connection graphics
- Journey path visualizations
