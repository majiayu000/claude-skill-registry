---
name: shadcn-component-review
description: Review custom components and layouts against shadcn design patterns, theme styles (Maia, Vega, Lyra, Nova, Mira), component structure, composability, and Radix UI best practices. Use when planning new components, reviewing existing components, auditing spacing, checking component structure, or verifying shadcn best practices alignment.
---

# shadcn Component Review

Systematic review process for ensuring custom components and layouts align with shadcn design patterns, official theme styles, and Radix UI best practices.

## Quick Start

### Planning Phase (Preventive)

Before building a component:

1. **Check existing patterns**: Review similar components in `src/ui/` and `src/components/`
2. **Reference your theme style**: See [references/theme-styles.md](references/theme-styles.md) for spacing/shape patterns
3. **Use shadcn MCP** (if available): Query components via shadcn MCP server
4. **Review checklist**: Use [references/review-checklist.md](references/review-checklist.md) as planning guide

### Review Phase (Post-Build)

After building a component:

1. **Run spacing audit**: Check against your theme's spacing patterns
2. **Verify structure**: Ensure proper use of `data-slot` attributes and composition
3. **Check design tokens**: Verify semantic tokens only (no hardcoded colors)
4. **Test composability**: Ensure component can be reused and customized via props
5. **Validate responsive**: Test mobile-first approach and breakpoints

## Core Review Areas

### 1. Spacing (Theme-Dependent)

Use `gap-*` for flex/grid containers. Spacing varies by theme style:

| Theme | Spacing | Shape |
|-------|---------|-------|
| **Vega** | Standard | Classic shadcn |
| **Nova** | Compact | Reduced padding/margins |
| **Maia** | Generous | Soft, rounded |
| **Lyra** | Standard | Boxy, sharp |
| **Mira** | Dense | Compact interfaces |

See [references/theme-styles.md](references/theme-styles.md) for theme-specific patterns.

### 2. Component Structure

- Use `data-slot` attributes: `data-slot="component-name"`
- Sub-components: `ComponentName.Header`, `ComponentName.Content`
- Composition over modification (never edit `src/ui/*` directly)

### 3. Design Tokens

Semantic tokens only - **never** hardcoded colors:

```tsx
// ✅ text-muted-foreground, bg-muted, hover:bg-accent
// ❌ text-neutral-500, bg-gray-100, hover:bg-neutral-50
```

### 4. Composability

- Prop-based customization (variants, sizes)
- Slot-based composition (children, content blocks)
- Single responsibility, clear interface

### 5. Responsive Design

- Mobile-first (< 768px base)
- Breakpoints: `md:` (768px+), `lg:` (1024px+)
- Touch targets: min 44px
- Flex children: `min-w-0` to prevent overflow

See [references/review-checklist.md](references/review-checklist.md) for detailed checklists.

## Foundational Patterns

### CVA (Class Variance Authority)

shadcn components use CVA for type-safe, declarative variants:

```tsx
import { cva, type VariantProps } from "class-variance-authority"

const buttonVariants = cva(
  "inline-flex items-center justify-center font-medium transition-colors",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        outline: "border border-input bg-background hover:bg-accent",
      },
      size: {
        default: "h-9 px-4 py-2",
        sm: "h-8 px-3 text-sm",
      },
    },
    defaultVariants: { variant: "default", size: "default" },
  }
)

interface ButtonProps extends VariantProps<typeof buttonVariants> {}
```

**Key points:**
- Base styles in first argument (always applied)
- Variants as declarative object
- Type-safe props via `VariantProps`
- Extend with new variants, don't modify base

### cn() Utility

Always use `cn()` for conditional and override classes:

```tsx
import { cn } from "@/lib/utils"

// Combines clsx (conditionals) + tailwind-merge (conflict resolution)
<div className={cn(
  "base-classes",
  isActive && "active-classes",
  className // allows consumer overrides
)} />
```

**Why it matters:**
- Prevents CSS cascade conflicts
- Enables prop-based class overrides
- Handles conditional classes cleanly

### Theme-Aware Styling

shadcn themes use CSS variables for consistent styling across components.

**Border radius** is theme-defined via `--radius`:

```tsx
// ✅ Uses theme radius (adapts to Maia rounded vs Lyra sharp)
<Button className="rounded-md">  // Uses --radius variable
<Card className="rounded-lg">

// ❌ Hardcoded (ignores theme settings)
<Button className="rounded-[20px]">
```

**Theme CSS variables** (defined in your theme's CSS):
- `--radius` - Base radius unit
- `--background`, `--foreground` - Base colors
- `--primary`, `--secondary`, `--accent` - Semantic colors
- `--muted`, `--card`, `--popover` - Surface colors

**Custom theme extensions**: If your project needs theme-switchable radius (e.g., pill vs sharp), create utility classes mapped to CSS variables:

```css
/* Example: Theme-switchable radius */
.rounded-theme-button {
  border-radius: var(--radius-button);
}
```

### Animation Patterns

Use consistent, subtle animations. See [references/animation-patterns.md](references/animation-patterns.md) for:
- Timing standards (150ms fast, 200ms normal, 300ms slow)
- Easing curves (ease-out for enter, ease-in for exit)
- Radix `data-state` animation patterns
- Framer Motion patterns for enter/exit
- Accessibility (`motion-safe:` prefixes)

## Resources

### shadcn Documentation

- **Components**: https://ui.shadcn.com/docs/components
- **Blocks**: https://ui.shadcn.com/blocks
- **Themes**: https://ui.shadcn.com/themes
- **Theme Creator**: https://ui.shadcn.com/create

### 2025 Updates

**Visual Styles** (via `npx shadcn create`):
- **Vega** - Classic shadcn/ui look
- **Nova** - Compact layouts, reduced spacing
- **Maia** - Soft and rounded, generous spacing
- **Lyra** - Boxy and sharp, pairs with mono fonts
- **Mira** - Dense interfaces

**New utility components**:
- `input-group` / `button-group` - Grouped controls
- `empty` - Empty state patterns
- `field` - Form field wrapper
- `spinner` - Loading indicator

**Technical updates**:
- Full Tailwind v4 support (`@theme` directive)
- OKLCH colors (from HSL)
- React 19 compatibility

### Community Tools

- **tweakcn**: https://tweakcn.com/ - Interactive theme editor
- **Shadcn Studio**: https://shadcnstudio.com/ - Theme generator
- **Shadcn Themer**: https://shadcnthemer.com/ - Theme creator

## Review Workflow

### Step 1: Structure Review

Check component structure against shadcn patterns:

```tsx
// ✅ Good: Proper structure with data-slot
<div data-slot="component-name" className="flex flex-col gap-4">
  <div data-slot="component-header" className="flex flex-col gap-2">
    {/* Header content */}
  </div>
  <div data-slot="component-content">
    {/* Main content */}
  </div>
</div>

// ❌ Bad: Missing data-slot, inconsistent spacing
<div className="space-y-4">
  <div className="mb-2">
    {/* Header content */}
  </div>
  <div>
    {/* Main content */}
  </div>
</div>
```

### Step 2: Spacing Audit

Verify spacing follows your theme's patterns:

- Check all flex containers use `gap-*` not `space-y-*` or margins
- Verify spacing values follow Tailwind scale (2, 4, 6, 8, etc.)
- Ensure responsive spacing uses `gap-X md:gap-Y` pattern
- Match spacing density to your theme (Maia=generous, Nova/Mira=compact)

### Step 3: Design Token Check

Verify semantic tokens only:

```bash
# Check for hardcoded colors
grep -r "neutral-\|gray-\|slate-" [component-file]
```

### Step 4: Composability Review

Ensure component can be:
- Reused in other contexts
- Customized via props (variants, sizes)
- Composed with other components
- Extended without modification

### Step 5: Responsive Verification

Test at breakpoints:
- Mobile: 375px
- Tablet: 768px
- Desktop: 1280px

## Examples

### Good Component Pattern

```tsx
// ✅ Follows shadcn patterns
export function PageContent({
  heading,
  description,
  contentBlock,
  children,
}: PageContentProps) {
  return (
    <div
      data-slot="page-content"
      className="min-w-0 flex flex-col gap-4 md:gap-6"
    >
      <div data-slot="page-content-header" className="flex flex-col gap-2">
        <h1 className="text-xl md:text-2xl tracking-tight font-semibold text-foreground">
          {heading}
        </h1>
        {description && (
          <p className="text-sm text-muted-foreground">{description}</p>
        )}
      </div>
      {contentBlock && (
        <div data-slot="page-content-block">{contentBlock}</div>
      )}
      {children}
    </div>
  );
}
```

### Bad Component Pattern

```tsx
// ❌ Violates multiple patterns
export function PageContent({ heading, description }: Props) {
  return (
    <div className="space-y-6">
      <div className="mb-4">
        <h1 className="text-2xl font-bold text-gray-900">{heading}</h1>
        <p className="mt-2 text-sm text-neutral-500">{description}</p>
      </div>
    </div>
  );
}
```

**Issues:**
- Uses `space-y-*` instead of `gap-*`
- Hardcoded colors (`text-gray-900`, `text-neutral-500`)
- Missing `data-slot` attributes
- Inconsistent spacing (`mb-4`, `mt-2` instead of flex gap)

## Additional Resources

- **Theme Styles**: [references/theme-styles.md](references/theme-styles.md)
- **Review Checklist**: [references/review-checklist.md](references/review-checklist.md)
- **Animation Patterns**: [references/animation-patterns.md](references/animation-patterns.md)
- **V2 Enhancement Ideas**: [references/v2-notes.md](references/v2-notes.md)
