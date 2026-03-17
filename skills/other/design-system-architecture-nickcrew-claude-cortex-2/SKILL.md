---
name: design-system-architecture
description: Build scalable design systems with design tokens, component APIs, and documentation. Use when creating or evolving component libraries.
keywords:
  - design system
  - design tokens
  - component library
  - ui components
  - theming
triggers:
  - design system
  - component library
  - design tokens
  - theme architecture
  - ui kit
---

# Design System Architecture

Comprehensive guide to building scalable design systems with proper token architecture, component APIs, and documentation strategies.

## When to Use This Skill

- Creating a new design system from scratch
- Evolving an existing component library
- Defining token architecture
- Establishing component API patterns
- Setting up design system documentation

## Token Architecture

### Three-Tier Token System

```
┌─────────────────────────────────────┐
│       Component Tokens              │  → button-primary-bg
│     (Specific to components)        │
├─────────────────────────────────────┤
│       Semantic Tokens               │  → color-action-primary
│     (Purpose-based naming)          │
├─────────────────────────────────────┤
│       Primitive Tokens              │  → blue-500
│     (Raw values)                    │
└─────────────────────────────────────┘
```

### Token Categories

```css
/* Primitive Tokens */
--color-blue-500: #3b82f6;
--spacing-4: 1rem;
--font-size-base: 16px;
--radius-md: 8px;

/* Semantic Tokens */
--color-action-primary: var(--color-blue-500);
--color-text-primary: var(--color-gray-900);
--spacing-component-gap: var(--spacing-4);

/* Component Tokens */
--button-bg: var(--color-action-primary);
--button-padding-x: var(--spacing-4);
--card-radius: var(--radius-md);
```

### Theme Support

```typescript
// tokens/themes.ts
export const lightTheme = {
  'color-bg-primary': 'var(--color-white)',
  'color-text-primary': 'var(--color-gray-900)',
  'color-border': 'var(--color-gray-200)',
}

export const darkTheme = {
  'color-bg-primary': 'var(--color-gray-900)',
  'color-text-primary': 'var(--color-gray-100)',
  'color-border': 'var(--color-gray-700)',
}
```

## Component API Patterns

### Prop API Design

```typescript
// ✅ Good: Clear, typed, with sensible defaults
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
  isDisabled?: boolean;
  leftIcon?: React.ReactNode;
  children: React.ReactNode;
  onClick?: () => void;
}

// ✅ With defaults
const Button = ({
  variant = 'primary',
  size = 'md',
  isLoading = false,
  isDisabled = false,
  ...props
}: ButtonProps) => { ... }
```

### Compound Component Pattern

```typescript
// Compound components for complex UIs
const Tabs = ({ children, defaultValue }) => { ... }
Tabs.List = ({ children }) => { ... }
Tabs.Tab = ({ value, children }) => { ... }
Tabs.Panel = ({ value, children }) => { ... }

// Usage
<Tabs defaultValue="tab1">
  <Tabs.List>
    <Tabs.Tab value="tab1">First</Tabs.Tab>
    <Tabs.Tab value="tab2">Second</Tabs.Tab>
  </Tabs.List>
  <Tabs.Panel value="tab1">Content 1</Tabs.Panel>
  <Tabs.Panel value="tab2">Content 2</Tabs.Panel>
</Tabs>
```

### Polymorphic Components

```typescript
// Component that can render as different elements
interface BoxProps<C extends React.ElementType> {
  as?: C;
  children?: React.ReactNode;
}

type PolymorphicProps<C extends React.ElementType> =
  BoxProps<C> & Omit<React.ComponentPropsWithoutRef<C>, keyof BoxProps<C>>;

const Box = <C extends React.ElementType = 'div'>({
  as,
  ...props
}: PolymorphicProps<C>) => {
  const Component = as || 'div';
  return <Component {...props} />;
};

// Usage
<Box as="section" className="...">Content</Box>
<Box as="button" onClick={...}>Click me</Box>
```

## Component Categories (Atomic Design)

### Atoms (Primitives)
- Button, Input, Label, Icon
- Typography (Text, Heading)
- Box, Flex, Grid (layout primitives)

### Molecules (Compositions)
- FormField (Label + Input + Error)
- SearchInput (Input + Icon + Button)
- Card (Box + padding + border)

### Organisms (Features)
- Header (Logo + Nav + UserMenu)
- DataTable (Table + Pagination + Filters)
- Modal (Overlay + Card + Actions)

## Documentation Strategy

### Component Documentation

```markdown
# Button

Buttons trigger actions or navigate users.

## Usage

\`\`\`jsx
import { Button } from '@/components/ui'

<Button variant="primary" size="md">
  Click me
</Button>
\`\`\`

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| variant | 'primary' \| 'secondary' \| 'ghost' | 'primary' | Visual style |
| size | 'sm' \| 'md' \| 'lg' | 'md' | Size preset |

## Examples

### Variants
[Interactive examples]

### With Icons
[Interactive examples]

## Accessibility

- Uses `<button>` element by default
- Supports keyboard activation
- Loading state announced to screen readers
```

## Best Practices

### Design Principles
1. **Composition over configuration**: Small, composable pieces
2. **Sensible defaults**: Works out of the box
3. **Accessible by default**: a11y is not optional
4. **Type-safe APIs**: TypeScript guides usage
5. **Minimal API surface**: Only expose what's needed

### Maintenance
- Semantic versioning for breaking changes
- Deprecation warnings before removal
- Migration guides for major versions
- Automated visual regression testing

## Resources

- [Radix UI Primitives](https://www.radix-ui.com/)
- [Chakra UI Component Patterns](https://chakra-ui.com/)
- [Design Tokens Community Group](https://www.w3.org/community/design-tokens/)
