---
name: color-palette
description: >
  Generate complete, accessible colour palettes from a single brand hex.
  Produces 11-shade scale (50-950), semantic tokens, dark mode variants,
  and Tailwind v4 CSS output. Includes WCAG contrast checking.
  Use when setting up design systems, creating Tailwind themes, building brand
  colours from a hex value, or checking colour accessibility.
---

# Colour Palette Generator

Generate a complete, accessible colour system from a single brand hex. Produces Tailwind v4 CSS ready to paste into your project.

## Workflow

### Step 1: Get the Brand Hex

Ask for the primary brand colour. A single hex like `#0D9488` is enough.

### Step 2: Generate 11-Shade Scale

Convert hex to HSL, then generate shades by varying lightness while keeping hue constant:

| Shade | Lightness | Use Case |
|-------|-----------|----------|
| 50 | 97% | Subtle backgrounds |
| 100 | 94% | Hover states |
| 200 | 87% | Borders, dividers |
| 300 | 75% | Disabled states |
| 400 | 62% | Placeholder text |
| 500 | 48% | **Brand colour** |
| 600 | 40% | Primary actions |
| 700 | 33% | Hover on primary |
| 800 | 27% | Active states |
| 900 | 20% | Text on light bg |
| 950 | 10% | Darkest accents |

See `references/shade-generation.md` for the conversion formula.

### Step 3: Map Semantic Tokens

**Light mode:**
```css
--background: white;
--foreground: primary-950;
--card: white;
--card-foreground: primary-900;
--primary: primary-600;
--primary-foreground: white;
--muted: primary-50;
--muted-foreground: primary-600;
--border: primary-200;
```

**Dark mode** — invert lightness while preserving relationships:
```css
--background: primary-950;
--foreground: primary-50;
--card: primary-900;
--card-foreground: primary-50;
--primary: primary-500;
--primary-foreground: white;
--muted: primary-800;
--muted-foreground: primary-400;
--border: primary-800;
```

### Step 4: Check Contrast

WCAG minimum ratios:
- **Text (AA)**: 4.5:1 normal, 3:1 large (18px+)
- **UI Elements**: 3:1

Quick check: `primary-600` on `white` and `white` on `primary-600`. See `references/contrast-checking.md` for formula.

### Step 5: Output Tailwind v4 CSS

```css
@theme {
  --color-primary-50: #F0FDFA;
  --color-primary-100: #CCFBF1;
  --color-primary-500: #14B8A6;
  --color-primary-950: #042F2E;

  --color-background: #FFFFFF;
  --color-foreground: var(--color-primary-950);
  --color-primary: var(--color-primary-600);
  --color-primary-foreground: #FFFFFF;
}

.dark {
  --color-background: var(--color-primary-950);
  --color-foreground: var(--color-primary-50);
  --color-primary: var(--color-primary-500);
}
```

Copy `assets/tailwind-colors.css` as a starting template.

---

## Common Adjustments

- **Too vibrant at light shades**: Reduce saturation by 10-20%
- **Poor contrast on primary**: Use shade 700+ for text
- **Dark mode too dark**: Use shade 900 instead of 950 for backgrounds
- **Brand colour too light/dark**: Adjust to shade 500-600 range

## Reference Files

| File | Purpose |
|------|---------|
| `references/shade-generation.md` | Hex to HSL conversion, lightness values |
| `references/semantic-mapping.md` | Token mapping for light/dark modes |
| `references/dark-mode-palette.md` | Inversion patterns |
| `references/contrast-checking.md` | WCAG formulas, quick check table |
| `assets/tailwind-colors.css` | Complete CSS output template |
