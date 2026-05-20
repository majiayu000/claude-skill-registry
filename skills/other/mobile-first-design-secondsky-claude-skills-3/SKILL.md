---
name: mobile-first-design
description: Designs responsive interfaces starting from mobile screens with progressive enhancement for larger devices. Use when building responsive websites, optimizing for mobile users, or implementing adaptive layouts.
---

# Mobile-First Design

Design interfaces starting with mobile as the foundation, then enhance for larger screens.

## Breakpoints

| Name | Width | Devices |
|------|-------|---------|
| Mobile | 320-480px | iPhone SE, small Android |
| Tablet | 481-768px | iPad mini |
| Desktop | 769-1024px | iPad Pro, laptops |
| Large | 1025px+ | Desktop monitors |

## Mobile-First CSS

```css
/* Base styles (mobile) */
.container {
  padding: 1rem;
}

.nav {
  display: none; /* Hidden on mobile */
}

.nav-toggle {
  display: block; /* Hamburger visible */
}

/* Tablet and up */
@media (min-width: 768px) {
  .container {
    padding: 2rem;
    max-width: 720px;
    margin: 0 auto;
  }

  .nav {
    display: flex;
  }

  .nav-toggle {
    display: none;
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .container {
    max-width: 960px;
  }
}
```

## Touch-Friendly Design

```css
/* Minimum touch target: 48x48px */
.button {
  min-height: 48px;
  min-width: 48px;
  padding: 12px 24px;
}

/* Adequate spacing */
.list-item {
  padding: 16px;
  margin-bottom: 8px;
}
```

## Performance Requirements

| Metric | Target |
|--------|--------|
| First Contentful Paint | <3s on 3G |
| JS bundle | <100KB gzipped |
| Total page weight | <500KB |

## Progressive Enhancement

```html
<!-- Layer 1: Semantic HTML (works without CSS/JS) -->
<nav>
  <a href="/home">Home</a>
  <a href="/about">About</a>
</nav>

<!-- Layer 2: CSS enhances appearance -->
<!-- Layer 3: JS adds interactivity -->
```

## Best Practices

- Start design at 320px width
- Use relative units (rem, %, vw)
- Test on real devices
- Optimize images for mobile
- Minimize JavaScript for initial load
- Ensure readable text without zooming
