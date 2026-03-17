---
name: tailwindcss-v4
description: Tailwind CSS v4.1 core features, @theme, directives, migration guide
user-invocable: false
---

# Tailwind CSS v4.1 Core

## Documentation

- [theme.md](../docs/theme.md) - CSS theme variables, design tokens, customization
- [functions-and-directives.md](../docs/functions-and-directives.md) - @utility, @variant, @theme, @apply
- [adding-custom-styles.md](../docs/adding-custom-styles.md) - Custom utilities and variants
- [detecting-classes-in-source-files.md](../docs/detecting-classes-in-source-files.md) - Content detection
- [upgrade-guide.md](../docs/upgrade-guide.md) - Migration from v3 to v4

## Quick Reference - @theme Namespaces

| Namespace | Generated Utilities |
|-----------|-------------------|
| `--color-*` | bg-*, text-*, border-*, fill-* |
| `--font-*` | font-* |
| `--text-*` | text-xs, text-sm, text-base, etc. |
| `--spacing-*` | p-*, m-*, gap-*, w-*, h-* |
| `--radius-*` | rounded-* |
| `--shadow-*` | shadow-* |
| `--breakpoint-*` | sm:*, md:*, lg:*, xl:* |
| `--animate-*` | animate-spin, animate-bounce, etc. |
| `--ease-*` | ease-in, ease-out, ease-in-out |

## Configuration CSS-first

### Before (v3)
```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: { brand: '#3B82F6' }
    }
  }
}
```

### After (v4)
```css
@import "tailwindcss";

@theme {
  --color-brand: #3B82F6;
}
```

## Directives v4

### @utility - Create a utility
```css
@utility tab-4 {
  tab-size: 4;
}
/* Usage: class="tab-4" */
```

### @variant - Conditional style
```css
.card {
  @variant dark {
    background: #1a1a2e;
  }
}
```

### @custom-variant - New variant
```css
@custom-variant dark (&:where([data-theme="dark"], [data-theme="dark"] *));
/* Usage: dark:bg-gray-900 */
```

## v3 → v4 Breaking Changes

### Removed @tailwind directives

```css
/* v3 */
@tailwind base;
@tailwind components;
@tailwind utilities;

/* v4 */
@import "tailwindcss";
```

### Renamed utilities

| v3 | v4 |
|----|-----|
| `shadow-sm` | `shadow-xs` |
| `shadow` | `shadow-sm` |
| `rounded-sm` | `rounded-xs` |
| `rounded` | `rounded-sm` |
| `outline-none` | `outline-hidden` |
| `ring` | `ring-3` |

### Removed deprecated utilities

- `bg-opacity-*` → use `bg-black/50`
- `text-opacity-*` → use `text-black/50`
- `flex-shrink-*` → use `shrink-*`
- `flex-grow-*` → use `grow-*`

### Custom utilities syntax

```css
/* v3 */
@layer utilities {
  .tab-4 {
    tab-size: 4;
  }
}

/* v4 */
@utility tab-4 {
  tab-size: 4;
}
```

### Variables in arbitrary values

```html
<!-- v3 -->
<div class="bg-[--brand-color]"></div>

<!-- v4 -->
<div class="bg-(--brand-color)"></div>
```

### Important modifier position

```html
<!-- v3 -->
<div class="!bg-red-500">

<!-- v4 -->
<div class="bg-red-500!">
```

## Upgrade Tool

```bash
npx @tailwindcss/upgrade
```

Requires Node.js 20+

## Browser Support

- Safari 16.4+
- Chrome 111+
- Firefox 128+

## Installation

```bash
npm install -D tailwindcss @tailwindcss/postcss
# or for Vite
npm install -D @tailwindcss/vite
# or for CLI
npm install -D @tailwindcss/cli
```

## Core API Functions

### --alpha()
Adjust color opacity:
```css
color: --alpha(var(--color-lime-300) / 50%);
```

### --spacing()
Generate spacing values:
```css
margin: --spacing(4);
```

### @apply
Inline utility classes:
```css
.btn {
  @apply px-4 py-2 rounded-lg font-bold;
}
```

## Key Resources

- Official Theme Variables Documentation
- @theme Directive Syntax
- Content Detection Configuration
- Custom Variant Creation
- Animation Keyframes Definition
- CSS Variables Usage
