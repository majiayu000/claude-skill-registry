---
name: scroll-driven-animations
description: CSS Scroll-Driven Animations with ScrollTimeline, ViewTimeline, parallax effects, and progressive enhancement for performant scroll effects
tags: [scroll-animation, scroll-timeline, view-timeline, parallax, css-animation, scroll-driven, performance]
context: fork
agent: frontend-ui-developer
version: 1.0.0
author: SkillForge
user-invocable: false
---

# Scroll-Driven Animations

CSS Scroll-Driven Animations API provides performant, declarative scroll-linked animations without JavaScript. Supported in Chrome 115+, Edge 115+, Safari 18.4+.

## When to Use

- Progress indicators tied to scroll position
- Parallax effects without JavaScript jank
- Element reveal animations on scroll into view
- Sticky header animations based on scroll
- Reading progress bars
- Scroll-triggered image/content reveals

## Core Concepts

### Timeline Types

| Timeline | CSS Function | Use Case |
|----------|--------------|----------|
| **Scroll Progress** | `scroll()` | Tied to scroll container position (0-100%) |
| **View Progress** | `view()` | Tied to element visibility in viewport |

## CSS Patterns

### 1. Scroll Progress Timeline (Reading Progress)

```css
/* Progress bar that fills as page scrolls */
.progress-bar {
  position: fixed;
  top: 0;
  left: 0;
  height: 4px;
  background: var(--color-primary);
  transform-origin: left;

  /* Animate based on root scroll */
  animation: grow-progress linear;
  animation-timeline: scroll(root block);
}

@keyframes grow-progress {
  from { transform: scaleX(0); }
  to { transform: scaleX(1); }
}
```

### 2. View Timeline (Reveal on Scroll)

```css
/* Fade in when element enters viewport */
.reveal-on-scroll {
  animation: fade-slide-up linear both;
  animation-timeline: view();
  animation-range: entry 0% entry 100%;
}

@keyframes fade-slide-up {
  from {
    opacity: 0;
    transform: translateY(50px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

### 3. Animation Range Control

```css
/* Fine-tune when animation runs */
.card {
  animation: scale-up linear both;
  animation-timeline: view();

  /* Start at 25% entry, complete at 75% entry */
  animation-range: entry 25% entry 75%;
}

/* Full visibility animation */
.hero-image {
  animation: parallax linear both;
  animation-timeline: view();

  /* Animate through entire visibility */
  animation-range: cover 0% cover 100%;
}

@keyframes parallax {
  from { transform: translateY(-20%); }
  to { transform: translateY(20%); }
}
```

### 4. Named Scroll Timelines

```css
/* Define timeline on scroll container */
.scroll-container {
  overflow-y: auto;
  scroll-timeline-name: --container-scroll;
  scroll-timeline-axis: block;
}

/* Use timeline in descendant */
.progress-indicator {
  animation: progress linear;
  animation-timeline: --container-scroll;
}

@keyframes progress {
  from { width: 0%; }
  to { width: 100%; }
}
```

### 5. Named View Timelines with Scope

```css
/* Parent sets up the timeline scope */
.gallery {
  timeline-scope: --card-timeline;
}

/* Each card defines its view timeline */
.gallery-card {
  view-timeline-name: --card-timeline;
  view-timeline-axis: block;
}

/* Animate based on card visibility */
.gallery-card .image {
  animation: zoom-in linear both;
  animation-timeline: --card-timeline;
  animation-range: entry 0% cover 50%;
}

@keyframes zoom-in {
  from { transform: scale(0.8); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}
```

### 6. Parallax Sections

```css
.parallax-section {
  position: relative;
  overflow: hidden;
}

.parallax-bg {
  position: absolute;
  inset: -20% 0;

  animation: parallax-scroll linear both;
  animation-timeline: view();
  animation-range: cover 0% cover 100%;
}

@keyframes parallax-scroll {
  from { transform: translateY(0); }
  to { transform: translateY(40%); }
}
```

### 7. Sticky Header Animation

```css
.header {
  position: sticky;
  top: 0;

  animation: shrink-header linear both;
  animation-timeline: scroll(root);
  animation-range: 0px 200px;
}

@keyframes shrink-header {
  from {
    padding-block: 2rem;
    background: transparent;
  }
  to {
    padding-block: 0.5rem;
    background: var(--color-surface);
    box-shadow: var(--shadow-md);
  }
}
```

## JavaScript API

### ScrollTimeline

```typescript
// Create scroll timeline programmatically
const scrollTimeline = new ScrollTimeline({
  source: document.documentElement, // or specific scroll container
  axis: 'block', // 'block' | 'inline' | 'x' | 'y'
});

// Attach to animation
element.animate(
  [
    { transform: 'translateY(100px)', opacity: 0 },
    { transform: 'translateY(0)', opacity: 1 },
  ],
  {
    timeline: scrollTimeline,
    fill: 'both',
  }
);
```

### ViewTimeline

```typescript
// Create view timeline for specific element
const viewTimeline = new ViewTimeline({
  subject: element, // Element to track
  axis: 'block',
  inset: [CSS.px(0), CSS.px(0)], // Optional viewport inset
});

// Animate based on element visibility
element.animate(
  [
    { opacity: 0, transform: 'scale(0.8)' },
    { opacity: 1, transform: 'scale(1)' },
  ],
  {
    timeline: viewTimeline,
    fill: 'both',
    rangeStart: 'entry 0%',
    rangeEnd: 'cover 50%',
  }
);
```

## React Integration

```tsx
import { useRef, useEffect } from 'react';

function useScrollAnimation(
  keyframes: Keyframe[],
  options: {
    timeline?: 'scroll' | 'view';
    range?: string;
  } = {}
) {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const element = ref.current;
    if (!element || !('animate' in element)) return;

    // Feature detection
    if (!('ScrollTimeline' in window)) {
      console.warn('Scroll-driven animations not supported');
      return;
    }

    const timeline = options.timeline === 'view'
      ? new ViewTimeline({ subject: element, axis: 'block' })
      : new ScrollTimeline({ source: document.documentElement, axis: 'block' });

    const animation = element.animate(keyframes, {
      timeline,
      fill: 'both',
      ...(options.range && {
        rangeStart: options.range.split(' ')[0],
        rangeEnd: options.range.split(' ')[1],
      }),
    });

    return () => animation.cancel();
  }, [keyframes, options.timeline, options.range]);

  return ref;
}

// Usage
function RevealCard({ children }: { children: React.ReactNode }) {
  const ref = useScrollAnimation(
    [
      { opacity: 0, transform: 'translateY(50px)' },
      { opacity: 1, transform: 'translateY(0)' },
    ],
    { timeline: 'view', range: 'entry cover' }
  );

  return <div ref={ref}>{children}</div>;
}
```

## Progressive Enhancement

```css
/* Fallback for unsupported browsers */
.reveal-on-scroll {
  opacity: 1; /* Default visible */
  transform: translateY(0);
}

/* Apply animation only when supported */
@supports (animation-timeline: view()) {
  .reveal-on-scroll {
    animation: fade-slide-up linear both;
    animation-timeline: view();
    animation-range: entry 0% entry 100%;
  }
}
```

```tsx
// Feature detection in React
const supportsScrollTimeline =
  typeof ScrollTimeline !== 'undefined';

function AnimatedSection({ children }: { children: React.ReactNode }) {
  if (!supportsScrollTimeline) {
    // Fallback: use Intersection Observer
    return <IntersectionObserverFallback>{children}</IntersectionObserverFallback>;
  }

  return <ScrollAnimatedSection>{children}</ScrollAnimatedSection>;
}
```

## Chrome DevTools Debugging

1. Open DevTools → Elements tab
2. Find "Scroll-Driven Animations" tab (may be in overflow ››)
3. Select element with scroll animation
4. Scrub timeline to preview animation
5. Inspect animation-timeline and animation-range values

## Performance Best Practices

```css
/* ✅ CORRECT: Animate transform/opacity only */
@keyframes good-animation {
  from { transform: translateY(100px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

/* ❌ WRONG: Animate layout properties */
@keyframes bad-animation {
  from { margin-top: 100px; height: 0; }
  to { margin-top: 0; height: auto; }
}

/* ✅ Use will-change sparingly */
.scroll-animated {
  will-change: transform, opacity;
}
```

## Anti-Patterns (FORBIDDEN)

```css
/* ❌ NEVER: Animate layout-triggering properties */
@keyframes bad {
  from { width: 0; margin-left: 100px; }
  to { width: 100%; margin-left: 0; }
}

/* ❌ NEVER: Use without fallback */
.element {
  animation-timeline: scroll(); /* Breaks in Firefox! */
}

/* ❌ NEVER: Overly complex animation chains */
.element {
  animation: anim1, anim2, anim3, anim4, anim5;
  animation-timeline: view(), scroll(), view(), scroll(), view();
}

/* ❌ NEVER: Scroll animations on non-scrollable containers */
.no-overflow {
  overflow: hidden;
  scroll-timeline-name: --timeline; /* Won't work! */
}
```

## Browser Support

| Browser | scroll() | view() | ScrollTimeline API |
|---------|----------|--------|-------------------|
| Chrome 115+ | ✅ | ✅ | ✅ |
| Edge 115+ | ✅ | ✅ | ✅ |
| Safari 18.4+ | ✅ | ✅ | ✅ |
| Firefox | ❌ | ❌ | ❌ (in development) |

## Key Decisions

| Decision | Option A | Option B | Recommendation |
|----------|----------|----------|----------------|
| Timeline type | scroll() | view() | **view()** for reveals, **scroll()** for progress |
| Fallback strategy | IntersectionObserver | No animation | **IntersectionObserver** fallback |
| Animation properties | All CSS | transform/opacity | **transform/opacity** only |
| Range units | Percentages | Named ranges | **Named ranges** (entry, cover) for clarity |

## Related Skills

- `motion-animation-patterns` - Framer Motion for JS animations
- `core-web-vitals` - Performance impact considerations
- `view-transitions` - Complementary page transitions

## Capability Details

### scroll-timeline
**Keywords**: scroll(), progress, scroll position, reading progress
**Solves**: Animations tied to scroll container position

### view-timeline
**Keywords**: view(), visibility, reveal, enter viewport
**Solves**: Animations triggered by element visibility

### parallax-effects
**Keywords**: parallax, background, depth, scroll speed
**Solves**: Performant parallax without JavaScript

### scroll-triggered
**Keywords**: trigger, intersection, enter, exit, reveal
**Solves**: Trigger animations on scroll position

### progressive-enhancement
**Keywords**: fallback, @supports, feature detection
**Solves**: Support for browsers without scroll-driven animations

## References

- `references/css-scroll-timeline.md` - CSS scroll() and view() functions
- `references/js-api.md` - JavaScript ScrollTimeline/ViewTimeline API
- `templates/parallax-section.tsx` - React parallax component
