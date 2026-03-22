---
name: web-a11y
description: (ePost) Use when web accessibility issues arise — ARIA roles, keyboard navigation, focus trapping, alt text, contrast, screen readers
user-invocable: false
metadata:
  keywords:
    - keyboard
    - aria
    - focus
    - screen-reader
    - web-accessibility
    - semantic-html
  agent-affinity:
    - epost-a11y-specialist
    - epost-fullstack-developer
  platforms:
    - web
  connections:
    extends: [a11y]
---

# Web Accessibility Skill

## Purpose

Comprehensive WCAG 2.1 AA accessibility rules for web development. Covers semantic HTML, ARIA patterns, keyboard navigation, focus management, color contrast, and screen reader testing for React/Next.js applications.

## Aspect Files

| File | Coverage |
|------|----------|
| `references/web-semantic-html.md` | Semantic elements, text alternatives, landmark roles, skip links, heading hierarchy |
| `references/web-aria.md` | ARIA labels, roles, live regions, dialog/tab/progressbar patterns, state attributes |
| `references/web-keyboard-focus.md` | :focus-visible, focus trapping, tabIndex, keyboard event handlers, focus order |
| `references/web-forms.md` | Label association, error announcements, required indicators, fieldset/legend, autocomplete |
| `references/web-contrast.md` | Contrast ratios, forced-colors, prefers-color-scheme, visually-hidden, motion reduction |
| `references/web-wcag-reference.md` | WCAG 2.1 success criteria (A/AA), ARIA patterns quick reference, screen reader commands, checklist |

## Fix Templates

| Template | When to Apply |
|----------|--------------|
| `add_alt_text` | `<img>` missing `alt` attribute or has `alt=""` on informative image |
| `make_decorative` | Decorative image with meaningful alt text — set `alt=""` and `role="presentation"` |
| `add_aria_label` | Interactive element has no accessible name (icon button, custom widget) |
| `add_heading_level` | Heading hierarchy skips levels (h1 → h3), or visual heading uses `<div>` |
| `add_focus_visible` | `:focus` outline removed via CSS without `:focus-visible` replacement |
| `add_form_label` | `<input>` has no associated `<label>`, `aria-label`, or `aria-labelledby` |
| `other_manual` | Complex widget, custom component, or context-dependent fix requiring manual review |

## Quick Reference

### Semantic HTML

```html
<!-- Prefer native elements -->
<button onclick="save()">Save</button>        <!-- ✅ -->
<div role="button" onclick="save()">Save</div> <!-- ❌ avoid -->

<!-- Landmark structure -->
<header>...</header>
<nav aria-label="Primary">...</nav>
<main>...</main>
<aside>...</aside>
<footer>...</footer>
```

### ARIA Labels

```html
<!-- When visible label is absent -->
<button aria-label="Close dialog">✕</button>

<!-- Link label from another element -->
<h2 id="article-title">...</h2>
<a aria-labelledby="article-title">Read more</a>

<!-- Live region for dynamic content -->
<div aria-live="polite" aria-atomic="true">Status updated</div>
```

### Keyboard Navigation

```css
/* Never suppress focus without replacement */
:focus-visible {
  outline: 2px solid #005fcc;
  outline-offset: 2px;
}
```

```js
// tabIndex rules
tabIndex={0}   // Natural keyboard order
tabIndex={-1}  // Programmatic focus only, not in tab order
// Never use positive tabIndex values
```

### React Patterns

```jsx
// Accessible icon button
<button aria-label="Delete item" onClick={handleDelete}>
  <TrashIcon aria-hidden="true" />
</button>

// Conditional ARIA state
<button aria-expanded={isOpen} aria-controls="menu-id">
  Menu
</button>
```

## Testing Tools

| Tool | Purpose |
|------|---------|
| Lighthouse | Automated audit in Chrome DevTools (score 0-100) |
| axe-core / axe DevTools | Rule-based violation detection, integrates with Jest/Playwright |
| VoiceOver (macOS/iOS) | Screen reader — `Cmd+F5` to toggle, navigate with `VO+Arrow` |
| NVDA (Windows) | Free screen reader for Windows cross-browser testing |
| Chrome DevTools | Accessibility tree inspector, contrast checker in Elements panel |

## Agents Using This Skill

- `epost-a11y-specialist` — Multi-platform accessibility orchestrator

## Related Documents

- `ios-a11y` — iOS counterpart (VoiceOver, UIKit, SwiftUI)
- `android-a11y` — Android counterpart (TalkBack, Compose, Semantics)
- `a11y` — Platform-agnostic core principles (POUR, scoring)
