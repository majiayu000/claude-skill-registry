---
name: accessibility-checklist
description: When building UI components, forms, or any user-facing interface. Check before every frontend PR.
version: 1.1.0
tokens: ~450
confidence: high
sources:
  - https://www.w3.org/WAI/WCAG22/quickref/
  - https://developer.mozilla.org/en-US/docs/Web/Accessibility
last_validated: 2025-12-10
next_review: 2025-12-24
tags: [accessibility, a11y, frontend, ux]
---

## When to Use
When building UI components, forms, or any user-facing interface. Check before every frontend PR.

## Patterns

### Keyboard Navigation
```html
<!-- All interactive elements focusable -->
<button>Click me</button>  <!-- ✅ Naturally focusable -->
<div role="button" tabindex="0">Click me</div>  <!-- ✅ Made focusable -->

<!-- Focus visible and not obscured (WCAG 2.2) -->
button:focus { outline: 2px solid blue; }
```

### Screen Reader Support
```html
<!-- Images -->
<img src="chart.png" alt="Sales increased 20% in Q4" />
<img src="decoration.png" alt="" />  <!-- Decorative: empty alt -->

<!-- Form labels -->
<label for="email">Email</label>
<input id="email" type="email" aria-required="true" />

<!-- Dynamic content -->
<div aria-live="polite" aria-busy="false">Loading complete</div>
```

### ARIA Essentials
```html
<!-- Button without text -->
<button aria-label="Close dialog"><svg>...</svg></button>

<!-- Expanded/collapsed -->
<button aria-expanded="false" aria-controls="menu">Menu</button>

<!-- Modal -->
<div role="dialog" aria-modal="true" aria-labelledby="title">
```

## Anti-Patterns
- Color-only indicators (add icons/text)
- Missing form labels (placeholder is NOT a label)
- Tiny touch targets (<44x44px)
- Keyboard traps (can't escape with Tab/Escape)
- Auto-playing media without controls
- Focus obscured by sticky headers/modals

## Verification Checklist
- [ ] All interactive elements reachable via Tab
- [ ] Focus indicator visible on all focusables
- [ ] Focus not obscured by sticky content (WCAG 2.2)
- [ ] Images have meaningful alt (or alt="" if decorative)
- [ ] Form inputs have associated labels
- [ ] Color contrast ≥4.5:1 (text) / ≥3:1 (large text)
- [ ] Touch targets ≥44x44px
- [ ] `prefers-reduced-motion` respected
- [ ] No cognitive tests for auth (avoid CAPTCHAs)
