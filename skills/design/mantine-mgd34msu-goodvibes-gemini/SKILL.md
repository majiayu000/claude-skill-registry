---
name: mantine
description: Builds React applications with Mantine's 100+ components, hooks, and form library. Use when creating feature-rich UIs with built-in dark mode, accessibility, and TypeScript support.
---

# Mantine

Full-featured React component library with 100+ customizable components and 50+ hooks.

## Quick Start

```bash
npm install @mantine/core @mantine/hooks
npm install -D postcss postcss-preset-mantine postcss-simple-vars
```

```js
// postcss.config.cjs
module.exports = {
  plugins: {
    'postcss-preset-mantine': {},
    'postcss-simple-vars': {
      variables: {
        'mantine-breakpoint-xs': '36em',
        'mantine-breakpoint-sm': '48em',
        'mantine-breakpoint-md': '62em',
        'mantine-breakpoint-lg': '75em',
        'mantine-breakpoint-xl': '88em',
      },
    },
  },
};
```

```tsx
// App.tsx
import '@mantine/core/styles.css';
import { MantineProvider, createTheme } from '@mantine/core';

const theme = createTheme({
  primaryColor: 'blue',
  fontFamily: 'Inter, sans-serif',
});

function App() {
  return (
    <MantineProvider theme={theme}>
      <YourApp />
    </MantineProvider>
  );
}
```

```tsx
// Usage
import { Button, TextInput, Group, Stack } from '@mantine/core';

function Demo() {
  return (
    <Stack>
      <TextInput label="Email" placeholder="you@example.com" />
      <Group>
        <Button>Submit</Button>
        <Button variant="outline">Cancel</Button>
      </Group>
    </Stack>
  );
}
```

## Core Components

### Button

```tsx
import { Button, ActionIcon } from '@mantine/core';
import { IconSettings } from '@tabler/icons-react';

// Variants
<Button variant="filled">Filled</Button>
<Button variant="light">Light</Button>
<Button variant="outline">Outline</Button>
<Button variant="subtle">Subtle</Button>
<Button variant="transparent">Transparent</Button>
<Button variant="white">White</Button>

// Sizes
<Button size="xs">Extra Small</Button>
<Button size="sm">Small</Button>
<Button size="md">Medium</Button>
<Button size="lg">Large</Button>
<Button size="xl">Extra Large</Button>

// Colors
<Button color="blue">Blue</Button>
<Button color="red">Red</Button>
<Button color="green">Green</Button>

// With icons
<Button leftSection={<IconSettings size={16} />}>Settings</Button>
<Button rightSection={<IconArrow size={16} />}>Next</Button>

// Loading
<Button loading>Processing...</Button>

// Icon button
<ActionIcon variant="filled" size="lg">
  <IconSettings size={18} />
</ActionIcon>
```

### TextInput

```tsx
import { TextInput, PasswordInput, Textarea, NumberInput } from '@mantine/core';

<TextInput
  label="Email"
  description="We'll never share your email"
  placeholder="you@example.com"
  required
  error="Invalid email"
/>

<PasswordInput
  label="Password"
  placeholder="Enter password"
  visible={visible}
  onVisibilityChange={toggle}
/>

<Textarea
  label="Message"
  placeholder="Your message"
  autosize
  minRows={3}
  maxRows={6}
/>

<NumberInput
  label="Amount"
  placeholder="Enter amount"
  min={0}
  max={100}
  step={5}
  prefix="$"
  thousandSeparator=","
/>
```

### Select and MultiSelect

```tsx
import { Select, MultiSelect, Combobox } from '@mantine/core';

<Select
  label="Framework"
  placeholder="Pick one"
  data={['React', 'Vue', 'Angular', 'Svelte']}
  searchable
  clearable
/>

<Select
  label="User"
  data={[
    { value: '1', label: 'John Doe' },
    { value: '2', label: 'Jane Smith' },
  ]}
/>

<MultiSelect
  label="Technologies"
  placeholder="Select technologies"
  data={['TypeScript', 'JavaScript', 'Python', 'Rust']}
  searchable
  maxSelectedValues={3}
/>
```

### Modal and Drawer

```tsx
import { Modal, Button } from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';

function ModalDemo() {
  const [opened, { open, close }] = useDisclosure(false);

  return (
    <>
      <Modal opened={opened} onClose={close} title="Authentication">
        Modal content here...
      </Modal>
      <Button onClick={open}>Open modal</Button>
    </>
  );
}

// Drawer
import { Drawer } from '@mantine/core';

<Drawer
  opened={opened}
  onClose={close}
  title="Navigation"
  position="left"  // left, right, top, bottom
  size="md"
>
  Drawer content...
</Drawer>
```

### Notifications

```bash
npm install @mantine/notifications
```

```tsx
import '@mantine/notifications/styles.css';
import { Notifications, notifications } from '@mantine/notifications';

// Add to app root
<MantineProvider>
  <Notifications position="top-right" />
  <App />
</MantineProvider>

// Show notification
notifications.show({
  title: 'Success',
  message: 'Your changes have been saved',
  color: 'green',
  autoClose: 5000,
});

// Update existing notification
const id = notifications.show({
  loading: true,
  title: 'Loading...',
  message: 'Please wait',
  autoClose: false,
});

notifications.update({
  id,
  loading: false,
  title: 'Complete',
  message: 'Data loaded successfully',
  color: 'green',
  autoClose: 3000,
});
```

### Tabs

```tsx
import { Tabs } from '@mantine/core';

<Tabs defaultValue="gallery">
  <Tabs.List>
    <Tabs.Tab value="gallery">Gallery</Tabs.Tab>
    <Tabs.Tab value="messages">Messages</Tabs.Tab>
    <Tabs.Tab value="settings">Settings</Tabs.Tab>
  </Tabs.List>

  <Tabs.Panel value="gallery" pt="md">
    Gallery content
  </Tabs.Panel>
  <Tabs.Panel value="messages" pt="md">
    Messages content
  </Tabs.Panel>
  <Tabs.Panel value="settings" pt="md">
    Settings content
  </Tabs.Panel>
</Tabs>
```

### Card

```tsx
import { Card, Image, Text, Badge, Button, Group } from '@mantine/core';

<Card shadow="sm" padding="lg" radius="md" withBorder>
  <Card.Section>
    <Image src="/product.jpg" height={160} alt="Product" />
  </Card.Section>

  <Group justify="space-between" mt="md" mb="xs">
    <Text fw={500}>Product Name</Text>
    <Badge color="pink">On Sale</Badge>
  </Group>

  <Text size="sm" c="dimmed">
    Product description goes here.
  </Text>

  <Button fullWidth mt="md" radius="md">
    Add to Cart
  </Button>
</Card>
```

## Forms

```bash
npm install @mantine/form
```

```tsx
import { useForm } from '@mantine/form';
import { TextInput, Button, Stack } from '@mantine/core';

function ContactForm() {
  const form = useForm({
    mode: 'uncontrolled',
    initialValues: {
      name: '',
      email: '',
      message: '',
    },
    validate: {
      name: (value) => value.length < 2 ? 'Name is too short' : null,
      email: (value) => /^\S+@\S+$/.test(value) ? null : 'Invalid email',
      message: (value) => value.length < 10 ? 'Message too short' : null,
    },
  });

  return (
    <form onSubmit={form.onSubmit((values) => console.log(values))}>
      <Stack>
        <TextInput
          label="Name"
          placeholder="Your name"
          key={form.key('name')}
          {...form.getInputProps('name')}
        />
        <TextInput
          label="Email"
          placeholder="your@email.com"
          key={form.key('email')}
          {...form.getInputProps('email')}
        />
        <Textarea
          label="Message"
          placeholder="Your message"
          key={form.key('message')}
          {...form.getInputProps('message')}
        />
        <Button type="submit">Submit</Button>
      </Stack>
    </form>
  );
}
```

### Form with Zod Validation

```tsx
import { useForm, zodResolver } from '@mantine/form';
import { z } from 'zod';

const schema = z.object({
  name: z.string().min(2, 'Name must be at least 2 characters'),
  email: z.string().email('Invalid email'),
  age: z.number().min(18, 'Must be 18 or older'),
});

const form = useForm({
  mode: 'uncontrolled',
  initialValues: { name: '', email: '', age: 18 },
  validate: zodResolver(schema),
});
```

## Hooks

```tsx
import {
  useDisclosure,
  useToggle,
  useDebouncedValue,
  useClipboard,
  useLocalStorage,
  useMediaQuery,
  useClickOutside,
  useHotkeys,
  useForm,
} from '@mantine/hooks';

// Disclosure (modals, menus)
const [opened, { open, close, toggle }] = useDisclosure(false);

// Toggle between values
const [value, toggle] = useToggle(['light', 'dark']);

// Debounced value
const [search, setSearch] = useState('');
const [debounced] = useDebouncedValue(search, 300);

// Clipboard
const clipboard = useClipboard({ timeout: 2000 });
clipboard.copy('Text to copy');
clipboard.copied // true after copy

// Local storage
const [value, setValue] = useLocalStorage({
  key: 'user-preference',
  defaultValue: 'dark',
});

// Media query
const isMobile = useMediaQuery('(max-width: 768px)');

// Click outside
const ref = useClickOutside(() => setOpened(false));

// Keyboard shortcuts
useHotkeys([
  ['mod+K', () => openSearch()],
  ['mod+S', () => saveDocument()],
  ['Escape', () => closeModal()],
]);
```

## Theming

### Custom Theme

```tsx
import { createTheme, MantineProvider } from '@mantine/core';

const theme = createTheme({
  // Primary color
  primaryColor: 'brand',
  primaryShade: { light: 6, dark: 8 },

  // Custom colors (10 shades each)
  colors: {
    brand: [
      '#e6f2ff', '#b3d9ff', '#80bfff', '#4da6ff', '#1a8cff',
      '#0073e6', '#005cb3', '#004480', '#002d4d', '#00161a',
    ],
  },

  // Typography
  fontFamily: 'Inter, sans-serif',
  fontFamilyMonospace: 'Fira Code, monospace',
  headings: {
    fontFamily: 'Inter, sans-serif',
    fontWeight: '600',
    sizes: {
      h1: { fontSize: '2.5rem', lineHeight: '1.2' },
      h2: { fontSize: '2rem', lineHeight: '1.3' },
    },
  },

  // Spacing scale
  spacing: {
    xs: '0.5rem',
    sm: '0.75rem',
    md: '1rem',
    lg: '1.5rem',
    xl: '2rem',
  },

  // Border radius
  radius: {
    xs: '2px',
    sm: '4px',
    md: '8px',
    lg: '16px',
    xl: '32px',
  },
  defaultRadius: 'md',

  // Shadows
  shadows: {
    xs: '0 1px 2px rgba(0, 0, 0, 0.05)',
    sm: '0 1px 3px rgba(0, 0, 0, 0.1)',
    md: '0 4px 6px rgba(0, 0, 0, 0.1)',
    lg: '0 10px 15px rgba(0, 0, 0, 0.1)',
    xl: '0 20px 25px rgba(0, 0, 0, 0.15)',
  },

  // Focus styles
  focusRing: 'auto', // 'auto' | 'always' | 'never'

  // Other
  cursorType: 'pointer', // 'default' | 'pointer'
  autoContrast: true,
});
```

### Dark Mode

```tsx
import { MantineProvider, useMantineColorScheme, Button } from '@mantine/core';

// Provider setup
<MantineProvider defaultColorScheme="auto">
  <App />
</MantineProvider>

// Toggle button
function ColorSchemeToggle() {
  const { colorScheme, toggleColorScheme } = useMantineColorScheme();

  return (
    <Button onClick={() => toggleColorScheme()}>
      {colorScheme === 'dark' ? 'Light' : 'Dark'} mode
    </Button>
  );
}
```

### Styles API

```tsx
import { Button, createStyles } from '@mantine/core';

// Using classNames prop
<Button
  classNames={{
    root: 'my-button-root',
    label: 'my-button-label',
  }}
>
  Styled Button
</Button>

// Using styles prop
<Button
  styles={{
    root: { backgroundColor: 'red' },
    label: { color: 'white' },
  }}
>
  Inline Styled
</Button>

// CSS Modules (recommended)
// Button.module.css
.root {
  background-color: var(--mantine-color-blue-6);
}

.label {
  font-weight: 700;
}

// Component
import classes from './Button.module.css';
<Button classNames={classes}>CSS Modules</Button>
```

### CSS Variables

```tsx
// Access theme tokens via CSS variables
.myComponent {
  background-color: var(--mantine-color-blue-6);
  padding: var(--mantine-spacing-md);
  border-radius: var(--mantine-radius-md);
  font-size: var(--mantine-font-size-sm);

  /* Dark mode specific */
  @mixin dark {
    background-color: var(--mantine-color-dark-6);
  }

  /* Responsive */
  @media (max-width: $mantine-breakpoint-sm) {
    padding: var(--mantine-spacing-xs);
  }
}
```

## Layout

```tsx
import {
  AppShell,
  Container,
  Grid,
  Group,
  Stack,
  Flex,
  SimpleGrid,
  Center,
} from '@mantine/core';

// App shell layout
<AppShell
  header={{ height: 60 }}
  navbar={{ width: 300, breakpoint: 'sm', collapsed: { mobile: !opened } }}
  padding="md"
>
  <AppShell.Header>Header</AppShell.Header>
  <AppShell.Navbar>Navbar</AppShell.Navbar>
  <AppShell.Main>Content</AppShell.Main>
</AppShell>

// Container with max width
<Container size="md">Content</Container>

// Grid
<Grid>
  <Grid.Col span={6}>Half</Grid.Col>
  <Grid.Col span={6}>Half</Grid.Col>
  <Grid.Col span={{ base: 12, md: 6, lg: 4 }}>Responsive</Grid.Col>
</Grid>

// Simple grid (equal columns)
<SimpleGrid cols={3}>
  <div>1</div>
  <div>2</div>
  <div>3</div>
</SimpleGrid>

// Flex layouts
<Group justify="space-between" align="center">
  <Text>Left</Text>
  <Text>Right</Text>
</Group>

<Stack gap="md">
  <Text>Item 1</Text>
  <Text>Item 2</Text>
</Stack>

<Flex gap="md" wrap="wrap" justify="center">
  <Box>Item</Box>
  <Box>Item</Box>
</Flex>
```

## Best Practices

1. **Use CSS modules** - Most performant styling approach
2. **Leverage hooks** - `useDisclosure`, `useDebouncedValue`, `useForm` for common patterns
3. **Use Styles API** - Override component parts with `classNames` prop
4. **Theme tokens** - Use CSS variables for consistent theming
5. **Form validation** - Use `@mantine/form` with Zod for type-safe forms

## Reference Files

- [references/components.md](references/components.md) - Complete component list
- [references/hooks.md](references/hooks.md) - All available hooks
