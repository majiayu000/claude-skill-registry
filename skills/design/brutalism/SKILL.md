---
name: design-system-builder
description: Framework-agnostic brutalist web design system with Space Grotesk typography, purple/cyan/pink palette, bold offset shadows, and sharp borders. Use when building any web interface (HTML, React, Vue, Svelte, Astro, etc.) that needs neo-brutalist aesthetics with consistent design tokens, typography scale, and component patterns.
---

# Design System Builder

Build web interfaces following a cohesive design system with neo-brutalist aesthetics, bold typography, and vibrant colors.

## Quick Start

1. Read `references/design-tokens.md` for CSS variables and Tailwind config
2. Apply the design system principles below
3. Use provided component patterns as starting points

## Core Design Principles

### Visual Identity
- **Style**: Neo-brutalist with bold shadows, sharp borders, no border-radius by default
- **Typography**: Space Grotesk (300-900 weights) as primary font
- **Colors**: Purple primary (#7b61ff), Cyan secondary (#2a9d9e), Pink accent (#e5729a)
- **Shadows**: Bold offset shadows (`4px 4px 0px rgba(58,60,66,0.92)`)
- **Borders**: 2px solid dark gray (#3a3c42)

### Typography Scale

```css
/* Headings - Space Grotesk */
H1: 60px/1.1, weight 900, letter-spacing -0.02em
H2: 48px/1.0, weight 700, letter-spacing -0.02em
H3: 30px/1.2, weight 700
H4: 24px/1.3, weight 700
H5: 20px/1.4, weight 700

/* Body */
Large: 18px/1.6, weight 400
Base: 16px/1.6, weight 400
Small: 14px/1.5, weight 400

/* Labels */
Label: 12px, weight 700, uppercase, letter-spacing 0.15em
```

### Spacing Scale (8px base)
```
4px | 8px | 12px | 16px | 24px | 32px | 40px | 48px | 64px | 80px
```

### Color Palette

| Role | Color | Hex |
|------|-------|-----|
| Primary | Purple | #7b61ff |
| Primary Dark | Deep Purple | #5b40c9 |
| Secondary | Cyan | #2a9d9e |
| Accent | Pink | #e5729a |
| Success | Green | #34c759 |
| Warning | Amber | #fbbf24 |
| Danger | Orange-Red | #ff8555 |
| Text | Charcoal | #22242a |
| Border | Dark Gray | #3a3c42 |
| Background | Off-White | #e8e8e8 |

## Component Patterns

### Buttons
```css
.btn {
  padding: 12px 16px;
  font: 700 1rem/1 'Space Grotesk';
  text-transform: uppercase;
  letter-spacing: 0.075em;
  border: 2px solid;
  border-radius: 0;
  cursor: pointer;
  transition: all 250ms ease;
}

.btn-primary {
  background: #7b61ff;
  color: white;
  border-color: #7b61ff;
}

.btn-primary:hover {
  background: #6b50d9;
  box-shadow: 4px 4px 0 rgba(58,60,66,0.92);
}

.btn-primary:active {
  transform: translate(2px, 2px);
  box-shadow: none;
}
```

### Cards
```css
.card {
  background: white;
  border: 2px solid #3a3c42;
  padding: 24px;
  transition: all 250ms ease;
}

.card:hover {
  box-shadow: 4px 4px 0 rgba(58,60,66,0.92);
  border-color: #7b61ff;
}
```

### Navigation
- Sticky top, white background
- 2px bottom border
- Brand: 24px, weight 900, primary color
- Links: uppercase, 700 weight, underline on hover

## Implementation Checklist

1. **Import Space Grotesk font**
   ```html
   <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700;900&display=swap" rel="stylesheet">
   ```

2. **Set CSS variables** - See `references/design-tokens.md`

3. **Apply base styles**
   ```css
   body {
     font-family: 'Space Grotesk', system-ui, sans-serif;
     color: #22242a;
     background: #f0f0f0;
   }
   ```

4. **Use design tokens** for all colors, spacing, typography

5. **Add hover states** with bold shadows and color shifts

6. **Ensure contrast** - Primary purple on white fails AA for body text; use darker variants

## References

- `references/design-tokens.md` - Complete CSS variables, Tailwind config, and color definitions
- `assets/globals.css` - Ready-to-use CSS file with all tokens and base styles
