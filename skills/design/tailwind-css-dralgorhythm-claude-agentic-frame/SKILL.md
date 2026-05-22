---
name: tailwind-css
description: Tailwind CSS 4.x utility-first styling patterns. Use when building UI components, creating responsive layouts, implementing design systems, or customizing themes. Covers CSS-first configuration, @theme directive, and component patterns.
---

# Tailwind CSS 4.x

> **Platform:** Web (Tailwind CSS 4.x). For mobile styling, see the **nativewind** skill (Tailwind 3.x for React Native).

## Overview

Utility-first CSS framework for rapid UI development. Tailwind CSS 4.x introduces a CSS-first configuration approach, automatic content detection, and improved performance with a new engine.

**Install**: `pnpm add -D tailwindcss @tailwindcss/vite`

## Key Changes in v4

Tailwind CSS 4.x is fundamentally different from v3:

- **CSS-first configuration** - Use `@theme` in CSS instead of `tailwind.config.js`
- **Single import** - Use `@import "tailwindcss"` instead of separate directives
- **Automatic content detection** - No `content` array needed
- **New color system** - OKLCH colors with wide gamut support
- **Built-in Vite plugin** - `@tailwindcss/vite` for optimal integration

## Workflows

**Setting up Tailwind v4:**
1. [ ] Install dependencies: `pnpm add -D tailwindcss @tailwindcss/vite`
2. [ ] Add Vite plugin to `vite.config.ts`
3. [ ] Create `index.css` with `@import "tailwindcss"`
4. [ ] Customize theme with `@theme` directive
5. [ ] Test build process and verify styles load

**Creating components:**
1. [ ] Start with semantic HTML structure
2. [ ] Apply utility classes for layout (flex, grid)
3. [ ] Add spacing utilities (p-*, m-*, gap-*)
4. [ ] Style with color, typography, borders
5. [ ] Add responsive variants (sm:, md:, lg:)
6. [ ] Test in multiple viewports

**Custom theme:**
1. [ ] Define design tokens using `@theme` in CSS
2. [ ] Add custom colors, spacing, fonts
3. [ ] Create semantic color aliases
4. [ ] Verify tokens work across components

## Configuration

### Vite Configuration

```typescript
// vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
  ],
});
```

### CSS Entry Point

```css
/* src/index.css */
@import "tailwindcss";

/* Theme customization with @theme */
@theme {
  /* Colors */
  --color-primary: oklch(0.6 0.2 250);
  --color-secondary: oklch(0.6 0.15 300);
  --color-success: oklch(0.7 0.2 150);
  --color-warning: oklch(0.8 0.15 85);
  --color-danger: oklch(0.6 0.25 25);

  /* Fonts */
  --font-sans: "Inter", system-ui, sans-serif;
  --font-mono: "Fira Code", monospace;

  /* Custom spacing */
  --spacing-128: 32rem;
  --spacing-144: 36rem;

  /* Custom animations */
  --animate-fade-in: fade-in 0.3s ease-out;
  --animate-slide-up: slide-up 0.3s ease-out;
}

/* Keyframe definitions */
@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slide-up {
  from { transform: translateY(20px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}
```

### Design Token Integration

```css
/* src/index.css */
@import "tailwindcss";

@theme {
  /* Brand colors using OKLCH for wide gamut */
  --color-brand-primary: oklch(0.55 0.2 250);
  --color-brand-secondary: oklch(0.55 0.15 300);
  --color-brand-accent: oklch(0.65 0.25 330);

  /* Semantic colors */
  --color-success: oklch(0.7 0.2 150);
  --color-warning: oklch(0.8 0.15 85);
  --color-error: oklch(0.6 0.25 25);
  --color-info: oklch(0.65 0.15 220);

  /* Neutral scale */
  --color-gray-50: oklch(0.98 0 0);
  --color-gray-100: oklch(0.96 0 0);
  --color-gray-200: oklch(0.92 0 0);
  --color-gray-300: oklch(0.87 0 0);
  --color-gray-400: oklch(0.7 0 0);
  --color-gray-500: oklch(0.55 0 0);
  --color-gray-600: oklch(0.45 0 0);
  --color-gray-700: oklch(0.37 0 0);
  --color-gray-800: oklch(0.27 0 0);
  --color-gray-900: oklch(0.2 0 0);
  --color-gray-950: oklch(0.13 0 0);

  /* Typography scale */
  --font-size-xs: 0.75rem;
  --font-size-sm: 0.875rem;
  --font-size-base: 1rem;
  --font-size-lg: 1.125rem;
  --font-size-xl: 1.25rem;
  --font-size-2xl: 1.5rem;
  --font-size-3xl: 1.875rem;
  --font-size-4xl: 2.25rem;
}
```

## Responsive Design

### Breakpoints

```tsx
// Default breakpoints (mobile-first)
// sm: 640px   - Small tablets, large phones
// md: 768px   - Tablets
// lg: 1024px  - Laptops
// xl: 1280px  - Desktops
// 2xl: 1536px - Large desktops

// Mobile-first approach
<div className="w-full sm:w-1/2 lg:w-1/3 xl:w-1/4">
  Responsive width
</div>

// Stack on mobile, grid on desktop
<div className="flex flex-col md:flex-row gap-4">
  <div className="w-full md:w-1/2">Left</div>
  <div className="w-full md:w-1/2">Right</div>
</div>

// Hide/show at breakpoints
<div className="hidden lg:block">Desktop only</div>
<div className="block lg:hidden">Mobile only</div>

// Responsive typography
<h1 className="text-2xl sm:text-3xl md:text-4xl lg:text-5xl">
  Scales with viewport
</h1>
```

### Custom Breakpoints

```css
/* In @theme block */
@theme {
  --breakpoint-demo: 1440px;
}
```

```tsx
// Usage
<div className="hidden demo:block">Demo mode only</div>
```

## Dark Mode

### Class-based Dark Mode

```css
/* src/index.css */
@import "tailwindcss";

/* Dark mode variants */
@variant dark (&:where(.dark, .dark *));
```

```tsx
// App-level dark mode toggle
import { useEffect, useState } from 'react';

function App() {
  const [isDark, setIsDark] = useState(false);

  useEffect(() => {
    document.documentElement.classList.toggle('dark', isDark);
  }, [isDark]);

  return (
    <div className="bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100">
      <button onClick={() => setIsDark(!isDark)}>
        Toggle Dark Mode
      </button>
    </div>
  );
}

// Component with dark mode styles
<div className="bg-gray-100 dark:bg-gray-800 border border-gray-300 dark:border-gray-700">
  <h2 className="text-gray-900 dark:text-gray-100">Title</h2>
  <p className="text-gray-600 dark:text-gray-400">Description</p>
</div>
```

## Component Patterns

### Cards

```tsx
// Basic card
<div className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
  <h3 className="text-lg font-semibold text-gray-900">Card Title</h3>
  <p className="mt-2 text-sm text-gray-600">Card description</p>
</div>

// Interactive card with hover
<div className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm transition-all hover:shadow-md hover:scale-[1.02] cursor-pointer">
  <h3 className="text-lg font-semibold text-gray-900">Clickable Card</h3>
</div>

// Card with header and footer
<div className="rounded-lg border border-gray-200 bg-white overflow-hidden">
  <div className="border-b border-gray-200 bg-gray-50 px-6 py-4">
    <h3 className="text-lg font-semibold text-gray-900">Header</h3>
  </div>
  <div className="p-6">
    <p className="text-sm text-gray-600">Content</p>
  </div>
  <div className="border-t border-gray-200 bg-gray-50 px-6 py-4">
    <button className="text-sm font-medium text-blue-600 hover:text-blue-700">
      Action
    </button>
  </div>
</div>
```

### Buttons

```tsx
// Primary button
<button className="rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 active:bg-blue-800 disabled:opacity-50 disabled:cursor-not-allowed transition-colors">
  Primary
</button>

// Secondary button
<button className="rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 active:bg-gray-100 transition-colors">
  Secondary
</button>

// Ghost button
<button className="rounded-md px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors">
  Ghost
</button>

// Button sizes via extractable pattern
const buttonSizes = {
  sm: 'px-3 py-1.5 text-xs',
  md: 'px-4 py-2 text-sm',
  lg: 'px-6 py-3 text-base',
};

<button className={`rounded-md bg-blue-600 text-white ${buttonSizes.lg}`}>
  Large Button
</button>
```

### Badges

```tsx
// Status badges
<span className="inline-flex items-center rounded-full bg-green-100 px-2.5 py-0.5 text-xs font-medium text-green-800">
  Success
</span>

<span className="inline-flex items-center rounded-full bg-yellow-100 px-2.5 py-0.5 text-xs font-medium text-yellow-800">
  Warning
</span>

<span className="inline-flex items-center rounded-full bg-red-100 px-2.5 py-0.5 text-xs font-medium text-red-800">
  Error
</span>
```

### Form Inputs

```tsx
// Text input
<div className="space-y-1">
  <label htmlFor="email" className="block text-sm font-medium text-gray-700">
    Email
  </label>
  <input
    type="email"
    id="email"
    className="block w-full rounded-md border border-gray-300 px-3 py-2 text-sm placeholder-gray-400 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
    placeholder="you@example.com"
  />
</div>

// Input with error state
<input
  type="text"
  className="block w-full rounded-md border border-red-300 px-3 py-2 text-sm shadow-sm focus:border-red-500 focus:outline-none focus:ring-1 focus:ring-red-500"
/>
<p className="mt-1 text-xs text-red-600">This field is required</p>
```

### Grid Layouts

```tsx
// Auto-fit responsive grid
<div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
  {items.map(item => (
    <div key={item.id} className="rounded-lg border border-gray-200 p-4">
      {item.content}
    </div>
  ))}
</div>

// Sidebar layout
<div className="flex gap-6">
  <aside className="w-64 shrink-0">Sidebar</aside>
  <main className="flex-1">Main content</main>
</div>

// Dashboard grid
<div className="grid grid-cols-12 gap-4">
  <div className="col-span-12 lg:col-span-8">Main</div>
  <div className="col-span-12 lg:col-span-4">Sidebar</div>
</div>
```

## Advanced Patterns

### Arbitrary Values

```tsx
// Custom values with []
<div className="top-[117px]">Custom positioning</div>
<div className="bg-[#1da1f2]">Custom color</div>
<div className="grid-cols-[1fr_500px_2fr]">Custom grid</div>

// CSS variables
<div className="bg-[var(--brand-color)]">CSS variable</div>

// Calc expressions
<div className="w-[calc(100%-2rem)]">Dynamic width</div>
```

### Custom Utilities with @utility

```css
/* src/index.css */
@import "tailwindcss";

@utility text-balance {
  text-wrap: balance;
}

@utility scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
  &::-webkit-scrollbar {
    display: none;
  }
}
```

```tsx
// Usage
<p className="text-balance">Balanced text wrapping</p>
<div className="scrollbar-hide overflow-auto">Hidden scrollbar</div>
```

### Variant Modifiers

```tsx
// Group hover
<div className="group hover:bg-gray-100">
  <h3 className="group-hover:text-blue-600">Hover parent to change me</h3>
</div>

// Peer (sibling state)
<input type="checkbox" className="peer" />
<label className="peer-checked:text-blue-600">Label changes when checked</label>

// First/last child
<ul>
  <li className="first:rounded-t-lg last:rounded-b-lg border-b last:border-b-0">Item</li>
</ul>

// Odd/even
<tr className="odd:bg-gray-50 even:bg-white">
  <td>Table cell</td>
</tr>

// Data attributes
<div data-state="active" className="data-[state=active]:bg-blue-100">
  Active state
</div>
```

## Migration from v3

### Key Differences

| v3 Pattern | v4 Pattern |
|------------|------------|
| `tailwind.config.js` | `@theme` in CSS |
| `@tailwind base;` etc. | `@import "tailwindcss"` |
| `content: [...]` | Automatic detection |
| PostCSS plugin | `@tailwindcss/vite` plugin |
| `@apply` in CSS | Still supported, prefer utilities |

### Migration Steps

1. Install new packages: `pnpm add -D tailwindcss @tailwindcss/vite`
2. Replace PostCSS config with Vite plugin
3. Replace `@tailwind` directives with `@import "tailwindcss"`
4. Move theme customizations from `tailwind.config.js` to `@theme` in CSS
5. Remove `content` array (auto-detected in v4)
6. Test all components for any breaking changes

## Best Practices

- **Mobile-first approach** - Start with base styles, add responsive variants
- **Use semantic color names** - primary, secondary, danger via `@theme`
- **Use `@theme` for design tokens** - Colors, spacing, fonts in CSS
- **Keep classes organized** - Layout → Spacing → Colors → Typography → States
- **Use arbitrary values sparingly** - Prefer theme tokens
- **Prefer utility classes** over custom CSS for maintainability
- **Group hover/focus states** with group-* and peer-* utilities
- **Use the Vite plugin** - `@tailwindcss/vite` for best performance

## Anti-Patterns

- ❌ Using `tailwind.config.js` for simple customization (use `@theme`)
- ❌ Using `@tailwind` directives (use `@import "tailwindcss"`)
- ❌ Manually configuring `content` array (auto-detected in v4)
- ❌ Using PostCSS plugin with Vite (use `@tailwindcss/vite`)
- ❌ Desktop-first responsive design (not mobile-friendly)
- ❌ Inline styles mixed with Tailwind (inconsistent)
- ❌ Ignoring accessibility (missing focus states)
- ❌ Hardcoding colors instead of using theme tokens

## Feedback Loops

**Build verification:**
```bash
# Check generated CSS size
pnpm build
# Inspect dist/assets/*.css file size
# Target: < 50KB for production
```

**Development mode:**
```bash
# Watch for changes
pnpm dev
# Verify new utilities are generated
# Check browser console for Tailwind warnings
```

**Accessibility check:**
```tsx
// Test focus states
// Tab through interactive elements
// Verify focus:ring-* utilities visible
// Check color contrast with devtools
```
