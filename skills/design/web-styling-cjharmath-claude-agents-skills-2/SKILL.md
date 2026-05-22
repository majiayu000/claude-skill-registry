---
name: web-styling
description: Styling patterns for React web applications. Use when working with Tailwind CSS, CSS Modules, theming, responsive design, or component styling.
---

# Web Styling (React)

## Tailwind CSS

### Basic Usage

```typescript
function Button({ variant = 'primary', children }) {
  const baseClasses = 'px-4 py-2 rounded-lg font-medium transition-colors';

  const variants = {
    primary: 'bg-blue-600 text-white hover:bg-blue-700',
    secondary: 'bg-gray-200 text-gray-800 hover:bg-gray-300',
    danger: 'bg-red-600 text-white hover:bg-red-700',
  };

  return (
    <button className={`${baseClasses} ${variants[variant]}`}>
      {children}
    </button>
  );
}
```

### Conditional Classes with clsx/cn

```typescript
import { clsx } from 'clsx';
// or with tailwind-merge for deduplication
import { twMerge } from 'tailwind-merge';

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

function Card({ isActive, isDisabled, className, children }) {
  return (
    <div
      className={cn(
        'p-4 rounded-lg border',
        isActive && 'border-blue-500 bg-blue-50',
        isDisabled && 'opacity-50 cursor-not-allowed',
        className // Allow overrides
      )}
    >
      {children}
    </div>
  );
}
```

### Responsive Design

```typescript
// Mobile-first breakpoints
// sm: 640px, md: 768px, lg: 1024px, xl: 1280px, 2xl: 1536px

<div className="
  grid
  grid-cols-1      /* Mobile: 1 column */
  sm:grid-cols-2   /* Tablet: 2 columns */
  lg:grid-cols-3   /* Desktop: 3 columns */
  xl:grid-cols-4   /* Large: 4 columns */
  gap-4
">
  {items.map(item => <Card key={item.id} {...item} />)}
</div>

// Responsive text
<h1 className="text-2xl md:text-3xl lg:text-4xl font-bold">
  Title
</h1>

// Hide/show at breakpoints
<nav className="hidden md:flex">Desktop Nav</nav>
<nav className="flex md:hidden">Mobile Nav</nav>
```

### Dark Mode

```typescript
// tailwind.config.js
module.exports = {
  darkMode: 'class', // or 'media' for OS preference
  // ...
};

// Component
<div className="bg-white dark:bg-gray-900 text-gray-900 dark:text-white">
  <h1 className="text-black dark:text-white">Title</h1>
  <p className="text-gray-600 dark:text-gray-400">Description</p>
</div>

// Toggle dark mode
function ThemeToggle() {
  const [isDark, setIsDark] = useState(false);

  useEffect(() => {
    document.documentElement.classList.toggle('dark', isDark);
  }, [isDark]);

  return (
    <button onClick={() => setIsDark(!isDark)}>
      {isDark ? '☀️' : '🌙'}
    </button>
  );
}
```

### Custom Design Tokens

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          500: '#0ea5e9',
          600: '#0284c7',
          700: '#0369a1',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
      },
    },
  },
};
```

```typescript
// Usage
<button className="bg-brand-500 hover:bg-brand-600">
  Brand Button
</button>
```

---

## CSS Modules

### Basic Usage

```css
/* Button.module.css */
.button {
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  font-weight: 500;
}

.primary {
  background-color: #3b82f6;
  color: white;
}

.secondary {
  background-color: #e5e7eb;
  color: #1f2937;
}
```

```typescript
// Button.tsx
import styles from './Button.module.css';

function Button({ variant = 'primary', children }) {
  return (
    <button className={`${styles.button} ${styles[variant]}`}>
      {children}
    </button>
  );
}
```

### With clsx

```typescript
import styles from './Card.module.css';
import { clsx } from 'clsx';

function Card({ isActive, className, children }) {
  return (
    <div
      className={clsx(
        styles.card,
        isActive && styles.active,
        className
      )}
    >
      {children}
    </div>
  );
}
```

---

## CSS-in-JS (styled-components)

```typescript
import styled from 'styled-components';

const Button = styled.button<{ variant?: 'primary' | 'secondary' }>`
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  font-weight: 500;
  transition: background-color 0.2s;

  ${({ variant = 'primary' }) =>
    variant === 'primary'
      ? `
        background-color: #3b82f6;
        color: white;
        &:hover {
          background-color: #2563eb;
        }
      `
      : `
        background-color: #e5e7eb;
        color: #1f2937;
        &:hover {
          background-color: #d1d5db;
        }
      `}
`;

// With theme
import { ThemeProvider } from 'styled-components';

const theme = {
  colors: {
    primary: '#3b82f6',
    secondary: '#e5e7eb',
  },
  spacing: {
    sm: '0.5rem',
    md: '1rem',
  },
};

const ThemedButton = styled.button`
  background-color: ${({ theme }) => theme.colors.primary};
  padding: ${({ theme }) => theme.spacing.md};
`;
```

---

## Component Variants Pattern

```typescript
// Using cva (class-variance-authority) with Tailwind
import { cva, type VariantProps } from 'class-variance-authority';

const buttonVariants = cva(
  'inline-flex items-center justify-center rounded-md font-medium transition-colors',
  {
    variants: {
      variant: {
        primary: 'bg-blue-600 text-white hover:bg-blue-700',
        secondary: 'bg-gray-100 text-gray-900 hover:bg-gray-200',
        outline: 'border border-gray-300 hover:bg-gray-50',
        ghost: 'hover:bg-gray-100',
        danger: 'bg-red-600 text-white hover:bg-red-700',
      },
      size: {
        sm: 'h-8 px-3 text-sm',
        md: 'h-10 px-4',
        lg: 'h-12 px-6 text-lg',
      },
    },
    defaultVariants: {
      variant: 'primary',
      size: 'md',
    },
  }
);

interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {}

function Button({ variant, size, className, ...props }: ButtonProps) {
  return (
    <button
      className={cn(buttonVariants({ variant, size }), className)}
      {...props}
    />
  );
}

// Usage
<Button variant="primary" size="lg">Large Primary</Button>
<Button variant="outline">Outline</Button>
```

---

## Animation Patterns

### Tailwind Animations

```typescript
// Built-in animations
<div className="animate-spin">Loading...</div>
<div className="animate-pulse">Loading...</div>
<div className="animate-bounce">Scroll down</div>

// Transitions
<button className="transition-all duration-200 hover:scale-105">
  Hover me
</button>

// Custom animation in tailwind.config.js
module.exports = {
  theme: {
    extend: {
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
};

// Usage
<div className="animate-fade-in">Fading in...</div>
```

### Framer Motion

```typescript
import { motion, AnimatePresence } from 'framer-motion';

function Modal({ isOpen, onClose, children }) {
  return (
    <AnimatePresence>
      {isOpen && (
        <>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/50"
            onClick={onClose}
          />
          <motion.div
            initial={{ opacity: 0, scale: 0.95, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 20 }}
            className="fixed inset-x-4 top-1/2 -translate-y-1/2 bg-white rounded-lg p-6"
          >
            {children}
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}
```

---

## Layout Patterns

### Flexbox

```typescript
// Centering
<div className="flex items-center justify-center min-h-screen">
  <Card>Centered content</Card>
</div>

// Space between
<div className="flex items-center justify-between">
  <Logo />
  <Navigation />
  <UserMenu />
</div>

// Responsive direction
<div className="flex flex-col md:flex-row gap-4">
  <Sidebar />
  <Main />
</div>
```

### Grid

```typescript
// Equal columns
<div className="grid grid-cols-3 gap-4">
  {items.map(item => <Card key={item.id} {...item} />)}
</div>

// Complex layout
<div className="grid grid-cols-12 gap-4">
  <aside className="col-span-3">Sidebar</aside>
  <main className="col-span-6">Main content</main>
  <aside className="col-span-3">Right sidebar</aside>
</div>

// Auto-fit for unknown count
<div className="grid grid-cols-[repeat(auto-fit,minmax(250px,1fr))] gap-4">
  {items.map(item => <Card key={item.id} {...item} />)}
</div>
```

### Container

```typescript
// Centered container with max-width
<div className="container mx-auto px-4">
  <Content />
</div>

// Or with custom max-width
<div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
  <Content />
</div>
```

---

## Theming System

```typescript
// theme.ts
export const theme = {
  colors: {
    primary: {
      50: '#eff6ff',
      500: '#3b82f6',
      600: '#2563eb',
      700: '#1d4ed8',
    },
    gray: {
      50: '#f9fafb',
      100: '#f3f4f6',
      900: '#111827',
    },
  },
  spacing: {
    xs: '0.25rem',
    sm: '0.5rem',
    md: '1rem',
    lg: '1.5rem',
    xl: '2rem',
  },
} as const;

// CSS Variables approach
:root {
  --color-primary: #3b82f6;
  --color-background: #ffffff;
  --color-text: #111827;
}

.dark {
  --color-primary: #60a5fa;
  --color-background: #111827;
  --color-text: #f9fafb;
}

// Usage with Tailwind
<div className="bg-[var(--color-background)] text-[var(--color-text)]">
  Content
</div>
```

---

## Common Issues

| Issue | Solution |
|-------|----------|
| Styles not applying | Check class specificity, Tailwind purging |
| Dark mode flicker | Use CSS variables or SSR-safe approach |
| Layout shift | Set explicit dimensions, use skeleton loaders |
| Mobile overflow | Add `overflow-x-hidden` to body |
| Z-index conflicts | Use consistent z-index scale |

---

## File Structure

```
styles/
  globals.css          # Global styles, Tailwind imports
  variables.css        # CSS custom properties
components/
  Button/
    Button.tsx
    Button.module.css  # If using CSS Modules
    index.ts
tailwind.config.js     # Tailwind configuration
```
