---
name: design-tokens
description: |
  Design token generation and management. Use when:
  - User asks for "design tokens", "type scale", "color palette", "spacing system"
  - Setting up a new project's design system or theme
  - User needs WCAG-compliant color combinations
  - User wants dark mode colors derived from a light palette
  - Building a Tailwind config or CSS custom properties
  - User asks for "theme setup", "design system", "color scale"
context: fork
---

# Design Tokens

Generate type scales, color palettes, spacing systems, and dark mode derivations with math — not guessing. Includes WCAG contrast checking, systematic spacing grids, and production-ready CSS/Tailwind output.

## When to Use

- User is setting up a new project's design system
- User asks for a type scale, color palette, or spacing system
- User needs WCAG-compliant color combinations
- User wants dark mode colors derived from a light palette
- User asks for "design tokens" or "theme setup"
- Building a Tailwind config or CSS custom properties

## Core Philosophy

- **Math over taste.** Scales should follow ratios, not arbitrary values.
- **Accessibility by default.** Every text/background combo must pass WCAG AA.
- **Systematic.** Every value should be derivable from a base + ratio.
- **Portable.** Output as CSS custom properties, Tailwind config, or JSON tokens.

---

## Type Scale Generation

### The Formula

```
fontSize = baseFontSize x ratio^step
```

### Recommended Ratios

| Ratio | Name | Value | Best for |
|-------|------|-------|----------|
| Minor Second | 1.067 | Tight, minimal difference | Dense UI, dashboards |
| Major Second | 1.125 | Subtle progression | Apps, data-heavy interfaces |
| Minor Third | 1.200 | Balanced, versatile | Most websites, SaaS |
| Major Third | 1.250 | Clear hierarchy | Marketing sites, blogs |
| Perfect Fourth | 1.333 | Strong contrast | Editorial, landing pages |
| Augmented Fourth | 1.414 | Dramatic | Bold designs, portfolios |
| Perfect Fifth | 1.500 | Very dramatic | Hero-heavy designs |

### Generating the Scale

Given a base size (typically 16px) and a ratio:

```
Step -2: 16 / ratio^2 = xs
Step -1: 16 / ratio   = sm
Step  0: 16           = base
Step  1: 16 x ratio   = lg
Step  2: 16 x ratio^2 = xl
Step  3: 16 x ratio^3 = 2xl
Step  4: 16 x ratio^4 = 3xl
Step  5: 16 x ratio^5 = 4xl
Step  6: 16 x ratio^6 = 5xl
```

Round to nearest 0.5px or convert to rem (/ 16).

### Line Height Rules

| Font Size | Line Height | Use |
|-----------|-------------|-----|
| <= 14px | 1.6-1.7 | Small text, captions |
| 16-20px | 1.5-1.6 | Body text |
| 20-32px | 1.3-1.4 | Subheadings |
| 32-48px | 1.1-1.2 | Headings |
| 48px+ | 1.0-1.1 | Display/hero text |

**Rule of thumb:** As font size increases, line height decreases.

### Letter Spacing Rules

| Size | Letter Spacing | Why |
|------|---------------|-----|
| Small text (<=14px) | `0.01-0.02em` | Slightly open for readability |
| Body text | `0em` (normal) | Don't touch it |
| Subheadings | `-0.01em` | Slightly tighten |
| Headings | `-0.02em` to `-0.03em` | Tighten as size grows |
| Display text | `-0.03em` to `-0.05em` | Tight tracking at large sizes |

### Font Weight Pairing

| Role | Weight | Tailwind |
|------|--------|----------|
| Body | 400 (Regular) | `font-normal` |
| Body emphasis | 500 (Medium) | `font-medium` |
| Subheading | 600 (Semibold) | `font-semibold` |
| Heading | 700 (Bold) | `font-bold` |
| Display | 800 (Extrabold) | `font-extrabold` |

### Output Example (CSS Custom Properties)

```css
:root {
  --font-size-xs: 0.694rem;    /* 11.1px */
  --font-size-sm: 0.833rem;    /* 13.3px */
  --font-size-base: 1rem;      /* 16px */
  --font-size-lg: 1.2rem;      /* 19.2px */
  --font-size-xl: 1.44rem;     /* 23px */
  --font-size-2xl: 1.728rem;   /* 27.6px */
  --font-size-3xl: 2.074rem;   /* 33.2px */
  --font-size-4xl: 2.488rem;   /* 39.8px */
  --font-size-5xl: 2.986rem;   /* 47.8px */
}
```

---

## Color Palette Generation

### Step 1: Choose Base Colors

Every palette needs:

| Token | Purpose | Example |
|-------|---------|---------|
| `primary` | Main brand color, CTAs | Blue, purple, etc. |
| `neutral` | Text, borders, backgrounds | Gray (warm/cool/pure) |
| `success` | Positive states | Green |
| `warning` | Caution states | Amber/yellow |
| `error` | Destructive states | Red |
| `info` | Informational | Blue (can overlap primary) |

### Step 2: Generate Shade Scale (50-950)

For each base color, generate a 10-step shade scale. The base color is typically the 500 step.

**Method: HSL manipulation**

Starting from the base HSL:

| Step | Lightness Adjustment | Saturation Adjustment |
|------|---------------------|----------------------|
| 50 | +45% | -30% |
| 100 | +38% | -25% |
| 200 | +28% | -15% |
| 300 | +18% | -5% |
| 400 | +8% | 0% |
| 500 | 0% (base) | 0% (base) |
| 600 | -8% | +5% |
| 700 | -18% | +5% |
| 800 | -28% | 0% |
| 900 | -38% | -10% |
| 950 | -45% | -20% |

Clamp all values: lightness 0-100%, saturation 0-100%.

### Step 3: Semantic Token Mapping

Map shade steps to semantic roles:

```css
/* Light mode */
--color-bg: var(--neutral-50);
--color-bg-subtle: var(--neutral-100);
--color-bg-muted: var(--neutral-200);
--color-border: var(--neutral-200);
--color-border-strong: var(--neutral-300);
--color-text-muted: var(--neutral-500);
--color-text-subtle: var(--neutral-600);
--color-text: var(--neutral-900);
--color-text-heading: var(--neutral-950);

--color-primary: var(--primary-600);
--color-primary-hover: var(--primary-700);
--color-primary-bg: var(--primary-50);
--color-primary-text: white;
```

---

## WCAG Contrast Checking

### The Formula

Contrast ratio = (L1 + 0.05) / (L2 + 0.05)

Where L1 = lighter relative luminance, L2 = darker.

### Relative Luminance

```
For each channel (R, G, B):
  sRGB = channel / 255
  linear = sRGB <= 0.04045 ? sRGB / 12.92 : ((sRGB + 0.055) / 1.055) ^ 2.4

L = 0.2126 x R_linear + 0.7152 x G_linear + 0.0722 x B_linear
```

### WCAG Requirements

| Level | Ratio | Applies to |
|-------|-------|-----------|
| AA Normal Text | >= 4.5:1 | Body text (< 18px or < 14px bold) |
| AA Large Text | >= 3:1 | >= 18px regular or >= 14px bold |
| AAA Normal Text | >= 7:1 | Enhanced accessibility |
| AA UI Components | >= 3:1 | Borders, icons, focus rings |

### Quick Reference (Neutral on White #FFFFFF)

| Shade | Approx Contrast | Passes |
|-------|-----------------|--------|
| 300 | ~2.5:1 | Decorative only |
| 400 | ~3.5:1 | Large text, UI |
| 500 | ~4.5:1 | AA body text |
| 600 | ~6:1 | AA comfortable |
| 700 | ~8:1 | AAA body text |

### Checking Contrast Programmatically

When generating palettes, always verify:
1. `text` (900) on `bg` (50) -> must be >= 4.5:1
2. `text-muted` (500) on `bg` (50) -> must be >= 4.5:1
3. `primary` (600) on `white` -> must be >= 4.5:1
4. `primary-text` on `primary` (600) -> must be >= 4.5:1
5. `border` (200) on `bg` (50) -> must be >= 3:1

If a combo fails, adjust the darker color one step darker until it passes.

---

## Spacing System

### Base-4 Scale (Recommended)

Everything is a multiple of 4px. Predictable, consistent, works with most font sizes.

```css
:root {
  --space-0: 0px;
  --space-0.5: 2px;
  --space-1: 4px;
  --space-1.5: 6px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 20px;
  --space-6: 24px;
  --space-8: 32px;
  --space-10: 40px;
  --space-12: 48px;
  --space-16: 64px;
  --space-20: 80px;
  --space-24: 96px;
  --space-32: 128px;
}
```

This matches Tailwind's default scale exactly.

### Spacing Usage Guide

| Context | Spacing | Values |
|---------|---------|--------|
| Inline icon gap | space-1 to space-2 | 4-8px |
| Button padding | space-2 x space-4 | 8px 16px |
| Card padding | space-4 to space-6 | 16-24px |
| Section gap (between elements) | space-6 to space-8 | 24-32px |
| Section padding (container) | space-12 to space-16 | 48-64px |
| Page section vertical rhythm | space-16 to space-24 | 64-96px |

### The Container Width Scale

| Token | Width | Use |
|-------|-------|-----|
| `sm` | 640px | Narrow content (auth forms) |
| `md` | 768px | Blog posts, documentation |
| `lg` | 1024px | App layouts |
| `xl` | 1280px | Wide layouts |
| `2xl` | 1536px | Full-width dashboards |

---

## Dark Mode Derivation

### The Inversion Pattern

Don't manually pick dark mode colors. Derive them systematically:

```
Light mode          ->  Dark mode
neutral-50  (bg)    ->  neutral-950 (bg)
neutral-100 (bg-subtle) -> neutral-900 (bg-subtle)
neutral-200 (border) -> neutral-800 (border)
neutral-300 (border-strong) -> neutral-700 (border-strong)
neutral-500 (text-muted) -> neutral-400 (text-muted)
neutral-600 (text-subtle) -> neutral-300 (text-subtle)
neutral-900 (text)  ->  neutral-50  (text)
neutral-950 (heading) -> neutral-50 (heading)
```

**The rule:** Background shades flip (50<->950, 100<->900, 200<->800). Text shades flip similarly. Middle shades (400-600) shift by ~1-2 steps.

### Primary Color in Dark Mode

- Use a lighter step: `primary-400` or `primary-500` instead of `primary-600`
- Reduce saturation slightly for dark backgrounds (avoids eye strain)
- Verify contrast against `neutral-900` or `neutral-950` background

### Semantic Tokens for Dark Mode

```css
/* Light */
:root {
  --color-bg: var(--neutral-50);
  --color-text: var(--neutral-900);
  --color-primary: var(--primary-600);
}

/* Dark */
.dark {
  --color-bg: var(--neutral-950);
  --color-text: var(--neutral-50);
  --color-primary: var(--primary-400);
}
```

The beauty: components reference semantic tokens, never raw shades. Switching themes is just swapping the token mapping.

---

## Output Formats

### CSS Custom Properties

```css
:root {
  /* Type */
  --font-size-base: 1rem;
  --font-size-lg: 1.2rem;
  /* Colors */
  --color-primary-500: hsl(220, 80%, 50%);
  /* Spacing */
  --space-4: 1rem;
}
```

### Tailwind Config

```js
module.exports = {
  theme: {
    extend: {
      fontSize: {
        'xs': '0.694rem',
        'sm': '0.833rem',
        'base': '1rem',
        'lg': '1.2rem',
        'xl': '1.44rem',
      },
      colors: {
        primary: {
          50: 'hsl(220, 50%, 95%)',
          500: 'hsl(220, 80%, 50%)',
          900: 'hsl(220, 60%, 15%)',
        },
      },
    },
  },
}
```

### JSON Design Tokens (W3C Format)

```json
{
  "color": {
    "primary": {
      "500": { "$value": "hsl(220, 80%, 50%)", "$type": "color" }
    }
  },
  "fontSize": {
    "base": { "$value": "1rem", "$type": "dimension" }
  }
}
```

---

## Step-by-Step: Full Design Token Setup

1. **Ask:** What's the project? (marketing site, SaaS app, dashboard?)
2. **Type scale:** Pick ratio based on project type -> generate scale
3. **Colors:** Get brand color -> generate shade scales for primary + neutral + semantic
4. **Verify contrast:** Check all text/bg combos against WCAG AA
5. **Spacing:** Use base-4 scale (match Tailwind)
6. **Dark mode:** Derive from light palette using inversion pattern
7. **Output:** Generate CSS custom properties and/or Tailwind config

## Examples

### Example 1: "Set up design tokens for a SaaS dashboard"

- Type: Minor Third (1.2) ratio, 16px base -- clear hierarchy without being dramatic
- Colors: Generate from brand blue, warm gray neutral
- Spacing: Base-4 (Tailwind default)
- Dark mode: Full derivation

### Example 2: "I need a color palette from this brand color: #6366F1"

- Parse HSL: ~239 deg, 84%, 67%
- Generate 50-950 scale using the shade generation method
- Map semantic tokens
- Verify WCAG contrast for all text/bg combos
- Output as CSS + Tailwind config

### Example 3: "Create a type scale for a blog"

- Ratio: Major Third (1.25) -- strong hierarchy for editorial content
- Base: 18px (slightly larger for long-form reading)
- Generate scale with line-height and letter-spacing for each step
