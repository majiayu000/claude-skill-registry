---
name: component-variants
description: Use when creating multi-style components, variant props, or style switching. Covers Glass, Outline, and Flat styles with CVA.
versions:
  cva: "1.x"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep
related-skills: glassmorphism-advanced, generating-components
---

# Component Variants

## Agent Workflow (MANDATORY)

Before implementation, use `TeamCreate` to spawn 3 agents:

1. **fuse-ai-pilot:explore-codebase** - Check existing variant patterns
2. **fuse-ai-pilot:research-expert** - cva/class-variance-authority docs

After: Run **fuse-ai-pilot:sniper** for validation.

---

## Overview

| Style | Characteristics | Use Case |
|-------|-----------------|----------|
| **Glass** | Blur + transparency + glow | Premium, modern, hero |
| **Outline** | Border only, no fill | Secondary actions |
| **Flat** | Solid color, no effects | Dense UI, fallback |

---

## Quick Reference

### CVA Card Variants

```tsx
import { cva, type VariantProps } from "class-variance-authority";

const cardVariants = cva(
  "rounded-2xl p-6 transition-all duration-200",
  {
    variants: {
      variant: {
        glass: [
          "bg-white/80 backdrop-blur-xl",
          "border border-white/20",
          "shadow-xl shadow-black/5",
        ],
        outline: [
          "bg-transparent",
          "border-2 border-primary/30",
          "hover:border-primary/50",
        ],
        flat: [
          "bg-surface",
          "border border-border",
        ],
      },
    },
    defaultVariants: {
      variant: "glass",
    },
  }
);
```

### Button Variants

```tsx
const buttonVariants = cva(
  "inline-flex items-center justify-center font-medium transition-all",
  {
    variants: {
      variant: {
        glass: "bg-white/20 backdrop-blur-md border border-white/30",
        outline: "bg-transparent border-2 border-primary text-primary",
        flat: "bg-primary text-primary-foreground",
      },
    },
  }
);
```

### Dark Mode Per Variant

```tsx
const glassVariant = {
  light: "bg-white/80 backdrop-blur-xl border-white/20",
  dark: "bg-black/40 backdrop-blur-xl border-white/10",
};

// Tailwind
className="bg-white/80 dark:bg-black/40 backdrop-blur-xl"
```

---

## Validation Checklist

```
[ ] All 3 variants defined (glass, outline, flat)
[ ] CVA or similar variant system used
[ ] Dark mode handled per variant
[ ] Default variant specified
[ ] Hover states per variant
```

---

## Best Practices

### DO
- Use CVA for type-safe variants
- Define all three styles consistently
- Handle dark mode per variant
- Add hover/focus states

### DON'T
- Mix variant systems
- Forget default variant
- Skip dark mode
- Ignore hover states
