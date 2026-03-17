---
name: color-palette
description: |
  Generate complete, accessible color palettes from a single brand hex. Creates 11-shade scale (50-950), semantic tokens (background, foreground, card, muted), and dark mode variants. Includes WCAG contrast checking for text accessibility.

  Use when: setting up design system, creating Tailwind theme, building brand colors from single hex, converting designs to code, checking color accessibility.
license: MIT
metadata:
  keywords: [color-palette, brand-colors, shade-generation, dark-mode, tailwind-colors, semantic-tokens, wcag-contrast, accessibility]
  last_verified: 2026-01-14
---

# Color Palette Generation

**Status**: Production Ready ✅
**Last Updated**: 2026-01-14
**Standard**: Tailwind v4 @theme syntax

---

## Quick Start

Generate complete palette from brand hex:

```javascript
// Input: Brand hex
const brandColor = "#0D9488" // Teal-600

// Output: 11-shade scale + semantic tokens + dark mode
primary-50:  #F0FDFA (lightest)
primary-500: #14B8A6 (brand)
primary-950: #042F2E (darkest)

background: #FFFFFF
foreground: #0F172A
primary: #14B8A6
```

Use the reference files to generate shades, map semantics, and check contrast.

---

## Color Scale Overview

### Standard 11-Shade Scale

| Shade | Lightness | Use Case |
|-------|-----------|----------|
| 50 | 97% | Subtle backgrounds |
| 100 | 94% | Hover states |
| 200 | 87% | Borders, dividers |
| 300 | 75% | Disabled states |
| 400 | 62% | Placeholder text |
| 500 | 48% | **Brand color** |
| 600 | 40% | Primary actions |
| 700 | 33% | Hover on primary |
| 800 | 27% | Active states |
| 900 | 20% | Text on light bg |
| 950 | 10% | Darkest accents |

**Key principle**: Shade 500 represents your brand color. Other shades maintain hue/saturation while varying lightness.

---

## Hex to HSL Conversion

Convert brand hex to HSL for shade generation:

```javascript
// Example: #0D9488 → hsl(174, 84%, 29%)
// H (Hue): 174deg
// S (Saturation): 84%
// L (Lightness): 29%
```

Generate shades by keeping hue constant, adjusting lightness:
- Lighter shades (50-400): Reduce saturation slightly
- Mid shades (500-600): Full saturation
- Darker shades (700-950): Full saturation

See `references/shade-generation.md` for conversion formula.

---

## Semantic Token Mapping

Map shade scale to semantic tokens for components:

### Light Mode
```css
--background: white
--foreground: primary-950
--card: white
--card-foreground: primary-900
--muted: primary-50
--muted-foreground: primary-600
--border: primary-200
--primary: primary-600
--primary-foreground: white
```

### Dark Mode
```css
--background: primary-950
--foreground: primary-50
--card: primary-900
--card-foreground: primary-50
--muted: primary-800
--muted-foreground: primary-400
--border: primary-800
--primary: primary-500
--primary-foreground: white
```

**Pattern**: Invert lightness while preserving relationships. See `references/semantic-mapping.md`.

---

## Dark Mode Pattern

Swap light and dark shades:

| Light Mode | Dark Mode |
|------------|-----------|
| 50 (97% L) | 950 (10% L) |
| 100 (94% L) | 900 (20% L) |
| 200 (87% L) | 800 (27% L) |
| 500 (brand) | 500 (brand, slightly brighter) |

**Preserve brand identity**: Keep hue/saturation consistent, only invert lightness.

CSS pattern:
```css
:root {
  --background: white;
  --foreground: hsl(var(--primary-950));
}

.dark {
  --background: hsl(var(--primary-950));
  --foreground: hsl(var(--primary-50));
}
```

---

## Contrast Checking

WCAG minimum ratios:
- **Text (AA)**: 4.5:1 normal, 3:1 large (18px+)
- **UI Elements**: 3:1 (buttons, borders)

Quick check pairs:
- `primary-600` text on `white` background
- `white` text on `primary-600` background
- `primary-900` text on `primary-50` background

**Formula**:
```javascript
contrast = (lighter + 0.05) / (darker + 0.05)
// Where lighter/darker are relative luminance values
```

See `references/contrast-checking.md` for full formula and fix patterns.

---

## Quick Reference

### Generate Complete Palette
1. Convert brand hex to HSL
2. Generate 11 shades (50-950) by varying lightness
3. Map shades to semantic tokens
4. Create dark mode variants (invert lightness)
5. Check contrast for text pairs

### Tailwind v4 Output
Use `@theme` directive:
```css
@theme {
  --color-primary-50: #F0FDFA;
  --color-primary-500: #14B8A6;
  --color-primary-950: #042F2E;

  --color-background: #FFFFFF;
  --color-foreground: var(--color-primary-950);
}
```

### Common Adjustments
- **Too vibrant at light shades**: Reduce saturation by 10-20%
- **Poor contrast on primary**: Use shade 700+ for text
- **Dark mode too dark**: Use shade 900 instead of 950 for backgrounds
- **Brand color too light/dark**: Adjust to shade 500-600 range

---

## Resources

| File | Purpose |
|------|---------|
| `references/shade-generation.md` | Hex→HSL conversion, lightness values |
| `references/semantic-mapping.md` | Token mapping for light/dark modes |
| `references/dark-mode-palette.md` | Inversion patterns, shade swapping |
| `references/contrast-checking.md` | WCAG formulas, quick check table |
| `templates/tailwind-colors.css` | Complete CSS output template |
| `rules/color-palette.md` | Common mistakes and corrections |

---

## Token Efficiency

**Without skill**: ~8-12k tokens trial-and-error for palette generation
**With skill**: ~3-4k tokens using references
**Savings**: ~65%

**Errors prevented**:
- Poor contrast ratios (accessibility violations)
- Inconsistent shade scales
- Broken dark mode (wrong lightness values)
- Raw Tailwind colors instead of semantic tokens
- Missing foreground pairs for backgrounds

---

## Examples

### Brand Color: Teal (#0D9488)
```css
@theme {
  /* Shade scale */
  --color-primary-50: #F0FDFA;
  --color-primary-100: #CCFBF1;
  --color-primary-200: #99F6E4;
  --color-primary-300: #5EEAD4;
  --color-primary-400: #2DD4BF;
  --color-primary-500: #14B8A6;
  --color-primary-600: #0D9488;
  --color-primary-700: #0F766E;
  --color-primary-800: #115E59;
  --color-primary-900: #134E4A;
  --color-primary-950: #042F2E;

  /* Light mode semantics */
  --color-background: #FFFFFF;
  --color-foreground: var(--color-primary-950);
  --color-primary: var(--color-primary-600);
  --color-primary-foreground: #FFFFFF;
}

.dark {
  /* Dark mode overrides */
  --color-background: var(--color-primary-950);
  --color-foreground: var(--color-primary-50);
  --color-primary: var(--color-primary-500);
}
```

### Brand Color: Purple (#7C3AED)
```css
@theme {
  --color-primary-50: #FAF5FF;
  --color-primary-500: #A855F7;
  --color-primary-950: #3B0764;

  --color-background: #FFFFFF;
  --color-foreground: var(--color-primary-950);
  --color-primary: var(--color-primary-600);
}
```

---

**Next Steps**: Use `references/shade-generation.md` to convert your brand hex to HSL and generate the 11-shade scale.
