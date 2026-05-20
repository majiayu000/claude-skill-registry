---
name: apply-design-system
description: Apply design tokens and system patterns correctly. Reference for semantic colors, spacing, typography, borders, and shadows. Never use arbitrary values.
---

# Apply Design System

Use design tokens exclusively. Never use arbitrary values (`[#hex]`, `[16px]`, etc.).

## Color Tokens

### Backgrounds
`bg-background`, `bg-card`, `bg-popover`, `bg-primary`, `bg-secondary`, `bg-muted`, `bg-accent`, `bg-destructive`

### Text
`text-foreground`, `text-muted-foreground`, `text-primary-foreground`, `text-secondary-foreground`, `text-accent-foreground`, `text-destructive-foreground`

### Borders
`border` (default), `border-input`, `border-ring`

## Spacing (Padding/Margin/Gap)

`0, 1, 2, 4, 6, 8, 12, 16, 20, 24` — e.g., `p-4`, `gap-6`, `space-y-4`

## Typography

- **Sizes**: `text-xs`, `text-sm`, `text-base`, `text-lg`, `text-xl`, `text-2xl`, `text-3xl`, `text-4xl`
- **Weights**: `font-normal`, `font-medium`, `font-semibold`, `font-bold`
- **Families**: `font-sans`, `font-heading`, `font-mono`

## Borders & Radius

`rounded-sm`, `rounded`, `rounded-md`, `rounded-lg`, `rounded-xl`, `rounded-full`

## Shadows

`shadow-sm`, `shadow`, `shadow-md`, `shadow-lg`, `shadow-xl`

## Common Patterns

**Card:** `bg-card text-card-foreground rounded-lg border shadow-sm p-6`

**Primary button:** `bg-primary text-primary-foreground hover:bg-primary/90 px-4 py-2 rounded-md font-medium`

**Input:** `flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm`

**Container:** `container mx-auto px-4 py-8`

## Using `cn()` for class merging

```tsx
import { cn } from '@acme/design-system/utils/style'

<div className={cn('base-styles', { 'conditional': variant === 'x' }, className)}>
```

## Responsive (mobile-first)

`md:` (768px+), `lg:` (1024px+), `xl:` (1280px+)

## Anti-Patterns

- `bg-[#FF0000]` — use semantic tokens
- `bg-red-500` — use semantic tokens
- `p-[16px]` — use `p-4`
- `style={{ ... }}` — use Tailwind classes
- `w-[250px]` — use `w-64` or similar

## When Tokens Don't Exist

1. Check for a close semantic token
2. Add to design tokens package (`packages/design-tokens/`)
3. Update Tailwind config
4. Document in `docs/typography-and-color.md`
