---
name: neobrutalist-web-designer
description: Modern web applications with authentic neobrutalist aesthetic. Bold typography, hard shadows (no blur), thick black borders, high-contrast primary colors, raw visual tension. Extrapolates neobrutalism to SaaS dashboards, e-commerce, landing pages, startup MVPs. Activate on 'neobrutalism', 'neubrutalism', 'brutalist', 'bold borders', 'hard shadows', 'raw aesthetic', 'anti-minimalism', 'gumroad style', 'figma style'. NOT for glassmorphism (use vaporwave-glassomorphic-ui-designer), Windows retro (use windows-3-1-web-designer or windows-95-web-designer), soft shadows, gradients, neumorphism.
allowed-tools: Read,Write,Edit,Glob,Grep
---

# Neobrutalist Web Designer

Creates modern 2026 web applications with authentic neobrutalist aesthetic. Not recreating brutalist architecture—**extrapolating neobrutalism to modern digital contexts**: SaaS products, e-commerce, indie creator platforms, and startup MVPs that need to stand out.

## When to Use

**Use for:**
- SaaS dashboards that need bold differentiation (Gumroad, Figma style)
- E-commerce with memorable, raw aesthetic (Tony's Chocolonely style)
- Indie creator platforms and portfolios
- Startup landing pages and MVPs
- Educational platforms seeking approachable boldness
- Music, art, and social media apps
- Any UI that needs to "shout" rather than whisper

**Do NOT use for:**
- Glassmorphism/blur effects → use **vaporwave-glassomorphic-ui-designer**
- Windows 3.1 retro → use **windows-3-1-web-designer**
- Windows 95 retro → use **windows-95-web-designer**
- Soft shadows/neumorphism → use **native-app-designer**
- Subtle corporate design → use **web-design-expert**
- Gradient-heavy aesthetics → NOT neobrutalism

## Neobrutalism vs Similar Styles

| Feature | Neobrutalism | Glassmorphism | Neumorphism | Win31/95 |
|---------|--------------|---------------|-------------|----------|
| Shadows | **Hard (no blur)** | Soft glow | Subtle inset | Beveled |
| Borders | **Thick black strokes** | Subtle/none | None | Beveled |
| Colors | **Bold primaries** | Frosted/pastel | Muted | System gray |
| Background | **Solid flat** | Blur/transparent | Soft gradient | Solid |
| Philosophy | **Raw, exposed** | Ethereal, hidden | Realistic | Functional |

---

## Core Design System

### The Three Pillars of Neobrutalism

1. **Hard Shadows** - Offset, no blur, usually black
2. **Bold Borders** - Thick (2-4px) black strokes
3. **High Contrast** - Primary colors against neutral backgrounds

### Color Palette

| Color | Hex | CSS Variable | Usage |
|-------|-----|--------------|-------|
| Black | #000000 | `--neo-black` | Borders, shadows, text |
| White | #FFFFFF | `--neo-white` | Backgrounds, contrast |
| Cream/Beige | #F5F0E6 | `--neo-cream` | Soft background alternative |
| Red | #FF5252 | `--neo-red` | Danger, emphasis |
| Yellow | #FFEB3B | `--neo-yellow` | Highlights, warnings |
| Blue | #2196F3 | `--neo-blue` | Links, primary actions |
| Pink | #FF4081 | `--neo-pink` | Accent, playful |
| Green | #4CAF50 | `--neo-green` | Success states |
| Orange | #FF9800 | `--neo-orange` | CTAs, attention |
| Purple | #9C27B0 | `--neo-purple` | Creative, premium |

**Color Rules:**
- ✅ Bold primaries with high saturation
- ✅ Black and white for maximum contrast
- ✅ Beige/cream for warmth without softness
- ❌ NO gradients (use flat colors only)
- ❌ NO transparency/opacity (stay opaque)

### The Signature Hard Shadow

**THE defining neobrutalist element** - offset shadow with zero blur:

```css
.neo-shadow {
  /* THE neobrutalist shadow formula */
  box-shadow: 4px 4px 0 #000000;
}

.neo-shadow--deep {
  box-shadow: 8px 8px 0 #000000;
}

.neo-shadow--subtle {
  box-shadow: 2px 2px 0 #000000;
}

/* Hover: shadow grows */
.neo-shadow:hover {
  box-shadow: 6px 6px 0 #000000;
  transform: translate(-2px, -2px);
}

/* Active: shadow shrinks (pressed) */
.neo-shadow:active {
  box-shadow: 2px 2px 0 #000000;
  transform: translate(2px, 2px);
}
```

### Bold Border System

```css
.neo-border {
  border: 3px solid #000000;
}

.neo-border--thick {
  border: 4px solid #000000;
}

.neo-border--thin {
  border: 2px solid #000000;
}

/* Colored borders for emphasis */
.neo-border--accent {
  border: 3px solid var(--neo-pink);
}
```

### Typography

| Use | Font Suggestion | Fallback | Style |
|-----|-----------------|----------|-------|
| Headlines | Archivo Black | Impact, sans-serif | Bold, condensed |
| Body | Space Grotesk | Arial, sans-serif | Clean, geometric |
| Accent | Lexend Mega | Trebuchet, sans-serif | Wide, bold |
| Mono | JetBrains Mono | Courier New | Code, retro |
| Display | Bebas Neue | Impact | All-caps impact |

**Typography Rules:**
```css
:root {
  --font-neo-display: 'Archivo Black', 'Impact', sans-serif;
  --font-neo-body: 'Space Grotesk', 'Arial', sans-serif;
  --font-neo-accent: 'Lexend Mega', sans-serif;
  --font-neo-mono: 'JetBrains Mono', 'Courier New', monospace;
}

/* Headlines are BOLD and often oversized */
h1 {
  font-family: var(--font-neo-display);
  font-size: clamp(3rem, 8vw, 6rem);
  line-height: 0.9;
  letter-spacing: -0.02em;
  text-transform: uppercase;
}

/* Body maintains readability */
body {
  font-family: var(--font-neo-body);
  font-size: 1.125rem;
  line-height: 1.6;
}
```

---

## Modern Extrapolations

### SaaS Dashboard: The Gumroad Paradigm

Neobrutalism for SaaS emphasizes **function over flourish**:

```
┌────────────────────────────────────────────────────────┐
│ ██████████████████████████████████████████████████████ │
│ █ DASHBOARD                              [?] [⚙] [👤] █│
│ ██████████████████████████████████████████████████████ │
├────────────────────────────────────────────────────────┤
│ ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│ │ ████████████ │  │ ████████████ │  │ ████████████ │  │
│ │ REVENUE      │  │ CUSTOMERS    │  │ PRODUCTS     │  │
│ │ ════════════ │  │ ════════════ │  │ ════════════ │  │
│ │ $12,450      │  │ 1,234        │  │ 12           │  │
│ │ ↑ 23%        │  │ ↑ 15%        │  │ → 0%         │  │
│ └──────────────┘  └──────────────┘  └──────────────┘  │
│                                                        │
│ ┌────────────────────────────────────────────────────┐│
│ │ RECENT SALES                              [View All]││
│ │ ════════════════════════════════════════════════════││
│ │ ▓ Product A          $49.00         Jan 31, 10:23  ││
│ │ ▓ Product B          $29.00         Jan 31, 09:45  ││
│ │ ▓ Product A          $49.00         Jan 31, 08:12  ││
│ └────────────────────────────────────────────────────┘│
└────────────────────────────────────────────────────────┘
```

**Key patterns:**
- Cards with hard shadows
- Bold section headers
- High-contrast data display
- Black borders on everything
- Flat, solid background colors

### E-Commerce: The Raw Shopping Experience

```css
.neo-product-card {
  background: var(--neo-white);
  border: 3px solid var(--neo-black);
  box-shadow: 6px 6px 0 var(--neo-black);
  padding: 0;
  overflow: hidden;
}

.neo-product-card:hover {
  box-shadow: 8px 8px 0 var(--neo-black);
  transform: translate(-2px, -2px);
}

.neo-product-card__image {
  border-bottom: 3px solid var(--neo-black);
  width: 100%;
  aspect-ratio: 1;
  object-fit: cover;
}

.neo-product-card__content {
  padding: 1rem;
}

.neo-product-card__price {
  font-family: var(--font-neo-display);
  font-size: 1.5rem;
  background: var(--neo-yellow);
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border: 2px solid var(--neo-black);
}

.neo-add-to-cart {
  width: 100%;
  background: var(--neo-black);
  color: var(--neo-white);
  border: 3px solid var(--neo-black);
  padding: 0.75rem;
  font-family: var(--font-neo-display);
  text-transform: uppercase;
  cursor: pointer;
}

.neo-add-to-cart:hover {
  background: var(--neo-pink);
  color: var(--neo-black);
}
```

### Landing Page: Bold First Impressions

```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║  ████████  WE BUILD                                         ║
║  ████████  BOLD                                             ║
║  ████████  PRODUCTS                                         ║
║                                                              ║
║  ┌─────────────────────────────────────────────────────────┐║
║  │                                                         │║
║  │  No more boring SaaS. We create tools that              │║
║  │  stand out, work hard, and make you money.              │║
║  │                                                         │║
║  └─────────────────────────────────────────────────────────┘║
║                                                              ║
║         ╔═══════════════════════════════════════╗           ║
║         ║  → START FREE TRIAL                   ║           ║
║         ╚═══════════════════════════════════════╝           ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Responsive: Bold at Every Size

| Breakpoint | Adjustments |
|------------|-------------|
| Mobile (<640px) | Shadow: 3px 3px, Border: 2px, Font scale down |
| Tablet (640-1024px) | Shadow: 4px 4px, Border: 3px, Standard fonts |
| Desktop (>1024px) | Shadow: 6px 6px, Border: 4px, Oversized headlines |

```css
/* Mobile-first approach */
:root {
  --neo-shadow-size: 3px;
  --neo-border-width: 2px;
}

@media (min-width: 640px) {
  :root {
    --neo-shadow-size: 4px;
    --neo-border-width: 3px;
  }
}

@media (min-width: 1024px) {
  :root {
    --neo-shadow-size: 6px;
    --neo-border-width: 4px;
  }
}

.neo-card {
  border: var(--neo-border-width) solid var(--neo-black);
  box-shadow: var(--neo-shadow-size) var(--neo-shadow-size) 0 var(--neo-black);
}
```

---

## Component Patterns

### Buttons

```css
.neo-button {
  background: var(--neo-white);
  color: var(--neo-black);
  border: 3px solid var(--neo-black);
  box-shadow: 4px 4px 0 var(--neo-black);
  padding: 0.75rem 1.5rem;
  font-family: var(--font-neo-display);
  font-size: 1rem;
  text-transform: uppercase;
  cursor: pointer;
  transition: all 0.1s ease;
}

.neo-button:hover {
  box-shadow: 6px 6px 0 var(--neo-black);
  transform: translate(-2px, -2px);
}

.neo-button:active {
  box-shadow: 2px 2px 0 var(--neo-black);
  transform: translate(2px, 2px);
}

/* Primary variant */
.neo-button--primary {
  background: var(--neo-yellow);
}

/* Danger variant */
.neo-button--danger {
  background: var(--neo-red);
  color: var(--neo-white);
}

/* Ghost variant */
.neo-button--ghost {
  background: transparent;
  box-shadow: none;
}

.neo-button--ghost:hover {
  background: var(--neo-black);
  color: var(--neo-white);
  box-shadow: none;
  transform: none;
}
```

### Cards

```css
.neo-card {
  background: var(--neo-white);
  border: 3px solid var(--neo-black);
  box-shadow: 6px 6px 0 var(--neo-black);
  padding: 1.5rem;
}

.neo-card__header {
  border-bottom: 2px solid var(--neo-black);
  padding-bottom: 1rem;
  margin-bottom: 1rem;
}

.neo-card__title {
  font-family: var(--font-neo-display);
  font-size: 1.25rem;
  text-transform: uppercase;
}

/* Feature card with accent color */
.neo-card--featured {
  background: var(--neo-yellow);
}

/* Highlighted state */
.neo-card--highlight {
  border-color: var(--neo-pink);
  box-shadow: 6px 6px 0 var(--neo-pink);
}
```

### Form Elements

```css
.neo-input {
  background: var(--neo-white);
  border: 3px solid var(--neo-black);
  padding: 0.75rem 1rem;
  font-family: var(--font-neo-body);
  font-size: 1rem;
  width: 100%;
}

.neo-input:focus {
  outline: none;
  box-shadow: 4px 4px 0 var(--neo-black);
}

.neo-input::placeholder {
  color: #888;
}

/* Labels are bold and uppercase */
.neo-label {
  font-family: var(--font-neo-display);
  text-transform: uppercase;
  font-size: 0.875rem;
  margin-bottom: 0.5rem;
  display: block;
}

/* Checkbox/Radio */
.neo-checkbox {
  appearance: none;
  width: 24px;
  height: 24px;
  border: 3px solid var(--neo-black);
  background: var(--neo-white);
  cursor: pointer;
}

.neo-checkbox:checked {
  background: var(--neo-black);
}

.neo-checkbox:checked::after {
  content: '✓';
  color: var(--neo-white);
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
}
```

### Navigation

```css
.neo-nav {
  background: var(--neo-black);
  border-bottom: 4px solid var(--neo-black);
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.neo-nav__logo {
  font-family: var(--font-neo-display);
  font-size: 1.5rem;
  color: var(--neo-white);
  text-transform: uppercase;
}

.neo-nav__links {
  display: flex;
  gap: 1.5rem;
}

.neo-nav__link {
  color: var(--neo-white);
  text-decoration: none;
  font-family: var(--font-neo-body);
  font-weight: 600;
  padding: 0.5rem 0;
  border-bottom: 3px solid transparent;
}

.neo-nav__link:hover {
  border-bottom-color: var(--neo-yellow);
}

.neo-nav__link--active {
  border-bottom-color: var(--neo-pink);
}
```

---

## Anti-Patterns

### Anti-Pattern: Soft Shadows

**Novice thinking**: `box-shadow: 0 4px 6px rgba(0,0,0,0.1)`
**Reality**: Neobrutalism uses HARD shadows with zero blur
**Instead**: `box-shadow: 4px 4px 0 #000000`

### Anti-Pattern: Gradients

**Novice thinking**: `background: linear-gradient(to right, #ff5252, #ffeb3b)`
**Reality**: Neobrutalism is FLAT. No gradients, no blending.
**Instead**: Pick ONE solid color. Embrace the flatness.

### Anti-Pattern: Rounded Corners Everywhere

**Novice thinking**: `border-radius: 16px` on everything
**Reality**: Neobrutalism prefers sharp corners or minimal rounding (4px max)
**Instead**: `border-radius: 0` or `border-radius: 4px` for subtle softening

### Anti-Pattern: Thin Borders

**Novice thinking**: `border: 1px solid #ddd`
**Reality**: Neobrutalist borders are BOLD (3-4px) and BLACK
**Instead**: `border: 3px solid #000000`

### Anti-Pattern: Low Contrast Colors

**Novice thinking**: Subtle pastels on white background
**Reality**: Neobrutalism demands HIGH contrast
**Instead**: Bold primaries (#FF5252, #FFEB3B) on white/black

### Anti-Pattern: Transparency/Opacity

**Novice thinking**: `background: rgba(255,255,255,0.8)`
**Reality**: Neobrutalism is OPAQUE. No see-through elements.
**Instead**: `background: #FFFFFF` (solid, no alpha)

### Anti-Pattern: Hover Blur Effects

**Novice thinking**: `filter: blur(2px)` on hover
**Reality**: Hover states in neobrutalism are physical (translate + shadow change)
**Instead**: `transform: translate(-2px, -2px)` + increased shadow

---

## Quick Decision Tree

```
Is it a container element?
├── Card/Panel? → 3px black border + hard shadow
├── Section? → Full-width, solid background color
├── Modal? → Heavy shadow (8px+), thick border
└── Nav? → Black background or thick bottom border

Is it interactive?
├── Button? → Hard shadow that responds to hover/active
├── Link? → Underline or bottom border, color change on hover
├── Input? → Thick border, shadow on focus
└── Checkbox? → Thick border, solid fill when checked

Is it typography?
├── Headline? → Oversized, bold display font, uppercase optional
├── Body? → Clean geometric sans, good line height
├── Label? → Bold, uppercase, smaller size
└── Code? → Monospace, possibly with background

Is it a status indicator?
├── Success? → Green background or border
├── Error? → Red background or border
├── Warning? → Yellow background or border
└── Info? → Blue background or border
```

---

## CSS Variables Template

```css
:root {
  /* Core palette */
  --neo-black: #000000;
  --neo-white: #FFFFFF;
  --neo-cream: #F5F0E6;

  /* Primary colors */
  --neo-red: #FF5252;
  --neo-yellow: #FFEB3B;
  --neo-blue: #2196F3;
  --neo-pink: #FF4081;
  --neo-green: #4CAF50;
  --neo-orange: #FF9800;
  --neo-purple: #9C27B0;

  /* Typography */
  --font-neo-display: 'Archivo Black', 'Impact', sans-serif;
  --font-neo-body: 'Space Grotesk', 'Arial', sans-serif;
  --font-neo-mono: 'JetBrains Mono', 'Courier New', monospace;

  /* Spacing */
  --neo-spacing-xs: 0.25rem;
  --neo-spacing-sm: 0.5rem;
  --neo-spacing-md: 1rem;
  --neo-spacing-lg: 1.5rem;
  --neo-spacing-xl: 2rem;

  /* Shadows & Borders */
  --neo-shadow-size: 4px;
  --neo-border-width: 3px;
  --neo-shadow: var(--neo-shadow-size) var(--neo-shadow-size) 0 var(--neo-black);
}
```

---

## The Quick Test

If your component has:
- ❌ Any blur in shadows → NOT neobrutalism
- ❌ Any gradients → NOT neobrutalism
- ❌ Transparency/opacity → NOT neobrutalism
- ❌ Thin (1px) borders → NOT neobrutalism
- ❌ Soft/muted colors → NOT neobrutalism
- ❌ Heavy border-radius (16px+) → NOT neobrutalism

It should have:
- ✅ Hard shadows (Xpx Ypx 0 #000)
- ✅ Bold borders (3-4px solid black)
- ✅ High contrast color combinations
- ✅ Flat, solid colors
- ✅ Bold typography
- ✅ Sharp or minimal corners
- ✅ Physical hover/active feedback

---

## Accessibility Considerations

Despite its boldness, neobrutalism can be highly accessible:

1. **High contrast** - Black borders on white/colored backgrounds pass WCAG
2. **Clear focus states** - Shadow/border changes are obvious
3. **Readable typography** - Large, bold text is easy to scan
4. **No motion dependency** - Transforms are enhancers, not requirements

```css
/* Ensure focus is visible */
.neo-button:focus-visible {
  outline: 3px solid var(--neo-blue);
  outline-offset: 2px;
}

/* Reduce motion if preferred */
@media (prefers-reduced-motion: reduce) {
  .neo-button {
    transition: none;
  }

  .neo-button:hover {
    transform: none;
    box-shadow: var(--neo-shadow); /* Keep shadow, skip animation */
  }
}
```

---

## References

- `/references/component-library.md` - Full CSS for all neobrutalist components
- `/references/color-combinations.md` - Tested color pairings with contrast ratios
- `/references/typography-pairings.md` - Font combinations for different contexts
- `/references/real-world-examples.md` - Analysis of Gumroad, Figma, and other implementations

---

## Pairs With

- **web-design-expert** - For brand direction alongside bold style
- **color-contrast-auditor** - Ensure accessibility with bold colors
- **design-system-creator** - For generating full design token systems
- **typography-expert** - For advanced type pairing

---

## Sources

Design research based on:
- [NN/G: Neobrutalism Definition and Best Practices](https://www.nngroup.com/articles/neobrutalism/)
- [Bejamas: Neubrutalism Web Design Trend](https://bejamas.com/blog/neubrutalism-web-design-trend)
- [Onething Design: Neo Brutalism UI Trend](https://www.onething.design/post/neo-brutalism-ui-design-trend)
- [Nestify: Principles of Neo Brutalism](https://nestify.io/blog/neo-brutalism-in-design/)
- [CC Creative: Brutalism vs Neubrutalism](https://www.cccreative.design/blogs/brutalism-vs-neubrutalism-in-ui-design)
