---
name: radix-ui
description: Expert guidance for building React UIs with Radix Themes and Radix Primitives. Use when creating accessible, customisable UI components, setting up theming systems, working with pre-styled Radix Themes components, or building custom components on top of unstyled Radix Primitives. Trigger keywords include "radix", "radix ui", "radix themes", "radix primitives", "accessible components", "Dialog", "Dropdown", "Select", "Accordion", "Tabs", "Tooltip".
---

# Radix UI

Radix provides two complementary libraries for React:

- **Radix Themes**: Pre-styled, ready-to-use component library with built-in theming
- **Radix Primitives**: Unstyled, accessible component primitives for custom design systems

## Choosing Between Themes and Primitives

**Use Radix Themes when:**

- Building applications quickly with minimal styling effort
- Wanting a consistent, polished design out of the box
- Theming via configuration props is sufficient

**Use Radix Primitives when:**

- Building a custom design system with complete styling control
- Integrating with existing styling solutions (Tailwind, styled-components, CSS modules)
- Needing only specific components without a full theme system

## Quick Start

### Radix Themes Setup

```bash
npm install @radix-ui/themes
```

```tsx
import "@radix-ui/themes/styles.css";
import { Theme } from "@radix-ui/themes";

export default function App() {
    return (
        <Theme accentColor="indigo" grayColor="slate" radius="medium">
            <MyApp />
        </Theme>
    );
}
```

### Radix Primitives Setup

Install individual components:

```bash
npm install @radix-ui/react-dialog @radix-ui/react-dropdown-menu
```

Or install the full package:

```bash
npm install radix-ui
```

## Radix Themes

### Theme Configuration

The `Theme` component accepts these props:

| Prop              | Values                                | Default     |
| ----------------- | ------------------------------------- | ----------- |
| `accentColor`     | indigo, cyan, crimson, orange, etc.   | indigo      |
| `grayColor`       | gray, mauve, slate, sage, olive, sand | gray        |
| `radius`          | none, small, medium, large, full      | medium      |
| `scaling`         | 90%, 95%, 100%, 105%, 110%            | 100%        |
| `panelBackground` | solid, translucent                    | translucent |

### Component Variants

Most Themes components support these variant props:

```tsx
<Button variant="solid" size="2" color="indigo" highContrast />
```

Common variants: `classic`, `solid`, `soft`, `surface`, `outline`, `ghost`

Sizes: `"1"`, `"2"`, `"3"`, `"4"` (component-specific)

### Layout Components

```tsx
import { Flex, Box, Grid, Container, Section } from "@radix-ui/themes";

<Flex direction="column" gap="3" align="center" justify="between">
  <Box p="4" style={{ background: "var(--gray-3)" }}>
    Content
  </Box>
</Flex>

<Grid columns="3" gap="4" width="auto">
  <Box>1</Box>
  <Box>2</Box>
  <Box>3</Box>
</Grid>
```

### Typography

```tsx
import { Text, Heading, Code, Em, Strong } from "@radix-ui/themes";

<Heading size="6" weight="bold">Title</Heading>
<Text size="2" color="gray">Body text</Text>
<Code variant="soft">const x = 1</Code>
```

For complete Themes component reference, see [references/themes-components.md](references/themes-components.md).

## Radix Primitives

### Core Concepts

**Compound Components**: Primitives use a compound component pattern with multiple parts:

```tsx
import * as Dialog from "@radix-ui/react-dialog";

<Dialog.Root>
    <Dialog.Trigger>Open</Dialog.Trigger>
    <Dialog.Portal>
        <Dialog.Overlay className="overlay" />
        <Dialog.Content className="content">
            <Dialog.Title>Title</Dialog.Title>
            <Dialog.Description>Description</Dialog.Description>
            <Dialog.Close>Close</Dialog.Close>
        </Dialog.Content>
    </Dialog.Portal>
</Dialog.Root>;
```

**Uncontrolled by Default**: Components work without state management:

```tsx
// Uncontrolled - manages its own state
<Dialog.Root>...</Dialog.Root>

// Controlled - you manage the state
<Dialog.Root open={isOpen} onOpenChange={setIsOpen}>...</Dialog.Root>
```

### The asChild Prop

Use `asChild` to compose Radix behaviour onto custom components:

```tsx
import * as Tooltip from "@radix-ui/react-tooltip";
import { MyButton } from "./MyButton";

<Tooltip.Trigger asChild>
    <MyButton>Hover me</MyButton>
</Tooltip.Trigger>;
```

Requirements for custom components with `asChild`:

1. Spread all props onto the underlying DOM element
2. Forward refs using `React.forwardRef`

```tsx
const MyButton = React.forwardRef<HTMLButtonElement, ButtonProps>(
    ({ children, ...props }, ref) => (
        <button ref={ref} {...props}>
            {children}
        </button>
    ),
);
```

### Styling Primitives

**With CSS classes:**

```tsx
<Dialog.Overlay className="dialog-overlay" />
<Dialog.Content className="dialog-content" />
```

**With data attributes for state:**

```css
.accordion-item[data-state="open"] {
    background: var(--accent-3);
}

.accordion-item[data-state="closed"] {
    background: transparent;
}
```

**With Tailwind CSS:**

```tsx
<Dialog.Overlay className="fixed inset-0 bg-black/50" />
<Dialog.Content className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white p-6 rounded-lg" />
```

For complete Primitives patterns, see [references/primitives-patterns.md](references/primitives-patterns.md).

## Accessibility

Radix Primitives implement WAI-ARIA patterns automatically:

- Focus management and trapping (modals)
- Keyboard navigation (arrow keys, Tab, Escape)
- Screen reader announcements
- Proper ARIA attributes

Ensure custom implementations maintain accessibility:

```tsx
// Dialog requires Title for screen readers
<Dialog.Content aria-describedby={undefined}>
    <Dialog.Title>Required for a11y</Dialog.Title>
    {/* If no description, set aria-describedby={undefined} on Content */}
</Dialog.Content>
```
