---
name: nean-styleguide
description: Design and UI style guide for NEAN web apps. Premium consumer aesthetic.
---

## Purpose

Enforce design quality and brand differentiation. Complements security, NFR, and coding standards skills.

For brand identity (colors, fonts, design direction, anti-patterns), see `/shared-brand`.

## PrimeNG customization

- Never use default PrimeNG themes unchanged
- Customize theme via CSS variables or custom SCSS
- Ensure components match brand aesthetic
- Override default spacing and typography

## NEAN-specific anti-patterns

- Default PrimeNG examples shipped unchanged
- Template SaaS layouts with no variation

## Requirements

### Responsive

- Mobile, tablet, desktop, large desktop
- Layouts adapt intentionally, not merely shrink
- Navigation patterns may change by breakpoint
- PrimeNG responsive utilities + Tailwind breakpoints

### Accessibility

- WCAG 2.1 AA minimum
- Keyboard navigation with visible focus states
- Respect `prefers-reduced-motion`
- Proper ARIA labels on interactive elements
- PrimeNG components are accessible by default; don't break this

### Browser support

- Chrome, Safari (including iOS), Firefox, Edge (latest)
- Mobile Safari mandatory; no Chromium-only behavior

## Reference

For semantic tokens, breakpoints, and detailed patterns, see `reference/nean-styleguide-reference.md`
