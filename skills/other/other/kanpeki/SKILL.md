---
name: kanpeki
description: "Use Kanpeki component library in React projects. Activate when user wants to add, use, customize, or compose accessible UI components from Kanpeki (@kanpeki/*). Covers installation, component patterns, forms, theming, and dark mode with React Aria Components + Tailwind CSS 4.1 + CVA."
---

# Kanpeki

Kanpeki is a copy-paste component library for React. Components are copied into your project (not installed as npm packages) via the shadcn CLI. Built on **React Aria Components** (accessibility), **CVA beta** (variants), and **Tailwind CSS 4.1** (styling).

Docs: https://kanpeki.vercel.app

## Quick Start

### 1. Install Dependencies

```bash
npm install cva@beta tailwind-merge tailwindcss-motion tailwindcss-react-aria-components react-aria-components -D
```

Remove shadcn defaults if present:
```bash
npm remove class-variance-authority clsx tw-animate-css
```

### 2. Create CVA Utility

`src/lib/cva.ts`:
```ts
import { defineConfig } from "cva";
import { twMerge } from "tailwind-merge";

export const { cva, cx: cn, compose } = defineConfig({
  hooks: {
    onComplete: (className) => twMerge(className),
  },
});
```

### 3. Configure Styles

Add to `globals.css`: Tailwind imports, plugins (`tailwindcss-react-aria-components`, `tailwindcss-motion`), `@custom-variant dark`, and OKLCH color tokens via `@theme inline`.

See [references/installation-setup.md](references/installation-setup.md) for full CSS.

### 4. Add Components

```bash
npx shadcn@latest add @kanpeki/button
npx shadcn@latest add @kanpeki/dialog
npx shadcn@latest add @kanpeki/field
```

Components are copied to `~/components/ui/<name>/`. You own the code.

## Component Architecture

Each component has: `index.ts` (exports), `<name>.tsx` (implementation), `styles.ts` (CVA variants).

### Simple Components

Single export. Example:

```tsx
import { Button } from "~/components/ui/button";

<Button variant="outline" size="lg">Click me</Button>
```

### Multi-Part Components

Namespace exports for compound components:

```tsx
import { Dialog } from "~/components/ui/dialog";

<Dialog.Root>
  <Button>Open</Button>
  <Dialog.Overlay>
    <Dialog.Modal>
      <Dialog.Content>
        <Dialog.Header>
          <Dialog.Title>Title</Dialog.Title>
          <Dialog.Description>Description</Dialog.Description>
        </Dialog.Header>
        <Dialog.Footer>
          <Button>Save</Button>
        </Dialog.Footer>
        <Dialog.Close />
      </Dialog.Content>
    </Dialog.Modal>
  </Dialog.Overlay>
</Dialog.Root>
```

Multi-part components with namespace exports: Accordion, Breadcrumb, ButtonGroup, Calendar, Card, Carousel, Chart, Combobox, DateField, DatePicker, Dialog, Drawer, Field, InputGroup, ListBox, Menu, NumberField, Pagination, Popover, RadioGroup, Resizable, ScrollArea, SearchField, Select, Sheet, Sidebar, Slider, Table, Tabs, Toast, ToggleGroup, Tooltip.

See [references/component-patterns.md](references/component-patterns.md) for full examples.

### Key Pattern: `composeRenderProps`

Always use `composeRenderProps` from `react-aria-components` when wrapping React Aria primitives. This ensures state-based selectors (`pressed:`, `selected:`, etc.) work.

```tsx
import { composeRenderProps } from "react-aria-components";

className={composeRenderProps(className, (className) =>
  Styles({ className, variant })
)}
```

For plain HTML elements (`div`, `p`), call CVA directly: `className={Styles({ className })}`.

## Form System

3-layer architecture: **Form** > **Field** > **Input component**.

### Field Composition

```tsx
import { Field } from "~/components/ui/field";
import { Input } from "~/components/ui/input";
import { TextField } from "~/components/ui/text-field";

<Field.Root render={<TextField type="email" isRequired />}>
  <Field.Label>Email</Field.Label>
  <Input placeholder="john@example.com" />
  <Field.Description>Help text</Field.Description>
  <Field.Error />
</Field.Root>
```

`Field.Root`'s `render` prop connects to a React Aria form primitive (TextField, Select, NumberField, etc.) for automatic label association and validation.

### InputGroup

```tsx
import { InputGroup } from "~/components/ui/input-group";

<InputGroup.Root>
  <InputGroup.Addon><SearchIcon /></InputGroup.Addon>
  <InputGroup.Input placeholder="Search..." />
</InputGroup.Root>
```

### TanStack Form

```tsx
<form.Field name="title">
  {(field) => (
    <Field.Root
      render={
        <TextField
          isInvalid={field.state.meta.isTouched && !field.state.meta.isValid}
          onChange={field.handleChange}
          onBlur={field.handleBlur}
          value={field.state.value}
        />
      }
    >
      <Field.Label>Title</Field.Label>
      <Input />
      <Field.Error errors={field.state.meta.errors} />
    </Field.Root>
  )}
</form.Field>
```

See [references/form-system.md](references/form-system.md) for full TanStack Form example with Zod validation.

## Styling & Theming

- **CVA** — variant definitions in `styles.ts`. Import `cva` from `~/lib/cva` (not `cva` directly).
- **`cn()`** — class merging utility from `~/lib/cva`. Wraps `twMerge`.
- **OKLCH colors** — defined in `globals.css` via `@theme inline`. Use `light-dark()` for automatic dark mode.
- **Dark mode** — `next-themes` (class strategy) + CSS `light-dark()`. Components auto-switch.
- **React Aria selectors** — `pressed:`, `selected:`, `disabled:`, `entering:`, `exiting:`, `focus-visible:`.
- **Animations** — `tailwindcss-motion` plugin: `motion-opacity-in`, `motion-scale-in-95`, `motion-duration-200`.

Override styles by passing `className` (twMerge resolves conflicts) or editing `styles.ts` directly.

See [references/styling-and-theming.md](references/styling-and-theming.md) for full token reference and CVA deep dive.

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Using `className={Styles(...)}` on React Aria components | Use `composeRenderProps` — required for state selectors |
| Missing `"use client"` directive | All interactive components need it (React Aria is client-only) |
| Importing `cva` from `"cva"` | Import from `~/lib/cva` — includes `twMerge` hook |
| Old shadcn deps installed (`class-variance-authority`, `clsx`) | Remove them, use `cva@beta` + `tailwind-merge` |
| Using `active:` for press state | Use `pressed:` — React Aria prefix |
| Using `@/` path alias | Kanpeki uses `~/` |

## Component List

Install any component: `npx shadcn@latest add @kanpeki/<name>`

**Layout & Structure:** card, separator, aspect-ratio, resizable, scroll-area, sidebar, collapsible, carousel

**Form Inputs:** input, textarea, text-field, number-field, search-field, checkbox, radio-group, select, combobox, autocomplete, switch, slider, date-field, date-picker, calendar, input-otp, dropzone, field, form, input-group

**Buttons & Actions:** button, button-group, link, link-button, toggle, toggle-group

**Overlays:** dialog, drawer, sheet, popover, tooltip, menu

**Data Display:** table, list-box, accordion, tabs, avatar, badge, keyboard, chart

**Feedback:** alert, toast, progress, spinner, skeleton

**Navigation:** breadcrumb, pagination

**Utilities:** label

## References

- [Installation & Setup](references/installation-setup.md) — full CSS, CVA config, dark mode, path alias
- [Component Patterns](references/component-patterns.md) — Button + Dialog examples, namespace pattern, customization
- [Form System](references/form-system.md) — Field/InputGroup/ButtonGroup API, TanStack Form + Zod example
- [Styling & Theming](references/styling-and-theming.md) — CVA deep dive, OKLCH tokens, React Aria selectors, animations
