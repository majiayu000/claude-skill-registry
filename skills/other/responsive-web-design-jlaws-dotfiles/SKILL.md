---
name: responsive-web-design
description: "Use when implementing responsive layouts, fluid typography, responsive images, or choosing between container queries and media queries."
---

# Responsive Web Design

## Container Queries vs Media Queries

| Feature | Media Queries | Container Queries |
|---|---|---|
| Based on | Viewport size | Parent container size |
| Use case | Page-level layout | Component-level layout |
| Nesting | N/A | Supported |
| Browser support | Universal | Modern browsers (2023+) |

**Default**: Media queries for page layout (nav, sidebar). Container queries for reusable components that render in different contexts.

```css
/* Container query setup */
.card-wrapper {
  container-type: inline-size;
  container-name: card;
}

@container card (min-width: 400px) {
  .card { flex-direction: row; }
  .card-image { width: 40%; }
}

@container card (max-width: 399px) {
  .card { flex-direction: column; }
  .card-image { width: 100%; }
}
```

## Fluid Typography

```css
/* clamp(min, preferred, max) — no breakpoints needed */
:root {
  --text-sm: clamp(0.8rem, 0.17vw + 0.76rem, 0.89rem);
  --text-base: clamp(1rem, 0.34vw + 0.91rem, 1.19rem);
  --text-lg: clamp(1.25rem, 0.61vw + 1.1rem, 1.58rem);
  --text-xl: clamp(1.56rem, 1vw + 1.31rem, 2.11rem);
  --text-2xl: clamp(1.95rem, 1.56vw + 1.56rem, 2.81rem);
  --text-3xl: clamp(2.44rem, 2.38vw + 1.85rem, 3.75rem);
}

h1 { font-size: var(--text-3xl); }
p { font-size: var(--text-base); }
```

## Mobile-First Strategy

Base styles = mobile. Layer up with `min-width` breakpoints: 640px (sm), 1024px (md), 1280px (lg).

## Responsive Images

Use `srcset` + `sizes` for resolution switching, `<picture>` + `<source media>` for art direction. Always `loading="lazy"` below fold.

## CSS Grid Patterns

Use `repeat(auto-fit, minmax(250px, 1fr))` for breakpoint-free responsive grids. Sidebar: fixed + `minmax(0, 1fr)` behind a media query.

## Gotchas

- **Viewport units on mobile**: `100vh` includes browser chrome; use `100dvh` (dynamic viewport height) instead
- **Container query support**: Baseline 2023 -- add `@supports (container-type: inline-size)` fallback for older browsers
- **Touch targets**: Minimum 44x44px (WCAG 2.5.5); use `min-height: 44px; min-width: 44px` on interactive elements
- **Horizontal scroll**: Always test with `overflow-x: hidden` on body during dev to catch overflow; use `max-width: 100%` on images/videos
- **Font loading shift**: Use `font-display: swap` and `size-adjust` to minimize CLS from web font loading

## Cross-References

- **frontend:tailwind-design-system** -- Tailwind responsive utilities, breakpoint config, container queries plugin
- **frontend:accessibility-testing** -- Touch target compliance, responsive WCAG requirements
