---
name: wcag-compliance
description: WCAG 2.2 AA accessibility compliance patterns for web applications. Use when auditing accessibility or implementing WCAG requirements.
context: fork
agent: accessibility-specialist
version: 1.0.0
tags: [accessibility, wcag, a11y, aria, screen-reader, compliance]
allowed-tools: [Read, Write, Grep, Glob, Bash]
author: SkillForge
user-invocable: false
---

# WCAG Compliance

Web Content Accessibility Guidelines 2.2 AA implementation for inclusive, legally compliant web applications.

## Overview

- Building accessible UI components from scratch
- Auditing applications for ADA/Section 508 compliance
- Implementing keyboard navigation and focus management
- Supporting screen readers and assistive technologies
- Fixing color contrast and visual accessibility issues

## Quick Reference

### Semantic HTML Structure
```tsx
<main>
  <article>
    <header><h1>Page Title</h1></header>
    <section aria-labelledby="features-heading">
      <h2 id="features-heading">Features</h2>
      <ul><li>Feature 1</li></ul>
    </section>
    <aside aria-label="Related content">...</aside>
  </article>
</main>
```

### ARIA Labels and States
```tsx
// Icon-only button
<button aria-label="Save document">
  <svg aria-hidden="true">...</svg>
</button>

// Form field with error
<input
  id="email"
  aria-required="true"
  aria-invalid={!!error}
  aria-describedby={error ? "email-error" : "email-hint"}
/>
{error && <p id="email-error" role="alert">{error}</p>}
```

### Color Contrast (CSS)
```css
:root {
  --text-primary: #1a1a1a;   /* 16.1:1 on white - normal text */
  --text-secondary: #595959; /* 7.0:1 on white - secondary */
  --focus-ring: #0052cc;     /* 7.3:1 - focus indicator */
}
:focus-visible {
  outline: 3px solid var(--focus-ring);
  outline-offset: 2px;
}
```

## WCAG 2.2 AA Checklist

| Criterion | Requirement | Test |
|-----------|-------------|------|
| 1.1.1 Non-text | Alt text for images | axe-core scan |
| 1.3.1 Info | Semantic HTML, headings | Manual + automated |
| 1.4.3 Contrast | 4.5:1 text, 3:1 large | WebAIM checker |
| 1.4.11 Non-text Contrast | 3:1 UI components | Manual inspection |
| 2.1.1 Keyboard | All functionality via keyboard | Tab through |
| 2.4.3 Focus Order | Logical tab sequence | Manual test |
| 2.4.7 Focus Visible | Clear focus indicator | Visual check |
| 2.4.11 Focus Not Obscured | Focus not hidden by sticky elements | scroll-margin-top |
| 2.5.7 Dragging | Single-pointer alternative | Button fallback |
| 2.5.8 Target Size | Min 24x24px interactive | CSS audit |
| 4.1.2 Name/Role/Value | Proper ARIA, labels | Screen reader test |

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Conformance level | WCAG 2.2 AA | Legal standard (ADA, Section 508) |
| Contrast ratio | 4.5:1 normal, 3:1 large | AA minimum requirement |
| Target size | 24px min, 44px touch | 2.5.8 + mobile usability |
| Focus indicator | 3px solid outline | High visibility, 3:1 contrast |
| Live regions | polite default, assertive for errors | Avoids interruption |
| Decorative images | alt="" role="presentation" | Hide from AT |
| Skip link | First focusable element | Keyboard user efficiency |

## Anti-Patterns (FORBIDDEN)

- **Div soup**: Using `<div>` instead of semantic elements (`<nav>`, `<main>`, `<article>`)
- **Color-only information**: Status indicated only by color without icon/text
- **Missing labels**: Form inputs without associated `<label>` or `aria-label`
- **Keyboard traps**: Focus that cannot escape without mouse
- **Auto-playing media**: Audio/video that plays without user action
- **Removing focus outline**: `outline: none` without replacement indicator
- **Positive tabindex**: Using `tabindex > 0` (disrupts natural order)
- **Empty links/buttons**: Interactive elements without accessible names
- **ARIA overuse**: Using ARIA when semantic HTML suffices

## Related Skills

- `a11y-testing` - Automated accessibility testing with axe-core and Playwright
- `design-system-starter` - Accessible component library patterns
- `i18n-date-patterns` - RTL layout and locale-aware formatting
- `motion-animation-patterns` - Reduced motion and animation accessibility

## Capability Details

### semantic-html
**Keywords:** semantic, landmark, heading, structure, html5, main, nav, article
**Solves:**
- Proper document structure with landmarks
- Heading hierarchy (h1-h6 in order)
- Form fieldsets and legends
- Lists for grouped content

### aria-patterns
**Keywords:** aria, role, state, property, live-region, alert, status
**Solves:**
- Custom widget accessibility (tabs, menus, dialogs)
- Dynamic content announcements
- Expanded/collapsed states
- Error/validation messaging

### focus-management
**Keywords:** keyboard, focus, tab, trap, modal, skip-link, roving
**Solves:**
- Modal focus trapping
- Skip links for navigation
- Roving tabindex for widgets
- Focus restoration after dialogs

### color-contrast
**Keywords:** contrast, color, wcag, perceivable, vision, ratio
**Solves:**
- Text contrast ratios (4.5:1 / 3:1)
- UI component contrast (3:1)
- Focus indicator visibility
- Non-color status indicators
