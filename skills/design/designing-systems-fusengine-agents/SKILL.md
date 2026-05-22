---
name: designing-systems
description: Create and manage design systems with tokens, color palettes, typography scales, and spacing systems. Use when user asks about design tokens, theming, color schemes, or consistent styling.
allowed-tools: Read, Write, Edit, Glob, Grep, Task
user-invocable: true
---

# Designing Systems

Create consistent, scalable design systems with tokens.

## APEX WORKFLOW

### Phase 0: ANALYZE EXISTING (CRITICAL)

```
Task: explore-codebase
Prompt: "Find existing design tokens: CSS variables, Tailwind config,
color palette, typography, spacing patterns"
```

**If design system exists:** Document and extend it.
**If no design system:** Create new following this guide.

## Design Token Categories

| Category | Format | Example |
|----------|--------|---------|
| Colors | OKLCH | `oklch(55% 0.20 260)` |
| Typography | rem | `--text-lg: 1.125rem` |
| Spacing | rem (4px grid) | `--spacing-4: 1rem` |
| Radius | px/rem | `--radius-lg: 0.75rem` |
| Shadows | CSS | `--shadow-md: ...` |

## Color System (OKLCH 2026)

```css
/* Primary palette - OKLCH for P3 wide gamut */
--color-primary-500: oklch(55% 0.20 260);
--color-primary-600: oklch(48% 0.18 260);

/* Semantic mapping */
--color-background: var(--color-neutral-50);
--color-foreground: var(--color-neutral-900);
--color-muted: var(--color-neutral-100);
--color-border: var(--color-neutral-200);

/* Dark mode */
.dark {
  --color-background: var(--color-neutral-900);
  --color-foreground: var(--color-neutral-50);
}
```

## Typography Scale (1.25 ratio)

```css
/* FORBIDDEN: Inter, Roboto, Arial */
/* USE: Clash Display, Satoshi, Bricolage Grotesque */

--font-display: 'Clash Display', sans-serif;
--font-sans: 'Satoshi', sans-serif;
--font-mono: 'JetBrains Mono', monospace;

--text-sm: 0.875rem;   /* 14px */
--text-base: 1rem;     /* 16px */
--text-lg: 1.125rem;   /* 18px */
--text-xl: 1.25rem;    /* 20px */
--text-2xl: 1.5rem;    /* 24px */
```

## Spacing (4px grid)

```css
--spacing-1: 0.25rem;  /* 4px */
--spacing-2: 0.5rem;   /* 8px */
--spacing-4: 1rem;     /* 16px */
--spacing-6: 1.5rem;   /* 24px */
--spacing-8: 2rem;     /* 32px */
```

## Tailwind v4 Config

```css
/* app.css - CSS-first config */
@import "tailwindcss";

@theme {
  --color-primary-*: oklch(55% 0.20 260);
  --font-display: 'Clash Display', sans-serif;
  --radius-lg: 0.75rem;
}
```

## Validation

```
[ ] Existing tokens documented (Phase 0)
[ ] No forbidden fonts (Inter/Roboto/Arial)
[ ] OKLCH colors for wide gamut
[ ] Dark mode variables defined
[ ] Tailwind v4 @theme configured
```

## References

- **Color System**: `../../references/color-system.md` (psychology, 60-30-10 rule, OKLCH)
- **Typography**: `../../references/typography.md` (mobile sizes, line-height, weights)
- **Grids & Layout**: `../../references/grids-layout.md` (12-column, gutters, margins)
- **UI Visual Design**: `../../references/ui-visual-design.md` (hierarchy, 2026 trends)
- **Theme Presets**: `../../references/theme-presets.md` (Brutalist, Solarpunk, etc.)
- **Tailwind Best Practices**: `../../references/tailwind-best-practices.md`
