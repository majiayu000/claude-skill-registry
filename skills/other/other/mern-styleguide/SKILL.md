---
name: mern-styleguide
description: Design and UI style guide for MERN web apps. Premium consumer aesthetic.
---

## Purpose

Enforce design quality and brand differentiation. Complements security, NFR, and coding standards skills.

For brand identity (colors, fonts, design direction, anti-patterns), see `/shared-brand`.

## MERN-specific anti-patterns

- Default shadcn examples shipped unchanged
- Template SaaS layouts with no variation

## Requirements

### Responsive

- Mobile, tablet, desktop, large desktop
- Layouts adapt intentionally, not merely shrink
- Navigation patterns may change by breakpoint

### Accessibility

- WCAG 2.1 AA minimum
- Keyboard navigation with visible focus states
- Respect `prefers-reduced-motion`

### Browser support

- Chrome, Safari (including iOS), Firefox, Edge (latest)
- Mobile Safari mandatory; no Chromium-only behavior

## Reference

For semantic tokens, breakpoints, and detailed patterns, see `reference/mern-styleguide-reference.md`
