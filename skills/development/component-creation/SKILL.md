---
name: component-creation
description: Comprehensive guide for creating React components in the squared package and squareone app. Use this skill when creating new components, setting up component structure, implementing CSS Modules styling, writing Storybook stories, or setting up component tests. Covers TypeScript patterns (type vs interface, no React.FC), CSS Modules with design tokens, compound component patterns, Storybook integration, and vitest testing.
---

# Component Creation Guide

> **Tip**: Use the **file-factory** CLI to scaffold new components: `pnpm file-factory component <name> --package <package>`. This creates the correct directory structure with all files (component, styles, tests, stories, index). Then follow the patterns in this guide for implementation.

## Component Structure

```
MyComponent/
├── MyComponent.tsx         # Component implementation
├── MyComponent.module.css  # Styles
├── MyComponent.stories.tsx # Storybook stories
├── MyComponent.test.tsx    # Tests
└── index.ts                # Exports
```

## TypeScript Patterns

### Prefer `type` over `interface`

```typescript
// ✅ Good
type MyComponentProps = {
  title: string;
  onClick?: () => void;
  variant?: 'primary' | 'secondary';
};

// ❌ Avoid
interface MyComponentProps {
  title: string;
}
```

### Avoid `React.FC`

```typescript
// ✅ Good - type props directly
export default function MyComponent({ title }: MyComponentProps) {
  return <div>{title}</div>;
}

// ❌ Avoid
const MyComponent: React.FC<MyComponentProps> = ({ title }) => {
  return <div>{title}</div>;
};
```

### Component Type Pattern

```typescript
import styles from './MyComponent.module.css';

type MyComponentProps = {
  /** Description for docs */
  title: string;
  /** Optional variant */
  variant?: 'primary' | 'secondary';
  /** Optional click handler */
  onClick?: () => void;
  /** Children elements */
  children?: React.ReactNode;
};

/**
 * MyComponent does X and Y.
 *
 * Use this component when...
 */
export default function MyComponent({
  title,
  variant = 'primary',
  onClick,
  children,
}: MyComponentProps) {
  return (
    <div className={styles.container} data-variant={variant} onClick={onClick}>
      <h2 className={styles.title}>{title}</h2>
      {children}
    </div>
  );
}
```

## CSS Modules with Design Tokens

### Basic Pattern

```css
/* MyComponent.module.css */
.container {
  padding: var(--sqo-space-md);
  background-color: var(--rsd-color-primary-600);
  border-radius: var(--sqo-border-radius-1);
  box-shadow: var(--sqo-elevation-md);
}

.title {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--rsd-component-text-color);
  margin-bottom: var(--sqo-space-sm);
}
```

### Variants with Data Attributes

```css
.container[data-variant='primary'] {
  background-color: var(--rsd-color-primary-600);
  color: var(--rsd-component-text-reverse-color);
}

.container[data-variant='secondary'] {
  background-color: var(--rsd-color-blue-600);
  color: var(--rsd-component-text-reverse-color);
}
```

### Available Design Tokens

See the **design-system** skill for complete CSS variable reference.

**Most commonly used:**
- **Spacing**: `--sqo-space-{xxxs,xxs,xs,sm,md,lg,xl,xxl,xxxl}` (responsive) or `--sqo-space-*-fixed` (fixed)
- **Colors**: `--rsd-color-{primary,blue,green,red,orange,yellow,purple,gray}-{100-800}`
- **Semantic colors**: `--rsd-component-text-color`, `--rsd-component-text-link-color`, etc.
- **Border radius**: `--sqo-border-radius-{0,1,2}`
- **Elevations**: `--sqo-elevation-{0,xs,sm,base,md,lg,xl,2xl,inner,outline}`
- **Transitions**: `--sqo-transition-basic`

**Key sources:**
- `packages/rubin-style-dictionary/dist/tokens.css` - Foundation tokens (prefix: `--rsd-*`)
- `packages/global-css/src/tokens.css` - Application tokens (prefix: `--sqo-*`)

## Export Pattern

```typescript
// MyComponent/index.ts
export { default } from './MyComponent';
export type { MyComponentProps } from './MyComponent';

// src/index.ts (add to main exports)
export { default as MyComponent } from './components/MyComponent';
export type { MyComponentProps } from './components/MyComponent';
```

## Story book Stories

```typescript
// MyComponent.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import MyComponent from './MyComponent';

const meta: Meta<typeof MyComponent> = {
  title: 'Components/MyComponent',
  component: MyComponent,
  tags: ['autodocs', 'test'],
  argTypes: {
    variant: {
      control: 'select',
      options: ['primary', 'secondary'],
    },
  },
};

export default meta;
type Story = StoryObj<typeof MyComponent>;

export const Primary: Story = {
  args: {
    title: 'Primary Component',
    variant: 'primary',
  },
};

export const Secondary: Story = {
  args: {
    title: 'Secondary Component',
    variant: 'secondary',
  },
};

export const WithChildren: Story = {
  args: {
    title: 'With Children',
    children: <p>Child content</p>,
  },
};
```

### Story Tests

```typescript
import { expect, within } from '@storybook/test';

export const WithTest: Story = {
  args: {
    title: 'Test Title',
  },
  tags: ['test'],
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    await expect(canvas.getByText('Test Title')).toBeInTheDocument();
  },
};
```

## Component Tests

```typescript
// MyComponent.test.tsx
import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import MyComponent from './MyComponent';

describe('MyComponent', () => {
  it('renders with title', () => {
    render(<MyComponent title="Test" />);
    expect(screen.getByText('Test')).toBeInTheDocument();
  });

  it('calls onClick when clicked', async () => {
    const handleClick = vi.fn();
    render(<MyComponent title="Test" onClick={handleClick} />);

    await userEvent.click(screen.getByText('Test'));
    expect(handleClick).toHaveBeenCalledOnce();
  });

  it('renders with variant', () => {
    const { container } = render(<MyComponent title="Test" variant="secondary" />);
    expect(container.firstChild).toHaveAttribute('data-variant', 'secondary');
  });
});
```

## Compound Components

```typescript
// Card.tsx
import styles from './Card.module.css';

type CardProps = {
  children: React.ReactNode;
};

export default function Card({ children }: CardProps) {
  return <div className={styles.card}>{children}</div>;
}

type CardHeaderProps = {
  children: React.ReactNode;
};

function CardHeader({ children }: CardHeaderProps) {
  return <div className={styles.header}>{children}</div>;
}

type CardBodyProps = {
  children: React.ReactNode;
};

function CardBody({ children }: CardBodyProps) {
  return <div className={styles.body}>{children}</div>;
}

// Attach sub-components
Card.Header = CardHeader;
Card.Body = CardBody;
```

Usage:
```typescript
<Card>
  <Card.Header>Title</Card.Header>
  <Card.Body>Content</Card.Body>
</Card>
```

## Import Conventions

```typescript
// External libraries first
import React from 'react';
import { useState } from 'react';

// Internal packages
import { Button } from '@lsst-sqre/squared';

// Relative imports
import styles from './MyComponent.module.css';
import SubComponent from './SubComponent';
```

## Accessibility

Use Radix UI primitives for accessible components:

```typescript
import * as Dialog from '@radix-ui/react-dialog';
import styles from './MyDialog.module.css';

export default function MyDialog({ children }) {
  return (
    <Dialog.Root>
      <Dialog.Trigger className={styles.trigger}>Open</Dialog.Trigger>
      <Dialog.Portal>
        <Dialog.Overlay className={styles.overlay} />
        <Dialog.Content className={styles.content}>
          {children}
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
```

## Common Patterns

### Forwarding Refs

```typescript
import { forwardRef } from 'react';

type InputProps = {
  label: string;
} & React.InputHTMLAttributes<HTMLInputElement>;

const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ label, ...props }, ref) => {
    return (
      <div className={styles.container}>
        <label className={styles.label}>{label}</label>
        <input ref={ref} className={styles.input} {...props} />
      </div>
    );
  }
);

Input.displayName = 'Input';
export default Input;
```

### Conditional Rendering

```typescript
export default function MyComponent({ showExtra, data }: Props) {
  if (!data) {
    return <div className={styles.empty}>No data</div>;
  }

  return (
    <div className={styles.container}>
      <div className={styles.content}>{data.content}</div>
      {showExtra && <div className={styles.extra}>Extra content</div>}
    </div>
  );
}
```

## Best Practices

1. **JSDoc comments** for component and props
2. **Default values** for optional props
3. **Semantic HTML** elements
4. **Accessible** markup and ARIA attributes
5. **Responsive** styles with media queries
6. **Design tokens** for all values (see **design-system** skill for complete reference)
7. **Tests** for key behaviors
8. **Stories** for all variants
9. **Compound components** for related UI
10. **TypeScript strict mode** compliant

## Related Skills

- **file-factory** - Use `pnpm file-factory component <name>` to scaffold new components with the correct structure before implementing
- **design-system** - Complete CSS variable and design token reference
- **squared-package** - Understanding NO BUILD STEP architecture for squared components
- **testing-infrastructure** - Writing tests for components
