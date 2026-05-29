---
name: ink-layout-styling
description: Use when creating terminal layouts with Ink using Flexbox-based positioning and styling for CLI applications.
allowed-tools: []
---

# Ink Layout and Styling

You are an expert in creating beautiful terminal layouts with Ink using Flexbox-based positioning and styling.

## Box Component - Layout Foundation

The Box component is the primary layout primitive, using Flexbox properties.

### Flexbox Direction

```tsx
// Vertical stack (default)
<Box flexDirection="column">
  <Text>First</Text>
  <Text>Second</Text>
</Box>

// Horizontal row
<Box flexDirection="row">
  <Text>Left</Text>
  <Text>Right</Text>
</Box>

// Reverse order
<Box flexDirection="column-reverse">
  <Text>Bottom (renders on top)</Text>
  <Text>Top (renders on bottom)</Text>
</Box>
```

### Spacing and Padding

```tsx
// Margin around element
<Box margin={1}>
  <Text>Content with margin</Text>
</Box>

// Directional margins
<Box marginTop={1} marginLeft={2} marginRight={2} marginBottom={1}>
  <Text>Custom margins</Text>
</Box>

// Padding inside element
<Box padding={1}>
  <Text>Content with padding</Text>
</Box>

// Directional padding
<Box paddingX={2} paddingY={1}>
  <Text>Horizontal and vertical padding</Text>
</Box>
```

### Alignment and Justification

```tsx
// Align items on cross axis
<Box alignItems="center">
  <Text>Centered</Text>
</Box>

<Box alignItems="flex-start">
  <Text>Top aligned</Text>
</Box>

<Box alignItems="flex-end">
  <Text>Bottom aligned</Text>
</Box>

// Justify content on main axis
<Box justifyContent="center">
  <Text>Centered horizontally</Text>
</Box>

<Box justifyContent="space-between">
  <Text>Left</Text>
  <Text>Right</Text>
</Box>

<Box justifyContent="space-around">
  <Text>Item 1</Text>
  <Text>Item 2</Text>
  <Text>Item 3</Text>
</Box>
```

### Dimensions

```tsx
// Fixed width
<Box width={50}>
  <Text>Fixed width content</Text>
</Box>

// Percentage width
<Box width="50%">
  <Text>Half width</Text>
</Box>

// Fixed height
<Box height={10}>
  <Text>Fixed height</Text>
</Box>

// Min/max dimensions
<Box minWidth={20} maxWidth={80}>
  <Text>Constrained width</Text>
</Box>
```

### Borders

```tsx
// Simple border
<Box borderStyle="single">
  <Text>Bordered content</Text>
</Box>

// Border styles: single, double, round, bold, singleDouble, doubleSingle, classic
<Box borderStyle="round" borderColor="cyan">
  <Text>Rounded border</Text>
</Box>

// Custom border color
<Box borderStyle="double" borderColor="green">
  <Text>Green double border</Text>
</Box>
```

## Text Component - Styling Text

### Colors

```tsx
// Foreground colors
<Text color="red">Error message</Text>
<Text color="green">Success message</Text>
<Text color="yellow">Warning message</Text>
<Text color="blue">Info message</Text>
<Text color="cyan">Highlight</Text>
<Text color="magenta">Special</Text>

// Background colors
<Text backgroundColor="red" color="white">
  Alert!
</Text>

// Hex colors
<Text color="#FF5733">Custom color</Text>
```

### Text Formatting

```tsx
// Bold
<Text bold>Important text</Text>

// Italic
<Text italic>Emphasized text</Text>

// Underline
<Text underline>Underlined text</Text>

// Strikethrough
<Text strikethrough>Removed text</Text>

// Dim
<Text dimColor>Subtle text</Text>

// Inverse
<Text inverse>Inverted colors</Text>

// Combinations
<Text bold color="cyan" underline>
  Multiple styles
</Text>
```

### Text Wrapping

```tsx
// Wrap text to fit width
<Box width={40}>
  <Text wrap="wrap">
    This is a long text that will wrap to fit within the 40 character width.
  </Text>
</Box>

// Truncate text
<Box width={20}>
  <Text wrap="truncate">This text will be truncated</Text>
</Box>

// Truncate with custom ellipsis
<Box width={20}>
  <Text wrap="truncate-end">This text will be truncated...</Text>
</Box>
```

## Layout Patterns

### Card Layout

```tsx
const Card: React.FC<{ title: string; children: React.ReactNode }> = ({ title, children }) => (
  <Box borderStyle="round" borderColor="cyan" padding={1} flexDirection="column">
    <Box marginBottom={1}>
      <Text bold color="cyan">
        {title}
      </Text>
    </Box>
    <Box>{children}</Box>
  </Box>
);
```

### Split Layout

```tsx
const SplitLayout: React.FC<{ left: React.ReactNode; right: React.ReactNode }> = ({
  left,
  right,
}) => (
  <Box>
    <Box width="50%" borderStyle="single" padding={1}>
      {left}
    </Box>
    <Box width="50%" borderStyle="single" padding={1}>
      {right}
    </Box>
  </Box>
);
```

### Header/Content/Footer

```tsx
const Layout: React.FC<{
  header: React.ReactNode;
  content: React.ReactNode;
  footer: React.ReactNode;
}> = ({ header, content, footer }) => (
  <Box flexDirection="column" height="100%">
    <Box borderStyle="single" borderColor="cyan" padding={1}>
      {header}
    </Box>
    <Box flexGrow={1} padding={1}>
      {content}
    </Box>
    <Box borderStyle="single" borderColor="gray" padding={1}>
      {footer}
    </Box>
  </Box>
);
```

### Grid Layout

```tsx
const Grid: React.FC<{ items: React.ReactNode[]; columns: number }> = ({ items, columns }) => {
  const rows: React.ReactNode[][] = [];
  for (let i = 0; i < items.length; i += columns) {
    rows.push(items.slice(i, i + columns));
  }

  return (
    <Box flexDirection="column">
      {rows.map((row, i) => (
        <Box key={i}>
          {row.map((item, j) => (
            <Box key={j} width={`${100 / columns}%`} padding={1}>
              {item}
            </Box>
          ))}
        </Box>
      ))}
    </Box>
  );
};
```

### Responsive Layout

```tsx
import { useStdout } from 'ink';

const ResponsiveLayout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { stdout } = useStdout();
  const isNarrow = stdout.columns < 80;

  return (
    <Box flexDirection={isNarrow ? 'column' : 'row'} width="100%">
      {children}
    </Box>
  );
};
```

## Utility Components

### Spacer

```tsx
// Push elements apart
<Box>
  <Text>Left</Text>
  <Spacer />
  <Text>Right</Text>
</Box>
```

### Newline

```tsx
<Box flexDirection="column">
  <Text>First line</Text>
  <Newline />
  <Text>After blank line</Text>
</Box>
```

## Best Practices

1. **Use Box for layout**: Don't use Text for layout, use Box
2. **Flexbox thinking**: Think in terms of Flexbox properties
3. **Consistent spacing**: Use consistent margin/padding values
4. **Color sparingly**: Don't overuse colors, use them for emphasis
5. **Test terminals**: Test on different terminal sizes and emulators

## Common Layout Patterns

### Full-width header

```tsx
<Box width="100%" borderStyle="single" padding={1}>
  <Text bold>Application Title</Text>
</Box>
```

### Centered modal

```tsx
<Box justifyContent="center" alignItems="center" height="100%">
  <Box borderStyle="round" padding={2} borderColor="cyan">
    <Text>Modal content</Text>
  </Box>
</Box>
```

### Sidebar layout

```tsx
<Box>
  <Box width={20} borderStyle="single" padding={1}>
    <Text>Sidebar</Text>
  </Box>
  <Box flexGrow={1} padding={1}>
    <Text>Main content</Text>
  </Box>
</Box>
```
