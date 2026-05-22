---
name: typescript-prop-definition
version: "1.0"
description: >
  TypeScript interface conventions for component props with JSDoc comments and utility types.
  PROACTIVELY activate for: (1) defining component prop interfaces, (2) using generics for reusable components, (3) integrating cva VariantProps.
  Triggers: "props", "interface", "VariantProps"
group: ui
core-integration:
  techniques:
    primary: ["structured_decomposition"]
    secondary: []
  contracts:
    input: "none"
    output: "none"
  patterns: "none"
  rubrics: "none"
---

# TypeScript Prop Definition

## Interface Convention

Use `interface` for component props:

```tsx
/**
 * Props for the Button component
 */
interface ButtonProps {
  /** Button text or content */
  children: React.ReactNode;
  /** Click handler */
  onClick?: () => void;
  /** Whether button is disabled */
  disabled?: boolean;
}

export function Button({ children, onClick, disabled }: ButtonProps) {
  // ...
}
```

## JSDoc Comments

Document each prop:

```tsx
interface UserCardProps {
  /** User's full name */
  name: string;
  /** User's email address */
  email: string;
  /** Optional avatar URL */
  avatarUrl?: string;
  /** Callback when card is clicked */
  onSelect?: (userId: string) => void;
}
```

## Generics for Reusable Components

```tsx
interface ListProps<T> {
  items: T[];
  renderItem: (item: T) => React.ReactNode;
  keyExtractor: (item: T) => string;
}

function List<T>({ items, renderItem, keyExtractor }: ListProps<T>) {
  return (
    <ul>
      {items.map(item => (
        <li key={keyExtractor(item)}>
          {renderItem(item)}
        </li>
      ))}
    </ul>
  );
}

// Usage
<List
  items={users}
  renderItem={(user) => <span>{user.name}</span>}
  keyExtractor={(user) => user.id}
/>
```

## Utility Types

### Extending Native Props

```tsx
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'default' | 'destructive';
  isLoading?: boolean;
}

export function Button({ variant, isLoading, children, ...props }: ButtonProps) {
  return (
    <button {...props} disabled={isLoading || props.disabled}>
      {isLoading ? 'Loading...' : children}
    </button>
  );
}
```

### Pick/Omit

```tsx
// Pick specific fields from existing type
type UserPublicInfo = Pick<User, 'name' | 'email'>;

// Omit sensitive fields
type UserWithoutPassword = Omit<User, 'password'>;

// Partial - all fields optional
type PartialUser = Partial<User>;

// Required - all fields required
type RequiredUser = Required<PartialUser>;
```

### ComponentPropsWithoutRef

```tsx
import { ComponentPropsWithoutRef } from 'react';

interface InputProps extends ComponentPropsWithoutRef<'input'> {
  label: string;
  error?: string;
}

export function Input({ label, error, ...props }: InputProps) {
  return (
    <div>
      <label>{label}</label>
      <input {...props} />
      {error && <span className="text-destructive">{error}</span>}
    </div>
  );
}
```

## cva + VariantProps Pattern

```tsx
import { cva, type VariantProps } from 'class-variance-authority';

const buttonVariants = cva("base-classes", {
  variants: {
    variant: {
      default: "...",
      destructive: "...",
    },
    size: {
      default: "...",
      sm: "...",
    },
  },
  defaultVariants: {
    variant: "default",
    size: "default",
  },
});

// Automatically inferred type from cva
interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  // variant?: "default" | "destructive" - inferred from cva
  // size?: "default" | "sm" - inferred from cva
}

export function Button({ variant, size, className, ...props }: ButtonProps) {
  return (
    <button
      className={buttonVariants({ variant, size, className })}
      {...props}
    />
  );
}
```

## Polymorphic Components

```tsx
type PolymorphicComponentProps<E extends React.ElementType> = {
  as?: E;
  children: React.ReactNode;
} & Omit<React.ComponentPropsWithoutRef<E>, 'as' | 'children'>;

function Box<E extends React.ElementType = 'div'>({
  as,
  children,
  ...props
}: PolymorphicComponentProps<E>) {
  const Component = as || 'div';
  return <Component {...props}>{children}</Component>;
}

// Usage
<Box>Default div</Box>
<Box as="section">Section element</Box>
<Box as="a" href="/about">Link element</Box>
```

## Anti-Patterns

- Using `any` type
- Missing JSDoc comments
- Manually typing variants (use VariantProps)
- `children: any` (use `React.ReactNode`)
- Not extending native element props

## Best Practices

- Explicit interface with JSDoc
- Use VariantProps for cva
- Leverage utility types (Pick, Omit, Partial)
- Extend native HTML attributes when wrapping elements
- Use generics for truly reusable components

---

**Related Skills**: `typescript-type-safe-api-contracts`, `shadcn-component-scaffolding`
