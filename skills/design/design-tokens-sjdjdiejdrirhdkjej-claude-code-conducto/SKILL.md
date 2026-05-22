# Design Tokens - Comprehensive Reference

**Version**: 2.0.0
**Purpose**: Generate and maintain design system tokens across all project surfaces (UI, emails, PDFs, CLI, charts, docs)

---

## Overview

This skill provides comprehensive guidance for initializing and maintaining design tokens in `design/systems/tokens.json` and `tokens.css`. Supports both brownfield (scan existing code) and greenfield (generate new palette) modes.

**Coverage**:
- UI components (React/Vue/Svelte)
- MJML/HTML emails
- PDF styling (WeasyPrint, Puppeteer)
- CLI colors (chalk/colorette)
- Data visualization (d3, Chart.js, Recharts)
- Documentation assets (MD/MDX)

---

## What Changed in v2

**Non-UI surface coverage**:
- MJML/HTML emails (inline CSS)
- PDF styling (WeasyPrint, Puppeteer CSS)
- CLI colors (chalk/colorette)
- Data visualization palettes (d3, Chart.js, Recharts)
- Documentation assets (MD/MDX)

**Brownfield scan improvements**:
- Source-agnostic: JSX/TSX, CSS/SCSS, CSS-in-JS, MD/MDX, MJML, Python/JS PDF styles
- Scans 10+ file types
- Detects arbitrary Tailwind values (`bg-[#xxx]`)

**Contrast enforcement**:
- Auto-nudges OKLCH lightness until WCAG 2.1 passes (≥4.5:1)
- Uses colorjs.io for perceptually accurate contrast calculation

**Tailwind v4 alignment**:
- Theme variables as CSS variables (not hardcoded palette)
- Validates tokens.css import in globals.css

**Color-blind-safe palettes**:
- Okabe-Ito categorical palette for charts
- 8 colors scientifically validated for color-blind users

---

## Mental Model

**Flow**: `detect mode → scan/generate → consolidate → validate wiring → contrast fixups → emit artifacts → report debt`

**Brownfield**: Scan existing code for patterns across UI, emails, PDFs, CLI, charts, docs. Consolidate duplicates and propose migrations.

**Greenfield**: Ask minimal questions, generate OKLCH palette with contrast validation.

---

## Prerequisites

**Dependencies**:
```json
{
  "devDependencies": {
    "colorjs.io": "^0.5.0",
    "picocolors": "^1.0.0",
    "fs-extra": "^11.2.0"
  }
}
```

**Install**:
```bash
pnpm add -D colorjs.io picocolors fs-extra
```

---

## Brownfield Scan (Multi-Surface)

**Scanned locations**:

| Surface | Paths | File Types | Patterns Detected |
|---------|-------|------------|-------------------|
| **UI** | `app/**`, `src/**`, `components/**` | `.tsx`, `.jsx`, `.css`, `.scss` | Hex colors, Tailwind classes, CSS-in-JS |
| **Emails** | `emails/**`, `templates/email/**` | `.mjml`, `.html` | Inline CSS, hex colors |
| **PDFs** | `server/pdf/**`, `reports/**` | `.css`, `.py` (WeasyPrint) | PDF-specific CSS, hex in templates |
| **CLI** | `scripts/**`, `bin/**` | `.js`, `.mjs`, `.ts` | chalk/colorette color names |
| **Charts** | `components/**`, `lib/**` | `.tsx`, `.js` | d3/Chart.js/Recharts palettes |
| **Docs** | `docs/**`, `*.md`, `*.mdx` | `.md`, `.mdx` | Fenced CSS blocks |

**Scan output**:
```
design/systems/
├── detected-tokens.json       # All detected colors with usage counts
├── token-analysis-report.md   # Consolidation opportunities
├── violations-colors.txt      # Hex colors found (file:line:color)
└── violations-arbitrary.txt   # Tailwind arbitrary values (file:line:value)
```

**Example violations-colors.txt**:
```
#3b82f6    47  (most used - primary candidate)
#3b81f6     3  (duplicate - consolidate)
#10b981    28  (success candidate)
#ef4444    15  (error candidate)
```

---

## Token Consolidation

**Consolidation rules**:
- Colors → 12 semantic + 7 neutral shades
- Type scale → 8 sizes (xs, sm, base, lg, xl, 2xl, 3xl, 4xl)
- Spacing → 8px grid (~13 values: 0, 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96px)

**Semantic mapping**:
```javascript
{
  brand: { primary, secondary, accent },
  semantic: { success, error, warning, info },
  neutral: { 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950 }
}
```

**Minimal user questions** (greenfield only):

1. **Primary brand color**: Blue (#3b82f6), Purple (#8b5cf6), Green (#10b981), Custom
2. **Visual style**: Minimal (Stripe, Linear), Bold (Figma, Notion), Technical (Vercel, GitHub)
3. **Primary font**: Inter (geometric sans), Geist (humanist sans), System fonts

**Consolidation output**:
```
Before: 47 colors → After: 12 tokens (74% reduction)
Before: 14 font sizes → After: 8 sizes (43% reduction)
Before: 23 spacing values → After: 13 values (43% reduction)

Duplicates removed:
  - #3b82f7, #3b81f6 → primary (#3b82f6)
  - 15px, 17px → base (16px), lg (18px)
```

---

## Token Structure

**Complete token structure** (`design/systems/tokens.json`):

```json
{
  "meta": {
    "colorSpace": "oklch",
    "fallbackSpace": "srgb",
    "version": "2.0.0",
    "generated": "2025-11-12T10:30:00Z"
  },
  "colors": {
    "brand": {
      "primary": {
        "oklch": "oklch(59.69% 0.156 261.45)",
        "fallback": "#3b82f6",
        "description": "Primary brand color"
      },
      "secondary": {
        "oklch": "oklch(58.23% 0.167 271.45)",
        "fallback": "#6366f1"
      },
      "accent": {
        "oklch": "oklch(67.89% 0.152 164.57)",
        "fallback": "#10b981"
      }
    },
    "semantic": {
      "success": {
        "bg": {"oklch": "oklch(95% 0.02 145)", "fallback": "#D1FAE5"},
        "fg": {"oklch": "oklch(25% 0.12 145)", "fallback": "#047857"},
        "border": {"oklch": "oklch(85% 0.05 145)", "fallback": "#A7F3D0"},
        "icon": {"oklch": "oklch(35% 0.13 145)", "fallback": "#059669"}
      },
      "error": {
        "bg": {"oklch": "oklch(95% 0.02 27)", "fallback": "#FEE2E2"},
        "fg": {"oklch": "oklch(30% 0.18 27)", "fallback": "#991B1B"},
        "border": {"oklch": "oklch(85% 0.08 27)", "fallback": "#FECACA"},
        "icon": {"oklch": "oklch(40% 0.20 27)", "fallback": "#DC2626"}
      },
      "warning": {
        "bg": {"oklch": "oklch(95% 0.02 90)", "fallback": "#FEF3C7"},
        "fg": {"oklch": "oklch(35% 0.15 90)", "fallback": "#92400E"},
        "border": {"oklch": "oklch(85% 0.08 90)", "fallback": "#FDE68A"},
        "icon": {"oklch": "oklch(45% 0.16 90)", "fallback": "#D97706"}
      },
      "info": {
        "bg": {"oklch": "oklch(95% 0.02 240)", "fallback": "#DBEAFE"},
        "fg": {"oklch": "oklch(30% 0.12 240)", "fallback": "#1E40AF"},
        "border": {"oklch": "oklch(85% 0.05 240)", "fallback": "#BFDBFE"},
        "icon": {"oklch": "oklch(40% 0.14 240)", "fallback": "#3B82F6"}
      }
    },
    "neutral": {
      "50": {"oklch": "oklch(98% 0 0)", "fallback": "#fafafa"},
      "100": {"oklch": "oklch(96% 0 0)", "fallback": "#f5f5f5"},
      "200": {"oklch": "oklch(90% 0 0)", "fallback": "#e5e5e5"},
      "300": {"oklch": "oklch(82% 0 0)", "fallback": "#d4d4d4"},
      "400": {"oklch": "oklch(64% 0 0)", "fallback": "#a3a3a3"},
      "500": {"oklch": "oklch(54% 0 0)", "fallback": "#737373"},
      "600": {"oklch": "oklch(42% 0 0)", "fallback": "#525252"},
      "700": {"oklch": "oklch(32% 0 0)", "fallback": "#404040"},
      "800": {"oklch": "oklch(23% 0 0)", "fallback": "#262626"},
      "900": {"oklch": "oklch(15% 0 0)", "fallback": "#171717"},
      "950": {"oklch": "oklch(11% 0 0)", "fallback": "#0a0a0a"}
    }
  },
  "typography": {
    "families": {
      "sans": "Inter, system-ui, -apple-system, BlinkMacSystemFont, sans-serif",
      "mono": "Fira Code, Menlo, Monaco, Consolas, monospace",
      "serif": "Georgia, Cambria, 'Times New Roman', Times, serif"
    },
    "sizes": {
      "xs": "0.75rem",
      "sm": "0.875rem",
      "base": "1rem",
      "lg": "1.125rem",
      "xl": "1.25rem",
      "2xl": "1.5rem",
      "3xl": "1.875rem",
      "4xl": "2.25rem"
    },
    "weights": {
      "normal": "400",
      "medium": "500",
      "semibold": "600",
      "bold": "700"
    },
    "lineHeights": {
      "tight": "1.25",
      "normal": "1.5",
      "relaxed": "1.75"
    },
    "letterSpacing": {
      "display": "-0.025em",
      "body": "0em",
      "cta": "0.025em"
    }
  },
  "spacing": {
    "0": "0px",
    "1": "4px",
    "2": "8px",
    "3": "12px",
    "4": "16px",
    "5": "20px",
    "6": "24px",
    "8": "32px",
    "10": "40px",
    "12": "48px",
    "16": "64px",
    "20": "80px",
    "24": "96px"
  },
  "shadows": {
    "light": {
      "sm": {"value": "0 1px 2px oklch(0% 0 0 / 0.05)", "fallback": "0 1px 2px rgba(0, 0, 0, 0.05)"},
      "md": {"value": "0 4px 6px oklch(0% 0 0 / 0.07), 0 2px 4px oklch(0% 0 0 / 0.06)", "fallback": "0 4px 6px rgba(0, 0, 0, 0.07), 0 2px 4px rgba(0, 0, 0, 0.06)"},
      "lg": {"value": "0 10px 15px oklch(0% 0 0 / 0.10), 0 4px 6px oklch(0% 0 0 / 0.05)", "fallback": "0 10px 15px rgba(0, 0, 0, 0.10), 0 4px 6px rgba(0, 0, 0, 0.05)"}
    },
    "dark": {
      "sm": {"value": "0 1px 2px oklch(0% 0 0 / 0.30)", "fallback": "0 1px 2px rgba(0, 0, 0, 0.30)"},
      "md": {"value": "0 4px 6px oklch(0% 0 0 / 0.35), 0 2px 4px oklch(0% 0 0 / 0.30)", "fallback": "0 4px 6px rgba(0, 0, 0, 0.35), 0 2px 4px rgba(0, 0, 0, 0.30)"},
      "lg": {"value": "0 10px 15px oklch(0% 0 0 / 0.40), 0 4px 6px oklch(0% 0 0 / 0.35)", "fallback": "0 10px 15px rgba(0, 0, 0, 0.40), 0 4px 6px rgba(0, 0, 0, 0.35)"}
    }
  },
  "motion": {
    "duration": {
      "fast": "150ms",
      "base": "200ms",
      "slow": "300ms",
      "slower": "500ms"
    },
    "easing": {
      "standard": "cubic-bezier(0.4, 0.0, 0.2, 1)",
      "decelerate": "cubic-bezier(0.0, 0.0, 0.2, 1)",
      "accelerate": "cubic-bezier(0.4, 0.0, 1.0, 1.0)"
    }
  },
  "dataViz": {
    "categorical": {
      "okabe-ito": {
        "orange": {"oklch": "oklch(68.29% 0.151 58.43)", "fallback": "#E69F00", "description": "Orange - warm accent"},
        "skyBlue": {"oklch": "oklch(70.17% 0.099 232.66)", "fallback": "#56B4E9", "description": "Sky blue - cool primary"},
        "bluishGreen": {"oklch": "oklch(59.78% 0.108 164.04)", "fallback": "#009E73", "description": "Bluish green - success"},
        "yellow": {"oklch": "oklch(89.87% 0.162 99.57)", "fallback": "#F0E442", "description": "Yellow - warning"},
        "blue": {"oklch": "oklch(46.86% 0.131 264.05)", "fallback": "#0072B2", "description": "Blue - information"},
        "vermillion": {"oklch": "oklch(57.50% 0.199 37.70)", "fallback": "#D55E00", "description": "Vermillion - error"},
        "reddishPurple": {"oklch": "oklch(50.27% 0.159 328.36)", "fallback": "#CC79A7", "description": "Reddish purple - accent"},
        "black": {"oklch": "oklch(0% 0 0)", "fallback": "#000000", "description": "Black - text"}
      }
    },
    "sequential": {
      "blue": ["oklch(95% 0.02 240)", "oklch(75% 0.08 240)", "oklch(55% 0.12 240)", "oklch(35% 0.14 240)", "oklch(25% 0.16 240)"],
      "green": ["oklch(95% 0.02 145)", "oklch(75% 0.08 145)", "oklch(55% 0.12 145)", "oklch(35% 0.14 145)", "oklch(25% 0.16 145)"]
    },
    "diverging": {
      "red-blue": ["oklch(95% 0.02 27)", "oklch(75% 0.08 27)", "oklch(90% 0 0)", "oklch(75% 0.08 240)", "oklch(95% 0.02 240)"]
    }
  }
}
```

---

## WCAG Contrast Validation + Auto-Fix

**Validation pairs**:
- `semantic.success.fg` on `semantic.success.bg`
- `semantic.error.fg` on `semantic.error.bg`
- `semantic.warning.fg` on `semantic.warning.bg`
- `semantic.info.fg` on `semantic.info.bg`
- `brand.primary` on `neutral.50` (light background)
- `brand.primary` on `neutral.950` (dark background)

**Auto-fix algorithm**:
```javascript
import Color from "colorjs.io";

function autofixContrast(fgColor, bgColor, targetRatio = 4.5) {
  const fg = new Color(fgColor);
  const bg = new Color(bgColor);

  let ratio = fg.contrast(bg, "WCAG21");
  if (ratio >= targetRatio) return fg.toString({format: "oklch"});

  // Nudge lightness until pass
  let [L, C, H] = fg.oklch;
  let iterations = 0;
  const maxIterations = 60;

  while (ratio < targetRatio && iterations < maxIterations) {
    // Move L away from bg lightness
    L = L < bg.oklch[0]
      ? Math.max(0, L - 0.01)   // Darker
      : Math.min(1, L + 0.01);  // Lighter

    const candidate = new Color("oklch", [L, C, H]);
    ratio = candidate.contrast(bg, "WCAG21");

    if (ratio >= targetRatio) {
      return candidate.toString({format: "oklch"});
    }
    iterations++;
  }

  return fg.toString({format: "oklch"}); // Fallback if can't fix
}
```

**Validation output**:
```
✅ success.fg on success.bg: 10.23:1 (AAA)
✅ error.fg on error.bg: 9.87:1 (AAA)
✅ warning.fg on warning.bg: 8.45:1 (AAA)
✅ info.fg on info.bg: 10.12:1 (AAA)
✅ primary on neutral-50: 4.83:1 (AA for large text)
⚠️  primary on neutral-200: Auto-adjusted L from 59.69% → 52.31% (4.51:1)
```

---

## Tailwind v4 Wiring

**Checks**:
1. Tailwind config exists (`tailwind.config.js` or `tailwind.config.ts`)
2. `globals.css` imports `design/systems/tokens.css`
3. Colors use CSS variables (`var(--color-*)`) not hardcoded palette
4. Font families match tokens
5. Shadow scale matches elevation scale

**Expected globals.css**:
```css
@import '../design/systems/tokens.css';

@tailwind base;
@tailwind components;
@tailwind utilities;
```

**Expected tailwind.config.js** (v4 style):
```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: ['./app/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: 'var(--color-primary)',
        secondary: 'var(--color-secondary)',
        // ... map all tokens
      }
    }
  }
}
```

**Validation errors**:
```
❌ Tailwind config not found
   Fix: npx tailwindcss init

❌ Missing import in globals.css
   Fix: Add @import '../design/systems/tokens.css';

⚠️  Hardcoded colors in tailwind.config.js
   Found: colors: { primary: '#3b82f6' }
   Expected: colors: { primary: 'var(--color-primary)' }
```

---

## CSS Variables Output

**Output** (`design/systems/tokens.css`):

```css
:root {
  /* Brand colors (OKLCH with sRGB fallback) */
  --color-primary: oklch(59.69% 0.156 261.45);
  --color-primary-fallback: #3b82f6;
  --color-secondary: oklch(58.23% 0.167 271.45);
  --color-secondary-fallback: #6366f1;
  --color-accent: oklch(67.89% 0.152 164.57);
  --color-accent-fallback: #10b981;

  /* Semantic colors (bg/fg/border/icon structure) */
  --color-success-bg: oklch(95% 0.02 145);
  --color-success-fg: oklch(25% 0.12 145);
  --color-success-border: oklch(85% 0.05 145);
  --color-success-icon: oklch(35% 0.13 145);

  --color-error-bg: oklch(95% 0.02 27);
  --color-error-fg: oklch(30% 0.18 27);
  --color-error-border: oklch(85% 0.08 27);
  --color-error-icon: oklch(40% 0.20 27);

  --color-warning-bg: oklch(95% 0.02 90);
  --color-warning-fg: oklch(35% 0.15 90);
  --color-warning-border: oklch(85% 0.08 90);
  --color-warning-icon: oklch(45% 0.16 90);

  --color-info-bg: oklch(95% 0.02 240);
  --color-info-fg: oklch(30% 0.12 240);
  --color-info-border: oklch(85% 0.05 240);
  --color-info-icon: oklch(40% 0.14 240);

  /* Neutral palette */
  --color-neutral-50: oklch(98% 0 0);
  --color-neutral-100: oklch(96% 0 0);
  --color-neutral-200: oklch(90% 0 0);
  --color-neutral-300: oklch(82% 0 0);
  --color-neutral-400: oklch(64% 0 0);
  --color-neutral-500: oklch(54% 0 0);
  --color-neutral-600: oklch(42% 0 0);
  --color-neutral-700: oklch(32% 0 0);
  --color-neutral-800: oklch(23% 0 0);
  --color-neutral-900: oklch(15% 0 0);
  --color-neutral-950: oklch(11% 0 0);

  /* Typography - Families */
  --font-sans: Inter, system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
  --font-mono: Fira Code, Menlo, Monaco, Consolas, monospace;
  --font-serif: Georgia, Cambria, 'Times New Roman', Times, serif;

  /* Typography - Sizes */
  --font-size-xs: 0.75rem;
  --font-size-sm: 0.875rem;
  --font-size-base: 1rem;
  --font-size-lg: 1.125rem;
  --font-size-xl: 1.25rem;
  --font-size-2xl: 1.5rem;
  --font-size-3xl: 1.875rem;
  --font-size-4xl: 2.25rem;

  /* Typography - Weights */
  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;

  /* Typography - Line Heights */
  --line-height-tight: 1.25;
  --line-height-normal: 1.5;
  --line-height-relaxed: 1.75;

  /* Typography - Letter Spacing */
  --letter-spacing-display: -0.025em;
  --letter-spacing-body: 0em;
  --letter-spacing-cta: 0.025em;

  /* Spacing scale (4px grid) */
  --spacing-0: 0px;
  --spacing-1: 4px;
  --spacing-2: 8px;
  --spacing-3: 12px;
  --spacing-4: 16px;
  --spacing-5: 20px;
  --spacing-6: 24px;
  --spacing-8: 32px;
  --spacing-10: 40px;
  --spacing-12: 48px;
  --spacing-16: 64px;
  --spacing-20: 80px;
  --spacing-24: 96px;

  /* Shadows - Light mode */
  --shadow-sm: 0 1px 2px oklch(0% 0 0 / 0.05);
  --shadow-md: 0 4px 6px oklch(0% 0 0 / 0.07), 0 2px 4px oklch(0% 0 0 / 0.06);
  --shadow-lg: 0 10px 15px oklch(0% 0 0 / 0.10), 0 4px 6px oklch(0% 0 0 / 0.05);

  /* Motion - Duration */
  --motion-duration-fast: 150ms;
  --motion-duration-base: 200ms;
  --motion-duration-slow: 300ms;
  --motion-duration-slower: 500ms;

  /* Motion - Easing */
  --motion-easing-standard: cubic-bezier(0.4, 0.0, 0.2, 1);
  --motion-easing-decelerate: cubic-bezier(0.0, 0.0, 0.2, 1);
  --motion-easing-accelerate: cubic-bezier(0.4, 0.0, 1.0, 1.0);

  /* Data visualization - Okabe-Ito (color-blind-safe) */
  --dataviz-okabe-ito-orange: oklch(68.29% 0.151 58.43);
  --dataviz-okabe-ito-sky-blue: oklch(70.17% 0.099 232.66);
  --dataviz-okabe-ito-bluish-green: oklch(59.78% 0.108 164.04);
  --dataviz-okabe-ito-yellow: oklch(89.87% 0.162 99.57);
  --dataviz-okabe-ito-blue: oklch(46.86% 0.131 264.05);
  --dataviz-okabe-ito-vermillion: oklch(57.50% 0.199 37.70);
  --dataviz-okabe-ito-reddish-purple: oklch(50.27% 0.159 328.36);
  --dataviz-okabe-ito-black: oklch(0% 0 0);

  /* Data visualization - Sequential scales */
  --dataviz-sequential-blue-1: oklch(95% 0.02 240);
  --dataviz-sequential-blue-2: oklch(75% 0.08 240);
  --dataviz-sequential-blue-3: oklch(55% 0.12 240);
  --dataviz-sequential-blue-4: oklch(35% 0.14 240);
  --dataviz-sequential-blue-5: oklch(25% 0.16 240);

  --dataviz-sequential-green-1: oklch(95% 0.02 145);
  --dataviz-sequential-green-2: oklch(75% 0.08 145);
  --dataviz-sequential-green-3: oklch(55% 0.12 145);
  --dataviz-sequential-green-4: oklch(35% 0.14 145);
  --dataviz-sequential-green-5: oklch(25% 0.16 145);

  /* Data visualization - Diverging scales */
  --dataviz-diverging-red-blue-1: oklch(95% 0.02 27);
  --dataviz-diverging-red-blue-2: oklch(75% 0.08 27);
  --dataviz-diverging-red-blue-3: oklch(90% 0 0);
  --dataviz-diverging-red-blue-4: oklch(75% 0.08 240);
  --dataviz-diverging-red-blue-5: oklch(95% 0.02 240);
}

/* Dark mode shadows (4-6x opacity increase) */
@media (prefers-color-scheme: dark) {
  :root {
    --shadow-sm: 0 1px 2px oklch(0% 0 0 / 0.30);
    --shadow-md: 0 4px 6px oklch(0% 0 0 / 0.35), 0 2px 4px oklch(0% 0 0 / 0.30);
    --shadow-lg: 0 10px 15px oklch(0% 0 0 / 0.40), 0 4px 6px oklch(0% 0 0 / 0.35);
  }
}

/* Reduced motion (accessibility) */
@media (prefers-reduced-motion: reduce) {
  :root {
    --motion-duration-fast: 0ms;
    --motion-duration-base: 0ms;
    --motion-duration-slow: 0ms;
    --motion-duration-slower: 0ms;
    --motion-easing-standard: linear;
    --motion-easing-decelerate: linear;
    --motion-easing-accelerate: linear;
  }
}

/* OKLCH fallback for legacy browsers (~8%) */
@supports not (color: oklch(0% 0 0)) {
  :root {
    --color-primary: var(--color-primary-fallback);
    --color-secondary: var(--color-secondary-fallback);
    --color-accent: var(--color-accent-fallback);
  }
}
```

---

## Style Debt Reporting

**Detection**:
```bash
# Find hardcoded colors
grep -rnE "#[0-9a-fA-F]{6}" app src components emails server/pdf \
  --include="*.tsx" --include="*.jsx" --include="*.css" --include="*.mjml" \
  > design/systems/violations-colors.txt

# Find arbitrary Tailwind values
grep -rnE "bg-\[|text-\[|border-\[|p-\[|m-\[|shadow-\[" app src components \
  --include="*.tsx" --include="*.jsx" \
  > design/systems/violations-arbitrary.txt
```

**Report output**:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  Style Debt Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Total violations: 127
  Hardcoded hex colors: 89
  Arbitrary Tailwind values: 38

Top offenders (hex colors):
  #3b82f6 → 23 occurrences (should be: bg-primary or var(--color-primary))
  #10b981 → 15 occurrences (should be: bg-success or var(--color-success-bg))
  #ef4444 → 12 occurrences (should be: bg-error or var(--color-error-bg))

Top offenders (arbitrary values):
  bg-[#3b82f6] → 8 occurrences (should be: bg-primary)
  p-[15px] → 6 occurrences (should be: p-4 [16px])
  shadow-[0_4px_8px_rgba(0,0,0,0.1)] → 4 occurrences (should be: shadow-md)

Migration guide: design/systems/token-migration-guide.md

Next steps:
1. Review violations-colors.txt and violations-arbitrary.txt
2. Migrate top offenders (see migration guide)
3. Re-run tokens:validate to check progress
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Quality Gates

**FAIL (block next phase)**:
- Tailwind config missing entirely
- `tokens.css` not imported in `globals.css`
- Any text color pairing <**4.5:1** after auto-fix (WCAG 2.1 minimum)
- >200 hardcoded violations (codebase too polluted - requires cleanup first)

**WARN (non-blocking)**:
- 20–200 hardcoded occurrences or arbitrary Tailwind values
- Data-viz palette not applied in chart config
- Some text only AA (4.5:1) not AAA (7:1)
- Custom font families not web-optimized (no `font-display: swap`)

---

## Migration Rules (Non-UI Surfaces)

### Emails (MJML/HTML)

**Before** (inline hex):
```html
<mj-section background-color="#3b82f6">
  <mj-text color="#ffffff">Welcome!</mj-text>
</mj-section>
```

**After** (CSS variables):
```html
<mj-style>
  .brand-primary { background-color: var(--color-primary); }
  .text-white { color: var(--color-neutral-50); }
</mj-style>
<mj-section css-class="brand-primary">
  <mj-text css-class="text-white">Welcome!</mj-text>
</mj-section>
```

**Note**: Some email clients don't support CSS variables. Use build-time replacement:
```javascript
// build-emails.js
const tokens = JSON.parse(fs.readFileSync('design/systems/tokens.json'));
const html = mjml(template);
const withTokens = html.replace(/var\(--color-(\w+)\)/g, (_, name) => {
  return tokens.colors.brand[name]?.fallback || tokens.colors.semantic[name]?.fallback;
});
```

---

### PDFs (WeasyPrint/Puppeteer)

**Before** (hardcoded CSS):
```css
/* report-styles.css */
.header {
  background-color: #3b82f6;
  color: #ffffff;
}
```

**After** (tokens):
```css
/* report-styles.css */
@import '../design/systems/tokens.css';

.header {
  background-color: var(--color-primary);
  color: var(--color-neutral-50);
}
```

**Python (WeasyPrint)**:
```python
from weasyprint import HTML, CSS

html = HTML(string=template_html)
css = CSS(filename='design/systems/tokens.css')
pdf = html.write_pdf(stylesheets=[css])
```

---

### CLI (chalk/colorette)

**Before** (raw hex):
```javascript
import chalk from 'chalk';

console.log(chalk.hex('#3b82f6')('Success!'));
console.log(chalk.hex('#ef4444')('Error!'));
```

**After** (token helpers):
```javascript
import { chalkPrimary, chalkError, chalkSuccess } from './lib/chalk-tokens.js';

console.log(chalkSuccess('Success!'));
console.log(chalkError('Error!'));
```

**Token helper** (`lib/chalk-tokens.js`):
```javascript
import chalk from 'chalk';
import tokens from '../design/systems/tokens.json' assert { type: 'json' };

export const chalkPrimary = chalk.hex(tokens.colors.brand.primary.fallback);
export const chalkError = chalk.hex(tokens.colors.semantic.error.fg.fallback);
export const chalkSuccess = chalk.hex(tokens.colors.semantic.success.fg.fallback);
export const chalkWarning = chalk.hex(tokens.colors.semantic.warning.fg.fallback);
export const chalkInfo = chalk.hex(tokens.colors.semantic.info.fg.fallback);
```

---

### Charts (d3/Chart.js/Recharts)

**Before** (random colors):
```javascript
const chartColors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444'];
```

**After** (Okabe-Ito color-blind-safe):
```javascript
import tokens from './design/systems/tokens.json';

const chartColors = Object.values(tokens.dataViz.categorical['okabe-ito'])
  .map(c => c.fallback);

// Chart.js example
new Chart(ctx, {
  type: 'bar',
  data: {
    datasets: [{
      backgroundColor: chartColors[0],
      borderColor: chartColors[0]
    }]
  }
});

// Recharts example
<BarChart>
  <Bar dataKey="value" fill={chartColors[0]} />
</BarChart>

// d3 example
d3.scaleOrdinal()
  .domain(categories)
  .range(chartColors);
```

**Why Okabe-Ito**: Scientifically validated for color-blind users (deuteranopia, protanopia, tritanopia). Used by Nature, Science, and R/ggplot2.

---

## Package Scripts

Add to `package.json`:

```json
{
  "scripts": {
    "tokens:init": "node .spec-flow/scripts/init-brand-tokens.mjs",
    "tokens:scan": "node .spec-flow/scripts/modules/scan.mjs",
    "tokens:validate": "node .spec-flow/scripts/modules/validate-tailwind.mjs",
    "tokens:report": "cat design/systems/violations-*.txt | wc -l && echo 'violations found'"
  }
}
```

**Usage**:
```bash
# First time setup
pnpm run tokens:init

# Re-scan after changes
pnpm run tokens:scan

# Check Tailwind wiring
pnpm run tokens:validate

# Get violation count
pnpm run tokens:report
```

---

## Error Handling

**Missing Tailwind config**: Show creation snippet, mark as error (block):
```
❌ Tailwind config not found

Fix: npx tailwindcss init
```

**Contrast failures**: Auto-adjust lightness until ≥4.5:1 ratio achieved:
```
⚠️  primary on neutral-200: Auto-adjusted L from 59.69% → 52.31% (4.51:1)
```

**Scan failures**: Continue with empty detected-tokens.json, warn user:
```
⚠️  Brownfield scan failed in directory: emails/
   Continuing with partial results...
```

**OKLCH support**: Auto-fallback to sRGB for legacy browsers via `@supports`:
```css
@supports not (color: oklch(0% 0 0)) {
  :root {
    --color-primary: var(--color-primary-fallback);
  }
}
```

---

## References

**Color spaces**:
- [OKLCH in CSS (MDN)](https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/oklch) - Perceptually uniform color space
- [Color.js documentation](https://colorjs.io/) - Contrast calculation and color manipulation

**WCAG standards**:
- [WCAG 2.1 Success Criterion 1.4.3](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html) - Minimum contrast 4.5:1 for normal text
- [WCAG 2.1 Success Criterion 1.4.6](https://www.w3.org/WAI/WCAG21/Understanding/contrast-enhanced.html) - Enhanced contrast 7:1 for AAA

**Tailwind**:
- [Tailwind CSS v4 beta](https://tailwindcss.com/docs/v4-beta) - Theme variables as CSS variables

**Color-blind palettes**:
- [Okabe-Ito palette (RDocumentation)](https://www.rdocumentation.org/packages/colorblindr/versions/0.1.0/topics/palette_OkabeIto) - Scientifically validated categorical palette
- [Color Universal Design (CUD)](https://jfly.uni-koeln.de/color/) - Original Okabe-Ito material

---

## Philosophy

**OKLCH over sRGB/HSL**: Perceptually uniform color space yields saner ramps and better contrast control. Fallback to sRGB for legacy browsers.

**Contrast-first**: Validate all text elements against WCAG AA minimum (4.5:1). Target AAA (7:1) for body text.

**Consolidate debt**: Brownfield scanning identifies duplicates; propose 60%+ reduction in unique values.

**CSS variables everywhere**: Tailwind v4 direction; single source of truth for design tokens.

**Accessibility built-in**: Reduced motion, focus ring, colorblind-safe data viz (Okabe-Ito palette).

**Non-UI surfaces matter**: Emails, PDFs, CLI, and charts deserve the same design system rigor as UI components.

---

## shadcn/ui Integration (v2.1)

### Overview

When the `--shadcn` flag is provided to `/init --tokens`, the system generates shadcn/ui-compatible CSS variable aliases that map OKLCH tokens to shadcn's expected variable names. This preserves OKLCH's superior accessibility while enabling seamless shadcn component usage.

**Key principle**: OKLCH tokens remain the source of truth. shadcn variables are aliases that reference OKLCH tokens.

### OKLCH → shadcn Variable Mapping

shadcn/ui components expect specific CSS variable names. The token bridge creates aliases:

```css
/* shadcn/ui CSS Variable Aliases */
/* These reference OKLCH tokens - not hardcoded values */

:root {
  /* Core Colors */
  --background: var(--color-neutral-50);
  --foreground: var(--color-neutral-900);

  /* Cards & Popovers */
  --card: var(--color-neutral-50);
  --card-foreground: var(--color-neutral-900);
  --popover: var(--color-neutral-50);
  --popover-foreground: var(--color-neutral-900);

  /* Primary */
  --primary: var(--color-primary);
  --primary-foreground: var(--color-neutral-50);

  /* Secondary */
  --secondary: var(--color-neutral-100);
  --secondary-foreground: var(--color-neutral-900);

  /* Muted */
  --muted: var(--color-neutral-100);
  --muted-foreground: var(--color-neutral-500);

  /* Accent */
  --accent: var(--color-neutral-100);
  --accent-foreground: var(--color-neutral-900);

  /* Destructive */
  --destructive: var(--color-error-fg);
  --destructive-foreground: var(--color-neutral-50);

  /* Borders & Inputs */
  --border: var(--color-neutral-200);
  --input: var(--color-neutral-200);
  --ring: var(--color-primary);

  /* Border Radius */
  --radius: 0.5rem;  /* Configurable via questionnaire */
}
```

### Dark Mode Mapping

```css
.dark {
  --background: var(--color-neutral-950);
  --foreground: var(--color-neutral-50);
  --card: var(--color-neutral-900);
  --card-foreground: var(--color-neutral-50);
  --popover: var(--color-neutral-900);
  --popover-foreground: var(--color-neutral-50);
  --primary: var(--color-primary);  /* OKLCH auto-adjusts */
  --primary-foreground: var(--color-neutral-950);
  --secondary: var(--color-neutral-800);
  --secondary-foreground: var(--color-neutral-50);
  --muted: var(--color-neutral-800);
  --muted-foreground: var(--color-neutral-400);
  --accent: var(--color-neutral-800);
  --accent-foreground: var(--color-neutral-50);
  --destructive: var(--color-error-icon);
  --destructive-foreground: var(--color-neutral-50);
  --border: var(--color-neutral-800);
  --input: var(--color-neutral-800);
  --ring: var(--color-primary);
}
```

### Menu Token Generation

Based on questionnaire answers for menu_color and menu_accent:

**Menu Color Options**:

| Choice | Token Values |
|--------|--------------|
| `background` | `--menu: var(--background)` |
| `surface` | `--menu: var(--card); --menu-shadow: var(--shadow-sm)` |
| `primaryTint` | `--menu: oklch(from var(--color-primary) l c h / 0.05)` |
| `glass` | `--menu: oklch(from var(--background) l c h / 0.8); --menu-backdrop: blur(8px)` |

**Menu Accent Options**:

| Choice | Token Values |
|--------|--------------|
| `border` | `--menu-accent-border: 3px solid var(--primary); --menu-accent-bg: transparent` |
| `background` | `--menu-accent-border: none; --menu-accent-bg: oklch(from var(--color-primary) l c h / 0.1)` |
| `iconTint` | `--menu-accent-border: none; --menu-accent-bg: transparent; --menu-accent-icon: var(--primary)` |
| `combined` | `--menu-accent-border: 3px solid var(--primary); --menu-accent-bg: oklch(from var(--color-primary) l c h / 0.05)` |

**Generated Menu CSS**:
```css
:root {
  /* Menu theming */
  --menu: var(--background);
  --menu-hover: var(--color-neutral-100);
  --menu-active: var(--primary);
  --menu-accent-border: 3px solid var(--primary);
  --menu-accent-bg: transparent;
  --menu-radius: calc(var(--radius) - 2px);
}

.dark {
  --menu: var(--color-neutral-900);
  --menu-hover: var(--color-neutral-800);
}
```

### components.json Generation

The token generation creates a shadcn/ui CLI configuration file:

```json
{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "default",
  "rsc": true,
  "tsx": true,
  "tailwind": {
    "config": "tailwind.config.ts",
    "css": "app/globals.css",
    "baseColor": "neutral",
    "cssVariables": true
  },
  "aliases": {
    "components": "@/components",
    "utils": "@/lib/utils",
    "ui": "@/components/ui",
    "lib": "@/lib",
    "hooks": "@/hooks"
  },
  "iconLibrary": "lucide"
}
```

**Style preset mapping**:

| Questionnaire Choice | shadcn Style | Density |
|---------------------|--------------|---------|
| Default | `default` | comfortable (1x) |
| New York | `new-york` | comfortable (1x) |
| Minimal | `default` | spacious (1.25x) |
| Bold | `new-york` | compact (0.85x) |

### Icon Library Integration

Based on questionnaire selection, install the appropriate package:

| Choice | Package | Import Pattern |
|--------|---------|----------------|
| Lucide | `lucide-react` | `import { Icon } from 'lucide-react'` |
| Heroicons | `@heroicons/react` | `import { IconOutline } from '@heroicons/react/24/outline'` |
| Phosphor | `@phosphor-icons/react` | `import { Icon } from '@phosphor-icons/react'` |

### Font Configuration (Next.js)

For Next.js projects, configure `next/font` in `app/layout.tsx`:

```typescript
// app/layout.tsx
import { Inter } from 'next/font/google'
// OR for Geist:
// import { GeistSans, GeistMono } from 'geist/font'
// OR for Plus Jakarta Sans:
// import { Plus_Jakarta_Sans } from 'next/font/google'

const fontSans = Inter({
  subsets: ['latin'],
  variable: '--font-sans',
})

const fontMono = /* Fira_Code, JetBrains_Mono, etc. */({
  subsets: ['latin'],
  variable: '--font-mono',
})

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={`${fontSans.variable} ${fontMono.variable}`}>
      <body>{children}</body>
    </html>
  )
}
```

### Border Radius Scale

Based on questionnaire selection:

| Choice | `--radius` Value | Effect |
|--------|------------------|--------|
| None | `0` | Sharp corners everywhere |
| Small | `0.25rem` (4px) | Minimal rounding |
| Medium | `0.5rem` (8px) | Modern balance |
| Large | `0.75rem` (12px) | Soft, friendly |
| Full | `9999px` | Pill shapes |

shadcn components use this value with modifiers:
- `--radius` - Default for buttons, inputs
- `calc(var(--radius) - 2px)` - Nested elements
- `calc(var(--radius) + 4px)` - Cards, dialogs

### Tailwind v4 Integration

Update `tailwind.config.ts` to reference CSS variables:

```typescript
// tailwind.config.ts
import type { Config } from 'tailwindcss'

const config: Config = {
  darkMode: ['class'],
  content: ['./app/**/*.{ts,tsx}', './components/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        // Map OKLCH tokens
        primary: 'var(--color-primary)',
        secondary: 'var(--color-secondary)',
        // ... other brand colors

        // shadcn aliases work automatically via CSS variables
      },
      borderRadius: {
        lg: 'var(--radius)',
        md: 'calc(var(--radius) - 2px)',
        sm: 'calc(var(--radius) - 4px)',
      },
      fontFamily: {
        sans: ['var(--font-sans)'],
        mono: ['var(--font-mono)'],
      },
    },
  },
  plugins: [require('tailwindcss-animate')],
}

export default config
```

### Menu Component Variants (tailwind-variants)

For projects using `tailwind-variants`, generate menu styling presets:

```typescript
// components/ui/menu-variants.ts
import { tv } from 'tailwind-variants'

export const menuStyles = tv({
  slots: {
    root: 'flex flex-col',
    item: 'flex items-center gap-3 px-3 py-2 rounded-[var(--menu-radius)] transition-colors',
    icon: 'h-5 w-5',
    label: 'flex-1',
  },
  variants: {
    menuColor: {
      background: { root: 'bg-[var(--menu)]' },
      surface: { root: 'bg-card shadow-sm' },
      primaryTint: { root: 'bg-primary/5' },
      glass: { root: 'bg-background/80 backdrop-blur-sm' },
    },
    menuAccent: {
      border: {
        item: 'data-[active=true]:border-l-[3px] data-[active=true]:border-primary data-[active=true]:pl-[calc(0.75rem-3px)]',
      },
      background: {
        item: 'data-[active=true]:bg-primary/10',
      },
      iconTint: {
        item: '[&[data-active=true]_svg]:text-primary',
      },
      combined: {
        item: 'data-[active=true]:border-l-[3px] data-[active=true]:border-primary data-[active=true]:bg-primary/5 data-[active=true]:pl-[calc(0.75rem-3px)]',
      },
    },
    state: {
      default: { item: 'text-foreground' },
      hover: { item: 'bg-[var(--menu-hover)]' },
      active: { item: 'font-medium' },
      disabled: { item: 'opacity-50 cursor-not-allowed' },
    },
  },
  defaultVariants: {
    menuColor: 'background',
    menuAccent: 'border',
    state: 'default',
  },
})
```

### Primary Scale Generation

Generate full 11-shade OKLCH scale from base hue:

```javascript
// generate-primary-scale.js
function generateOKLCHScale(hue, chroma = 0.15) {
  const lightnesses = {
    50:  0.98,
    100: 0.94,
    200: 0.88,
    300: 0.78,
    400: 0.65,
    500: 0.55,
    600: 0.48,  // Primary action color
    700: 0.40,
    800: 0.32,
    900: 0.22,
    950: 0.14,
  };

  const scale = {};
  for (const [name, lightness] of Object.entries(lightnesses)) {
    // Reduce chroma at extreme lightnesses for better contrast
    const adjustedChroma = lightness > 0.9 || lightness < 0.2
      ? chroma * 0.3
      : chroma;
    scale[name] = `oklch(${lightness * 100}% ${adjustedChroma} ${hue})`;
  }
  return scale;
}

// Usage based on questionnaire
const hueMap = { blue: 250, purple: 285, green: 150, orange: 50, red: 25 };
const primaryScale = generateOKLCHScale(hueMap[selectedColor]);
```

### Customization Summary Table

| Questionnaire | Affects | Files Modified |
|---------------|---------|----------------|
| Style preset | shadcn style, density | `components.json`, spacing tokens |
| Base color | Primary scale (11 shades) | `tokens.json`, `tokens.css` |
| Theme mode | Dark mode CSS | `tokens.css`, `layout.tsx` |
| Icon library | Icon imports | `package.json`, `components.json` |
| Font family | Typography | `layout.tsx`, `tailwind.config.ts` |
| Border radius | `--radius` variable | `tokens.css` |
| Menu color | Menu background tokens | `tokens.css`, `menu-variants.ts` |
| Menu accent | Menu active state tokens | `tokens.css`, `menu-variants.ts` |

### Quality Gates (shadcn Integration)

**FAIL**:
- `components.json` missing after --shadcn flag
- Icon library not installed
- shadcn CSS variable aliases missing from tokens.css

**WARN**:
- Font not configured in layout.tsx
- `tailwindcss-animate` plugin not installed
- Dark mode class not on html element
