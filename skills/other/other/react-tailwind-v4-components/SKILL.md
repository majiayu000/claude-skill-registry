---
name: react-tailwind-v4-components
description: Use when building React components with Tailwind CSS v4, shadcn/ui, or Radix primitives. Use when writing className strings, cva variants, or CSS variable values in Tailwind.
---

# React Components with Tailwind v4 + shadcn/ui

## Overview

Reference for building React components with Tailwind CSS v4, shadcn/ui, and Radix primitives.

## Tailwind v4 Syntax

### CSS Variables: Parentheses Syntax

```tsx
// Reading CSS variables in class names
<div className="bg-(--brand-color) text-(--text-color) ring-(--accent)">
```

**Use parentheses `(--var)` to reference CSS variables.** This works everywhere — className props, cva() strings, and arbitrary values.

### Opacity Modifiers with CSS Variables

```tsx
<div className="bg-(--brand-color)/10 border-(--accent)/50 text-(--heading)/80">
```

### Setting CSS Variables Per Variant

Tailwind v4 exposes all theme values as CSS variables: `--color-blue-500`, `--spacing-4`, `--radius-lg`, etc. Use `var(--color-*)` to reference them.

**Option A: data-attribute + CSS (preferred for many variants):**

```css
/* In your CSS file */
[data-variant="info"] { --alert-accent: var(--color-blue-500); }
[data-variant="success"] { --alert-accent: var(--color-green-500); }
[data-variant="warning"] { --alert-accent: var(--color-amber-500); }
```

```tsx
// Component uses the CSS variable, variant sets it via data attribute
const alertVariants = cva("border-(--alert-accent) bg-(--alert-accent)/10", {
  variants: {
    variant: {
      info: "text-blue-900",
      success: "text-green-900",
      warning: "text-amber-900",
    },
  },
})

export function Alert({ variant, className, ...props }: AlertProps) {
  return <div data-variant={variant} className={cn(alertVariants({ variant }), className)} {...props} />
}
```

**Option B: inline style (for dynamic values):**

```tsx
const fillColors: Record<string, string> = {
  success: "var(--color-green-500)",
  danger: "var(--color-red-500)",
}

<div
  className="bg-(--fill-color) border-(--fill-color)/50"
  style={{ "--fill-color": fillColors[variant] } as React.CSSProperties}
/>
```

**Option C: Tailwind utilities directly (simplest, when you don't need CSS var indirection):**

```tsx
const variants = cva("base", {
  variants: {
    variant: {
      info: "border-blue-200 bg-blue-50 text-blue-900",
      error: "border-red-200 bg-red-50 text-red-900",
    },
  },
})
```

### Utility Size Scale

**Size scale from smallest to largest:** `-xs` → `-sm` → (default/base) → `-md` → `-lg` → `-xl`

| Utility | Smallest | Small | Base | Notes |
|---------|----------|-------|------|-------|
| `shadow-*` | `shadow-xs` | `shadow-sm` | `shadow` | Use `-xs` for subtle shadows |
| `rounded-*` | `rounded-xs` | `rounded-sm` | `rounded` | Use `-xs` for subtle rounding |
| `blur-*` | `blur-xs` | `blur-sm` | `blur` | |
| `drop-shadow-*` | `drop-shadow-xs` | `drop-shadow-sm` | `drop-shadow` | |
| `backdrop-blur-*` | `backdrop-blur-xs` | `backdrop-blur-sm` | `backdrop-blur` | |

**Ring width:** `ring` = 1px. Use `ring-2`, `ring-3`, etc. for thicker rings.

### Important Modifier

Append **!** suffix for important — e.g. `text-red-500` becomes text-red-500**!**

### Opacity Utilities

Use slash modifiers: `bg-black/50`, `text-white/80`, `ring-blue-500/30`

### Inset Shadows and Rings

```tsx
// Inset shadow
<div className="inset-shadow-sm inset-shadow-black/10">

// Inset ring (inner border)
<div className="inset-ring inset-ring-black/10">
```

### Focus Ring Patterns

```tsx
// Ring with gap from element:
<input className="focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-(--ring-color)" />

// Flush ring (no gap):
<input className="focus-visible:ring-2 focus-visible:ring-(--ring-color)" />

// Inset ring:
<input className="focus-visible:inset-ring-2 focus-visible:inset-ring-(--ring-color)" />
```

### Theme Configuration

```css
@import "tailwindcss";

@theme inline {
  --color-primary: var(--primary);
  --radius-lg: var(--radius);
}
```

Use `@theme inline` when variables reference other `var()` values. Use plain `@theme` for static values like `--color-brand: oklch(0.7 0.15 200);`.

**Theme CSS variables:**

| Theme value | CSS variable pattern | Example |
|-------------|---------------------|---------|
| Colors | `--color-{name}-{shade}` | `var(--color-blue-500)` |
| Spacing | `--spacing-{value}` | `var(--spacing-4)` |
| Fonts | `--font-{name}` | `var(--font-sans)` |
| Radii | `--radius-{size}` | `var(--radius-lg)` |
| Shadows | `--shadow-{size}` | `var(--shadow-sm)` |
| Breakpoints | `--breakpoint-{name}` | `var(--breakpoint-xl)` |

### Container Queries (Built-in)

```tsx
<div className="@container">
  <div className="@sm:flex @md:grid @lg:grid-cols-3">
```

### Dynamic Values (No Config Needed)

```tsx
<div className="mt-13 w-[347px] z-73">  // Works without defining in config
```

## Component Patterns

### Always Use `cn()` for Class Merging

```tsx
// lib/utils.ts — canonical cn() implementation
import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"
export function cn(...inputs: ClassValue[]) { return twMerge(clsx(inputs)) }
```

```tsx
import { cn } from "@/lib/utils"

// CORRECT
<div className={cn("base-classes", active && "bg-active", className)}>

// WRONG — template literals cause Tailwind conflicts
<div className={`base-classes ${active ? 'bg-active' : ''}`}>
```

### Variants with `cva`

```tsx
import { cva, type VariantProps } from "class-variance-authority"

const cardVariants = cva(
  "rounded-sm border p-4 transition-colors",  // base
  {
    variants: {
      variant: {
        default: "border-border bg-card",
        destructive: "border-destructive/50 bg-destructive/10",
      },
      size: {
        sm: "p-2 text-sm",
        default: "p-4",
        lg: "p-6 text-lg",
      },
    },
    defaultVariants: { variant: "default", size: "default" },
  }
)

interface CardProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof cardVariants> {}

export function Card({ className, variant, size, ...props }: CardProps) {
  return <div className={cn(cardVariants({ variant, size, className }))} {...props} />
}
```

### Extending shadcn Components (Wrap, Don't Modify)

```tsx
import { Button, type ButtonProps } from "./button"

export function PrimaryButton({ className, ...props }: ButtonProps) {
  return <Button className={cn("bg-brand-500 hover:bg-brand-600", className)} {...props} />
}
```

**DO:** Customize via `className`, wrap to extend, use variant system.
**DON'T:** Modify shadcn source for one-off changes, override Radix accessibility props, use inline styles.

### Radix `asChild` / Slot Pattern

```tsx
import { Slot } from "@radix-ui/react-slot"

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  asChild?: boolean
}

function Button({ asChild = false, ...props }: ButtonProps) {
  const Comp = asChild ? Slot : "button"
  return <Comp {...props} />
}

// Renders as <a> with button styles
<Button asChild><a href="/home">Home</a></Button>
```

### Forms: react-hook-form + zod

```tsx
const schema = z.object({ email: z.string().email(), name: z.string().min(2) })
type FormData = z.infer<typeof schema>

const form = useForm<FormData>({ resolver: zodResolver(schema) })

// Compose with shadcn form primitives:
<Form {...form}>
  <FormField control={form.control} name="email" render={({ field }) => (
    <FormItem>
      <FormLabel>Email</FormLabel>
      <FormControl><Input placeholder="you@example.com" {...field} /></FormControl>
      <FormMessage />
    </FormItem>
  )} />
</Form>
```

### Loading & Error States

```tsx
// Component-level
if (isLoading) return <Skeleton className="h-32 w-full" />
if (error) return <Alert variant="destructive"><AlertDescription>{error.message}</AlertDescription></Alert>

// Button loading
<Button disabled={isLoading}>
  {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
  {isLoading ? "Saving..." : "Save"}
</Button>
```

## File Organization

```
components/
  ui/           # shadcn/ui base components
  forms/        # Form-specific components
  layout/       # Header, Sidebar, etc.
  [feature]/    # Feature-specific components
```

## Accessibility Checklist

- Interactive elements keyboard accessible
- Visible focus states (`focus-visible:outline-2 focus-visible:outline-offset-2`)
- Color contrast WCAG AA (4.5:1)
- Form fields have labels
- Error messages announced to screen readers
- Loading states use `aria-busy`
- Decorative icons have `aria-hidden="true"`

## Common Mistakes

| Incorrect | Correct | Why |
|-----------|---------|-----|
| `bg-[--brand]` | `bg-(--brand)` | Use parentheses for CSS variables |
| `bg-[var(--brand)]` | `bg-(--brand)` | No need for `var()` wrapper |
| `ring` for 3px ring | `ring-3` | `ring` = 1px width |
| `ring-offset-2` | `outline-2 outline-offset-2` | Use outline for ring-with-gap |
| prefix **!** (wrong) | suffix **!** after class | Important modifier is suffix, not prefix |
| `shadow-inset` | `inset-shadow-sm` | Separate utility namespace |
| `outline-none` to hide | `outline-hidden` | `outline-none` sets style:none |
| `` `base ${x}` `` | `cn("base", x)` | Use cn() for class merging |
| `style={{ color: "var(--x)" }}` | `className="text-(--x)"` | Read CSS vars with Tailwind |
| `[--var:theme(colors.x.y)]` | data-attr + CSS | Set CSS vars via CSS or inline style |
| `theme(colors.blue.500)` | `var(--color-blue-500)` | Use CSS variables directly |
| Modifying shadcn source | Wrap the component | Preserve upgradeability |
| Overriding Radix `aria-*` | Don't | Radix handles accessibility |

## Quick Self-Check

**Before committing, verify:**

- CSS variables use parentheses: `(--var)` not `[--var]`
- Smallest sizes use `-xs`: `shadow-xs`, `rounded-xs`
- Ring with gap uses `outline-offset-*` not `ring-offset-*`
- Important modifier is suffix (append **!**), not prefix
- Inset shadows use `inset-shadow-*` namespace
- Hide outlines with `outline-hidden` not `outline-none`
- Class strings use `cn()` not template literals

**Inline `style` IS acceptable for SETTING CSS custom properties** (e.g., `style={{ "--fill": "var(--color-blue-500)" }}`). Use Tailwind syntax for reading them.
