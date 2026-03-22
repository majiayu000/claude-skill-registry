---
name: "mobile-first-pwa"
description: "Implement mobile-first responsive design patterns and PWA features for modern web applications with focus on performance and user experience. Use for: responsive web design, progressive enhancement, mobile UX optimization, cross-device compatibility, touch interface design, mobile performance tuning."
---

# Mobile-First PWA Design

Implement mobile-first responsive design patterns with progressive enhancement and PWA capabilities.

## Overview

Apply mobile-first design methodology to create fast, accessible web experiences that work across all devices. Focus on responsive layout patterns, touch optimization, performance budgets, and progressive enhancement strategies.

## Mobile-First vs Desktop-First

| Aspect | Mobile-First | Desktop-First |
|--------|-------------|---------------|
| Base styles | Mobile layout | Desktop layout |
| Media queries | min-width (add complexity) | max-width (reduce complexity) |
| Performance | Optimized by default | May over-serve mobile |
| Content | Priority-driven | Feature-driven |
| Approach | Progressive enhancement | Graceful degradation |

## Responsive Design Checklist

- [ ] Viewport meta tag configured
- [ ] Touch targets ≥44px minimum
- [ ] Readable text without zooming (16px+ base)
- [ ] No horizontal scroll at any breakpoint
- [ ] Images use responsive srcset
- [ ] Navigation adapts to screen size
- [ ] Forms optimized for touch input
- [ ] Core Web Vitals pass on mobile

## Adaptive vs Responsive

| Approach | How It Works | When to Use |
|----------|-------------|-------------|
| Responsive | Fluid layouts, flexible grids | Most websites |
| Adaptive | Distinct layouts per breakpoint | Complex UI differences |
| Hybrid | Responsive within adaptive breakpoints | Large applications |

## Using the Reference Files

### When to Read Each Reference

**`/references/responsive-patterns.md`** — Read when implementing responsive layouts, CSS grid/flexbox patterns, or adaptive components.

**`/references/mobile-ux-performance.md`** — Read when optimizing mobile user experience, form design, navigation patterns, or performance metrics.

## Reference Files

This skill includes the following detailed reference materials:

- [Mobile Ux Performance](references/mobile-ux-performance.md)
- [Responsive Patterns](references/responsive-patterns.md)
