---
name: semantic-theming
description: Enforce semantic CSS variable theming in Tailwind projects. Prevents raw colors (hex, rgb) and non-theme Tailwind classes. Use when project has semantic tokens, CSS vars, or custom ESLint theming rules.
---

# Semantic Theming Skill

Use semantic design tokens instead of raw colors. This skill teaches Claude to write theme-compliant code from the start.

## Detection Criteria

**This skill applies when the project has ANY of:**

- `docs/THEMING.md` exists
- `eslint-rules/no-raw-colors.js` exists
- ESLint config includes `wescobar/no-raw-colors` or similar theming rule
- `src/index.css` defines CSS custom properties (e.g., `--color-primary`)

**Quick check:** Look for these indicators before applying this skill.

## When to Use

- Writing or editing React components with `className`
- Using Tailwind utility classes for colors/backgrounds/borders
- Working with `cn()`, `clsx()`, or `cva()` class composition
- Styling any UI element with colors

## Forbidden Patterns

### Raw Color Literals

```tsx
// FORBIDDEN - Will fail ESLint
style={{ color: '#ff0000' }}
style={{ backgroundColor: 'rgb(255, 0, 0)' }}
style={{ borderColor: 'hsl(0, 100%, 50%)' }}
```

### Non-Semantic Tailwind Classes

```tsx
// FORBIDDEN - Will fail ESLint
className="bg-red-500"
className="text-white"
className="border-blue-300"
className="bg-slate-900 text-gray-100"
className="from-purple-500 via-pink-500 to-red-500"
```

## Correct Patterns

### Semantic Token Classes

```tsx
// CORRECT - Use semantic tokens
className="bg-surface text-primary"
className="bg-surface-secondary border-primary"
className="bg-error text-error"
className="bg-success text-success"
className="text-secondary bg-primary"
```

### Common Semantic Tokens

| Category | Tokens |
|----------|--------|
| **Background** | `bg-surface`, `bg-surface-secondary`, `bg-primary`, `bg-error`, `bg-success` |
| **Text** | `text-primary`, `text-secondary`, `text-accent`, `text-error`, `text-success` |
| **Border** | `border-primary`, `border-error`, `border-surface` |

### With Class Composition

```tsx
// CORRECT - Semantic tokens in cn/clsx/cva
import { cn } from '@/lib/utils';

className={cn(
  "bg-surface text-primary",
  isActive && "bg-primary text-surface",
  hasError && "border-error text-error"
)}
```

### CVA Variants

```tsx
// CORRECT - Semantic tokens in cva
const buttonVariants = cva(
  "bg-surface text-primary border-primary", // Base
  {
    variants: {
      variant: {
        primary: "bg-primary text-surface",
        error: "bg-error text-surface",
        success: "bg-success text-surface",
      }
    }
  }
);
```

## Escape Hatches

When absolutely necessary (rare):

```tsx
// Line-level disable
// eslint-disable-next-line wescobar/no-raw-colors
className="bg-red-500" // Legacy code migration

// File-level disable (very rare)
/* eslint-disable wescobar/no-raw-colors */
```

**Use sparingly** - prefer fixing to disabling.

## Migration Examples

| Old (Forbidden) | New (Semantic) |
|-----------------|----------------|
| `bg-white` | `bg-surface` |
| `bg-gray-900` | `bg-surface-secondary` |
| `text-white` | `text-surface` (on dark bg) |
| `text-gray-900` | `text-primary` |
| `text-gray-500` | `text-secondary` |
| `border-gray-300` | `border-primary` |
| `bg-red-500` | `bg-error` |
| `bg-green-500` | `bg-success` |
| `text-blue-500` | `text-accent` |

## Project-Specific Tokens

**Check `docs/THEMING.md` or `src/index.css`** for the full list of available semantic tokens in this project. Token names may vary between projects.

## Integration with ESLint

The `no-raw-colors` ESLint rule enforces this at:
- Pre-commit hooks (blocks commit)
- IDE integration (inline errors)
- CI/CD pipeline

**Generate correct code from the start** to avoid fix cycles.

## Related Skills

- `validate-lint` - Run linting validation
- `quality-gate` - Complete quality checks including lint

## Validation

After writing styled code:
1. Check for any raw colors or non-semantic Tailwind classes
2. Replace with semantic tokens from the project's theme
3. If unsure, check `docs/THEMING.md` for available tokens
