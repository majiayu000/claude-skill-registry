---
name: treido-tailwind-v4
description: Tailwind CSS v4 specialist for Treido. Use for styling, token usage, and globals.css theme mappings. Not for component logic or data.
---

# treido-tailwind-v4

Deep expertise in Tailwind CSS v4 CSS-first architecture.

## Core Knowledge

### Configuration (I KNOW THIS)

Tailwind v4 is **CSS-first**. There is no `tailwind.config.js`.

| v3 (OLD) | v4 (CURRENT) |
|----------|--------------|
| `tailwind.config.js` | Does not exist |
| `theme.extend.colors` | `@theme { --color-* }` in CSS |
| Plugin configuration | CSS `@theme` blocks |

**Token SSOT**: `app/globals.css`

### Semantic Tokens (AUTHORITATIVE)

| Token | Usage | CSS Variable |
|-------|-------|--------------|
| `bg-background` | Page backgrounds | `--color-background` |
| `bg-card` | Card surfaces | `--color-card` |
| `bg-popover` | Dropdown surfaces | `--color-popover` |
| `text-foreground` | Primary text | `--color-foreground` |
| `text-muted-foreground` | Secondary text | `--color-muted-foreground` |
| `bg-primary` | Brand CTA | `--color-primary` |
| `bg-secondary` | Secondary action | `--color-secondary` |
| `bg-destructive` | Danger state | `--color-destructive` |
| `border-border` | All borders | `--color-border` |
| `bg-input` | Form inputs | `--color-input` |
| `ring-ring` | Focus rings | `--color-ring` |

### Forbidden Patterns (VIOLATIONS)

| Pattern | Why Forbidden | Fix |
|---------|--------------|-----|
| `bg-gray-100` | Palette color | `bg-muted` |
| `text-blue-500` | Palette color | Use semantic token |
| `bg-gradient-to-r` | Gradients banned | Use solid token |
| `from-*`, `to-*` | Gradient stops | Remove |
| `w-[500px]` | Arbitrary value | Use spacing scale |
| `text-[13px]` | Arbitrary value | Use text scale |
| `bg-primary/10` | Opacity hack | Use dedicated subtle token |
| `bg-white` | Hardcoded | `bg-background` |
| `text-black` | Hardcoded | `text-foreground` |

### Spacing Scale (AUTHORITATIVE)

Use Tailwind's spacing scale, not arbitrary values:

| Class | Size | Use For |
|-------|------|---------|
| `gap-1` | 4px | Tight coupling |
| `gap-2` | 8px | Related elements |
| `gap-3` | 12px | Medium spacing |
| `gap-4` | 16px | Standard spacing |
| `gap-6` | 24px | Section padding |
| `gap-8` | 32px | Large spacing |

## ✅ Do

```tsx
<div className="bg-background text-foreground border border-border rounded-lg p-4">
  <h2 className="text-lg font-semibold">Title</h2>
  <p className="text-muted-foreground text-sm">Description</p>
  <button className="bg-primary text-primary-foreground px-4 py-2 rounded-md hover:bg-hover">
    Action
  </button>
</div>
```

## ❌ Don't

```tsx
<div className="bg-white text-gray-900 border border-gray-200 rounded-lg p-[18px]">
  <h2 className="text-[17px] font-semibold">Title</h2>
  <p className="text-gray-500 text-sm">Description</p>
  <button className="bg-gradient-to-r from-blue-500 to-purple-500 px-4 py-2">
    Action
  </button>
</div>
```

## Dark Mode

Tokens automatically adapt to dark mode via `.dark` class on root.

```css
/* In globals.css - already configured */
:root {
  --color-background: oklch(100% 0 0);  /* Light */
}
.dark {
  --color-background: oklch(10% 0 0);   /* Dark */
}
```

**No manual dark: prefixes needed when using semantic tokens.**

## Review Checklist

- No palette classes (`bg-gray-*`, `text-blue-*`, etc.)
- No gradients (`bg-gradient-*`, `from-*`, `to-*`)
- No arbitrary values (`w-[…]`, `text-[…]`, etc.)
- No token opacity hacks (`bg-primary/10`)
