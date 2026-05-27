---
description: "UI component patterns with style-specific implementations and accessibility"
triggers:
  - component
  - button
  - card
  - modal
  - form
  - input
  - navigation
  - layout
  - grid
globs:
  - "components/**"
  - "*.tsx"
  - "*.jsx"
---

# Component Patterns Skill

UI component patterns with style-specific implementations and accessibility.

## Overview

This skill provides comprehensive component patterns with multiple design style implementations, accessibility features, and best practices for modern frontend development.

## Component Library Structure

```
components/
├── atoms/
│   ├── Button/
│   │   ├── Button.tsx
│   │   ├── Button.styles.ts
│   │   ├── Button.test.tsx
│   │   └── index.ts
│   ├── Input/
│   ├── Icon/
│   └── Badge/
├── molecules/
│   ├── FormField/
│   ├── Card/
│   ├── SearchBar/
│   └── MenuItem/
├── organisms/
│   ├── Navigation/
│   ├── Modal/
│   ├── Form/
│   └── DataTable/
├── templates/
│   ├── DashboardLayout/
│   ├── AuthLayout/
│   └── ContentLayout/
└── pages/
    ├── Dashboard/
    ├── Login/
    └── Profile/
```

## Button Variants by Design Style

### Base Button Component

**components/atoms/Button/Button.tsx:**
```typescript
import React, { ButtonHTMLAttributes, forwardRef } from 'react';
import { VariantProps } from 'class-variance-authority';
import { buttonVariants } from './Button.styles';

export interface ButtonProps
  extends ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  loading?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      className,
      variant,
      size,
      styleType,
      loading,
      leftIcon,
      rightIcon,
      children,
      disabled,
      ...props
    },
    ref
  ) => {
    return (
      <button
        ref={ref}
        className={buttonVariants({ variant, size, styleType, className })}
        disabled={disabled || loading}
        aria-busy={loading}
        {...props}
      >
        {loading && (
          <span className="button-spinner" role="status" aria-label="Loading">
            <span className="sr-only">Loading...</span>
          </span>
        )}
        {!loading && leftIcon && <span className="button-icon-left">{leftIcon}</span>}
        <span className="button-content">{children}</span>
        {!loading && rightIcon && <span className="button-icon-right">{rightIcon}</span>}
      </button>
    );
  }
);

Button.displayName = 'Button';
```

### Button Styles (Tailwind + CVA)

**components/atoms/Button/Button.styles.ts:**
```typescript
import { cva } from 'class-variance-authority';

export const buttonVariants = cva(
  'inline-flex items-center justify-center font-medium transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50',
  {
    variants: {
      variant: {
        primary: '',
        secondary: '',
        outline: '',
        ghost: '',
        danger: '',
      },
      size: {
        sm: 'h-9 px-3 text-sm',
        md: 'h-10 px-4 text-base',
        lg: 'h-11 px-6 text-lg',
        xl: 'h-12 px-8 text-xl',
      },
      styleType: {
        default: '',
        glassmorphism: '',
        neumorphism: '',
        brutalist: '',
        'neo-brutalist': '',
      },
    },
    compoundVariants: [
      // Default Style
      {
        variant: 'primary',
        styleType: 'default',
        class: 'bg-primary-500 text-white hover:bg-primary-600 shadow-sm',
      },
      {
        variant: 'secondary',
        styleType: 'default',
        class: 'bg-secondary-500 text-white hover:bg-secondary-600 shadow-sm',
      },
      {
        variant: 'outline',
        styleType: 'default',
        class: 'border-2 border-primary-500 text-primary-500 hover:bg-primary-50',
      },
      {
        variant: 'ghost',
        styleType: 'default',
        class: 'text-primary-500 hover:bg-primary-50',
      },

      // Glassmorphism Style
      {
        variant: 'primary',
        styleType: 'glassmorphism',
        class: 'bg-white/10 backdrop-blur-md border border-white/20 text-white hover:bg-white/20 shadow-glass',
      },
      {
        variant: 'secondary',
        styleType: 'glassmorphism',
        class: 'bg-black/10 backdrop-blur-md border border-black/20 hover:bg-black/20 shadow-glass',
      },

      // Neumorphism Style
      {
        variant: 'primary',
        styleType: 'neumorphism',
        class: 'bg-neutral-200 text-neutral-800 shadow-neumorphic hover:shadow-neumorphic-hover active:shadow-neumorphic-inset',
      },
      {
        variant: 'secondary',
        styleType: 'neumorphism',
        class: 'bg-neutral-300 text-neutral-800 shadow-neumorphic-sm hover:shadow-neumorphic',
      },

      // Brutalist Style
      {
        variant: 'primary',
        styleType: 'brutalist',
        class: 'bg-black text-white border-4 border-black font-bold uppercase tracking-wider',
      },
      {
        variant: 'secondary',
        styleType: 'brutalist',
        class: 'bg-white text-black border-4 border-black font-bold uppercase tracking-wider',
      },

      // Neo-Brutalist Style
      {
        variant: 'primary',
        styleType: 'neo-brutalist',
        class: 'bg-yellow-400 text-black border-4 border-black shadow-brutalist hover:translate-x-1 hover:translate-y-1 hover:shadow-none font-bold',
      },
      {
        variant: 'secondary',
        styleType: 'neo-brutalist',
        class: 'bg-cyan-400 text-black border-4 border-black shadow-brutalist hover:translate-x-1 hover:translate-y-1 hover:shadow-none font-bold',
      },
      {
        variant: 'danger',
        styleType: 'neo-brutalist',
        class: 'bg-red-500 text-white border-4 border-black shadow-brutalist hover:translate-x-1 hover:translate-y-1 hover:shadow-none font-bold',
      },
    ],
    defaultVariants: {
      variant: 'primary',
      size: 'md',
      styleType: 'default',
    },
  }
);
```

### Usage Examples

```tsx
// Default style
<Button variant="primary" size="md">
  Click Me
</Button>

// Glassmorphism style
<Button variant="primary" size="lg" styleType="glassmorphism">
  Frosted Glass
</Button>

// Neo-brutalist style with icon
<Button
  variant="primary"
  size="md"
  styleType="neo-brutalist"
  leftIcon={<IconPlus />}
>
  Add Item
</Button>

// Loading state
<Button variant="primary" loading>
  Processing...
</Button>

// Disabled state
<Button variant="primary" disabled>
  Disabled
</Button>
```

## Card Patterns

### Base Card Component

**components/molecules/Card/Card.tsx:**
```typescript
import React, { HTMLAttributes, forwardRef } from 'react';
import { VariantProps } from 'class-variance-authority';
import { cardVariants } from './Card.styles';

export interface CardProps
  extends HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof cardVariants> {
  header?: React.ReactNode;
  footer?: React.ReactNode;
  hoverable?: boolean;
  clickable?: boolean;
}

export const Card = forwardRef<HTMLDivElement, CardProps>(
  (
    {
      className,
      variant,
      styleType,
      header,
      footer,
      hoverable,
      clickable,
      children,
      onClick,
      ...props
    },
    ref
  ) => {
    return (
      <div
        ref={ref}
        className={cardVariants({
          variant,
          styleType,
          hoverable,
          clickable,
          className,
        })}
        onClick={onClick}
        role={clickable ? 'button' : undefined}
        tabIndex={clickable ? 0 : undefined}
        {...props}
      >
        {header && (
          <div className="card-header" role="heading" aria-level={2}>
            {header}
          </div>
        )}
        <div className="card-body">{children}</div>
        {footer && <div className="card-footer">{footer}</div>}
      </div>
    );
  }
);

Card.displayName = 'Card';
```

### Card Styles

**components/molecules/Card/Card.styles.ts:**
```typescript
import { cva } from 'class-variance-authority';

export const cardVariants = cva(
  'rounded-lg overflow-hidden transition-all',
  {
    variants: {
      variant: {
        default: '',
        elevated: '',
        outlined: '',
      },
      styleType: {
        default: '',
        glassmorphism: '',
        neumorphism: '',
        neubrutalism: '',
        minimalist: '',
      },
      hoverable: {
        true: 'hover:scale-105 cursor-pointer',
        false: '',
      },
      clickable: {
        true: 'cursor-pointer focus-visible:ring-2 focus-visible:ring-primary-500',
        false: '',
      },
    },
    compoundVariants: [
      // Default Style
      {
        variant: 'default',
        styleType: 'default',
        class: 'bg-white shadow-md',
      },
      {
        variant: 'elevated',
        styleType: 'default',
        class: 'bg-white shadow-lg hover:shadow-xl',
      },
      {
        variant: 'outlined',
        styleType: 'default',
        class: 'bg-white border-2 border-neutral-200',
      },

      // Glassmorphism Style
      {
        variant: 'default',
        styleType: 'glassmorphism',
        class: 'bg-white/10 backdrop-blur-lg border border-white/20 shadow-glass',
      },
      {
        variant: 'elevated',
        styleType: 'glassmorphism',
        class: 'bg-white/20 backdrop-blur-xl border border-white/30 shadow-glass-lg',
      },

      // Neumorphism Style
      {
        variant: 'default',
        styleType: 'neumorphism',
        class: 'bg-neutral-200 shadow-neumorphic',
      },
      {
        variant: 'elevated',
        styleType: 'neumorphism',
        class: 'bg-neutral-200 shadow-neumorphic-lg',
      },

      // Neubrutalism Style
      {
        variant: 'default',
        styleType: 'neubrutalism',
        class: 'bg-white border-4 border-black shadow-brutalist',
      },
      {
        variant: 'elevated',
        styleType: 'neubrutalism',
        class: 'bg-yellow-200 border-4 border-black shadow-brutalist-lg',
      },

      // Minimalist Style
      {
        variant: 'default',
        styleType: 'minimalist',
        class: 'bg-white border border-neutral-100',
      },
      {
        variant: 'elevated',
        styleType: 'minimalist',
        class: 'bg-white shadow-sm',
      },
    ],
    defaultVariants: {
      variant: 'default',
      styleType: 'default',
      hoverable: false,
      clickable: false,
    },
  }
);
```

## Form Components with Validation Styling

### Input Component

**components/atoms/Input/Input.tsx:**
```typescript
import React, { InputHTMLAttributes, forwardRef } from 'react';
import { VariantProps } from 'class-variance-authority';
import { inputVariants } from './Input.styles';

export interface InputProps
  extends InputHTMLAttributes<HTMLInputElement>,
    VariantProps<typeof inputVariants> {
  label?: string;
  error?: string;
  helperText?: string;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  (
    {
      className,
      variant,
      size,
      styleType,
      label,
      error,
      helperText,
      leftIcon,
      rightIcon,
      id,
      ...props
    },
    ref
  ) => {
    const inputId = id || `input-${Math.random().toString(36).substr(2, 9)}`;
    const errorId = error ? `${inputId}-error` : undefined;
    const helperId = helperText ? `${inputId}-helper` : undefined;

    return (
      <div className="input-wrapper">
        {label && (
          <label htmlFor={inputId} className="input-label">
            {label}
            {props.required && <span className="text-error-500 ml-1">*</span>}
          </label>
        )}

        <div className="input-container relative">
          {leftIcon && (
            <div className="input-icon-left absolute left-3 top-1/2 -translate-y-1/2">
              {leftIcon}
            </div>
          )}

          <input
            ref={ref}
            id={inputId}
            className={inputVariants({
              variant,
              size,
              styleType,
              hasLeftIcon: !!leftIcon,
              hasRightIcon: !!rightIcon,
              hasError: !!error,
              className,
            })}
            aria-invalid={!!error}
            aria-describedby={[errorId, helperId].filter(Boolean).join(' ') || undefined}
            {...props}
          />

          {rightIcon && (
            <div className="input-icon-right absolute right-3 top-1/2 -translate-y-1/2">
              {rightIcon}
            </div>
          )}
        </div>

        {error && (
          <p id={errorId} className="input-error text-error-500 text-sm mt-1" role="alert">
            {error}
          </p>
        )}

        {helperText && !error && (
          <p id={helperId} className="input-helper text-neutral-500 text-sm mt-1">
            {helperText}
          </p>
        )}
      </div>
    );
  }
);

Input.displayName = 'Input';
```

### Input Styles

**components/atoms/Input/Input.styles.ts:**
```typescript
import { cva } from 'class-variance-authority';

export const inputVariants = cva(
  'w-full transition-all focus-visible:outline-none disabled:cursor-not-allowed disabled:opacity-50',
  {
    variants: {
      variant: {
        default: '',
        filled: '',
        outlined: '',
      },
      size: {
        sm: 'h-9 text-sm',
        md: 'h-10 text-base',
        lg: 'h-11 text-lg',
      },
      styleType: {
        default: '',
        glassmorphism: '',
        neumorphism: '',
        brutalist: '',
        minimalist: '',
      },
      hasLeftIcon: {
        true: 'pl-10',
        false: 'pl-3',
      },
      hasRightIcon: {
        true: 'pr-10',
        false: 'pr-3',
      },
      hasError: {
        true: '',
        false: '',
      },
    },
    compoundVariants: [
      // Default Style
      {
        variant: 'default',
        styleType: 'default',
        hasError: false,
        class: 'bg-white border border-neutral-300 rounded-md focus:border-primary-500 focus:ring-2 focus:ring-primary-500/20',
      },
      {
        variant: 'default',
        styleType: 'default',
        hasError: true,
        class: 'bg-white border-2 border-error-500 rounded-md focus:border-error-600 focus:ring-2 focus:ring-error-500/20',
      },
      {
        variant: 'filled',
        styleType: 'default',
        hasError: false,
        class: 'bg-neutral-100 border-transparent rounded-md focus:bg-white focus:border-primary-500 focus:ring-2 focus:ring-primary-500/20',
      },
      {
        variant: 'outlined',
        styleType: 'default',
        hasError: false,
        class: 'bg-transparent border-2 border-neutral-300 rounded-md focus:border-primary-500',
      },

      // Glassmorphism Style
      {
        variant: 'default',
        styleType: 'glassmorphism',
        class: 'bg-white/10 backdrop-blur-md border border-white/20 rounded-lg text-white placeholder:text-white/50 focus:bg-white/20 focus:border-white/40',
      },

      // Neumorphism Style
      {
        variant: 'default',
        styleType: 'neumorphism',
        class: 'bg-neutral-200 border-none rounded-lg shadow-neumorphic-inset focus:shadow-neumorphic-inset-deep',
      },

      // Brutalist Style
      {
        variant: 'default',
        styleType: 'brutalist',
        class: 'bg-white border-4 border-black rounded-none font-mono focus:border-black focus:shadow-brutalist',
      },

      // Minimalist Style
      {
        variant: 'default',
        styleType: 'minimalist',
        class: 'bg-white border-b-2 border-neutral-200 rounded-none focus:border-primary-500',
      },
    ],
    defaultVariants: {
      variant: 'default',
      size: 'md',
      styleType: 'default',
      hasLeftIcon: false,
      hasRightIcon: false,
      hasError: false,
    },
  }
);
```

## Navigation Patterns

### Navbar Component

**components/organisms/Navigation/Navbar.tsx:**
```typescript
import React from 'react';
import Link from 'next/link';

export interface NavItem {
  label: string;
  href: string;
  icon?: React.ReactNode;
  badge?: string | number;
  children?: NavItem[];
}

export interface NavbarProps {
  logo: React.ReactNode;
  items: NavItem[];
  actions?: React.ReactNode;
  styleType?: 'default' | 'glassmorphism' | 'minimalist' | 'brutalist';
}

export function Navbar({ logo, items, actions, styleType = 'default' }: NavbarProps) {
  const navClasses = {
    default: 'bg-white shadow-md border-b border-neutral-200',
    glassmorphism: 'bg-white/10 backdrop-blur-lg border-b border-white/20',
    minimalist: 'bg-white border-b border-neutral-100',
    brutalist: 'bg-black border-b-4 border-black',
  };

  return (
    <nav className={`h-16 ${navClasses[styleType]}`} role="navigation">
      <div className="container mx-auto h-full flex items-center justify-between px-4">
        <div className="flex items-center gap-8">
          <div className="navbar-logo">{logo}</div>

          <ul className="hidden md:flex items-center gap-6" role="menubar">
            {items.map((item, index) => (
              <li key={index} role="none">
                <Link
                  href={item.href}
                  className="nav-item flex items-center gap-2 text-neutral-700 hover:text-primary-500 transition-colors"
                  role="menuitem"
                >
                  {item.icon}
                  <span>{item.label}</span>
                  {item.badge && (
                    <span className="badge bg-primary-500 text-white text-xs px-2 py-0.5 rounded-full">
                      {item.badge}
                    </span>
                  )}
                </Link>
              </li>
            ))}
          </ul>
        </div>

        {actions && <div className="navbar-actions">{actions}</div>}
      </div>
    </nav>
  );
}
```

## Layout Systems

### Grid Layout

**components/templates/GridLayout.tsx:**
```typescript
import React, { HTMLAttributes } from 'react';
import { VariantProps, cva } from 'class-variance-authority';

const gridVariants = cva('grid gap-4', {
  variants: {
    cols: {
      1: 'grid-cols-1',
      2: 'grid-cols-1 md:grid-cols-2',
      3: 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3',
      4: 'grid-cols-1 md:grid-cols-2 lg:grid-cols-4',
      6: 'grid-cols-2 md:grid-cols-3 lg:grid-cols-6',
      12: 'grid-cols-12',
    },
    gap: {
      none: 'gap-0',
      sm: 'gap-2',
      md: 'gap-4',
      lg: 'gap-6',
      xl: 'gap-8',
    },
    responsive: {
      true: '',
      false: '',
    },
  },
  defaultVariants: {
    cols: 3,
    gap: 'md',
    responsive: true,
  },
});

export interface GridLayoutProps
  extends HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof gridVariants> {}

export function GridLayout({ className, cols, gap, responsive, children, ...props }: GridLayoutProps) {
  return (
    <div className={gridVariants({ cols, gap, responsive, className })} {...props}>
      {children}
    </div>
  );
}
```

### Flexbox Layout

**components/templates/FlexLayout.tsx:**
```typescript
import React, { HTMLAttributes } from 'react';
import { VariantProps, cva } from 'class-variance-authority';

const flexVariants = cva('flex', {
  variants: {
    direction: {
      row: 'flex-row',
      col: 'flex-col',
      'row-reverse': 'flex-row-reverse',
      'col-reverse': 'flex-col-reverse',
    },
    justify: {
      start: 'justify-start',
      end: 'justify-end',
      center: 'justify-center',
      between: 'justify-between',
      around: 'justify-around',
      evenly: 'justify-evenly',
    },
    align: {
      start: 'items-start',
      end: 'items-end',
      center: 'items-center',
      baseline: 'items-baseline',
      stretch: 'items-stretch',
    },
    gap: {
      none: 'gap-0',
      sm: 'gap-2',
      md: 'gap-4',
      lg: 'gap-6',
      xl: 'gap-8',
    },
    wrap: {
      true: 'flex-wrap',
      false: 'flex-nowrap',
    },
  },
  defaultVariants: {
    direction: 'row',
    justify: 'start',
    align: 'start',
    gap: 'md',
    wrap: false,
  },
});

export interface FlexLayoutProps
  extends HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof flexVariants> {}

export function FlexLayout({
  className,
  direction,
  justify,
  align,
  gap,
  wrap,
  children,
  ...props
}: FlexLayoutProps) {
  return (
    <div className={flexVariants({ direction, justify, align, gap, wrap, className })} {...props}>
      {children}
    </div>
  );
}
```

## Accessibility Patterns

### Focus Management

```typescript
// Custom hook for managing focus trap in modals
export function useFocusTrap(isActive: boolean) {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!isActive || !containerRef.current) return;

    const container = containerRef.current;
    const focusableElements = container.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );

    const firstElement = focusableElements[0] as HTMLElement;
    const lastElement = focusableElements[focusableElements.length - 1] as HTMLElement;

    function handleTabKey(e: KeyboardEvent) {
      if (e.key !== 'Tab') return;

      if (e.shiftKey) {
        if (document.activeElement === firstElement) {
          e.preventDefault();
          lastElement?.focus();
        }
      } else {
        if (document.activeElement === lastElement) {
          e.preventDefault();
          firstElement?.focus();
        }
      }
    }

    container.addEventListener('keydown', handleTabKey);
    firstElement?.focus();

    return () => {
      container.removeEventListener('keydown', handleTabKey);
    };
  }, [isActive]);

  return containerRef;
}
```

### ARIA Patterns

**Modal with ARIA:**
```typescript
export function Modal({ isOpen, onClose, title, children }: ModalProps) {
  const containerRef = useFocusTrap(isOpen);

  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
      const previousFocus = document.activeElement as HTMLElement;

      return () => {
        document.body.style.overflow = '';
        previousFocus?.focus();
      };
    }
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <div
      className="modal-overlay"
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
      onClick={onClose}
    >
      <div
        ref={containerRef}
        className="modal-content"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="modal-header">
          <h2 id="modal-title" className="modal-title">
            {title}
          </h2>
          <button
            onClick={onClose}
            className="modal-close"
            aria-label="Close modal"
          >
            <IconX />
          </button>
        </div>
        <div className="modal-body">{children}</div>
      </div>
    </div>
  );
}
```

### Keyboard Navigation

```typescript
// Custom hook for keyboard navigation in lists
export function useKeyboardNavigation(itemCount: number) {
  const [selectedIndex, setSelectedIndex] = useState(0);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        setSelectedIndex((prev) => (prev + 1) % itemCount);
        break;
      case 'ArrowUp':
        e.preventDefault();
        setSelectedIndex((prev) => (prev - 1 + itemCount) % itemCount);
        break;
      case 'Home':
        e.preventDefault();
        setSelectedIndex(0);
        break;
      case 'End':
        e.preventDefault();
        setSelectedIndex(itemCount - 1);
        break;
    }
  };

  return { selectedIndex, handleKeyDown, setSelectedIndex };
}
```

## Component Testing Patterns

**Button.test.tsx:**
```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from './Button';

describe('Button', () => {
  it('renders with children', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByRole('button', { name: /click me/i })).toBeInTheDocument();
  });

  it('handles onClick events', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click me</Button>);

    fireEvent.click(screen.getByRole('button'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('disables button when loading', () => {
    render(<Button loading>Loading</Button>);
    const button = screen.getByRole('button');

    expect(button).toBeDisabled();
    expect(button).toHaveAttribute('aria-busy', 'true');
  });

  it('applies correct variant classes', () => {
    const { container } = render(<Button variant="primary">Primary</Button>);
    expect(container.firstChild).toHaveClass('bg-primary-500');
  });

  it('supports keyboard interaction', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click me</Button>);

    const button = screen.getByRole('button');
    fireEvent.keyDown(button, { key: 'Enter' });

    expect(handleClick).toHaveBeenCalled();
  });

  it('is accessible with screen reader', () => {
    render(
      <Button leftIcon={<span>+</span>}>
        Add Item
      </Button>
    );

    const button = screen.getByRole('button', { name: /add item/i });
    expect(button).toBeInTheDocument();
  });
});
```

## Storybook Integration

**Button.stories.tsx:**
```typescript
import type { Meta, StoryObj } from '@storybook/react';
import { Button } from './Button';

const meta: Meta<typeof Button> = {
  title: 'Components/Atoms/Button',
  component: Button,
  tags: ['autodocs'],
  argTypes: {
    variant: {
      control: 'select',
      options: ['primary', 'secondary', 'outline', 'ghost', 'danger'],
    },
    size: {
      control: 'select',
      options: ['sm', 'md', 'lg', 'xl'],
    },
    styleType: {
      control: 'select',
      options: ['default', 'glassmorphism', 'neumorphism', 'brutalist', 'neo-brutalist'],
    },
  },
};

export default meta;
type Story = StoryObj<typeof Button>;

export const Primary: Story = {
  args: {
    variant: 'primary',
    children: 'Button',
  },
};

export const Glassmorphism: Story = {
  args: {
    variant: 'primary',
    styleType: 'glassmorphism',
    children: 'Frosted Glass',
  },
  parameters: {
    backgrounds: {
      default: 'dark',
    },
  },
};

export const NeoBrutalist: Story = {
  args: {
    variant: 'primary',
    styleType: 'neo-brutalist',
    children: 'Bold Button',
  },
};

export const WithIcon: Story = {
  args: {
    variant: 'primary',
    leftIcon: <span>+</span>,
    children: 'Add Item',
  },
};

export const Loading: Story = {
  args: {
    variant: 'primary',
    loading: true,
    children: 'Processing',
  },
};
```

## Best Practices

1. **Accessibility First**: Always include ARIA labels, roles, and keyboard navigation
2. **Semantic HTML**: Use appropriate HTML elements (button, nav, main, etc.)
3. **Responsive Design**: Test components on mobile, tablet, and desktop
4. **Dark Mode Support**: Provide dark mode variants for all components
5. **Performance**: Lazy load heavy components, memoize expensive computations
6. **Type Safety**: Use TypeScript for all components with proper prop types
7. **Testing**: Write unit tests for all components, test accessibility
8. **Documentation**: Document props, variants, and usage examples with Storybook

## Integration with Other Skills

- **design-styles**: Apply different design styles to components
- **css-generation**: Generate component styles from design tokens
- **keycloak-theming**: Use components in authentication pages

## Resources

- [React Accessibility](https://reactjs.org/docs/accessibility.html)
- [WAI-ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/)
- [Radix UI Primitives](https://www.radix-ui.com/)
- [Headless UI](https://headlessui.com/)
- [shadcn/ui](https://ui.shadcn.com/)
- [class-variance-authority](https://cva.style/docs)
