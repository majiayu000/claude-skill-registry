---
name: ui-ux-patterns
description: When designing layouts, navigation, forms, or feedback components. Reference for consistent UI decisions.
version: 1.0.0
tokens: ~550
confidence: high
sources:
  - https://www.nngroup.com/articles/
  - https://lawsofux.com/
last_validated: 2025-01-10
next_review: 2025-01-24
tags: [ui, ux, design, frontend]
---

## When to Use
When designing layouts, navigation, forms, or feedback components. Reference for consistent UI decisions.

## Patterns

### 4 Required Screen States
Every screen MUST define:
1. **Loading** - skeleton or spinner
2. **Empty** - illustration + CTA
3. **Error** - message + recovery action
4. **Success** - content + next steps

### Layout Patterns
```
Card Grid     - Products, dashboard widgets
Master-Detail - Email client, settings
Split View    - Editor + preview
```

### Form Best Practices
```
- Validate on blur (not on every keystroke)
- Error message below field (not tooltip)
- Color + icon for status (not color alone)
- Multi-step: max 5-7 steps, progress indicator
```

### Feedback Patterns
```
Toast         - Auto-dismiss 3-5s, non-blocking, offer Undo
Modal         - Destructive actions, critical decisions only
Loading       - Skeleton (<3s), Spinner (unknown), Progress (>5s)
```

### Action Hierarchy
```
Primary   - Right side, filled button, max 1 per view
Secondary - Left of primary, outline button
Danger    - Red outline (not filled), requires confirmation
```

## Anti-Patterns
- Skipping empty/error states
- Walls of text (use scannable content)
- Desktop-only thinking (mobile-first!)
- Modal for non-critical info (use toast)
- Tiny touch targets (<44px)

## Verification Checklist
- [ ] All 4 states defined (loading, empty, error, success)
- [ ] Touch targets ≥44x44px
- [ ] Mobile breakpoints defined
- [ ] One primary action per view
- [ ] Destructive actions require confirmation
- [ ] Feedback is immediate and clear
