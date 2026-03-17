---
name: frontend-css-patterns
description: Framework-agnostic CSS patterns for typography, color, motion, and spatial composition.
allowed-tools: []
---

# Frontend CSS Patterns

Implementation patterns for distinctive visual design.

## Typography

```css
/* AVOID: Generic defaults */
font-family: Inter, system-ui, sans-serif;

/* PREFER: Distinctive pairings */
--font-display: 'Clash Display', 'Space Grotesk', sans-serif;
--font-body: 'Satoshi', 'General Sans', sans-serif;

/* Specific moods */
--font-luxury: 'Cormorant Garamond', serif;
--font-brutalist: 'JetBrains Mono', monospace;
--font-playful: 'Fredoka', 'Quicksand', sans-serif;
```

**Typography scale:**

```css
:root {
  --text-hero: clamp(3rem, 10vw, 8rem);
  --text-display: clamp(2rem, 5vw, 4rem);
  --text-heading: clamp(1.5rem, 3vw, 2.5rem);
  --text-body: clamp(1rem, 1.5vw, 1.125rem);
}
```

## Color & Theme

```css
:root {
  /* Dominant + sharp accent */
  --color-bg: #0a0a0a;
  --color-fg: #fafafa;
  --color-accent: #ff3366;
  --color-accent-muted: #ff336633;
}
```

Commit to: high contrast, limited palette (3-4 colors), accent colors that pop.

## Motion

**Focus on high-impact moments over scattered micro-interactions:**

```css
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.reveal {
  animation: fadeInUp 0.6s ease-out forwards;
}

.reveal:nth-child(1) { animation-delay: 0.1s; }
.reveal:nth-child(2) { animation-delay: 0.2s; }
```

Focus on: page load sequences, scroll-triggered reveals, state transitions.

## Spatial Composition

**Break the grid:**

- **Asymmetry**: Offset elements intentionally
- **Overlap**: Layer elements for depth
- **Diagonal flow**: Guide the eye dynamically
- **Whitespace**: Let content breathe

```css
.hero-image {
  position: relative;
  top: -5vh;      /* Overlap the header */
  right: -2rem;   /* Extend past container */
}
```

## Visual Details

```css
/* Gradient overlay */
.card::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, transparent 40%, rgba(255,255,255,0.05));
  pointer-events: none;
}

/* Glow effects */
.accent-element {
  box-shadow: 0 0 20px var(--color-accent-muted), 0 0 40px var(--color-accent-muted);
}
```

## Tailwind Customization

**Customize the theme—don't use defaults:**

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      fontFamily: { display: ['Clash Display', 'sans-serif'] },
      colors: { brand: { DEFAULT: '#ff3366', muted: 'rgba(255, 51, 102, 0.2)' } },
    },
  },
}
```
