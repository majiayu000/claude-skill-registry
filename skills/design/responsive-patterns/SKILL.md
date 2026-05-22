---
name: responsive-patterns
description: Responsive design with Container Queries, fluid typography, cqi/cqb units, and mobile-first patterns for React applications
tags: [responsive, container-queries, fluid-typography, mobile-first, css-grid, clamp, cqi, breakpoints]
context: fork
agent: frontend-ui-developer
version: 1.0.0
author: SkillForge
user-invocable: false
---

# Responsive Patterns

Modern responsive design patterns using Container Queries, fluid typography, and mobile-first strategies for React applications (2026 best practices).

## When to Use

- Building reusable components that adapt to their container
- Implementing fluid typography that scales smoothly
- Creating responsive layouts without media query overload
- Building design system components for multiple contexts
- Optimizing for variable container sizes (sidebars, modals, grids)

## Core Concepts

### Container Queries vs Media Queries

| Feature | Media Queries | Container Queries |
|---------|---------------|-------------------|
| Responds to | Viewport size | Container size |
| Component reuse | Context-dependent | Truly portable |
| Browser support | Universal | Baseline 2023+ |
| Use case | Page layouts | Component layouts |

## CSS Patterns

### 1. Container Query Basics

```css
/* Define a query container */
.card-container {
  container-type: inline-size;
  container-name: card;
}

/* Style based on container width */
@container card (min-width: 400px) {
  .card {
    display: grid;
    grid-template-columns: 200px 1fr;
  }
}

@container card (max-width: 399px) {
  .card {
    display: flex;
    flex-direction: column;
  }
}
```

### 2. Container Query Units (cqi, cqb)

```css
/* Use cqi (container query inline) over cqw */
.card-title {
  /* 5% of container's inline size */
  font-size: clamp(1rem, 5cqi, 2rem);
}

.card-content {
  /* Responsive padding based on container */
  padding: 2cqi;
}

/* cqb for block dimension (height-aware containers) */
.sidebar-item {
  height: 10cqb;
}
```

### 3. Fluid Typography with clamp()

```css
/* Accessible fluid typography */
:root {
  /* Base font respects user preferences (rem) */
  --font-size-base: 1rem;

  /* Fluid scale with min/max bounds */
  --font-size-sm: clamp(0.875rem, 0.8rem + 0.25vw, 1rem);
  --font-size-md: clamp(1rem, 0.9rem + 0.5vw, 1.25rem);
  --font-size-lg: clamp(1.25rem, 1rem + 1vw, 2rem);
  --font-size-xl: clamp(1.5rem, 1rem + 2vw, 3rem);
  --font-size-2xl: clamp(2rem, 1rem + 3vw, 4rem);
}

h1 { font-size: var(--font-size-2xl); }
h2 { font-size: var(--font-size-xl); }
h3 { font-size: var(--font-size-lg); }
p { font-size: var(--font-size-md); }
small { font-size: var(--font-size-sm); }
```

### 4. Container-Based Fluid Typography

```css
/* For component-scoped fluid text */
.widget {
  container-type: inline-size;
}

.widget-title {
  /* Fluid within container, respecting user rem */
  font-size: clamp(1rem, 0.5rem + 5cqi, 2rem);
}

.widget-body {
  font-size: clamp(0.875rem, 0.5rem + 3cqi, 1.125rem);
}
```

### 5. Mobile-First Breakpoints

```css
/* Mobile-first: start small, add complexity */
.layout {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

/* Tablet and up */
@media (min-width: 768px) {
  .layout {
    flex-direction: row;
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .layout {
    max-width: 1200px;
    margin-inline: auto;
  }
}
```

### 6. CSS Grid Responsive Patterns

```css
/* Auto-fit grid (fills available space) */
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
}

/* Auto-fill grid (maintains minimum columns) */
.icon-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  gap: 1rem;
}

/* Subgrid for nested alignment */
.card {
  display: grid;
  grid-template-rows: subgrid;
  grid-row: span 3;
}
```

### 7. Container Scroll-Queries (Chrome 126+)

```css
/* Query based on scroll state */
.scroll-container {
  container-type: scroll-state;
  container-name: scroller;
}

@container scroller scroll-state(scrollable: top) {
  .scroll-indicator-top {
    opacity: 0;
  }
}

@container scroller scroll-state(scrollable: bottom) {
  .scroll-indicator-bottom {
    opacity: 0;
  }
}
```

## React Patterns

### Responsive Component with Container Queries

```tsx
import { cn } from '@/lib/utils';

interface CardProps {
  title: string;
  description: string;
  image: string;
}

export function ResponsiveCard({ title, description, image }: CardProps) {
  return (
    <div className="@container">
      <article className={cn(
        "flex flex-col gap-4",
        "@md:flex-row @md:gap-6" // Container query breakpoints
      )}>
        <img
          src={image}
          alt=""
          className="w-full @md:w-48 aspect-video object-cover rounded-lg"
        />
        <div className="flex flex-col gap-2">
          <h3 className="text-[clamp(1rem,0.5rem+3cqi,1.5rem)] font-semibold">
            {title}
          </h3>
          <p className="text-[clamp(0.875rem,0.5rem+2cqi,1rem)] text-muted-foreground">
            {description}
          </p>
        </div>
      </article>
    </div>
  );
}
```

### Tailwind CSS Container Queries

```tsx
// @container enables container query variants (@sm, @md, @lg, etc.)
<div className="@container">
  <div className="flex flex-col @lg:flex-row @xl:gap-8">
    <div className="@sm:p-4 @md:p-6 @lg:p-8">
      Content adapts to container
    </div>
  </div>
</div>
```

### useContainerQuery Hook

```tsx
import { useRef, useState, useEffect } from 'react';

function useContainerQuery(breakpoint: number) {
  const ref = useRef<HTMLDivElement>(null);
  const [isAbove, setIsAbove] = useState(false);

  useEffect(() => {
    const element = ref.current;
    if (!element) return;

    const observer = new ResizeObserver(([entry]) => {
      setIsAbove(entry.contentRect.width >= breakpoint);
    });

    observer.observe(element);
    return () => observer.disconnect();
  }, [breakpoint]);

  return [ref, isAbove] as const;
}

// Usage
function AdaptiveCard() {
  const [containerRef, isWide] = useContainerQuery(400);

  return (
    <div ref={containerRef}>
      {isWide ? <HorizontalLayout /> : <VerticalLayout />}
    </div>
  );
}
```

### Responsive Images Pattern

```tsx
function ResponsiveImage({
  src,
  alt,
  sizes = "(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"
}: {
  src: string;
  alt: string;
  sizes?: string;
}) {
  return (
    <picture>
      {/* Art direction with different crops */}
      <source
        media="(max-width: 640px)"
        srcSet={`${src}?w=640&aspect=1:1`}
      />
      <source
        media="(max-width: 1024px)"
        srcSet={`${src}?w=800&aspect=4:3`}
      />
      <img
        src={`${src}?w=1200`}
        alt={alt}
        sizes={sizes}
        loading="lazy"
        decoding="async"
        className="w-full h-auto object-cover"
      />
    </picture>
  );
}
```

## Accessibility Considerations

```css
/* IMPORTANT: Always include rem in fluid typography */
/* This ensures user font preferences are respected */

/* ❌ WRONG: Viewport-only ignores user preferences */
font-size: 5vw;

/* ✅ CORRECT: Include rem to respect user settings */
font-size: clamp(1rem, 0.5rem + 2vw, 2rem);

/* User zooming must still work */
@media (min-width: 768px) {
  /* Use em/rem, not px, for breakpoints in ideal world */
  /* (browsers still use px, but consider user zoom) */
}
```

## Anti-Patterns (FORBIDDEN)

```css
/* ❌ NEVER: Use only viewport units for text */
.title {
  font-size: 5vw; /* Ignores user font preferences! */
}

/* ❌ NEVER: Use cqw/cqh (use cqi/cqb instead) */
.card {
  padding: 5cqw; /* cqw = container width, not logical */
}
/* ✅ CORRECT: Use logical units */
.card {
  padding: 5cqi; /* Container inline = logical direction */
}

/* ❌ NEVER: Container queries without container-type */
@container (min-width: 400px) {
  /* Won't work without container-type on parent! */
}

/* ❌ NEVER: Desktop-first media queries */
.element {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
}
@media (max-width: 768px) {
  .element {
    grid-template-columns: 1fr; /* Overriding = more CSS */
  }
}

/* ❌ NEVER: Fixed pixel breakpoints for text */
@media (min-width: 768px) {
  body { font-size: 18px; } /* Use rem! */
}

/* ❌ NEVER: Over-nesting container queries */
@container a {
  @container b {
    @container c {
      /* Too complex, reconsider architecture */
    }
  }
}
```

## Browser Support

| Feature | Chrome | Safari | Firefox | Edge |
|---------|--------|--------|---------|------|
| Container Size Queries | 105+ | 16+ | 110+ | 105+ |
| Container Style Queries | 111+ | ❌ | ❌ | 111+ |
| Container Scroll-State | 126+ | ❌ | ❌ | 126+ |
| cqi/cqb units | 105+ | 16+ | 110+ | 105+ |
| clamp() | 79+ | 13.1+ | 75+ | 79+ |
| Subgrid | 117+ | 16+ | 71+ | 117+ |

## Key Decisions

| Decision | Option A | Option B | Recommendation |
|----------|----------|----------|----------------|
| Query type | Media queries | Container queries | **Container** for components, **Media** for layout |
| Container units | cqw/cqh | cqi/cqb | **cqi/cqb** (logical, i18n-ready) |
| Fluid type base | vw only | rem + vw | **rem + vw** (accessibility) |
| Mobile-first | Yes | Desktop-first | **Mobile-first** (less CSS, progressive) |
| Grid pattern | auto-fit | auto-fill | **auto-fit** for cards, **auto-fill** for icons |

## Related Skills

- `design-system-starter` - Building responsive design systems
- `core-web-vitals` - CLS and responsive images
- `image-optimization` - Responsive image strategies
- `i18n-date-patterns` - RTL/LTR responsive considerations

## Capability Details

### container-queries
**Keywords**: @container, container-type, inline-size, container-name
**Solves**: Component-level responsive design

### fluid-typography
**Keywords**: clamp(), fluid, vw, rem, scale, typography
**Solves**: Smooth font scaling without breakpoints

### responsive-images
**Keywords**: srcset, sizes, picture, art direction
**Solves**: Responsive images for different viewports

### mobile-first-strategy
**Keywords**: min-width, mobile, progressive, breakpoints
**Solves**: Efficient responsive CSS architecture

### grid-flexbox-patterns
**Keywords**: auto-fit, auto-fill, subgrid, minmax
**Solves**: Responsive grid and flexbox layouts

### container-units
**Keywords**: cqi, cqb, container width, container height
**Solves**: Sizing relative to container dimensions

## References

- `references/container-queries.md` - Container query patterns
- `references/fluid-typography.md` - Accessible fluid type scales
- `templates/responsive-card.tsx` - Responsive card component
