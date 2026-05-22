---
name: interactive-states
description: Interactive states for UI elements - hover, active, focus, disabled, loading. Use when implementing button states, form field states, or interactive feedback.
allowed-tools: Read, Write, Edit, Glob, Grep
user-invocable: true
---

# Interactive States

Complete state system for interactive elements.

## Agent Workflow (MANDATORY)

Before implementation:
1. **fuse-ai-pilot:explore-codebase** - Check existing state patterns
2. **fuse-ai-pilot:research-expert** - Framer Motion state animations

After: Run **fuse-ai-pilot:sniper** for validation.

## State Flow

```
Default → Hover → Pressed/Active → Focus → Disabled → Loading
```

## Button States

```tsx
import { motion } from "framer-motion";

export function Button({ children, disabled, isLoading }) {
  return (
    <motion.button
      // Hover state (50-100ms)
      whileHover={{ scale: 1.02 }}
      // Pressed state (100-150ms)
      whileTap={{ scale: 0.98 }}
      transition={{ duration: 0.1 }}
      disabled={disabled || isLoading}
      className={cn(
        // Default
        "px-4 py-2 rounded-lg bg-primary text-primary-foreground",
        "font-medium transition-colors",
        // Focus visible
        "focus:outline-none focus-visible:ring-2 focus-visible:ring-primary/50",
        // Disabled
        "disabled:opacity-50 disabled:cursor-not-allowed disabled:pointer-events-none",
      )}
    >
      {isLoading ? <Spinner className="h-4 w-4 animate-spin" /> : children}
    </motion.button>
  );
}
```

## State Timing Guide

| State | Duration | Easing |
|-------|----------|--------|
| Hover in | 50-100ms | ease-out |
| Hover out | 150ms | ease-in |
| Press | 100-150ms | ease-out |
| Focus | instant | - |
| Loading | - | linear (spin) |

## Card Hover States

```tsx
<motion.div
  className="bg-surface rounded-2xl p-6 shadow-md transition-shadow"
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  whileHover={{
    y: -4,
    boxShadow: "0 25px 50px -12px rgb(0 0 0 / 0.15)",
  }}
  transition={{ duration: 0.2 }}
>
  {children}
</motion.div>
```

## Input Field States

```tsx
const inputStates = {
  default: "border-border bg-surface",
  focus: "border-primary ring-2 ring-primary/20",
  valid: "border-success bg-success/5",
  error: "border-destructive bg-destructive/5",
  disabled: "border-muted bg-muted/50 cursor-not-allowed",
};

<input
  className={cn(
    "w-full px-4 py-3 rounded-lg border transition-all",
    "focus:outline-none",
    inputStates[state]
  )}
/>
```

## Focus States (Accessibility)

```tsx
/* Visible focus ring */
className="focus:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2"

/* Focus within (for groups) */
className="focus-within:ring-2 focus-within:ring-primary"
```

## Loading States

```tsx
/* Spinner button */
<button disabled={isLoading}>
  {isLoading ? (
    <Loader2 className="h-4 w-4 animate-spin" />
  ) : (
    "Submit"
  )}
</button>

/* Skeleton loading */
<div className="animate-pulse">
  <div className="h-4 bg-muted rounded w-3/4" />
  <div className="h-4 bg-muted rounded w-1/2 mt-2" />
</div>

/* Progress state */
<motion.div
  className="h-1 bg-primary rounded-full"
  initial={{ width: 0 }}
  animate={{ width: `${progress}%` }}
/>
```

## Interactive Feedback Patterns

```tsx
/* Ripple effect on click */
const [ripple, setRipple] = useState(null);

<button
  onClick={(e) => {
    const rect = e.currentTarget.getBoundingClientRect();
    setRipple({ x: e.clientX - rect.left, y: e.clientY - rect.top });
  }}
>
  {ripple && (
    <motion.span
      className="absolute bg-white/30 rounded-full"
      initial={{ width: 0, height: 0 }}
      animate={{ width: 100, height: 100, opacity: 0 }}
      style={{ left: ripple.x, top: ripple.y }}
    />
  )}
</button>

/* Checkbox toggle */
<motion.div
  animate={{ scale: checked ? 1 : 0 }}
  transition={{ type: "spring", stiffness: 500 }}
>
  <Check className="h-4 w-4" />
</motion.div>
```

## State Composition with CVA

```tsx
const buttonVariants = cva("...", {
  variants: {
    state: {
      default: "",
      loading: "opacity-80 pointer-events-none",
      success: "bg-success text-success-foreground",
      error: "bg-destructive text-destructive-foreground",
    },
  },
});
```

## Validation

```
[ ] All 5 states defined (default, hover, active, focus, disabled)
[ ] Loading state with spinner/skeleton
[ ] Hover timing 50-100ms
[ ] Focus visible for keyboard users
[ ] Disabled prevents all interaction
[ ] Motion respects prefers-reduced-motion
```

## References

- `../../references/buttons-guide.md` - Button states detail
- `../../references/forms-guide.md` - Form field states
- `../../references/motion-patterns.md` - Animation timings
