---
name: atomic-design-atoms
description: Use when creating atomic-level UI components like buttons, inputs, labels, and icons. The smallest building blocks of a design system.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# Atomic Design: Atoms

Master the creation of atomic components - the fundamental, indivisible building blocks of your design system. Atoms are the smallest functional units that cannot be broken down further without losing meaning.

## What Are Atoms?

Atoms are the basic UI elements that serve as the foundation for everything else in your design system. They are:

- **Indivisible**: Cannot be broken down into smaller functional units
- **Reusable**: Used throughout the application in various contexts
- **Stateless**: Typically controlled by parent components
- **Styled**: Implement design tokens for consistent appearance
- **Accessible**: Built with a11y in mind from the start

## Common Atom Types

### Interactive Atoms

- Buttons
- Links
- Inputs (text, checkbox, radio, select)
- Toggles/Switches
- Sliders

### Display Atoms

- Typography (headings, paragraphs, labels)
- Icons
- Images/Avatars
- Badges/Tags
- Dividers
- Spinners/Loaders

### Form Atoms

- Input fields
- Textareas
- Checkboxes
- Radio buttons
- Select dropdowns
- Labels

## Button Atom Example

### Basic Implementation

```typescript
// atoms/Button/Button.tsx
import React from 'react';
import type { ButtonHTMLAttributes } from 'react';
import styles from './Button.module.css';

export type ButtonVariant = 'primary' | 'secondary' | 'tertiary' | 'danger';
export type ButtonSize = 'sm' | 'md' | 'lg';

export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  /** Visual style variant */
  variant?: ButtonVariant;
  /** Size of the button */
  size?: ButtonSize;
  /** Full width button */
  fullWidth?: boolean;
  /** Loading state */
  isLoading?: boolean;
  /** Left icon */
  leftIcon?: React.ReactNode;
  /** Right icon */
  rightIcon?: React.ReactNode;
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      variant = 'primary',
      size = 'md',
      fullWidth = false,
      isLoading = false,
      leftIcon,
      rightIcon,
      disabled,
      children,
      className,
      ...props
    },
    ref
  ) => {
    const classNames = [
      styles.button,
      styles[variant],
      styles[size],
      fullWidth && styles.fullWidth,
      isLoading && styles.loading,
      className,
    ]
      .filter(Boolean)
      .join(' ');

    return (
      <button
        ref={ref}
        className={classNames}
        disabled={disabled || isLoading}
        aria-busy={isLoading}
        {...props}
      >
        {isLoading ? (
          <span className={styles.spinner} aria-hidden="true" />
        ) : (
          <>
            {leftIcon && <span className={styles.leftIcon}>{leftIcon}</span>}
            <span className={styles.content}>{children}</span>
            {rightIcon && <span className={styles.rightIcon}>{rightIcon}</span>}
          </>
        )}
      </button>
    );
  }
);

Button.displayName = 'Button';
```

### Button Styles

```css
/* atoms/Button/Button.module.css */
.button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  border: none;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 150ms ease-in-out;
  text-decoration: none;
}

.button:focus-visible {
  outline: 2px solid var(--color-focus);
  outline-offset: 2px;
}

.button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Variants */
.primary {
  background-color: var(--color-primary-500);
  color: var(--color-white);
}

.primary:hover:not(:disabled) {
  background-color: var(--color-primary-600);
}

.secondary {
  background-color: transparent;
  color: var(--color-primary-500);
  border: 1px solid var(--color-primary-500);
}

.secondary:hover:not(:disabled) {
  background-color: var(--color-primary-50);
}

.tertiary {
  background-color: transparent;
  color: var(--color-primary-500);
}

.tertiary:hover:not(:disabled) {
  background-color: var(--color-primary-50);
}

.danger {
  background-color: var(--color-danger-500);
  color: var(--color-white);
}

.danger:hover:not(:disabled) {
  background-color: var(--color-danger-600);
}

/* Sizes */
.sm {
  padding: 6px 12px;
  font-size: 14px;
  min-height: 32px;
}

.md {
  padding: 8px 16px;
  font-size: 16px;
  min-height: 40px;
}

.lg {
  padding: 12px 24px;
  font-size: 18px;
  min-height: 48px;
}

/* Modifiers */
.fullWidth {
  width: 100%;
}

.loading {
  position: relative;
  color: transparent;
}

.spinner {
  position: absolute;
  width: 16px;
  height: 16px;
  border: 2px solid currentColor;
  border-right-color: transparent;
  border-radius: 50%;
  animation: spin 0.75s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Icon spacing */
.leftIcon,
.rightIcon {
  display: flex;
  align-items: center;
}
```

## Input Atom Example

```typescript
// atoms/Input/Input.tsx
import React from 'react';
import type { InputHTMLAttributes } from 'react';
import styles from './Input.module.css';

export type InputSize = 'sm' | 'md' | 'lg';

export interface InputProps
  extends Omit<InputHTMLAttributes<HTMLInputElement>, 'size'> {
  /** Size variant */
  size?: InputSize;
  /** Error state */
  hasError?: boolean;
  /** Left addon element */
  leftAddon?: React.ReactNode;
  /** Right addon element */
  rightAddon?: React.ReactNode;
}

export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  (
    {
      size = 'md',
      hasError = false,
      leftAddon,
      rightAddon,
      disabled,
      className,
      ...props
    },
    ref
  ) => {
    const wrapperClasses = [
      styles.wrapper,
      styles[size],
      hasError && styles.error,
      disabled && styles.disabled,
      className,
    ]
      .filter(Boolean)
      .join(' ');

    return (
      <div className={wrapperClasses}>
        {leftAddon && <span className={styles.leftAddon}>{leftAddon}</span>}
        <input
          ref={ref}
          className={styles.input}
          disabled={disabled}
          aria-invalid={hasError}
          {...props}
        />
        {rightAddon && <span className={styles.rightAddon}>{rightAddon}</span>}
      </div>
    );
  }
);

Input.displayName = 'Input';
```

```css
/* atoms/Input/Input.module.css */
.wrapper {
  display: flex;
  align-items: center;
  border: 1px solid var(--color-neutral-300);
  border-radius: 6px;
  background-color: var(--color-white);
  transition: border-color 150ms, box-shadow 150ms;
}

.wrapper:focus-within {
  border-color: var(--color-primary-500);
  box-shadow: 0 0 0 3px var(--color-primary-100);
}

.input {
  flex: 1;
  border: none;
  background: transparent;
  outline: none;
  width: 100%;
}

.input::placeholder {
  color: var(--color-neutral-400);
}

/* Error state */
.error {
  border-color: var(--color-danger-500);
}

.error:focus-within {
  border-color: var(--color-danger-500);
  box-shadow: 0 0 0 3px var(--color-danger-100);
}

/* Disabled state */
.disabled {
  background-color: var(--color-neutral-100);
  cursor: not-allowed;
}

.disabled .input {
  cursor: not-allowed;
}

/* Sizes */
.sm {
  min-height: 32px;
}

.sm .input {
  padding: 6px 12px;
  font-size: 14px;
}

.md {
  min-height: 40px;
}

.md .input {
  padding: 8px 12px;
  font-size: 16px;
}

.lg {
  min-height: 48px;
}

.lg .input {
  padding: 12px 16px;
  font-size: 18px;
}

/* Addons */
.leftAddon,
.rightAddon {
  display: flex;
  align-items: center;
  padding: 0 12px;
  color: var(--color-neutral-500);
}
```

## Label Atom Example

```typescript
// atoms/Label/Label.tsx
import React from 'react';
import type { LabelHTMLAttributes } from 'react';
import styles from './Label.module.css';

export interface LabelProps extends LabelHTMLAttributes<HTMLLabelElement> {
  /** Indicates required field */
  required?: boolean;
  /** Disabled state styling */
  disabled?: boolean;
}

export const Label = React.forwardRef<HTMLLabelElement, LabelProps>(
  ({ required = false, disabled = false, children, className, ...props }, ref) => {
    const classNames = [
      styles.label,
      disabled && styles.disabled,
      className,
    ]
      .filter(Boolean)
      .join(' ');

    return (
      <label ref={ref} className={classNames} {...props}>
        {children}
        {required && (
          <span className={styles.required} aria-hidden="true">
            *
          </span>
        )}
      </label>
    );
  }
);

Label.displayName = 'Label';
```

## Icon Atom Example

```typescript
// atoms/Icon/Icon.tsx
import React from 'react';

export type IconSize = 'xs' | 'sm' | 'md' | 'lg' | 'xl';

const sizeMap: Record<IconSize, number> = {
  xs: 12,
  sm: 16,
  md: 20,
  lg: 24,
  xl: 32,
};

export interface IconProps extends React.SVGAttributes<SVGElement> {
  /** Icon name/identifier */
  name: string;
  /** Icon size */
  size?: IconSize;
  /** Custom color */
  color?: string;
  /** Accessible label */
  label?: string;
}

export const Icon: React.FC<IconProps> = ({
  name,
  size = 'md',
  color = 'currentColor',
  label,
  className,
  ...props
}) => {
  const pixelSize = sizeMap[size];

  return (
    <svg
      className={className}
      width={pixelSize}
      height={pixelSize}
      fill={color}
      aria-label={label}
      aria-hidden={!label}
      role={label ? 'img' : 'presentation'}
      {...props}
    >
      <use href={`/icons.svg#${name}`} />
    </svg>
  );
};

Icon.displayName = 'Icon';
```

## Avatar Atom Example

```typescript
// atoms/Avatar/Avatar.tsx
import React from 'react';
import styles from './Avatar.module.css';

export type AvatarSize = 'xs' | 'sm' | 'md' | 'lg' | 'xl';

export interface AvatarProps {
  /** Image source URL */
  src?: string;
  /** Alt text for image */
  alt: string;
  /** Fallback initials */
  initials?: string;
  /** Size variant */
  size?: AvatarSize;
  /** Additional class name */
  className?: string;
}

export const Avatar: React.FC<AvatarProps> = ({
  src,
  alt,
  initials,
  size = 'md',
  className,
}) => {
  const [imageError, setImageError] = React.useState(false);

  const classNames = [styles.avatar, styles[size], className]
    .filter(Boolean)
    .join(' ');

  const showImage = src && !imageError;
  const showInitials = !showImage && initials;

  return (
    <div className={classNames} role="img" aria-label={alt}>
      {showImage && (
        <img
          src={src}
          alt={alt}
          className={styles.image}
          onError={() => setImageError(true)}
        />
      )}
      {showInitials && (
        <span className={styles.initials} aria-hidden="true">
          {initials}
        </span>
      )}
      {!showImage && !showInitials && (
        <span className={styles.placeholder} aria-hidden="true">
          ?
        </span>
      )}
    </div>
  );
};

Avatar.displayName = 'Avatar';
```

## Badge Atom Example

```typescript
// atoms/Badge/Badge.tsx
import React from 'react';
import styles from './Badge.module.css';

export type BadgeVariant =
  | 'default'
  | 'primary'
  | 'success'
  | 'warning'
  | 'danger'
  | 'info';

export type BadgeSize = 'sm' | 'md';

export interface BadgeProps {
  /** Visual variant */
  variant?: BadgeVariant;
  /** Size variant */
  size?: BadgeSize;
  /** Badge content */
  children: React.ReactNode;
  /** Additional class name */
  className?: string;
}

export const Badge: React.FC<BadgeProps> = ({
  variant = 'default',
  size = 'md',
  children,
  className,
}) => {
  const classNames = [styles.badge, styles[variant], styles[size], className]
    .filter(Boolean)
    .join(' ');

  return <span className={classNames}>{children}</span>;
};

Badge.displayName = 'Badge';
```

## Checkbox Atom Example

```typescript
// atoms/Checkbox/Checkbox.tsx
import React from 'react';
import type { InputHTMLAttributes } from 'react';
import styles from './Checkbox.module.css';

export interface CheckboxProps
  extends Omit<InputHTMLAttributes<HTMLInputElement>, 'type'> {
  /** Indeterminate state */
  indeterminate?: boolean;
  /** Label text */
  label?: string;
}

export const Checkbox = React.forwardRef<HTMLInputElement, CheckboxProps>(
  ({ indeterminate = false, label, disabled, className, ...props }, ref) => {
    const inputRef = React.useRef<HTMLInputElement>(null);

    React.useImperativeHandle(ref, () => inputRef.current!);

    React.useEffect(() => {
      if (inputRef.current) {
        inputRef.current.indeterminate = indeterminate;
      }
    }, [indeterminate]);

    const wrapperClasses = [
      styles.wrapper,
      disabled && styles.disabled,
      className,
    ]
      .filter(Boolean)
      .join(' ');

    const checkbox = (
      <span className={styles.checkbox}>
        <input
          ref={inputRef}
          type="checkbox"
          className={styles.input}
          disabled={disabled}
          {...props}
        />
        <span className={styles.control} aria-hidden="true">
          <svg className={styles.check} viewBox="0 0 12 10">
            <polyline points="1.5 6 4.5 9 10.5 1" />
          </svg>
          <svg className={styles.indeterminate} viewBox="0 0 12 2">
            <line x1="1" y1="1" x2="11" y2="1" />
          </svg>
        </span>
      </span>
    );

    if (label) {
      return (
        <label className={wrapperClasses}>
          {checkbox}
          <span className={styles.label}>{label}</span>
        </label>
      );
    }

    return checkbox;
  }
);

Checkbox.displayName = 'Checkbox';
```

## Typography Atoms

```typescript
// atoms/Typography/Text.tsx
import React from 'react';
import styles from './Typography.module.css';

export type TextSize = 'xs' | 'sm' | 'md' | 'lg' | 'xl';
export type TextWeight = 'normal' | 'medium' | 'semibold' | 'bold';
export type TextColor = 'default' | 'muted' | 'primary' | 'success' | 'danger';

export interface TextProps {
  as?: 'p' | 'span' | 'div';
  size?: TextSize;
  weight?: TextWeight;
  color?: TextColor;
  truncate?: boolean;
  children: React.ReactNode;
  className?: string;
}

export const Text: React.FC<TextProps> = ({
  as: Component = 'p',
  size = 'md',
  weight = 'normal',
  color = 'default',
  truncate = false,
  children,
  className,
}) => {
  const classNames = [
    styles.text,
    styles[`size-${size}`],
    styles[`weight-${weight}`],
    styles[`color-${color}`],
    truncate && styles.truncate,
    className,
  ]
    .filter(Boolean)
    .join(' ');

  return <Component className={classNames}>{children}</Component>;
};

// atoms/Typography/Heading.tsx
export type HeadingLevel = 1 | 2 | 3 | 4 | 5 | 6;

export interface HeadingProps {
  level: HeadingLevel;
  as?: `h${HeadingLevel}`;
  children: React.ReactNode;
  className?: string;
}

export const Heading: React.FC<HeadingProps> = ({
  level,
  as,
  children,
  className,
}) => {
  const Component = as || (`h${level}` as const);
  const classNames = [styles.heading, styles[`h${level}`], className]
    .filter(Boolean)
    .join(' ');

  return <Component className={classNames}>{children}</Component>;
};
```

## Best Practices

### 1. Use forwardRef for DOM Access

```typescript
// GOOD: Allows parent to access DOM node
export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  (props, ref) => <input ref={ref} {...props} />
);

// BAD: No way for parent to access DOM
export const Input = (props: InputProps) => <input {...props} />;
```

### 2. Extend Native HTML Attributes

```typescript
// GOOD: Supports all native button attributes
interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary';
}

// BAD: Missing native attributes
interface ButtonProps {
  onClick?: () => void;
  disabled?: boolean;
}
```

### 3. Provide Sensible Defaults

```typescript
// GOOD: Works out of the box
export const Button = ({
  variant = 'primary',
  size = 'md',
  type = 'button', // Prevent accidental form submissions
  ...props
}) => { ... };

// BAD: Requires explicit props
export const Button = ({ variant, size, ...props }) => { ... };
```

### 4. Keep Atoms Presentation-Only

```typescript
// GOOD: No business logic
const Button = ({ onClick, children }) => (
  <button onClick={onClick}>{children}</button>
);

// BAD: Atom has API call
const SubmitButton = () => {
  const handleClick = async () => {
    await api.submit(); // Business logic in atom!
  };
  return <button onClick={handleClick}>Submit</button>;
};
```

## Anti-Patterns to Avoid

### 1. Atoms with Internal State

```typescript
// BAD: Atom manages its own state
const Input = () => {
  const [value, setValue] = useState('');
  return <input value={value} onChange={(e) => setValue(e.target.value)} />;
};

// GOOD: Controlled by parent
const Input = ({ value, onChange }) => (
  <input value={value} onChange={onChange} />
);
```

### 2. Atoms with Complex Logic

```typescript
// BAD: Complex validation in atom
const EmailInput = ({ value, onChange }) => {
  const isValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
  return <input value={value} className={isValid ? '' : 'error'} />;
};

// GOOD: Validation handled by parent/molecule
const Input = ({ value, onChange, hasError }) => (
  <input value={value} className={hasError ? 'error' : ''} />
);
```

### 3. Hardcoded Styles

```typescript
// BAD: Hardcoded colors
const Button = () => (
  <button style={{ backgroundColor: '#2196f3' }}>Click</button>
);

// GOOD: Uses design tokens
const Button = () => (
  <button style={{ backgroundColor: 'var(--color-primary-500)' }}>
    Click
  </button>
);
```

## When to Use This Skill

- Creating new basic UI components
- Refactoring existing components to atoms
- Building a design system foundation
- Ensuring consistency across components
- Improving component reusability

## Related Skills

- `atomic-design-fundamentals` - Core methodology overview
- `atomic-design-molecules` - Composing atoms into molecules
