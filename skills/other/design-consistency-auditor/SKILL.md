---
name: design-consistency-auditor
description: Audit and maintain design system consistency, UX/UI patterns, color palettes, and design best practices across frontend applications
version: 1.0.0
tags:
  - design
  - ux
  - ui
  - consistency
  - audit
  - tailwind
  - agenticindiedev-ui
  - accessibility
---

# Design Consistency Auditor

## Purpose

Audit and maintain design consistency across frontend applications. Before auditing, discover the project's frontend structure from documentation.

Ensures:

- Color palettes are used consistently
- UI/UX patterns follow best practices
- Components maintain visual harmony
- Accessibility standards are met
- Design system is properly applied
- No design debt accumulates

## When to Use

- Auditing design consistency across apps
- Reviewing color palette usage
- Checking UI/UX patterns
- Validating component styling
- Ensuring accessibility compliance
- Identifying design inconsistencies
- Reviewing new features for design standards

## Quick Reference

### Color Rules

**DO:** Use semantic tokens (`bg-primary`, `text-base-content`, `bg-base-100`)
**DON'T:** Hardcode hex colors (`#000000`) or arbitrary values (`bg-[#123456]`)

### Component Patterns

- Cards: `.gf-card`
- App shells: `.gf-app`
- Modals: `.glass-modal`
- Inputs: `.glass-input`, `.form-focus`
- Buttons: `btn btn-primary`, `.btn-secondary`, `btn-ghost`

### Spacing

**DO:** Use Tailwind scale (`p-4`, `m-6`, `gap-4`)
**DON'T:** Use arbitrary values (`p-[17px]`)

### Accessibility

- Semantic HTML (`<button>`, `<nav>`, `<main>`)
- ARIA labels on interactive elements
- 4.5:1 contrast for text, 3:1 for UI
- Focus states: `focus:outline-none focus:ring-2 focus:ring-primary`

### Responsive

- Mobile-first with `sm:`, `md:`, `lg:`, `xl:` modifiers
- Responsive typography: `text-3xl sm:text-4xl`

## Audit Phases

1. **Color Palette** - Scan for hardcoded colors, verify theme tokens
2. **Component Patterns** - Check cards, buttons, forms use theme classes
3. **Spacing & Layout** - Verify consistent spacing scale
4. **Typography** - Check heading hierarchy and text styles
5. **Accessibility** - Run automated checks, keyboard testing

## AI Slop Prevention

Audit for generic "AI-generated" aesthetics:

- Generic fonts (Inter, Roboto everywhere)
- Purple gradients on white
- Predictable layouts without character
- Safe, boring color choices

Push for distinctive, branded designs with personality.

---

**For detailed checklists, examples, reporting templates, and audit commands, see:** `references/full-guide.md`
