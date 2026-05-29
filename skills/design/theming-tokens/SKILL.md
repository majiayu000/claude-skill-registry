---
name: theming-tokens
description: Use when creating theme systems, color variables, or design system tokens. Covers primitives, semantic, and component tokens.
versions:
  tailwindcss: "4.1"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep
related-skills: designing-systems, dark-light-modes
---

# Theming Tokens

## Agent Workflow (MANDATORY)

Before implementation, use `TeamCreate` to spawn 3 agents:

1. **fuse-ai-pilot:explore-codebase** - Find existing tokens
2. **fuse-ai-pilot:research-expert** - Tailwind v4 @theme patterns

After: Run **fuse-ai-pilot:sniper** for validation.

---

## Overview

| Feature | Description |
|---------|-------------|
| **Primitives** | Raw values (blue-500, radius-lg) |
| **Semantic** | Purpose-based (primary, surface) |
| **Component** | Specific (button-bg, card-border) |

---

## Token Hierarchy

```
┌─────────────────────────────────────────────────┐
│ COMPONENT TOKENS (specific)                     │
│ --button-bg, --card-border, --input-focus       │
├─────────────────────────────────────────────────┤
│ SEMANTIC TOKENS (purpose)                       │
│ --color-primary, --color-surface, --color-text  │
├─────────────────────────────────────────────────┤
│ PRIMITIVE TOKENS (raw values)                   │
│ --blue-500, --gray-100, --radius-lg             │
└─────────────────────────────────────────────────┘
```

---

## Quick Reference

### Primitive Tokens

```css
:root {
  /* Colors - OKLCH for P3 gamut */
  --blue-500: oklch(55% 0.20 260);
  --green-500: oklch(65% 0.20 145);

  /* Radius */
  --radius-lg: 0.75rem;
  --radius-2xl: 1.5rem;

  /* Spacing (4px grid) */
  --space-4: 1rem;
  --space-6: 1.5rem;
}
```

### Semantic Tokens

```css
:root {
  --color-background: var(--gray-50);
  --color-foreground: var(--gray-900);
  --color-primary: var(--blue-500);
  --color-surface: var(--white);

  /* Glass */
  --glass-bg: rgba(255, 255, 255, 0.8);
  --glass-border: rgba(255, 255, 255, 0.2);
}

.dark {
  --color-background: var(--gray-950);
  --color-foreground: var(--gray-50);
  --glass-bg: rgba(0, 0, 0, 0.4);
}
```

### Component Tokens

```css
:root {
  --button-height: 2.5rem;
  --button-radius: var(--radius-lg);
  --card-radius: var(--radius-2xl);
  --card-padding: var(--space-6);
}
```

### Tailwind v4 @theme

```css
@import "tailwindcss";

@theme {
  --color-primary: oklch(55% 0.20 260);
  --font-display: 'Clash Display', sans-serif;
}
```

---

## Validation Checklist

```
[ ] Primitives defined (colors, spacing, radius)
[ ] Semantics mapped to primitives
[ ] Dark mode overrides present
[ ] @theme configured for Tailwind v4
[ ] No hard-coded hex in components
```

---

## Best Practices

### DO
- Use three-tier hierarchy
- Map semantics to primitives
- Define dark mode overrides
- Use OKLCH for colors

### DON'T
- Hard-code hex values
- Skip semantic layer
- Forget dark mode
- Mix color spaces
