---
name: panda-css
description: Implements build-time CSS-in-JS with Panda CSS using type-safe tokens, recipes, and patterns. Use when wanting zero-runtime CSS-in-JS, design system tokens, or type-safe component variants.
---

# Panda CSS

Build-time, type-safe CSS-in-JS framework with zero runtime.

## Quick Start

**Install:**
```bash
npm install -D @pandacss/dev
npx panda init --postcss
```

**Configure:**
```typescript
// panda.config.ts
import { defineConfig } from '@pandacss/dev';

export default defineConfig({
  preflight: true,
  include: ['./src/**/*.{js,jsx,ts,tsx}'],
  exclude: [],
  outdir: 'styled-system',
});
```

**Use in component:**
```tsx
import { css } from '../styled-system/css';

function Button({ children }: { children: React.ReactNode }) {
  return (
    <button className={css({
      padding: '12px 24px',
      borderRadius: 'md',
      bg: 'blue.500',
      color: 'white',
      cursor: 'pointer',
      _hover: { bg: 'blue.600' },
    })}>
      {children}
    </button>
  );
}
```

## CSS Function

### Basic Usage

```tsx
import { css } from '../styled-system/css';

const styles = css({
  display: 'flex',
  alignItems: 'center',
  gap: '4',
  padding: '4',
  bg: 'gray.100',
  borderRadius: 'lg',
});

<div className={styles}>Content</div>
```

### Pseudo Selectors

```tsx
const buttonStyles = css({
  bg: 'blue.500',
  color: 'white',
  _hover: {
    bg: 'blue.600',
  },
  _active: {
    bg: 'blue.700',
  },
  _disabled: {
    opacity: '0.5',
    cursor: 'not-allowed',
  },
  _focus: {
    outline: '2px solid',
    outlineColor: 'blue.300',
    outlineOffset: '2px',
  },
});
```

### Responsive Styles

```tsx
const containerStyles = css({
  padding: { base: '4', md: '6', lg: '8' },
  display: { base: 'block', md: 'flex' },
  flexDirection: { md: 'row' },
  gap: { md: '4', lg: '6' },
});
```

### Conditional Styles

```tsx
function Card({ elevated }: { elevated?: boolean }) {
  return (
    <div className={css({
      padding: '4',
      borderRadius: 'lg',
      bg: 'white',
      boxShadow: elevated ? 'lg' : 'sm',
    })}>
      Content
    </div>
  );
}
```

## Design Tokens

### Define in Config

```typescript
// panda.config.ts
import { defineConfig } from '@pandacss/dev';

export default defineConfig({
  theme: {
    extend: {
      tokens: {
        colors: {
          primary: { value: '#3b82f6' },
          secondary: { value: '#6b7280' },
        },
        spacing: {
          '4.5': { value: '1.125rem' },
        },
        radii: {
          button: { value: '8px' },
        },
      },
      semanticTokens: {
        colors: {
          text: {
            value: { base: '{colors.gray.900}', _dark: '{colors.gray.100}' },
          },
          bg: {
            value: { base: '{colors.white}', _dark: '{colors.gray.900}' },
          },
          accent: {
            value: { base: '{colors.primary}', _dark: '{colors.blue.400}' },
          },
        },
      },
    },
  },
});
```

### Use Tokens

```tsx
const styles = css({
  color: 'text',
  bg: 'bg',
  borderColor: 'accent',
  padding: '4.5',
  borderRadius: 'button',
});
```

## Recipes

### Basic Recipe

```typescript
// button.recipe.ts
import { cva } from '../styled-system/css';

export const button = cva({
  base: {
    display: 'inline-flex',
    alignItems: 'center',
    justifyContent: 'center',
    borderRadius: 'md',
    fontWeight: 'semibold',
    cursor: 'pointer',
    transition: 'all 0.2s',
  },
  variants: {
    variant: {
      solid: {
        bg: 'blue.500',
        color: 'white',
        _hover: { bg: 'blue.600' },
      },
      outline: {
        border: '2px solid',
        borderColor: 'blue.500',
        color: 'blue.500',
        _hover: { bg: 'blue.50' },
      },
      ghost: {
        color: 'blue.500',
        _hover: { bg: 'blue.50' },
      },
    },
    size: {
      sm: { px: '3', py: '1.5', fontSize: 'sm' },
      md: { px: '4', py: '2', fontSize: 'md' },
      lg: { px: '6', py: '3', fontSize: 'lg' },
    },
  },
  defaultVariants: {
    variant: 'solid',
    size: 'md',
  },
});
```

### Use Recipe

```tsx
import { button } from './button.recipe';

function Button({ variant, size, children }: ButtonProps) {
  return (
    <button className={button({ variant, size })}>
      {children}
    </button>
  );
}

// Usage
<Button variant="outline" size="lg">Click me</Button>
```

### Compound Variants

```typescript
const button = cva({
  base: { /* ... */ },
  variants: {
    variant: {
      solid: { /* ... */ },
      outline: { /* ... */ },
    },
    size: {
      sm: { /* ... */ },
      lg: { /* ... */ },
    },
  },
  compoundVariants: [
    {
      variant: 'solid',
      size: 'lg',
      css: {
        boxShadow: 'lg',
      },
    },
  ],
});
```

## Patterns

Built-in layout patterns:

```tsx
import { stack, hstack, vstack, center, container } from '../styled-system/patterns';

// Vertical stack
<div className={stack({ gap: '4', direction: 'column' })}>
  <div>Item 1</div>
  <div>Item 2</div>
</div>

// Horizontal stack
<div className={hstack({ gap: '4' })}>
  <div>Left</div>
  <div>Right</div>
</div>

// Center content
<div className={center({ h: 'screen' })}>
  <div>Centered</div>
</div>

// Container
<div className={container({ maxW: '4xl', px: '4' })}>
  Content
</div>
```

### Custom Patterns

```typescript
// panda.config.ts
export default defineConfig({
  patterns: {
    extend: {
      card: {
        properties: {
          elevated: { type: 'boolean' },
        },
        transform(props) {
          const { elevated, ...rest } = props;
          return {
            padding: '4',
            borderRadius: 'lg',
            bg: 'white',
            boxShadow: elevated ? 'lg' : 'sm',
            ...rest,
          };
        },
      },
    },
  },
});

// Usage
import { card } from '../styled-system/patterns';

<div className={card({ elevated: true })}>
  Card content
</div>
```

## Slot Recipes

For multi-part components:

```typescript
import { sva } from '../styled-system/css';

const card = sva({
  slots: ['root', 'header', 'body', 'footer'],
  base: {
    root: {
      borderRadius: 'lg',
      overflow: 'hidden',
      bg: 'white',
      boxShadow: 'md',
    },
    header: {
      p: '4',
      borderBottom: '1px solid',
      borderColor: 'gray.200',
    },
    body: {
      p: '4',
    },
    footer: {
      p: '4',
      borderTop: '1px solid',
      borderColor: 'gray.200',
      bg: 'gray.50',
    },
  },
  variants: {
    size: {
      sm: {
        root: { maxW: 'sm' },
        header: { p: '3' },
        body: { p: '3' },
      },
      lg: {
        root: { maxW: 'lg' },
        header: { p: '6' },
        body: { p: '6' },
      },
    },
  },
});

// Usage
function Card({ size, children }: CardProps) {
  const styles = card({ size });

  return (
    <div className={styles.root}>
      <div className={styles.header}>Title</div>
      <div className={styles.body}>{children}</div>
      <div className={styles.footer}>Actions</div>
    </div>
  );
}
```

## JSX Style Props

Enable styled components syntax:

```typescript
// panda.config.ts
export default defineConfig({
  jsxFramework: 'react',
  // ...
});
```

```tsx
import { styled } from '../styled-system/jsx';

const Button = styled('button', {
  base: {
    px: '4',
    py: '2',
    borderRadius: 'md',
  },
  variants: {
    variant: {
      primary: { bg: 'blue.500', color: 'white' },
      secondary: { bg: 'gray.200', color: 'gray.800' },
    },
  },
});

// Usage
<Button variant="primary">Click me</Button>

// Or with Box
import { Box, Flex, Stack } from '../styled-system/jsx';

<Box p="4" bg="gray.100" borderRadius="lg">
  <Flex gap="4" alignItems="center">
    <Stack gap="2">
      <Text>Hello</Text>
    </Stack>
  </Flex>
</Box>
```

## Config Recipes

Define recipes in config:

```typescript
// panda.config.ts
export default defineConfig({
  theme: {
    extend: {
      recipes: {
        button: {
          className: 'button',
          base: {
            display: 'inline-flex',
            fontWeight: 'semibold',
          },
          variants: {
            size: {
              sm: { px: '3', py: '1' },
              md: { px: '4', py: '2' },
            },
          },
        },
      },
    },
  },
});
```

## Best Practices

1. **Use semantic tokens** - Map raw values to semantic names
2. **Define recipes** - Create reusable component styles
3. **Leverage patterns** - Use built-in layout primitives
4. **Type safety** - Let TypeScript catch style errors
5. **Organize tokens** - Group by purpose (colors, spacing)

## Reference Files

- [references/tokens.md](references/tokens.md) - Token system
- [references/recipes.md](references/recipes.md) - Recipe patterns
