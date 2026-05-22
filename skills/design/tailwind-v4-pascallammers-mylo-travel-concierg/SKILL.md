---
name: tailwind-v4
description: Auto-activates when user mentions Tailwind, Tailwind CSS, utility classes, or CSS styling. Expert in Tailwind CSS v4 including CSS-first configuration, Oxide engine, and modern utilities.
category: styling
---

# Tailwind CSS v4 Best Practices

**Official Tailwind CSS v4 guidelines - CSS-first config, new Oxide engine, modern features**

## Core Principles

1. **CSS-First Configuration** - Define theme in CSS using `@theme`, not JavaScript
2. **Oxide Engine** - 10x faster builds, 100x faster incremental rebuilds
3. **Container Queries** - Built-in, no plugin needed
4. **Dynamic Utilities** - Use arbitrary values without brackets: `h-100` instead of `h-[100px]`
5. **Modern CSS** - `@starting-style`, `color-mix()`, `@property` support

## CSS-First Configuration

### ✅ Good: Define Theme in CSS
```css
/* app.css */
@import "tailwindcss";

@theme {
  /* Colors using oklch for vibrant, consistent colors */
  --color-primary-50: oklch(0.98 0.02 250);
  --color-primary-100: oklch(0.95 0.04 250);
  --color-primary-500: oklch(0.55 0.22 250);
  --color-primary-900: oklch(0.25 0.15 250);

  /* Custom spacing scale */
  --spacing-xs: 0.5rem;
  --spacing-sm: 0.75rem;
  --spacing-md: 1rem;
  --spacing-lg: 1.5rem;
  --spacing-xl: 2rem;

  /* Font families */
  --font-sans: "Inter", system-ui, sans-serif;
  --font-mono: "JetBrains Mono", monospace;

  /* Font sizes */
  --font-size-xs: 0.75rem;
  --font-size-sm: 0.875rem;
  --font-size-base: 1rem;
  --font-size-lg: 1.125rem;
  --font-size-xl: 1.25rem;
  --font-size-2xl: 1.5rem;

  /* Border radius */
  --radius-sm: 0.25rem;
  --radius-md: 0.375rem;
  --radius-lg: 0.5rem;
  --radius-xl: 0.75rem;
  --radius-full: 9999px;

  /* Shadows */
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);

  /* Breakpoints (optional customization) */
  --breakpoint-sm: 640px;
  --breakpoint-md: 768px;
  --breakpoint-lg: 1024px;
  --breakpoint-xl: 1280px;
  --breakpoint-2xl: 1536px;
}

/* Use custom properties */
.btn-primary {
  background-color: var(--color-primary-500);
  padding: var(--spacing-md) var(--spacing-lg);
  border-radius: var(--radius-md);
}
```

### ✅ Good: Dark Mode in CSS
```css
@import "tailwindcss";

@theme {
  /* Light mode colors */
  --color-background: oklch(1 0 0);
  --color-foreground: oklch(0.2 0 0);

  /* Dark mode colors */
  @media (prefers-color-scheme: dark) {
    --color-background: oklch(0.2 0 0);
    --color-foreground: oklch(0.95 0 0);
  }
}

/* Or use class-based dark mode */
:root {
  --color-background: oklch(1 0 0);
  --color-foreground: oklch(0.2 0 0);
}

.dark {
  --color-background: oklch(0.2 0 0);
  --color-foreground: oklch(0.95 0 0);
}
```

### ✅ Good: Referencing CSS Variables
```html
<!-- Use with parentheses, not brackets -->
<div class="bg-(--color-primary-500)">
  Primary background
</div>

<div class="text-(--color-foreground)">
  Foreground text
</div>
```

### ❌ Bad: Old JavaScript Config (Tailwind v3)
```javascript
// ❌ Don't use tailwind.config.js anymore
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: {
          500: '#3b82f6'
        }
      }
    }
  }
}
```

## Dynamic Utility Values

### ✅ Good: Bracket-Free Arbitrary Values
```html
<!-- Tailwind v4 - no brackets needed for many values -->
<div class="h-100 w-200 mt-15 text-32">
  Dynamic sizes without brackets
</div>

<!-- Grid columns -->
<div class="grid-cols-15">
  15 column grid
</div>

<!-- Still use parentheses for CSS variables -->
<div class="bg-(--my-color) text-(--my-text-color)">
  CSS variable references
</div>
```

### ✅ Good: Complex Arbitrary Values (Still Use Brackets)
```html
<!-- Use brackets for complex values -->
<div class="bg-[linear-gradient(to_right,red,blue)]">
  Gradient background
</div>

<div class="grid-cols-[200px_1fr_1fr]">
  Complex grid template
</div>
```

## Oxide Engine Performance

### ✅ Good: Fast Development Setup
```javascript
// vite.config.js
import { defineConfig } from 'vite'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [tailwindcss()],
})
```

```css
/* app.css - minimal imports */
@import "tailwindcss";

/* That's it! Oxide engine handles the rest */
```

### Performance Benefits
- **Full builds**: 5x faster than v3
- **Incremental builds**: 100x faster than v3
- **Build times**: ~12s → ~2.4s for large projects
- **Watch mode**: <10ms for changes

## Container Queries (Built-in)

### ✅ Good: Container Query Utilities
```html
<!-- Mark element as container -->
<div class="@container">
  <div class="@sm:grid-cols-2 @md:grid-cols-3 @lg:grid-cols-4">
    <!-- Responds to container size, not viewport -->
  </div>
</div>

<!-- Named containers -->
<div class="@container/sidebar">
  <div class="@lg/sidebar:flex">
    Responds to sidebar container
  </div>
</div>
```

### ✅ Good: Container Query Breakpoints
```html
<div class="@container">
  <!-- Container query breakpoints -->
  <div class="@sm:text-lg">    <!-- min-width: 24rem (384px) -->
  <div class="@md:text-xl">    <!-- min-width: 28rem (448px) -->
  <div class="@lg:text-2xl">   <!-- min-width: 32rem (512px) -->
  <div class="@xl:text-3xl">   <!-- min-width: 36rem (576px) -->
  <div class="@2xl:text-4xl">  <!-- min-width: 42rem (672px) -->
</div>
```

### ✅ Good: Max-Width Container Queries
```html
<div class="@container">
  <!-- Show on small containers, hide on large -->
  <div class="block @lg:hidden">
    Visible when container is small
  </div>

  <!-- Max-width container queries -->
  <div class="@max-md:text-sm">
    Small text when container is narrow
  </div>
</div>
```

### ✅ Good: Responsive Card Component
```html
<div class="@container">
  <div class="flex @sm:flex-row @max-sm:flex-col gap-4">
    <img class="@sm:w-48 @max-sm:w-full" src="..." />
    <div class="flex-1">
      <h3 class="@sm:text-xl @max-sm:text-lg">Title</h3>
      <p class="@sm:text-base @max-sm:text-sm">Description</p>
    </div>
  </div>
</div>
```

## 3D Transform Utilities

### ✅ Good: 3D Rotations
```html
<!-- Rotate on X, Y, Z axes -->
<div class="rotate-x-45">
  Rotated 45deg on X-axis
</div>

<div class="rotate-y-90">
  Rotated 90deg on Y-axis
</div>

<div class="rotate-z-180">
  Rotated 180deg on Z-axis (same as rotate-180)
</div>

<!-- Arbitrary 3D rotations -->
<div class="rotate-x-[30deg] rotate-y-[45deg]">
  Custom 3D rotation
</div>
```

### ✅ Good: 3D Translations
```html
<!-- Translate on Z-axis -->
<div class="translate-z-12">
  Moved 12px forward in 3D space
</div>

<div class="translate-z-[-20px]">
  Moved 20px backward
</div>
```

### ✅ Good: 3D Scale
```html
<!-- Scale on Z-axis -->
<div class="scale-z-150">
  Scaled to 150% on Z-axis
</div>

<div class="scale-z-50">
  Scaled to 50% on Z-axis
</div>
```

### ✅ Good: 3D Transform Card
```html
<div class="perspective-1000">
  <div class="
    transform-gpu
    transition-transform
    hover:rotate-y-12
    hover:rotate-x-6
    hover:scale-105
  ">
    <div class="bg-white rounded-lg shadow-lg p-6">
      Hover for 3D effect
    </div>
  </div>
</div>
```

## Expanded Gradient APIs

### ✅ Good: Linear Gradients with Angles
```html
<!-- Linear gradient with angle -->
<div class="bg-linear-[to_right,red,blue]">
  Left to right gradient
</div>

<div class="bg-linear-[45deg,#f00,#00f]">
  45-degree gradient
</div>

<div class="bg-linear-[135deg,red_0%,yellow_50%,green_100%]">
  Multi-stop gradient
</div>
```

### ✅ Good: Radial Gradients
```html
<!-- Radial gradient -->
<div class="bg-radial-[circle,red,blue]">
  Circle radial gradient
</div>

<div class="bg-radial-[ellipse_at_top,red,blue]">
  Ellipse at top
</div>

<div class="bg-radial-[circle_at_50%_50%,red_0%,blue_100%]">
  Positioned radial gradient
</div>
```

### ✅ Good: Conic Gradients
```html
<!-- Conic gradient -->
<div class="bg-conic-[from_0deg,red,yellow,green,blue,red]">
  Color wheel
</div>

<div class="bg-conic-[from_45deg_at_50%_50%,red,blue]">
  Conic from 45deg
</div>
```

### ✅ Good: Gradient with Color Interpolation
```html
<!-- oklch color space for smoother gradients -->
<div class="bg-linear-[in_oklch,red,blue]">
  Smoother gradient using oklch
</div>

<div class="bg-linear-[in_oklch_longer_hue,red,blue]">
  Gradient with longer hue interpolation
</div>
```

## @starting-style Support

### ✅ Good: Animate Elements on Entry
```css
@import "tailwindcss";

/* Define starting styles */
@starting-style {
  .fade-in {
    opacity: 0;
    transform: translateY(20px);
  }
}

/* Final styles */
.fade-in {
  opacity: 1;
  transform: translateY(0);
  transition: opacity 0.3s, transform 0.3s;
}
```

```html
<!-- Element fades in when added to DOM -->
<div class="fade-in">
  I animate in automatically!
</div>
```

### ✅ Good: Dialog Entry Animation
```css
@starting-style {
  dialog[open] {
    opacity: 0;
    transform: scale(0.9);
  }
}

dialog[open] {
  opacity: 1;
  transform: scale(1);
  transition: opacity 0.2s, transform 0.2s;
}
```

```html
<dialog>
  <p>I animate in when opened!</p>
</dialog>
```

## not-\* Variant

### ✅ Good: Negative Pseudo-Class Matching
```html
<!-- Style elements that are NOT hovered -->
<div class="not-hover:opacity-50">
  Faded when not hovered
</div>

<!-- Style elements that are NOT focused -->
<input class="not-focus:border-gray-300" />

<!-- Style elements that are NOT first child -->
<li class="not-first:border-t">
  Border on all except first
</li>

<!-- Style elements that are NOT last child -->
<li class="not-last:mb-4">
  Margin on all except last
</li>
```

### ✅ Good: Complex not-\* Usage
```html
<!-- Not disabled -->
<button class="not-disabled:hover:bg-blue-600">
  Only hover when enabled
</button>

<!-- Not checked -->
<input type="checkbox" class="not-checked:bg-gray-200" />

<!-- Combination -->
<div class="group">
  <p class="not-group-hover:text-gray-500">
    Gray when group not hovered
  </p>
</div>
```

## Composable Variants

### ✅ Good: group-\* Variants
```html
<div class="group">
  <div class="group-hover:bg-blue-500">
    Changes when parent hovered
  </div>

  <div class="group-focus:ring-2">
    Changes when parent focused
  </div>

  <div class="group-active:scale-95">
    Changes when parent active
  </div>
</div>
```

### ✅ Good: peer-\* Variants
```html
<!-- Peer checkbox -->
<input type="checkbox" class="peer" />

<!-- Styles based on peer state -->
<label class="peer-checked:bg-blue-500">
  Label changes when checkbox checked
</label>

<div class="peer-focus:ring-2">
  Highlights when checkbox focused
</div>

<div class="peer-disabled:opacity-50">
  Faded when checkbox disabled
</div>
```

### ✅ Good: has-\* Variants
```html
<!-- Style parent based on child state -->
<div class="has-[input:focus]:ring-2">
  Highlights when any input inside is focused
</div>

<div class="has-[>img]:grid-cols-2">
  2 columns only if contains image
</div>

<div class="has-[.error]:border-red-500">
  Red border if contains error
</div>
```

## Modern Color Palette (oklch)

### ✅ Good: Using oklch Colors
```css
@theme {
  /* oklch provides more vibrant, perceptually uniform colors */
  --color-blue-50: oklch(0.97 0.01 250);
  --color-blue-100: oklch(0.93 0.03 250);
  --color-blue-500: oklch(0.55 0.22 250);
  --color-blue-900: oklch(0.25 0.15 250);
}
```

```html
<!-- Use like any color -->
<div class="bg-blue-500 text-white">
  Vibrant oklch blue
</div>
```

### ✅ Good: P3 Wide Gamut Colors
```css
@theme {
  /* P3 colors for modern displays */
  --color-vivid-red: color(display-p3 1 0 0);
  --color-vivid-green: color(display-p3 0 1 0);
  --color-vivid-blue: color(display-p3 0 0 1);
}
```

## Responsive Design

### ✅ Good: Mobile-First Responsive
```html
<!-- Default (mobile), then progressively enhance -->
<div class="
  text-sm
  sm:text-base
  md:text-lg
  lg:text-xl
  xl:text-2xl
">
  Responsive text size
</div>

<!-- Grid layout -->
<div class="
  grid
  grid-cols-1
  sm:grid-cols-2
  md:grid-cols-3
  lg:grid-cols-4
  gap-4
">
  Responsive grid
</div>
```

### ✅ Good: Max-Width Utilities
```html
<!-- Hide on large screens -->
<div class="block lg:hidden">
  Mobile only
</div>

<!-- Show only on large screens -->
<div class="hidden lg:block">
  Desktop only
</div>

<!-- Max-width utilities -->
<div class="text-2xl max-lg:text-xl max-md:text-lg">
  Larger on bigger screens
</div>
```

## Dark Mode

### ✅ Good: Class-Based Dark Mode
```html
<!-- Enable dark mode -->
<html class="dark">
  <!-- Dark mode styles automatically apply -->
  <div class="bg-white dark:bg-gray-900">
    <p class="text-gray-900 dark:text-white">
      Adapts to dark mode
    </p>
  </div>
</html>
```

### ✅ Good: Dark Mode Toggle
```typescript
// Toggle dark mode
function toggleDarkMode() {
  document.documentElement.classList.toggle('dark')
}
```

### ✅ Good: System Preference Dark Mode
```css
/* Respect system preference by default */
@media (prefers-color-scheme: dark) {
  :root {
    --color-background: oklch(0.2 0 0);
    --color-foreground: oklch(0.95 0 0);
  }
}
```

## State Variants

### ✅ Good: Interactive States
```html
<!-- Hover -->
<button class="bg-blue-500 hover:bg-blue-600">
  Hover me
</button>

<!-- Focus -->
<input class="border-gray-300 focus:border-blue-500 focus:ring-2" />

<!-- Active -->
<button class="bg-blue-500 active:bg-blue-700">
  Press me
</button>

<!-- Disabled -->
<button class="bg-blue-500 disabled:bg-gray-400 disabled:cursor-not-allowed">
  Disabled
</button>

<!-- Focus-visible (keyboard only) -->
<button class="focus-visible:ring-2">
  Keyboard focus only
</button>
```

### ✅ Good: Form States
```html
<!-- Required -->
<input class="required:border-red-500" required />

<!-- Invalid -->
<input class="invalid:border-red-500" type="email" />

<!-- Valid -->
<input class="valid:border-green-500" type="email" />

<!-- Checked (checkbox/radio) -->
<input type="checkbox" class="checked:bg-blue-500" />

<!-- Indeterminate -->
<input type="checkbox" class="indeterminate:bg-gray-500" />
```

## Utility Composition

### ✅ Good: Component Classes with @apply
```css
@import "tailwindcss";

.btn {
  @apply px-4 py-2 rounded-md font-medium transition-colors;
}

.btn-primary {
  @apply bg-blue-500 text-white hover:bg-blue-600;
}

.btn-secondary {
  @apply bg-gray-200 text-gray-900 hover:bg-gray-300;
}

.card {
  @apply bg-white rounded-lg shadow-md p-6;
}
```

```html
<button class="btn btn-primary">
  Primary Button
</button>

<div class="card">
  Card content
</div>
```

### ❌ Bad: Overusing @apply
```css
/* ❌ Don't recreate semantic CSS */
.heading {
  @apply text-2xl font-bold text-gray-900;
}

.paragraph {
  @apply text-base text-gray-700;
}

/* ✅ Use Tailwind classes directly */
<h1 class="text-2xl font-bold text-gray-900">Heading</h1>
<p class="text-base text-gray-700">Paragraph</p>
```

## Custom Utilities

### ✅ Good: Define Custom Utilities
```css
@import "tailwindcss";

@layer utilities {
  .text-balance {
    text-wrap: balance;
  }

  .scrollbar-hide {
    -ms-overflow-style: none;
    scrollbar-width: none;
  }
  
  .scrollbar-hide::-webkit-scrollbar {
    display: none;
  }

  .animate-spin-slow {
    animation: spin 3s linear infinite;
  }
}
```

```html
<h1 class="text-balance">
  Balanced text wrapping
</h1>

<div class="overflow-x-auto scrollbar-hide">
  Hidden scrollbar
</div>

<div class="animate-spin-slow">
  Slow spin
</div>
```

## Animation

### ✅ Good: Built-in Animations
```html
<!-- Spin -->
<div class="animate-spin">
  Loading...
</div>

<!-- Ping -->
<div class="relative">
  <div class="absolute animate-ping">
  <div class="relative">Notification</div>
</div>

<!-- Pulse -->
<div class="animate-pulse">
  Loading skeleton
</div>

<!-- Bounce -->
<div class="animate-bounce">
  Scroll down
</div>
```

### ✅ Good: Custom Animations
```css
@import "tailwindcss";

@layer utilities {
  @keyframes slide-in {
    from {
      transform: translateX(-100%);
      opacity: 0;
    }
    to {
      transform: translateX(0);
      opacity: 1;
    }
  }

  .animate-slide-in {
    animation: slide-in 0.3s ease-out;
  }
}
```

```html
<div class="animate-slide-in">
  Slides in from left
</div>
```

## Accessibility

### ✅ Good: Screen Reader Only
```html
<span class="sr-only">
  Hidden from visual users, available to screen readers
</span>

<!-- Focus-visible for keyboard navigation -->
<button class="focus:outline-none focus-visible:ring-2">
  Keyboard accessible
</button>
```

### ✅ Good: Proper Focus Styles
```html
<!-- Remove default outline, add custom focus -->
<button class="
  focus:outline-none
  focus-visible:ring-2
  focus-visible:ring-blue-500
  focus-visible:ring-offset-2
">
  Accessible button
</button>

<!-- Input focus -->
<input class="
  border-gray-300
  focus:border-blue-500
  focus:ring-2
  focus:ring-blue-200
" />
```

## Performance

### ✅ Good: Optimize Rendering
```html
<!-- Use transform for animations (GPU accelerated) -->
<div class="transform-gpu hover:scale-110 transition-transform">
  Hardware accelerated
</div>

<!-- Prevent layout shifts -->
<img class="w-full h-auto aspect-video" loading="lazy" />

<!-- Content visibility -->
<div class="content-auto">
  Optimized rendering
</div>
```

### ✅ Good: Reduce Bundle Size
```css
/* Only import what you need */
@import "tailwindcss";

/* Purge automatically handles unused styles in v4 */
```

## Tooling Integration

### ✅ Good: Vite Setup
```javascript
// vite.config.js
import { defineConfig } from 'vite'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [tailwindcss()],
})
```

```css
/* app.css */
@import "tailwindcss";
```

### ✅ Good: Next.js Setup
```javascript
// next.config.js
const tailwindcss = require('@tailwindcss/postcss')

module.exports = {
  experimental: {
    optimizeCss: true,
  },
}
```

```css
/* app/globals.css */
@import "tailwindcss";
```

### ✅ Good: TypeScript IntelliSense
```typescript
// tailwind.config.ts (optional for type safety)
import type { Config } from 'tailwindcss'

export default {
  // config
} satisfies Config
```

## Migration from v3 to v4

### Upgrade Command
```bash
# Automatic migration
npx @tailwindcss/upgrade@next
```

### Key Changes
1. **Config**: JavaScript → CSS (`@theme`)
2. **Arbitrary values**: Some don't need brackets
3. **CSS variables**: Use `()` not `[]`: `bg-(--my-color)`
4. **Container queries**: Built-in, no plugin
5. **@apply**: Can't use with custom `@layer` classes

### Manual Migration Checklist
```css
/* Old v3 */
@tailwind base;
@tailwind components;
@tailwind utilities;

/* New v4 */
@import "tailwindcss";

/* Old v3 config */
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: '#3b82f6'
      }
    }
  }
}

/* New v4 config */
@theme {
  --color-primary: oklch(0.55 0.22 250);
}
```

**CRITICAL: Use CSS-first config with `@theme`, leverage container queries for responsive components, use oklch for vibrant colors, and apply 3D transforms for depth.**
