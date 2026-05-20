---
name: tailwind
description: Tailwind CSS v4 patterns, design systems, and responsive design. Use when styling with Tailwind, building design tokens, creating responsive layouts, or implementing dark mode.
---

# Tailwind CSS Skill

## Overview
Tailwind CSS v4 patterns, design systems, and responsive design.

## Core Concepts

### 1. Utility-First Approach
```html
<!-- Instead of writing CSS -->
<div class="flex items-center gap-4 p-6 bg-white rounded-xl shadow-lg">
  <img class="size-16 rounded-full" src="avatar.jpg" alt="">
  <div>
    <h3 class="text-lg font-semibold text-gray-900">John Doe</h3>
    <p class="text-gray-500">Developer</p>
  </div>
</div>
```

### 2. Responsive Design
```html
<!-- Mobile-first approach -->
<div class="
  grid grid-cols-1 gap-4
  sm:grid-cols-2
  md:grid-cols-3
  lg:grid-cols-4
">
  <!-- Cards -->
</div>

<!-- Container widths -->
<div class="container mx-auto px-4 sm:px-6 lg:px-8">
  <!-- Content -->
</div>
```

### 3. Dark Mode
```html
<div class="bg-white dark:bg-gray-900">
  <h1 class="text-gray-900 dark:text-white">Title</h1>
  <p class="text-gray-600 dark:text-gray-300">Description</p>
</div>
```

### 4. State Variants
```html
<button class="
  bg-blue-500 
  hover:bg-blue-600 
  focus:ring-2 focus:ring-blue-500 focus:ring-offset-2
  active:bg-blue-700
  disabled:opacity-50 disabled:cursor-not-allowed
  transition-colors duration-200
">
  Submit
</button>
```

## Component Patterns

### Card Component
```html
<div class="
  bg-white rounded-2xl shadow-md
  overflow-hidden
  hover:shadow-xl transition-shadow duration-300
">
  <img class="w-full h-48 object-cover" src="..." alt="">
  <div class="p-6">
    <h3 class="text-xl font-bold mb-2">Card Title</h3>
    <p class="text-gray-600 line-clamp-2">Description...</p>
  </div>
</div>
```

### Form Input
```html
<div class="space-y-2">
  <label class="block text-sm font-medium text-gray-700">Email</label>
  <input 
    type="email"
    class="
      w-full px-4 py-2 
      border border-gray-300 rounded-lg
      focus:ring-2 focus:ring-blue-500 focus:border-blue-500
      placeholder:text-gray-400
    "
    placeholder="you@example.com"
  >
</div>
```

### Button Variants
```html
<!-- Primary -->
<button class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
  Primary
</button>

<!-- Secondary -->
<button class="px-4 py-2 bg-gray-100 text-gray-900 rounded-lg hover:bg-gray-200">
  Secondary
</button>

<!-- Outline -->
<button class="px-4 py-2 border-2 border-blue-600 text-blue-600 rounded-lg hover:bg-blue-50">
  Outline
</button>
```

## Custom Design System

### tailwind.config.js
```javascript
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
        },
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
    },
  },
};
```

## Best Practices
- Use `@apply` sparingly (prefer utilities in HTML)
- Extract components instead of `@apply`
- Use arbitrary values `[]` for one-off designs
- Enable JIT mode for development
