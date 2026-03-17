---
name: tailwind
description: |
  Applies utility-first CSS styling with Tailwind and custom theme configuration.
  Use when: Styling components, implementing dark mode themes, creating animations,
  using glassmorphism effects, or working with shadcn/ui components.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# Tailwind Skill

This codebase implements a **dark cinematic design system** using Tailwind CSS 3.x with HSL-based CSS custom properties for runtime theme switching across 11 theme variants. All styling flows through the `cn()` utility combining `clsx` and `tailwind-merge`.

## Quick Start

### Class Composition with cn()

```typescript
// src/lib/utils.ts - ALWAYS use this for class merging
import { cn } from "@/lib/utils";

// Conditional classes
<div className={cn(
  "base-classes",
  isActive && "active-styles",
  className // Allow prop overrides
)} />
```

### HSL Color Variables

```typescript
// Use semantic color tokens, not raw colors
<div className="bg-primary text-primary-foreground" />
<div className="border-border bg-card" />
<div className="text-muted-foreground" />

// Opacity modifiers work with HSL
<div className="bg-primary/20 border-border/50" />
```

### CVA Variant Components

```typescript
import { cva, type VariantProps } from "class-variance-authority";

const buttonVariants = cva(
  "inline-flex items-center justify-center transition-all duration-300",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        outline: "border border-border hover:bg-card",
      },
      size: {
        default: "h-10 px-5 rounded-lg",
        sm: "h-9 px-4 text-xs",
      },
    },
    defaultVariants: { variant: "default", size: "default" },
  }
);
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| Color tokens | HSL variables via `hsl(var(--name))` | `bg-primary`, `text-foreground` |
| Glass effects | Backdrop blur + transparency | `glass`, `glass-subtle` |
| Book covers | Shadow + shine overlay | `book-cover`, `book-cover-glow` |
| Status badges | Semantic color classes | `status-requested`, `status-available` |
| Animations | Radix-aware keyframes | `animate-fade-in-up`, `animate-glow` |

## Common Patterns

### Hover Effects with Transform

```typescript
// Scale + shadow on hover
<div className="transition-transform duration-500 group-hover:scale-105" />

// Reveal on hover with staggered animation
<div className="translate-y-2 opacity-0 group-hover:translate-y-0 group-hover:opacity-100 transition-[transform,opacity] duration-300" />
```

### Glassmorphism (Desktop Only)

```typescript
// Glass effect - disabled on mobile for performance
<div className="glass" />        // bg-card/60 backdrop-blur-xl
<div className="glass-subtle" /> // bg-card/40 backdrop-blur-lg
<div className="glass-strong" /> // bg-card/80 backdrop-blur-2xl
```

## See Also

- [patterns](references/patterns.md) - Component styling patterns, anti-patterns
- [workflows](references/workflows.md) - Theme customization, adding new components

## Related Skills

- See the **shadcn-ui** skill for component primitives
- See the **react** skill for component patterns
- See the **typescript** skill for type-safe variants with CVA