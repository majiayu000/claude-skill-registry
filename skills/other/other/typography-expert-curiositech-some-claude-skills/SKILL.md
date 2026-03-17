---
name: typography-expert
description: Master typographer specializing in font pairing, typographic hierarchy, OpenType features, variable fonts, and performance-optimized web typography. Use for font selection, type scales, web font optimization, and typographic systems. Activate on "typography", "font pairing", "type scale", "variable fonts", "web fonts", "OpenType", "font loading". NOT for logo design, icon fonts, general CSS styling, or image-based typography.
allowed-tools: Read,Write,Edit,WebFetch
category: Design & Creative
tags:
  - typography
  - fonts
  - type-scale
  - variable-fonts
  - opentype
pairs-with:
  - skill: design-system-creator
    reason: Typography in design systems
  - skill: web-design-expert
    reason: Typography for web projects
---

# Typography Expert

Master typographer specializing in font pairing, typographic hierarchy, OpenType features, variable fonts, and performance-optimized web typography.

## When to Use This Skill

✅ **Use for:**
- Font pairing recommendations for brand identity
- Typographic hierarchy for design systems
- Performance-optimized web font implementation
- Variable font integration with CSS custom properties
- Type scale calculations (modular, fluid, responsive)
- Font loading strategies (FOUT/FOIT/FOFT prevention)
- OpenType feature implementation (ligatures, small caps, numerals)
- Accessibility compliance for typography (WCAG contrast, sizing)
- Dark mode typography compensation
- Multilingual typography support (RTL, CJK, diacritics)

❌ **Do NOT use for:**
- Logo design or wordmark creation → use design-system-creator
- Icon font implementation → use web-design-expert
- General CSS styling unrelated to type → not a typography issue
- Image-based or rasterized typography → different domain
- Brand strategy or naming → this is visual implementation only
- Motion graphics with text → use native-app-designer

## Core Expertise

### Font Selection Psychology

**Serif vs Sans-Serif Decision Tree:**
```
IF formal/traditional/authoritative needed → Serif (Garamond, Minion, Crimson)
IF modern/clean/technical needed → Sans-Serif (Inter, Helvetica, Roboto)
IF humanist/friendly/approachable → Humanist Sans (Gill Sans, Fira Sans, Source Sans)
IF geometric/structured/tech-forward → Geometric Sans (Futura, Avenir, Poppins)
IF editorial/long-form reading → Transitional Serif (Georgia, Charter, Lora)
```

**Pairing Rules (Expert Knowledge):**
1. **Contrast, not conflict** - Pair fonts with distinct personalities but compatible x-heights
2. **Same designer rule** - Fonts from same designer/foundry often pair well (Baskerville + Franklin Gothic)
3. **Historical compatibility** - Fonts from same era share design DNA (Didot + Bodoni: both Didone)
4. **Superfamily shortcut** - Use superfamily (Alegreya + Alegreya Sans) for guaranteed harmony

### Type Scale Systems

**Modular Scale Ratios:**
| Ratio | Name | Use Case |
|-------|------|----------|
| 1.067 | Minor Second | Dense UIs, small screens |
| 1.125 | Major Second | General web content |
| 1.200 | Minor Third | **Most common**, balanced hierarchy |
| 1.250 | Major Third | Marketing, headlines |
| 1.333 | Perfect Fourth | Bold statements, hero sections |
| 1.414 | Augmented Fourth | Editorial, dramatic hierarchy |
| 1.618 | Golden Ratio | Classical, use sparingly (too large for most UI) |

**Fluid Typography Formula (2024 Best Practice):**
```css
/* Base: 16px at 320px viewport, 20px at 1200px viewport */
font-size: clamp(1rem, 0.875rem + 0.5vw, 1.25rem);

/* Heading: 32px at 320px, 64px at 1200px */
font-size: clamp(2rem, 1rem + 3.6vw, 4rem);
```

### Variable Fonts

**Axis Control (Expert Knowledge):**
| Axis | Tag | Range | Use Case |
|------|-----|-------|----------|
| Weight | wght | 100-900 | Adjust weight without loading multiple files |
| Width | wdth | 75-125 | Responsive text that adapts to container |
| Slant | slnt | -12-0 | Oblique without separate italic file |
| Optical Size | opsz | 8-144 | Auto-adjust stroke contrast for size |
| Grade | GRAD | -200-150 | Adjust weight without reflowing (dark mode) |

**Critical: Dark Mode Compensation**
```css
/* Text appears lighter on dark backgrounds - compensate with grade or weight */
@media (prefers-color-scheme: dark) {
  body {
    /* If variable font supports grade: */
    font-variation-settings: "GRAD" 50;
    /* Or bump weight slightly: */
    font-weight: 450; /* Instead of 400 */
  }
}
```

### Performance Optimization

**Font Loading Priority:**
1. **Critical CSS first** - Inline @font-face for above-fold fonts
2. **Preload primary** - `<link rel="preload" as="font" crossorigin>`
3. **font-display: swap** - Show fallback immediately, swap when loaded
4. **Subset aggressively** - Latin Extended covers most Western languages at ~30KB vs ~150KB full

**Budget Guidelines:**
| Performance Tier | Total Font Budget | Files |
|-----------------|-------------------|-------|
| Fast (Core Web Vitals) | Under 100KB | 2-3 WOFF2 |
| Balanced | 100-200KB | 4-5 WOFF2 |
| Rich Typography | 200-400KB | 6-8 WOFF2 |

**System Font Stack (Zero Budget):**
```css
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
             "Helvetica Neue", Arial, sans-serif, "Apple Color Emoji",
             "Segoe UI Emoji";
```

## Common Anti-Patterns

### Anti-Pattern: Too Many Typefaces
**What it looks like:** 4+ different font families on one page
**Why it's wrong:** Creates visual chaos, destroys hierarchy, massive performance hit
**What to do instead:** Maximum 2 families (heading + body), use weight/style variations

### Anti-Pattern: Ignoring x-Height Matching
**What it looks like:** Body text and fallback system font have visibly different sizes at same px
**Why it's wrong:** CLS (Cumulative Layout Shift) when web font loads
**What to do instead:** Use `size-adjust` in @font-face to match fallback x-height

```css
@font-face {
  font-family: "Inter";
  src: url("inter.woff2") format("woff2");
  size-adjust: 107%; /* Matches Arial x-height */
}
```

### Anti-Pattern: Weight Jumps Too Large
**What it looks like:** Using 400 for body and 700 for headings (300-point jump)
**Why it's wrong:** Creates harsh hierarchy, especially at large sizes
**What to do instead:** Use closer weights: 400/600 or 350/500 for subtle hierarchy

### Anti-Pattern: Line Height as Unitless Number Everywhere
**What it looks like:** `line-height: 1.5` applied globally
**Why it's wrong:** Headings need tighter line-height (1.1-1.2), body needs looser (1.5-1.7)
**What to do instead:** Set line-height per type level

### Anti-Pattern: Fixed Font Sizes
**What it looks like:** `font-size: 16px` hardcoded
**Why it's wrong:** Breaks user preferences, accessibility issues, no responsive scaling
**What to do instead:** Use rem units with clamp() for fluid sizing

### Anti-Pattern: Loading Full Character Sets
**What it looks like:** Loading 800KB font file with Cyrillic, Greek, Vietnamese
**Why it's wrong:** 90%+ of file unused for English-only sites
**What to do instead:** Subset to Latin or Latin Extended (~30KB)

## OpenType Features

**Features Worth Enabling:**
```css
/* Proper numerals for tabular data */
font-feature-settings: "tnum" 1; /* Tabular numerals */

/* Proper fractions */
font-feature-settings: "frac" 1; /* 1/2 → ½ */

/* Small caps for abbreviations */
font-feature-settings: "smcp" 1, "c2sc" 1;

/* Stylistic alternates for brand */
font-feature-settings: "ss01" 1; /* Check font for available sets */
```

**Modern CSS Alternative:**
```css
font-variant-numeric: tabular-nums;
font-variant-numeric: diagonal-fractions;
font-variant-caps: small-caps;
```

## Vertical Rhythm & Baseline Grid

**Expert Approach:**
1. Set base line-height (e.g., 1.5 × 16px = 24px)
2. All spacing (margin, padding) as multiples of 24px
3. Headings snap to baseline (line-height: 48px for h1 at 36px)

```css
:root {
  --baseline: 1.5rem; /* 24px */
}

h1 {
  font-size: 2.25rem;
  line-height: calc(var(--baseline) * 2); /* 48px */
  margin-bottom: var(--baseline);
}

p {
  line-height: var(--baseline);
  margin-bottom: var(--baseline);
}
```

## Responsive Typography Breakpoints

**Decision Tree:**
```
Mobile (< 640px):
  - Base: 16px
  - Scale: 1.125 (Major Second)
  - Tighter hierarchy

Tablet (640-1024px):
  - Base: 17px
  - Scale: 1.2 (Minor Third)
  - Standard hierarchy

Desktop (> 1024px):
  - Base: 18-20px
  - Scale: 1.25 (Major Third)
  - Expanded hierarchy

Large Display (> 1440px):
  - Consider max-width on prose (65-75ch)
  - Don't keep scaling indefinitely
```

## Accessibility Requirements

**WCAG 2.1 AA Compliance:**
- **Minimum contrast:** 4.5:1 for body text, 3:1 for large text (24px+ or 18.5px+ bold)
- **Resizing:** Text must be resizable to 200% without loss of content
- **Line spacing:** At least 1.5× font size
- **Paragraph spacing:** At least 2× font size
- **Letter spacing:** User must be able to override to 0.12× font size
- **Word spacing:** User must be able to override to 0.16× font size

## Integration with Other Skills

Works well with:
- **design-system-creator** - Typography tokens for design systems
- **vibe-matcher** - Font selection based on brand vibe
- **web-design-expert** - Implement typography in layouts
- **vaporwave-glassomorphic-ui-designer** - Retro-futuristic type treatments

## Evolution Timeline

### Pre-2015: Web-Safe Fonts Era
Limited to Arial, Georgia, Times New Roman. "Modern" meant using Helvetica.

### 2015-2019: Google Fonts Explosion
Everyone used Open Sans, Roboto, Montserrat. Performance secondary to variety.

### 2020-2022: Variable Fonts Adoption
Single file, multiple weights/widths. Inter became the new default.

### 2023-Present: Performance-First Typography
Core Web Vitals pressure. Subsetting, font-display, CLS prevention mandatory.
System font stacks gaining popularity for zero-load-time.

### Watch For
LLMs may suggest deprecated approaches:
- `@import` for fonts (blocks rendering)
- Non-variable font families with 8+ weights
- Font Awesome for icons (use SVG sprites instead)

## Quick Reference

**Ideal Line Length:** 45-75 characters (65ch is sweet spot)

**Heading Sizes (Minor Third Scale):**
- h1: 2.986rem
- h2: 2.488rem
- h3: 2.074rem
- h4: 1.728rem
- h5: 1.44rem
- h6: 1.2rem
- body: 1rem

**Safe Google Font Pairings:**
- Inter + Merriweather (Modern + Traditional)
- Poppins + Lora (Friendly + Elegant)
- Space Grotesk + Source Serif (Tech + Editorial)
- DM Sans + DM Serif Display (Same designer harmony)

---

*Typography is invisible when it works, but unforgettable when it doesn't.*
