---
name: ink-component-patterns
description: Use when building terminal UIs with Ink component patterns for React-based CLI applications.
allowed-tools: []
---

# Ink Component Patterns

You are an expert in building terminal UIs with Ink, React for the terminal.

## Core Principles

- Use functional components with TypeScript for type safety
- Leverage Ink's built-in components (Box, Text, Newline, Spacer)
- Keep components focused and composable
- Use proper prop types and interfaces
- Handle terminal resizing gracefully

## Component Structure

### Basic Component

```tsx
import { Box, Text } from 'ink';
import React from 'react';

interface MyComponentProps {
  title: string;
  items: string[];
}

export const MyComponent: React.FC<MyComponentProps> = ({ title, items }) => {
  return (
    <Box flexDirection="column">
      <Text bold color="cyan">
        {title}
      </Text>
      {items.map((item, index) => (
        <Box key={index} marginLeft={2}>
          <Text>• {item}</Text>
        </Box>
      ))}
    </Box>
  );
};
```

### Layout Patterns

#### Vertical Stack

```tsx
<Box flexDirection="column">
  <Text>First item</Text>
  <Text>Second item</Text>
</Box>
```

#### Horizontal Row

```tsx
<Box>
  <Text>Left</Text>
  <Spacer />
  <Text>Right</Text>
</Box>
```

#### Centered Content

```tsx
<Box justifyContent="center" alignItems="center" height={10}>
  <Text>Centered content</Text>
</Box>
```

#### Padded Container

```tsx
<Box padding={1} borderStyle="round" borderColor="cyan">
  <Text>Content with border and padding</Text>
</Box>
```

## Common Patterns

### List with Icons

```tsx
interface ListItem {
  icon: string;
  label: string;
  value: string;
}

const List: React.FC<{ items: ListItem[] }> = ({ items }) => (
  <Box flexDirection="column">
    {items.map((item, i) => (
      <Box key={i}>
        <Text color="yellow">{item.icon} </Text>
        <Text bold>{item.label}: </Text>
        <Text>{item.value}</Text>
      </Box>
    ))}
  </Box>
);
```

### Status Messages

```tsx
const StatusMessage: React.FC<{ type: 'success' | 'error' | 'warning'; message: string }> = ({
  type,
  message,
}) => {
  const config = {
    success: { icon: '✅', color: 'green' },
    error: { icon: '❌', color: 'red' },
    warning: { icon: '⚠️', color: 'yellow' },
  };

  const { icon, color } = config[type];

  return (
    <Box>
      <Text color={color}>
        {icon} {message}
      </Text>
    </Box>
  );
};
```

### Progress Indicator

```tsx
const ProgressIndicator: React.FC<{ current: number; total: number; label: string }> = ({
  current,
  total,
  label,
}) => (
  <Box>
    <Text color="blue">
      {label}: {current}/{total}
    </Text>
  </Box>
);
```

### Collapsible Section

```tsx
const CollapsibleSection: React.FC<{ title: string; isOpen: boolean; children: React.ReactNode }> = ({
  title,
  isOpen,
  children,
}) => (
  <Box flexDirection="column">
    <Text bold>
      {isOpen ? '▼' : '▶'} {title}
    </Text>
    {isOpen && <Box marginLeft={2}>{children}</Box>}
  </Box>
);
```

## Best Practices

1. **Type Safety**: Always define prop interfaces
2. **Performance**: Use React.memo for expensive renders
3. **Accessibility**: Use semantic structure and clear labels
4. **Error Boundaries**: Wrap components in error boundaries
5. **Testing**: Test components with ink-testing-library

## Anti-Patterns to Avoid

- Don't use DOM-specific APIs (document, window)
- Don't use CSS classes or inline styles (use Ink props)
- Don't mutate terminal state directly
- Don't forget to handle edge cases (empty arrays, null values)
- Don't create deeply nested component trees (keep it flat)
