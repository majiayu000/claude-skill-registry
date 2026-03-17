---
name: skeleton-ui
description: >
  Use Skeleton UI components instead of building custom markup. MUST be consulted
  when creating or modifying any UI: buttons, forms, dialogs, modals, drawers,
  navigation, tabs, accordions, tooltips, popovers, toasts, alerts, dropdowns,
  selects, switches, sliders, checkboxes, radios, tags, file uploads, avatars,
  progress bars, ratings, badges, cards, tables, inputs, textareas, segments,
  clipboards, or pin inputs.
---

# Skeleton UI Component Skill

## Core Principle

**Before building ANY UI element, check if Skeleton has a component or styled element for it.** Do not hand-roll markup when a Skeleton component exists. This catalog lists everything available.

## Import Pattern

```ts
import { ComponentName, Portal } from '@skeletonlabs/skeleton-svelte';
```

## Composition Pattern

Skeleton uses granular child components:

```svelte
<Avatar>
  <Avatar.Image src="..." />
  <Avatar.Fallback>JD</Avatar.Fallback>
</Avatar>
```

## Data Flow

- Props in, `onXxxChange` callbacks out (e.g., `onValueChange`, `onOpenChange`)
- Collections use `useListCollection()` helper for item mapping

## Positioned Content

Components that render floating/overlay content need `<Portal>`:
Combobox, Popover, Tooltip, Dialog, Select, Toast

---

## Component Catalog

### Layout & Navigation

| Component      | Use When                                                  |
| -------------- | --------------------------------------------------------- |
| **Navigation** | App-level nav bars, sidebar navigation                    |
| **Tabs**       | Switching between views/panels in the same context        |
| **Accordion**  | Collapsible sections, FAQ lists, expandable details       |
| **Segment**    | Toggle between a small set of options (like button group) |

### Overlays & Feedback

| Component    | Use When                                              |
| ------------ | ----------------------------------------------------- |
| **Dialog**   | Confirmation prompts, modal forms, detail views       |
| **Drawer**   | Side panels, mobile menus, supplementary content      |
| **Popover**  | Rich contextual content on click (menus, info panels) |
| **Tooltip**  | Brief hover hints for icons/buttons                   |
| **Toast**    | Temporary notifications, success/error messages       |
| **Alert**    | Inline banners, warnings, info messages               |
| **Progress** | Loading indicators, completion bars                   |

### Form Components

| Component      | Use When                                          |
| -------------- | ------------------------------------------------- |
| **Combobox**   | Searchable dropdown, autocomplete, multi-select   |
| **Select**     | Simple dropdown selection (no search needed)      |
| **Switch**     | Boolean toggles                                   |
| **Slider**     | Numeric range input                               |
| **Checkbox**   | Multiple selections from a list                   |
| **Radio**      | Single selection from a list                      |
| **TagsInput**  | Freeform tag/token entry                          |
| **FileUpload** | File selection with drag-and-drop                 |
| **Clipboard**  | Copy-to-clipboard buttons                         |
| **PinInput**   | Verification codes, OTP entry                     |

### Data Display

| Component  | Use When                                |
| ---------- | --------------------------------------- |
| **Avatar** | User/entity profile images with fallback |
| **Rating** | Star ratings, scoring displays          |

### Styled Elements (Tailwind classes, not components)

These are applied as CSS classes on standard HTML elements:

| Class        | Element       | Example                                              |
| ------------ | ------------- | ---------------------------------------------------- |
| `btn`        | `<button>`    | `<button class="btn preset-filled-primary-500">`     |
| `card`       | `<div>`       | `<div class="card p-4">`                             |
| `badge`      | `<span>`      | `<span class="badge preset-filled-primary-500">`     |
| `input`      | `<input>`     | `<input class="input" type="text" />`                |
| `select`     | `<select>`    | `<select class="select">`                            |
| `textarea`   | `<textarea>`  | `<textarea class="textarea">`                        |
| `table`      | `<table>`     | `<table class="table">`                              |
| `label`      | `<label>`     | `<label class="label">`                              |
| `progress`   | `<progress>`  | `<progress class="progress" value="50" max="100">`   |
| `hr`         | `<hr>`        | `<hr class="hr" />`                                  |

### Preset Classes

Style variants follow the pattern: `preset-{style}-{color}-{shade}`

- Styles: `filled`, `tonal`, `outlined`
- Colors: `primary`, `secondary`, `tertiary`, `success`, `warning`, `error`, `surface`
- Shade: typically `500`

Examples:
- `preset-filled-primary-500`
- `preset-tonal-error`
- `preset-outlined-surface-500`

---

## Documentation Lookup

When implementing UI, use **Context7 MCP** for accurate reference docs:

**Skeleton components** — full props, events, and examples:
```
Library ID: /websites/skeleton_dev_svelte
Query: "[ComponentName] component props examples usage"
```

**Tailwind CSS** — utility classes, modifiers, and layout:
```
Library ID: /tailwindlabs/tailwindcss.com
Query: "[topic] classes usage examples"
```

Look up Tailwind docs when unsure about utility classes (grid, flex, spacing, responsive modifiers, dark mode, etc.) rather than guessing class names. This is especially important for Skeleton's styled elements which are composed with Tailwind utilities.

## Decision Checklist

1. Is there a **Skeleton component** for this? (see catalog above) -> Use it
2. Is there a **styled element class** for this? (btn, card, badge, etc.) -> Use it
3. Neither exists? -> Build custom markup with Tailwind, matching Skeleton's design tokens
