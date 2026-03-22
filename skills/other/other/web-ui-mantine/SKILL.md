---
name: web-ui-mantine
description: Mantine v7 component library — theming, styling, hooks, forms, notifications
---

# Mantine v7 Component Patterns

> **Quick Guide:** Mantine v7 is a full-featured React component library using CSS Modules (not CSS-in-JS). Wrap your app in `MantineProvider` with a `createTheme` object. Style with CSS Modules + PostCSS preset mixins, the Styles API (`classNames`/`styles` props), or style props (`p`, `m`, `bg`, etc.). Use `@mantine/form` for form management, `@mantine/hooks` for utility hooks, and `@mantine/notifications` for toasts. PostCSS preset with `postcss-preset-mantine` is required for responsive mixins and `light-dark()`.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST wrap your app in `MantineProvider` and import `@mantine/core/styles.css` at the root)**

**(You MUST install and configure `postcss-preset-mantine` for CSS Modules mixins and responsive utilities)**

**(You MUST use CSS Modules (`.module.css`) for custom component styles - `createStyles` was removed in v7)**

**(You MUST provide 10-shade color tuples when adding custom colors to the theme)**

</critical_requirements>

---

**Auto-detection:** Mantine, @mantine/core, @mantine/hooks, @mantine/form, @mantine/notifications, @mantine/dates, MantineProvider, createTheme, useForm, useDisclosure, useDebouncedValue, useMediaQuery, postcss-preset-mantine, light-dark(), getInputProps, classNames prop, styles prop

**When to use:**

- Building React applications needing 100+ ready-to-use accessible components
- Projects requiring built-in form management, date pickers, or notification systems
- Applications where CSS Modules (no runtime CSS-in-JS) are preferred for performance
- Teams wanting a batteries-included library with hooks, theming, and responsive utilities

**When NOT to use:**

- Projects committed to a different component library (MUI, Chakra, shadcn/ui)
- Applications requiring Tailwind-first styling (Mantine uses CSS Modules, not Tailwind)
- When only a few components are needed and a full library is overkill

**Key patterns covered:**

- MantineProvider setup with createTheme and PostCSS configuration
- Core components (Button, TextInput, Select, Modal, Drawer, Menu, Tabs, Accordion)
- Styling with CSS Modules, Styles API (classNames/styles/vars), and style props
- Theming with createTheme (colors, defaultRadius, component defaults)
- Color scheme (light/dark/auto) with useMantineColorScheme
- @mantine/form (useForm, validation, nested fields, list management)
- @mantine/hooks (useDisclosure, useDebouncedValue, useMediaQuery)
- @mantine/notifications and @mantine/dates

---

<philosophy>

## Philosophy

Mantine is a **batteries-included** React component library. Unlike copy-and-own systems, Mantine provides pre-built components that are styled via CSS Modules and customized through a theme object and Styles API. The v7 rewrite (late 2023) dropped Emotion for native CSS Modules, eliminating CSS-in-JS runtime overhead entirely.

**What Mantine handles vs what other skills handle:**

- Mantine: component rendering, theming, form management, hooks, notifications, dates
- Your styling approach: custom CSS beyond Mantine's Styles API
- Your data fetching solution: server state management
- Your state management solution: global client state beyond component state

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: MantineProvider Setup

Every Mantine app requires `MantineProvider` at the root with CSS imports and PostCSS configuration.

```tsx
// app.tsx
import "@mantine/core/styles.css";
// Import additional package styles only if using those packages:
// import '@mantine/dates/styles.css';
// import '@mantine/notifications/styles.css';

import { createTheme, MantineProvider } from "@mantine/core";

const theme = createTheme({
  primaryColor: "blue",
  defaultRadius: "md",
});

export function App() {
  return (
    <MantineProvider theme={theme}>{/* Your app content */}</MantineProvider>
  );
}
```

#### PostCSS Configuration

```javascript
// postcss.config.cjs
module.exports = {
  plugins: {
    "postcss-preset-mantine": {},
    "postcss-simple-vars": {
      variables: {
        "mantine-breakpoint-xs": "36em",
        "mantine-breakpoint-sm": "48em",
        "mantine-breakpoint-md": "62em",
        "mantine-breakpoint-lg": "75em",
        "mantine-breakpoint-xl": "88em",
      },
    },
  },
};
```

#### SSR Setup (Required for SSR Frameworks)

```tsx
import { ColorSchemeScript, mantineHtmlProps } from "@mantine/core";

// In your root HTML/layout:
<html lang="en" {...mantineHtmlProps}>
  <head>
    <ColorSchemeScript defaultColorScheme="auto" />
  </head>
  <body>
    <App />
  </body>
</html>;
```

**Why good:** Theme object lives outside component body (prevents re-renders), PostCSS preset enables responsive mixins, `ColorSchemeScript` prevents flash of wrong theme on SSR

---

### Pattern 2: Core Components

Mantine components accept `className`, `style`, style props, and the Styles API. All support `variant`, `size`, `color`, and `radius` props.

```tsx
import {
  Button,
  TextInput,
  Select,
  Checkbox,
  Group,
  Stack,
} from "@mantine/core";

// Button with variants and sizes
<Button variant="filled" color="blue" size="md" loading={isLoading}>
  Submit
</Button>
<Button variant="outline">Cancel</Button>
<Button variant="light" color="red" leftSection={<TrashIcon />}>
  Delete
</Button>

// Text inputs
<TextInput
  label="Email"
  placeholder="you@example.com"
  withAsterisk
  error={errors.email}
/>

// Select
<Select
  label="Role"
  data={["Admin", "Editor", "Viewer"]}
  placeholder="Pick a role"
  searchable
  clearable
/>

// Checkbox
<Checkbox label="Accept terms" checked={accepted} onChange={handleChange} />

// Layout components
<Group gap="md">{/* Horizontal flex */}</Group>
<Stack gap="sm">{/* Vertical flex */}</Stack>
```

**Why good:** Consistent API across all components (variant, size, color, radius), layout components (Group, Stack) replace manual flexbox

---

### Pattern 3: Modal, Drawer, Menu, Tabs, Accordion

Overlay and compound components use `useDisclosure` for state management.

```tsx
import { Modal, Button } from "@mantine/core";
import { useDisclosure } from "@mantine/hooks";

function Demo() {
  const [opened, { open, close }] = useDisclosure(false);

  return (
    <>
      <Modal opened={opened} onClose={close} title="Confirm Action">
        <p>Are you sure?</p>
        <Group mt="md" justify="flex-end">
          <Button variant="outline" onClick={close}>
            Cancel
          </Button>
          <Button onClick={handleConfirm}>Confirm</Button>
        </Group>
      </Modal>
      <Button onClick={open}>Open Modal</Button>
    </>
  );
}
```

```tsx
// Drawer - same pattern as Modal
import { Drawer } from "@mantine/core";

<Drawer opened={opened} onClose={close} title="Settings" position="right">
  {/* Drawer content */}
</Drawer>;
```

```tsx
// Menu
import { Menu, Button } from "@mantine/core";

<Menu shadow="md" width={200}>
  <Menu.Target>
    <Button>Actions</Button>
  </Menu.Target>
  <Menu.Dropdown>
    <Menu.Label>Application</Menu.Label>
    <Menu.Item leftSection={<SettingsIcon />}>Settings</Menu.Item>
    <Menu.Divider />
    <Menu.Item color="red" leftSection={<TrashIcon />}>
      Delete
    </Menu.Item>
  </Menu.Dropdown>
</Menu>;
```

```tsx
// Tabs
import { Tabs } from "@mantine/core";

<Tabs defaultValue="general">
  <Tabs.List>
    <Tabs.Tab value="general">General</Tabs.Tab>
    <Tabs.Tab value="security">Security</Tabs.Tab>
  </Tabs.List>
  <Tabs.Panel value="general">General settings...</Tabs.Panel>
  <Tabs.Panel value="security">Security settings...</Tabs.Panel>
</Tabs>;
```

```tsx
// Accordion
import { Accordion } from "@mantine/core";

<Accordion>
  <Accordion.Item value="faq-1">
    <Accordion.Control>How does billing work?</Accordion.Control>
    <Accordion.Panel>Monthly billing starts on signup date.</Accordion.Panel>
  </Accordion.Item>
  <Accordion.Item value="faq-2">
    <Accordion.Control>Can I cancel anytime?</Accordion.Control>
    <Accordion.Panel>Yes, cancel anytime from settings.</Accordion.Panel>
  </Accordion.Item>
</Accordion>;
```

**Why good:** Consistent compound component pattern (Component.Sub), `useDisclosure` manages open/close state without manual useState boilerplate

---

### Pattern 4: Styling with CSS Modules and Styles API

Mantine v7 uses CSS Modules as the primary styling approach. The PostCSS preset provides responsive mixins and `light-dark()`.

#### CSS Modules

```css
/* feature-card.module.css */
.card {
  padding: var(--mantine-spacing-md);
  border-radius: var(--mantine-radius-md);
  background-color: light-dark(
    var(--mantine-color-white),
    var(--mantine-color-dark-6)
  );

  @mixin hover {
    box-shadow: var(--mantine-shadow-md);
  }

  @mixin smaller-than 48em {
    padding: var(--mantine-spacing-sm);
  }
}

.title {
  font-weight: 700;
  color: light-dark(var(--mantine-color-black), var(--mantine-color-white));
}
```

```tsx
import { Card, Text } from "@mantine/core";
import classes from "./feature-card.module.css";

export function FeatureCard({ title, children }: FeatureCardProps) {
  return (
    <Card className={classes.card}>
      <Text className={classes.title}>{title}</Text>
      {children}
    </Card>
  );
}
```

#### Styles API (classNames and styles props)

Every Mantine component exposes named selectors for inner elements:

```tsx
// Target specific inner elements with classNames
<TextInput
  classNames={{
    root: classes.inputRoot,
    input: classes.inputField,
    label: classes.inputLabel,
  }}
/>

// Or inline styles for quick overrides
<TextInput
  styles={{
    input: { backgroundColor: "var(--mantine-color-blue-0)" },
    label: { fontWeight: 700 },
  }}
/>
```

#### Style Props

All Mantine components support shorthand style props with responsive object syntax:

```tsx
import { Box } from "@mantine/core";

<Box
  p="md"
  bg="blue.1"
  c="blue.9"
  w={{ base: "100%", sm: 400, lg: 600 }}
  fz="sm"
  ta="center"
/>;
```

**Why good:** CSS Modules have zero runtime overhead, Styles API targets inner elements without source modification, style props enable rapid prototyping with responsive breakpoints

---

### Pattern 5: Theming with createTheme

Customize the entire library through the theme object. Theme is deeply merged with Mantine defaults.

```tsx
import {
  createTheme,
  MantineProvider,
  virtualColor,
  Button,
} from "@mantine/core";

const BRAND_COLORS = [
  "#f0e4ff",
  "#d9b8ff",
  "#c28dff",
  "#aa61ff",
  "#9336ff",
  "#7b0bff",
  "#6700d9",
  "#5300b3",
  "#3f008c",
  "#2b0066",
] as const;

const theme = createTheme({
  // Colors - each color is a 10-shade tuple (index 0 lightest, 9 darkest)
  colors: {
    brand: [...BRAND_COLORS],
    // virtualColor switches based on color scheme
    surface: virtualColor({
      name: "surface",
      dark: "dark",
      light: "gray",
    }),
  },
  primaryColor: "brand",
  primaryShade: { light: 6, dark: 8 },

  // Typography
  fontFamily: "Inter, sans-serif",
  headings: { fontFamily: "Inter, sans-serif" },

  // Layout
  defaultRadius: "md",

  // Component defaults - override props and styles globally
  components: {
    Button: Button.extend({
      defaultProps: {
        variant: "filled",
        size: "sm",
      },
    }),
  },
});
```

**Why good:** Colors are 10-shade tuples enabling automatic shade selection, `virtualColor` handles dark/light mode switching, component defaults reduce prop repetition across the app

See [examples/theming.md](examples/theming.md) for custom color generation, theme extension, and component default override patterns.

---

### Pattern 6: Color Scheme (Light/Dark/Auto)

Mantine supports `light`, `dark`, and `auto` color schemes with localStorage persistence.

```tsx
import {
  useMantineColorScheme,
  useComputedColorScheme,
  ActionIcon,
} from "@mantine/core";

export function ColorSchemeToggle() {
  const { setColorScheme } = useMantineColorScheme();
  const computedScheme = useComputedColorScheme("light");

  return (
    <ActionIcon
      variant="outline"
      onClick={() =>
        setColorScheme(computedScheme === "dark" ? "light" : "dark")
      }
    >
      {computedScheme === "dark" ? <SunIcon /> : <MoonIcon />}
    </ActionIcon>
  );
}
```

**Critical:** Use `useComputedColorScheme` (not `useMantineColorScheme().colorScheme`) for toggle logic. When set to `"auto"`, `colorScheme` returns `"auto"` not the resolved value.

```tsx
// MantineProvider configuration for color scheme
<MantineProvider theme={theme} defaultColorScheme="auto">
  {/* App */}
</MantineProvider>
```

**Conditional visibility:**

```tsx
// Built-in props for scheme-conditional rendering
<Button lightHidden>Only visible in dark mode</Button>
<Button darkHidden>Only visible in light mode</Button>
```

**Why good:** `auto` respects system preference, localStorage persists user choice, `useComputedColorScheme` resolves `auto` to actual value

---

### Pattern 7: @mantine/form (useForm)

Full form management with validation, nested fields, and list operations.

```tsx
import { useForm } from "@mantine/form";
import { TextInput, Checkbox, Button, Group, Box } from "@mantine/core";

export function SignupForm() {
  const form = useForm({
    mode: "uncontrolled",
    initialValues: {
      email: "",
      name: "",
      termsAccepted: false,
    },
    validate: {
      email: (value) => (/^\S+@\S+$/.test(value) ? null : "Invalid email"),
      name: (value) =>
        value.length < 2 ? "Name must be at least 2 characters" : null,
      termsAccepted: (value) => (value ? null : "You must accept terms"),
    },
  });

  return (
    <Box component="form" onSubmit={form.onSubmit(handleSubmit)}>
      <TextInput
        label="Name"
        withAsterisk
        key={form.key("name")}
        {...form.getInputProps("name")}
      />
      <TextInput
        label="Email"
        withAsterisk
        key={form.key("email")}
        {...form.getInputProps("email")}
      />
      <Checkbox
        label="I accept the terms"
        key={form.key("termsAccepted")}
        {...form.getInputProps("termsAccepted", { type: "checkbox" })}
      />
      <Group mt="md" justify="flex-end">
        <Button type="submit">Submit</Button>
      </Group>
    </Box>
  );
}
```

#### Cross-field Validation

```tsx
const form = useForm({
  mode: "uncontrolled",
  initialValues: { password: "", confirmPassword: "" },
  validate: {
    confirmPassword: (value, values) =>
      value !== values.password ? "Passwords do not match" : null,
  },
});
```

#### Nested Fields and Lists

```tsx
const form = useForm({
  mode: "uncontrolled",
  initialValues: {
    employees: [{ name: "", email: "" }],
  },
});

// Add item
form.insertListItem("employees", { name: "", email: "" });

// Remove item
form.removeListItem("employees", index);

// Access nested fields with dot notation
form.getInputProps("employees.0.name");
form.getInputProps("employees.0.email");
```

**Why good:** `getInputProps` auto-binds value, onChange, and error to inputs; `mode: "uncontrolled"` (default) avoids re-renders on every keystroke; `form.key()` is required for uncontrolled mode to maintain React key stability

See [examples/forms.md](examples/forms.md) for Zod resolver integration, dynamic list forms, and validation timing options.

---

### Pattern 8: @mantine/hooks

Utility hooks that solve common React patterns.

```tsx
import { useState } from "react";
import {
  useDisclosure,
  useDebouncedValue,
  useMediaQuery,
  useClickOutside,
  useClipboard,
} from "@mantine/hooks";

// useDisclosure - boolean state with handlers
const [opened, { open, close, toggle }] = useDisclosure(false);

// useDebouncedValue - debounce any value
const [search, setSearch] = useState("");
const [debounced] = useDebouncedValue(search, 300);

// useMediaQuery - responsive logic in JS
const isMobile = useMediaQuery("(max-width: 48em)");

// useClickOutside - close on outside click
const ref = useClickOutside(() => close());

// useClipboard - copy to clipboard with timeout
const clipboard = useClipboard({ timeout: 2000 });
clipboard.copy("text to copy");
// clipboard.copied is true for 2000ms after copy
```

**Why good:** Purpose-built hooks eliminate boilerplate, `useDebouncedValue` handles cleanup automatically, `useMediaQuery` returns `undefined` during SSR (safe for hydration)

---

### Pattern 9: @mantine/notifications

Toast notification system with queue management.

```tsx
// Root setup (once)
import { Notifications } from "@mantine/notifications";
import "@mantine/notifications/styles.css";

<MantineProvider>
  <Notifications position="top-right" />
  <App />
</MantineProvider>;
```

```tsx
// Show notifications anywhere
import { notifications } from "@mantine/notifications";

// Basic notification
notifications.show({
  title: "Success",
  message: "Your changes have been saved",
  color: "green",
});

// Loading notification that updates
const id = notifications.show({
  loading: true,
  title: "Uploading file",
  message: "Please wait...",
  autoClose: false,
  withCloseButton: false,
});

// Update to success
notifications.update({
  id,
  loading: false,
  title: "Upload complete",
  message: "File has been uploaded",
  color: "green",
  autoClose: 3000,
});

// Clean all
notifications.clean();
```

**Why good:** Queue management prevents notification flooding, `update` pattern handles async operations elegantly, consistent positioning across the app

---

### Pattern 10: @mantine/dates

Date components built on dayjs. Requires separate package and CSS import.

```bash
npm install @mantine/dates dayjs
```

```tsx
import "@mantine/dates/styles.css";
import { DatePickerInput, DatesProvider } from "@mantine/dates";

// Wrap with DatesProvider for locale/firstDayOfWeek
<DatesProvider settings={{ locale: "en", firstDayOfWeek: 0 }}>
  <App />
</DatesProvider>;

// v7: Date objects
const [date, setDate] = useState<Date | null>(null);
// v8: string values in "YYYY-MM-DD" format
// const [date, setDate] = useState<string | null>(null);
<DatePickerInput
  label="Pick date"
  placeholder="Pick date"
  value={date}
  onChange={setDate}
/>;

// v7: Date range
const [range, setRange] = useState<[Date | null, Date | null]>([null, null]);
// v8: const [range, setRange] = useState<[string | null, string | null]>([null, null]);
<DatePickerInput
  type="range"
  label="Date range"
  value={range}
  onChange={setRange}
/>;
```

**Why good:** dayjs is lightweight (2KB), DatesProvider centralizes locale settings, type parameter controls single/range/multiple selection modes

> **v8 note:** Mantine v8 changed all `@mantine/dates` components from `Date` objects to `"YYYY-MM-DD"` strings. `DatesProvider` no longer supports the `timezone` option.

</patterns>

---

**Detailed Resources:**

- [examples/core.md](examples/core.md) - MantineProvider setup, CSS Modules patterns, Styles API, style props, PostCSS mixins
- [examples/theming.md](examples/theming.md) - Custom colors, component defaults, virtualColor, theme extension
- [examples/forms.md](examples/forms.md) - useForm validation, Zod resolver, nested fields, dynamic lists
- [reference.md](reference.md) - Decision frameworks, component selection, anti-patterns, quick reference

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- **Using `createStyles`** - Removed in v7. Use CSS Modules (`.module.css`) instead
- **Missing PostCSS preset** - Responsive mixins (`@mixin smaller-than`), `light-dark()`, and `rem()` will not work
- **Missing `@mantine/core/styles.css` import** - Components will render unstyled
- **Providing fewer than 10 shades for custom colors** - Mantine requires exactly 10-shade tuples, TypeScript will error

**Medium Priority Issues:**

- **Using `colorScheme` directly for toggle logic** - Returns `"auto"` when set to auto; use `useComputedColorScheme` to get resolved `"light"` or `"dark"`
- **Forgetting `form.key()` in uncontrolled mode** - Required for React key stability when using `mode: "uncontrolled"` with `getInputProps`
- **Not importing package-specific CSS** - `@mantine/dates/styles.css`, `@mantine/notifications/styles.css` must be imported separately if using those packages
- **Overriding styles with inline `style` prop** - Use `classNames`/`styles` Styles API or CSS Modules to target inner elements properly

**Gotchas & Edge Cases:**

- **`mantineHtmlProps` required for SSR** - Must be spread on `<html>` element to prevent hydration mismatches
- **`ColorSchemeScript` must be in `<head>`** - Prevents flash of wrong color scheme before hydration
- **Style props use theme values, not CSS values** - `p="md"` resolves to `theme.spacing.md`, not the string `"md"`
- **Color dot notation** - `color="blue.6"` accesses shade 6 of the blue palette, not a CSS color name
- **`useMediaQuery` returns `undefined` during SSR** - Handle the initial render state to prevent hydration mismatch
- **PostCSS breakpoint variables must match Mantine defaults** - If you change `theme.breakpoints`, update `postcss.config.cjs` variables too
- **v8 exists (released May 2025)** - Key v8 changes: `@mantine/dates` uses `"YYYY-MM-DD"` strings instead of `Date` objects, `DatesProvider` drops `timezone`, `CodeHighlight` drops highlight.js. Check [migration guide](https://mantine.dev/guides/7x-to-8x/) if upgrading
- **`light-dark()` is a PostCSS function, not native CSS** - Requires `postcss-preset-mantine` to compile

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST wrap your app in `MantineProvider` and import `@mantine/core/styles.css` at the root)**

**(You MUST install and configure `postcss-preset-mantine` for CSS Modules mixins and responsive utilities)**

**(You MUST use CSS Modules (`.module.css`) for custom component styles - `createStyles` was removed in v7)**

**(You MUST provide 10-shade color tuples when adding custom colors to the theme)**

**Failure to follow these rules will cause unstyled components, broken responsive layouts, and TypeScript errors.**

</critical_reminders>
