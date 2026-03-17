---
name: generic-static-design-system
description: Complete design system reference for static HTML/CSS/JS sites. Covers colors, typography, component patterns, animations, and accessibility. Use when implementing UI, choosing colors, or ensuring brand consistency.
---

# Static Site Design System

Design system patterns for minimalist static sites (pure HTML/CSS/JS).

**Extends:** [Generic Design System](../generic-design-system/SKILL.md) - Read base skill for color theory, typography scale, spacing system, and component states.

## Pure CSS Approach

No preprocessors, no Tailwind, no build tools. Just CSS.

### CSS Custom Properties

```css
:root {
  /* Brand colors - keep palette minimal */
  --bg-primary: #000000;
  --text-primary: #ffffff;
  --accent: #00ff00;

  /* Spacing */
  --space-sm: 0.5rem;
  --space-md: 1rem;
  --space-lg: 2rem;

  /* Timing */
  --transition-fast: 0.15s;
  --transition-base: 0.3s;
}
```

### System Font Stack (No Web Fonts)

```css
/* System fonts = zero load time */
body {
  font-family:
    -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

code {
  font-family: "SF Mono", Monaco, "Courier New", monospace;
}
```

### Responsive Typography with clamp()

```css
/* Fluid sizing, no media queries needed */
h1 {
  font-size: clamp(1.5rem, 5vw, 2.5rem);
}

body {
  font-size: clamp(1rem, 3vw, 1.125rem);
}
```

## CSS-Only Animations

### Keyframe Animations

```css
@keyframes pulse {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.pulse {
  animation: pulse 2s ease-in-out infinite;
}
```

### Transition Patterns

```css
/* Hover effect - GPU accelerated */
.link {
  transition:
    transform var(--transition-base) ease,
    color var(--transition-base) ease;
}

.link:hover {
  transform: translateY(-2px);
  color: var(--accent);
}
```

### Staggered Animation with nth-child

```css
.menu a {
  opacity: 0;
  transform: translateY(-10px);
  transition: all 0.3s ease;
}

.menu.visible a {
  opacity: 1;
  transform: translateY(0);
}
.menu.visible a:nth-child(1) {
  transition-delay: 0.1s;
}
.menu.visible a:nth-child(2) {
  transition-delay: 0.2s;
}
.menu.visible a:nth-child(3) {
  transition-delay: 0.3s;
}
```

## CSS-Only Interactive Patterns

### Hidden/Visible Toggle

```css
.hidden {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s ease;
}

.visible {
  max-height: 300px; /* Must be > content height */
}
```

### Icon Rotation

```css
.arrow {
  transition: transform 0.3s ease;
}

.rotated .arrow {
  transform: rotate(180deg);
}
```

### Focus States

```css
a:focus-visible,
button:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}
```

## Component Patterns (No JS)

### Accessible Button

```html
<button class="btn" type="button">Click Me</button>
```

```css
.btn {
  padding: var(--space-sm) var(--space-md);
  background: transparent;
  border: 1px solid var(--text-primary);
  color: var(--text-primary);
  cursor: pointer;
  transition: all var(--transition-base) ease;
}

.btn:hover {
  background: var(--accent);
  border-color: var(--accent);
  color: var(--bg-primary);
}
```

### Navigation

```html
<nav>
  <a href="#section1">Section 1</a>
  <a href="#section2">Section 2</a>
</nav>
```

```css
nav a {
  padding: var(--space-sm);
  text-decoration: none;
  color: var(--text-primary);
}

nav a:hover {
  color: var(--accent);
}
```

## Performance Targets

| File  | Max Size |
| ----- | -------- |
| HTML  | < 5KB    |
| CSS   | < 10KB   |
| JS    | < 5KB    |
| Total | < 50KB   |

| Lighthouse     | Target |
| -------------- | ------ |
| Performance    | 95+    |
| Accessibility  | 90+    |
| Best Practices | 100    |

## See Also

- [Generic Design System](../generic-design-system/SKILL.md) - Token organization, spacing
- [Design Patterns](../_shared/DESIGN_PATTERNS.md) - Core patterns
- [UX Principles](../_shared/UX_PRINCIPLES.md) - Visual hierarchy
