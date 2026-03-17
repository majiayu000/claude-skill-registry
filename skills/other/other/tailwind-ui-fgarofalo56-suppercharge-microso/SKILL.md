---
name: tailwind-ui
description: Master Tailwind CSS for modern, responsive UI styling. Covers utility-first patterns, responsive design, dark mode, custom themes, animations, and component libraries like shadcn/ui and Headless UI. Use for styling React apps, building design systems, and rapid UI development.
---

# Tailwind CSS UI Development

Build beautiful, responsive interfaces using Tailwind CSS utility-first approach.

## Instructions

1. **Use utility classes directly** - Avoid custom CSS when Tailwind utilities exist
2. **Mobile-first approach** - Start with base styles, add responsive modifiers
3. **Extract components** - When patterns repeat 3+ times, create a component
4. **Use design tokens** - Leverage Tailwind's spacing, color, and typography scales
5. **Implement dark mode** - Use `dark:` variant for theme support

## Core Patterns

### Responsive Design

```tsx
// Mobile-first: base → sm → md → lg → xl → 2xl
<div className="
  w-full              // Mobile: full width
  sm:w-1/2            // 640px+: half width
  md:w-1/3            // 768px+: third width
  lg:w-1/4            // 1024px+: quarter width
  p-4 sm:p-6 lg:p-8   // Responsive padding
">
  Content
</div>
```

### Dark Mode

```tsx
<div className="
  bg-white dark:bg-gray-900
  text-gray-900 dark:text-gray-100
  border border-gray-200 dark:border-gray-700
">
  <h2 className="text-gray-800 dark:text-gray-200">
    Title
  </h2>
</div>
```

### Flexbox & Grid Layouts

```tsx
// Flexbox
<div className="flex items-center justify-between gap-4">
  <div className="flex-1">Content</div>
  <div className="flex-shrink-0">Fixed</div>
</div>

// Grid
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  <div>Card 1</div>
  <div>Card 2</div>
  <div>Card 3</div>
</div>

// Auto-fit grid
<div className="grid grid-cols-[repeat(auto-fit,minmax(300px,1fr))] gap-4">
  {items.map(item => <Card key={item.id} {...item} />)}
</div>
```

## Component Examples

### Button Variants

```tsx
const buttonVariants = {
  primary: "bg-blue-600 hover:bg-blue-700 text-white",
  secondary: "bg-gray-200 hover:bg-gray-300 text-gray-900 dark:bg-gray-700 dark:text-gray-100",
  danger: "bg-red-600 hover:bg-red-700 text-white",
  ghost: "hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-700 dark:text-gray-300",
  outline: "border-2 border-gray-300 hover:border-gray-400 text-gray-700",
};

const buttonSizes = {
  sm: "px-3 py-1.5 text-sm",
  md: "px-4 py-2 text-base",
  lg: "px-6 py-3 text-lg",
};

interface ButtonProps {
  variant?: keyof typeof buttonVariants;
  size?: keyof typeof buttonSizes;
  children: React.ReactNode;
}

export function Button({ variant = 'primary', size = 'md', children }: ButtonProps) {
  return (
    <button className={`
      ${buttonVariants[variant]}
      ${buttonSizes[size]}
      inline-flex items-center justify-center
      font-medium rounded-lg
      transition-colors duration-200
      focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500
      disabled:opacity-50 disabled:cursor-not-allowed
    `}>
      {children}
    </button>
  );
}
```

### Card Component

```tsx
export function Card({ children, className = '' }: { children: React.ReactNode; className?: string }) {
  return (
    <div className={`
      bg-white dark:bg-gray-800
      rounded-xl shadow-sm
      border border-gray-200 dark:border-gray-700
      overflow-hidden
      ${className}
    `}>
      {children}
    </div>
  );
}

Card.Header = ({ children }: { children: React.ReactNode }) => (
  <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
    {children}
  </div>
);

Card.Body = ({ children }: { children: React.ReactNode }) => (
  <div className="px-6 py-4">{children}</div>
);

Card.Footer = ({ children }: { children: React.ReactNode }) => (
  <div className="px-6 py-4 bg-gray-50 dark:bg-gray-900/50 border-t border-gray-200 dark:border-gray-700">
    {children}
  </div>
);
```

### Input with Label

```tsx
interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label: string;
  error?: string;
  hint?: string;
}

export function Input({ label, error, hint, id, ...props }: InputProps) {
  const inputId = id || label.toLowerCase().replace(/\s+/g, '-');

  return (
    <div className="space-y-1">
      <label
        htmlFor={inputId}
        className="block text-sm font-medium text-gray-700 dark:text-gray-300"
      >
        {label}
      </label>
      <input
        id={inputId}
        className={`
          w-full px-3 py-2 rounded-lg
          border transition-colors duration-200
          ${error
            ? 'border-red-500 focus:ring-red-500'
            : 'border-gray-300 dark:border-gray-600 focus:ring-blue-500'
          }
          bg-white dark:bg-gray-800
          text-gray-900 dark:text-gray-100
          placeholder-gray-400 dark:placeholder-gray-500
          focus:outline-none focus:ring-2 focus:ring-offset-0
          disabled:bg-gray-100 disabled:cursor-not-allowed
        `}
        aria-invalid={!!error}
        aria-describedby={error ? `${inputId}-error` : hint ? `${inputId}-hint` : undefined}
        {...props}
      />
      {hint && !error && (
        <p id={`${inputId}-hint`} className="text-sm text-gray-500 dark:text-gray-400">
          {hint}
        </p>
      )}
      {error && (
        <p id={`${inputId}-error`} className="text-sm text-red-600 dark:text-red-400" role="alert">
          {error}
        </p>
      )}
    </div>
  );
}
```

## Tailwind Configuration

### Custom Theme

```js
// tailwind.config.js
/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#eff6ff',
          100: '#dbeafe',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
      },
      animation: {
        'fade-in': 'fadeIn 0.3s ease-out',
        'slide-up': 'slideUp 0.3s ease-out',
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
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
};
```

## shadcn/ui Integration

```bash
# Initialize shadcn/ui
npx shadcn@latest init

# Add components
npx shadcn@latest add button card input dialog
```

```tsx
// Using shadcn/ui components
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";

function Dashboard() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Analytics</CardTitle>
      </CardHeader>
      <CardContent>
        <Button variant="outline">View Details</Button>
      </CardContent>
    </Card>
  );
}
```

## Best Practices

1. **Use `cn()` utility** - Merge class names conditionally with clsx/tailwind-merge
2. **Group related utilities** - Keep layout, spacing, colors together
3. **Avoid arbitrary values** - Use theme tokens when possible
4. **Use CSS variables for themes** - Dynamic theming with HSL colors
5. **Purge unused styles** - Configure content paths correctly

## When to Use

- Styling React/Vue/Svelte applications
- Building component libraries
- Rapid prototyping
- Design system implementation
- Responsive web design

## Notes

- Requires PostCSS configuration
- Use Tailwind CSS IntelliSense VS Code extension
- Consider class variance authority (CVA) for complex variants
- Pair with Headless UI for accessible components
