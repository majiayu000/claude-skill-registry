---
name: interactive-states
description: Use when implementing button states, form field states, or interactive feedback. Covers hover, active, focus, disabled, loading states.
versions:
  framer-motion: "11"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep
related-skills: adding-animations, generating-components
---

# Interactive States

## Agent Workflow (MANDATORY)

Before implementation, use `TeamCreate` to spawn 3 agents:

1. **fuse-ai-pilot:explore-codebase** - Check existing state patterns
2. **fuse-ai-pilot:research-expert** - Framer Motion state animations

After: Run **fuse-ai-pilot:sniper** for validation.

---

## Overview

| State | Visual | Timing |
|-------|--------|--------|
| Default | Base appearance | - |
| Hover | Scale/color change | 50-100ms |
| Pressed | Scale down | 100-150ms |
| Focus | Ring outline | instant |
| Disabled | Opacity 50% | - |
| Loading | Spinner | - |

---

## Quick Reference

### Button States

```tsx
<motion.button
  whileHover={{ scale: 1.02 }}
  whileTap={{ scale: 0.98 }}
  transition={{ duration: 0.1 }}
  className={cn(
    "px-4 py-2 rounded-lg bg-primary",
    "focus:outline-none focus-visible:ring-2",
    "disabled:opacity-50 disabled:cursor-not-allowed",
  )}
>
  {isLoading ? <Spinner /> : children}
</motion.button>
```

### Card Hover

```tsx
<motion.div
  whileHover={{
    y: -4,
    boxShadow: "0 25px 50px -12px rgb(0 0 0 / 0.15)",
  }}
  transition={{ duration: 0.2 }}
>
```

### Input States

```tsx
const inputStates = {
  default: "border-border bg-surface",
  focus: "border-primary ring-2 ring-primary/20",
  valid: "border-success bg-success/5",
  error: "border-destructive bg-destructive/5",
  disabled: "border-muted bg-muted/50 cursor-not-allowed",
};
```

### Focus Visible

```tsx
className="focus:outline-none focus-visible:ring-2 focus-visible:ring-primary"
```

### Loading State

```tsx
<button disabled={isLoading}>
  {isLoading ? (
    <Loader2 className="h-4 w-4 animate-spin" />
  ) : (
    "Submit"
  )}
</button>
```

---

## Validation Checklist

```
[ ] All 5 states defined (default, hover, active, focus, disabled)
[ ] Loading state with spinner
[ ] Hover timing 50-100ms
[ ] Focus visible for keyboard users
[ ] Disabled prevents interaction
```

---

## Best Practices

### DO
- Use Framer Motion for hover/tap
- Visible focus for accessibility
- Spinner for loading states
- Consistent timing across app

### DON'T
- Skip focus states
- Forget loading feedback
- Use slow animations (>200ms)
- Remove outline without replacement
