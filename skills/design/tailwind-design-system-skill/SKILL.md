---
name: "Tailwind CSS Design System"
description: "Build consistent, accessible UI components with Tailwind CSS, shadcn/ui, and custom design tokens. Apply when styling components, creating design systems, implementing responsive layouts, or optimizing CSS performance."
allowed-tools: Read, Write, Edit
version: 1.0.0
---

# Tailwind CSS Design System

Systematic Tailwind CSS usage with component patterns, design tokens, and shadcn/ui integration.

## Overview

This Skill enforces:
- Utility-first CSS with Tailwind
- Design tokens and custom configuration
- Component composition patterns
- shadcn/ui integration
- Responsive design (mobile-first)
- Dark mode support
- Performance optimization

Apply when styling components, building design systems, or implementing responsive layouts.

## Tailwind Configuration

### Custom Design Tokens

```ts
// tailwind.config.ts
import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}'
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          100: '#dbeafe',
          500: '#3b82f6',
          600: '#2563eb',
          900: '#1e3a8a'
        },
        secondary: {
          500: '#8b5cf6',
          600: '#7c3aed'
        }
      },
      spacing: {
        '18': '4.5rem',
        '22': '5.5rem'
      },
      fontSize: {
        'xs': '0.75rem',
        'sm': '0.875rem',
        'base': '1rem',
        'lg': '1.125rem',
        'xl': '1.25rem',
        '2xl': '1.5rem'
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace']
      },
      borderRadius: {
        'none': '0',
        'sm': '0.125rem',
        DEFAULT: '0.25rem',
        'md': '0.375rem',
        'lg': '0.5rem',
        'xl': '0.75rem',
        'full': '9999px'
      },
      boxShadow: {
        'sm': '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
        DEFAULT: '0 1px 3px 0 rgba(0, 0, 0, 0.1)',
        'md': '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
        'lg': '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
        'xl': '0 20px 25px -5px rgba(0, 0, 0, 0.1)',
        'glass': '0 8px 32px 0 rgba(31, 38, 135, 0.37)'
      }
    }
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography')
  ]
};

export default config;
```

## Component Patterns

### Button Component

```tsx
// components/ui/Button.tsx
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const buttonVariants = cva(
  'inline-flex items-center justify-center rounded-md font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 disabled:pointer-events-none disabled:opacity-50',
  {
    variants: {
      variant: {
        default: 'bg-primary-600 text-white hover:bg-primary-700',
        secondary: 'bg-secondary-500 text-white hover:bg-secondary-600',
        outline: 'border border-gray-300 bg-transparent hover:bg-gray-100',
        ghost: 'hover:bg-gray-100',
        danger: 'bg-red-600 text-white hover:bg-red-700'
      },
      size: {
        sm: 'h-9 px-3 text-sm',
        md: 'h-10 px-4 text-base',
        lg: 'h-11 px-8 text-lg',
        icon: 'h-10 w-10'
      }
    },
    defaultVariants: {
      variant: 'default',
      size: 'md'
    }
  }
);

interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  loading?: boolean;
}

export function Button({
  className,
  variant,
  size,
  loading,
  disabled,
  children,
  ...props
}: ButtonProps) {
  return (
    <button
      className={cn(buttonVariants({ variant, size, className }))}
      disabled={disabled || loading}
      {...props}
    >
      {loading && <span className="mr-2">Loading...</span>}
      {children}
    </button>
  );
}

// Usage
<Button variant="default" size="md">Submit</Button>
<Button variant="outline" size="sm">Cancel</Button>
<Button variant="danger" loading>Delete</Button>
```

### Card Component

```tsx
// components/ui/Card.tsx
import { cn } from '@/lib/utils';

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {}

export function Card({ className, children, ...props }: CardProps) {
  return (
    <div
      className={cn(
        'rounded-lg border border-gray-200 bg-white p-6 shadow-sm',
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
}

export function CardHeader({ className, children, ...props }: CardProps) {
  return (
    <div className={cn('mb-4', className)} {...props}>
      {children}
    </div>
  );
}

export function CardTitle({ className, children, ...props }: CardProps) {
  return (
    <h3 className={cn('text-2xl font-semibold', className)} {...props}>
      {children}
    </h3>
  );
}

export function CardContent({ className, children, ...props }: CardProps) {
  return (
    <div className={cn('', className)} {...props}>
      {children}
    </div>
  );
}

// Usage
<Card>
  <CardHeader>
    <CardTitle>Title</CardTitle>
  </CardHeader>
  <CardContent>
    <p>Content goes here</p>
  </CardContent>
</Card>
```

## Responsive Design (Mobile-First)

```tsx
// ✅ GOOD: Mobile-first responsive design
<div className="
  flex flex-col       // Mobile: stack vertically
  md:flex-row         // Tablet: horizontal layout
  lg:gap-8            // Desktop: larger spacing
">
  <aside className="
    w-full            // Mobile: full width
    md:w-64           // Tablet: fixed sidebar width
  ">
    Sidebar
  </aside>
  <main className="
    w-full            // Mobile: full width
    md:flex-1         // Tablet+: flexible main content
  ">
    Content
  </main>
</div>

// ✅ GOOD: Responsive typography
<h1 className="
  text-2xl          // Mobile: smaller
  md:text-3xl       // Tablet: medium
  lg:text-4xl       // Desktop: larger
  font-bold
">
  Heading
</h1>

// ✅ GOOD: Responsive padding
<section className="
  p-4              // Mobile: smaller padding
  md:p-6           // Tablet: medium padding
  lg:p-8           // Desktop: larger padding
">
  Content
</section>
```

## Dark Mode Support

```tsx
// tailwind.config.ts
module.exports = {
  darkMode: 'class',  // Use class-based dark mode
  // ...
};

// Usage
<div className="
  bg-white           // Light mode
  dark:bg-gray-900   // Dark mode
  text-gray-900
  dark:text-white
">
  Content
</div>

// Toggle dark mode
'use client';

import { useEffect, useState } from 'react';

export function ThemeToggle() {
  const [theme, setTheme] = useState('light');

  useEffect(() => {
    const root = document.documentElement;
    root.classList.remove('light', 'dark');
    root.classList.add(theme);
    localStorage.setItem('theme', theme);
  }, [theme]);

  return (
    <button
      onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}
      className="p-2 rounded-md bg-gray-200 dark:bg-gray-700"
    >
      {theme === 'light' ? '🌙' : '☀️'}
    </button>
  );
}
```

## Glassmorphism Pattern

```tsx
<div className="
  relative
  rounded-xl
  bg-white/10
  backdrop-blur-lg
  border border-white/20
  shadow-glass
  p-6
">
  Glass card content
</div>

// tailwind.config.ts
boxShadow: {
  'glass': '0 8px 32px 0 rgba(31, 38, 135, 0.37)'
}
```

## Form Components

```tsx
// components/ui/Input.tsx
import { cn } from '@/lib/utils';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  error?: string;
}

export function Input({ className, error, ...props }: InputProps) {
  return (
    <div className="w-full">
      <input
        className={cn(
          'w-full rounded-md border border-gray-300 px-3 py-2',
          'focus:outline-none focus:ring-2 focus:ring-primary-500',
          'disabled:cursor-not-allowed disabled:opacity-50',
          error && 'border-red-500 focus:ring-red-500',
          className
        )}
        {...props}
      />
      {error && <p className="mt-1 text-sm text-red-600">{error}</p>}
    </div>
  );
}

// Usage
<Input placeholder="Email" error={errors.email} />
```

## Layout Patterns

### Container

```tsx
<div className="container mx-auto px-4 md:px-6 lg:px-8 max-w-7xl">
  Content
</div>
```

### Grid

```tsx
<div className="
  grid
  grid-cols-1         // Mobile: 1 column
  md:grid-cols-2      // Tablet: 2 columns
  lg:grid-cols-3      // Desktop: 3 columns
  gap-4
">
  <div>Item 1</div>
  <div>Item 2</div>
  <div>Item 3</div>
</div>
```

### Flexbox

```tsx
<div className="flex items-center justify-between">
  <span>Left</span>
  <span>Right</span>
</div>
```

## Performance Optimization

### Purge Unused Classes

```ts
// tailwind.config.ts
module.exports = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}'
  ],
  // Tailwind automatically purges unused classes in production
};
```

### Use @layer for Custom CSS

```css
/* app/globals.css */
@layer components {
  .btn-primary {
    @apply bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700;
  }
}
```

## Anti-Patterns

```tsx
// ❌ BAD: Inline styles instead of Tailwind
<div style={{ backgroundColor: 'blue', padding: '16px' }}>
  Content
</div>

// ✅ GOOD: Use Tailwind classes
<div className="bg-blue-500 p-4">
  Content
</div>

// ❌ BAD: Magic numbers
<div className="mt-[23px] w-[347px]">
  Content
</div>

// ✅ GOOD: Use spacing scale
<div className="mt-6 w-80">
  Content
</div>

// ❌ BAD: Non-responsive
<div className="w-96 p-8">
  Content
</div>

// ✅ GOOD: Responsive
<div className="w-full md:w-96 p-4 md:p-8">
  Content
</div>

// ❌ BAD: Desktop-first
<div className="lg:flex-row flex-col">
  Content
</div>

// ✅ GOOD: Mobile-first
<div className="flex-col lg:flex-row">
  Content
</div>
```

## Utility Function

```ts
// lib/utils.ts
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

// Usage: Merge classes safely
<div className={cn('bg-blue-500', className)}>
  Content
</div>
```

## Verification Before Production

- [ ] Tailwind configured with custom tokens
- [ ] Mobile-first responsive design
- [ ] Component variants defined with CVA
- [ ] Dark mode support implemented
- [ ] Forms accessible with labels
- [ ] Performance optimized (purge enabled)
- [ ] No inline styles (use Tailwind)
- [ ] Consistent spacing scale used
- [ ] Color contrast meets WCAG AA
- [ ] Custom utilities documented

## Integration with Project Standards

Enforces design consistency:
- U-1: WCAG 2.1 AA compliant (color contrast)
- Responsive design patterns
- Component reusability
- Performance optimization

## Resources

- Tailwind CSS Docs: https://tailwindcss.com/docs
- shadcn/ui: https://ui.shadcn.com
- CVA (Class Variance Authority): https://cva.style
