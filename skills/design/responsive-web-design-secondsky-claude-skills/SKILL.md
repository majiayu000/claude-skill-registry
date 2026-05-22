---
name: responsive-web-design
description: Builds adaptive web interfaces using Flexbox, CSS Grid, and media queries with a mobile-first approach. Use when creating multi-device layouts, implementing flexible UI systems, or ensuring cross-browser compatibility.
---

# Responsive Web Design

Build adaptive interfaces using modern CSS techniques for all screen sizes.

## Mobile-First Media Queries

```css
/* Base: Mobile (320px+) */
.container {
  padding: 1rem;
}

/* Tablet (640px+) */
@media (min-width: 640px) {
  .container {
    padding: 2rem;
    max-width: 640px;
    margin: 0 auto;
  }
}

/* Desktop (1024px+) */
@media (min-width: 1024px) {
  .container {
    max-width: 1024px;
  }
}
```

## Flexible Grid

```css
.grid {
  display: grid;
  gap: 1rem;
  grid-template-columns: 1fr; /* Mobile: single column */
}

@media (min-width: 640px) {
  .grid {
    grid-template-columns: repeat(2, 1fr); /* Tablet: 2 columns */
  }
}

@media (min-width: 1024px) {
  .grid {
    grid-template-columns: repeat(3, 1fr); /* Desktop: 3 columns */
  }
}
```

## Fluid Typography

```css
/* Scales smoothly between breakpoints */
h1 {
  font-size: clamp(1.5rem, 4vw, 3rem);
}

p {
  font-size: clamp(1rem, 2vw, 1.25rem);
}
```

## Responsive Images

```css
img {
  max-width: 100%;
  height: auto;
}

.hero-image {
  width: 100%;
  aspect-ratio: 16 / 9;
  object-fit: cover;
}
```

## Flexbox Navigation

```css
.nav {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

@media (min-width: 768px) {
  .nav {
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
  }
}
```

## Best Practices

- Start with mobile styles first
- Use flexible units (%, rem, vw)
- Test on real devices
- Ensure minimum 48px touch targets
- Maintain readable line lengths (45-75 chars)
- Use CSS Grid for 2D layouts, Flexbox for 1D

## Resources

- [MDN Flexbox Guide](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Flexible_Box_Layout)
- [MDN Grid Guide](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Grid_Layout)
