---
name: tailwind-v4
description: Tailwind CSS v4 with CSS-first configuration and design tokens. Use when setting up Tailwind v4, defining theme variables, using OKLCH colors, or configuring dark mode. Triggers on @theme, @tailwindcss/vite, oklch, CSS variables, --color-, tailwind v4.
---

# Tailwind CSS v4 Best Practices

## Quick Reference

**Vite Plugin Setup**:
```ts
// vite.config.ts
import tailwindcss from '@tailwindcss/vite';
import { defineConfig } from 'vite';

export default defineConfig({
  plugins: [tailwindcss()],
});
```

**CSS Entry Point**:
```css
/* src/index.css */
@import 'tailwindcss';
```

**@theme Inline Directive**:
```css
@theme inline {
  --color-primary: oklch(60% 0.24 262);
  --color-surface: oklch(98% 0.002 247);
}
```

## Key Differences from v3

| Feature | v3 | v4 |
|---------|----|----|
| Configuration | tailwind.config.js | @theme in CSS |
| Build Tool | PostCSS plugin | @tailwindcss/vite |
| Colors | rgb() / hsl() | oklch() (default) |
| Theme Extension | extend: {} in JS | CSS variables |
| Dark Mode | darkMode config option | CSS variants |

## @theme Directive Modes

### default (standard mode)
Generates CSS variables that can be referenced elsewhere:
```css
@theme {
  --color-brand: oklch(60% 0.24 262);
}

/* Generates: :root { --color-brand: oklch(...); } */
/* Usage: text-brand → color: var(--color-brand) */
```

**Note**: You can also use `@theme default` explicitly to mark theme values that can be overridden by non-default @theme declarations.

### inline
Inlines values directly without CSS variables (better performance):
```css
@theme inline {
  --color-brand: oklch(60% 0.24 262);
}

/* Usage: text-brand → color: oklch(60% 0.24 262) */
```

### reference
Inlines values as fallbacks without emitting CSS variables:
```css
@theme reference {
  --color-internal: oklch(50% 0.1 180);
}

/* No :root variable, but utilities use fallback */
/* Usage: bg-internal → background-color: var(--color-internal, oklch(50% 0.1 180)) */
```

## OKLCH Color Format

OKLCH provides perceptually uniform colors with better consistency across hues:

```css
oklch(L% C H)
```

- **L (Lightness)**: 0% (black) to 100% (white)
- **C (Chroma)**: 0 (gray) to ~0.4 (vibrant)
- **H (Hue)**: 0-360 degrees (red → yellow → green → blue → magenta)

**Examples**:
```css
--color-sky-500: oklch(68.5% 0.169 237.323);  /* Bright blue */
--color-red-600: oklch(57.7% 0.245 27.325);   /* Vibrant red */
--color-zinc-900: oklch(21% 0.006 285.885);   /* Near-black gray */
```

## CSS Variable Naming

Tailwind v4 uses double-dash CSS variable naming conventions:

```css
@theme {
  /* Colors: --color-{name}-{shade} */
  --color-primary-500: oklch(60% 0.24 262);

  /* Spacing: --spacing multiplier */
  --spacing: 0.25rem;  /* Base unit for spacing scale */

  /* Fonts: --font-{family} */
  --font-display: 'Inter Variable', system-ui, sans-serif;

  /* Breakpoints: --breakpoint-{size} */
  --breakpoint-lg: 64rem;

  /* Custom animations: --animate-{name} */
  --animate-fade-in: fade-in 0.3s ease-out;
}
```

## No Config Files Needed

Tailwind v4 eliminates configuration files:

- **No `tailwind.config.js`** - Use @theme in CSS instead
- **No `postcss.config.js`** - Use @tailwindcss/vite plugin
- **TypeScript support** - Add `@types/node` for path resolution

```json
{
  "devDependencies": {
    "@tailwindcss/vite": "^4.0.0",
    "@types/node": "^22.0.0",
    "tailwindcss": "^4.0.0",
    "vite": "^6.0.0"
  }
}
```

## Progressive Disclosure

- **Setup & Installation**: See [references/setup.md](references/setup.md) for Vite plugin configuration, package setup, TypeScript config
- **Theming & Design Tokens**: See [references/theming.md](references/theming.md) for @theme modes, color palettes, custom fonts, animations
- **Dark Mode Strategies**: See [references/dark-mode.md](references/dark-mode.md) for media queries, class-based, attribute-based approaches

## Decision Guide

### When to use @theme inline vs default

**Use `@theme inline`**:
- Better performance (no CSS variable overhead)
- Static color values that won't change
- Animation keyframes with multiple values
- Utilities that need direct value inlining

**Use `@theme` (default)**:
- Dynamic theming with JavaScript
- CSS variable references in custom CSS
- Values that change based on context
- Better debugging (inspect CSS variables in DevTools)

### When to use @theme reference

**Use `@theme reference`**:
- Provide fallback values without CSS variable overhead
- Values that should work even if variable isn't defined
- Reducing :root bloat while maintaining utility support
- Combining with inline for direct value substitution

## Common Patterns

### Two-Tier Variable System

Semantic variables that map to design tokens:

```css
@theme {
  /* Design tokens (OKLCH colors) */
  --color-blue-600: oklch(54.6% 0.245 262.881);
  --color-slate-800: oklch(27.9% 0.041 260.031);

  /* Semantic mappings */
  --color-primary: var(--color-blue-600);
  --color-surface: var(--color-slate-800);
}

/* Usage: bg-primary, bg-surface */
```

### Custom Font Configuration

```css
@theme {
  --font-display: 'Inter Variable', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', ui-monospace, monospace;

  --font-display--font-variation-settings: 'wght' 400;
  --font-display--font-feature-settings: 'cv02', 'cv03', 'cv04';
}

/* Usage: font-display, font-mono */
```

### Animation Keyframes

```css
@theme inline {
  --animate-beacon: beacon 2s ease-in-out infinite;

  @keyframes beacon {
    0%, 100% {
      opacity: 1;
      transform: scale(1);
    }
    50% {
      opacity: 0.5;
      transform: scale(1.05);
    }
  }
}

/* Usage: animate-beacon */
```
