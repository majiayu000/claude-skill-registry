---
name: styling-with-tailwind
description: Provides utility-first CSS styling patterns using Tailwind CSS 3.x. Use when styling components with utility classes, configuring tailwind.config.js, implementing responsive designs, or creating dark mode themes.
---

# Tailwind CSS 3.x Skill

**Target**: Tailwind CSS 3.4+ | **Purpose**: Utility-first CSS styling reference

---

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Core Utility Classes](#core-utility-classes)
- [Flexbox](#flexbox)
- [Grid](#grid)
- [Responsive Design](#responsive-design)
- [State Variants](#state-variants)
- [Dark Mode](#dark-mode)
- [Basic Configuration](#basic-configuration)
- [Essential Component Patterns](#essential-component-patterns)
- [@apply Directive](#apply-directive)
- [Arbitrary Values](#arbitrary-values)
- [Performance Tips](#performance-tips)
- [Quick Reference Card](#quick-reference-card)

---

## Overview

**What is Tailwind CSS**: A utility-first CSS framework that provides low-level utility classes to build custom designs directly in markup.

**When to Use This Skill**:
- Styling components with utility classes
- Configuring `tailwind.config.js`
- Implementing responsive designs
- Creating dark mode themes

**Prerequisites**: Node.js 14.0+ (for build tools)

---

## Quick Start

### Installation

```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

### Minimal Configuration

**tailwind.config.js**:
```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx,html}", "./index.html"],
  theme: { extend: {} },
  plugins: [],
}
```

**CSS Entry Point**:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

---

## Core Utility Classes

### Spacing (Margin & Padding)

| Pattern | Example | Result |
|---------|---------|--------|
| `m-{size}` | `m-4` | margin: 1rem |
| `p-{size}` | `p-8` | padding: 2rem |
| `mx-auto` | `mx-auto` | center horizontally |
| `space-x-{size}` | `space-x-4` | horizontal gap between children |

**Scale**: `0`=0px, `1`=0.25rem, `2`=0.5rem, `4`=1rem, `8`=2rem, `16`=4rem

### Colors

**Format**: `{property}-{color}-{shade}`

```html
<div class="bg-blue-500 text-white border-gray-300">
```

**Properties**: `text-`, `bg-`, `border-`, `ring-`, `divide-`
**Shades**: 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950

### Typography

| Class | Effect |
|-------|--------|
| `text-sm/base/lg/xl/2xl` | Font size |
| `font-normal/medium/semibold/bold` | Font weight |
| `text-left/center/right` | Text alignment |
| `truncate` | Ellipsis overflow |
| `line-clamp-{1-6}` | Multi-line truncation |

### Sizing

| Pattern | Example |
|---------|---------|
| `w-full`, `w-1/2`, `w-64` | Width |
| `h-screen`, `h-48` | Height |
| `max-w-sm/md/lg/xl` | Max width |
| `size-10` | Width + height together |

---

## Flexbox

### Quick Pattern

```html
<div class="flex flex-row items-center justify-between gap-4">
  <!-- children -->
</div>
```

| Class | Effect |
|-------|--------|
| `flex` / `flex-col` | Enable flexbox, set direction |
| `items-center` | Vertical alignment |
| `justify-between` | Horizontal distribution |
| `gap-4` | Gap between items |
| `flex-1` | Grow to fill space |
| `shrink-0` | Prevent shrinking |

---

## Grid

### Quick Pattern

```html
<div class="grid grid-cols-3 gap-4">
  <div class="col-span-2">Wide</div>
  <div>Normal</div>
</div>
```

| Class | Effect |
|-------|--------|
| `grid-cols-{1-12}` | Column count |
| `col-span-{1-12}` | Span columns |
| `gap-{size}` | Gap between cells |

### Auto-fit Pattern (Responsive without Breakpoints)

```html
<div class="grid grid-cols-[repeat(auto-fit,minmax(250px,1fr))] gap-4">
```

---

## Responsive Design

### Breakpoint Prefixes (Mobile-First)

| Prefix | Min-Width |
|--------|-----------|
| `sm:` | 640px |
| `md:` | 768px |
| `lg:` | 1024px |
| `xl:` | 1280px |
| `2xl:` | 1536px |

### Common Patterns

```html
<!-- Stack on mobile, row on tablet+ -->
<div class="flex flex-col md:flex-row gap-4">

<!-- Hide on mobile, show on desktop -->
<div class="hidden lg:block">Desktop only</div>

<!-- Responsive text -->
<h1 class="text-2xl md:text-4xl lg:text-6xl">
```

---

## State Variants

### Hover, Focus, Active

```html
<button class="bg-blue-500 hover:bg-blue-600 focus:ring-2 active:bg-blue-700">
```

| Prefix | Trigger |
|--------|---------|
| `hover:` | Mouse over |
| `focus:` | Element focused |
| `active:` | Being clicked |
| `disabled:` | Disabled element |

### Group and Peer

```html
<!-- Group: parent state affects children -->
<div class="group hover:bg-gray-100">
  <span class="group-hover:text-blue-500">Hover parent</span>
</div>

<!-- Peer: sibling state affects element -->
<input class="peer" type="checkbox" />
<label class="peer-checked:text-green-500">Checked!</label>
```

---

## Dark Mode

### Configuration

```javascript
// tailwind.config.js
module.exports = {
  darkMode: 'class', // or 'media' for OS preference
}
```

### Usage

```html
<html class="dark">
  <body class="bg-white dark:bg-gray-900 text-gray-900 dark:text-white">
```

---

## Basic Configuration

### Extending Theme

```javascript
module.exports = {
  theme: {
    extend: {
      colors: {
        brand: { 500: '#3b82f6', 900: '#1e3a8a' },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
}
```

See [REFERENCE.md](./REFERENCE.md) for advanced configuration (custom screens, container, presets, plugins).

---

## Essential Component Patterns

### Button

```html
<button class="
  px-4 py-2
  bg-blue-500 hover:bg-blue-600
  text-white font-medium rounded-lg
  focus:outline-none focus:ring-2 focus:ring-blue-300
  disabled:opacity-50 disabled:cursor-not-allowed
  transition-colors
">
  Button
</button>
```

### Card

```html
<div class="
  bg-white dark:bg-gray-800
  rounded-xl shadow-lg p-6
  border border-gray-200 dark:border-gray-700
">
  <h3 class="text-xl font-semibold">Title</h3>
  <p class="mt-2 text-gray-600 dark:text-gray-300">Description</p>
</div>
```

See [REFERENCE.md](./REFERENCE.md) for more component patterns (input, navigation, badge, modal).

---

## @apply Directive

Extract repeated utilities into custom classes:

```css
@layer components {
  .btn {
    @apply px-4 py-2 rounded-lg font-medium transition-colors;
  }
  .btn-primary {
    @apply btn bg-blue-500 text-white hover:bg-blue-600;
  }
}
```

**When to Use**: Repeated utility combinations, component libraries
**When to Avoid**: One-off styles (use inline utilities)

---

## Arbitrary Values

Use brackets for one-off custom values:

```html
<div class="w-[137px]">Exact width</div>
<div class="bg-[#1da1f2]">Custom color</div>
<div class="grid-cols-[1fr_500px_2fr]">Custom columns</div>
```

---

## Performance Tips

1. **Content Configuration**: Ensure all template paths are in `content` array
2. **Avoid Dynamic Classes**: `bg-${color}-500` won't work

```javascript
// DON'T
className={`bg-${color}-500`}

// DO
const colorClasses = { blue: 'bg-blue-500', red: 'bg-red-500' };
className={colorClasses[color]}
```

---

## Quick Reference Card

```
SPACING: m-4 p-4 mx-auto space-x-4 gap-4
SIZING: w-full h-screen max-w-xl size-10
FLEX: flex flex-col items-center justify-between flex-1
GRID: grid grid-cols-3 col-span-2 gap-4
TEXT: text-lg font-bold text-center truncate
COLORS: bg-blue-500 text-white border-gray-300
BORDERS: border rounded-lg border-2
SHADOWS: shadow-sm shadow-lg
POSITION: absolute relative fixed sticky top-0 z-50
RESPONSIVE: sm: md: lg: xl: 2xl:
STATES: hover: focus: active: disabled: dark:
TRANSITIONS: transition duration-200
```

---

**See Also**: [REFERENCE.md](./REFERENCE.md) for:
- Complete utility class reference (layout, typography, effects, filters)
- Advanced configuration (presets, content transform, safelist)
- Custom plugin development
- Animation utilities and custom keyframes
- Typography plugin usage
- CSS-in-JS integration (twin.macro, CVA, clsx)
- Framework integration (Next.js, Vite, Nuxt, SvelteKit)
- Performance optimization
- Migration guides

**See Also**: [REFERENCE.md](./REFERENCE.md) for comprehensive documentation.
