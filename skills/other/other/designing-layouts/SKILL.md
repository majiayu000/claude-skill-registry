---
name: designing-layouts
description: Designs layout systems and responsive interfaces including grid systems, flexbox patterns, sidebar layouts, and responsive breakpoints. Use when structuring app layouts, building responsive designs, or creating complex page structures.
---

# Layout Systems & Responsive Design

## Purpose

This skill provides comprehensive guidance for creating responsive layout systems using modern CSS techniques. It covers grid systems, flexbox patterns, container queries, spacing systems, and mobile-first design strategies to build flexible, accessible interfaces that adapt seamlessly across devices.

## When to Use

Invoke this skill when:
- Building responsive admin dashboards with sidebars and headers
- Creating grid-based layouts for content cards or galleries
- Implementing masonry or Pinterest-style layouts
- Designing split-pane interfaces with resizable panels
- Establishing responsive breakpoint systems
- Structuring application shells with navigation and content areas
- Building mobile-first responsive designs
- Creating flexible spacing and container systems

## Layout Patterns

### Grid Systems

For structured, two-dimensional layouts, use CSS Grid with design tokens.

**12-Column Grid:**
```css
.grid-container {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: var(--grid-gap);
  max-width: var(--container-max-width);
  margin: 0 auto;
  padding: 0 var(--container-padding-x);
}

.col-span-6 { grid-column: span 6; }
.col-span-4 { grid-column: span 4; }
.col-span-3 { grid-column: span 3; }
```

**Auto-Fit Responsive Grid:**
```css
.auto-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(280px, 100%), 1fr));
  gap: var(--grid-gap);
}
```

For complex grid layouts and advanced patterns, see `references/layout-patterns.md`.

### Flexbox Patterns

For one-dimensional layouts and alignment control.

**Holy Grail Layout:**
```css
.holy-grail {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.holy-grail__body {
  flex: 1;
  display: flex;
}

.holy-grail__nav {
  width: var(--sidebar-width);
  flex-shrink: 0;
}

.holy-grail__main {
  flex: 1;
  min-width: 0; /* Prevent overflow */
}

.holy-grail__aside {
  width: var(--sidebar-width);
  flex-shrink: 0;
}
```

For additional flexbox patterns including sticky footer and centering, see `references/css-techniques.md`.

### Container Queries

For component-responsive design that adapts based on container size, not viewport.

```css
.card-container {
  container-type: inline-size;
  container-name: card;
}

@container card (min-width: 400px) {
  .card {
    grid-template-columns: auto 1fr;
    gap: var(--spacing-lg);
  }
}

@container card (min-width: 600px) {
  .card {
    grid-template-columns: 200px 1fr auto;
  }
}
```

Container queries are production-ready in all modern browsers (2025). For detailed usage and fallback strategies, see `references/responsive-strategies.md`.

## Responsive Breakpoints

Use mobile-first approach with semantic breakpoints.

```css
/* Mobile-first breakpoints using design tokens */
@media (min-width: 640px) {  /* sm: Tablet portrait */
  .container { max-width: 640px; }
}

@media (min-width: 768px) {  /* md: Tablet landscape */
  .container { max-width: 768px; }
}

@media (min-width: 1024px) { /* lg: Desktop */
  .container { max-width: 1024px; }
}

@media (min-width: 1280px) { /* xl: Wide desktop */
  .container { max-width: 1280px; }
}

@media (min-width: 1536px) { /* 2xl: Ultra-wide */
  .container { max-width: 1536px; }
}
```

For fluid typography and advanced responsive techniques, see `references/responsive-strategies.md`.

## Spacing Systems

Implement consistent spacing using design tokens.

```css
/* Base unit: 4px or 8px */
:root {
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;
  --spacing-2xl: 48px;
  --spacing-3xl: 64px;
}

/* Apply systematically */
.section { padding: var(--section-spacing) 0; }
.container { padding: 0 var(--container-padding-x); }
.card { padding: var(--spacing-lg); }
.stack > * + * { margin-top: var(--spacing-md); }
```

## CSS Framework Integration

### Tailwind CSS

For utility-first approach with custom configuration:

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      spacing: {
        'xs': 'var(--spacing-xs)',
        'sm': 'var(--spacing-sm)',
        'md': 'var(--spacing-md)',
        'lg': 'var(--spacing-lg)',
        'xl': 'var(--spacing-xl)',
      },
      screens: {
        'sm': '640px',
        'md': '768px',
        'lg': '1024px',
        'xl': '1280px',
        '2xl': '1536px',
      }
    }
  }
}
```

For Tailwind patterns and optimization, see `references/library-guide.md`.

## How to Use

### 1. Define Layout Requirements

Determine layout type and responsive behavior needed.

### 2. Choose Layout Method

- **CSS Grid**: Two-dimensional layouts, complex grids
- **Flexbox**: One-dimensional layouts, alignment
- **Container Queries**: Component-responsive designs

### 3. Implement with Design Tokens

Use design tokens from `skills/design-tokens/` for consistent spacing, breakpoints, and sizing.

### 4. Generate Configurations

For responsive breakpoints:
```bash
node scripts/generate_breakpoints.js --approach mobile-first
```

For fluid typography scale:
```bash
node scripts/calculate_fluid_typography.js --min-vw 320 --max-vw 1920
```

### 5. Validate Accessibility

Check semantic HTML and landmark regions:
```bash
node scripts/validate_layout_accessibility.js path/to/component.tsx
```

### 6. Test Responsiveness

Test across device sizes using responsive preview tools and actual devices.

## Scripts

- `scripts/generate_breakpoints.js` - Generate responsive breakpoint system
- `scripts/calculate_fluid_typography.js` - Calculate fluid typography scales
- `scripts/validate_layout_accessibility.js` - Validate semantic HTML and ARIA landmarks

## References

- `references/layout-patterns.md` - Common layout patterns (sidebar, masonry, split-pane)
- `references/responsive-strategies.md` - Mobile-first design and responsive techniques
- `references/css-techniques.md` - Modern CSS features (Grid, Flexbox, Container Queries)
- `references/accessibility-layouts.md` - Semantic HTML and ARIA landmarks
- `references/library-guide.md` - Framework integration (Tailwind, styled-components)
- `references/performance-optimization.md` - CSS performance and layout thrashing

## Examples

- `examples/admin-layout.tsx` - Complete admin dashboard with sidebar
- `examples/responsive-grid.tsx` - Auto-responsive grid system
- `examples/masonry-layout.tsx` - Pinterest-style masonry grid
- `examples/split-pane.tsx` - Resizable split-pane interface

## Assets

- `assets/breakpoint-config.json` - Standard breakpoint configurations
- `assets/layout-templates.json` - Common layout templates
- `assets/spacing-scale.json` - Spacing system configurations