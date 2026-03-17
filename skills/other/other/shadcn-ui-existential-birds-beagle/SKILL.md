---
name: shadcn-ui
description: shadcn/ui component patterns with Radix primitives and Tailwind styling. Use when building UI components, using CVA variants, implementing compound components, or styling with data-slot attributes. Triggers on shadcn, cva, cn(), data-slot, Radix, Button, Card, Dialog, VariantProps.
---

# shadcn/ui Component Development

## Contents

- [CLI Commands](#cli-commands) - Installing and adding components
- [Quick Reference](#quick-reference) - cn(), basic CVA pattern
- [Component Anatomy](#component-anatomy) - Props typing, asChild, data-slot
- [Component Patterns](#component-patterns) - Compound components
- [Styling Techniques](#styling-techniques) - CVA variants, modern CSS selectors, accessibility states
- [Decision Tables](#decision-tables) - When to use CVA, compound components, asChild, Context
- [Common Patterns](#common-patterns) - Form elements, dialogs, sidebars
- [Reference Files](#reference-files) - Full implementations and advanced patterns

## CLI Commands

### Initialize shadcn/ui

```bash
npx shadcn@latest init
```

This creates a `components.json` configuration file and sets up:
- Tailwind CSS configuration
- CSS variables for theming
- cn() utility function
- Required dependencies

### Add Components

```bash
# Add a single component
npx shadcn@latest add button

# Add multiple components
npx shadcn@latest add button card dialog

# Add all available components
npx shadcn@latest add --all
```

**Important:** The package name changed in 2024:
- Old (deprecated): `npx shadcn-ui@latest add`
- Current: `npx shadcn@latest add`

### Common Options

- `-y, --yes` - Skip confirmation prompt
- `-o, --overwrite` - Overwrite existing files
- `-c, --cwd <cwd>` - Set working directory
- `--src-dir` - Use src directory structure

## Quick Reference

### cn() Utility

```tsx
import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

### Basic CVA Pattern

```tsx
import { cva, type VariantProps } from "class-variance-authority"

const buttonVariants = cva(
  "base-classes-applied-to-all-variants",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground",
        outline: "border bg-background",
      },
      size: {
        sm: "h-8 px-3",
        lg: "h-10 px-6",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "sm",
    },
  }
)

function Button({
  variant,
  size,
  className,
  ...props
}: React.ComponentProps<"button"> & VariantProps<typeof buttonVariants>) {
  return (
    <button
      className={cn(buttonVariants({ variant, size }), className)}
      {...props}
    />
  )
}

export { Button, buttonVariants }
```

## Component Anatomy

### Props Typing Patterns

```tsx
// HTML elements
function Component({ className, ...props }: React.ComponentProps<"div">) {
  return <div className={cn("base-classes", className)} {...props} />
}

// Radix primitives
function Component({ className, ...props }: React.ComponentProps<typeof RadixPrimitive.Root>) {
  return <RadixPrimitive.Root className={cn("base-classes", className)} {...props} />
}

// With CVA variants
function Component({
  variant, size, className, ...props
}: React.ComponentProps<"button"> & VariantProps<typeof variants>) {
  return <button className={cn(variants({ variant, size }), className)} {...props} />
}
```

### asChild Pattern

Enables polymorphic rendering via `@radix-ui/react-slot`:

```tsx
import { Slot } from "@radix-ui/react-slot"

function Button({
  asChild = false,
  className,
  variant,
  size,
  ...props
}: React.ComponentProps<"button"> & VariantProps<typeof buttonVariants> & { asChild?: boolean }) {
  const Comp = asChild ? Slot : "button"
  return (
    <Comp
      data-slot="button"
      className={cn(buttonVariants({ variant, size }), className)}
      {...props}
    />
  )
}
```

**Usage:**
```tsx
<Button>Click me</Button>                           // Renders <button>
<Button asChild><a href="/home">Home</a></Button>   // Renders <a> with button styling
<Button asChild><Link href="/dash">Dash</Link></Button>  // Works with Next.js Link
```

### data-slot Attributes

Every component includes `data-slot` for CSS targeting:

```tsx
function Card({ ...props }) { return <div data-slot="card" {...props} /> }
function CardHeader({ ...props }) { return <div data-slot="card-header" {...props} /> }
```

**CSS/Tailwind targeting:**
```css
[data-slot="button"] { /* styles */ }
[data-slot="card"] [data-slot="button"] { /* nested targeting */ }
```

```tsx
<div className="[&_[data-slot=button]]:shadow-lg">
  <Button>Automatically styled</Button>
</div>
```

**Conditional layouts with has():**
```tsx
<div
  data-slot="card-header"
  className={cn(
    "grid gap-2",
    "has-data-[slot=card-action]:grid-cols-[1fr_auto]"
  )}
/>
```

## Component Patterns

### Compound Components

```tsx
export { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter }

function Card({ className, ...props }: React.ComponentProps<"div">) {
  return (
    <div
      data-slot="card"
      className={cn("bg-card text-card-foreground flex flex-col gap-6 rounded-xl border py-6 shadow-sm", className)}
      {...props}
    />
  )
}

function CardHeader({ className, ...props }: React.ComponentProps<"div">) {
  return <div data-slot="card-header" className={cn("grid gap-2 px-6", className)} {...props} />
}

function CardTitle({ className, ...props }: React.ComponentProps<"div">) {
  return <div data-slot="card-title" className={cn("leading-none font-semibold", className)} {...props} />
}
```

## Styling Techniques

### CVA Variants

**Multiple dimensions:**
```tsx
const buttonVariants = cva("base-classes", {
  variants: {
    variant: {
      default: "bg-primary text-primary-foreground",
      destructive: "bg-destructive text-white",
      outline: "border bg-background",
      ghost: "hover:bg-accent",
      link: "text-primary underline-offset-4 hover:underline",
    },
    size: {
      default: "h-9 px-4 py-2",
      sm: "h-8 px-3",
      lg: "h-10 px-6",
      icon: "size-9",
    },
  },
  defaultVariants: { variant: "default", size: "default" },
})
```

**Compound variants:**
```tsx
compoundVariants: [
  { variant: "outline", size: "lg", class: "border-2" },
]
```

**Type extraction:**
```tsx
type ButtonVariants = VariantProps<typeof buttonVariants>
// Result: { variant?: "default" | "outline" | ..., size?: "sm" | "lg" | ... }
```

### Modern CSS Selectors in Tailwind

**has() selector:**
```tsx
<button className="px-4 has-[>svg]:px-3">  // Adjusts padding when contains icon
<div className="has-data-[slot=action]:grid-cols-[1fr_auto]">  // Conditional layout
```

**Group/peer selectors:**
```tsx
<div className="group" data-state="collapsed">
  <div className="group-data-[state=collapsed]:hidden">Hidden when collapsed</div>
</div>

<button className="peer/menu" data-active="true">Menu</button>
<div className="peer-data-[active=true]/menu:text-accent">Styled when sibling active</div>
```

**Container queries:**
```tsx
<div className="@container/card">
  <div className="@md:flex-row">Responds to container width</div>
</div>
```

### Accessibility States

```tsx
className={cn(
  // Focus
  "outline-none focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:ring-[3px]",
  // Invalid
  "aria-invalid:border-destructive aria-invalid:ring-destructive/20",
  // Disabled
  "disabled:pointer-events-none disabled:opacity-50",
)}

<span className="sr-only">Close</span>  // Screen reader only
```

### Dark Mode

Semantic tokens adapt automatically:
```tsx
className="bg-background text-foreground dark:bg-input/30 dark:hover:bg-input/50"
```

Tokens: `bg-background`, `text-foreground`, `bg-primary`, `text-primary-foreground`, `bg-card`, `text-card-foreground`, `border-input`, `text-muted-foreground`

## Decision Tables

### When to Use CVA

| Scenario | Use CVA | Alternative |
|----------|---------|-------------|
| Multiple visual variants (primary, outline, ghost) | Yes | Plain className |
| Size variations (sm, md, lg) | Yes | Plain className |
| Compound conditions (outline + large = thick border) | Yes | Conditional cn() |
| One-off custom styling | No | className prop |
| Dynamic colors from props | No | Inline styles or CSS variables |

### When to Use Compound Components

| Scenario | Use Compound | Alternative |
|----------|--------------|-------------|
| Complex UI with multiple semantic parts | Yes | Single component with many props |
| Optional sections (header, footer) | Yes | Boolean show/hide props |
| Different styling for each part | Yes | CSS selectors |
| Shared state between parts | Yes + Context | Props drilling |
| Simple wrapper with children | No | Single component |

### When to Use asChild

| Scenario | Use asChild | Alternative |
|----------|-------------|-------------|
| Component should work as link or button | Yes | Duplicate component |
| Need button styles on custom element | Yes | Export variant styles |
| Integration with routing libraries | Yes | Wrapper components |
| Always renders same element | No | Standard component |

### When to Use Context

| Scenario | Use Context | Alternative |
|----------|-------------|-------------|
| Deep prop drilling (>3 levels) | Yes | Props |
| State shared by many siblings | Yes | Lift state up |
| Plugin/extension architecture | Yes | Props |
| Simple parent-child communication | No | Props |

## Common Patterns

### Form Input

```tsx
function Input({ className, type, ...props }: React.ComponentProps<"input">) {
  return (
    <input
      type={type}
      data-slot="input"
      className={cn(
        "h-9 w-full rounded-md border px-3 py-1",
        "outline-none focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:ring-[3px]",
        "aria-invalid:border-destructive aria-invalid:ring-destructive/20",
        "disabled:cursor-not-allowed disabled:opacity-50",
        "placeholder:text-muted-foreground dark:bg-input/30",
        className
      )}
      {...props}
    />
  )
}
```

### Dialog Content

```tsx
function DialogContent({ children, showCloseButton = true, ...props }) {
  return (
    <DialogPortal>
      <DialogOverlay />
      <DialogPrimitive.Content
        data-slot="dialog-content"
        className={cn(
          "fixed top-[50%] left-[50%] translate-x-[-50%] translate-y-[-50%] w-full max-w-lg",
          "bg-background border rounded-lg p-6 shadow-lg",
          "data-[state=open]:animate-in data-[state=open]:fade-in-0 data-[state=open]:zoom-in-95",
          "data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=closed]:zoom-out-95",
        )}
        {...props}
      >
        {children}
        {showCloseButton && (
          <DialogPrimitive.Close className="absolute top-4 right-4">
            <XIcon /><span className="sr-only">Close</span>
          </DialogPrimitive.Close>
        )}
      </DialogPrimitive.Content>
    </DialogPortal>
  )
}
```

### Sidebar with Context

```tsx
function SidebarProvider({ defaultOpen = true, children }) {
  const isMobile = useIsMobile()
  const [open, setOpen] = React.useState(defaultOpen)

  React.useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "b" && (e.metaKey || e.ctrlKey)) {
        e.preventDefault()
        setOpen(o => !o)
      }
    }
    window.addEventListener("keydown", handleKeyDown)
    return () => window.removeEventListener("keydown", handleKeyDown)
  }, [])

  const contextValue = React.useMemo(
    () => ({ state: open ? "expanded" : "collapsed", open, setOpen, isMobile }),
    [open, setOpen, isMobile]
  )

  return (
    <SidebarContext.Provider value={contextValue}>
      <div
        data-slot="sidebar-wrapper"
        style={{ "--sidebar-width": "16rem", "--sidebar-width-icon": "3rem" } as React.CSSProperties}
      >
        {children}
      </div>
    </SidebarContext.Provider>
  )
}
```

## Reference Files

For comprehensive examples and advanced patterns:

- **[components.md](./references/components.md)** - Full implementations: Button, Card, Badge, Input, Label, Textarea, Dialog
- **[cva.md](./references/cva.md)** - CVA patterns: compound variants, responsive variants, type extraction
- **[patterns.md](./references/patterns.md)** - Architectural patterns: compound components, asChild, controlled state, Context, data-slot, has() selectors
