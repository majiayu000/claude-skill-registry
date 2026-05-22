---
name: mantine-developing
description: Build React UIs with Mantine component library. Customize styles with Styles API, handle forms with @mantine/form, implement theming, and avoid accessibility pitfalls. Use when creating Mantine components or fixing styling issues.
version: 1.0.0
---

# Mantine UI Development

## Purpose

Build React UIs with Mantine's component library, Styles API for customization, and @mantine/form for form handling.

## When NOT to Use

- Basic React development (Claude knows this)
- Non-Mantine UI libraries (Material UI, Chakra, etc.)
- Simple HTML/CSS without Mantine
- Mantine v6 or earlier (this skill covers v7+)

## Quick Start

### Step 1: Import Components

```tsx
// Core components
import { Button, TextInput, Select, Modal } from '@mantine/core';

// Hooks
import { useDisclosure, useToggle } from '@mantine/hooks';

// Form handling
import { useForm } from '@mantine/form';
```

### Step 2: Basic Component Usage

```tsx
<Button variant="filled" color="blue" size="md" loading={isLoading}>
  Submit
</Button>

<TextInput
  label="Email"
  placeholder="your@email.com"
  error={errors.email}
  required
/>
```

### Step 3: Customize with Styles API

See [Core Patterns](#core-patterns) below.

### Step 4: Validate Accessibility

- Add `aria-label` to icon-only buttons
- Check keyboard navigation works
- Verify focus states are visible

## Core Patterns

### Styles API (Critical)

Mantine components have multiple inner elements. Use Styles API to target them:

```tsx
// Option 1: classNames prop (recommended for CSS modules)
import classes from './Button.module.css';

<Button classNames={{
  root: classes.button,      // Outer wrapper
  label: classes.buttonLabel // Text content
}} />
```

```css
/* Button.module.css */
.button {
  background: linear-gradient(45deg, blue, purple);
}
.buttonLabel {
  font-weight: 700;
}
```

```tsx
// Option 2: styles prop (inline styles for inner elements)
<Button styles={{
  root: { padding: '10px 20px' },
  label: { color: 'white' }
}} />

// Option 3: CSS variables
<Button style={{ '--button-bg': 'var(--mantine-color-blue-6)' }} />

// Option 4: Data attributes for state
<Button data-active={isActive} />
```

**Finding selector names:** Check Mantine docs for each component's "Styles API" section listing available selectors.

### Form Handling (@mantine/form)

```tsx
import { useForm } from '@mantine/form';
import { TextInput, Checkbox, Button, Box } from '@mantine/core';

function LoginForm() {
  const form = useForm({
    initialValues: {
      email: '',
      password: '',
      rememberMe: false,
    },
    validate: {
      email: (value) =>
        /^\S+@\S+$/.test(value) ? null : 'Invalid email',
      password: (value) =>
        value.length >= 8 ? null : 'Password must be 8+ characters',
    },
    // Optional: validate on change instead of only on submit
    validateInputOnChange: true,
  });

  const handleSubmit = (values: typeof form.values) => {
    console.log('Form submitted:', values);
  };

  return (
    <Box component="form" onSubmit={form.onSubmit(handleSubmit)}>
      <TextInput
        label="Email"
        placeholder="your@email.com"
        {...form.getInputProps('email')}
      />
      <TextInput
        label="Password"
        type="password"
        {...form.getInputProps('password')}
      />
      <Checkbox
        label="Remember me"
        {...form.getInputProps('rememberMe', { type: 'checkbox' })}
      />
      <Button type="submit" mt="md">Login</Button>
    </Box>
  );
}
```

**Key form methods:**
- `form.getInputProps('fieldName')` - Binds value, onChange, error
- `form.getInputProps('field', { type: 'checkbox' })` - For checkboxes/switches
- `form.onSubmit(handler)` - Validates before calling handler
- `form.setFieldValue('field', value)` - Programmatic updates
- `form.reset()` - Reset to initial values
- `form.validate()` - Manual validation

### Polymorphic Components

Change the underlying HTML element:

```tsx
// Button as link
<Button component="a" href="/dashboard">
  Go to Dashboard
</Button>

// Text as span (default is p)
<Text component="span">Inline text</Text>

// Card as article
<Card component="article">Content</Card>
```

**TypeScript note:** Ref type changes with component prop!
```tsx
// Default: HTMLButtonElement
const buttonRef = useRef<HTMLButtonElement>(null);
<Button ref={buttonRef} />

// With component="a": HTMLAnchorElement
const linkRef = useRef<HTMLAnchorElement>(null);
<Button component="a" ref={linkRef} href="/" />
```

### Theming

```tsx
import { MantineProvider, createTheme } from '@mantine/core';

const theme = createTheme({
  primaryColor: 'violet',
  colors: {
    // Add custom color palette
    brand: [
      '#f0e6ff', '#d9c2ff', '#c29dff', '#ab79ff',
      '#9454ff', '#7d30ff', '#660bff', '#5200d9',
      '#3e00a6', '#2b0073'
    ],
  },
  components: {
    Button: {
      defaultProps: {
        radius: 'md',
      },
    },
  },
});

function App() {
  return (
    <MantineProvider theme={theme}>
      {/* Your app */}
    </MantineProvider>
  );
}
```

### Dark Mode

```tsx
import { useMantineColorScheme, Button } from '@mantine/core';

function ColorSchemeToggle() {
  const { colorScheme, toggleColorScheme } = useMantineColorScheme();

  return (
    <Button onClick={() => toggleColorScheme()}>
      {colorScheme === 'dark' ? 'Light' : 'Dark'} mode
    </Button>
  );
}
```

**CSS for dark mode:**
```css
/* Use light-dark() function */
.myComponent {
  background: light-dark(white, var(--mantine-color-dark-7));
  color: light-dark(black, white);
}
```

## Common Pitfalls

### 1. Nested Interactive Elements

**Wrong:**
```tsx
<Accordion.Control>
  <Button onClick={handleDelete}>Delete</Button>  {/* Invalid! */}
</Accordion.Control>
```

**Correct:**
```tsx
<Accordion.Item>
  <Box style={{ display: 'flex', alignItems: 'center' }}>
    <Accordion.Control style={{ flex: 1 }}>Title</Accordion.Control>
    <Button onClick={handleDelete}>Delete</Button>
  </Box>
  <Accordion.Panel>Content</Accordion.Panel>
</Accordion.Item>
```

### 2. Tooltip on Disabled Button

**Wrong:**
```tsx
<Tooltip label="Disabled">
  <Button disabled>Click me</Button>  {/* Tooltip won't show! */}
</Tooltip>
```

**Correct:**
```tsx
<Tooltip label="Disabled">
  <Button data-disabled onClick={(e) => e.preventDefault()}>
    Click me
  </Button>
</Tooltip>
```

### 3. ActionIcon.Group Wrapping

**Wrong:**
```tsx
<ActionIcon.Group>
  <div>  {/* Invalid wrapper! */}
    <ActionIcon><IconEdit /></ActionIcon>
  </div>
</ActionIcon.Group>
```

**Correct:**
```tsx
<ActionIcon.Group>
  <ActionIcon><IconEdit /></ActionIcon>
  <ActionIcon><IconTrash /></ActionIcon>
</ActionIcon.Group>
```

### 4. Missing aria-label

**Wrong:**
```tsx
<ActionIcon>
  <IconSearch />  {/* No accessible name! */}
</ActionIcon>
```

**Correct:**
```tsx
<ActionIcon aria-label="Search">
  <IconSearch />
</ActionIcon>
```

### 5. AspectRatio in Flexbox

**Wrong:**
```tsx
<Flex>
  <AspectRatio ratio={16/9}>  {/* Won't size correctly */}
    <Image src="/photo.jpg" />
  </AspectRatio>
</Flex>
```

**Correct:**
```tsx
<Flex>
  <AspectRatio ratio={16/9} w={300}>  {/* Explicit width */}
    <Image src="/photo.jpg" />
  </AspectRatio>
</Flex>
```

### 6. Select vs Autocomplete Confusion

- **Select**: User MUST choose from options (enforces list)
- **Autocomplete**: User CAN type any value (suggestions only)

```tsx
// Use Select when value must be from list
<Select data={['Option 1', 'Option 2']} />

// Use Autocomplete when free text is acceptable
<Autocomplete data={['Suggestion 1', 'Suggestion 2']} />
```

## Accessibility Requirements

1. **Icon buttons must have aria-label:**
   ```tsx
   <ActionIcon aria-label="Close modal">
     <IconX />
   </ActionIcon>
   ```

2. **Use closeButtonLabel prop:**
   ```tsx
   <Modal closeButtonLabel="Close this dialog" opened={opened} onClose={close}>
   ```

3. **Set heading order for accordions:**
   ```tsx
   <Accordion.Control order={3}>  {/* Renders as <h3> */}
   ```

4. **Test keyboard navigation:**
   - Tab through form fields
   - Enter/Space on buttons
   - Escape to close modals
   - Arrow keys in menus

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Styles not applying | Wrong selector name | Check component's Styles API docs for available selectors |
| Dark mode has wrong colors | Hardcoded color values | Use `light-dark()` CSS function or theme colors |
| Form not validating | Wrong config | Use `validate` for submit-time, `validateInputOnChange` for live validation |
| TypeScript ref errors | Polymorphic component | Update ref type to match `component` prop value |
| Component won't accept custom props | Polymorphic typing | Props don't extend default element; use `component` to change |
| Tooltip not showing on disabled | Disabled blocks events | Use `data-disabled` with `onClick` preventDefault |

## External Documentation

For latest Mantine documentation:

1. **Context7** (recommended):
   ```
   mcp__context7__get-library-docs
   context7CompatibleLibraryID: "/mantinedev/mantine"
   topic: "Button" or "Select" or "form" etc.
   ```

2. **Direct fetch**:
   ```
   WebFetch → https://mantine.dev/llms.txt
   ```

3. **Official docs**: https://mantine.dev

## Component Quick Reference

See REFERENCE.md for detailed component patterns including:
- Layout: Stack, Group, Grid, Flex, Container, AppShell
- Inputs: TextInput, Select, Checkbox, DatePicker
- Feedback: Modal, Notifications, Alert
- Navigation: Tabs, NavLink, Breadcrumbs
- Data: Table, Skeleton, Timeline


---

## Related Agent

For comprehensive React + Mantine UI guidance that coordinates this and other Mantine skills, use the **`mantine-ui-expert`** agent.

**Cost Optimization:** Use `model="haiku"` when invoking this agent for routine component development tasks. Haiku is sufficient for template-based Mantine patterns and Styles API usage.
