---
name: design-system-patterns
description: "Use when building component libraries, choosing headless UI primitives, designing component APIs, or implementing theming and design tokens."
---

# Design System Patterns

## Headless Component Libraries

| Library | Framework | Bundle | Styling | Accessibility |
|---|---|---|---|---|
| Radix UI | React | Per-component | Unstyled | Full WAI-ARIA |
| Headless UI | React/Vue | ~10kb | Unstyled | Full WAI-ARIA |
| Ark UI | React/Vue/Solid | Per-component | Unstyled | Full WAI-ARIA |
| React Aria | React | Per-hook | Unstyled | Full WAI-ARIA |

**Default**: Radix UI for React projects needing broad primitive coverage. Headless UI for simpler needs or Vue support.

## Component API Design

### Compound Components

```typescript
// Expose composable parts — consumer controls layout
const Select = { Root, Trigger, Content, Item, Value }

// Usage: full layout control
<Select.Root value={val} onValueChange={setVal}>
  <Select.Trigger><Select.Value placeholder="Pick one" /></Select.Trigger>
  <Select.Content>
    {items.map(i => <Select.Item key={i.value} value={i.value}>{i.label}</Select.Item>)}
  </Select.Content>
</Select.Root>
```

### Polymorphic `as` Prop

```typescript
type PolymorphicProps<E extends React.ElementType, P = {}> = P &
  Omit<React.ComponentPropsWithRef<E>, keyof P> & { as?: E }

function Box<E extends React.ElementType = 'div'>({ as, ...props }: PolymorphicProps<E>) {
  const Comp = as || 'div'
  return <Comp {...props} />
}

// Renders as <a> with anchor props
<Box as="a" href="/about">About</Box>
```

## Variant System (CVA)

```typescript
import { cva, type VariantProps } from 'class-variance-authority'

const badge = cva('inline-flex items-center rounded-full font-medium', {
  variants: {
    variant: {
      default: 'bg-primary/10 text-primary',
      success: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
      warning: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200',
      error: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200',
    },
    size: { sm: 'px-2 py-0.5 text-xs', md: 'px-2.5 py-0.5 text-sm', lg: 'px-3 py-1 text-base' },
  },
  defaultVariants: { variant: 'default', size: 'md' },
})

export type BadgeProps = React.HTMLAttributes<HTMLSpanElement> & VariantProps<typeof badge>
export function Badge({ className, variant, size, ...props }: BadgeProps) {
  return <span className={cn(badge({ variant, size }), className)} {...props} />
}
```

## Design Tokens

```css
/* Token hierarchy: primitive → semantic → component */
:root {
  /* Primitives */
  --color-blue-500: 217 91% 60%;
  --color-gray-100: 220 14% 96%;

  /* Semantic */
  --color-primary: var(--color-blue-500);
  --color-surface: var(--color-gray-100);

  /* Component */
  --button-bg: hsl(var(--color-primary));
  --card-bg: hsl(var(--color-surface));

  /* Spacing scale (4px base) */
  --space-1: 0.25rem; --space-2: 0.5rem; --space-3: 0.75rem;
  --space-4: 1rem; --space-6: 1.5rem; --space-8: 2rem;

  /* Typography */
  --font-sans: 'Inter', system-ui, sans-serif;
  --text-sm: 0.875rem; --text-base: 1rem; --text-lg: 1.125rem;
}

.dark {
  --color-primary: 217 91% 70%;
  --color-surface: 220 14% 14%;
}
```

## Gotchas

- **Style encapsulation**: CSS Modules or Tailwind scoping avoid global class collisions; CSS-in-JS adds runtime cost
- **SSR + CSS-in-JS**: Libraries like styled-components need server-side style extraction; prefer CSS variables for zero-JS theming
- **Accessibility defaults**: Headless libraries handle ARIA; never override `role` or `aria-*` attributes they set
- **Prop API bloat**: Prefer compound components over deeply nested config objects -- easier to extend and tree-shake
- **Token naming**: Use semantic names (`--color-primary`) not visual (`--color-blue`) -- enables theming

## Cross-References

- **frontend:tailwind-design-system** -- Tailwind-specific token config, CVA patterns, and dark mode setup
- **frontend:accessibility-testing** -- WCAG compliance testing for component libraries
