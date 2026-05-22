---
name: design-system
description: StepLeague design system, theme configuration, CSS variables, badge styling, and UI patterns. Use when working with colors, themes, styling, badges, buttons, cards, or any visual UI changes. Keywords: CSS, theme, colors, dark mode, light mode, variables, styling, UI, design.
compatibility: Antigravity, Claude Code, Cursor
metadata:
  version: "1.1"
  project: "stepleague"
---

# Design System Skill

## Core Rule

**NEVER use hardcoded Tailwind colors. ALWAYS use semantic CSS variables.**

```tsx
// ❌ WRONG
<div className="bg-slate-900 text-slate-300 border-slate-700">

// ✅ CORRECT
<div className="bg-card text-foreground border-border">
```

---

## Full Documentation

**MUST READ:** [docs/THEME_SYSTEM.md](file:///docs/THEME_SYSTEM.md)

This skill is a quick reference. The full theme documentation contains:
- Complete CSS variable reference
- Light/dark mode implementation
- Accessibility requirements
- Common pitfalls and solutions

---

## Quick Reference: CSS Variables

### Backgrounds

| Variable | Usage |
|----------|-------|
| `bg-background` | Page background |
| `bg-card` | Card/container background |
| `bg-muted` | Muted/subtle background |
| `bg-primary` | Primary action background |
| `bg-secondary` | Secondary background |

### Text

| Variable | Usage |
|----------|-------|
| `text-foreground` | Primary text |
| `text-muted-foreground` | Secondary/muted text |
| `text-primary` | Emphasised text (brand color) |

### Status Colors

```tsx
// Use HSL syntax for status colors
className="text-[hsl(var(--success))]"  // Green
className="text-[hsl(var(--warning))]"  // Amber
className="text-[hsl(var(--info))]"     // Blue
className="text-destructive"             // Red
```

### With Opacity

```tsx
className="bg-primary/90"                    // 90% opacity
className="bg-[hsl(var(--success)/0.1)]"     // 10% opacity
```

---

## Badge Components

### Two Distinct Systems

| Component | Import | Use Case |
|-----------|--------|----------|
| `Badge` | `@/components/ui/badge` | General UI (variant prop) |
| `SystemBadge` | `@/components/ui/SystemBadge` | Category-based (Kanban, Roadmap) |

### shadcn Badge

```tsx
import { Badge } from "@/components/ui/badge";

<Badge variant="default">Default</Badge>
<Badge variant="secondary">Secondary</Badge>
<Badge variant="destructive">Error</Badge>
<Badge variant="outline">Outline</Badge>
```

### SystemBadge

```tsx
import { SystemBadge } from "@/components/ui/SystemBadge";

<SystemBadge category="status" value="verified" />
<SystemBadge category="type" value="bug" size="sm" />
<SystemBadge category="release" value="now" />
```

### Central Badge Configuration

All badge colors are in `src/lib/badges.ts`:

```typescript
import { getBadgeClass, getBadgeConfig } from '@/lib/badges';

const statusClass = getBadgeClass('status', 'verified');
const badgeConfig = getBadgeConfig('type', 'bug');
```

---

## Critical Patterns

### Text Truncation

**CRITICAL:** `truncate` won't work without `min-w-0`!

```tsx
// ✅ CORRECT
<div className="flex items-center gap-3">
  <Icon className="flex-shrink-0" />        // Prevent icon shrinking
  <div className="flex-1 min-w-0">          // Enable truncation
    <div className="truncate">Long text...</div>
  </div>
</div>

// ❌ WRONG - truncate won't work
<div className="flex-1">
  <div className="truncate">Long text...</div>
</div>
```

### Hover States

```tsx
className="hover:bg-secondary"
className="hover:border-primary/50"
className="hover:bg-[hsl(var(--success)/0.1)]"
```

### Focus States

```tsx
className="focus:outline-none focus:ring-1 focus:ring-primary"
```

---

## ⚠️ Light/Dark Mode (CRITICAL)

### The Rule

**Every color MUST work in BOTH light AND dark mode. No exceptions.**

### How It Works

| Property | Value |
|----------|-------|
| Framework | `next-themes` |
| Attribute | `data-theme="light"` (NOT class-based) |
| Default | Dark mode |
| Toggle | User preference via settings |

### CSS Variable Pattern

**ALWAYS define BOTH variants:**

```css
/* In globals.css */
:root {
  /* Dark mode (default) */
  --custom-color: 200 50% 50%;
}

[data-theme="light"] {
  /* Light mode - MUST be defined! */
  --custom-color: 200 60% 30%;  /* Darker for light bg */
}
```

### Common Mistakes

```tsx
// ❌ WRONG - Hardcoded, breaks in one theme
<div className="bg-slate-900 text-white">

// ❌ WRONG - Only works in dark mode
<div className="bg-gray-800">

// ❌ WRONG - Custom inline color
<div style={{ backgroundColor: '#1e293b' }}>

// ✅ CORRECT - Uses semantic variables
<div className="bg-card text-foreground">

// ✅ CORRECT - With opacity
<div className="bg-muted/50">
```

### Testing Requirement

> **ALWAYS test in BOTH themes before considering work complete.**
> Toggle to light mode via user settings or browser dev tools.

---

## ⚠️ Contrast Requirements (CRITICAL)

### WCAG 2.1 AA Standard

| Text Type | Minimum Ratio |
|-----------|---------------|
| Body text | **4.5:1** |
| Large text (18px+ or 14px bold) | **3:1** |
| UI components | **3:1** |

### How to Check

1. Use browser DevTools color picker
2. Or use [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)

### Common Problem: Muted Text

```tsx
// ❌ RISKY - muted-foreground may have low contrast
<p className="text-muted-foreground text-sm">Small muted text</p>

// ✅ SAFER - use for secondary info only, not critical content
<p className="text-muted-foreground">Secondary description</p>
<p className="text-foreground">Important content here</p>
```

### Status Colors Must Have Contrast

```tsx
// ✅ Status on dark background - use appropriate contrast
<span className="text-[hsl(var(--success))]">Verified</span>
<span className="text-destructive">Error occurred</span>

// ✅ Status as background - ensure text contrast
<Badge variant="success">Verified</Badge>  // Uses pre-defined contrast
```

---

## Hardcoded Colors = FORBIDDEN

### Zero Tolerance Policy

| Forbidden | Why |
|-----------|-----|
| `bg-slate-*` | Breaks light mode |
| `text-gray-*` | Inconsistent theming |
| `border-zinc-*` | Not semantic |
| `#1e293b`, `rgb(...)` | Hardcoded |
| `dark:` prefix | Use `data-theme` instead |

### Allowed Patterns

| Pattern | Example |
|---------|---------|
| Semantic variables | `bg-card`, `text-foreground` |
| Status colors (HSL) | `text-[hsl(var(--success))]` |
| With opacity | `bg-primary/90` |
| Custom vars in globals.css | After defining light/dark variants |

### Finding Violations

Search for hardcoded colors in codebase:

```bash
# Find Tailwind color classes (potential violations)
grep -r "bg-slate\|bg-gray\|text-slate\|text-gray" src/
grep -r "border-zinc\|bg-zinc" src/
```

---

## Accessibility

### Screen Reader Support

```tsx
<button aria-label="Close modal">
  <X className="h-5 w-5" />
</button>

// Always add aria-label for icon-only buttons
<button aria-label="Delete item" className="text-destructive">
  <Trash2 className="h-4 w-4" />
</button>
```

### Focus Indicators

All interactive elements must have visible focus:

```tsx
className="focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2"
```

---

## shadcn/ui Components

### Installed Components

| Component | Location |
|-----------|----------|
| `toast`, `toaster` | Notifications |
| `dialog` | Modals |
| `dropdown-menu` | Dropdowns |
| `input`, `label`, `textarea` | Form fields |
| `select`, `checkbox` | Form controls |
| `tooltip` | Tooltips |
| `confirm-dialog` | Confirmation prompts |

### Usage

```tsx
// Toasts
import { toast } from "@/hooks/use-toast";
toast({ title: "Success!", description: "Saved" });
toast({ title: "Error", variant: "destructive" });

// Confirmation
import { ConfirmDialog } from "@/components/ui/confirm-dialog";
<ConfirmDialog
  open={showDelete}
  onOpenChange={setShowDelete}
  title="Delete?"
  variant="destructive"
  onConfirm={handleDelete}
/>
```

---

## Reference Files

| File | Purpose |
|------|---------|
| `docs/THEME_SYSTEM.md` | **Full documentation** |
| `src/app/globals.css` | CSS variable definitions |
| `src/lib/badges.ts` | Badge color configuration |
| `/admin/design-system` | Live component examples |

---

## Checklist

Before completing any UI work:

- [ ] Using semantic CSS variables (not hardcoded colors)
- [ ] Tested in BOTH light and dark themes
- [ ] Used `min-w-0` for flex containers needing truncation
- [ ] Used `flex-shrink-0` on icons in flex layouts
- [ ] Added focus indicators to interactive elements
- [ ] Text contrast meets 4.5:1 ratio
- [ ] Updated design system page if adding new patterns

---

## Related Skills

- `form-components` - Form field styling
- `architecture-philosophy` - Use shadcn over custom components
