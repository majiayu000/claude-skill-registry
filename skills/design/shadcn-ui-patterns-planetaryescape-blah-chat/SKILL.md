---
name: shadcn-ui-patterns
description: shadcn/ui component patterns for this project. CVA variants, data-slot pattern, Radix composition, mobile touch targets. Triggers on "shadcn", "ui component", "cva", "class-variance-authority", "data-slot".
---

# shadcn/ui Patterns

New York style variant with Tailwind v4. All components in `src/components/ui/`. Uses `class-variance-authority` for type-safe variants, Radix UI for primitives.

## Component Structure

Two types: variant-based (Button, Badge) and composition-based (Card).

### Variant-Based (cva)

```typescript
// From components/ui/button.tsx
import { Slot } from "@radix-ui/react-slot";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

const buttonVariants = cva(
  "inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium transition-all duration-200 ease-out disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg:not([class*='size-'])]:size-4 shrink-0",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        destructive: "bg-destructive text-white hover:bg-destructive/90",
        outline: "border bg-background shadow-xs hover:bg-accent",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        link: "text-primary underline-offset-4 hover:underline",
      },
      size: {
        default: "h-9 px-4 py-2 has-[>svg]:px-3 min-h-[44px] sm:min-h-0",
        sm: "h-8 rounded-md gap-1.5 px-3 min-h-[44px] sm:min-h-0",
        lg: "h-10 rounded-md px-6 min-h-[44px] sm:min-h-0",
        icon: "size-9 min-h-[44px] min-w-[44px] sm:size-9",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  },
);

function Button({
  className,
  variant,
  size,
  asChild = false,
  ...props
}: React.ComponentProps<"button"> &
  VariantProps<typeof buttonVariants> & {
    asChild?: boolean;
  }) {
  const Comp = asChild ? Slot : "button";

  return (
    <Comp
      data-slot="button"
      className={cn(buttonVariants({ variant, size, className }))}
      {...props}
    />
  );
}

export { Button, buttonVariants };
```

### Composition-Based (no cva)

```typescript
// From components/ui/card.tsx
function Card({ className, ...props }: React.ComponentProps<"div">) {
  return (
    <div
      data-slot="card"
      className={cn(
        "bg-card text-card-foreground flex flex-col gap-6 rounded-xl border py-6 shadow-sm",
        className,
      )}
      {...props}
    />
  );
}

function CardHeader({ className, ...props }: React.ComponentProps<"div">) {
  return (
    <div
      data-slot="card-header"
      className={cn(
        "@container/card-header grid auto-rows-min grid-rows-[auto_auto] items-start gap-2 px-6 has-data-[slot=card-action]:grid-cols-[1fr_auto]",
        className,
      )}
      {...props}
    />
  );
}

function CardTitle({ className, ...props }: React.ComponentProps<"div">) {
  return (
    <div
      data-slot="card-title"
      className={cn("leading-none font-semibold", className)}
      {...props}
    />
  );
}

export { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter, CardAction };
```

## Variant Pattern

**Standard structure**:
1. Base classes (always applied)
2. `variants` object with categories (variant, size, etc.)
3. `defaultVariants` for sensible defaults
4. Export both component and variants (for external use)

```typescript
// From components/ui/badge.tsx
const badgeVariants = cva(
  "inline-flex items-center justify-center rounded-full border px-2 py-0.5 text-xs font-medium w-fit whitespace-nowrap",
  {
    variants: {
      variant: {
        default: "border-transparent bg-primary text-primary-foreground",
        secondary: "border-transparent bg-secondary text-secondary-foreground",
        destructive: "border-transparent bg-destructive text-white",
        outline: "text-foreground [a&]:hover:bg-accent",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  },
);
```

## asChild Pattern (Radix Slot)

Allow polymorphic rendering - render as different element while keeping styles.

```typescript
// Usage
<Button asChild>
  <Link href="/dashboard">Go to Dashboard</Link>
</Button>

// Renders as: <a href="/dashboard" class="button-classes">Go to Dashboard</a>
```

**Implementation**:
```typescript
import { Slot } from "@radix-ui/react-slot";

function Button({ asChild = false, ...props }) {
  const Comp = asChild ? Slot : "button";
  return <Comp {...props} />;
}
```

Use for: Button, Badge. Don't use for: simple divs (Card, Input).

## cn() Utility

Merges Tailwind classes intelligently - resolves conflicts (last one wins).

```typescript
// From lib/utils.ts
import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

// Usage
<Input className={cn("h-12", className)} />
// If user passes "h-8", result is "h-8" (not "h-12 h-8")
```

Always use in components: `className={cn(baseClasses, className)}`

## data-slot Pattern

All components use `data-slot` attribute for targeted styling by parent selectors.

```typescript
// From components/ui/input.tsx
<input
  data-slot="input"
  className={cn("...", className)}
/>

// From components/ui/card.tsx
<div data-slot="card-header" className={cn(
  "@container/card-header grid ... has-data-[slot=card-action]:grid-cols-[1fr_auto]",
  className
)} />
```

**CardHeader uses it**: detects CardAction presence with `has-data-[slot=card-action]`, adjusts grid layout.

Use for:
- Parent-child component communication (Card detecting CardAction)
- Scoped styles in multi-component patterns
- Debug/testing selectors

## Mobile Touch Targets (44px)

**CRITICAL**: All interactive elements must be 44x44px minimum on mobile (iOS/Android HIG).

```typescript
// From components/ui/button.tsx
size: {
  default: "h-9 px-4 py-2 min-h-[44px] sm:min-h-0",  // 44px mobile, 36px desktop
  icon: "size-9 min-h-[44px] min-w-[44px] sm:size-9", // 44x44 mobile, 36x36 desktop
}
```

**Pattern**: `min-h-[44px] sm:min-h-0` for height, `min-h-[44px] min-w-[44px] sm:size-X` for icons.

Apply to: Button, Badge (when interactive), Toggle, Switch, Checkbox, Radio, any clickable element.

## Focus States

Consistent focus ring across all interactive components.

```typescript
// Standard pattern
className={cn(
  "outline-none",
  "focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:ring-[3px]",
  "aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40 aria-invalid:border-destructive",
  className
)}
```

- `focus-visible`: only on keyboard navigation (not mouse click)
- 3px ring width with 50% opacity
- Invalid state: destructive ring color

From: components/ui/input.tsx, button.tsx

## SVG Icon Handling

Auto-size and style icons inside components.

```typescript
// From components/ui/button.tsx
"[&_svg]:pointer-events-none [&_svg:not([class*='size-'])]:size-4 shrink-0 [&_svg]:shrink-0"

// Usage
<Button>
  <Upload /> {/* Auto-sized to size-4 (16px) */}
  Upload File
</Button>
```

Pattern: `[&_svg]:size-4` (16px default), `[&_svg]:pointer-events-none` (clicks go to button), `shrink-0` (prevent squish).

Badge uses `[&>svg]:size-3` (12px for smaller badges).

## Installation

```bash
bunx shadcn@latest add button
bunx shadcn@latest add card
```

Config: `components.json` at repo root.

```json
{
  "style": "new-york",
  "rsc": true,
  "aliases": {
    "components": "@/components",
    "utils": "@/lib/utils",
    "ui": "@/components/ui"
  }
}
```

## Customization

**Edit directly in `components/ui/`** - they're source files, not library code.

Common customizations:
- Change variant colors: edit cva variants
- Add new sizes: add to variants object
- Adjust animations: edit base classes or add new compound variants
- Mobile breakpoints: change `sm:` prefix in min-h overrides

Don't:
- Wrap in another component just to change styles - edit the source
- Create custom variants externally - add to cva definition

## Composition Patterns

**Card with action button**:
```typescript
<Card>
  <CardHeader>
    <CardTitle>Title</CardTitle>
    <CardDescription>Description</CardDescription>
    <CardAction>
      <Button variant="ghost" size="icon">
        <MoreHorizontal />
      </Button>
    </CardAction>
  </CardHeader>
  <CardContent>Content here</CardContent>
</Card>
```

CardHeader detects CardAction via `has-data-[slot=card-action]`, switches to 2-column grid.

## Key Files

- `src/components/ui/button.tsx` - Variant-based with asChild, mobile touch, icon handling
- `src/components/ui/badge.tsx` - Variant-based with asChild, link hover states
- `src/components/ui/card.tsx` - Composition-based, grid layout detection
- `src/components/ui/input.tsx` - Simple wrapper, focus/invalid states
- `src/lib/utils.ts` - cn() utility
- `components.json` - shadcn config (New York style, RSC, aliases)

## Avoid

- **Don't** use `clsx` alone - always use `cn()` (merges Tailwind conflicts)
- **Don't** skip `data-slot` - used by parent components for layout detection
- **Don't** forget mobile touch targets - add `min-h-[44px] sm:min-h-0` to interactive elements
- **Don't** create wrapper components - edit source files in `components/ui/` directly
- **Don't** mix variant approaches - use cva for multiple variants, plain cn() for simple components
- **Don't** hardcode Radix component names - use `asChild` pattern for polymorphism
