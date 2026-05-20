---
name: design-tokens
description: |
  Design tokens naming and creation rules for Wythm mobile app.

  **Use this skill when:**
  - Creating or renaming design tokens (colors, spacing, typography)
  - Replacing hardcoded colors/styles with tokens
  - Reviewing PRs where styles or colors are touched
  - Adding new UI components that need theming

  **Goal:**
  - Consistent naming across design and code
  - Tokens are discoverable, composable, and theme-aware
---

# Design Tokens

This skill ensures consistent token naming and usage across Wythm's codebase.

## Token Architecture

Wythm uses a **two-layer system**:

1. **Primitives** (`colors.primitives.ts`) - Raw hex values. The ONLY place for color literals.
2. **Semantic Tokens** (`colors.semantic.ts`) - Theme-aware tokens organized by usage.

## Quick Reference

### Token Structure (dot notation)

```
color.{usage}.{variant}
```

In code: `theme.colors.{usage}.{variant}`

| Usage        | Examples                                                         |
| ------------ | ---------------------------------------------------------------- |
| `text`       | `color.text.base`, `color.text.secondary`, `color.text.on-brand` |
| `background` | `color.background.base`, `color.background.brand`                |
| `border`     | `color.border.base`, `color.border.secondary`                    |
| `field`      | `color.field.background`, `color.field.border-danger`            |
| `icon`       | `color.icon.brand`, `color.icon.on-brand`                        |

### Variant Patterns

| Pattern            | Meaning                              |
| ------------------ | ------------------------------------ |
| `base`             | Default variant                      |
| `secondary`        | Less prominent                       |
| `tertiary`         | Least prominent                      |
| `brand`            | Brand color applied                  |
| `danger`           | Error/destructive state              |
| `on-brand`         | Used ON brand-colored background     |
| `{element}-disabled` | Disabled state (field only)        |

## Critical Rules

### DO

- Use `theme.colors.{usage}.{variant}` in all components
- Add new tokens to BOTH `light` and `dark` schemes
- Follow dot notation naming: `color.{usage}.{variant}`
- Use kebab-case for multi-word variants: `on-brand`, `border-danger`
- Check for existing tokens before creating new ones

### DON'T

- Use hex literals outside `colors.primitives.ts`
- Create deeply nested tokens (max 2 levels)
- Use `on-default` (use `base` instead)
- Add tokens to only one color scheme
- Use camelCase in token names (use kebab-case: `on-brand` not `onBrand`)

## File Locations

| File | Purpose |
| ---- | ------- |
| `src/shared/theme/tokens/colors.primitives.ts` | Raw hex colors |
| `src/shared/theme/tokens/colors.semantic.ts` | Semantic tokens |
| `src/shared/theme/types.ts` | TypeScript types |

## When to Read Full Reference

Load `references/token-grammar.md` when:

- Creating a new usage category (beyond text/background/border/field/icon)
- Adding a new sentiment color (success, warning, info)
- Understanding the complete token creation workflow
- Reviewing naming convention edge cases

## Checklist for New Tokens

1. [ ] Does similar token already exist? (search `colors.semantic.ts`)
2. [ ] Is raw value needed? (add to `colors.primitives.ts`)
3. [ ] Added to correct usage category?
4. [ ] Uses dot notation with kebab-case? (`color.text.on-brand`)
5. [ ] Added to BOTH light and dark schemes?
6. [ ] Updated TypeScript types if new keys added?
7. [ ] Component uses `theme.colors.X.Y` not hex literal?

## Dot Notation to Code Mapping

| Dot notation (design)     | TypeScript (code)         |
| ------------------------- | ------------------------- |
| `color.text.base`         | `theme.colors.text.base`  |
| `color.text.on-brand`     | `theme.colors.text.onBrand` |
| `color.field.border-danger` | `theme.colors.field.borderDanger` |

**Rule**: Dot notation uses kebab-case, TypeScript uses camelCase for object keys.
