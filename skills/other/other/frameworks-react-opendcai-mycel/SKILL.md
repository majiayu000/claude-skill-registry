---
name: react
description: Builds token-driven React components with TypeScript and modern patterns. Use when creating React component libraries, integrating CSS custom properties, or building Next.js design system components with forwardRef and composition.
---

# React Component Patterns

## Overview

Build accessible, token-driven React components following modern patterns. Covers styling approaches, TypeScript integration, composition patterns, and how to consume design tokens from the token skills.

## When to Use

- Creating a React component library
- Building components that use design tokens
- Setting up a design system in React/Next.js
- Converting designs to React components

## The Process

1. **Identify component type**: Primitive, composite, or layout?
2. **Choose styling approach**: CSS Modules, Tailwind, styled-components, or CSS-in-JS?
3. **Define props interface**: TypeScript types with sensible defaults
4. **Implement with tokens**: Use CSS custom properties or theme context
5. **Add accessibility**: ARIA, keyboard handling, focus management
6. **Export properly**: Named exports, types, and variants

## Styling Approaches

| Approach | When to Use | Token Integration |
|----------|-------------|-------------------|
| CSS Modules | Build-time CSS, SSR-friendly | Import CSS with `var(--token)` |
| Tailwind | Utility-first, rapid development | Extend config with tokens |
| styled-components | Runtime theming, dynamic styles | ThemeProvider with tokens |
| Vanilla Extract | Type-safe, zero-runtime | Import tokens as TS objects |
| CSS Custom Properties | Framework-agnostic, simple | Direct `var(--token)` usage |

## Project Structure

```
src/
├── components/
│   ├── primitives/          # Base components
│   │   ├── Button/
│   │   │   ├── Button.tsx
│   │   │   ├── Button.module.css
│   │   │   ├── Button.test.tsx
│   │   │   └── index.ts
│   │   ├── Input/
│   │   └── Text/
│   ├── composite/           # Composed components
│   │   ├── Card/
│   │   ├── Modal/
│   │   └── Dropdown/
│   └── layout/              # Layout components
│       ├── Stack/
│       ├── Grid/
│       └── Container/
├── tokens/
│   ├── colors.css
│   ├── spacing.css
│   └── index.css
├── hooks/
│   └── useTheme.ts
└── index.ts                 # Public exports
```

## Component Patterns

### Button Component

**Button.tsx:**
```tsx
import { forwardRef, type ButtonHTMLAttributes, type ReactNode } from 'react';
import styles from './Button.module.css';
import { clsx } from 'clsx';

export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  /** Visual style variant */
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger';
  /** Size of the button */
  size?: 'sm' | 'md' | 'lg';
  /** Full width button */
  fullWidth?: boolean;
  /** Loading state - disables button and shows spinner */
  loading?: boolean;
  /** Icon before text */
  leftIcon?: ReactNode;
  /** Icon after text */
  rightIcon?: ReactNode;
  children: ReactNode;
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      variant = 'primary',
      size = 'md',
      fullWidth = false,
      loading = false,
      leftIcon,
      rightIcon,
      disabled,
      className,
      children,
      ...props
    },
    ref
  ) => {
    const isDisabled = disabled || loading;

    return (
      <button
        ref={ref}
        className={clsx(
          styles.button,
          styles[variant],
          styles[size],
          fullWidth && styles.fullWidth,
          loading && styles.loading,
          className
        )}
        disabled={isDisabled}
        aria-busy={loading}
        {...props}
      >
        {loading && <span className={styles.spinner} aria-hidden="true" />}
        {leftIcon && <span className={styles.icon}>{leftIcon}</span>}
        <span className={styles.label}>{children}</span>
        {rightIcon && <span className={styles.icon}>{rightIcon}</span>}
      </button>
    );
  }
);

Button.displayName = 'Button';
```

**Button.module.css:**
```css
.button {
  /* Layout */
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-xs);

  /* Typography */
  font-family: inherit;
  font-weight: 500;
  line-height: 1;
  white-space: nowrap;

  /* Interaction */
  cursor: pointer;
  user-select: none;
  transition:
    background-color 150ms ease,
    border-color 150ms ease,
    transform 100ms ease;

  /* Reset */
  border: 1px solid transparent;
  border-radius: var(--radius-md);
}

.button:focus-visible {
  outline: 2px solid var(--color-primary-500);
  outline-offset: 2px;
}

.button:active:not(:disabled) {
  transform: scale(0.98);
}

.button:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}

/* Variants */
.primary {
  background-color: var(--color-primary-500);
  color: white;
}

.primary:hover:not(:disabled) {
  background-color: var(--color-primary-600);
}

.secondary {
  background-color: transparent;
  border-color: var(--color-gray-300);
  color: var(--color-gray-700);
}

.secondary:hover:not(:disabled) {
  background-color: var(--color-gray-50);
  border-color: var(--color-gray-400);
}

.ghost {
  background-color: transparent;
  color: var(--color-gray-700);
}

.ghost:hover:not(:disabled) {
  background-color: var(--color-gray-100);
}

.danger {
  background-color: var(--color-error-500);
  color: white;
}

.danger:hover:not(:disabled) {
  background-color: var(--color-error-600);
}

/* Sizes */
.sm {
  height: 32px;
  padding: 0 var(--spacing-sm);
  font-size: var(--text-sm);
}

.md {
  height: 40px;
  padding: 0 var(--spacing-md);
  font-size: var(--text-base);
}

.lg {
  height: 48px;
  padding: 0 var(--spacing-lg);
  font-size: var(--text-lg);
}

/* Modifiers */
.fullWidth {
  width: 100%;
}

.loading .label {
  opacity: 0;
}

.spinner {
  position: absolute;
  width: 1em;
  height: 1em;
  border: 2px solid currentColor;
  border-right-color: transparent;
  border-radius: 50%;
  animation: spin 600ms linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.icon {
  display: flex;
  flex-shrink: 0;
}
```

---

### Input Component

**Input.tsx:**
```tsx
import { forwardRef, type InputHTMLAttributes, type ReactNode } from 'react';
import styles from './Input.module.css';
import { clsx } from 'clsx';

export interface InputProps extends Omit<InputHTMLAttributes<HTMLInputElement>, 'size'> {
  /** Label text */
  label?: string;
  /** Helper text below input */
  helperText?: string;
  /** Error message - sets error state */
  error?: string;
  /** Size variant */
  size?: 'sm' | 'md' | 'lg';
  /** Icon/element at start */
  startAdornment?: ReactNode;
  /** Icon/element at end */
  endAdornment?: ReactNode;
  /** Full width */
  fullWidth?: boolean;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  (
    {
      label,
      helperText,
      error,
      size = 'md',
      startAdornment,
      endAdornment,
      fullWidth = false,
      disabled,
      id,
      className,
      ...props
    },
    ref
  ) => {
    const inputId = id || `input-${Math.random().toString(36).slice(2, 9)}`;
    const helperId = `${inputId}-helper`;
    const errorId = `${inputId}-error`;

    return (
      <div className={clsx(styles.wrapper, fullWidth && styles.fullWidth, className)}>
        {label && (
          <label htmlFor={inputId} className={styles.label}>
            {label}
          </label>
        )}

        <div
          className={clsx(
            styles.inputWrapper,
            styles[size],
            error && styles.error,
            disabled && styles.disabled
          )}
        >
          {startAdornment && (
            <span className={styles.adornment}>{startAdornment}</span>
          )}

          <input
            ref={ref}
            id={inputId}
            className={styles.input}
            disabled={disabled}
            aria-invalid={!!error}
            aria-describedby={
              error ? errorId : helperText ? helperId : undefined
            }
            {...props}
          />

          {endAdornment && (
            <span className={styles.adornment}>{endAdornment}</span>
          )}
        </div>

        {error && (
          <span id={errorId} className={styles.errorText} role="alert">
            {error}
          </span>
        )}

        {helperText && !error && (
          <span id={helperId} className={styles.helperText}>
            {helperText}
          </span>
        )}
      </div>
    );
  }
);

Input.displayName = 'Input';
```

---

### Stack Layout Component

**Stack.tsx:**
```tsx
import { forwardRef, type HTMLAttributes, type ElementType } from 'react';
import styles from './Stack.module.css';
import { clsx } from 'clsx';

type SpacingToken = 'none' | 'xs' | 'sm' | 'md' | 'lg' | 'xl' | '2xl';

export interface StackProps extends HTMLAttributes<HTMLElement> {
  /** HTML element or component to render */
  as?: ElementType;
  /** Direction of stacking */
  direction?: 'row' | 'column';
  /** Gap between items */
  gap?: SpacingToken;
  /** Horizontal alignment */
  align?: 'start' | 'center' | 'end' | 'stretch' | 'baseline';
  /** Vertical alignment (when row) or horizontal (when column) */
  justify?: 'start' | 'center' | 'end' | 'between' | 'around' | 'evenly';
  /** Wrap items */
  wrap?: boolean;
  /** Full width */
  fullWidth?: boolean;
}

export const Stack = forwardRef<HTMLElement, StackProps>(
  (
    {
      as: Component = 'div',
      direction = 'column',
      gap = 'md',
      align = 'stretch',
      justify = 'start',
      wrap = false,
      fullWidth = false,
      className,
      style,
      ...props
    },
    ref
  ) => {
    return (
      <Component
        ref={ref}
        className={clsx(
          styles.stack,
          styles[direction],
          wrap && styles.wrap,
          fullWidth && styles.fullWidth,
          className
        )}
        style={{
          '--stack-gap': `var(--spacing-${gap})`,
          '--stack-align': alignMap[align],
          '--stack-justify': justifyMap[justify],
          ...style,
        } as React.CSSProperties}
        {...props}
      />
    );
  }
);

const alignMap = {
  start: 'flex-start',
  center: 'center',
  end: 'flex-end',
  stretch: 'stretch',
  baseline: 'baseline',
};

const justifyMap = {
  start: 'flex-start',
  center: 'center',
  end: 'flex-end',
  between: 'space-between',
  around: 'space-around',
  evenly: 'space-evenly',
};

Stack.displayName = 'Stack';
```

**Stack.module.css:**
```css
.stack {
  display: flex;
  gap: var(--stack-gap, var(--spacing-md));
  align-items: var(--stack-align, stretch);
  justify-content: var(--stack-justify, flex-start);
}

.column {
  flex-direction: column;
}

.row {
  flex-direction: row;
}

.wrap {
  flex-wrap: wrap;
}

.fullWidth {
  width: 100%;
}
```

---

### Card Component

**Card.tsx:**
```tsx
import { forwardRef, type HTMLAttributes, type ReactNode } from 'react';
import styles from './Card.module.css';
import { clsx } from 'clsx';

export interface CardProps extends HTMLAttributes<HTMLDivElement> {
  /** Padding size */
  padding?: 'none' | 'sm' | 'md' | 'lg';
  /** Shadow elevation */
  elevation?: 'none' | 'sm' | 'md' | 'lg';
  /** Border style */
  variant?: 'elevated' | 'outlined' | 'filled';
  /** Make card interactive (hover effects, cursor) */
  interactive?: boolean;
  /** As a link or button */
  as?: 'div' | 'article' | 'section' | 'a' | 'button';
}

export const Card = forwardRef<HTMLDivElement, CardProps>(
  (
    {
      padding = 'md',
      elevation = 'sm',
      variant = 'elevated',
      interactive = false,
      as: Component = 'div',
      className,
      children,
      ...props
    },
    ref
  ) => {
    return (
      <Component
        ref={ref as any}
        className={clsx(
          styles.card,
          styles[`padding-${padding}`],
          styles[`elevation-${elevation}`],
          styles[variant],
          interactive && styles.interactive,
          className
        )}
        {...props}
      >
        {children}
      </Component>
    );
  }
);

Card.displayName = 'Card';

// Sub-components
export const CardHeader = ({ className, ...props }: HTMLAttributes<HTMLDivElement>) => (
  <div className={clsx(styles.header, className)} {...props} />
);

export const CardBody = ({ className, ...props }: HTMLAttributes<HTMLDivElement>) => (
  <div className={clsx(styles.body, className)} {...props} />
);

export const CardFooter = ({ className, ...props }: HTMLAttributes<HTMLDivElement>) => (
  <div className={clsx(styles.footer, className)} {...props} />
);
```

---

## Theme Context Pattern

**ThemeProvider.tsx:**
```tsx
import { createContext, useContext, useState, useEffect, type ReactNode } from 'react';

type Theme = 'light' | 'dark' | 'system';

interface ThemeContextValue {
  theme: Theme;
  resolvedTheme: 'light' | 'dark';
  setTheme: (theme: Theme) => void;
}

const ThemeContext = createContext<ThemeContextValue | null>(null);

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme, setTheme] = useState<Theme>('system');
  const [resolvedTheme, setResolvedTheme] = useState<'light' | 'dark'>('light');

  useEffect(() => {
    const root = document.documentElement;

    if (theme === 'system') {
      const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
      const handleChange = () => {
        const resolved = mediaQuery.matches ? 'dark' : 'light';
        setResolvedTheme(resolved);
        root.dataset.theme = resolved;
      };
      handleChange();
      mediaQuery.addEventListener('change', handleChange);
      return () => mediaQuery.removeEventListener('change', handleChange);
    } else {
      setResolvedTheme(theme);
      root.dataset.theme = theme;
    }
  }, [theme]);

  return (
    <ThemeContext.Provider value={{ theme, resolvedTheme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) throw new Error('useTheme must be used within ThemeProvider');
  return context;
}
```

**Theme tokens in CSS:**
```css
:root,
[data-theme="light"] {
  --color-background: var(--color-white);
  --color-foreground: var(--color-gray-900);
  --color-muted: var(--color-gray-500);
  --color-border: var(--color-gray-200);
  --color-surface: var(--color-gray-50);
}

[data-theme="dark"] {
  --color-background: var(--color-gray-950);
  --color-foreground: var(--color-gray-50);
  --color-muted: var(--color-gray-400);
  --color-border: var(--color-gray-800);
  --color-surface: var(--color-gray-900);
}
```

---

## Compound Component Pattern

**Select.tsx:**
```tsx
import {
  createContext,
  useContext,
  useState,
  type ReactNode,
  type HTMLAttributes,
} from 'react';

interface SelectContextValue {
  value: string;
  onChange: (value: string) => void;
  open: boolean;
  setOpen: (open: boolean) => void;
}

const SelectContext = createContext<SelectContextValue | null>(null);

interface SelectProps {
  value: string;
  onChange: (value: string) => void;
  children: ReactNode;
}

export function Select({ value, onChange, children }: SelectProps) {
  const [open, setOpen] = useState(false);

  return (
    <SelectContext.Provider value={{ value, onChange, open, setOpen }}>
      <div className="select" data-open={open}>
        {children}
      </div>
    </SelectContext.Provider>
  );
}

Select.Trigger = function SelectTrigger({ children }: { children: ReactNode }) {
  const ctx = useContext(SelectContext)!;
  return (
    <button
      type="button"
      aria-haspopup="listbox"
      aria-expanded={ctx.open}
      onClick={() => ctx.setOpen(!ctx.open)}
    >
      {children}
    </button>
  );
};

Select.Content = function SelectContent({ children }: { children: ReactNode }) {
  const ctx = useContext(SelectContext)!;
  if (!ctx.open) return null;
  return (
    <ul role="listbox">
      {children}
    </ul>
  );
};

Select.Option = function SelectOption({
  value,
  children,
}: {
  value: string;
  children: ReactNode;
}) {
  const ctx = useContext(SelectContext)!;
  const selected = ctx.value === value;
  return (
    <li
      role="option"
      aria-selected={selected}
      onClick={() => {
        ctx.onChange(value);
        ctx.setOpen(false);
      }}
    >
      {children}
    </li>
  );
};
```

---

## Hook Patterns

**useControllable (controlled/uncontrolled state):**
```tsx
import { useState, useCallback } from 'react';

export function useControllable<T>({
  value,
  defaultValue,
  onChange,
}: {
  value?: T;
  defaultValue: T;
  onChange?: (value: T) => void;
}) {
  const [internalValue, setInternalValue] = useState(defaultValue);
  const isControlled = value !== undefined;
  const currentValue = isControlled ? value : internalValue;

  const setValue = useCallback(
    (next: T | ((prev: T) => T)) => {
      const nextValue = typeof next === 'function' ? (next as Function)(currentValue) : next;
      if (!isControlled) setInternalValue(nextValue);
      onChange?.(nextValue);
    },
    [isControlled, currentValue, onChange]
  );

  return [currentValue, setValue] as const;
}
```

**useMediaQuery:**
```tsx
import { useState, useEffect } from 'react';

export function useMediaQuery(query: string): boolean {
  const [matches, setMatches] = useState(false);

  useEffect(() => {
    const mediaQuery = window.matchMedia(query);
    setMatches(mediaQuery.matches);

    const handler = (e: MediaQueryListEvent) => setMatches(e.matches);
    mediaQuery.addEventListener('change', handler);
    return () => mediaQuery.removeEventListener('change', handler);
  }, [query]);

  return matches;
}

// Usage with breakpoint tokens
const isMobile = useMediaQuery('(max-width: 767px)');
const isTablet = useMediaQuery('(min-width: 768px) and (max-width: 1023px)');
const isDesktop = useMediaQuery('(min-width: 1024px)');
```

---

## Export Pattern

**index.ts (component barrel):**
```tsx
// Components
export { Button, type ButtonProps } from './components/primitives/Button';
export { Input, type InputProps } from './components/primitives/Input';
export { Card, CardHeader, CardBody, CardFooter, type CardProps } from './components/composite/Card';
export { Stack, type StackProps } from './components/layout/Stack';

// Hooks
export { useTheme } from './hooks/useTheme';
export { useControllable } from './hooks/useControllable';
export { useMediaQuery } from './hooks/useMediaQuery';

// Context
export { ThemeProvider } from './providers/ThemeProvider';

// Types
export type { Theme } from './types';
```

---

## Testing Patterns

**Button.test.tsx:**
```tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Button } from './Button';

describe('Button', () => {
  it('renders children', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByRole('button', { name: 'Click me' })).toBeInTheDocument();
  });

  it('handles click events', async () => {
    const onClick = vi.fn();
    render(<Button onClick={onClick}>Click me</Button>);
    await userEvent.click(screen.getByRole('button'));
    expect(onClick).toHaveBeenCalledTimes(1);
  });

  it('is disabled when loading', () => {
    render(<Button loading>Click me</Button>);
    expect(screen.getByRole('button')).toBeDisabled();
    expect(screen.getByRole('button')).toHaveAttribute('aria-busy', 'true');
  });

  it('applies variant classes', () => {
    render(<Button variant="danger">Delete</Button>);
    expect(screen.getByRole('button')).toHaveClass('danger');
  });
});
```
