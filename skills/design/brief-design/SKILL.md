---
description: Brief-specific design system, typography, colors, and component patterns
---

# Brief Design Skill

Use this skill when creating or modifying UI components. Brief has a complete design system—**always use it** instead of inventing new patterns.

## Quick Reference

| Category | Use | Avoid |
|----------|-----|-------|
| Sans font | `font-sans` (Spline Sans) | Inter, Roboto, Arial, system fonts |
| Serif font | `font-serif` (Piazzolla) | Times, Georgia |
| Mono font | `font-mono` (Spline Sans Mono) | Courier, Monaco |
| Primary color | `bg-primary` (fern green) | Purple gradients, arbitrary hex |
| Focus rings | `ring-ring` (sky-blue) | Custom ring colors |
| Components | `@/components/ui/*` | Custom from-scratch implementations |

## Typography

### Font Families

Brief uses three font families configured in `web/lib/fonts.ts`:

```tsx
// ✅ Correct - use CSS variables
<h1 className="font-sans">Spline Sans (default)</h1>
<blockquote className="font-serif">Piazzolla for accents</blockquote>
<code className="font-mono">Spline Sans Mono</code>

// ❌ Wrong - hardcoded fonts
<h1 style={{ fontFamily: 'Inter' }}>Never do this</h1>
```

### Semantic Typography Classes

Use these predefined classes from `globals.css` instead of ad-hoc combinations:

| Class | Size | Weight | Use For |
|-------|------|--------|---------|
| `.large-title` | 3xl | normal | Hero headlines |
| `.large-title-heavy` | 3xl | semibold | Emphasized headlines |
| `.title-1` | 2xl | normal | Page titles |
| `.title-2` | xl | normal | Section headers |
| `.title-3` | lg | normal | Card headers |
| `.body` | base | normal | Default body text |
| `.callout` | sm | normal | Supporting info |
| `.subhead` | xs | normal | Labels, metadata |
| `.caption-1` | xxs | normal | Fine print |

Add `-heavy` suffix for semibold variants (e.g., `.title-1-heavy`).

```tsx
// ✅ Good
<h1 className="title-1">Page Title</h1>
<p className="body">Content goes here</p>

// ❌ Bad - recreating what exists
<h1 className="text-2xl font-normal tracking-tight leading-7">Page Title</h1>
```

## Color System

### Layer 1: OKLCH Primitives

All colors are OKLCH-based. Key ramps defined in `globals.css`:

- **`brand-fern`** — Primary brand green (050–095 stops)
- **`neutral`** — Grays for backgrounds/borders
- **`sky-blue`** — Focus states and interactive chrome

```tsx
// Primitive utilities (use sparingly, prefer semantics)
<div className="bg-brand-fern-050">Primary brand surface</div>
<div className="border-neutral-090">High-contrast border</div>
```

### Layer 2: Semantic Tokens

**Always prefer semantic tokens** over primitives.

> ⚠️ **CRITICAL: Only use tokens that exist.** Do NOT invent tokens by pattern-matching (e.g., don't create `bg-background-secondary` because `bg-background` exists).

#### Complete Token Allowlist

These are the **only** semantic tokens available. If it's not listed, it doesn't exist:

| Token | Foreground Variant | Usage |
|-------|-------------------|-------|
| `background` | `foreground` | Page/app background |
| `card` | `card-foreground` | Card surfaces |
| `popover` | `popover-foreground` | Dropdowns, tooltips |
| `primary` | `primary-foreground` | Primary actions, CTAs |
| `secondary` | `secondary-foreground` | Secondary actions |
| `muted` | `muted-foreground` | Subdued surfaces, hint text |
| `accent` | `accent-foreground` | Highlighted items |
| `destructive` | `destructive-foreground` | Danger/delete actions |

| Utility Tokens | Usage |
|----------------|-------|
| `border` | Dividers, card edges |
| `input` | Form input backgrounds |
| `ring` | Focus rings (sky-blue) |

| Sidebar Tokens | Usage |
|----------------|-------|
| `sidebar` / `sidebar-foreground` | Sidebar surfaces |
| `sidebar-primary` / `sidebar-primary-foreground` | Sidebar primary |
| `sidebar-accent` / `sidebar-accent-foreground` | Sidebar highlights |
| `sidebar-border` / `sidebar-ring` | Sidebar chrome |

| Chart Tokens | Usage |
|--------------|-------|
| `chart-1` through `chart-5` | Data visualization |

#### Common Invented Tokens (DON'T USE)

```tsx
// ❌ These tokens DO NOT EXIST - don't invent them
bg-background-secondary    // Use: bg-secondary
bg-background-muted        // Use: bg-muted
text-primary               // Use: text-foreground or text-primary-foreground
bg-surface                 // Use: bg-card or bg-background
text-subtle                // Use: text-muted-foreground
border-muted               // Use: border-border
bg-hover                   // Use: hover:bg-accent
```

```tsx
// ✅ Semantic (preferred)
<Button className="bg-primary text-primary-foreground">Save</Button>
<div className="border border-border rounded-lg">Card</div>
<span className="text-muted-foreground">Optional hint</span>

// ❌ Avoid raw values
<Button className="bg-[#2d6a4f]">Save</Button>
<div style={{ borderColor: '#e5e5e5' }}>Card</div>
```

### Focus Rings

All interactive elements use consistent focus rings:

```tsx
className="focus-visible:ring-ring/50 focus-visible:ring-[3px]"
```

## Component Reuse

### CRITICAL: Search Before Creating

**Before writing any component:**

1. Check `@/components/ui/*` (TailStack components)
2. Search codebase: `grep -r "ComponentName" components/`
3. Check `packages/chat-ui/src/` for shared components

### TailStack Components

Always use existing primitives from `/components/ui/`:

```tsx
// ✅ Use design system
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Dialog, DialogContent } from "@/components/ui/dialog";
import { Card, CardHeader, CardContent } from "@/components/ui/card";

// ❌ Never recreate
const MyButton = () => <button className="px-4 py-2 bg-blue-500">...</button>;
```

### Composition Over Duplication

Extend existing components via composition:

```tsx
// ✅ Good - compose from Button
export function SubmitButton({ children, ...props }) {
  return (
    <Button variant="default" size="lg" {...props}>
      <CheckIcon className="mr-2 h-4 w-4" />
      {children}
    </Button>
  );
}

// ❌ Bad - duplicate Button internals
export function SubmitButton({ children }) {
  return (
    <button className="inline-flex items-center justify-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground">
      <CheckIcon className="mr-2 h-4 w-4" />
      {children}
    </button>
  );
}
```

## Anti-Patterns (AI Slop Prevention)

### ❌ Typography Anti-Patterns

```tsx
// NEVER use these fonts
fontFamily: 'Inter'           // Generic AI default
fontFamily: 'Roboto'          // Google generic
fontFamily: 'Arial'           // System fallback
fontFamily: 'system-ui'       // Platform default
className="font-['Inter']"    // Hardcoded font
```

### ❌ Color Anti-Patterns

```tsx
// NEVER use these patterns
className="bg-gradient-to-r from-purple-500 to-pink-500"  // Purple gradient slop
className="bg-indigo-600"      // Arbitrary Tailwind color
style={{ backgroundColor: '#6366f1' }}  // Hardcoded hex
className="bg-blue-500"        // Generic blue
```

### ❌ Layout Anti-Patterns

```tsx
// NEVER nest cards in cards
<Card>
  <Card>  {/* Card inception = bad */}
    <CardContent>...</CardContent>
  </Card>
</Card>

// Use flat hierarchy with spacing instead
<Card>
  <CardContent className="space-y-4">
    <section>...</section>
    <section>...</section>
  </CardContent>
</Card>
```

### ❌ Component Anti-Patterns

```tsx
// NEVER recreate existing components
const MyModal = ({ children }) => (
  <div className="fixed inset-0 bg-black/50 flex items-center justify-center">
    <div className="bg-white rounded-lg p-6">{children}</div>
  </div>
);
// Use: import { Dialog, DialogContent } from "@/components/ui/dialog";

// NEVER hardcode shadows
className="shadow-[0_4px_6px_rgba(0,0,0,0.1)]"
// Use: className="shadow-sm" or "shadow-md"
```

## Icons

Brief is transitioning from Lucide to custom icons:

```tsx
// Preferred - Custom Brief icons (when available)
import { BriefIcon } from "@/components/icons/react";

// Fallback - Lucide (still installed)
import { Check, X, ChevronDown } from "lucide-react";

// Icon sizing follows Button conventions
<Button size="icon">
  <Check className="h-4 w-4" />
</Button>
```

## Spacing & Layout

### Use `gap` Over Margin

```tsx
// ✅ Good
<div className="flex flex-col gap-4">
  <Item />
  <Item />
</div>

// ❌ Avoid
<div className="flex flex-col">
  <Item className="mb-4" />
  <Item />
</div>
```

### Standard Spacing Scale

| Gap | Pixels | Use For |
|-----|--------|---------|
| `gap-1` | 4px | Tight groupings |
| `gap-2` | 8px | Related items |
| `gap-4` | 16px | Section spacing |
| `gap-6` | 24px | Major sections |
| `gap-8` | 32px | Page sections |

### Border Radius

```tsx
className="rounded-md"   // 6px - default for inputs/buttons
className="rounded-lg"   // 8px - cards, dialogs
className="rounded-xl"   // 12px - large containers
```

## Verification

After creating/modifying a component:

1. **Check Storybook** — Run `pnpm run storybook` in `packages/ui-storybook`
2. **Verify tokens** — Inspect computed styles, confirm OKLCH/semantic usage
3. **Test focus states** — Tab through, verify ring color is sky-blue
4. **No hardcoded values** — Search for hex codes, arbitrary colors

## Resources

- **Design System Docs**: `docs/design/system.md`
- **Storybook**: `packages/ui-storybook` (run with `pnpm run storybook`)
- **UI Components**: `web/components/ui/`
- **Color Tokens**: `web/app/globals.css` (`:root` and `@theme inline` sections)
- **Font Config**: `web/lib/fonts.ts`

## Deep-Dive Reference Docs

For detailed context beyond this quick reference, see the `reference/` subdirectory:

| Doc | When to Use |
|-----|-------------|
| `reference/typography.md` | Font stack rationale, type scale, semantic classes, font loading |
| `reference/color.md` | OKLCH color architecture, token layers, contrast requirements |
| `reference/motion.md` | Animation timing, easing curves, CSS vs Motion library, a11y |

Use these for edge cases, advanced patterns, or when you need to explain *why* a pattern exists.
