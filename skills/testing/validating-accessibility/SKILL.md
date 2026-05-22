---
name: validating-accessibility
description: Validate UI components for WCAG 2.2 Level AA compliance. Use when checking accessibility, color contrast, keyboard navigation, screen reader support, or ARIA attributes.
allowed-tools: Read, Edit, Glob, Grep
user-invocable: true
---

# Validating Accessibility

Ensure WCAG 2.2 Level AA compliance.

## Quick Checklist

```
[ ] Color contrast: 4.5:1 (text), 3:1 (UI/large text)
[ ] Keyboard: All interactive elements focusable
[ ] Focus: Visible focus indicators
[ ] ARIA: Correct attributes on custom controls
[ ] Motion: prefers-reduced-motion respected
[ ] Semantic: Proper heading hierarchy (h1→h2→h3)
[ ] Labels: All form inputs have labels
[ ] Alt text: All images have alt attributes
```

## Color Contrast

```
Normal text (<18px):     4.5:1 minimum
Large text (≥18px):      3:1 minimum
UI components:           3:1 minimum
```

```css
/* Safe high-contrast pairs */
--text-on-light: oklch(15% 0 0);   /* ~16:1 on white */
--text-on-dark: oklch(95% 0 0);    /* ~14:1 on black */
```

## Keyboard Navigation

```tsx
// Visible focus indicator (MANDATORY)
className="focus:outline-none focus-visible:ring-2 focus-visible:ring-primary"

// Skip link (first element in body)
<a href="#main" className="sr-only focus:not-sr-only">
  Skip to main content
</a>
```

## Semantic HTML

```html
<!-- Correct heading hierarchy -->
<h1>Page Title</h1>
  <h2>Section</h2>
    <h3>Subsection</h3>

<!-- Landmarks -->
<header role="banner">
<nav role="navigation">
<main role="main" id="main">
<footer role="contentinfo">
```

## ARIA Patterns

```tsx
// Button with icon only
<button aria-label="Close dialog">
  <X className="h-4 w-4" />
</button>

// Expandable content
<button aria-expanded={isOpen} aria-controls="panel">
  Toggle
</button>
<div id="panel" aria-hidden={!isOpen}>Content</div>

// Form with description
<input aria-describedby="hint" />
<p id="hint">Must be 8+ characters</p>
```

## Motion Accessibility

```tsx
// Framer Motion with reduced motion
import { useReducedMotion } from "framer-motion";

function Component() {
  const shouldReduce = useReducedMotion();
  return (
    <motion.div
      animate={shouldReduce ? {} : { y: 0, opacity: 1 }}
    />
  );
}
```

```css
/* CSS fallback */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

## References

- **UX Principles**: `../../references/ux-principles.md` (Nielsen heuristics, WCAG 2.2)
- **Forms Guide**: `../../references/forms-guide.md` (validation states, labels, error messages)
- **Buttons Guide**: `../../references/buttons-guide.md` (touch targets 44x44px, focus states)
- **Icons Guide**: `../../references/icons-guide.md` (aria-label for icon buttons)
- **Color System**: `../../references/color-system.md` (contrast ratios)
- **Design Patterns**: `../../references/design-patterns.md`
- **WCAG 2.2**: https://www.w3.org/WAI/WCAG22/quickref/
