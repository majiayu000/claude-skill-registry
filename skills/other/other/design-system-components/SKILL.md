---
name: design-system-components
model: standard
description: Patterns for building design system components using Surface primitives, CVA variants, and consistent styling. Use when building reusable UI components that follow design token architecture. Triggers on Surface component, CVA, class-variance-authority, component variants, design tokens.
---

# Design System Components

Build reusable components that leverage design tokens with Surface primitives and CVA (class-variance-authority).


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install design-system-components
```


---

## When to Use

- Building component libraries with design tokens
- Need variant-based styling (size, color, state)
- Creating layered UI with consistent surfaces
- Want type-safe component APIs

---

## Pattern 1: Surface Primitive

Single component for all layered surfaces:

```tsx
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const surfaceVariants = cva(
  'rounded-lg backdrop-blur-sm transition-colors',
  {
    variants: {
      layer: {
        panel: 'bg-tone-cadet/40 border border-tone-jordy/10 shadow-card',
        tile: 'bg-tone-midnight/60 border border-tone-jordy/5',
        chip: 'bg-tone-cyan/10 border border-tone-cyan/20 rounded-full',
        deep: 'bg-tone-void/80',
        metric: 'bg-tone-cadet/20 border border-tone-jordy/8',
        glass: 'bg-glass-bg backdrop-blur-lg border border-glass-border',
      },
      interactive: {
        true: 'cursor-pointer hover:bg-tone-cadet/50 active:scale-[0.98]',
        false: '',
      },
      glow: {
        true: 'shadow-glow',
        false: '',
      },
    },
    defaultVariants: {
      layer: 'tile',
      interactive: false,
      glow: false,
    },
  }
);

interface SurfaceProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof surfaceVariants> {}

export function Surface({
  layer,
  interactive,
  glow,
  className,
  ...props
}: SurfaceProps) {
  return (
    <div
      className={cn(surfaceVariants({ layer, interactive, glow }), className)}
      {...props}
    />
  );
}
```

### Usage

```tsx
<Surface layer="panel" className="p-4">
  <h2>Dashboard</h2>
</Surface>

<Surface layer="chip" interactive>
  <span>Active</span>
</Surface>

<Surface layer="metric" glow>
  <span className="text-2xl">$1,234.56</span>
</Surface>
```

---

## Pattern 2: CVA Button Variants

```tsx
const buttonVariants = cva(
  'inline-flex items-center justify-center rounded-md font-medium transition-all focus-visible:outline-none focus-visible:ring-2 disabled:pointer-events-none disabled:opacity-50',
  {
    variants: {
      variant: {
        default: 'bg-primary text-primary-foreground hover:bg-primary/90',
        destructive: 'bg-destructive text-destructive-foreground hover:bg-destructive/90',
        outline: 'border border-input bg-background hover:bg-accent hover:text-accent-foreground',
        ghost: 'hover:bg-accent hover:text-accent-foreground',
        link: 'text-primary underline-offset-4 hover:underline',
        cyber: 'bg-gradient-to-r from-tone-cadet to-tone-azure text-white border border-tone-cyan/30 shadow-glow hover:shadow-glow-lg',
      },
      size: {
        default: 'h-10 px-4 py-2',
        sm: 'h-9 rounded-md px-3',
        lg: 'h-11 rounded-md px-8',
        icon: 'h-10 w-10',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'default',
    },
  }
);
```

---

## Pattern 3: Metric Display Component

```tsx
const metricVariants = cva(
  'font-mono tabular-nums',
  {
    variants: {
      size: {
        lg: 'text-3xl font-bold tracking-tight',
        md: 'text-xl font-semibold',
        sm: 'text-base font-medium',
      },
      trend: {
        positive: 'text-success',
        negative: 'text-destructive',
        neutral: 'text-foreground',
      },
    },
    defaultVariants: {
      size: 'md',
      trend: 'neutral',
    },
  }
);

interface MetricProps extends VariantProps<typeof metricVariants> {
  value: string | number;
  label?: string;
  prefix?: string;
  suffix?: string;
}

export function Metric({
  value,
  label,
  prefix = '',
  suffix = '',
  size,
  trend,
}: MetricProps) {
  return (
    <div className="flex flex-col">
      {label && (
        <span className="text-xs uppercase tracking-wider text-muted-foreground mb-1">
          {label}
        </span>
      )}
      <span className={cn(metricVariants({ size, trend }))}>
        {prefix}{value}{suffix}
      </span>
    </div>
  );
}
```

---

## Pattern 4: Card with Header

```tsx
interface CardProps {
  title?: string;
  description?: string;
  action?: React.ReactNode;
  children: React.ReactNode;
}

export function Card({ title, description, action, children }: CardProps) {
  return (
    <Surface layer="panel" className="flex flex-col">
      {(title || action) && (
        <div className="flex items-center justify-between px-4 py-3 border-b border-tone-jordy/10">
          <div>
            {title && (
              <h3 className="font-display text-sm font-medium">{title}</h3>
            )}
            {description && (
              <p className="text-xs text-muted-foreground">{description}</p>
            )}
          </div>
          {action}
        </div>
      )}
      <div className="p-4">{children}</div>
    </Surface>
  );
}
```

---

## Pattern 5: Badge/Chip Variants

```tsx
const badgeVariants = cva(
  'inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium transition-colors',
  {
    variants: {
      variant: {
        default: 'bg-primary/10 text-primary border border-primary/20',
        success: 'bg-success/10 text-success border border-success/20',
        warning: 'bg-warning/10 text-warning border border-warning/20',
        destructive: 'bg-destructive/10 text-destructive border border-destructive/20',
        outline: 'border border-input text-foreground',
      },
    },
    defaultVariants: {
      variant: 'default',
    },
  }
);
```

---

## Pattern 6: Composing Variants

Combine CVA with conditional classes:

```tsx
function StatusIndicator({ 
  status, 
  size = 'md' 
}: { 
  status: 'online' | 'offline' | 'away';
  size?: 'sm' | 'md' | 'lg';
}) {
  const sizeClasses = {
    sm: 'size-2',
    md: 'size-3',
    lg: 'size-4',
  };

  const statusClasses = {
    online: 'bg-success animate-pulse',
    offline: 'bg-muted-foreground',
    away: 'bg-warning',
  };

  return (
    <span
      className={cn(
        'rounded-full',
        sizeClasses[size],
        statusClasses[status]
      )}
    />
  );
}
```

---

## Related Skills

- **Meta-skill:** [ai/skills/meta/design-system-creation/](../../meta/design-system-creation/) — Complete design system workflow
- [distinctive-design-systems](../distinctive-design-systems/) — Token architecture and aesthetic foundations
- [loading-state-patterns](../loading-state-patterns/) — Skeleton components for loading states

---

## NEVER Do

- **Build custom card containers** — Use Surface primitive
- **Hardcode colors in components** — Use design tokens
- **Skip variant types** — CVA provides type safety
- **Mix styling approaches** — Pick CVA or cn(), not random inline styles
- **Forget default variants** — Components should work without props

---

## Quick Reference

```tsx
// 1. Define variants with CVA
const variants = cva('base-classes', {
  variants: {
    size: { sm: '...', md: '...', lg: '...' },
    color: { primary: '...', secondary: '...' },
  },
  defaultVariants: { size: 'md', color: 'primary' },
});

// 2. Type props from variants
interface Props extends VariantProps<typeof variants> {}

// 3. Apply in component
<div className={cn(variants({ size, color }), className)} />
```
