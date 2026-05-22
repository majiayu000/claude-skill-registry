---
name: web-ui-chakra-ui
description: Accessible React component library with style props and theming
---

# Chakra UI v3 Patterns

> **Quick Guide:** Chakra UI v3 is a composable, accessible React component library. Set up with `createSystem(defaultConfig)` and `ChakraProvider`. Style via props (`bg`, `p`, `color`), not className. Components are composable by default (`Dialog.Root`, `Dialog.Content`). Theme with design tokens and recipes via `defineConfig`. Dark mode uses semantic tokens (`bg.subtle`, `fg.muted`) and `_dark` condition. Removed `framer-motion` and `@emotion/styled` deps from v2 -- uses CSS animations and recipes instead.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST wrap your app with `ChakraProvider value={system}` where system is created via `createSystem(defaultConfig)`)**

**(You MUST use composable component patterns (`Dialog.Root`, `Dialog.Content`) -- v3 removed closed component APIs)**

**(You MUST use style props (`bg`, `p`, `color`) or the `chakra` factory for styling -- not raw className strings)**

**(You MUST prefer semantic tokens (`bg.subtle`, `fg.muted`) or `_dark` condition for dark mode -- avoid `useColorModeValue` when tokens suffice)**

</critical_requirements>

---

**Auto-detection:** Chakra UI, @chakra-ui/react, ChakraProvider, createSystem, defaultConfig, chakra factory, style props, defineRecipe, defineSlotRecipe, colorPalette, semantic tokens, Ark UI

**When to use:**

- Building React applications with accessible, composable UI components
- Rapid prototyping with style props (inline CSS via props)
- Implementing design token-based theming with dark mode support
- Creating component variants with the recipe system
- Projects that value accessibility and keyboard navigation out of the box

**When NOT to use:**

- Projects already using another component library (MUI, Ant Design, shadcn/ui)
- Projects requiring zero-runtime CSS (Chakra uses Emotion at runtime)
- Projects that need Tailwind CSS integration (use shadcn/ui instead)
- Extremely bundle-size-sensitive applications

**Key patterns covered:**

- Provider setup with `createSystem` and `ChakraProvider`
- Style props for layout, spacing, color, and typography
- Responsive design with object and array syntax
- Theme customization with tokens, semantic tokens, and recipes
- Composable components (Dialog, Menu, Popover, Drawer)
- Form components with Field pattern
- Dark mode via semantic tokens and `_dark` condition
- `chakra` factory for custom styled components

---

<philosophy>

## Philosophy

Chakra UI v3 is built on three pillars: **Ark UI** (headless component logic and accessibility), **Panda CSS-inspired APIs** (design tokens and recipes, powered by Emotion at runtime), and **Park UI** (default design system). Components are composable by default -- you compose `Dialog.Root > Dialog.Content > Dialog.Body` instead of passing everything as props to a single `<Dialog>`.

**Key v3 principles:**

1. **Composable over configurable** -- compound components replace prop-heavy APIs
2. **Tokens over hardcoded values** -- colors, spacing, radii reference design tokens
3. **Recipes over runtime styles** -- variant-based styling replaces runtime theme functions
4. **Semantic tokens for dark mode** -- `bg.subtle` adapts automatically, no conditional logic
5. **CSS animations over JS** -- removed framer-motion, uses native CSS for animations

**What Chakra UI handles vs what other skills handle:**

- Chakra UI: component structure, style props, design tokens, recipes, composition, accessibility
- Your form library: validation schemas, submission logic, form state management
- Your data layer: server state, caching, mutations

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Provider Setup

Every Chakra v3 app needs `createSystem` and `ChakraProvider`. Add `@layer` directive for proper CSS ordering.

```tsx
// theme.ts
import { createSystem, defaultConfig, defineConfig } from "@chakra-ui/react";

// Basic: use defaults
export const system = createSystem(defaultConfig);

// Custom: extend with your tokens
const config = defineConfig({
  theme: {
    tokens: {
      colors: {
        brand: {
          50: { value: "#ffe5f1" },
          500: { value: "#d53f8c" },
          900: { value: "#521b41" },
        },
      },
    },
  },
});

export const system = createSystem(defaultConfig, config);
```

```tsx
// app.tsx
import { ChakraProvider } from "@chakra-ui/react";
import { system } from "./theme";

export function App({ children }: { children: React.ReactNode }) {
  return <ChakraProvider value={system}>{children}</ChakraProvider>;
}
```

```css
/* Required CSS layer directive */
@layer reset, base, tokens, recipes;
```

**Why good:** `createSystem` merges your config with defaults, tokens become CSS variables, recipes generate atomic classes

See [examples/core.md](examples/core.md) for framework-specific setup (SPA, SSR).

---

### Pattern 2: Style Props

Style props are the primary way to style elements. They map directly to CSS properties with shorthand aliases and token values.

```tsx
import { Box, Flex, Text } from "@chakra-ui/react";

// Style props with token values
<Box bg="blue.500" color="white" p="4" rounded="md" shadow="lg">
  Styled via props
</Box>

// Shorthand aliases
<Box
  mt="4"       // marginTop
  px="6"       // paddingX (left + right)
  w="full"     // width: 100%
  maxW="md"    // maxWidth
  mx="auto"    // marginX: auto (centering)
/>

// Layout with Flex
<Flex gap="4" align="center" justify="between" wrap="wrap">
  <Text fontSize="lg" fontWeight="bold">Title</Text>
  <Text color="fg.muted">Subtitle</Text>
</Flex>
```

**Why good:** co-located styles, type-safe token values, responsive-ready, no separate CSS files

```tsx
// BAD: using className strings with Chakra components
<Box className="bg-blue-500 p-4 rounded-md">Wrong approach</Box>
```

**Why bad:** bypasses token system, no type safety, loses dark mode adaptation

See [examples/core.md](examples/core.md) for complete style prop reference.

---

### Pattern 3: Responsive Design

Use object syntax (recommended) or array syntax for responsive values. Mobile-first with `base` as default.

```tsx
// Object syntax (preferred) -- explicit breakpoint names
<Box
  p={{ base: "4", md: "6", lg: "8" }}
  fontSize={{ base: "sm", md: "md", lg: "lg" }}
  display={{ base: "block", md: "flex" }}
/>

// Array syntax -- positional: [base, sm, md, lg, xl, 2xl]
<Box p={["4", "4", "6", "6", "8"]} />

// Skip breakpoints with undefined
<Text fontWeight={["medium", undefined, undefined, "bold"]} />

// Advanced: range targeting
<Text fontWeight={{ mdToXl: "bold" }} />

// Visibility helpers
<Box hideBelow="md">Desktop only</Box>
<Box hideFrom="md">Mobile only</Box>
```

**Why good:** mobile-first approach, named breakpoints are self-documenting, range targeting avoids repetition

---

### Pattern 4: Composable Components

v3 uses compound components with dot notation. All complex components follow `Root > Trigger > Content > ...` pattern.

```tsx
import { Dialog, Button } from "@chakra-ui/react";

// Composable dialog
function ConfirmDialog() {
  return (
    <Dialog.Root>
      <Dialog.Trigger asChild>
        <Button>Open</Button>
      </Dialog.Trigger>
      <Dialog.Backdrop />
      <Dialog.Content>
        <Dialog.Header>Confirm Action</Dialog.Header>
        <Dialog.Body>Are you sure?</Dialog.Body>
        <Dialog.Footer>
          <Dialog.CloseTrigger asChild>
            <Button variant="outline">Cancel</Button>
          </Dialog.CloseTrigger>
          <Button colorPalette="red">Confirm</Button>
        </Dialog.Footer>
      </Dialog.Content>
    </Dialog.Root>
  );
}
```

```tsx
// BAD: v2-style closed component API (removed in v3)
<Modal isOpen={isOpen} onClose={onClose}>
  <ModalOverlay />
  <ModalContent>
    <ModalHeader>Title</ModalHeader>
    <ModalBody>Content</ModalBody>
  </ModalContent>
</Modal>
```

**Why bad:** v2 API removed in v3, `isOpen`/`onClose` replaced by `open`/`onOpenChange`, separate imports replaced by dot notation

See [examples/composable-components.md](examples/composable-components.md) for Menu, Popover, Drawer, and controlled patterns.

---

### Pattern 5: Recipes and Variants

Recipes define reusable component styles with variants. Use `defineRecipe` for single-part, `defineSlotRecipe` for multi-part components.

```tsx
import { defineRecipe } from "@chakra-ui/react";

const badgeRecipe = defineRecipe({
  base: {
    display: "inline-flex",
    alignItems: "center",
    fontWeight: "medium",
    rounded: "full",
  },
  variants: {
    variant: {
      solid: { bg: "colorPalette.500", color: "white" },
      outline: { borderWidth: "1px", borderColor: "colorPalette.500" },
      subtle: { bg: "colorPalette.100", color: "colorPalette.800" },
    },
    size: {
      sm: { px: "2", py: "0.5", fontSize: "xs" },
      md: { px: "3", py: "1", fontSize: "sm" },
    },
  },
  defaultVariants: { variant: "subtle", size: "sm" },
});
```

Register recipes in your system config via `defineConfig({ theme: { recipes: { badge: badgeRecipe } } })`.

Use with `useRecipe` hook or the `chakra` factory (recommended):

```tsx
import { chakra } from "@chakra-ui/react";

const Badge = chakra("span", badgeRecipe);

// Usage
<Badge variant="solid" colorPalette="green" size="md">
  Active
</Badge>;
```

See [examples/theming.md](examples/theming.md) for slot recipes, custom tokens, and semantic tokens.

---

### Pattern 6: Dark Mode

Chakra v3 uses semantic tokens that adapt to color mode automatically. No conditional logic needed.

```tsx
// RECOMMENDED: semantic tokens -- adapt automatically
<Box bg="bg.subtle" color="fg.default" borderColor="border.muted">
  This adapts to light/dark mode automatically
</Box>

// Direct _dark condition for overrides
<Box bg="white" _dark={{ bg: "gray.800" }}>
  Explicit dark mode override
</Box>

// Inline condition syntax
<Box bg={{ base: "white", _dark: "gray.800" }}>
  Inline dark override
</Box>
```

Setup requires `ColorModeProvider` and the CLI snippet:

```bash
npx @chakra-ui/cli snippet add color-mode
```

```tsx
import { ColorModeProvider } from "@/components/ui/color-mode";
import { ChakraProvider } from "@chakra-ui/react";
import { system } from "./theme";

function App({ children }: { children: React.ReactNode }) {
  return (
    <ChakraProvider value={system}>
      <ColorModeProvider>{children}</ColorModeProvider>
    </ChakraProvider>
  );
}
```

**Why good:** semantic tokens are the cleanest approach, `_dark` condition for one-offs, avoids `useColorModeValue` boilerplate when tokens cover the use case

See [examples/theming.md](examples/theming.md) for theme toggle component and semantic token reference.

---

### Pattern 7: Form Components

Use `Field` for form layout with labels, help text, and error messages. Works with any form library.

```tsx
import { Field, Input, Button, Stack } from "@chakra-ui/react";

function LoginForm() {
  return (
    <Stack gap="4">
      <Field.Root required>
        <Field.Label>Email</Field.Label>
        <Input type="email" placeholder="you@example.com" />
        <Field.HelperText>We will never share your email.</Field.HelperText>
      </Field.Root>

      <Field.Root required invalid={!!errors?.password}>
        <Field.Label>Password</Field.Label>
        <Input type="password" />
        {errors?.password && (
          <Field.ErrorMessage>{errors.password}</Field.ErrorMessage>
        )}
      </Field.Root>

      <Button type="submit" colorPalette="blue">
        Sign In
      </Button>
    </Stack>
  );
}
```

**Why good:** Field is form-library-agnostic, provides accessible labels and error messaging, composable structure

See [examples/core.md](examples/core.md) for more form patterns.

</patterns>

---

**Detailed Resources:**

- [examples/core.md](examples/core.md) - Provider setup, style props reference, layout components, form patterns
- [examples/theming.md](examples/theming.md) - Tokens, semantic tokens, recipes, slot recipes, dark mode
- [examples/composable-components.md](examples/composable-components.md) - Dialog, Menu, Popover, Drawer, controlled state
- [reference.md](reference.md) - Decision frameworks, v2-to-v3 migration, anti-patterns

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- **Using v2 APIs** -- `isOpen`/`onClose` props, `useDisclosure`, `ChakraProvider` without `value` prop, `extendTheme` are all removed
- **Missing `@layer` CSS directive** -- without `@layer reset, base, tokens, recipes;` styles may not apply correctly
- **Importing `framer-motion`** -- removed in v3; use CSS animations or Chakra's built-in motion
- **Using `@emotion/styled`** -- removed in v3; use `chakra` factory or style props instead

**Medium Priority Issues:**

- **Boolean props with `is` prefix** -- `isDisabled` is now `disabled`, `isLoading` is now `loading`, `isInvalid` is now `invalid`
- **`spacing` prop on Stack** -- renamed to `gap` to align with CSS
- **Importing icons from `@chakra-ui/icons`** -- removed in v3; use your preferred icon library
- **Using `useColorModeValue` when semantic tokens suffice** -- prefer `bg.subtle`, `fg.muted` tokens or `_dark` condition; `useColorModeValue` still works but adds unnecessary boilerplate

**Common Mistakes:**

- **Separate component imports** -- `import { ListItem }` is now `List.Item` via dot notation
- **Hardcoding color values** -- use token values (`blue.500`) or semantic tokens (`colorPalette.500`)
- **Not using `asChild` for composition** -- the `as` prop has limited support; use `asChild` for polymorphism
- **Missing `ChakraProvider`** -- components silently fail without the provider context

**Gotchas & Edge Cases:**

- **`onOpenChange` callback shape** -- receives `{ open: boolean }` object, not a plain boolean: `onOpenChange={(details) => setOpen(details.open)}`
- **CSS layer order matters** -- `@layer reset, base, tokens, recipes;` must be in your root CSS
- **Snippet system** -- many "components" are CLI-generated snippets (`npx @chakra-ui/cli snippet add`), not installed packages
- **`colorPalette` prop** -- swaps the entire color context for a component tree; affects all children using `colorPalette.*` tokens
- **`defaultSystem` shortcut** -- for zero-config, import `defaultSystem` directly instead of calling `createSystem`

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST wrap your app with `ChakraProvider value={system}` where system is created via `createSystem(defaultConfig)`)**

**(You MUST use composable component patterns (`Dialog.Root`, `Dialog.Content`) -- v3 removed closed component APIs)**

**(You MUST use style props (`bg`, `p`, `color`) or the `chakra` factory for styling -- not raw className strings)**

**(You MUST prefer semantic tokens (`bg.subtle`, `fg.muted`) or `_dark` condition for dark mode -- avoid `useColorModeValue` when tokens suffice)**

**Failure to follow these rules will produce broken v2-style code that does not work with Chakra UI v3.**

</critical_reminders>
