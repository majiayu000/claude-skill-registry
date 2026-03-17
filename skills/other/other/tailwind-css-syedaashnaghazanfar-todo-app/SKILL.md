---
name: tailwind-css
description: Comprehensive Tailwind CSS utility framework patterns including responsive design, dark mode, custom themes, and layout systems. Use when styling React/Next.js applications with utility-first CSS.
---

# Tailwind CSS Skill

Utility-first CSS framework for rapid, consistent UI development.

## Quick Start

### Installation

```bash
# npm
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# pnpm
pnpm add -D tailwindcss postcss autoprefixer
pnpm dlx tailwindcss init -p
```

### Configuration

```js
// tailwind.config.js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

### CSS Setup

```css
/* globals.css */
@tailwind base;
@tailwind components;
@tailwind utilities;
```

## Core Concepts

| Concept | Guide |
|---------|-------|
| **Utility Classes** | [reference/utilities.md](reference/utilities.md) |
| **Responsive Design** | [reference/responsive.md](reference/responsive.md) |
| **Dark Mode** | [reference/dark-mode.md](reference/dark-mode.md) |
| **Customization** | [reference/customization.md](reference/customization.md) |

## Examples

| Pattern | Guide |
|---------|-------|
| **Layout Patterns** | [examples/layouts.md](examples/layouts.md) |
| **Spacing Systems** | [examples/spacing.md](examples/spacing.md) |
| **Typography** | [examples/typography.md](examples/typography.md) |

## Templates

| Template | Purpose |
|----------|---------|
| [templates/tailwind.config.ts](templates/tailwind.config.ts) | Extended configuration |

## Quick Reference

### Spacing Scale

| Class | Value | Pixels |
|-------|-------|--------|
| `0` | 0 | 0px |
| `0.5` | 0.125rem | 2px |
| `1` | 0.25rem | 4px |
| `2` | 0.5rem | 8px |
| `3` | 0.75rem | 12px |
| `4` | 1rem | 16px |
| `5` | 1.25rem | 20px |
| `6` | 1.5rem | 24px |
| `8` | 2rem | 32px |
| `10` | 2.5rem | 40px |
| `12` | 3rem | 48px |
| `16` | 4rem | 64px |
| `20` | 5rem | 80px |
| `24` | 6rem | 96px |

### Breakpoints

| Prefix | Min-width | CSS |
|--------|-----------|-----|
| `sm` | 640px | `@media (min-width: 640px)` |
| `md` | 768px | `@media (min-width: 768px)` |
| `lg` | 1024px | `@media (min-width: 1024px)` |
| `xl` | 1280px | `@media (min-width: 1280px)` |
| `2xl` | 1536px | `@media (min-width: 1536px)` |

### Common Utilities

```tsx
// Layout
<div className="flex items-center justify-between" />
<div className="grid grid-cols-3 gap-4" />
<div className="container mx-auto px-4" />

// Spacing
<div className="p-4 m-2 space-y-4" />
<div className="px-6 py-3 mt-4 mb-8" />

// Typography
<h1 className="text-4xl font-bold tracking-tight" />
<p className="text-sm text-muted-foreground leading-relaxed" />

// Colors
<div className="bg-primary text-primary-foreground" />
<div className="bg-slate-100 dark:bg-slate-900" />

// Borders & Effects
<div className="rounded-lg border shadow-sm" />
<div className="ring-2 ring-primary ring-offset-2" />

// Sizing
<div className="w-full h-screen max-w-md min-h-[200px]" />

// Position
<div className="relative absolute top-0 left-0 z-10" />
<div className="fixed bottom-4 right-4 sticky top-0" />
```

### State Variants

```tsx
// Hover, Focus, Active
<button className="hover:bg-primary/90 focus:ring-2 active:scale-95" />

// Disabled
<button className="disabled:opacity-50 disabled:cursor-not-allowed" />

// Group hover
<div className="group">
  <span className="group-hover:text-primary" />
</div>

// Focus within
<div className="focus-within:ring-2" />

// First/Last child
<li className="first:pt-0 last:pb-0" />
```

### Responsive Patterns

```tsx
// Mobile-first responsive
<div className="text-sm md:text-base lg:text-lg" />
<div className="flex-col md:flex-row" />
<div className="grid-cols-1 sm:grid-cols-2 lg:grid-cols-4" />
<div className="hidden md:block" />
<div className="md:hidden" />
```

### Dark Mode

```tsx
// Dark mode variants
<div className="bg-white dark:bg-slate-950" />
<p className="text-slate-900 dark:text-slate-100" />
<div className="border-slate-200 dark:border-slate-800" />
```

## Best Practices

1. **Mobile-first**: Start with mobile styles, add breakpoint prefixes for larger screens
2. **Consistent spacing**: Use the spacing scale (4, 8, 12, 16, 24, 32, 48, 64)
3. **Semantic colors**: Use design tokens (`primary`, `muted`, `destructive`) over raw colors
4. **Component extraction**: Use `@apply` sparingly, prefer component abstraction
5. **Arbitrary values**: Use `[value]` syntax for one-off values: `w-[237px]`

## Integration with shadcn/ui

Tailwind CSS is the styling foundation for shadcn/ui. The shadcn skill covers:
- CSS variables for theming
- Component-specific utility patterns
- Design token integration

See [shadcn skill](../shadcn/SKILL.md) for component-specific patterns.
