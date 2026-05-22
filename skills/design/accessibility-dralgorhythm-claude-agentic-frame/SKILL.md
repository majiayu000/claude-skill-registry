---
name: accessibility
description: Ensure digital accessibility. Use when designing for accessibility, auditing WCAG compliance, or implementing a11y features. Covers WCAG 2.1 guidelines.
allowed-tools: Read, Glob, Grep
---

# Accessibility

## WCAG 2.1 Principles (POUR)

### Perceivable
Content must be presentable in ways users can perceive.

### Operable
Interface must be operable by all users.

### Understandable
Content and operation must be understandable.

### Robust
Content must work with current and future technologies.

## Common Issues & Fixes

### Images
```html
<!-- Bad -->
<img src="chart.png">

<!-- Good -->
<img src="chart.png" alt="Sales increased 25% in Q4 2024">
```

### Forms
```html
<!-- Bad -->
<input type="email" placeholder="Email">

<!-- Good -->
<label for="email">Email</label>
<input id="email" type="email" aria-describedby="email-hint">
<span id="email-hint">We'll never share your email</span>
```

### Color Contrast
- Normal text: 4.5:1 minimum
- Large text (18pt+): 3:1 minimum
- UI components: 3:1 minimum

### Keyboard Navigation
- All interactive elements focusable
- Visible focus indicator
- Logical tab order
- Skip links for navigation

### Screen Readers
```html
<!-- Hidden visually but accessible -->
<span class="sr-only">Open menu</span>

<!-- Live regions for updates -->
<div aria-live="polite">Item added to cart</div>
```

## ARIA Basics

```html
<!-- Roles -->
<nav role="navigation">

<!-- States -->
<button aria-expanded="false">Menu</button>

<!-- Properties -->
<input aria-required="true">

<!-- Labels -->
<button aria-label="Close dialog">×</button>
```

## Testing Checklist

- [ ] Keyboard navigation works
- [ ] Screen reader announces correctly
- [ ] Color contrast passes
- [ ] Focus visible
- [ ] Form labels present
- [ ] Images have alt text
- [ ] Headings hierarchical
- [ ] Links descriptive

## Tools

- Axe DevTools (browser extension)
- WAVE (web accessibility evaluator)
- Lighthouse (Chrome DevTools)
- Screen readers: NVDA, VoiceOver, JAWS
