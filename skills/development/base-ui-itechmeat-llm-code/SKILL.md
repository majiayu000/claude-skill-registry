---
name: base-ui
description: "Base UI unstyled React components. Covers forms, menus, overlays, composition. Keywords: @base-ui/react, render props."
version: "1.1.0"
release_date: "2026-01-15"
---

# Base UI (React)

Base UI provides unstyled, composable React components. This skill focuses on assembling multi-part components, composing with the `render` prop, and meeting accessibility requirements while you supply styling.

## When to use

Use this skill when the user wants to:

- Build UI with `@base-ui/react` primitives.
- Compose unstyled components with custom markup and styling.
- Implement menus, overlays, toasts, and toolbars.
- Build accessible form controls and grouped inputs.

## Quick navigation (references)

### Utilities

- references/csp-provider.md
- references/direction-provider.md
- references/merge-props.md
- references/use-render.md

### Forms & inputs

- references/form.md
- references/fieldset.md
- references/input.md
- references/number-field.md
- references/radio.md
- references/select.md
- references/slider.md
- references/switch.md

### Feedback & status

- references/meter.md
- references/progress.md
- references/toast.md

### Menus, navigation, overlays

- references/menu.md
- references/menubar.md
- references/navigation-menu.md
- references/popover.md
- references/preview-card.md
- references/tooltip.md

### Toggles & controls

- references/toggle.md
- references/toggle-group.md
- references/toolbar.md

### Layout & separators

- references/scroll-area.md
- references/separator.md

## Core concepts to apply

- **Unstyled primitives**: all visuals come from your CSS/Tailwind/CSS Modules. Base UI handles behavior and accessibility.
- **Multi-part anatomy**: most components follow `Root` + subparts (`Trigger`, `Popup`, `Item`, etc.). Assemble them explicitly.
- **`render` prop**: replace the default element or wrap with your own component; when using the function form, merge props manually with `mergeProps`.
- **State-driven styling**: many parts expose data attributes such as `data-[popup-open]`, `data-[highlighted]`, `data-[pressed]`, `data-[checked]`, `data-[invalid]`, etc.
- **Portals for overlays**: use `Portal` + `Positioner` + `Popup` for popovers, menus, tooltips, select, navigation menu content, and preview cards.

## Recipes

### 1) Build accessible forms quickly

- Wrap inputs with `Form` for submission and error aggregation.
- Use `Field.Root` with a `name`, then `Field.Label`, `Field.Control`, and `Field.Error` for labels and errors.
- Group related fields with `Fieldset.Root` + `Fieldset.Legend`.
- For `Radio` groups, either use `RadioGroup` with `aria-labelledby`, or render `RadioGroup` via `Fieldset.Root` and use `Field.Label` for each option.
- Ensure **every** form control has an accessible name (label or `Field`/`Fieldset` labeling pattern).

### 2) Compose with `render` + `mergeProps`

- When passing a React element to `render`, Base UI merges props automatically.
- When passing a function to `render`, **merge** Base UI props and your props with `mergeProps`.
- Use `event.preventBaseUIHandler()` inside merged event handlers to stop Base UI’s internal behavior when needed (synthetic events only).

### 3) Overlays and menus (portaled UI)

- Build popups using `Root` + `Trigger` + `Portal` + `Positioner` + `Popup`.
- For menus and navigation, add `Item`, `Separator`, `Arrow`, and list/viewport parts as needed.
- `NavigationMenu.Link` supports `render` for framework router links.

### 4) Toasts

- Wrap the app (or a subtree) with `Toast.Provider`.
- Use `Toast.useToastManager()` to create toasts.
- Render a `Toast.Viewport` inside `Toast.Portal`, then map `toasts` to `Toast.Root` entries with `Toast.Content`, `Toast.Title`, `Toast.Description`, and `Toast.Close`.

### 5) RTL and CSP constraints

- For RTL behavior, wrap with `DirectionProvider` and also set `dir="rtl"` (provider does not set the DOM direction).
- For strict CSP, wrap with `CSPProvider` and pass `nonce`, or disable inline style elements if your app supplies external styles. Beware inline style **attributes** are not controlled by `CSPProvider`.

### 6) Sliders and ranges

- Single value sliders: one `Slider.Thumb`.
- Range sliders: pass an array and render a `Slider.Thumb` per value; add `index` for SSR alignment.
- Adjust thumb alignment with `thumbAlignment` when edge alignment is required.

## Critical prohibitions

- Do not omit accessible labels for inputs, sliders, switches, or radio groups.
- Do not expect Base UI to provide default styling; apply your own styles.
- Do not forget `Portal` for overlays that need to escape stacking/overflow contexts.
- Do not skip `mergeProps` when using the function form of `render`.

## Output expectations

When responding to the user, provide:

- The specific Base UI components to use (and their key parts).
- A brief assembly plan (Root + parts + portal/positioner where relevant).
- A short checklist for accessibility and state-driven styling.
