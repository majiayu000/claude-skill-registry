---
name: tailwindcss-advanced-components
description: Tailwind CSS advanced component patterns with CVA integration and variant management
---

# Tailwind CSS Advanced Component Patterns

## Component Variants with CVA

### Class Variance Authority Integration

```bash
npm install class-variance-authority
```

```typescript
// components/Button.tsx
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const buttonVariants = cva(
  // Base styles
  'inline-flex items-center justify-center rounded-lg font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50',
  {
    variants: {
      variant: {
        default: 'bg-brand-500 text-white hover:bg-brand-600 focus-visible:ring-brand-500',
        secondary: 'bg-gray-100 text-gray-900 hover:bg-gray-200 focus-visible:ring-gray-500',
        outline: 'border border-gray-300 bg-transparent hover:bg-gray-100 focus-visible:ring-gray-500',
        ghost: 'hover:bg-gray-100 focus-visible:ring-gray-500',
        destructive: 'bg-red-500 text-white hover:bg-red-600 focus-visible:ring-red-500',
        link: 'text-brand-500 underline-offset-4 hover:underline',
      },
      size: {
        sm: 'h-8 px-3 text-sm',
        md: 'h-10 px-4 text-sm',
        lg: 'h-12 px-6 text-base',
        xl: 'h-14 px-8 text-lg',
        icon: 'h-10 w-10',
      },
      fullWidth: {
        true: 'w-full',
      },
    },
    compoundVariants: [
      {
        variant: 'outline',
        size: 'sm',
        className: 'border',
      },
      {
        variant: 'outline',
        size: ['md', 'lg', 'xl'],
        className: 'border-2',
      },
    ],
    defaultVariants: {
      variant: 'default',
      size: 'md',
    },
  }
);

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean;
}

export function Button({
  className,
  variant,
  size,
  fullWidth,
  asChild = false,
  ...props
}: ButtonProps) {
  return (
    <button
      className={cn(buttonVariants({ variant, size, fullWidth, className }))}
      {...props}
    />
  );
}
```

### Usage

```tsx
<Button>Default</Button>
<Button variant="secondary" size="lg">Large Secondary</Button>
<Button variant="destructive" fullWidth>Delete</Button>
<Button variant="ghost" size="icon"><IconMenu /></Button>
```

## Compound Components Pattern

### Context-Based Component System

```tsx
// components/Card/index.tsx
import { createContext, useContext, forwardRef } from 'react';
import { cn } from '@/lib/utils';

// Context for shared state
const CardContext = createContext<{ variant?: 'default' | 'elevated' | 'outline' }>({});

// Root component
interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: 'default' | 'elevated' | 'outline';
}

const Card = forwardRef<HTMLDivElement, CardProps>(
  ({ className, variant = 'default', children, ...props }, ref) => {
    const variants = {
      default: 'bg-white border border-gray-200',
      elevated: 'bg-white shadow-lg',
      outline: 'bg-transparent border-2 border-gray-300',
    };

    return (
      <CardContext.Provider value={{ variant }}>
        <div
          ref={ref}
          className={cn(
            'rounded-xl',
            variants[variant],
            className
          )}
          {...props}
        >
          {children}
        </div>
      </CardContext.Provider>
    );
  }
);

// Sub-components
const CardHeader = forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div
      ref={ref}
      className={cn('flex flex-col gap-1.5 p-6 pb-0', className)}
      {...props}
    />
  )
);

const CardTitle = forwardRef<HTMLHeadingElement, React.HTMLAttributes<HTMLHeadingElement>>(
  ({ className, ...props }, ref) => (
    <h3
      ref={ref}
      className={cn('text-xl font-semibold leading-none tracking-tight', className)}
      {...props}
    />
  )
);

const CardDescription = forwardRef<HTMLParagraphElement, React.HTMLAttributes<HTMLParagraphElement>>(
  ({ className, ...props }, ref) => (
    <p
      ref={ref}
      className={cn('text-sm text-gray-500', className)}
      {...props}
    />
  )
);

const CardContent = forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn('p-6', className)} {...props} />
  )
);

const CardFooter = forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div
      ref={ref}
      className={cn('flex items-center p-6 pt-0', className)}
      {...props}
    />
  )
);

// Named exports
Card.displayName = 'Card';
CardHeader.displayName = 'CardHeader';
CardTitle.displayName = 'CardTitle';
CardDescription.displayName = 'CardDescription';
CardContent.displayName = 'CardContent';
CardFooter.displayName = 'CardFooter';

export { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter };
```

### Usage

```tsx
<Card variant="elevated">
  <CardHeader>
    <CardTitle>Account Settings</CardTitle>
    <CardDescription>Manage your account preferences</CardDescription>
  </CardHeader>
  <CardContent>
    <form>...</form>
  </CardContent>
  <CardFooter className="justify-between">
    <Button variant="ghost">Cancel</Button>
    <Button>Save Changes</Button>
  </CardFooter>
</Card>
```

## Data Attribute Variants

### CSS-Based State Management

```css
/* Define data attribute variants */
@custom-variant data-state-open (&[data-state="open"]);
@custom-variant data-state-closed (&[data-state="closed"]);
@custom-variant data-side-top (&[data-side="top"]);
@custom-variant data-side-bottom (&[data-side="bottom"]);
@custom-variant data-side-left (&[data-side="left"]);
@custom-variant data-side-right (&[data-side="right"]);
@custom-variant data-highlighted (&[data-highlighted]);
@custom-variant data-disabled (&[data-disabled]);
```

```tsx
// Dropdown component using data attributes
function DropdownContent({ children, ...props }) {
  return (
    <div
      data-state={isOpen ? 'open' : 'closed'}
      data-side={side}
      className="
        absolute z-50 min-w-[8rem] overflow-hidden rounded-md
        border border-gray-200 bg-white p-1 shadow-lg

        data-state-open:animate-in
        data-state-open:fade-in-0
        data-state-open:zoom-in-95

        data-state-closed:animate-out
        data-state-closed:fade-out-0
        data-state-closed:zoom-out-95

        data-side-top:slide-in-from-bottom-2
        data-side-bottom:slide-in-from-top-2
        data-side-left:slide-in-from-right-2
        data-side-right:slide-in-from-left-2
      "
      {...props}
    >
      {children}
    </div>
  );
}

function DropdownItem({ children, disabled, ...props }) {
  return (
    <div
      data-highlighted={isHighlighted || undefined}
      data-disabled={disabled || undefined}
      className="
        relative flex cursor-pointer select-none items-center
        rounded-sm px-2 py-1.5 text-sm outline-none

        data-highlighted:bg-gray-100
        data-disabled:pointer-events-none
        data-disabled:opacity-50
      "
      {...props}
    >
      {children}
    </div>
  );
}
```

## Group and Peer Patterns

### Complex State Propagation

```html
<!-- Group pattern: Parent hover affects children -->
<div class="group relative overflow-hidden rounded-xl">
  <img
    src="image.jpg"
    class="transition-transform duration-300 group-hover:scale-110"
  />
  <div class="
    absolute inset-0 bg-gradient-to-t from-black/80 to-transparent
    opacity-0 transition-opacity group-hover:opacity-100
  ">
    <div class="
      absolute bottom-0 left-0 right-0 p-6
      translate-y-4 transition-transform group-hover:translate-y-0
    ">
      <h3 class="text-xl font-bold text-white">Title</h3>
      <p class="text-gray-200">Description</p>
    </div>
  </div>
</div>

<!-- Named groups for nested components -->
<div class="group/card">
  <div class="group/header">
    <button class="group-hover/header:text-blue-500">
      Header Action
    </button>
  </div>
  <div class="group-hover/card:bg-gray-50">
    Card content
  </div>
</div>

<!-- Peer pattern: Sibling state affects elements -->
<div class="relative">
  <input
    type="email"
    class="peer w-full border rounded-lg px-4 py-2 placeholder-transparent"
    placeholder="Email"
  />
  <label class="
    absolute left-4 top-2 text-gray-500
    transition-all
    peer-placeholder-shown:top-2 peer-placeholder-shown:text-base
    peer-focus:-top-6 peer-focus:text-sm peer-focus:text-blue-500
    peer-[:not(:placeholder-shown)]:-top-6 peer-[:not(:placeholder-shown)]:text-sm
  ">
    Email address
  </label>
</div>

<!-- Peer for form validation -->
<div>
  <input
    type="email"
    class="peer"
    required
  />
  <p class="hidden text-red-500 peer-invalid:block">
    Please enter a valid email
  </p>
</div>
```

## Slot Pattern with @apply

### Reusable Component Slots

```css
@layer components {
  /* Base dialog structure */
  .dialog {
    @apply fixed inset-0 z-50 flex items-center justify-center;
  }

  .dialog-overlay {
    @apply fixed inset-0 bg-black/50 backdrop-blur-sm;
    @apply data-state-open:animate-in data-state-open:fade-in-0;
    @apply data-state-closed:animate-out data-state-closed:fade-out-0;
  }

  .dialog-content {
    @apply relative z-50 w-full max-w-lg rounded-xl bg-white p-6 shadow-xl;
    @apply data-state-open:animate-in data-state-open:fade-in-0 data-state-open:zoom-in-95;
    @apply data-state-closed:animate-out data-state-closed:fade-out-0 data-state-closed:zoom-out-95;
  }

  .dialog-header {
    @apply flex flex-col gap-1.5 text-center sm:text-left;
  }

  .dialog-title {
    @apply text-lg font-semibold leading-none tracking-tight;
  }

  .dialog-description {
    @apply text-sm text-gray-500;
  }

  .dialog-footer {
    @apply flex flex-col-reverse gap-2 sm:flex-row sm:justify-end;
  }

  .dialog-close {
    @apply absolute right-4 top-4 rounded-sm opacity-70 hover:opacity-100;
    @apply focus:outline-none focus:ring-2 focus:ring-offset-2;
  }
}
```

## Polymorphic Components

### "as" Prop Pattern

```tsx
import { forwardRef, ElementType, ComponentPropsWithoutRef } from 'react';
import { cn } from '@/lib/utils';

type PolymorphicRef<C extends ElementType> = ComponentPropsWithoutRef<C>['ref'];

type PolymorphicComponentProps<C extends ElementType, Props = {}> = Props & {
  as?: C;
  className?: string;
  children?: React.ReactNode;
} & Omit<ComponentPropsWithoutRef<C>, 'as' | 'className' | keyof Props>;

// Text component that can be any element
interface TextProps {
  size?: 'xs' | 'sm' | 'base' | 'lg' | 'xl' | '2xl';
  weight?: 'normal' | 'medium' | 'semibold' | 'bold';
  color?: 'default' | 'muted' | 'accent';
}

type TextComponent = <C extends ElementType = 'span'>(
  props: PolymorphicComponentProps<C, TextProps> & { ref?: PolymorphicRef<C> }
) => React.ReactElement | null;

export const Text: TextComponent = forwardRef(
  <C extends ElementType = 'span'>(
    {
      as,
      size = 'base',
      weight = 'normal',
      color = 'default',
      className,
      children,
      ...props
    }: PolymorphicComponentProps<C, TextProps>,
    ref?: PolymorphicRef<C>
  ) => {
    const Component = as || 'span';

    const sizes = {
      xs: 'text-xs',
      sm: 'text-sm',
      base: 'text-base',
      lg: 'text-lg',
      xl: 'text-xl',
      '2xl': 'text-2xl',
    };

    const weights = {
      normal: 'font-normal',
      medium: 'font-medium',
      semibold: 'font-semibold',
      bold: 'font-bold',
    };

    const colors = {
      default: 'text-gray-900',
      muted: 'text-gray-500',
      accent: 'text-brand-500',
    };

    return (
      <Component
        ref={ref}
        className={cn(sizes[size], weights[weight], colors[color], className)}
        {...props}
      >
        {children}
      </Component>
    );
  }
);
```

### Usage

```tsx
<Text>Default span</Text>
<Text as="p" size="lg" color="muted">Large muted paragraph</Text>
<Text as="h1" size="2xl" weight="bold">Bold heading</Text>
<Text as="a" href="/link" color="accent">Accent link</Text>
```

## Headless Component Integration

### Headless UI with Tailwind

```tsx
import { Dialog, Transition } from '@headlessui/react';
import { Fragment } from 'react';

function Modal({ isOpen, onClose, title, children }) {
  return (
    <Transition appear show={isOpen} as={Fragment}>
      <Dialog as="div" className="relative z-50" onClose={onClose}>
        {/* Backdrop */}
        <Transition.Child
          as={Fragment}
          enter="ease-out duration-300"
          enterFrom="opacity-0"
          enterTo="opacity-100"
          leave="ease-in duration-200"
          leaveFrom="opacity-100"
          leaveTo="opacity-0"
        >
          <div className="fixed inset-0 bg-black/50 backdrop-blur-sm" />
        </Transition.Child>

        <div className="fixed inset-0 overflow-y-auto">
          <div className="flex min-h-full items-center justify-center p-4">
            <Transition.Child
              as={Fragment}
              enter="ease-out duration-300"
              enterFrom="opacity-0 scale-95"
              enterTo="opacity-100 scale-100"
              leave="ease-in duration-200"
              leaveFrom="opacity-100 scale-100"
              leaveTo="opacity-0 scale-95"
            >
              <Dialog.Panel className="
                w-full max-w-md transform overflow-hidden rounded-2xl
                bg-white p-6 text-left align-middle shadow-xl transition-all
              ">
                <Dialog.Title className="text-lg font-medium leading-6 text-gray-900">
                  {title}
                </Dialog.Title>
                <div className="mt-2">
                  {children}
                </div>
              </Dialog.Panel>
            </Transition.Child>
          </div>
        </div>
      </Dialog>
    </Transition>
  );
}
```

### Radix UI with Tailwind

```tsx
import * as DropdownMenu from '@radix-ui/react-dropdown-menu';

function Dropdown() {
  return (
    <DropdownMenu.Root>
      <DropdownMenu.Trigger className="
        inline-flex items-center justify-center rounded-md
        bg-white px-4 py-2 text-sm font-medium
        border border-gray-300 hover:bg-gray-50
        focus:outline-none focus:ring-2 focus:ring-brand-500
      ">
        Options
        <ChevronDownIcon className="ml-2 h-4 w-4" />
      </DropdownMenu.Trigger>

      <DropdownMenu.Portal>
        <DropdownMenu.Content
          className="
            min-w-[200px] rounded-md bg-white p-1 shadow-lg
            border border-gray-200
            animate-in fade-in-0 zoom-in-95
            data-[side=bottom]:slide-in-from-top-2
            data-[side=top]:slide-in-from-bottom-2
          "
          sideOffset={5}
        >
          <DropdownMenu.Item className="
            relative flex cursor-pointer select-none items-center
            rounded-sm px-2 py-2 text-sm outline-none
            data-[highlighted]:bg-gray-100
          ">
            Profile
          </DropdownMenu.Item>

          <DropdownMenu.Separator className="my-1 h-px bg-gray-200" />

          <DropdownMenu.Item className="
            relative flex cursor-pointer select-none items-center
            rounded-sm px-2 py-2 text-sm text-red-600 outline-none
            data-[highlighted]:bg-red-50
          ">
            Delete
          </DropdownMenu.Item>
        </DropdownMenu.Content>
      </DropdownMenu.Portal>
    </DropdownMenu.Root>
  );
}
```

## Animation Patterns

### Staggered Animations

```tsx
function StaggeredList({ items }) {
  return (
    <ul className="space-y-2">
      {items.map((item, index) => (
        <li
          key={item.id}
          className="animate-in fade-in-0 slide-in-from-left-4"
          style={{ animationDelay: `${index * 100}ms` }}
        >
          {item.content}
        </li>
      ))}
    </ul>
  );
}
```

### Skeleton Loading

```tsx
function Skeleton({ className, ...props }) {
  return (
    <div
      className={cn(
        'animate-pulse rounded-md bg-gray-200',
        className
      )}
      {...props}
    />
  );
}

function CardSkeleton() {
  return (
    <div className="rounded-xl border border-gray-200 p-6">
      <div className="flex items-center gap-4">
        <Skeleton className="h-12 w-12 rounded-full" />
        <div className="space-y-2">
          <Skeleton className="h-4 w-[200px]" />
          <Skeleton className="h-3 w-[150px]" />
        </div>
      </div>
      <div className="mt-4 space-y-2">
        <Skeleton className="h-3 w-full" />
        <Skeleton className="h-3 w-full" />
        <Skeleton className="h-3 w-3/4" />
      </div>
    </div>
  );
}
```

## Best Practices

### 1. Use cn() Utility for Class Merging

```typescript
// lib/utils.ts
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

### 2. Extract Common Patterns

```css
@layer components {
  /* Consistent focus ring */
  .focus-ring {
    @apply focus:outline-none focus-visible:ring-2 focus-visible:ring-brand-500 focus-visible:ring-offset-2;
  }

  /* Consistent disabled state */
  .disabled-state {
    @apply disabled:pointer-events-none disabled:opacity-50;
  }

  /* Truncate text */
  .truncate-lines-2 {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
}
```

### 3. Document Component APIs

```tsx
/**
 * Button component with multiple variants
 *
 * @example
 * <Button variant="primary" size="lg">Click me</Button>
 *
 * @example
 * <Button variant="ghost" size="icon">
 *   <IconMenu />
 * </Button>
 */
export function Button({ ... }) { ... }
```

### 4. Test Component Variants

```tsx
// Button.test.tsx
describe('Button', () => {
  it('renders all variants correctly', () => {
    const variants = ['default', 'secondary', 'outline', 'ghost', 'destructive'];

    variants.forEach(variant => {
      render(<Button variant={variant}>Test</Button>);
      // Assert classes are applied correctly
    });
  });
});
```
