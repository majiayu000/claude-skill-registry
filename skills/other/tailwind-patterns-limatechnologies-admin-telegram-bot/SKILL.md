---
name: tailwind-patterns
description: Tailwind CSS patterns and utilities. Responsive design, dark mode, animations, custom components. Use when styling with Tailwind CSS.
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Tailwind Patterns - Utility-First CSS

## Purpose

Expert guidance for Tailwind CSS:

- **Responsive Design** - Mobile-first breakpoints
- **Dark Mode** - Theming patterns
- **Animations** - Transitions and keyframes
- **Layout** - Flexbox and Grid patterns
- **Custom Utilities** - Extending Tailwind

---

## Responsive Breakpoints

### Default Breakpoints

```typescript
// Mobile-first approach
const breakpoints = {
	sm: '640px', // Small devices
	md: '768px', // Tablets
	lg: '1024px', // Laptops
	xl: '1280px', // Desktops
	'2xl': '1536px', // Large screens
};
```

### Usage Pattern

```tsx
// Mobile-first: styles apply from that breakpoint UP
<div className="
  w-full          // All screens
  md:w-1/2        // >= 768px
  lg:w-1/3        // >= 1024px
  xl:w-1/4        // >= 1280px
">
```

### Custom Breakpoints

```javascript
// tailwind.config.js
module.exports = {
	theme: {
		screens: {
			xs: '375px', // iPhone SE
			sm: '640px',
			md: '768px',
			lg: '1024px',
			xl: '1280px',
			'2xl': '1536px',
		},
	},
};
```

---

## Layout Patterns

### Flexbox

```tsx
// Center content
<div className="flex items-center justify-center h-screen">
  <Content />
</div>

// Space between
<div className="flex items-center justify-between">
  <Logo />
  <Navigation />
</div>

// Column layout
<div className="flex flex-col gap-4">
  <Header />
  <Main />
  <Footer />
</div>

// Responsive direction
<div className="flex flex-col md:flex-row gap-4">
  <Sidebar />
  <Content />
</div>
```

### Grid

```tsx
// Basic grid
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  {items.map((item) => <Card key={item.id} />)}
</div>

// Auto-fit grid
<div className="grid grid-cols-[repeat(auto-fit,minmax(300px,1fr))] gap-4">
  {items.map((item) => <Card key={item.id} />)}
</div>

// Complex layout
<div className="grid grid-cols-12 gap-4">
  <aside className="col-span-12 lg:col-span-3">Sidebar</aside>
  <main className="col-span-12 lg:col-span-9">Content</main>
</div>
```

### Container

```tsx
// Centered container with padding
<div className="container mx-auto px-4">
  <Content />
</div>

// Max-width variations
<div className="max-w-screen-xl mx-auto px-4 sm:px-6 lg:px-8">
  <Content />
</div>
```

---

## Common Component Patterns

### Card

```tsx
<div
	className="
  bg-white dark:bg-gray-800
  rounded-lg shadow-md
  p-6
  border border-gray-200 dark:border-gray-700
  hover:shadow-lg transition-shadow
"
>
	<h3 className="text-lg font-semibold text-gray-900 dark:text-white">Title</h3>
	<p className="mt-2 text-gray-600 dark:text-gray-300">Description</p>
</div>
```

### Button

```tsx
// Primary
<button className="
  bg-primary text-primary-foreground
  px-4 py-2 rounded-md
  font-medium
  hover:bg-primary/90
  focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2
  disabled:opacity-50 disabled:cursor-not-allowed
  transition-colors
">
  Click me
</button>

// Icon button
<button className="
  p-2 rounded-full
  hover:bg-gray-100 dark:hover:bg-gray-800
  focus:outline-none focus:ring-2 focus:ring-offset-2
  transition-colors
">
  <Icon className="h-5 w-5" />
  <span className="sr-only">Action</span>
</button>
```

### Input

```tsx
<input
	type="text"
	className="
    w-full px-3 py-2
    bg-white dark:bg-gray-900
    border border-gray-300 dark:border-gray-700
    rounded-md
    text-gray-900 dark:text-white
    placeholder:text-gray-400
    focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent
    disabled:opacity-50 disabled:cursor-not-allowed
  "
	placeholder="Enter text..."
/>
```

---

## Dark Mode

### Setup

```javascript
// tailwind.config.js
module.exports = {
	darkMode: 'class', // or 'media' for system preference
};
```

### Usage

```tsx
<div
	className="
  bg-white dark:bg-gray-900
  text-gray-900 dark:text-white
  border-gray-200 dark:border-gray-800
"
>
	<p className="text-gray-600 dark:text-gray-300">Content adapts to theme</p>
</div>
```

### Theme Provider

```tsx
'use client';

import { ThemeProvider } from 'next-themes';

export function Providers({ children }: { children: React.ReactNode }) {
	return (
		<ThemeProvider attribute="class" defaultTheme="system" enableSystem>
			{children}
		</ThemeProvider>
	);
}
```

---

## Animations

### Transitions

```tsx
// Color transition
<button className="bg-blue-500 hover:bg-blue-600 transition-colors duration-200">
  Hover me
</button>

// Multiple properties
<div className="transform hover:scale-105 transition-all duration-300 ease-in-out">
  Scale on hover
</div>

// Custom timing
<div className="transition-transform duration-500 ease-[cubic-bezier(0.4,0,0.2,1)]">
  Custom easing
</div>
```

### Built-in Animations

```tsx
// Spin
<Loader className="h-5 w-5 animate-spin" />

// Pulse (skeleton loading)
<div className="h-4 w-24 bg-gray-200 animate-pulse rounded" />

// Bounce
<div className="animate-bounce">New!</div>

// Ping
<span className="relative flex h-3 w-3">
  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75" />
  <span className="relative inline-flex rounded-full h-3 w-3 bg-red-500" />
</span>
```

### Custom Animations

```javascript
// tailwind.config.js
module.exports = {
	theme: {
		extend: {
			animation: {
				'fade-in': 'fadeIn 0.3s ease-in-out',
				'slide-up': 'slideUp 0.3s ease-out',
				'slide-down': 'slideDown 0.3s ease-out',
			},
			keyframes: {
				fadeIn: {
					'0%': { opacity: '0' },
					'100%': { opacity: '1' },
				},
				slideUp: {
					'0%': { transform: 'translateY(10px)', opacity: '0' },
					'100%': { transform: 'translateY(0)', opacity: '1' },
				},
				slideDown: {
					'0%': { transform: 'translateY(-10px)', opacity: '0' },
					'100%': { transform: 'translateY(0)', opacity: '1' },
				},
			},
		},
	},
};
```

---

## Typography

```tsx
// Headings
<h1 className="text-4xl font-bold tracking-tight text-gray-900 dark:text-white">
  Heading 1
</h1>

// Body text
<p className="text-base text-gray-600 dark:text-gray-300 leading-relaxed">
  Body text with comfortable line height.
</p>

// Small/muted text
<span className="text-sm text-gray-500 dark:text-gray-400">
  Secondary information
</span>

// Truncate
<p className="truncate">Very long text that will be truncated...</p>

// Line clamp
<p className="line-clamp-3">
  Long text that will be limited to 3 lines...
</p>
```

---

## Spacing System

```tsx
// Consistent spacing scale (4px base)
<div className="space-y-4">    {/* 16px gap between children */}
  <Item />
  <Item />
</div>

// Padding
<div className="p-4">          {/* 16px all sides */}
<div className="px-4 py-2">    {/* 16px horizontal, 8px vertical */}
<div className="pt-8 pb-4">    {/* 32px top, 16px bottom */}

// Margin
<div className="mt-4">         {/* 16px top margin */}
<div className="mx-auto">      {/* auto horizontal margins (center) */}

// Gap (for flex/grid)
<div className="flex gap-4">   {/* 16px gap between items */}
```

---

## Hiding/Showing

```tsx
// Hide on mobile, show on desktop
<div className="hidden lg:block">Desktop only</div>

// Show on mobile, hide on desktop
<div className="block lg:hidden">Mobile only</div>

// Screen reader only
<span className="sr-only">For screen readers</span>

// Not screen reader only (visible)
<span className="not-sr-only">Visible</span>
```

---

## Custom Utilities

### Extend Theme

```javascript
// tailwind.config.js
module.exports = {
	theme: {
		extend: {
			colors: {
				brand: {
					50: '#f0f9ff',
					500: '#3b82f6',
					900: '#1e3a8a',
				},
			},
			spacing: {
				18: '4.5rem',
				88: '22rem',
			},
			fontSize: {
				xxs: '0.625rem',
			},
		},
	},
};
```

### Plugin

```javascript
// tailwind.config.js
const plugin = require('tailwindcss/plugin');

module.exports = {
	plugins: [
		plugin(function ({ addUtilities }) {
			addUtilities({
				'.scrollbar-hide': {
					'-ms-overflow-style': 'none',
					'scrollbar-width': 'none',
					'&::-webkit-scrollbar': {
						display: 'none',
					},
				},
			});
		}),
	],
};
```

---

## Agent Integration

This skill is used by:

- **tailwind-expert** subagent
- **ui-mobile/tablet/desktop** agents
- **design-system-enforcer** agent
- **render-optimizer** for performance

---

## FORBIDDEN

1. **`!important`** - Fix specificity properly
2. **Arbitrary values when utilities exist** - Use the scale
3. **Mixing CSS with Tailwind** - Stick to utilities
4. **Overly long class strings** - Use @apply or components
5. **Inconsistent spacing** - Follow the 4px scale

---

## Version

- **v1.0.0** - Initial implementation based on Tailwind CSS 3.x patterns
