---
name: tailwind-css-patterns
description: Provides comprehensive Tailwind CSS utility-first styling patterns including responsive design, layout utilities, flexbox, grid, spacing, typography, colors, and modern CSS best practices. Use when styling React/Vue/Svelte components, building responsive layouts, implementing design systems, or optimizing CSS workflow.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Tailwind CSS Development Patterns

## Overview

Expert guide for building modern, responsive user interfaces with Tailwind CSS utility-first framework. Covers v4.1+ features including CSS-first configuration, custom utilities, and enhanced developer experience.

## When to Use

- Styling React/HTML components with utility classes
- Building responsive layouts with breakpoints
- Implementing flexbox and grid layouts
- Managing spacing, colors, and typography
- Creating custom design systems
- Optimizing for mobile-first design
- Building dark mode interfaces

## Instructions

1. **Start Mobile-First**: Write base styles for mobile, add responsive prefixes for larger screens
2. **Use Design Tokens**: Leverage Tailwind's spacing, color, and typography scales
3. **Compose Utilities**: Combine multiple utilities for complex styles
4. **Extract Components**: Create reusable component classes for repeated patterns
5. **Configure Theme**: Customize design tokens in tailwind.config.js
6. **Optimize for Production**: Ensure content paths are configured for CSS purging
7. **Test Responsive**: Verify layouts at all breakpoint sizes

## Examples

### Responsive Card Component

```tsx
function ProductCard({ product }: { product: Product }) {
  return (
    <div className="bg-white rounded-lg shadow-lg overflow-hidden
                    sm:flex sm:max-w-2xl">
      <img
        className="h-48 w-full object-cover sm:h-auto sm:w-48"
        src={product.image}
        alt={product.name}
      />
      <div className="p-6">
        <h3 className="text-lg font-semibold text-gray-900">
          {product.name}
        </h3>
        <p className="mt-2 text-gray-600">
          {product.description}
        </p>
        <button className="mt-4 px-4 py-2 bg-indigo-600 text-white
                          rounded-lg hover:bg-indigo-700 transition">
          Add to Cart
        </button>
      </div>
    </div>
  );
}
```

## Constraints and Warnings

- **Class Proliferation**: Long class strings can reduce readability; extract components when needed
- **Purge Configuration**: Must configure content paths correctly for production builds
- **Arbitrary Values**: Use sparingly; prefer design tokens for consistency
- **Specificity Issues**: Avoid @apply with complex selectors
- **Dark Mode**: Requires proper configuration (class or media strategy)
- **JIT Mode**: Some dynamic patterns may not be detected; use safelist if needed
- **Browser Support**: Check Tailwind docs for browser compatibility

## Core Concepts

### Utility-First Approach

Apply styles directly in markup using utility classes:

```html
<button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
  Click me
</button>
```

### Responsive Design

Mobile-first breakpoints with prefixes:

```html
<div class="w-full md:w-1/2 lg:w-1/3">
  <!-- Full width on mobile, half on tablet, third on desktop -->
</div>
```

Breakpoint prefixes:
- `sm:` - 640px and above
- `md:` - 768px and above
- `lg:` - 1024px and above
- `xl:` - 1280px and above
- `2xl:` - 1536px and above

## Layout Utilities

### Flexbox Layouts

Basic flex container:

```html
<div class="flex items-center justify-between">
  <div>Left</div>
  <div>Center</div>
  <div>Right</div>
</div>
```

Responsive flex direction:

```html
<div class="flex flex-col md:flex-row gap-4">
  <div class="flex-1">Item 1</div>
  <div class="flex-1">Item 2</div>
  <div class="flex-1">Item 3</div>
</div>
```

Common flex patterns:

```html
<!-- Center content -->
<div class="flex items-center justify-center min-h-screen">
  <div>Centered Content</div>
</div>

<!-- Space between items -->
<div class="flex justify-between items-center">
  <span>Left</span>
  <span>Right</span>
</div>

<!-- Vertical stack with gap -->
<div class="flex flex-col gap-4">
  <div>Item 1</div>
  <div>Item 2</div>
</div>
```

### Grid Layouts

Basic grid:

```html
<div class="grid grid-cols-3 gap-4">
  <div>Column 1</div>
  <div>Column 2</div>
  <div>Column 3</div>
</div>
```

Responsive grid:

```html
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
  <!-- 1 column mobile, 2 tablet, 4 desktop -->
  <div>Item 1</div>
  <div>Item 2</div>
  <div>Item 3</div>
  <div>Item 4</div>
</div>
```

Auto-fit columns:

```html
<div class="grid grid-cols-[repeat(auto-fit,minmax(250px,1fr))] gap-4">
  <!-- Automatically fit columns based on container width -->
</div>
```

### Container & Max Width

Centered container with max width:

```html
<div class="container mx-auto px-4 max-w-7xl">
  <!-- Centered content with padding -->
</div>
```

Responsive max width:

```html
<div class="w-full max-w-md mx-auto">
  <!-- Max 448px width, centered -->
</div>
```

## Spacing

### Padding & Margin

Uniform spacing:

```html
<div class="p-4">Padding all sides</div>
<div class="m-4">Margin all sides</div>
```

Individual sides:

```html
<div class="pt-4 pr-8 pb-4 pl-8">
  <!-- Top 1rem, Right 2rem, Bottom 1rem, Left 2rem -->
</div>
```

Axis-based spacing:

```html
<div class="px-4 py-8">
  <!-- Horizontal padding 1rem, Vertical padding 2rem -->
</div>
```

Responsive spacing:

```html
<div class="p-4 md:p-8 lg:p-12">
  <!-- Increases padding at larger breakpoints -->
</div>
```

Space between children:

```html
<div class="space-y-4">
  <div>Item 1</div>
  <div>Item 2</div>
  <div>Item 3</div>
</div>
```

## Typography

### Font Size & Weight

```html
<h1 class="text-4xl font-bold">Large Heading</h1>
<h2 class="text-2xl font-semibold">Subheading</h2>
<p class="text-base font-normal">Body text</p>
<small class="text-sm text-gray-600">Small text</small>
```

Responsive typography:

```html
<h1 class="text-2xl md:text-4xl lg:text-6xl font-bold">
  Responsive Heading
</h1>
```

### Line Height & Letter Spacing

```html
<p class="leading-relaxed tracking-wide">
  Text with relaxed line height and wide letter spacing
</p>
```

### Text Alignment

```html
<p class="text-left md:text-center">
  Left aligned on mobile, centered on tablet+
</p>
```

## Colors

### Background Colors

```html
<div class="bg-blue-500">Blue background</div>
<div class="bg-gray-100">Light gray background</div>
<div class="bg-gradient-to-r from-blue-500 to-purple-600">
  Gradient background
</div>
```

### Text Colors

```html
<p class="text-gray-900">Dark text</p>
<p class="text-blue-600">Blue text</p>
<p class="text-red-500">Error text</p>
```

### Opacity

```html
<div class="bg-blue-500 bg-opacity-50">
  Semi-transparent blue
</div>
```

## Interactive States

### Hover States

```html
<button class="bg-blue-500 hover:bg-blue-700 transition">
  Hover me
</button>

<a class="text-blue-600 hover:text-blue-800 hover:underline">
  Hover link
</a>
```

### Focus States

```html
<input class="border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none">
```

### Active & Disabled States

```html
<button class="bg-blue-500 active:bg-blue-800 disabled:opacity-50 disabled:cursor-not-allowed">
  Button
</button>
```

### Group Hover

```html
<div class="group">
  <img class="group-hover:opacity-75" src="image.jpg" />
  <p class="group-hover:text-blue-600">Hover the parent</p>
</div>
```

## Component Patterns

### Card Component

```html
<div class="bg-white rounded-lg shadow-lg overflow-hidden">
  <img class="w-full h-48 object-cover" src="image.jpg" alt="Card image" />
  <div class="p-6">
    <h3 class="text-xl font-bold mb-2">Card Title</h3>
    <p class="text-gray-700 mb-4">Card description text goes here.</p>
    <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
      Action
    </button>
  </div>
</div>
```

### Responsive User Card

```html
<div class="max-w-sm mx-auto bg-white rounded-xl shadow-lg overflow-hidden sm:flex sm:max-w-2xl">
  <img class="h-48 w-full object-cover sm:h-auto sm:w-48" 
       src="profile.jpg" 
       alt="Profile" />
  <div class="p-8">
    <div class="uppercase tracking-wide text-sm text-indigo-500 font-semibold">
      Product Engineer
    </div>
    <h2 class="mt-1 text-xl font-semibold text-gray-900">
      John Doe
    </h2>
    <p class="mt-2 text-gray-500">
      Building amazing products with modern technology.
    </p>
    <button class="mt-4 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition">
      Contact
    </button>
  </div>
</div>
```

### Navigation Bar

```html
<nav class="bg-white shadow-lg">
  <div class="container mx-auto px-4">
    <div class="flex justify-between items-center h-16">
      <div class="flex items-center">
        <a href="#" class="text-xl font-bold text-gray-800">Logo</a>
      </div>
      <div class="hidden md:flex space-x-8">
        <a href="#" class="text-gray-700 hover:text-blue-600 transition">Home</a>
        <a href="#" class="text-gray-700 hover:text-blue-600 transition">About</a>
        <a href="#" class="text-gray-700 hover:text-blue-600 transition">Services</a>
        <a href="#" class="text-gray-700 hover:text-blue-600 transition">Contact</a>
      </div>
      <button class="md:hidden">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
        </svg>
      </button>
    </div>
  </div>
</nav>
```

### Form Elements

```html
<form class="space-y-6 max-w-md mx-auto">
  <div>
    <label class="block text-sm font-medium text-gray-700 mb-2">
      Email
    </label>
    <input 
      type="email" 
      class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
      placeholder="you@example.com"
    />
  </div>
  
  <div>
    <label class="block text-sm font-medium text-gray-700 mb-2">
      Password
    </label>
    <input 
      type="password" 
      class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
    />
  </div>
  
  <div class="flex items-center">
    <input type="checkbox" class="mr-2" />
    <label class="text-sm text-gray-600">Remember me</label>
  </div>
  
  <button 
    type="submit"
    class="w-full bg-blue-600 text-white font-semibold py-2 px-4 rounded-lg hover:bg-blue-700 transition"
  >
    Sign In
  </button>
</form>
```

### Modal/Dialog

```html
<div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
  <div class="bg-white rounded-lg shadow-xl max-w-md w-full p-6">
    <div class="flex justify-between items-center mb-4">
      <h3 class="text-xl font-bold">Modal Title</h3>
      <button class="text-gray-500 hover:text-gray-700">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
        </svg>
      </button>
    </div>
    <p class="text-gray-700 mb-6">
      Modal content goes here.
    </p>
    <div class="flex justify-end space-x-4">
      <button class="px-4 py-2 text-gray-600 hover:text-gray-800">
        Cancel
      </button>
      <button class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
        Confirm
      </button>
    </div>
  </div>
</div>
```

## Responsive Design Patterns

### Mobile-First Responsive Layout

```html
<div class="container mx-auto px-4">
  <!-- Hero Section -->
  <div class="flex flex-col md:flex-row items-center gap-8 py-12">
    <div class="flex-1">
      <h1 class="text-3xl md:text-5xl font-bold mb-4">
        Welcome to Our Site
      </h1>
      <p class="text-lg text-gray-600 mb-6">
        Build amazing things with Tailwind CSS
      </p>
      <button class="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700">
        Get Started
      </button>
    </div>
    <div class="flex-1">
      <img src="hero.jpg" class="w-full rounded-lg shadow-lg" />
    </div>
  </div>
</div>
```

### Responsive Grid Gallery

```html
<div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 p-4">
  <div class="aspect-square bg-gray-200 rounded-lg overflow-hidden">
    <img src="image1.jpg" class="w-full h-full object-cover hover:scale-105 transition" />
  </div>
  <div class="aspect-square bg-gray-200 rounded-lg overflow-hidden">
    <img src="image2.jpg" class="w-full h-full object-cover hover:scale-105 transition" />
  </div>
  <!-- More items... -->
</div>
```

## Dark Mode

### Basic Dark Mode Support

```html
<div class="bg-white dark:bg-gray-900 text-gray-900 dark:text-white">
  <h1 class="text-gray-900 dark:text-white">Title</h1>
  <p class="text-gray-600 dark:text-gray-400">Description</p>
</div>
```

Enable dark mode in tailwind.config.js:

```javascript
module.exports = {
  darkMode: 'class', // or 'media'
  // ...
}
```

## Animations & Transitions

### Basic Transitions

```html
<button class="bg-blue-500 hover:bg-blue-700 transition duration-300">
  Smooth transition
</button>
```

### Transform Effects

```html
<div class="transform hover:scale-110 transition duration-300">
  Scale on hover
</div>

<img class="transform hover:rotate-6 transition duration-300" />
```

### Built-in Animations

```html
<div class="animate-spin">Spinning</div>
<div class="animate-pulse">Pulsing</div>
<div class="animate-bounce">Bouncing</div>
```

## Performance Optimization

### Bundle Size Optimization

Configure content sources for optimal purging:

```javascript
// tailwind.config.js
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx,vue,svelte}",
    "./node_modules/@mycompany/ui-lib/**/*.{js,ts,jsx,tsx}",
  ],
  // Enable JIT for faster builds
  jit: true,
}
```

### CSS Optimization Techniques

```html
<!-- Use content-visibility for offscreen content -->
<div class="content-visibility-auto">
  <div>Heavy content that's initially offscreen</div>
</div>

<!-- Optimize images with aspect-ratio -->
<img class="aspect-video w-full object-cover" src="video.jpg" alt="Video thumbnail" />

<!-- Use contain for paint optimization -->
<div class="contain-layout">
  Complex layout that doesn't affect outside elements
</div>
```

### Development Performance

```css
/* Enable CSS-first configuration in v4.1 */
@import "tailwindcss";

@theme {
  /* Define once, use everywhere */
  --color-brand: #3b82f6;
  --font-mono: "Fira Code", monospace;
}

/* Critical CSS for above-the-fold content */
@layer critical {
  .hero-title {
    @apply text-4xl md:text-6xl font-bold;
  }
}
```

## Accessibility Guidelines

### Focus Management

```html
<!-- Custom focus styles that meet WCAG AA -->
<button class="focus:outline-none focus:ring-4 focus:ring-blue-500 focus:ring-offset-2">
  Accessible Button
</button>

<!-- Skip links for keyboard navigation -->
<a href="#main-content" class="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4">
  Skip to main content
</a>
```

### Screen Reader Support

```html
<!-- Semantic buttons with ARIA labels -->
<button aria-label="Close dialog" class="p-2">
  <svg class="w-5 h-5" fill="none" stroke="currentColor">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
  </svg>
</button>

<!-- Descriptive links -->
<a href="/docs" aria-describedby="docs-description">
  Documentation
</a>
<p id="docs-description" class="sr-only">
  Learn how to use our API and integration guides
</p>
```

### Color Contrast

```html
<!-- Ensure sufficient contrast ratios -->
<div class="bg-gray-900 text-white">
  High contrast text (WCAG AAA)
</div>

<div class="bg-blue-500 text-blue-100">
  Good contrast on colored backgrounds
</div>

<!-- Use contrast utilities for testing -->
<div class="bg-red-500 text-white contrast-more:bg-red-600 contrast-more:text-red-100">
  Adjusts for high contrast mode
</div>
```

### Motion Preferences

```html
<!-- Respect prefers-reduced-motion -->
<div class="transform transition-transform motion-reduce:transition-none">
  Doesn't animate when user prefers reduced motion
</div>

<!-- Conditional animations -->
<div class="animate-pulse motion-safe:hover:animate-spin">
  Only animates when motion is preferred
</div>
```

## Best Practices

1. **Mobile-First**: Start with mobile styles, add responsive prefixes for larger screens
2. **Consistent Spacing**: Use Tailwind's spacing scale (4, 8, 12, 16, etc.)
3. **Color Palette**: Stick to Tailwind's color system for consistency
4. **Component Extraction**: Extract repeated patterns into components
5. **Utility Composition**: Prefer utility classes over @apply for better maintainability
6. **Semantic HTML**: Use proper HTML elements with Tailwind classes
7. **Performance**: Configure content paths correctly for optimal CSS purging
8. **Accessibility**: Include focus styles, ARIA labels, and respect user preferences
9. **CSS-First Config**: Use @theme directive for v4.1+ instead of JavaScript config
10. **Custom Utilities**: Create reusable utilities with @utility for complex patterns

## Configuration

### CSS-First Configuration (v4.1+)

Use the `@theme` directive for CSS-based configuration:

```css
/* src/styles.css */
@import "tailwindcss";

@theme {
  /* Custom colors */
  --color-brand-50: #f0f9ff;
  --color-brand-500: #3b82f6;
  --color-brand-900: #1e3a8a;

  /* Custom fonts */
  --font-display: "Inter", system-ui, sans-serif;
  --font-mono: "Fira Code", monospace;

  /* Custom spacing */
  --spacing-128: 32rem;

  /* Custom animations */
  --animate-fade-in: fadeIn 0.5s ease-in-out;

  /* Custom breakpoints */
  --breakpoint-3xl: 1920px;
}

/* Define custom animations */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* Custom utilities */
@utility content-auto {
  content-visibility: auto;
}
```

### JavaScript Configuration (Legacy)

```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx,vue,svelte}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f9ff',
          500: '#3b82f6',
          900: '#1e3a8a',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      spacing: {
        '128': '32rem',
      },
    },
  },
  plugins: [],
}
```

### Vite Integration (v4.1+)

```javascript
// vite.config.ts
import { defineConfig } from 'vite'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [
    tailwindcss(),
  ],
})
```

## Advanced v4.1 Features

### Native CSS Custom Properties

```html
<div class="bg-[var(--color-brand-500)] text-[var(--color-white)]">
  Using CSS custom properties directly
</div>
```

### Enhanced Arbitrary Values

```html
<!-- Complex grid with custom tracks -->
<div class="grid grid-cols-[repeat(auto-fit,minmax(250px,1fr))] gap-4">
  Responsive grid without custom CSS
</div>

<!-- Custom animation timing -->
<div class="animate-bounce ease-[cubic-bezier(0.68,-0.55,0.265,1.55)]">
  Bounce with custom easing
</div>
```

### Container Queries

```html
<!-- Component that responds to its container size -->
<div class="@container">
  <div class="@lg:text-xl @2xl:text-2xl">
    Text size based on container, not viewport
  </div>
</div>
```

## Common Patterns with React/JSX

```tsx
import { useState } from 'react';

function Button({ 
  variant = 'primary', 
  size = 'md', 
  children 
}: {
  variant?: 'primary' | 'secondary';
  size?: 'sm' | 'md' | 'lg';
  children: React.ReactNode;
}) {
  const baseClasses = 'font-semibold rounded transition';
  
  const variantClasses = {
    primary: 'bg-blue-600 text-white hover:bg-blue-700',
    secondary: 'bg-gray-200 text-gray-800 hover:bg-gray-300',
  };
  
  const sizeClasses = {
    sm: 'px-3 py-1 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg',
  };
  
  return (
    <button 
      className={`${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]}`}
    >
      {children}
    </button>
  );
}
```

## References

- Tailwind CSS Docs: https://tailwindcss.com/docs
- Tailwind UI: https://tailwindui.com
- Tailwind Play: https://play.tailwindcss.com
- Headless UI: https://headlessui.com
