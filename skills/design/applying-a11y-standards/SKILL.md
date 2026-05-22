---
name: applying-a11y-standards
description: Rules for ensuring Accessibility (a11y) across the Tourly app. Use to build inclusive interfaces.
---

# Accessibility Standards (a11y)

## When to use this skill
- Every time you create a new component or page.
- During UI audits.

## Best Practices
- **Semantic HTML**: Use `<main>`, `<header>`, `<footer>`, `<nav>`, and appropriate heading levels.
- **ARIA Labels**: Use `aria-label` for icon-only buttons.
- **Keyboard Nav**: Ensure all interactive elements have a visible `:focus-visible` state.
- **Contrast**: Maintain a text-to-background contrast ratio of at least 4.5:1.

## Instructions
- **Tools**: Use the `axe-core` library or Lighthouse to run automated audits.
- **Alt Text**: Every `Image` must have a descriptive `alt` attribute.
