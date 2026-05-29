---
name: web-architect
description: Generate brand assets and audit web code against best practices - CSS, favicons, social images, exports, React/Next.js performance
---

# Web Architect Skill

Implements the brand system by generating all required assets. Also audits web code against best practices.

## Related Skills

- **react-best-practices** - React/Next.js performance optimization. Use when building or auditing React sites.

## Capabilities

- Generate favicon package (all sizes)
- Create social assets (OG images, banners, PFP)
- Build CSS with brand tokens
- Export SVGs to PNGs
- Audit asset completeness
- Update preview files with final assets

## Input Requirements

Requires `knowledge/BRAND_DECISIONS.md` with:
- Selected mark
- Color palette
- Typography choices

## Commands

```
/web-architect                    # Show status
/web-architect audit              # Check what's missing
/web-architect implement all      # Generate everything
/web-architect implement css      # Generate CSS only
/web-architect implement favicons # Generate favicon package
/web-architect implement social   # Generate social assets
/web-architect implement marks    # Generate mark size variants
/web-architect export png         # Export all SVGs to PNG
```

## Workflow

### Audit

```
/web-architect audit

Checking brand assets...

MARKS:
├─ [✓] Primary mark selected
├─ [✓] Transparent version
├─ [ ] Size variants (80, 160, 400)
└─ [ ] Dark/light variants

FAVICONS:
├─ [ ] 16px
├─ [ ] 32px
├─ [ ] 48px
├─ [ ] 96px
├─ [ ] 180px (Apple Touch)
├─ [ ] 192px (Android)
└─ [ ] 512px (PWA)

SOCIAL:
├─ [ ] Twitter banner (1500x500)
├─ [ ] OG image (1200x630)
├─ [ ] Twitter PFP (400x400)
└─ [ ] Banner size variants

CSS:
├─ [ ] Color tokens
├─ [ ] Typography tokens
└─ [ ] global.css generated

Missing: 18 assets
Run /web-architect implement all to generate.
```

### Implement All

```
/web-architect implement all

Generating brand assets...

MARKS:
├─ [✓] mark-v3-80-dark.svg
├─ [✓] mark-v3-80-light.svg
├─ [✓] mark-v3-160-dark.svg
├─ [✓] mark-v3-400-dark.svg
└─ Saved to outputs/svg/mark/

FAVICONS:
├─ [✓] favicon-16-dark.svg
├─ [✓] favicon-32-dark.svg
├─ [✓] favicon-48-dark.svg
├─ [✓] favicon-96-dark.svg
├─ [✓] favicon-180-dark.svg
├─ [✓] favicon-192-dark.svg
├─ [✓] favicon-512-dark.svg
└─ Saved to outputs/svg/favicon/

SOCIAL:
├─ [✓] twitter-banner-sm-1500x500-dark.svg
├─ [✓] twitter-banner-md-1500x500-dark.svg
├─ [✓] twitter-banner-lg-1500x500-dark.svg
├─ [✓] twitter-banner-xl-1500x500-dark.svg
├─ [✓] og-default-1200x630-dark.svg
├─ [✓] pfp-400-dark.svg
└─ Saved to outputs/svg/social/

CSS:
├─ [✓] outputs/css/global.css
└─ Tokens from BRAND_DECISIONS.md

PNG EXPORT:
├─ [✓] All SVGs exported to PNG
└─ Saved to outputs/png/

Complete! 24 assets generated.
```

## Asset Generation

### Favicons

Generate all standard favicon sizes:

```bash
# Sizes needed
16   - Browser tab
32   - Browser tab @2x
48   - Windows
96   - Android Chrome
180  - Apple Touch Icon
192  - Android Chrome @2x
512  - PWA splash
```

SVG structure:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}">
  <rect width="100%" height="100%" fill="{bg-color}"/>
  <!-- Mark scaled to fit with padding -->
</svg>
```

### Social Assets

#### Twitter Banner (1500x500)
- Box with mark inside
- Left-aligned with padding
- Size variants: sm, md, lg, xl

#### OG Image (1200x630)
- Mark centered in box
- Optional: tagline variant

#### PFP (400x400)
- Square crop
- Mark centered
- High contrast

### CSS Generation

Read from BRAND_DECISIONS.md and generate:

```css
:root {
  /* Colors from decisions */
  --brand-bg: {bg};
  --brand-fg: {fg};
  --brand-accent: {accent};

  /* Typography from decisions */
  --brand-font: {font-stack};
  --brand-font-weight: {weight};
}
```

### PNG Export

Use rsvg-convert for all SVG → PNG conversions:

```bash
# Single file
rsvg-convert -w {width} -h {height} input.svg -o output.png

# Batch export script
./scripts/export-pngs.sh
```

## File Structure

```
outputs/
├── svg/
│   ├── mark/
│   │   ├── mark-v3-transparent.svg
│   │   ├── mark-v3-80-dark.svg
│   │   ├── mark-v3-80-light.svg
│   │   ├── mark-v3-160-dark.svg
│   │   ├── mark-v3-400-dark.svg
│   │   └── ...
│   ├── social/
│   │   ├── twitter-banner-sm-1500x500-dark.svg
│   │   ├── twitter-banner-md-1500x500-dark.svg
│   │   ├── twitter-banner-lg-1500x500-dark.svg
│   │   ├── twitter-banner-xl-1500x500-dark.svg
│   │   ├── og-default-1200x630-dark.svg
│   │   ├── pfp-400-dark.svg
│   │   └── (light variants)
│   └── favicon/
│       ├── favicon-16-dark.svg
│       ├── favicon-32-dark.svg
│       └── ...
├── png/
│   ├── mark/
│   ├── social/
│   └── favicon/
└── css/
    └── global.css
```

## Naming Conventions

```
{type}-{variant}-{size}-{theme}.{ext}

Examples:
mark-v3-80-dark.svg
twitter-banner-xl-1500x500-dark.svg
og-tagline-1200x630-dark.svg
favicon-32-dark.png
```

## Error Handling

### No Decisions Found
```
No brand decisions found.

Run /brand-architect first to:
1. Generate mark options
2. Select colors and typography
3. Record decisions

Then run /web-architect implement all.
```

### Missing Dependencies
```
rsvg-convert not found.

PNG export requires librsvg. Install with:
  brew install librsvg   # macOS
  apt install librsvg2-bin  # Ubuntu
```

### Incomplete Decisions
```
Brand decisions incomplete.

Missing:
- Primary mark selection
- Color palette

Update knowledge/BRAND_DECISIONS.md or run /brand-architect decide.
```

---

## Code Auditing

### React/Next.js Projects

For React or Next.js sites, use the **react-best-practices** skill:

```
/web-architect audit react
```

This runs the Vercel React Best Practices audit covering:
- Eliminating waterfalls (CRITICAL)
- Bundle size optimization (CRITICAL)
- Server-side performance (HIGH)
- Client-side data fetching (MEDIUM-HIGH)
- Re-render optimization (MEDIUM)
- Rendering performance (MEDIUM)
- JavaScript performance (LOW-MEDIUM)

See `skills/react-best-practices/SKILL.md` for full rule reference.

### Static Sites

For static HTML sites:
```
/web-architect audit static
```

Checks:
- Asset optimization (images, SVGs)
- CSS best practices
- Accessibility basics
- Performance hints
