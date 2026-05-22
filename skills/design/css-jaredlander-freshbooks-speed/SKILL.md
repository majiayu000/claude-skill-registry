---
name: css
description: Expert-level CSS development with modern features and best practices. Use when asked to (1) write or debug CSS, (2) implement layouts with flexbox, grid, or container queries, (3) create animations and transitions, (4) optimize CSS performance, (5) work with CSS preprocessors or CSS-in-JS, (6) implement responsive design, or when phrases like "style", "CSS", "stylesheet", "design", "layout", "animation" appear.
---

# Expert CSS Development

Write modern, performant, maintainable CSS following current best practices with deep knowledge of browser compatibility and CSS specifications.

## Documentation Lookup with context7

**IMPORTANT**: When you need to look up CSS properties, syntax, browser compatibility, or spec details, use the context7 MCP tool to query MDN and other documentation sources.

### How to use context7 for CSS

```bash
# Look up CSS properties
context7 "CSS flexbox properties"
context7 "CSS grid-template-areas syntax"
context7 "CSS custom properties inheritance"

# Check browser compatibility
context7 "CSS container queries browser support"
context7 "CSS :has() selector compatibility"

# Find best practices
context7 "CSS performance optimization"
context7 "CSS naming conventions BEM"

# Explore modern features
context7 "CSS cascade layers @layer"
context7 "CSS subgrid"
context7 "CSS color-mix function"
```

**Use context7 whenever**:
- You're unsure about exact syntax or property values
- You need to verify browser support for a feature
- You want to find the most current best practices
- You're working with cutting-edge CSS features
- You need to understand spec details or edge cases

## Core Principles

1. **Mobile-first responsive design** - Start with mobile layout, scale up
2. **Progressive enhancement** - Core functionality works everywhere, enhancements where supported
3. **CSS cascade and specificity** - Understand and leverage, don't fight against it
4. **Performance matters** - Minimize reflows, optimize animations, reduce file size
5. **Maintainability** - Use consistent naming, logical organization, clear documentation

## Modern Layout Techniques

### Flexbox for One-Dimensional Layouts

```css
/* Common flex patterns */
.container {
  display: flex;
  gap: 1rem; /* Prefer gap over margins for spacing */
}

/* Center content */
.centered {
  display: flex;
  justify-content: center;
  align-items: center;
}

/* Responsive flex wrapping */
.flex-wrap {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.flex-wrap > * {
  flex: 1 1 300px; /* Grow, shrink, basis */
}

/* Common flex utilities */
.flex-1 { flex: 1; }
.flex-none { flex: none; }
.flex-auto { flex: auto; }
```

### Grid for Two-Dimensional Layouts

```css
/* Responsive grid with auto-fit */
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}

/* Named grid areas for semantic layouts */
.layout {
  display: grid;
  grid-template-areas:
    "header header"
    "sidebar main"
    "footer footer";
  grid-template-columns: 250px 1fr;
  grid-template-rows: auto 1fr auto;
  min-height: 100vh;
}

.header { grid-area: header; }
.sidebar { grid-area: sidebar; }
.main { grid-area: main; }
.footer { grid-area: footer; }

/* Dense packing for masonry-like layouts */
.masonry {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  grid-auto-flow: dense;
  gap: 1rem;
}
```

### Container Queries (Modern Alternative to Media Queries)

```css
/* Container query setup */
.card-container {
  container-type: inline-size;
  container-name: card;
}

/* Query the container, not the viewport */
@container card (min-width: 400px) {
  .card {
    display: grid;
    grid-template-columns: 150px 1fr;
  }
}

@container card (min-width: 600px) {
  .card {
    grid-template-columns: 200px 1fr;
  }
}
```

## Modern CSS Features

### Custom Properties (CSS Variables)

```css
:root {
  /* Color system */
  --color-primary: #0066cc;
  --color-primary-dark: #004499;
  --color-surface: #ffffff;
  --color-text: #1a1a1a;
  
  /* Spacing scale */
  --space-xs: 0.25rem;
  --space-sm: 0.5rem;
  --space-md: 1rem;
  --space-lg: 2rem;
  --space-xl: 4rem;
  
  /* Typography */
  --font-sans: system-ui, -apple-system, sans-serif;
  --font-mono: 'Fira Code', monospace;
  
  /* Dark mode using data attribute */
  --bg: var(--color-surface);
  --fg: var(--color-text);
}

[data-theme="dark"] {
  --color-surface: #1a1a1a;
  --color-text: #e5e5e5;
}

/* Using custom properties */
.button {
  background: var(--color-primary);
  padding: var(--space-sm) var(--space-md);
  font-family: var(--font-sans);
}
```

### Cascade Layers (@layer)

```css
/* Define layer order - lowest specificity first */
@layer reset, base, components, utilities;

@layer reset {
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }
}

@layer base {
  body {
    font-family: system-ui, sans-serif;
    line-height: 1.5;
  }
}

@layer components {
  .button {
    padding: 0.5rem 1rem;
    border-radius: 0.25rem;
  }
}

@layer utilities {
  .text-center { text-align: center; }
  .hidden { display: none; }
}
```

### Modern Selectors

```css
/* :is() for grouping (no specificity increase) */
:is(h1, h2, h3) {
  font-weight: 700;
  line-height: 1.2;
}

/* :where() for zero specificity */
:where(.card, .panel) > :where(h2, h3) {
  margin-top: 0;
}

/* :has() for parent selection */
.card:has(img) {
  display: grid;
  grid-template-columns: 200px 1fr;
}

.form:has(:invalid) .submit-button {
  opacity: 0.5;
  pointer-events: none;
}

/* Logical properties for internationalization */
.element {
  margin-inline-start: 1rem; /* Instead of margin-left */
  padding-block: 2rem; /* Instead of padding-top and padding-bottom */
  border-inline-end: 1px solid; /* Instead of border-right */
}
```

## Animations and Transitions

### Performant Animations

```css
/* Only animate transform and opacity for 60fps */
.smooth-animation {
  /* Hint to browser for optimization */
  will-change: transform;
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.smooth-animation:hover {
  transform: translateY(-4px);
}

/* Remove will-change after animation */
.smooth-animation:not(:hover) {
  will-change: auto;
}

/* Complex keyframe animations */
@keyframes slideInFade {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-in {
  animation: slideInFade 0.4s ease-out;
}
```

### View Transitions API

```css
/* Smooth page transitions */
::view-transition-old(root),
::view-transition-new(root) {
  animation-duration: 0.3s;
}

/* Named transitions for specific elements */
.hero {
  view-transition-name: hero-image;
}

::view-transition-old(hero-image),
::view-transition-new(hero-image) {
  animation-duration: 0.5s;
}
```

### Scroll-Driven Animations

```css
/* Animate on scroll progress */
@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(50px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.scroll-reveal {
  animation: fade-in linear;
  animation-timeline: view();
  animation-range: entry 0% cover 30%;
}
```

## Responsive Design Patterns

### Modern Media Query Strategy

```css
/* Mobile-first approach */
.component {
  /* Base mobile styles */
  padding: 1rem;
}

/* Tablet */
@media (min-width: 768px) {
  .component {
    padding: 2rem;
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .component {
    padding: 3rem;
  }
}

/* Wide desktop */
@media (min-width: 1440px) {
  .component {
    padding: 4rem;
  }
}

/* Prefer reduced motion */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

/* Dark mode preference */
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #1a1a1a;
    --fg: #e5e5e5;
  }
}
```

### Fluid Typography

```css
/* Clamp for responsive font sizes */
h1 {
  font-size: clamp(2rem, 4vw + 1rem, 4rem);
}

body {
  font-size: clamp(1rem, 0.5vw + 0.875rem, 1.125rem);
}

/* Or using custom properties */
:root {
  --fluid-min-width: 320;
  --fluid-max-width: 1140;
  --fluid-min-size: 16;
  --fluid-max-size: 20;
  
  --fluid-size: calc(
    (var(--fluid-min-size) * 1px) +
    (var(--fluid-max-size) - var(--fluid-min-size)) *
    ((100vw - (var(--fluid-min-width) * 1px)) /
    (var(--fluid-max-width) - var(--fluid-min-width)))
  );
}

body {
  font-size: clamp(
    var(--fluid-min-size) * 1px,
    var(--fluid-size),
    var(--fluid-max-size) * 1px
  );
}
```

## Performance Optimization

### Critical Performance Rules

```css
/* 1. Avoid expensive properties */
.avoid {
  box-shadow: ...; /* OK, GPU accelerated */
  filter: ...; /* Expensive, use sparingly */
}

/* 2. Use containment for isolated components */
.card {
  contain: layout style paint;
  /* Tells browser this element's styles won't affect others */
}

.isolated-component {
  content-visibility: auto; /* Skip rendering offscreen elements */
}

/* 3. Optimize selectors - specificity vs performance */
/* Fast ✅ */
.button { }
.nav-item { }

/* Slower ❌ */
div.container ul li a.link { }
[class*="btn-"] { }
```

### CSS Loading Strategies

```html
<!-- Critical CSS inline in <head> -->
<style>
  /* Above-the-fold styles */
</style>

<!-- Non-critical CSS with media query trick -->
<link rel="stylesheet" href="styles.css" media="print" onload="this.media='all'">

<!-- Preload for faster loading -->
<link rel="preload" href="fonts.woff2" as="font" type="font/woff2" crossorigin>
```

## Naming Conventions and Organization

### BEM (Block Element Modifier)

```css
/* Block */
.card { }

/* Element - part of block */
.card__title { }
.card__body { }
.card__footer { }

/* Modifier - variation of block */
.card--featured { }
.card--large { }
.card__title--primary { }
```

### Utility-First (Tailwind-style)

```css
/* Spacing utilities */
.p-4 { padding: 1rem; }
.px-4 { padding-left: 1rem; padding-right: 1rem; }
.mt-2 { margin-top: 0.5rem; }

/* Layout utilities */
.flex { display: flex; }
.grid { display: grid; }
.hidden { display: none; }

/* Typography utilities */
.text-lg { font-size: 1.125rem; }
.font-bold { font-weight: 700; }
.text-center { text-align: center; }
```

### File Organization

```
styles/
├── base/
│   ├── reset.css
│   ├── typography.css
│   └── utilities.css
├── components/
│   ├── button.css
│   ├── card.css
│   └── nav.css
├── layout/
│   ├── grid.css
│   ├── header.css
│   └── footer.css
├── themes/
│   ├── light.css
│   └── dark.css
└── main.css (imports all)
```

## Modern Color Functions

```css
:root {
  /* Modern color functions */
  --primary: oklch(60% 0.2 250); /* Perceptually uniform */
  --surface: color-mix(in oklch, var(--primary) 10%, white);
  
  /* Relative colors */
  --primary-light: oklch(from var(--primary) calc(l + 20%) c h);
  --primary-dark: oklch(from var(--primary) calc(l - 20%) c h);
  
  /* Color contrast for accessibility */
  --text-color: color-contrast(
    var(--surface) vs black, white
  );
}
```

## Browser Compatibility Strategies

### Feature Queries (@supports)

```css
/* Fallback for older browsers */
.grid {
  display: flex;
  flex-wrap: wrap;
}

/* Enhanced for modern browsers */
@supports (display: grid) {
  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  }
}

/* Progressive enhancement */
.button {
  background: blue;
}

@supports (backdrop-filter: blur(10px)) {
  .button {
    background: rgba(0, 0, 255, 0.8);
    backdrop-filter: blur(10px);
  }
}
```

## Common Patterns and Solutions

### Aspect Ratio

```css
/* Modern way */
.video {
  aspect-ratio: 16 / 9;
}

/* For images */
img {
  aspect-ratio: 16 / 9;
  object-fit: cover;
}
```

### Truncation

```css
/* Single line */
.truncate {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* Multiple lines */
.line-clamp {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
```

### Smooth Scrolling

```css
html {
  scroll-behavior: smooth;
}

/* Scroll snapping */
.carousel {
  scroll-snap-type: x mandatory;
  overflow-x: auto;
}

.carousel > * {
  scroll-snap-align: start;
}
```

## Accessibility Considerations

```css
/* Focus visible for keyboard users only */
:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

/* Hide visually but keep for screen readers */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}

/* Respect user preferences */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

@media (prefers-contrast: high) {
  .button {
    border: 2px solid currentColor;
  }
}
```

## CSS Reset / Normalize

```css
/* Modern CSS reset */
*,
*::before,
*::after {
  box-sizing: border-box;
  margin: 0;
}

html {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

body {
  min-height: 100vh;
  line-height: 1.5;
}

img,
picture,
video,
canvas,
svg {
  display: block;
  max-width: 100%;
}

input,
button,
textarea,
select {
  font: inherit;
}

p,
h1,
h2,
h3,
h4,
h5,
h6 {
  overflow-wrap: break-word;
}
```

## Quick Reference

See [references/](references/) for detailed guides on:
- Modern layout techniques (flexbox, grid, container queries)
- Animation and transition best practices
- Performance optimization strategies
- Responsive design patterns
- Accessibility guidelines

## Workflow

1. **Start with context7** - Look up unfamiliar properties or modern features
2. **Mobile-first** - Design and code for mobile, enhance for larger screens
3. **Use feature queries** - Progressive enhancement with @supports
4. **Test across browsers** - Verify in Chrome, Firefox, Safari, Edge
5. **Validate** - Use W3C CSS Validator for standard compliance
6. **Optimize** - Minimize reflows, use contain, leverage GPU acceleration
7. **Document** - Comment complex calculations, magic numbers, browser hacks

## Tools and Resources

- **context7** - Primary documentation lookup tool
- **MDN Web Docs** - Comprehensive CSS reference (via context7)
- **Can I Use** - Browser compatibility data (via context7)
- **CSS Specifications** - W3C specs for detailed behavior (via context7)
- **PostCSS** - Transform CSS with JavaScript plugins
- **CSS Modules** - Scoped CSS for components
- **Sass/SCSS** - CSS preprocessor with variables, nesting, mixins
- **Lightning CSS** - Fast CSS parser, transformer, and minifier

---

**Remember**: When in doubt about any CSS feature, syntax, or browser support, use context7 to look it up in real-time documentation.
