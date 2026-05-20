---
name: web-ui-shadcn-ui
description: shadcn/ui component library patterns, CLI usage, theming, customization
---

# shadcn/ui Component Patterns

> **Quick Guide:** shadcn/ui is a copy-and-own component system built on Radix primitives and Tailwind. Use `npx shadcn@latest add` to install components into `components/ui/`. Theme via CSS custom properties in OKLCH format. Compose with compound component patterns. Use the `cn()` utility for class merging. New `Field` component replaces the old `Form/FormField` pattern for form-library-agnostic field layout.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use the CLI to add components - `npx shadcn@latest add [component]` - not manual copy)**

**(You MUST customize components through CSS variables and the cn() utility - not direct style overrides)**

**(You MUST keep components in the `components/ui/` directory - this is the shadcn convention)**

**(You MUST define foreground colors for every new background color - `--brand` needs `--brand-foreground`)**

</critical_requirements>

---

**Auto-detection:** shadcn/ui, shadcn, @shadcn, components.json, npx shadcn, cn() utility, ui components, Radix-based components, data-slot, Field component, cva variants

**When to use:**

- Building React applications with accessible, customizable UI components
- Setting up a copy-and-own component library with full source control
- Implementing CSS variable theming with OKLCH colors and dark mode
- Creating forms with the new Field component (form-library-agnostic)
- Using compound components (Card, Dialog, Sheet, Tabs, Command)

**When NOT to use:**

- Projects requiring a specific opinionated design system (Material, Ant Design)
- Applications where you cannot control the component source
- Projects not using Tailwind CSS

**Key patterns covered:**

- CLI installation, inspection flags, and component management
- CSS variable theming with OKLCH format and Tailwind v4
- cn() utility for conflict-free class merging
- Compound component composition and extension
- Field component for form-library-agnostic field layout
- Variant system with cva (class-variance-authority)

---

<philosophy>

## Philosophy

shadcn/ui is **not a traditional component library** - it is how you build your component library. Components are copied into your codebase via CLI, giving you full ownership. Core functionality (accessibility, keyboard nav) comes from Radix primitives; the styling layer is yours to customize.

**Five Core Principles:**

1. **Open Code** - Component source is visible and modifiable
2. **Composition** - Consistent, composable compound component interfaces
3. **Distribution** - CLI and flat-file schema enable component distribution
4. **Beautiful Defaults** - Carefully curated styling that works out of the box
5. **AI-Ready** - Open source architecture allows tools to read and improve components

**What shadcn/ui handles vs what other skills handle:**

- shadcn/ui: component structure, CSS variables, cn() utility, composition patterns, Field layout
- Your styling approach: Tailwind configuration, utility class conventions, custom CSS
- Your form library: useForm hook, validation schemas, submission logic, state management

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: CLI Installation and Management

Always use the CLI to add components. It resolves dependencies, installs Radix packages, and creates proper file structure.

```bash
# Initialize (creates components.json)
npx shadcn@latest init

# Add components
npx shadcn@latest add button card dialog

# Inspection flags (CLI v4)
npx shadcn@latest add button --dry-run   # Preview changes
npx shadcn@latest add button --diff      # Check for updates
npx shadcn@latest add button --view      # Display component payload

# Monorepo support
npx shadcn@latest add button --path=packages/ui/src/components

# Project info (useful for AI agents)
npx shadcn@latest info

# View component docs from CLI (v4)
npx shadcn@latest docs combobox
```

Components go in `components/ui/`. The `cn()` utility goes in `lib/utils.ts`. Both are created automatically.

**Why good:** CLI handles dependency resolution, provides inspection before changes, components become owned source code

---

### Pattern 2: CSS Variable Theming (OKLCH)

shadcn/ui uses CSS custom properties with OKLCH color format (Tailwind v4). Every color follows a background/foreground naming convention.

```css
/* The naming convention - understand this, don't memorize values */
:root {
  --primary: oklch(0.205 0 0); /* Background color */
  --primary-foreground: oklch(0.985 0 0); /* Text ON that background */
}

.dark {
  --primary: oklch(0.985 0 0); /* Inverted for dark mode */
  --primary-foreground: oklch(0.205 0 0);
}
```

Key Tailwind v4 changes from older shadcn versions:

- **OKLCH** replaces HSL for better perceptual uniformity
- **`@theme inline`** directive maps CSS variables to Tailwind utilities
- **`@custom-variant dark`** defines dark mode selector
- **`--chart-*`** and **`--sidebar-*`** variable families for specialized components
- **Computed radius**: `--radius-sm/md/lg/xl` derived from base `--radius`

Adding custom colors requires both the CSS variable AND the `@theme inline` mapping:

```css
:root {
  --brand: oklch(0.627 0.265 303.9);
  --brand-foreground: oklch(1 0 0);
}

@theme inline {
  --color-brand: var(--brand);
  --color-brand-foreground: var(--brand-foreground);
}
```

Then use as: `bg-brand text-brand-foreground hover:bg-brand/90`

See [examples/theming.md](examples/theming.md) for complete variable reference and custom color examples.

---

### Pattern 3: The cn() Utility

Combines `clsx` (conditional classes) with `tailwind-merge` (conflict resolution). Consumer `className` always comes last so overrides work.

```tsx
// lib/utils.ts - auto-generated by shadcn init
import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

// Usage in components - className last for consumer overrides
function Card({ className, ...props }: CardProps) {
  return (
    <div
      className={cn("rounded-lg border bg-card shadow-sm", className)}
      {...props}
    />
  );
}
```

**Critical behavior:** `cn("px-4", "px-8")` produces `"px-8"` (last wins), not `"px-4 px-8"`. This is why consumer `className` overrides work correctly.

See [examples/core.md](examples/core.md) for more cn() examples.

---

### Pattern 4: Component Extension with Variants

Use `cva` (class-variance-authority) for variant-based component styling. This is how shadcn/ui itself structures Button, Badge, and Alert.

```tsx
import { cva, type VariantProps } from "class-variance-authority";

const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-md text-sm font-medium",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        destructive:
          "bg-destructive text-destructive-foreground hover:bg-destructive/90",
        outline: "border border-input bg-background hover:bg-accent",
        ghost: "hover:bg-accent hover:text-accent-foreground",
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-9 px-3",
        lg: "h-11 px-8",
        icon: "h-10 w-10",
      },
    },
    defaultVariants: { variant: "default", size: "default" },
  },
);
```

To add a new variant, edit the component source directly - you own it. To use variants: `<Button variant="destructive" size="sm">`.

See [examples/composition.md](examples/composition.md) for extended button with loading state and responsive dialog/drawer patterns.

---

### Pattern 5: Field Component (Form Layout)

The `Field` component is the modern form-library-agnostic way to compose form fields. It provides labels, descriptions, error messages, and accessibility - without coupling to any specific form library.

```tsx
import {
  Field,
  FieldLabel,
  FieldDescription,
  FieldError,
} from "@/components/ui/field";
import { Input } from "@/components/ui/input";

// Field is a layout primitive - bring your own form library
<Field data-invalid={hasError}>
  <FieldLabel htmlFor="email">Email</FieldLabel>
  <Input id="email" aria-invalid={hasError} {...fieldProps} />
  <FieldDescription>We will never share your email.</FieldDescription>
  {hasError && <FieldError errors={errors} />}
</Field>;
```

**Replaces the old `Form/FormField/FormItem/FormControl/FormMessage` pattern** which was tightly coupled to React Hook Form. The Field component works with any form library or server actions.

Related components: `FieldGroup` for grouping related fields, `FieldSet` and `FieldLegend` for semantic grouping.

See [examples/forms.md](examples/forms.md) for complete form integration examples.

---

### Pattern 6: Compound Component Composition

shadcn/ui uses compound components (Card, Dialog, Sheet, Tabs, Command) with consistent sub-component patterns. Extend by wrapping, not replacing.

```tsx
// CORRECT: Extend by wrapping compound components
function ProductCard({ title, price, ...props }: ProductCardProps) {
  return (
    <Card {...props}>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
        <CardDescription>${price}</CardDescription>
      </CardHeader>
    </Card>
  );
}

// WRONG: Breaking compound structure with plain divs
<div className="card">
  <div className="card-header">
    <h2>{title}</h2>
  </div>
</div>;
```

**`asChild` prop** - Use when composing interactive elements to avoid nesting (e.g., Button wrapping a Link):

```tsx
<Button asChild>
  <Link href="/dashboard">Dashboard</Link>
</Button>
```

See [examples/dialogs.md](examples/dialogs.md) for AlertDialog, Sheet, and toast patterns. See [examples/data-table.md](examples/data-table.md) for table with row actions. See [examples/command-palette.md](examples/command-palette.md) for command menu.

---

### Pattern 7: New Components (October 2025+)

Recent additions that solve common patterns:

| Component        | Purpose                                  | Install                              |
| ---------------- | ---------------------------------------- | ------------------------------------ |
| **Field**        | Form-library-agnostic field layout       | `npx shadcn@latest add field`        |
| **Spinner**      | Loading indicator (replaces custom ones) | `npx shadcn@latest add spinner`      |
| **Kbd**          | Keyboard shortcut display                | `npx shadcn@latest add kbd`          |
| **Button Group** | Grouped button container                 | `npx shadcn@latest add button-group` |
| **Input Group**  | Input with addons (icons, buttons)       | `npx shadcn@latest add input-group`  |
| **Item**         | Flex container for lists/cards           | `npx shadcn@latest add item`         |
| **Empty**        | Empty state display                      | `npx shadcn@latest add empty`        |

These components work across Radix and Base UI primitives.

---

### Pattern 8: Recent Platform Changes

**Unified Radix UI package (Feb 2026):** Individual `@radix-ui/react-*` packages are now a single `radix-ui` package. Migrate with `npx shadcn@latest migrate radix`.

```tsx
// Old (pre-Feb 2026)
import * as DialogPrimitive from "@radix-ui/react-dialog";

// New (unified package)
import { Dialog as DialogPrimitive } from "radix-ui";
```

**CLI v4 (March 2026):**

- `npx shadcn@latest docs [component]` - View component docs from CLI (useful for AI agents)
- `npx shadcn@latest init --template` - Full project scaffolding for Next.js, Vite, Astro, React Router, TanStack Start, Laravel
- `--preset` flag packs entire design system config (colors, fonts, radius, icons) into a shareable code
- `shadcn/skills` - AI agent context for component patterns and registry workflows
- `registry:base` - Distribute entire design systems as single payloads

**RTL support (Jan 2026):** First-class right-to-left layout support. The CLI transforms physical CSS classes to logical equivalents at install time.

</patterns>

---

**Detailed Resources:**

- [examples/core.md](examples/core.md) - Setup, cn() utility, skeleton loading
- [examples/composition.md](examples/composition.md) - Extended button, responsive dialog/drawer
- [examples/forms.md](examples/forms.md) - Field component, form integration patterns
- [examples/dialogs.md](examples/dialogs.md) - AlertDialog, Sheet, toast patterns, dark mode provider
- [examples/data-table.md](examples/data-table.md) - Sortable table with row actions
- [examples/command-palette.md](examples/command-palette.md) - Command menu with keyboard navigation
- [examples/theming.md](examples/theming.md) - Complete CSS variables, custom colors, theme toggle
- [reference.md](reference.md) - Decision frameworks, anti-patterns, checklists

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- **Not using CLI for installation** - Manual copy misses dependencies and proper file structure
- **Breaking OKLCH format** - Wrapping values in `hsl()` when they are already OKLCH
- **Not using cn()** - Direct className concatenation breaks Tailwind class merging
- **Missing components.json** - CLI commands will fail without configuration
- **Hardcoding colors** - Use CSS variables for theme consistency

**Medium Priority Issues:**

- **Overriding styles with !important** - Use cn() and proper class ordering instead
- **Not exposing className prop** - Custom components should accept className for override
- **Ignoring accessibility attributes** - Radix provides them; custom extensions can break them
- **Not updating both :root and .dark** - New colors need both light and dark mode

**Gotchas & Edge Cases:**

- **Foreground convention** - `--primary-foreground` is text color ON `--primary` background, not primary-colored text
- **React 19** - No `forwardRef` needed; `ref` is now a regular prop. Components use `data-slot` attributes
- **`asChild` required for Link composition** - Prevents nested interactive elements (button inside anchor)
- **Select controlled usage** - Requires both `onValueChange` and `defaultValue` (or `value`)
- **Chart config (Tailwind v4)** - Use `var(--chart-1)` directly, no `hsl()` wrapper needed
- **`suppressHydrationWarning`** - Required on `<html>` when using theme provider to prevent hydration mismatch
- **Old Form components** - `Form/FormField/FormItem/FormControl/FormMessage` are legacy; prefer `Field` component for new code
- **Base UI option** - Since Feb 2026, you can choose between Radix and Base UI as the primitive library (`--base radix` or `--base base`)
- **Unified Radix package** - Since Feb 2026, import from `radix-ui` (not individual `@radix-ui/react-*` packages). Migrate with `npx shadcn@latest migrate radix`

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST use the CLI to add components - `npx shadcn@latest add [component]` - not manual copy)**

**(You MUST customize components through CSS variables and the cn() utility - not direct style overrides)**

**(You MUST keep components in the `components/ui/` directory - this is the shadcn convention)**

**(You MUST define foreground colors for every new background color - `--brand` needs `--brand-foreground`)**

**Failure to follow these rules will break component updates, cause styling conflicts, and violate shadcn/ui conventions.**

</critical_reminders>
