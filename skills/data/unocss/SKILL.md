---
name: unocss
description: Implements atomic CSS with UnoCSS using on-demand generation, custom rules, and presets. Use when wanting instant atomic CSS, custom utility frameworks, or Tailwind alternatives with more flexibility.
---

# UnoCSS

Instant on-demand atomic CSS engine with full customization.

## Quick Start

**Install:**
```bash
npm install -D unocss
```

**Configure Vite:**
```typescript
// vite.config.ts
import UnoCSS from 'unocss/vite';
import { defineConfig } from 'vite';

export default defineConfig({
  plugins: [UnoCSS()],
});
```

**Create config:**
```typescript
// uno.config.ts
import { defineConfig, presetUno } from 'unocss';

export default defineConfig({
  presets: [
    presetUno(),
  ],
});
```

**Import in entry:**
```typescript
// main.ts
import 'virtual:uno.css';
```

**Use in component:**
```tsx
function Button({ children }) {
  return (
    <button className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors">
      {children}
    </button>
  );
}
```

## Core Concepts

### Rules

Define custom utilities:

```typescript
// uno.config.ts
import { defineConfig } from 'unocss';

export default defineConfig({
  rules: [
    // Static rule
    ['custom-red', { color: 'red' }],

    // Dynamic rule with regex
    [/^m-(\d+)$/, ([, d]) => ({ margin: `${d}px` })],

    // With units
    [/^p-(\d+)$/, ([, d]) => ({ padding: `${d / 4}rem` })],

    // Named capture groups
    [/^bg-(?<color>\w+)-(?<shade>\d+)$/, ({ groups }) => ({
      backgroundColor: `var(--color-${groups.color}-${groups.shade})`,
    })],
  ],
});
```

### Shortcuts

Alias multiple utilities:

```typescript
export default defineConfig({
  shortcuts: {
    // Static shortcut
    'btn': 'px-4 py-2 rounded-lg font-semibold cursor-pointer',
    'btn-primary': 'btn bg-blue-500 text-white hover:bg-blue-600',
    'btn-secondary': 'btn bg-gray-200 text-gray-800 hover:bg-gray-300',

    // Dynamic shortcuts
    [/^btn-(.*)$/, ([, c]) => `btn bg-${c}-500 text-white hover:bg-${c}-600`],
  },
});
```

Use:
```tsx
<button className="btn-primary">Primary</button>
<button className="btn-red">Dynamic Red</button>
```

### Variants

Conditional styles:

```typescript
export default defineConfig({
  variants: [
    // Custom variant
    (matcher) => {
      if (!matcher.startsWith('custom:')) return matcher;
      return {
        matcher: matcher.slice(7),
        selector: s => `.custom-class ${s}`,
      };
    },
  ],
});
```

Built-in variants:
```tsx
<div className="
  hover:bg-blue-600
  focus:ring-2
  active:scale-95
  dark:bg-gray-800
  sm:flex
  md:grid
  lg:grid-cols-3
">
```

## Presets

### preset-uno (Default)

Tailwind/Windi compatible:

```typescript
import { defineConfig, presetUno } from 'unocss';

export default defineConfig({
  presets: [
    presetUno(),
  ],
});
```

### preset-wind

Tailwind CSS utilities:

```typescript
import { defineConfig, presetWind } from 'unocss';

export default defineConfig({
  presets: [
    presetWind(),
  ],
});
```

### preset-mini

Minimal essential rules:

```typescript
import { defineConfig, presetMini } from 'unocss';

export default defineConfig({
  presets: [
    presetMini(),
  ],
});
```

### preset-icons

Pure CSS icons from Iconify:

```bash
npm install -D @iconify-json/heroicons @iconify-json/lucide
```

```typescript
import { defineConfig, presetIcons } from 'unocss';

export default defineConfig({
  presets: [
    presetIcons({
      scale: 1.2,
      extraProperties: {
        'display': 'inline-block',
        'vertical-align': 'middle',
      },
    }),
  ],
});
```

Use:
```tsx
<span className="i-heroicons-check text-green-500" />
<span className="i-lucide-settings text-2xl" />
```

### preset-attributify

Use attributes instead of class:

```typescript
import { defineConfig, presetAttributify } from 'unocss';

export default defineConfig({
  presets: [
    presetAttributify(),
  ],
});
```

Use:
```tsx
<div
  bg="blue-500 hover:blue-600"
  text="white lg"
  p="4"
  rounded="lg"
>
  Attributify mode
</div>
```

### preset-typography

Prose styling:

```typescript
import { defineConfig, presetTypography } from 'unocss';

export default defineConfig({
  presets: [
    presetTypography(),
  ],
});
```

Use:
```tsx
<article className="prose prose-lg dark:prose-invert">
  <h1>Title</h1>
  <p>Content with nice typography...</p>
</article>
```

## Theme Configuration

```typescript
import { defineConfig } from 'unocss';

export default defineConfig({
  theme: {
    colors: {
      primary: {
        50: '#eff6ff',
        100: '#dbeafe',
        500: '#3b82f6',
        600: '#2563eb',
        700: '#1d4ed8',
      },
      secondary: '#6b7280',
    },
    breakpoints: {
      sm: '640px',
      md: '768px',
      lg: '1024px',
      xl: '1280px',
    },
    fontFamily: {
      sans: ['Inter', 'sans-serif'],
      mono: ['Fira Code', 'monospace'],
    },
    spacing: {
      sm: '8px',
      md: '16px',
      lg: '24px',
    },
  },
});
```

## Variant Groups

Group variants for cleaner syntax:

```typescript
import { defineConfig, transformerVariantGroup } from 'unocss';

export default defineConfig({
  transformers: [
    transformerVariantGroup(),
  ],
});
```

Use:
```tsx
<div className="hover:(bg-blue-600 text-white scale-105) focus:(ring-2 ring-blue-300)">
  Grouped variants
</div>

<!-- Equivalent to: -->
<div className="hover:bg-blue-600 hover:text-white hover:scale-105 focus:ring-2 focus:ring-blue-300">
```

## Directives

CSS directives support:

```typescript
import { defineConfig, transformerDirectives } from 'unocss';

export default defineConfig({
  transformers: [
    transformerDirectives(),
  ],
});
```

Use in CSS:
```css
.button {
  @apply px-4 py-2 rounded-lg bg-blue-500 text-white;
}

.container {
  @apply max-w-4xl mx-auto px-4;
}

@screen md {
  .button {
    @apply px-6 py-3;
  }
}
```

## Safelist

Always include classes:

```typescript
export default defineConfig({
  safelist: [
    'bg-red-500',
    'bg-green-500',
    'bg-blue-500',
    // Dynamic patterns
    ...['sm', 'md', 'lg'].map(size => `text-${size}`),
  ],
});
```

## Preflights

Global styles:

```typescript
export default defineConfig({
  preflights: [
    {
      getCSS: () => `
        *, *::before, *::after {
          box-sizing: border-box;
        }
        body {
          margin: 0;
          font-family: system-ui, sans-serif;
        }
      `,
    },
  ],
});
```

## Framework Integration

### Next.js

```bash
npm install -D @unocss/webpack
```

```javascript
// next.config.js
const UnoCSS = require('@unocss/webpack').default;

module.exports = {
  webpack: (config) => {
    config.plugins.push(UnoCSS());
    return config;
  },
};
```

### Nuxt

```bash
npm install -D @unocss/nuxt
```

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  modules: ['@unocss/nuxt'],
});
```

### Astro

```bash
npm install -D unocss
```

```typescript
// astro.config.mjs
import UnoCSS from 'unocss/astro';

export default defineConfig({
  integrations: [UnoCSS()],
});
```

## Common Utilities

```tsx
// Layout
<div className="flex items-center justify-between gap-4" />
<div className="grid grid-cols-3 gap-4" />

// Spacing
<div className="p-4 px-6 py-2 m-auto mt-4" />

// Typography
<p className="text-lg font-semibold text-gray-700 leading-relaxed" />

// Colors
<div className="bg-blue-500 text-white border-gray-200" />

// Sizing
<div className="w-full max-w-lg h-screen min-h-64" />

// Effects
<div className="shadow-lg rounded-xl opacity-90 blur-sm" />

// Transitions
<div className="transition-all duration-300 ease-in-out" />
```

## Best Practices

1. **Use presets** - Start with preset-uno or preset-wind
2. **Define shortcuts** - For repeated patterns
3. **Theme tokens** - Define design system in theme
4. **Variant groups** - Cleaner responsive/state styles
5. **Safelist dynamic** - Include dynamically generated classes

## Reference Files

- [references/rules.md](references/rules.md) - Custom rules
- [references/presets.md](references/presets.md) - Preset configurations
