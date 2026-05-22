---
name: tailwind-components
description: Use when building reusable component patterns with Tailwind CSS. Covers component extraction, @apply directive, and composable design patterns.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# Tailwind CSS - Component Patterns

While Tailwind is utility-first, you'll often want to extract common patterns into reusable components. This skill covers strategies for building maintainable component architectures with Tailwind.

## Key Concepts

### Component Extraction Strategies

There are several approaches to creating reusable components with Tailwind:

1. **Template/Component Abstraction** (Recommended)
2. **CSS `@apply` Directive** (Use sparingly)
3. **JavaScript/TypeScript Component Classes**
4. **Tailwind Plugins**

### Template Component Abstraction

The most maintainable approach is to extract components at the template level:

```jsx
// Button.tsx
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'outline'
  size?: 'sm' | 'md' | 'lg'
  children: React.ReactNode
  onClick?: () => void
}

export function Button({
  variant = 'primary',
  size = 'md',
  children,
  onClick
}: ButtonProps) {
  const baseClasses = 'font-semibold rounded transition-colors focus:ring-2 focus:ring-offset-2'

  const variantClasses = {
    primary: 'bg-blue-500 hover:bg-blue-600 text-white focus:ring-blue-300',
    secondary: 'bg-gray-500 hover:bg-gray-600 text-white focus:ring-gray-300',
    outline: 'border-2 border-blue-500 text-blue-500 hover:bg-blue-50 focus:ring-blue-300',
  }

  const sizeClasses = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg',
  }

  return (
    <button
      className={`${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]}`}
      onClick={onClick}
    >
      {children}
    </button>
  )
}
```

## Best Practices

### 1. Use Class Variance Authority (CVA)

For complex component variants, use `cva` for better type safety:

```typescript
import { cva, type VariantProps } from 'class-variance-authority'

const button = cva(
  // Base classes
  'font-semibold rounded transition-colors focus:ring-2',
  {
    variants: {
      intent: {
        primary: 'bg-blue-500 hover:bg-blue-600 text-white',
        secondary: 'bg-gray-500 hover:bg-gray-600 text-white',
        danger: 'bg-red-500 hover:bg-red-600 text-white',
      },
      size: {
        small: 'text-sm px-3 py-1.5',
        medium: 'text-base px-4 py-2',
        large: 'text-lg px-6 py-3',
      },
      disabled: {
        true: 'opacity-50 cursor-not-allowed',
      },
    },
    compoundVariants: [
      {
        intent: 'primary',
        size: 'medium',
        className: 'uppercase',
      },
    ],
    defaultVariants: {
      intent: 'primary',
      size: 'medium',
    },
  }
)

interface ButtonProps extends VariantProps<typeof button> {
  children: React.ReactNode
}

export function Button({ intent, size, disabled, children }: ButtonProps) {
  return (
    <button className={button({ intent, size, disabled })}>
      {children}
    </button>
  )
}
```

### 2. Use clsx/cn for Conditional Classes

Combine multiple class strings efficiently:

```typescript
import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

// Usage
<div className={cn(
  'base-classes',
  isActive && 'active-classes',
  isDisabled && 'disabled-classes',
  className // Allow props override
)} />
```

### 3. Create Compound Components

Build flexible component APIs:

```tsx
// Card.tsx
interface CardProps {
  children: React.ReactNode
  className?: string
}

export function Card({ children, className }: CardProps) {
  return (
    <div className={cn(
      'bg-white rounded-lg shadow-md overflow-hidden',
      className
    )}>
      {children}
    </div>
  )
}

Card.Header = function CardHeader({ children, className }: CardProps) {
  return (
    <div className={cn('px-6 py-4 border-b border-gray-200', className)}>
      {children}
    </div>
  )
}

Card.Body = function CardBody({ children, className }: CardProps) {
  return (
    <div className={cn('px-6 py-4', className)}>
      {children}
    </div>
  )
}

Card.Footer = function CardFooter({ children, className }: CardProps) {
  return (
    <div className={cn('px-6 py-4 bg-gray-50 border-t border-gray-200', className)}>
      {children}
    </div>
  )
}

// Usage
<Card>
  <Card.Header>
    <h2 className="text-xl font-bold">Title</h2>
  </Card.Header>
  <Card.Body>
    <p>Content goes here</p>
  </Card.Body>
  <Card.Footer>
    <button>Action</button>
  </Card.Footer>
</Card>
```

### 4. Use @apply Sparingly

Only use `@apply` for truly reusable base styles:

```css
/* globals.css */
@layer components {
  .btn {
    @apply px-4 py-2 rounded font-semibold transition-colors;
  }

  .btn-primary {
    @apply bg-blue-500 hover:bg-blue-600 text-white;
  }

  .btn-secondary {
    @apply bg-gray-500 hover:bg-gray-600 text-white;
  }
}
```

**Note:** Prefer component abstraction over `@apply` to maintain Tailwind's utility-first benefits.

### 5. Design System Integration

Create a centralized design system:

```typescript
// design-system/index.ts
export const colors = {
  primary: 'blue-500',
  secondary: 'gray-500',
  success: 'green-500',
  danger: 'red-500',
  warning: 'yellow-500',
}

export const spacing = {
  xs: '1',
  sm: '2',
  md: '4',
  lg: '6',
  xl: '8',
}

export const typography = {
  heading: 'font-bold tracking-tight',
  body: 'font-normal leading-relaxed',
  caption: 'text-sm text-gray-600',
}

// Usage in components
import { colors, spacing } from '@/design-system'

<button className={`bg-${colors.primary} p-${spacing.md}`}>
  Click me
</button>
```

## Examples

### Form Input Component

```tsx
import { forwardRef } from 'react'
import { cn } from '@/lib/utils'

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string
  error?: string
  helperText?: string
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, helperText, className, ...props }, ref) => {
    return (
      <div className="w-full">
        {label && (
          <label className="block text-sm font-medium text-gray-700 mb-1">
            {label}
          </label>
        )}
        <input
          ref={ref}
          className={cn(
            'w-full px-3 py-2 border rounded-md',
            'focus:outline-none focus:ring-2 focus:ring-offset-0',
            'transition-colors',
            error
              ? 'border-red-500 focus:ring-red-300'
              : 'border-gray-300 focus:ring-blue-300',
            props.disabled && 'bg-gray-100 cursor-not-allowed',
            className
          )}
          {...props}
        />
        {error && (
          <p className="mt-1 text-sm text-red-600">{error}</p>
        )}
        {helperText && !error && (
          <p className="mt-1 text-sm text-gray-500">{helperText}</p>
        )}
      </div>
    )
  }
)

Input.displayName = 'Input'
```

### Modal Component

```tsx
import { useEffect } from 'react'
import { createPortal } from 'react-dom'
import { cn } from '@/lib/utils'

interface ModalProps {
  isOpen: boolean
  onClose: () => void
  children: React.ReactNode
  title?: string
  size?: 'sm' | 'md' | 'lg' | 'xl'
}

export function Modal({
  isOpen,
  onClose,
  children,
  title,
  size = 'md'
}: ModalProps) {
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden'
    } else {
      document.body.style.overflow = 'unset'
    }
    return () => {
      document.body.style.overflow = 'unset'
    }
  }, [isOpen])

  if (!isOpen) return null

  const sizeClasses = {
    sm: 'max-w-md',
    md: 'max-w-lg',
    lg: 'max-w-2xl',
    xl: 'max-w-4xl',
  }

  return createPortal(
    <div className="fixed inset-0 z-50 overflow-y-auto">
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-black bg-opacity-50 transition-opacity"
        onClick={onClose}
      />

      {/* Modal */}
      <div className="flex min-h-screen items-center justify-center p-4">
        <div
          className={cn(
            'relative bg-white rounded-lg shadow-xl',
            'w-full transform transition-all',
            sizeClasses[size]
          )}
        >
          {/* Header */}
          {title && (
            <div className="px-6 py-4 border-b border-gray-200">
              <h2 className="text-xl font-semibold">{title}</h2>
              <button
                onClick={onClose}
                className="absolute top-4 right-4 text-gray-400 hover:text-gray-600"
              >
                <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          )}

          {/* Content */}
          <div className="px-6 py-4">
            {children}
          </div>
        </div>
      </div>
    </div>,
    document.body
  )
}
```

### Dropdown Menu Component

```tsx
import { useState, useRef, useEffect } from 'react'
import { cn } from '@/lib/utils'

interface DropdownProps {
  trigger: React.ReactNode
  children: React.ReactNode
  align?: 'left' | 'right'
}

export function Dropdown({ trigger, children, align = 'left' }: DropdownProps) {
  const [isOpen, setIsOpen] = useState(false)
  const dropdownRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false)
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  return (
    <div className="relative inline-block" ref={dropdownRef}>
      <div onClick={() => setIsOpen(!isOpen)}>
        {trigger}
      </div>

      {isOpen && (
        <div className={cn(
          'absolute z-50 mt-2 w-56',
          'bg-white rounded-md shadow-lg',
          'border border-gray-200',
          'py-1',
          align === 'right' ? 'right-0' : 'left-0'
        )}>
          {children}
        </div>
      )}
    </div>
  )
}

Dropdown.Item = function DropdownItem({
  children,
  onClick
}: {
  children: React.ReactNode
  onClick?: () => void
}) {
  return (
    <button
      className={cn(
        'w-full text-left px-4 py-2',
        'hover:bg-gray-100',
        'transition-colors'
      )}
      onClick={onClick}
    >
      {children}
    </button>
  )
}
```

## Common Patterns

### Loading States

```tsx
export function LoadingButton({
  isLoading,
  children,
  ...props
}: ButtonProps & { isLoading?: boolean }) {
  return (
    <button
      className={cn(
        'relative',
        isLoading && 'cursor-not-allowed opacity-70'
      )}
      disabled={isLoading}
      {...props}
    >
      {isLoading && (
        <span className="absolute inset-0 flex items-center justify-center">
          <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
              fill="none"
            />
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            />
          </svg>
        </span>
      )}
      <span className={cn(isLoading && 'invisible')}>
        {children}
      </span>
    </button>
  )
}
```

### Badge Component

```tsx
const badge = cva(
  'inline-flex items-center rounded-full font-medium',
  {
    variants: {
      variant: {
        default: 'bg-gray-100 text-gray-800',
        primary: 'bg-blue-100 text-blue-800',
        success: 'bg-green-100 text-green-800',
        warning: 'bg-yellow-100 text-yellow-800',
        danger: 'bg-red-100 text-red-800',
      },
      size: {
        sm: 'px-2 py-0.5 text-xs',
        md: 'px-2.5 py-1 text-sm',
        lg: 'px-3 py-1.5 text-base',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'md',
    },
  }
)

export function Badge({ variant, size, children }: VariantProps<typeof badge> & { children: React.ReactNode }) {
  return (
    <span className={badge({ variant, size })}>
      {children}
    </span>
  )
}
```

## Anti-Patterns

### ❌ Don't Overuse @apply

```css
/* Bad: Recreating Bootstrap */
.btn {
  @apply px-4 py-2 rounded font-semibold transition-colors focus:ring-2;
}
.btn-primary {
  @apply bg-blue-500 hover:bg-blue-600 text-white focus:ring-blue-300;
}
.btn-secondary {
  @apply bg-gray-500 hover:bg-gray-600 text-white focus:ring-gray-300;
}
.btn-sm { @apply px-3 py-1 text-sm; }
.btn-lg { @apply px-6 py-3 text-lg; }

/* Good: Component abstraction instead */
```

### ❌ Don't Create Overly Generic Components

```tsx
// Bad: Too flexible, loses Tailwind benefits
<Box padding="4" margin="2" bg="blue" />

// Good: Semantic components
<Card className="p-4 m-2 bg-blue-500" />
```

### ❌ Don't Ignore Prop Overrides

```tsx
// Bad: Can't override styles
export function Button({ children }: { children: React.ReactNode }) {
  return <button className="bg-blue-500 px-4 py-2">{children}</button>
}

// Good: Accept className prop
export function Button({ children, className }: { children: React.ReactNode; className?: string }) {
  return (
    <button className={cn('bg-blue-500 px-4 py-2', className)}>
      {children}
    </button>
  )
}
```

## Related Skills

- **tailwind-utility-classes**: Using Tailwind's utility classes effectively
- **tailwind-configuration**: Customizing Tailwind config and theme
- **tailwind-responsive-design**: Building responsive component patterns
