---
name: theming-tokens
description: Design token architecture with primitives, semantic, and component tokens. Use when creating theme systems, color variables, or design system tokens.
allowed-tools: Read, Write, Edit, Glob, Grep
user-invocable: true
---

# Theming Tokens

Three-tier token architecture inspired by DesignCode UI.

## Agent Workflow (MANDATORY)

Before implementation:
1. **fuse-ai-pilot:explore-codebase** - Find existing tokens
2. **fuse-ai-pilot:research-expert** - Tailwind v4 @theme patterns

After: Run **fuse-ai-pilot:sniper** for validation.

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

## 1. Primitive Tokens

```css
:root {
  /* Colors - OKLCH for P3 gamut */
  --blue-500: oklch(55% 0.20 260);
  --blue-600: oklch(48% 0.18 260);
  --green-500: oklch(65% 0.20 145);

  /* Opacity scale */
  --opacity-5: 0.05;
  --opacity-10: 0.10;
  --opacity-20: 0.20;
  --opacity-80: 0.80;

  /* Radius */
  --radius-sm: 0.375rem;
  --radius-md: 0.5rem;
  --radius-lg: 0.75rem;
  --radius-xl: 1rem;
  --radius-2xl: 1.5rem;

  /* Spacing (4px grid) */
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-4: 1rem;
  --space-6: 1.5rem;
  --space-8: 2rem;
}
```

## 2. Semantic Tokens

```css
:root {
  /* Surfaces */
  --color-background: var(--gray-50);
  --color-surface: var(--white);
  --color-surface-elevated: var(--white);

  /* Text */
  --color-foreground: var(--gray-900);
  --color-muted: var(--gray-500);

  /* Brand */
  --color-primary: var(--blue-500);
  --color-primary-foreground: var(--white);
  --color-accent: var(--green-500);

  /* States */
  --color-destructive: var(--red-500);
  --color-success: var(--green-500);

  /* Glass */
  --glass-bg: rgba(255, 255, 255, var(--opacity-80));
  --glass-border: rgba(255, 255, 255, var(--opacity-20));
}

.dark {
  --color-background: var(--gray-950);
  --color-surface: var(--gray-900);
  --color-foreground: var(--gray-50);
  --glass-bg: rgba(0, 0, 0, 0.4);
  --glass-border: rgba(255, 255, 255, 0.1);
}
```

## 3. Component Tokens

```css
:root {
  /* Buttons */
  --button-height: 2.5rem;
  --button-radius: var(--radius-lg);
  --button-font-weight: 500;

  /* Cards */
  --card-radius: var(--radius-2xl);
  --card-padding: var(--space-6);
  --card-shadow: 0 25px 50px -12px rgb(0 0 0 / 0.1);

  /* Inputs */
  --input-height: 2.75rem;
  --input-radius: var(--radius-md);
  --input-border: var(--gray-200);
}
```

## Tailwind v4 @theme

```css
/* app.css */
@import "tailwindcss";

@theme {
  --color-primary: oklch(55% 0.20 260);
  --color-accent: oklch(65% 0.20 145);
  --font-display: 'Inter', sans-serif;
  --radius-lg: 0.75rem;
}
```

## Usage in Components

```tsx
/* Direct CSS variable */
className="bg-[var(--color-surface)] text-[var(--color-foreground)]"

/* Via Tailwind (if @theme mapped) */
className="bg-primary text-primary-foreground"

/* Glass pattern */
className="bg-[var(--glass-bg)] backdrop-blur-xl border-[var(--glass-border)]"
```

## Validation

```
[ ] Primitives defined (colors, spacing, radius)
[ ] Semantics mapped to primitives
[ ] Dark mode overrides present
[ ] @theme configured for Tailwind v4
[ ] No hard-coded hex in components
```

## References

- `../../references/color-system.md` - OKLCH, psychology
- `../../references/designing-systems/SKILL.md` - Full system setup
