---
name: tailwind-css
description: Tailwind CSS patterns for modern UI. Use when styling components, building responsive layouts, creating design systems, or any Tailwind/CSS work.
---

# Tailwind CSS Patterns

## Setup (tailwind.config.ts)
```typescript
import type { Config } from 'tailwindcss'

export default {
  content: ['./src/**/*.{ts,tsx}', './app/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          500: '#3b82f6',
          600: '#2563eb',
          900: '#1e3a8a',
        },
        // Use CSS variables for theming
        background: 'hsl(var(--background))',
        foreground: 'hsl(var(--foreground))',
      },
      fontFamily: {
        sans: ['Inter var', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      borderRadius: { DEFAULT: '0.5rem' },
      animation: {
        'fade-in': 'fadeIn 0.2s ease-in-out',
        'slide-up': 'slideUp 0.3s ease-out',
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
} satisfies Config
```

## Component Patterns

### Button
```tsx
const buttonVariants = {
  primary: 'bg-primary-600 text-white hover:bg-primary-700 focus:ring-primary-500',
  secondary: 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50',
  danger: 'bg-red-600 text-white hover:bg-red-700 focus:ring-red-500',
  ghost: 'text-gray-700 hover:bg-gray-100',
}

export function Button({ variant = 'primary', size = 'md', className, ...props }) {
  return (
    <button
      className={cn(
        'inline-flex items-center justify-center rounded-md font-medium',
        'focus:outline-none focus:ring-2 focus:ring-offset-2',
        'disabled:opacity-50 disabled:cursor-not-allowed',
        'transition-colors duration-150',
        {
          'px-3 py-1.5 text-sm': size === 'sm',
          'px-4 py-2 text-sm': size === 'md',
          'px-6 py-3 text-base': size === 'lg',
        },
        buttonVariants[variant],
        className,
      )}
      {...props}
    />
  )
}
```

### Card
```tsx
export function Card({ children, className }: { children: React.ReactNode; className?: string }) {
  return (
    <div className={cn('bg-white rounded-xl border border-gray-200 shadow-sm p-6', className)}>
      {children}
    </div>
  )
}
```

### Responsive Layout
```tsx
// Mobile-first: base = mobile, sm/md/lg = progressively larger
<div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
  {items.map(item => <Card key={item.id} />)}
</div>

// Sidebar layout
<div className="flex min-h-screen">
  <aside className="hidden lg:flex lg:w-64 lg:flex-col bg-gray-900 text-white">
    {/* Sidebar */}
  </aside>
  <main className="flex-1 overflow-auto">
    {/* Content */}
  </main>
</div>
```

### Dark Mode
```tsx
// tailwind.config.ts: darkMode: 'class'
// Root layout:
<html className={isDark ? 'dark' : ''}>

// Components use dark: prefix:
<div className="bg-white dark:bg-gray-900 text-gray-900 dark:text-white">
```

### cn() utility (merge classes)
```typescript
import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
// twMerge handles conflicting classes: cn('p-4', 'p-6') → 'p-6'
```

## Common Patterns
```tsx
// Loading skeleton
<div className="animate-pulse space-y-3">
  <div className="h-4 bg-gray-200 rounded w-3/4" />
  <div className="h-4 bg-gray-200 rounded w-1/2" />
</div>

// Badge
<span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
  Active
</span>

// Input with error state
<input className={cn(
  'block w-full rounded-md border px-3 py-2 text-sm focus:outline-none focus:ring-2',
  error
    ? 'border-red-300 focus:ring-red-500 text-red-900 placeholder:text-red-300'
    : 'border-gray-300 focus:ring-primary-500'
)} />

// Modal overlay
<div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
  <div className="bg-white rounded-xl shadow-2xl p-6 w-full max-w-md mx-4">
    {/* Modal content */}
  </div>
</div>
```

## Rules
- Mobile-first: style for mobile (no prefix), then override for larger screens
- Use `cn()` from clsx + tailwind-merge to compose dynamic classes
- Extract repeated class combos to reusable components — not @apply
- Use CSS variables for design tokens (colors, radius) for easy theming
- Avoid arbitrary values [w-123px] — use the design system scale
- `gap-` not `space-x/y-` for flex/grid layouts (more predictable)
- Dark mode via `dark:` prefix + class strategy (not media query)
- Use `@tailwindcss/forms` for better default form styling
