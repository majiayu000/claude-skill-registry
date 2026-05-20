---
name: component-library
description: Build reusable component libraries and design systems. Covers design tokens, atomic design, Storybook documentation, variant patterns, compound components, and theming. Use for creating shared UI libraries, design systems, and consistent component APIs.
---

# Component Library Development

Build scalable, documented component libraries and design systems.

## Instructions

1. **Start with design tokens** - Colors, spacing, typography as variables
2. **Use atomic design** - Atoms → Molecules → Organisms → Templates
3. **Document with Storybook** - Interactive component documentation
4. **Design flexible APIs** - Props for variants, not endless components
5. **Test components** - Visual regression and interaction testing

## Design Tokens

### Token Structure

```typescript
// tokens/colors.ts
export const colors = {
  // Primitives (raw values)
  gray: {
    50: '#f9fafb',
    100: '#f3f4f6',
    200: '#e5e7eb',
    300: '#d1d5db',
    400: '#9ca3af',
    500: '#6b7280',
    600: '#4b5563',
    700: '#374151',
    800: '#1f2937',
    900: '#111827',
  },
  blue: {
    50: '#eff6ff',
    100: '#dbeafe',
    500: '#3b82f6',
    600: '#2563eb',
    700: '#1d4ed8',
  },
  // ... more primitive colors
};

// Semantic tokens (purpose-based)
export const semanticColors = {
  text: {
    primary: colors.gray[900],
    secondary: colors.gray[600],
    disabled: colors.gray[400],
    inverse: colors.gray[50],
  },
  background: {
    default: colors.gray[50],
    paper: '#ffffff',
    subtle: colors.gray[100],
  },
  border: {
    default: colors.gray[200],
    focus: colors.blue[500],
  },
  action: {
    primary: colors.blue[600],
    primaryHover: colors.blue[700],
    danger: colors.red[600],
    dangerHover: colors.red[700],
  },
};
```

### Spacing & Typography Tokens

```typescript
// tokens/spacing.ts
export const spacing = {
  px: '1px',
  0.5: '0.125rem',  // 2px
  1: '0.25rem',     // 4px
  2: '0.5rem',      // 8px
  3: '0.75rem',     // 12px
  4: '1rem',        // 16px
  5: '1.25rem',     // 20px
  6: '1.5rem',      // 24px
  8: '2rem',        // 32px
  10: '2.5rem',     // 40px
  12: '3rem',       // 48px
  16: '4rem',       // 64px
};

// tokens/typography.ts
export const typography = {
  fontFamily: {
    sans: ['Inter', 'system-ui', 'sans-serif'],
    mono: ['JetBrains Mono', 'monospace'],
  },
  fontSize: {
    xs: ['0.75rem', { lineHeight: '1rem' }],
    sm: ['0.875rem', { lineHeight: '1.25rem' }],
    base: ['1rem', { lineHeight: '1.5rem' }],
    lg: ['1.125rem', { lineHeight: '1.75rem' }],
    xl: ['1.25rem', { lineHeight: '1.75rem' }],
    '2xl': ['1.5rem', { lineHeight: '2rem' }],
    '3xl': ['1.875rem', { lineHeight: '2.25rem' }],
    '4xl': ['2.25rem', { lineHeight: '2.5rem' }],
  },
  fontWeight: {
    normal: '400',
    medium: '500',
    semibold: '600',
    bold: '700',
  },
};
```

### CSS Variables Integration

```typescript
// tokens/css-variables.ts
export function generateCSSVariables(tokens: Tokens): string {
  return `
    :root {
      /* Colors */
      --color-primary: ${tokens.colors.action.primary};
      --color-primary-hover: ${tokens.colors.action.primaryHover};
      --color-text-primary: ${tokens.colors.text.primary};
      --color-text-secondary: ${tokens.colors.text.secondary};
      --color-background: ${tokens.colors.background.default};
      --color-border: ${tokens.colors.border.default};

      /* Spacing */
      --space-1: ${tokens.spacing[1]};
      --space-2: ${tokens.spacing[2]};
      --space-4: ${tokens.spacing[4]};
      --space-6: ${tokens.spacing[6]};
      --space-8: ${tokens.spacing[8]};

      /* Border radius */
      --radius-sm: 0.25rem;
      --radius-md: 0.5rem;
      --radius-lg: 0.75rem;
      --radius-full: 9999px;
    }

    .dark {
      --color-text-primary: ${tokens.colors.gray[100]};
      --color-background: ${tokens.colors.gray[900]};
      --color-border: ${tokens.colors.gray[700]};
    }
  `;
}
```

## Component Patterns

### Variant-Based Components (CVA)

```typescript
// Using class-variance-authority
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const buttonVariants = cva(
  // Base styles
  'inline-flex items-center justify-center rounded-lg font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50',
  {
    variants: {
      variant: {
        primary: 'bg-blue-600 text-white hover:bg-blue-700 focus-visible:ring-blue-500',
        secondary: 'bg-gray-100 text-gray-900 hover:bg-gray-200 focus-visible:ring-gray-500',
        outline: 'border border-gray-300 bg-transparent hover:bg-gray-100 focus-visible:ring-gray-500',
        ghost: 'hover:bg-gray-100 focus-visible:ring-gray-500',
        danger: 'bg-red-600 text-white hover:bg-red-700 focus-visible:ring-red-500',
      },
      size: {
        sm: 'h-8 px-3 text-sm',
        md: 'h-10 px-4 text-sm',
        lg: 'h-12 px-6 text-base',
        icon: 'h-10 w-10',
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
      {loading && <Spinner className="mr-2 h-4 w-4" />}
      {children}
    </button>
  );
}
```

### Compound Components

```typescript
import { createContext, useContext, useState, ReactNode } from 'react';

// Context for compound component
interface TabsContextType {
  activeTab: string;
  setActiveTab: (id: string) => void;
}

const TabsContext = createContext<TabsContextType | null>(null);

function useTabs() {
  const context = useContext(TabsContext);
  if (!context) {
    throw new Error('Tabs components must be used within Tabs');
  }
  return context;
}

// Root component
interface TabsProps {
  defaultValue: string;
  children: ReactNode;
  className?: string;
}

export function Tabs({ defaultValue, children, className }: TabsProps) {
  const [activeTab, setActiveTab] = useState(defaultValue);

  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      <div className={className}>{children}</div>
    </TabsContext.Provider>
  );
}

// Tab list
Tabs.List = function TabsList({ children, className }: { children: ReactNode; className?: string }) {
  return (
    <div role="tablist" className={cn('flex border-b', className)}>
      {children}
    </div>
  );
};

// Individual tab trigger
Tabs.Trigger = function TabsTrigger({
  value,
  children,
  className,
}: {
  value: string;
  children: ReactNode;
  className?: string;
}) {
  const { activeTab, setActiveTab } = useTabs();
  const isActive = activeTab === value;

  return (
    <button
      role="tab"
      aria-selected={isActive}
      onClick={() => setActiveTab(value)}
      className={cn(
        'px-4 py-2 text-sm font-medium transition-colors',
        isActive
          ? 'border-b-2 border-blue-600 text-blue-600'
          : 'text-gray-500 hover:text-gray-700',
        className
      )}
    >
      {children}
    </button>
  );
};

// Tab content panel
Tabs.Content = function TabsContent({
  value,
  children,
  className,
}: {
  value: string;
  children: ReactNode;
  className?: string;
}) {
  const { activeTab } = useTabs();

  if (activeTab !== value) return null;

  return (
    <div role="tabpanel" className={cn('py-4', className)}>
      {children}
    </div>
  );
};

// Usage
<Tabs defaultValue="tab1">
  <Tabs.List>
    <Tabs.Trigger value="tab1">Overview</Tabs.Trigger>
    <Tabs.Trigger value="tab2">Details</Tabs.Trigger>
    <Tabs.Trigger value="tab3">Settings</Tabs.Trigger>
  </Tabs.List>
  <Tabs.Content value="tab1">Overview content</Tabs.Content>
  <Tabs.Content value="tab2">Details content</Tabs.Content>
  <Tabs.Content value="tab3">Settings content</Tabs.Content>
</Tabs>
```

### Polymorphic Components

```typescript
import { ElementType, ComponentPropsWithoutRef, ReactNode } from 'react';

type BoxProps<T extends ElementType> = {
  as?: T;
  children?: ReactNode;
} & ComponentPropsWithoutRef<T>;

export function Box<T extends ElementType = 'div'>({
  as,
  children,
  ...props
}: BoxProps<T>) {
  const Component = as || 'div';
  return <Component {...props}>{children}</Component>;
}

// Usage
<Box as="section" className="p-4">Section content</Box>
<Box as="article" className="prose">Article content</Box>
<Box as="a" href="/about">Link</Box>
```

## Storybook Documentation

### Story Structure

```typescript
// Button.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { Button } from './Button';

const meta: Meta<typeof Button> = {
  title: 'Components/Button',
  component: Button,
  tags: ['autodocs'],
  argTypes: {
    variant: {
      control: 'select',
      options: ['primary', 'secondary', 'outline', 'ghost', 'danger'],
      description: 'The visual style of the button',
    },
    size: {
      control: 'radio',
      options: ['sm', 'md', 'lg'],
    },
    loading: {
      control: 'boolean',
    },
    disabled: {
      control: 'boolean',
    },
  },
};

export default meta;
type Story = StoryObj<typeof Button>;

export const Primary: Story = {
  args: {
    children: 'Primary Button',
    variant: 'primary',
  },
};

export const Secondary: Story = {
  args: {
    children: 'Secondary Button',
    variant: 'secondary',
  },
};

export const AllVariants: Story = {
  render: () => (
    <div className="flex flex-wrap gap-4">
      <Button variant="primary">Primary</Button>
      <Button variant="secondary">Secondary</Button>
      <Button variant="outline">Outline</Button>
      <Button variant="ghost">Ghost</Button>
      <Button variant="danger">Danger</Button>
    </div>
  ),
};

export const Sizes: Story = {
  render: () => (
    <div className="flex items-center gap-4">
      <Button size="sm">Small</Button>
      <Button size="md">Medium</Button>
      <Button size="lg">Large</Button>
    </div>
  ),
};

export const Loading: Story = {
  args: {
    children: 'Loading...',
    loading: true,
  },
};
```

### Documentation Page

```mdx
{/* Button.mdx */}
import { Meta, Story, Canvas, Controls } from '@storybook/blocks';
import * as ButtonStories from './Button.stories';

<Meta of={ButtonStories} />

# Button

Buttons trigger actions or navigation. Use the appropriate variant
for the action's importance and context.

## Usage Guidelines

- Use **Primary** for the main action on a page
- Use **Secondary** for less important actions
- Use **Danger** only for destructive actions
- Limit to one primary button per section

<Canvas of={ButtonStories.Primary} />

## Props

<Controls />

## Variants

<Canvas of={ButtonStories.AllVariants} />

## Sizes

<Canvas of={ButtonStories.Sizes} />

## Accessibility

- Buttons have proper focus states
- Loading state disables interaction and shows spinner
- Use `aria-label` for icon-only buttons
```

## Component Testing

### Visual Testing

```typescript
// Button.test.tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Button } from './Button';

describe('Button', () => {
  it('renders with children', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByRole('button', { name: 'Click me' })).toBeInTheDocument();
  });

  it('calls onClick when clicked', async () => {
    const onClick = vi.fn();
    render(<Button onClick={onClick}>Click me</Button>);

    await userEvent.click(screen.getByRole('button'));
    expect(onClick).toHaveBeenCalledTimes(1);
  });

  it('does not call onClick when disabled', async () => {
    const onClick = vi.fn();
    render(<Button onClick={onClick} disabled>Click me</Button>);

    await userEvent.click(screen.getByRole('button'));
    expect(onClick).not.toHaveBeenCalled();
  });

  it('shows loading spinner', () => {
    render(<Button loading>Submit</Button>);
    expect(screen.getByRole('button')).toHaveAttribute('disabled');
  });

  it('applies variant classes', () => {
    const { rerender } = render(<Button variant="primary">Button</Button>);
    expect(screen.getByRole('button')).toHaveClass('bg-blue-600');

    rerender(<Button variant="danger">Button</Button>);
    expect(screen.getByRole('button')).toHaveClass('bg-red-600');
  });
});
```

## Package Structure

```
my-component-library/
├── src/
│   ├── components/
│   │   ├── Button/
│   │   │   ├── Button.tsx
│   │   │   ├── Button.test.tsx
│   │   │   ├── Button.stories.tsx
│   │   │   └── index.ts
│   │   ├── Input/
│   │   ├── Card/
│   │   └── index.ts
│   ├── tokens/
│   │   ├── colors.ts
│   │   ├── spacing.ts
│   │   ├── typography.ts
│   │   └── index.ts
│   ├── hooks/
│   │   └── index.ts
│   ├── utils/
│   │   ├── cn.ts
│   │   └── index.ts
│   └── index.ts
├── .storybook/
├── package.json
└── tsconfig.json
```

## Best Practices

1. **Single responsibility** - One component, one job
2. **Composition over inheritance** - Compose small components
3. **Prop drilling limits** - Max 3 levels, then use context
4. **Forward refs** - Allow parent access to DOM
5. **Semantic versioning** - Breaking changes = major version
6. **Changelog** - Document all changes

## When to Use

- Building shared UI libraries
- Creating design systems
- Standardizing UI across teams
- Open-source component packages
- Enterprise design consistency

## Notes

- Use Radix or Headless UI for accessible primitives
- Consider tree-shaking for bundle size
- Test across browsers and screen sizes
- Document accessibility requirements
