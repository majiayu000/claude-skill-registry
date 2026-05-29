---
name: validating-accessibility
description: Use when checking accessibility, color contrast, keyboard navigation, ARIA, or WCAG compliance. Covers WCAG 2.2 Level AA requirements.
versions:
  wcag: "2.2"
user-invocable: true
allowed-tools: Read, Edit, Glob, Grep
references: references/ux-nielsen.md, references/ux-laws.md, references/ux-wcag.md, references/ux-patterns.md, references/buttons-guide.md, references/forms-guide.md
related-skills: generating-components, interactive-states
---

# Validating Accessibility

## Agent Workflow (MANDATORY)

Before ANY accessibility validation, use `TeamCreate` to spawn 3 agents:

1. **fuse-ai-pilot:explore-codebase** - Find components to audit
2. **fuse-ai-pilot:research-expert** - Verify latest WCAG 2.2 requirements
3. Check existing ARIA patterns in codebase

After fixes, run **fuse-ai-pilot:sniper** for validation.

---

## Overview

| Feature | Description |
|---------|-------------|
| **WCAG 2.2 AA** | Minimum compliance level |
| **Color Contrast** | 4.5:1 text, 3:1 UI |
| **Keyboard** | Full navigation support |
| **ARIA** | Screen reader support |

---

## Critical Rules

1. **4.5:1 contrast** - Normal text minimum
2. **3:1 contrast** - Large text and UI components
3. **Focus visible** - All interactive elements
4. **Reduced motion** - Respect user preference
5. **Labels required** - All form inputs

---

## Quick Checklist

```
[ ] Color contrast: 4.5:1 (text), 3:1 (UI)
[ ] Keyboard: All elements focusable
[ ] Focus: Visible indicators (ring-2)
[ ] ARIA: Correct attributes
[ ] Motion: prefers-reduced-motion
[ ] Semantic: Proper heading hierarchy
[ ] Labels: All inputs labeled
[ ] Alt text: All images
```

---

## Reference Guide

### Concepts

| Topic | Reference | When to Consult |
|-------|-----------|-----------------|
| **Nielsen Heuristics** | [ux-nielsen.md](references/ux-nielsen.md) | 10 usability heuristics |
| **Laws of UX** | [ux-laws.md](references/ux-laws.md) | Cognitive psychology |
| **WCAG 2.2** | [ux-wcag.md](references/ux-wcag.md) | Accessibility standards |
| **UX Patterns** | [ux-patterns.md](references/ux-patterns.md) | Common UX patterns |
| **Buttons** | [buttons-guide.md](references/buttons-guide.md) | Touch targets, focus |
| **Forms** | [forms-guide.md](references/forms-guide.md) | Labels, validation |

---

## Quick Reference

### Color Contrast

```
Normal text (<18px):     4.5:1 minimum
Large text (≥18px):      3:1 minimum
UI components:           3:1 minimum
```

### Focus Indicator

```tsx
className="focus:outline-none focus-visible:ring-2 focus-visible:ring-primary"
```

### Reduced Motion

```tsx
import { useReducedMotion } from "framer-motion";

const shouldReduce = useReducedMotion();
<motion.div animate={shouldReduce ? {} : { y: 0 }} />
```

### ARIA Patterns

```tsx
// Icon button
<button aria-label="Close">
  <X className="h-4 w-4" />
</button>

// Form with description
<input aria-describedby="hint" />
<p id="hint">Must be 8+ characters</p>
```

→ See [ux-principles.md](references/ux-principles.md) for complete patterns

---

## Best Practices

### DO
- Test with keyboard only
- Use semantic HTML first
- Add aria-label to icon buttons
- Respect reduced motion
- Test with screen reader

### DON'T
- Skip focus indicators
- Use color alone for meaning
- Forget alt text on images
- Remove outline without replacement
- Ignore heading hierarchy
