---
name: dev-implement-ui-ux
emoji: "🎨"
description: Comprehensive UI/UX design and implementation skill covering visual design principles, color theory, typography, spacing systems, layout composition, accessibility (WCAG 2.2), animation, and systematic implementation workflows
---

# UI/UX Design & Implementation

**Version:** 2.0.0
**Category:** Design + Implement
**Related Skills:** dev-storybook, dev-vue, dev-css-design-system

## Overview

Comprehensive skill for both **designing** and **implementing** UI/UX. Covers visual design principles (color, typography, spacing, layout, hierarchy), accessibility compliance (WCAG 2.2), animation patterns, and systematic implementation workflows.

## When to Activate This Skill

Invoke this skill when:
- Designing color palettes or visual systems
- Creating typography hierarchies
- Building spacing and layout systems
- Implementing UI/UX fixes from audits
- Ensuring WCAG 2.2 accessibility compliance
- Adding animations and microinteractions
- Avoiding AI-generic design patterns
- Matching reference designs

---

# PART 1: COLOR THEORY & PALETTE GENERATION

## 1.1 HSL Color Model

```
HSL = Hue, Saturation, Lightness

Hue (0-360°):
- 0° = Red
- 60° = Yellow
- 120° = Green
- 180° = Cyan
- 240° = Blue
- 300° = Magenta

Saturation (0-100%):
- 0% = Grayscale
- 100% = Pure color

Lightness (0-100%):
- 0% = Black
- 50% = Pure color
- 100% = White
```

## 1.2 Color Wheel Relationships

| Relationship | Formula | Degrees | Use Case |
|--------------|---------|---------|----------|
| Analogous | H ± 30° | -30°, 0°, +30° | Harmonious, safe |
| Complementary | H + 180° | Opposite | High contrast |
| Triadic | H + 120°, H + 240° | Equally spaced | Vibrant, balanced |
| Split-Complementary | H + 150°, H + 210° | 150° apart | Less harsh |
| Tetradic | H + 90°, H + 180°, H + 270° | 90° apart | Complex but harmonious |

### Example: Building Palette from Blue (210°)

```
Primary Blue: 210° (hsl(210, 70%, 50%))

Analogous (210° ± 30°):
- 180° Cyan
- 210° Blue ← Primary
- 240° Indigo

Complementary:
- 30° Orange

Triadic:
- 210° Blue
- 330° Magenta
- 90° Yellow-Green
```

## 1.3 Tints, Shades, and Tones

```css
:root {
  /* Base color */
  --hue-primary: 210;
  --sat-primary: 70%;

  /* Tints (increase lightness) */
  --color-primary-50: hsl(var(--hue-primary), var(--sat-primary), 95%);
  --color-primary-100: hsl(var(--hue-primary), var(--sat-primary), 90%);
  --color-primary-200: hsl(var(--hue-primary), var(--sat-primary), 80%);
  --color-primary-300: hsl(var(--hue-primary), var(--sat-primary), 70%);
  --color-primary-400: hsl(var(--hue-primary), var(--sat-primary), 60%);

  /* Core */
  --color-primary-500: hsl(var(--hue-primary), var(--sat-primary), 50%);
  --color-primary-600: hsl(var(--hue-primary), var(--sat-primary), 40%);

  /* Shades (decrease lightness) */
  --color-primary-700: hsl(var(--hue-primary), var(--sat-primary), 30%);
  --color-primary-800: hsl(var(--hue-primary), var(--sat-primary), 20%);
  --color-primary-900: hsl(var(--hue-primary), var(--sat-primary), 10%);
}
```

## 1.4 Color Psychology

| Color | Hue | Psychology | UI Uses |
|-------|-----|------------|---------|
| Red | 0° | Energy, urgency, danger | Error states, delete actions, alerts |
| Orange | 30° | Enthusiasm, warmth | Friendly CTAs, warnings |
| Yellow | 60° | Happiness, caution | Warning messages, highlights |
| Green | 120° | Growth, safety, success | Success states, "go" actions |
| Blue | 240° | Trust, stability, calm | Primary brand, links, info |
| Purple | 270° | Creativity, luxury | Premium features, AI/magic |
| Gray | Neutral | Balance, sophistication | Secondary actions, disabled |

## 1.5 The 60-30-10 Rule

```
60% - Primary (dominant, background/large areas)
30% - Secondary (supporting, surface colors)
10% - Accent (emphasis, CTAs, highlights)
```

```css
:root {
  /* 60% - Primary: light neutral background */
  --color-60: #F5F5F5;

  /* 30% - Secondary: surface/card color */
  --color-30: #FFFFFF;

  /* 10% - Accent: brand for CTAs */
  --color-10: #0EA5E9;
}

body { background: var(--color-60); }
.card { background: var(--color-30); }
button { background: var(--color-10); }
```

## 1.6 WCAG Contrast Requirements

| Content Type | Minimum Ratio | Example |
|--------------|---------------|---------|
| Normal text | 4.5:1 | Black on white = 21:1 ✓ |
| Large text (18px+) | 3:1 | Navy on light blue = 8.6:1 ✓ |
| UI components | 3:1 | Button border on background |
| Focus indicator | 3:1 | Focus outline on element |

### Quick Reference: Common Contrast Ratios

```
White #FFFFFF on:
- Black #000000 = 21:1 ✓ Excellent
- Navy #003366 = 11.3:1 ✓ Excellent
- Blue #0EA5E9 = 5.74:1 ✓ Good (AA)
- Gray #6B7280 = 7.5:1 ✓ Good (AAA)
- Light gray #D1D5DB = 2.1:1 ✗ Fail
```

## 1.7 Dark Mode Strategy

**Key Principle:** Adjust LIGHTNESS and SATURATION, not HUE.

```css
/* Light Mode */
:root {
  --color-primary: hsl(210, 70%, 50%);
  --color-text: hsl(0, 0%, 15%);
  --color-bg: hsl(0, 0%, 97%);
}

/* Dark Mode */
@media (prefers-color-scheme: dark) {
  :root {
    /* Brighter, less saturated for dark backgrounds */
    --color-primary: hsl(210, 60%, 65%);

    /* Text: white with opacity */
    --color-text: hsla(0, 0%, 100%, 0.87);
    --color-text-secondary: hsla(0, 0%, 100%, 0.60);

    /* Background: dark neutral */
    --color-bg: hsl(0, 0%, 12%);
    --color-surface: hsl(0, 0%, 18%);
  }
}
```

### Dark Mode Elevation (Lighter = More Elevated)

```css
@media (prefers-color-scheme: dark) {
  :root {
    --color-surface-base: hsl(210, 10%, 12%);    /* Darkest */
    --color-surface-1: hsl(210, 10%, 16%);       /* Raised */
    --color-surface-2: hsl(210, 10%, 20%);       /* More raised */
    --color-surface-3: hsl(210, 10%, 24%);       /* Even more */
    --color-surface-4: hsl(210, 10%, 28%);       /* Highest */
  }

  body { background: var(--color-surface-base); }
  .card { background: var(--color-surface-2); }
  .modal { background: var(--color-surface-3); }
}
```

---

# PART 2: TYPOGRAPHY SYSTEM

## 2.1 Type Scale Ratios

| Ratio | Name | Best For |
|-------|------|----------|
| 1.067 | Minor Second | Small UI, dense |
| 1.125 | Major Second | Apps, compact |
| 1.200 | Minor Third | Balanced web |
| **1.250** | **Major Third** | **Web apps (recommended)** |
| 1.333 | Perfect Fourth | Editorial |
| 1.414 | Augmented Fourth | Magazine |
| 1.500 | Perfect Fifth | Large displays |
| 1.618 | Golden Ratio | Art, luxury |

### Complete Type Scale (1.25 ratio, 16px base)

```
-2 (11px) - caption, small labels
-1 (13px) - fine print, helper text
 0 (16px) - body text, default
 1 (20px) - subheading, emphasis
 2 (25px) - section heading
 3 (31px) - large section heading
 4 (39px) - page heading
 5 (49px) - hero text
```

## 2.2 Fluid Typography with clamp()

```css
:root {
  --text-xs: clamp(11px, 1.5vw, 13px);
  --text-sm: clamp(12px, 1.8vw, 14px);
  --text-base: clamp(14px, 2vw, 16px);
  --text-md: clamp(16px, 2.2vw, 18px);
  --text-lg: clamp(18px, 2.5vw, 20px);
  --text-xl: clamp(20px, 3vw, 24px);
  --text-2xl: clamp(24px, 4vw, 30px);
  --text-3xl: clamp(28px, 5vw, 36px);
  --text-4xl: clamp(32px, 6vw, 42px);
  --text-5xl: clamp(36px, 8vw, 52px);
}

body { font-size: var(--text-base); }
h3 { font-size: var(--text-2xl); }
h2 { font-size: var(--text-3xl); }
h1 { font-size: var(--text-5xl); }
```

## 2.3 Line Height Guidelines

| Context | Line Height | Usage |
|---------|-------------|-------|
| Body text | 1.5 - 1.7 | Comfortable reading |
| Headings | 1.1 - 1.3 | Compact, readable |
| Dense UI | 1.4 - 1.5 | Forms, lists |
| Code/mono | 1.6 - 1.8 | Extra clarity |

```css
p { line-height: 1.6; }
h1, h2, h3 { line-height: 1.2; }
label { line-height: 1.5; }
code { line-height: 1.7; }
```

## 2.4 Line Length (Measure)

**Optimal: 45-75 characters (65ch ideal)**

```css
.prose {
  max-width: 65ch;  /* ~65 characters */
  margin: 0 auto;
}
```

## 2.5 Font Weight Usage

| Weight | Name | Usage |
|--------|------|-------|
| 400 | Regular | Body text (default) |
| 500 | Medium | Subtle emphasis, labels |
| 600 | Semi-bold | UI elements, captions |
| 700 | Bold | Strong emphasis, headings |

**Rule: Use only 2-3 weights for clarity (400, 600, 700)**

```css
body { font-weight: 400; }
label { font-weight: 600; }
h1, h2, strong { font-weight: 700; }
```

## 2.6 Font Pairing

| Heading | Body | Best For |
|---------|------|----------|
| Poppins | Inter | Tech, SaaS |
| Playfair Display | Lato | Luxury, editorial |
| Montserrat | Open Sans | Modern, friendly |

```css
:root {
  --font-display: 'Poppins', sans-serif;
  --font-body: 'Inter', -apple-system, sans-serif;
  --font-mono: 'Fira Code', monospace;
}

h1, h2, h3 { font-family: var(--font-display); }
body { font-family: var(--font-body); }
code { font-family: var(--font-mono); }
```

---

# PART 3: SPACING & RHYTHM SYSTEMS

## 3.1 8-Point Grid System

| Token | Value | Usage |
|-------|-------|-------|
| 0.5 | 2px | Hairlines, minimal |
| 1 | 4px | Micro spacing |
| 2 | 8px | Small gaps (xs) |
| 3 | 12px | Compact |
| 4 | 16px | Standard (sm) |
| 5 | 20px | Medium |
| 6 | 24px | Comfortable (md) |
| 8 | 32px | Large (lg) |
| 10 | 40px | Extra large (xl) |
| 12 | 48px | Huge (2xl) |
| 16 | 64px | Page spacing (3xl) |
| 20 | 80px | Section gaps |
| 24 | 96px | Hero spacing |

```css
:root {
  --space-0: 0;
  --space-0-5: 2px;
  --space-1: 4px;
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
}

.btn { padding: var(--space-2) var(--space-4); }  /* 8px 16px */
.card { padding: var(--space-6); }                 /* 24px */
section { padding: var(--space-16) 0; }            /* 64px */
```

## 3.2 Fibonacci Spacing (Alternative)

```
8 × 1  = 8px
8 × 2  = 16px
8 × 3  = 24px
8 × 5  = 40px
8 × 8  = 64px
8 × 13 = 104px
8 × 21 = 168px
```

**Use Fibonacci for:** Editorial, landing pages, organic feel
**Use 8-Point for:** Apps, forms, UI components

## 3.3 Golden Ratio Spacing (1.618)

```css
:root {
  --golden-1: 8px;
  --golden-2: 13px;   /* 8 × 1.618 */
  --golden-3: 21px;   /* 13 × 1.618 */
  --golden-4: 34px;
  --golden-5: 55px;
  --golden-6: 89px;
}
```

## 3.4 Proximity Principle

**Rule: Related items < 16px apart, unrelated > 24px apart**

```css
.form-group {
  margin-bottom: 24px;  /* Between groups - LARGE */
}

.form-group label {
  margin-bottom: 8px;   /* Label to input - SMALL */
}
```

---

# PART 4: LAYOUT COMPOSITION & GRIDS

## 4.1 Golden Ratio Layouts (1.618:1)

```
For container W pixels wide:
Main content = W ÷ 1.618
Sidebar = W - Main content

1200px container:
Main: 742px, Sidebar: 458px
```

```css
.golden-layout {
  display: grid;
  grid-template-columns: 1fr 0.618fr;
  gap: 24px;
  max-width: 1200px;
}

@media (max-width: 768px) {
  .golden-layout {
    grid-template-columns: 1fr;
  }
}
```

## 4.2 Rule of Thirds

Place focal points at grid intersections for natural visual flow.

```css
.rule-of-thirds {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  grid-template-rows: 1fr 1fr 1fr;
}

.focal-point {
  grid-column: 2 / 3;
  grid-row: 1 / 2;
  place-self: end;
}
```

## 4.3 12-Column Grid

```css
.grid-12 {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 24px;
  max-width: 1200px;
}

.col-4 { grid-column: span 4; }   /* 33% */
.col-6 { grid-column: span 6; }   /* 50% */
.col-8 { grid-column: span 8; }   /* 66% */
.col-12 { grid-column: span 12; } /* 100% */
```

## 4.4 Container Widths

| Size | Width | Use Case |
|------|-------|----------|
| xs | 480px | Mobile |
| sm | 640px | Large mobile |
| md | 768px | Tablet |
| lg | 1024px | Desktop |
| xl | 1280px | Wide desktop |
| 2xl | 1536px | Maximum |

```css
.container {
  max-width: 1024px;
  margin: 0 auto;
  padding: 0 24px;
}

.prose-container {
  max-width: 65ch;  /* Readable */
}
```

## 4.5 Auto-Fit Responsive Grids

```css
.grid-responsive {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
}
```

---

# PART 5: VISUAL HIERARCHY & BALANCE

## 5.1 Creating Hierarchy

### Size (1.2-1.5× each level)

```css
.caption { font-size: 13px; }
.body { font-size: 16px; }
.subhead { font-size: 20px; }
.h3 { font-size: 25px; }
.h2 { font-size: 31px; }
.h1 { font-size: 39px; }
```

### Color (Opacity)

```css
.text-primary { color: rgba(0, 0, 0, 0.87); }
.text-secondary { color: rgba(0, 0, 0, 0.60); }
.text-tertiary { color: rgba(0, 0, 0, 0.38); }
.text-disabled { color: rgba(0, 0, 0, 0.26); }
```

### Weight

```css
.body { font-weight: 400; }
.label { font-weight: 500; }
.subhead { font-weight: 600; }
.h1 { font-weight: 700; }
```

## 5.2 Gestalt Principles

| Principle | Rule | CSS Example |
|-----------|------|-------------|
| Proximity | Related < 16px | `gap: 8px` between label and input |
| Similarity | Same style = related | All buttons have same padding |
| Continuity | Aligned elements are path | `align-items: start` |
| Closure | Mind completes shapes | Dashed borders, outlined buttons |
| Figure-Ground | Elevated stands out | Cards with shadow on page |

## 5.3 Focal Point Creation

```css
.cta-primary {
  background: var(--color-primary);
  color: white;
  padding: 16px 32px;
  font-size: 18px;
  font-weight: 600;
  border-radius: 8px;
  box-shadow: 0 8px 16px rgba(0,0,0,0.15);
  margin: 48px 0;  /* Isolated */
}

.cta-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 24px rgba(0,0,0,0.2);
}
```

---

# PART 6: WCAG 2.2 ACCESSIBILITY (2024-2025)

## 6.1 All 9 New WCAG 2.2 Criteria

### 2.4.11 Focus Not Obscured (Minimum) - Level A

```css
*:focus {
  scroll-margin-top: 80px;  /* Account for sticky header */
}
```

### 2.4.12 Focus Not Obscured (Enhanced) - Level AA

No part of focused component hidden.

### 2.4.13 Focus Appearance - Level AAA

2px thick, 3:1 contrast.

```css
button:focus-visible {
  outline: 2px solid #0066CC;  /* 5.7:1 contrast ✓ */
  outline-offset: 2px;
}
```

### 2.5.7 Dragging Movements - Level AA

Provide single-pointer alternative to drag.

```html
<input type="range" id="slider">
<button onclick="setValue(0)">Min</button>
<button onclick="setValue(100)">Max</button>
```

### 2.5.8 Target Size (Minimum) - Level AA

**24×24px minimum, 44×44px recommended**

```css
button, a, input[type="checkbox"] {
  min-width: 24px;
  min-height: 24px;
}

.btn {
  min-width: 44px;
  min-height: 44px;
}

.icon-btn {
  width: 20px;
  height: 20px;
  padding: 12px;  /* Total: 44×44px */
}
```

### 3.2.6 Consistent Help - Level A

Help in same location on all pages.

### 3.3.7 Redundant Entry - Level A

Don't ask for same info twice. Use `autocomplete`.

### 3.3.8 Accessible Authentication (Minimum) - Level AA

No CAPTCHA as ONLY option.

```html
<button onclick="sendEmailLink()">Email me a sign-in link</button>
<button onclick="useWebAuthn()">Sign in with passkey</button>
<input type="password" autocomplete="current-password">
```

### 3.3.9 Accessible Authentication (Enhanced) - Level AAA

No cognitive test at all.

## 6.2 Complete Focus Implementation

```css
*:focus { outline: none; }

*:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

@media (prefers-contrast: more) {
  *:focus-visible {
    outline-width: 3px;
    outline-color: Highlight;
  }
}

.skip-link {
  position: absolute;
  top: -100px;
}

.skip-link:focus {
  top: 8px;
  left: 8px;
  padding: 12px 16px;
  background: white;
}
```

---

# PART 7: MICROINTERACTIONS & ANIMATION

## 7.1 Animation Timing

| Duration | Name | Use Case |
|----------|------|----------|
| 100-150ms | Micro | Instant feedback, hover |
| 150-200ms | Fast | Click, press |
| 200-300ms | Normal | Standard UI, modal |
| 300-400ms | Moderate | Panel slide |
| 400-500ms | Slow | Page transition |

```css
:root {
  --duration-micro: 100ms;
  --duration-fast: 150ms;
  --duration-normal: 250ms;
  --duration-moderate: 350ms;
  --duration-slow: 450ms;
}
```

## 7.2 Easing Curves

```css
:root {
  /* Entrances: fast start, slow end */
  --ease-out: cubic-bezier(0, 0, 0.2, 1);

  /* Exits: slow start, fast end */
  --ease-in: cubic-bezier(0.4, 0, 1, 1);

  /* State changes */
  --ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);

  /* Standard */
  --ease-standard: cubic-bezier(0.4, 0, 0.6, 1);
}

.modal-enter { animation: fadeIn 250ms var(--ease-out); }
.modal-exit { animation: fadeOut 200ms var(--ease-in); }
button:hover { transition: all 150ms var(--ease-standard); }
```

## 7.3 Reduced Motion Support

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

---

# PART 8: AVOIDING AI-GENERIC DESIGN

## 8.1 Anti-Patterns to Avoid

### Blue/Purple Gradients

```css
/* ❌ AI-GENERIC */
.hero { background: linear-gradient(135deg, #667eea, #764ba2); }

/* ✅ DISTINCTIVE */
.hero { background: var(--brand-primary); }
```

### Excessive Rounding

```css
/* ❌ AI-GENERIC */
* { border-radius: 12px; }

/* ✅ DISTINCTIVE - Strategic rounding */
.card { border-radius: 8px; }
.button { border-radius: 6px; }
.badge { border-radius: 16px; }
.input { border-radius: 4px; }
```

### Safe Sans-Serif Only

```css
/* ❌ AI-GENERIC */
body { font-family: -apple-system, sans-serif; }

/* ✅ DISTINCTIVE */
:root {
  --font-display: 'Poppins', sans-serif;
  --font-body: 'Inter', -apple-system, sans-serif;
}
```

## 8.2 Creating Distinctive Aesthetics

```css
:root {
  /* Brand-named colors, not generic "primary" */
  --color-ocean: #0891B2;
  --color-sunset: #F59E0B;
  --color-forest: #10B981;

  /* Intentional radius strategy */
  --radius-sm: 4px;
  --radius-brand: 6px;
  --radius-lg: 8px;
}

/* Distinctive hover */
.btn:hover {
  transform: translateY(-2px) scale(1.02);
  box-shadow: 0 8px 16px rgba(0,0,0,0.15);
}
```

---

# PART 9: IMPLEMENTATION WORKFLOWS

## 9.1 Design Token Migration

```bash
# Find hardcoded colors
grep -rn "color: #\|background: #" src/components --include="*.vue"

# Find hardcoded spacing
grep -rn "padding: [0-9]\|margin: [0-9]" src/components --include="*.vue"
```

```vue
<!-- BEFORE -->
<style scoped>
.button {
  color: #4ECDC4;
  background: #000;
  padding: 12px 24px;
}
</style>

<!-- AFTER -->
<style scoped>
.button {
  color: var(--brand-primary);
  background: var(--surface-elevated);
  padding: var(--space-3) var(--space-6);
}
</style>
```

## 9.2 Button Consolidation

```vue
<!-- BEFORE -->
<button class="menu-icon-button" @click="handleClick">
  <TrashIcon />
</button>

<!-- AFTER -->
<BaseIconButton
  variant="ghost"
  size="sm"
  aria-label="Delete item"
  @click="handleClick"
>
  <TrashIcon />
</BaseIconButton>
```

## 9.3 Accessibility Implementation

```bash
# Find buttons without aria-label
grep -rn "<button" src/components --include="*.vue" | grep -v "aria-label"
```

```vue
<!-- Icon-only buttons MUST have aria-label -->
<BaseIconButton aria-label="Delete task" @click="deleteTask">
  <TrashIcon />
</BaseIconButton>

<!-- Decorative icons should be aria-hidden -->
<BaseButton @click="save">
  <CheckIcon aria-hidden="true" />
  Save Changes
</BaseButton>
```

## 9.4 Theme Consistency

```bash
# Find hardcoded white backgrounds
grep -rn "background.*white\|background.*#fff" src/components --include="*.vue"
```

```vue
<!-- BEFORE: Breaks in dark theme -->
<style>
.card { background: white; color: black; }
</style>

<!-- AFTER: Respects theme -->
<style>
.card {
  background: var(--surface-elevated);
  color: var(--text-primary);
}
</style>
```

---

# PART 10: QUALITY CHECKLISTS

## Color Checklist

- [ ] Primary color chosen with brand intention
- [ ] Accent colors from color wheel (complementary/triadic)
- [ ] 60-30-10 rule applied
- [ ] WCAG AA contrast verified (4.5:1 normal, 3:1 large)
- [ ] Dark mode uses same hue, adjusted S/L

## Typography Checklist

- [ ] Type scale ratio chosen (1.25 recommended)
- [ ] Fluid sizing with clamp()
- [ ] Line heights: 1.5-1.7 body, 1.1-1.3 headings
- [ ] Line length: 65ch max
- [ ] Font weights: 400, 600, 700 only

## Spacing Checklist

- [ ] 8-point grid implemented
- [ ] Semantic tokens defined
- [ ] Related items < 16px, unrelated > 24px
- [ ] Vertical rhythm maintained

## Layout Checklist

- [ ] Golden ratio where appropriate
- [ ] 12-column grid for responsive
- [ ] Container widths: sm/md/lg/xl
- [ ] Whitespace used strategically

## Accessibility Checklist (WCAG 2.2 AA)

- [ ] Focus indicators: 2px, 3:1 contrast
- [ ] Touch targets: ≥24px (44px recommended)
- [ ] Keyboard navigation complete
- [ ] Color not only indicator
- [ ] Contrast: 4.5:1 normal text
- [ ] Help consistent across pages
- [ ] No CAPTCHA-only auth
- [ ] Dragging has alternatives
- [ ] prefers-reduced-motion respected

## Animation Checklist

- [ ] Timing: 100-500ms appropriate
- [ ] Easing: ease-out for entrances
- [ ] prefers-reduced-motion supported
- [ ] Animations serve purpose

## Distinctiveness Checklist

- [ ] Brand colors intentional (not generic blue)
- [ ] Rounding strategic (not 12px everywhere)
- [ ] Typography has personality
- [ ] Hover states distinctive
- [ ] No AI-generic patterns

---

## MANDATORY USER VERIFICATION REQUIREMENT

**CRITICAL**: Before claiming ANY issue is "fixed" or "complete":

1. **Technical Verification**: Run tests, verify no console errors
2. **Ask User**: Use `AskUserQuestion` to request verification
3. **Wait for Confirmation**: Do NOT claim success until user confirms

**Remember: The user is the final authority on whether something is fixed.**

---

# PART 11: APP ICON GENERATION (Tauri/Desktop/PWA)

## 11.1 Icon Size Requirements

| Platform | Sizes Required |
|----------|----------------|
| **Tauri/Desktop** | 32x32, 128x128, 256x256 (128x128@2x), 512x512 |
| **Windows ICO** | 16, 32, 48, 64, 128, 256 (multi-size) |
| **macOS ICNS** | 512x512 source |
| **Windows Store** | 44, 71, 89, 107, 142, 150, 284, 310 |
| **PWA/Web** | 180x180 (apple-touch-icon), favicon.ico |

## 11.2 ImageMagick Icon Pipeline

### CRITICAL: Scaling Without Cropping

When source image has different aspect ratio than target (e.g., wide 1312x736 → square 512x512):

```bash
# ❌ WRONG - Scales by height, crops width
magick convert source.png -resize x420 -gravity center -extent 512x512 icon.png

# ✅ CORRECT - Scales to FIT within bounds, centers with padding
magick convert source.png \
  -trim +repage \
  -resize 500x500 \
  -gravity center \
  -background none \
  -extent 512x512 \
  icon.png
```

**Key insight:** `-resize 500x500` scales proportionally until the LARGER dimension hits 500px. For a wide image, width becomes 500px, height scales proportionally (e.g., ~280px). Then `-extent 512x512` centers it with transparent padding.

### Complete Icon Generation Script

```bash
#!/bin/bash
# Generate all Tauri app icons from a 512x512 source

cd src-tauri/icons

# PNG sizes for Linux/Windows
magick convert icon.png -resize 32x32 32x32.png
magick convert icon.png -resize 128x128 128x128.png
magick convert icon.png -resize 256x256 128x128@2x.png

# Windows ICO (multi-size)
magick convert icon.png -define icon:auto-resize=256,128,64,48,32,16 icon.ico

# macOS ICNS
png2icns icon.icns icon.png 2>/dev/null || \
  magick convert icon.png -resize 512x512 icon.icns

# Windows Store logos
for size in 44 71 89 107 142 150 284 310; do
  magick convert icon.png -resize ${size}x${size} Square${size}x${size}Logo.png
done
magick convert icon.png -resize 50x50 StoreLogo.png

# PWA/Web icons
cd ../../public
magick convert ../src-tauri/icons/icon.png -resize 180x180 apple-touch-icon.png
magick convert ../src-tauri/icons/icon.png -define icon:auto-resize=48,32,16 favicon.ico

echo "All icons generated!"
```

## 11.3 Image Processing for Icons

### Remove Background (Flood Fill)

```bash
# Replace white/near-white background with transparency
magick convert input.png \
  -fuzz 10% \
  -transparent white \
  -trim +repage \
  output.png
```

### Prepare Wide Image for Square Icon

```bash
# For images wider than tall (e.g., 1312x736)
magick convert wide-source.png \
  -trim +repage \              # Remove whitespace
  -resize 500x500 \            # Fit within 500x500 (maintains aspect)
  -gravity center \            # Center the result
  -background none \           # Transparent background
  -extent 512x512 \            # Pad to exact 512x512
  icon.png
```

## 11.4 Verification

```bash
# Check dimensions
magick identify icon.png
# Expected: icon.png PNG 512x512 512x512+0+0 ...

# Check ICO contains all sizes
magick identify icon.ico
# Expected: Multiple lines showing 256x256, 128x128, 64x64, etc.
```

## 11.5 Tauri Icon Files

```
src-tauri/icons/
├── icon.png          # 512x512 master (REQUIRED)
├── icon.ico          # Windows (multi-size)
├── icon.icns         # macOS
├── 32x32.png         # Small
├── 128x128.png       # Medium
├── 128x128@2x.png    # Retina (256x256)
├── Square*.png       # Windows Store
└── StoreLogo.png     # Windows Store
```

## 11.6 Reinstall & Refresh (Linux/KDE)

After regenerating icons, rebuild and reinstall:

```bash
npm run tauri build
sudo dpkg -i src-tauri/target/release/bundle/deb/AppName_*.deb
kbuildsycoca6 --noincremental  # Rebuild KDE cache
kquitapp6 plasmashell && sleep 1 && kstart plasmashell &  # Restart panel
```

---

**Skill Keywords:** UI design, UX, color theory, typography, spacing, layout, grid, accessibility, WCAG 2.2, animation, design tokens, visual hierarchy, Gestalt, app icons, ImageMagick, Tauri

**Standards:** WCAG 2.2 (June 2024), Material Design 3, Apple HIG

**Last Updated:** January 2026
