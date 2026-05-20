# Tailwind CSS Skill

---
progressive_disclosure:
  entry_point:
    - summary
    - when_to_use
    - quick_start
  sections:
    core_concepts:
      - utility_first_approach
      - responsive_design
      - configuration
    advanced:
      - dark_mode
      - custom_utilities
      - plugins
      - performance_optimization
    integration:
      - framework_integration
      - component_patterns
    reference:
      - common_utilities
      - breakpoints
      - color_system
tokens:
  entry: 75
  full: 4500
---

## Summary

Tailwind CSS is a utility-first CSS framework that provides low-level utility classes to build custom designs without writing CSS. It offers responsive design, dark mode, customization through configuration, and integrates seamlessly with modern frameworks.

## When to Use

**Best for:**
- Rapid prototyping with consistent design systems
- Component-based frameworks (React, Vue, Svelte)
- Projects requiring responsive and dark mode support
- Teams wanting to avoid CSS file maintenance
- Design systems with standardized spacing/colors

**Consider alternatives when:**
- Team unfamiliar with utility-first approach (learning curve)
- Project requires extensive custom CSS animations
- Legacy browser support needed (IE11)
- Minimal CSS footprint required without build process

## Quick Start

### Installation

```bash
# npm
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# yarn
yarn add -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# pnpm
pnpm add -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

### Configuration

**tailwind.config.js:**
```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./public/index.html",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

### Basic CSS Setup

**styles/globals.css:**
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

### First Component

```jsx
// Simple button with Tailwind utilities
function Button({ children, variant = 'primary' }) {
  const baseClasses = "px-4 py-2 rounded-lg font-medium transition-colors";
  const variants = {
    primary: "bg-blue-600 text-white hover:bg-blue-700",
    secondary: "bg-gray-200 text-gray-900 hover:bg-gray-300",
    danger: "bg-red-600 text-white hover:bg-red-700"
  };

  return (
    <button className={`${baseClasses} ${variants[variant]}`}>
      {children}
    </button>
  );
}
```

---

## Core Concepts

### Utility-First Approach

Tailwind provides single-purpose utility classes that map directly to CSS properties.

#### Layout Utilities

**Flexbox:**
```jsx
// Centered flex container
<div className="flex items-center justify-center">
  <div>Centered content</div>
</div>

// Responsive flex direction
<div className="flex flex-col md:flex-row gap-4">
  <div className="flex-1">Column 1</div>
  <div className="flex-1">Column 2</div>
</div>

// Flex wrapping and alignment
<div className="flex flex-wrap items-start justify-between">
  <div className="w-1/2 md:w-1/4">Item</div>
  <div className="w-1/2 md:w-1/4">Item</div>
</div>
```

**Grid:**
```jsx
// Basic grid
<div className="grid grid-cols-3 gap-4">
  <div>1</div>
  <div>2</div>
  <div>3</div>
</div>

// Responsive grid
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
  <div className="col-span-1 md:col-span-2">Wide item</div>
  <div>Item</div>
  <div>Item</div>
</div>

// Auto-fit grid
<div className="grid grid-cols-[repeat(auto-fit,minmax(250px,1fr))] gap-4">
  <div>Auto-sized item</div>
  <div>Auto-sized item</div>
</div>
```

#### Spacing System

**Padding and Margin:**
```jsx
// Uniform spacing
<div className="p-4">Padding all sides</div>
<div className="m-8">Margin all sides</div>

// Directional spacing
<div className="pt-4 pb-8 px-6">Top 4, bottom 8, horizontal 6</div>
<div className="ml-auto mr-0">Right-aligned with margin</div>

// Negative margins
<div className="mt-4 -mb-2">Overlap bottom</div>

// Responsive spacing
<div className="p-2 md:p-4 lg:p-8">Responsive padding</div>
```

**Space Between:**
```jsx
// Gap between children
<div className="flex gap-4">
  <div>Item 1</div>
  <div>Item 2</div>
</div>

// Responsive gap
<div className="grid grid-cols-3 gap-2 md:gap-4 lg:gap-6">
  <div>1</div>
  <div>2</div>
  <div>3</div>
</div>
```

#### Typography

```jsx
// Font sizes and weights
<h1 className="text-4xl font-bold">Heading</h1>
<p className="text-base font-normal leading-relaxed">Paragraph</p>
<span className="text-sm font-medium text-gray-600">Caption</span>

// Text alignment and decoration
<p className="text-center underline">Centered underlined text</p>
<p className="text-right line-through">Right-aligned strikethrough</p>

// Responsive typography
<h1 className="text-2xl md:text-4xl lg:text-6xl font-bold">
  Responsive heading
</h1>

// Text overflow handling
<p className="truncate">This text will be truncated with ellipsis...</p>
<p className="line-clamp-3">
  This text will be clamped to 3 lines with ellipsis...
</p>
```

#### Colors

```jsx
// Background colors
<div className="bg-blue-500">Blue background</div>
<div className="bg-gray-100 dark:bg-gray-800">Adaptive background</div>

// Text colors
<p className="text-red-600">Red text</p>
<p className="text-gray-700 dark:text-gray-300">Adaptive text</p>

// Border colors
<div className="border border-gray-300 hover:border-blue-500">
  Hover border
</div>

// Opacity modifiers
<div className="bg-blue-500/50">50% opacity blue</div>
<div className="bg-black/25">25% opacity black</div>
```

### Responsive Design

Tailwind uses mobile-first breakpoint system.

#### Breakpoints

```javascript
// Default breakpoints (tailwind.config.js)
{
  theme: {
    screens: {
      'sm': '640px',   // Small devices
      'md': '768px',   // Medium devices
      'lg': '1024px',  // Large devices
      'xl': '1280px',  // Extra large
      '2xl': '1536px', // 2X extra large
    }
  }
}
```

#### Responsive Patterns

```jsx
// Hide/show at breakpoints
<div className="hidden md:block">Visible on desktop</div>
<div className="block md:hidden">Visible on mobile</div>

// Responsive layout
<div className="
  flex flex-col          // Mobile: stack vertically
  md:flex-row           // Desktop: horizontal
  gap-4 md:gap-8        // Larger gap on desktop
">
  <aside className="w-full md:w-64">Sidebar</aside>
  <main className="flex-1">Content</main>
</div>

// Responsive grid
<div className="
  grid
  grid-cols-1           // Mobile: 1 column
  sm:grid-cols-2        // Small: 2 columns
  lg:grid-cols-3        // Large: 3 columns
  xl:grid-cols-4        // XL: 4 columns
  gap-4
">
  {items.map(item => <Card key={item.id} {...item} />)}
</div>

// Container with responsive padding
<div className="
  container mx-auto
  px-4 sm:px-6 lg:px-8
  max-w-7xl
">
  <h1>Responsive container</h1>
</div>
```

### Configuration

#### Theme Extension

**tailwind.config.js:**
```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{js,jsx,ts,tsx}'],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          500: '#0ea5e9',
          900: '#0c4a6e',
        },
        accent: '#ff6b6b',
      },
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
        '128': '32rem',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        display: ['Poppins', 'sans-serif'],
        mono: ['Fira Code', 'monospace'],
      },
      fontSize: {
        '2xs': '0.625rem',
        '3xl': '2rem',
      },
      borderRadius: {
        '4xl': '2rem',
      },
      boxShadow: {
        'inner-lg': 'inset 0 2px 4px 0 rgb(0 0 0 / 0.1)',
      },
      animation: {
        'slide-in': 'slideIn 0.3s ease-out',
        'fade-in': 'fadeIn 0.2s ease-in',
      },
      keyframes: {
        slideIn: {
          '0%': { transform: 'translateX(-100%)' },
          '100%': { transform: 'translateX(0)' },
        },
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
      },
    },
  },
  plugins: [],
}
```

#### Custom Breakpoints

```javascript
module.exports = {
  theme: {
    screens: {
      'xs': '475px',
      'sm': '640px',
      'md': '768px',
      'lg': '1024px',
      'xl': '1280px',
      '2xl': '1536px',
      '3xl': '1920px',
      // Custom breakpoints
      'tablet': '640px',
      'laptop': '1024px',
      'desktop': '1280px',
      // Max-width breakpoints
      'max-md': {'max': '767px'},
    },
  },
}
```

---

## Advanced Features

### Dark Mode

#### Class Strategy (Recommended)

**tailwind.config.js:**
```javascript
module.exports = {
  darkMode: 'class', // or 'media' for OS preference
  // ...
}
```

**Implementation:**
```jsx
// Toggle component
function DarkModeToggle() {
  const [isDark, setIsDark] = useState(false);

  useEffect(() => {
    if (isDark) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [isDark]);

  return (
    <button
      onClick={() => setIsDark(!isDark)}
      className="p-2 rounded-lg bg-gray-200 dark:bg-gray-700"
    >
      {isDark ? '🌞' : '🌙'}
    </button>
  );
}

// Dark mode styles
function Card() {
  return (
    <div className="
      bg-white dark:bg-gray-800
      text-gray-900 dark:text-gray-100
      border border-gray-200 dark:border-gray-700
      shadow-lg dark:shadow-none
    ">
      <h2 className="text-xl font-bold mb-2">Card Title</h2>
      <p className="text-gray-600 dark:text-gray-400">
        Card content adapts to dark mode
      </p>
    </div>
  );
}
```

#### System Preference Strategy

```javascript
// tailwind.config.js
module.exports = {
  darkMode: 'media', // Uses OS preference
}
```

```jsx
// Automatically adapts to system preference
<div className="bg-white dark:bg-gray-900">
  Content adapts automatically
</div>
```

### Custom Utilities

#### Adding Custom Utilities

**tailwind.config.js:**
```javascript
const plugin = require('tailwindcss/plugin');

module.exports = {
  plugins: [
    plugin(function({ addUtilities, addComponents, theme }) {
      // Custom utilities
      addUtilities({
        '.scrollbar-hide': {
          '-ms-overflow-style': 'none',
          'scrollbar-width': 'none',
          '&::-webkit-scrollbar': {
            display: 'none',
          },
        },
        '.text-balance': {
          'text-wrap': 'balance',
        },
      });

      // Custom components
      addComponents({
        '.btn': {
          padding: theme('spacing.4'),
          borderRadius: theme('borderRadius.lg'),
          fontWeight: theme('fontWeight.medium'),
          '&:hover': {
            opacity: 0.9,
          },
        },
        '.card': {
          backgroundColor: theme('colors.white'),
          borderRadius: theme('borderRadius.lg'),
          padding: theme('spacing.6'),
          boxShadow: theme('boxShadow.lg'),
        },
      });
    }),
  ],
}
```

#### Custom Variants

```javascript
const plugin = require('tailwindcss/plugin');

module.exports = {
  plugins: [
    plugin(function({ addVariant }) {
      // Custom variant for third child
      addVariant('third', '&:nth-child(3)');

      // Custom variant for not-last child
      addVariant('not-last', '&:not(:last-child)');

      // Custom variant for group-hover with specific element
      addVariant('group-hover-show', '.group:hover &');
    }),
  ],
}

// Usage
<div className="third:font-bold not-last:border-b">
  Custom variant styles
</div>
```

### Plugins

#### Official Plugins

```bash
npm install -D @tailwindcss/forms @tailwindcss/typography @tailwindcss/aspect-ratio
```

**tailwind.config.js:**
```javascript
module.exports = {
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
    require('@tailwindcss/aspect-ratio'),
  ],
}
```

#### Forms Plugin

```jsx
// Automatic form styling
<form className="space-y-4">
  <input
    type="text"
    className="
      form-input
      rounded-lg
      border-gray-300
      focus:border-blue-500
      focus:ring-blue-500
    "
    placeholder="Name"
  />

  <select className="form-select rounded-lg">
    <option>Option 1</option>
    <option>Option 2</option>
  </select>

  <label className="flex items-center">
    <input type="checkbox" className="form-checkbox text-blue-600" />
    <span className="ml-2">Agree to terms</span>
  </label>
</form>
```

#### Typography Plugin

```jsx
// Beautiful prose styling
<article className="
  prose
  prose-lg
  prose-slate
  dark:prose-invert
  max-w-none
">
  <h1>Article Title</h1>
  <p>Automatic typography styles for markdown content...</p>
  <ul>
    <li>Styled lists</li>
    <li>Proper spacing</li>
  </ul>
</article>
```

#### Aspect Ratio Plugin

```jsx
// Maintain aspect ratios
<div className="aspect-w-16 aspect-h-9">
  <iframe src="..." className="w-full h-full" />
</div>

<div className="aspect-square">
  <img src="..." className="object-cover w-full h-full" />
</div>
```

### Performance Optimization

#### Content Configuration

```javascript
// Optimize purge paths
module.exports = {
  content: [
    './src/**/*.{js,jsx,ts,tsx}',
    './public/index.html',
    // Include component libraries
    './node_modules/@my-ui/**/*.js',
  ],
  // Safelist dynamic classes
  safelist: [
    'bg-red-500',
    'bg-green-500',
    {
      pattern: /bg-(red|green|blue)-(400|500|600)/,
      variants: ['hover', 'focus'],
    },
  ],
}
```

#### JIT Mode (Default in v3+)

Just-In-Time compilation generates styles on-demand:

```jsx
// Arbitrary values work instantly
<div className="top-[117px]">Custom value</div>
<div className="bg-[#1da1f2]">Custom color</div>
<div className="grid-cols-[1fr_500px_2fr]">Custom grid</div>

// No rebuild needed for new utilities
<div className="before:content-['★']">Star before</div>
```

#### Build Optimization

```javascript
// postcss.config.js
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
    // Production minification
    ...(process.env.NODE_ENV === 'production'
      ? { cssnano: {} }
      : {}),
  },
}
```

---

## Framework Integration

### React / Next.js

**Installation:**
```bash
npx create-next-app@latest my-app --tailwind
# or add to existing project
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

**next.config.js:**
```javascript
/** @type {import('next').NextConfig} */
module.exports = {
  // Tailwind works out of box with Next.js
}
```

**_app.tsx:**
```typescript
import '@/styles/globals.css'
import type { AppProps } from 'next/app'

export default function App({ Component, pageProps }: AppProps) {
  return <Component {...pageProps} />
}
```

**Component Example:**
```tsx
// components/Button.tsx
import { ButtonHTMLAttributes, forwardRef } from 'react'
import { cva, type VariantProps } from 'class-variance-authority'

const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-lg font-medium transition-colors",
  {
    variants: {
      variant: {
        default: "bg-blue-600 text-white hover:bg-blue-700",
        outline: "border border-gray-300 hover:bg-gray-100",
        ghost: "hover:bg-gray-100",
      },
      size: {
        sm: "px-3 py-1.5 text-sm",
        md: "px-4 py-2",
        lg: "px-6 py-3 text-lg",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "md",
    },
  }
)

interface ButtonProps
  extends ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {}

const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, ...props }, ref) => {
    return (
      <button
        ref={ref}
        className={buttonVariants({ variant, size, className })}
        {...props}
      />
    )
  }
)

export default Button
```

### SvelteKit

**Installation:**
```bash
npx sv create my-app
# Select Tailwind CSS option
# or add to existing
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

**svelte.config.js:**
```javascript
import adapter from '@sveltejs/adapter-auto';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

export default {
  preprocess: vitePreprocess(),
  kit: {
    adapter: adapter()
  }
};
```

**Component Example:**
```svelte
<!-- Button.svelte -->
<script lang="ts">
  export let variant: 'primary' | 'secondary' = 'primary';
  export let size: 'sm' | 'md' | 'lg' = 'md';

  const variants = {
    primary: 'bg-blue-600 text-white hover:bg-blue-700',
    secondary: 'bg-gray-200 text-gray-900 hover:bg-gray-300'
  };

  const sizes = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2',
    lg: 'px-6 py-3 text-lg'
  };
</script>

<button
  class="rounded-lg font-medium transition-colors {variants[variant]} {sizes[size]}"
  on:click
>
  <slot />
</button>
```

### Vue 3

**Installation:**
```bash
npm create vue@latest my-app
# Select Tailwind CSS
# or add to existing
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

**main.ts:**
```typescript
import { createApp } from 'vue'
import App from './App.vue'
import './assets/main.css'

createApp(App).mount('#app')
```

**Component Example:**
```vue
<!-- Button.vue -->
<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  variant?: 'primary' | 'secondary'
  size?: 'sm' | 'md' | 'lg'
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'primary',
  size: 'md'
})

const classes = computed(() => {
  const base = 'rounded-lg font-medium transition-colors'
  const variants = {
    primary: 'bg-blue-600 text-white hover:bg-blue-700',
    secondary: 'bg-gray-200 text-gray-900 hover:bg-gray-300'
  }
  const sizes = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2',
    lg: 'px-6 py-3 text-lg'
  }

  return `${base} ${variants[props.variant]} ${sizes[props.size]}`
})
</script>

<template>
  <button :class="classes">
    <slot />
  </button>
</template>
```

---

## Component Patterns

### Layout Components

#### Container

```jsx
function Container({ children, size = 'default' }) {
  const sizes = {
    sm: 'max-w-3xl',
    default: 'max-w-7xl',
    full: 'max-w-full'
  };

  return (
    <div className={`container mx-auto px-4 sm:px-6 lg:px-8 ${sizes[size]}`}>
      {children}
    </div>
  );
}
```

#### Grid Layout

```jsx
function GridLayout({ children, cols = { default: 1, md: 2, lg: 3 } }) {
  return (
    <div className={`
      grid
      grid-cols-${cols.default}
      md:grid-cols-${cols.md}
      lg:grid-cols-${cols.lg}
      gap-6
    `}>
      {children}
    </div>
  );
}
```

#### Stack (Vertical Spacing)

```jsx
function Stack({ children, spacing = 4 }) {
  return (
    <div className={`flex flex-col gap-${spacing}`}>
      {children}
    </div>
  );
}
```

### UI Components

#### Card

```jsx
function Card({ title, description, image, footer }) {
  return (
    <div className="
      bg-white dark:bg-gray-800
      rounded-lg shadow-lg
      overflow-hidden
      transition-transform hover:scale-105
    ">
      {image && (
        <img
          src={image}
          alt={title}
          className="w-full h-48 object-cover"
        />
      )}
      <div className="p-6">
        <h3 className="text-xl font-bold mb-2 text-gray-900 dark:text-white">
          {title}
        </h3>
        <p className="text-gray-600 dark:text-gray-400">
          {description}
        </p>
      </div>
      {footer && (
        <div className="px-6 py-4 bg-gray-50 dark:bg-gray-700 border-t border-gray-200 dark:border-gray-600">
          {footer}
        </div>
      )}
    </div>
  );
}
```

#### Modal

```jsx
function Modal({ isOpen, onClose, title, children }) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-black/50 backdrop-blur-sm"
        onClick={onClose}
      />

      {/* Modal */}
      <div className="flex min-h-full items-center justify-center p-4">
        <div className="
          relative bg-white dark:bg-gray-800
          rounded-lg shadow-xl
          max-w-md w-full
          p-6
          animate-fade-in
        ">
          <h2 className="text-2xl font-bold mb-4">
            {title}
          </h2>
          <button
            onClick={onClose}
            className="absolute top-4 right-4 text-gray-400 hover:text-gray-600"
          >
            ✕
          </button>
          {children}
        </div>
      </div>
    </div>
  );
}
```

#### Form Input

```jsx
function Input({ label, error, ...props }) {
  return (
    <div className="mb-4">
      {label && (
        <label className="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">
          {label}
        </label>
      )}
      <input
        className={`
          w-full px-4 py-2 rounded-lg
          border ${error ? 'border-red-500' : 'border-gray-300'}
          focus:outline-none focus:ring-2
          ${error ? 'focus:ring-red-500' : 'focus:ring-blue-500'}
          bg-white dark:bg-gray-700
          text-gray-900 dark:text-white
          placeholder-gray-400
        `}
        {...props}
      />
      {error && (
        <p className="mt-1 text-sm text-red-500">{error}</p>
      )}
    </div>
  );
}
```

#### Badge

```jsx
function Badge({ children, variant = 'default', size = 'md' }) {
  const variants = {
    default: 'bg-gray-100 text-gray-800',
    primary: 'bg-blue-100 text-blue-800',
    success: 'bg-green-100 text-green-800',
    warning: 'bg-yellow-100 text-yellow-800',
    danger: 'bg-red-100 text-red-800',
  };

  const sizes = {
    sm: 'text-xs px-2 py-0.5',
    md: 'text-sm px-2.5 py-1',
    lg: 'text-base px-3 py-1.5',
  };

  return (
    <span className={`
      inline-flex items-center
      rounded-full font-medium
      ${variants[variant]}
      ${sizes[size]}
    `}>
      {children}
    </span>
  );
}
```

---

## Reference

### Common Utility Classes

#### Display & Positioning

```
display: block, inline-block, inline, flex, inline-flex, grid, inline-grid, hidden
position: static, fixed, absolute, relative, sticky
top/right/bottom/left: 0, auto, 1-96 (in 0.25rem increments)
z-index: z-0, z-10, z-20, z-30, z-40, z-50, z-auto
```

#### Flexbox & Grid

```
flex-direction: flex-row, flex-col, flex-row-reverse, flex-col-reverse
justify-content: justify-start, justify-center, justify-end, justify-between, justify-around
align-items: items-start, items-center, items-end, items-baseline, items-stretch
gap: gap-0 to gap-96 (in 0.25rem increments)
grid-cols: grid-cols-1 to grid-cols-12, grid-cols-none
```

#### Sizing

```
width: w-0 to w-96, w-auto, w-full, w-screen, w-1/2, w-1/3, w-2/3, etc.
height: h-0 to h-96, h-auto, h-full, h-screen
min/max-width: min-w-0, min-w-full, max-w-xs to max-w-7xl
min/max-height: min-h-0, min-h-full, max-h-screen
```

#### Spacing (0.25rem = 4px increments)

```
padding: p-0 to p-96, px-*, py-*, pt-*, pr-*, pb-*, pl-*
margin: m-0 to m-96, mx-*, my-*, mt-*, mr-*, mb-*, ml-*, -m-*
space-between: space-x-*, space-y-*
```

#### Typography

```
font-size: text-xs, text-sm, text-base, text-lg, text-xl to text-9xl
font-weight: font-thin to font-black (100-900)
text-align: text-left, text-center, text-right, text-justify
line-height: leading-none to leading-loose
letter-spacing: tracking-tighter to tracking-widest
```

#### Colors (50-900 scale)

```
text-{color}-{shade}: text-gray-500, text-blue-600, text-red-700
bg-{color}-{shade}: bg-white, bg-gray-100, bg-blue-500
border-{color}-{shade}: border-gray-300, border-blue-500
Colors: slate, gray, zinc, neutral, stone, red, orange, amber, yellow, lime,
        green, emerald, teal, cyan, sky, blue, indigo, violet, purple, fuchsia,
        pink, rose
```

#### Borders

```
border-width: border, border-0, border-2, border-4, border-8
border-style: border-solid, border-dashed, border-dotted, border-double, border-none
border-radius: rounded-none, rounded-sm, rounded, rounded-lg, rounded-full
border-color: border-gray-300, etc.
```

#### Effects

```
shadow: shadow-sm, shadow, shadow-md, shadow-lg, shadow-xl, shadow-2xl, shadow-none
opacity: opacity-0 to opacity-100 (in 5% increments)
blur: blur-none, blur-sm, blur, blur-lg, blur-xl
```

#### Transitions & Animations

```
transition: transition-none, transition-all, transition, transition-colors, transition-opacity
duration: duration-75 to duration-1000 (ms)
timing: ease-linear, ease-in, ease-out, ease-in-out
animation: animate-none, animate-spin, animate-ping, animate-pulse, animate-bounce
```

### Responsive Breakpoints

```
sm:  640px  @media (min-width: 640px)
md:  768px  @media (min-width: 768px)
lg:  1024px @media (min-width: 1024px)
xl:  1280px @media (min-width: 1280px)
2xl: 1536px @media (min-width: 1536px)
```

### State Variants

```
hover:     &:hover
focus:     &:focus
active:    &:active
disabled:  &:disabled
visited:   &:visited (links)
checked:   &:checked (inputs)
group-hover: .group:hover &
peer-focus:  .peer:focus ~ &
first:     &:first-child
last:      &:last-child
odd:       &:nth-child(odd)
even:      &:nth-child(even)
```

### Dark Mode

```
dark:      .dark &
dark:hover: .dark &:hover
dark:focus: .dark &:focus
```

---

## Best Practices

### Class Organization

```jsx
// Group classes logically
<div className={`
  // Layout
  flex items-center justify-between
  // Spacing
  px-4 py-2 gap-2
  // Typography
  text-lg font-medium
  // Colors
  bg-white text-gray-900
  // Borders & Effects
  border border-gray-200 rounded-lg shadow-sm
  // States
  hover:bg-gray-50 focus:ring-2 focus:ring-blue-500
  // Responsive
  md:px-6 md:py-3
  // Dark mode
  dark:bg-gray-800 dark:text-white
`}>
  Content
</div>
```

### Extracting Components

```jsx
// DON'T repeat complex class strings
<button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
  Button 1
</button>
<button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
  Button 2
</button>

// DO extract to component
function Button({ children }) {
  return (
    <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
      {children}
    </button>
  );
}
```

### Using CSS Variables

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: 'rgb(var(--color-primary) / <alpha-value>)',
        secondary: 'rgb(var(--color-secondary) / <alpha-value>)',
      },
    },
  },
}
```

```css
/* globals.css */
:root {
  --color-primary: 59 130 246; /* RGB values for blue-500 */
  --color-secondary: 139 92 246; /* RGB values for purple-500 */
}

.dark {
  --color-primary: 96 165 250; /* Lighter blue for dark mode */
  --color-secondary: 167 139 250; /* Lighter purple for dark mode */
}
```

```jsx
// Usage with opacity
<div className="bg-primary/50 text-primary">
  50% opacity primary color
</div>
```

### Avoiding Class Conflicts

```jsx
// DON'T use conflicting utilities
<div className="text-center text-left"> {/* text-left wins */}

// DO use conditional classes
<div className={isCenter ? 'text-center' : 'text-left'}>

// Or use clsx/cn utility
import { clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

function cn(...inputs) {
  return twMerge(clsx(inputs))
}

<div className={cn(
  'text-center',
  isLeft && 'text-left'  // Properly overrides
)}>
```

---

## Troubleshooting

### Styles Not Applying

1. **Check content paths in config:**
   ```javascript
   content: ['./src/**/*.{js,jsx,ts,tsx}']
   ```

2. **Verify CSS imports:**
   ```css
   @tailwind base;
   @tailwind components;
   @tailwind utilities;
   ```

3. **Rebuild for dynamic classes:**
   ```javascript
   // DON'T - won't be detected
   <div className={`text-${color}-500`}>

   // DO - use safelist or complete class names
   <div className={color === 'red' ? 'text-red-500' : 'text-blue-500'}>
   ```

### Build Size Issues

1. **Optimize content configuration**
2. **Remove unused plugins**
3. **Use environment-specific configs**
4. **Enable compression in production**

### Dark Mode Not Working

1. **Check darkMode setting in config**
2. **Verify 'dark' class on html/body**
3. **Test dark: variant syntax**
4. **Check system preferences (media strategy)**

---

## Resources

- **Official Docs:** https://tailwindcss.com/docs
- **Playground:** https://play.tailwindcss.com
- **Tailwind UI:** https://tailwindui.com (Premium components)
- **Headless UI:** https://headlessui.com (Unstyled accessible components)
- **Tailwind CLI:** https://tailwindcss.com/docs/installation
- **Class Variance Authority:** https://cva.style (Type-safe variants)
- **Prettier Plugin:** https://github.com/tailwindlabs/prettier-plugin-tailwindcss