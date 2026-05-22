---
name: shadcn-patterns
description: shadcn/ui component patterns including CVA variants, OKLCH theming, cn() utility, and composition. Use when adding shadcn components, building variant systems, or customizing themes.
context: fork
agent: frontend-ui-developer
version: 1.0.0
tags: [shadcn, ui, cva, variants, tailwind, theming, oklch, components]
user-invocable: false
---

# shadcn/ui Patterns

Beautifully designed, accessible components you own and customize.

## Core Pattern: CVA (Class Variance Authority)

Declarative, type-safe variant definitions:

```tsx
import { cva, type VariantProps } from 'class-variance-authority'

const buttonVariants = cva(
  // Base classes (always applied)
  'inline-flex items-center justify-center rounded-md font-medium transition-colors',
  {
    variants: {
      variant: {
        default: 'bg-primary text-primary-foreground hover:bg-primary/90',
        destructive: 'bg-destructive text-destructive-foreground',
        outline: 'border border-input bg-background hover:bg-accent',
        ghost: 'hover:bg-accent hover:text-accent-foreground',
      },
      size: {
        default: 'h-10 px-4 py-2',
        sm: 'h-9 px-3',
        lg: 'h-11 px-8',
        icon: 'h-10 w-10',
      },
    },
    compoundVariants: [
      { variant: 'outline', size: 'lg', className: 'border-2' },
    ],
    defaultVariants: {
      variant: 'default',
      size: 'default',
    },
  }
)

// Type-safe props
interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {}
```

## Core Pattern: cn() Utility

Combines `clsx` + `tailwind-merge` for conflict resolution:

```tsx
import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

// Usage - later classes win
cn('px-4 py-2', 'px-6') // => 'py-2 px-6'
cn('text-red-500', condition && 'text-blue-500')
```

## OKLCH Theming (2026 Standard)

Modern perceptually uniform color space:

```css
:root {
  --background: oklch(1 0 0);
  --foreground: oklch(0.145 0 0);
  --primary: oklch(0.205 0 0);
  --primary-foreground: oklch(0.985 0 0);
  --destructive: oklch(0.577 0.245 27.325);
  --border: oklch(0.922 0 0);
  --ring: oklch(0.708 0 0);
  --radius: 0.625rem;
}

.dark {
  --background: oklch(0.145 0 0);
  --foreground: oklch(0.985 0 0);
  --primary: oklch(0.985 0 0);
  --destructive: oklch(0.396 0.141 25.723);
}
```

**Why OKLCH?**
- Perceptually uniform (equal steps look equal)
- Better dark mode contrast
- Wide gamut support
- Format: `oklch(lightness chroma hue)`

## Component Extension Strategy

**Wrap, don't modify source:**

```tsx
import { Button as ShadcnButton } from '@/components/ui/button'

// Extend with new variants
const Button = React.forwardRef<
  React.ElementRef<typeof ShadcnButton>,
  React.ComponentPropsWithoutRef<typeof ShadcnButton> & {
    loading?: boolean
  }
>(({ loading, children, disabled, ...props }, ref) => (
  <ShadcnButton ref={ref} disabled={disabled || loading} {...props}>
    {loading && <Spinner className="mr-2" />}
    {children}
  </ShadcnButton>
))
```

## Quick Reference

```bash
# Add components
npx shadcn@latest add button
npx shadcn@latest add dialog

# Initialize in project
npx shadcn@latest init
```

## Key Decisions

| Decision | Recommendation |
|----------|----------------|
| Color format | OKLCH for perceptually uniform theming |
| Class merging | Always use cn() for Tailwind conflicts |
| Extending components | Wrap, don't modify source files |
| Variants | Use CVA for type-safe multi-axis variants |

## Related Skills

- `radix-primitives` - Underlying accessibility primitives
- `design-system-starter` - Design system patterns
- `biome-linting` - Code quality for components

## References

- [CVA Variant System](references/cva-variant-system.md) - CVA patterns
- [OKLCH Theming](references/oklch-theming.md) - Modern color space
- [cn() Utility](references/cn-utility-patterns.md) - Class merging
- [Component Extension](references/component-extension.md) - Extending components
- [Dark Mode](references/dark-mode-toggle.md) - next-themes integration
