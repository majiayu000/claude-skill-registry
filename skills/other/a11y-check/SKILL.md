---
name: a11y-check
description: "Accessibility audit against WCAG 2.1 AA. Checks semantic HTML, ARIA, keyboard navigation, color contrast, screen reader compatibility."
instruction_budget: 26
---

# Accessibility Audit

Evaluate user-facing work against WCAG 2.1 AA. Accessibility is a design constraint, not a polish step (Downe Principle 11).

## WCAG 2.1 AA Checklist by Principle

### 1. Perceivable
- [ ] All images have meaningful alt text (or alt="" for decorative)
- [ ] Video has captions; audio has transcripts
- [ ] Color is never the sole indicator of meaning
- [ ] Color contrast: 4.5:1 normal text, 3:1 large text
- [ ] Content is readable at 200% zoom without horizontal scroll
- [ ] Text spacing can be adjusted without loss of content

### 2. Operable
- [ ] All interactive elements reachable via keyboard (Tab/Shift+Tab)
- [ ] Visible focus indicators on all focusable elements
- [ ] No keyboard traps (can always Tab away)
- [ ] Skip navigation link for repetitive content
- [ ] Page titles are descriptive and unique
- [ ] Focus order matches visual order
- [ ] Touch targets are at least 44x44 CSS pixels

### 3. Understandable
- [ ] Language of page is declared (lang attribute)
- [ ] Form inputs have associated labels
- [ ] Error messages identify the field and describe the fix
- [ ] Instructions don't rely solely on sensory characteristics
- [ ] Navigation is consistent across pages

### 4. Robust
- [ ] Valid HTML (no duplicate IDs, proper nesting)
- [ ] ARIA used correctly (roles, states, properties)
- [ ] Custom components expose name, role, value to assistive tech
- [ ] Status messages use aria-live regions

## Automated Testing Tools (by stack)

| Stack | Tool | Command |
|-------|------|---------|
| React/Web | axe-core | `npx axe <url>` or axe-core in tests |
| Any web | Lighthouse | `npx lighthouse <url> --only-categories=accessibility` |
| Any web | pa11y | `npx pa11y <url>` |
| CI/CD | axe-linter | Add to CI pipeline |

## Common Violations and Fixes

| Violation | Fix |
|-----------|-----|
| Missing alt text | Add descriptive alt or alt="" for decorative |
| Low color contrast | Increase contrast ratio to 4.5:1 minimum |
| Missing form labels | Add `<label for="id">` or aria-label |
| No focus indicator | Add `:focus-visible` styles, never `outline: none` |
| Non-semantic buttons | Use `<button>` not `<div onclick>` |
| Missing heading hierarchy | Use h1-h6 in order, don't skip levels |
| Auto-playing media | Add pause/stop controls, respect prefers-reduced-motion |

## When to Run
- During development: after every UI component
- Before PR: full automated scan
- Before release: manual screen reader test of critical journeys
- After design changes: re-audit affected components

## Sensitive Context Note
For products handling sensitive user contexts (health, finance, domestic violence, government services), also review trauma-informed design principles in `domains/quality/CLAUDE.md`. Source: Hussain (Chayn), built on SAMHSA's 6 Principles (2014).

## Neurodiversity Considerations
For information-dense or learning-oriented products, supplement WCAG with the Neurodiversity Design System (neurodiversity.design, Soward). Its 8 principle categories with neurotype-to-UI-element matrix address cognitive accessibility needs that WCAG does not fully cover (e.g., font shapes for dyslexia, number formatting for dyscalculia, animation controls for ADHD).
