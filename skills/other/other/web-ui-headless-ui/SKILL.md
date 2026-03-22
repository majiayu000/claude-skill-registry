---
name: web-ui-headless-ui
description: Unstyled accessible UI components by Tailwind Labs
---

# Headless UI Patterns

> **Quick Guide:** Headless UI provides completely unstyled, fully accessible UI components designed for Tailwind CSS. Use compound component patterns (Menu/MenuButton/MenuItems/MenuItem), `data-*` attributes for styling states, built-in anchor positioning for floating elements, and the `transition` prop for CSS-powered animations. All components handle ARIA, keyboard navigation, and focus management automatically. **Current: v2.2.9 (React only).**

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use the v2 compound component anatomy - e.g. Menu/MenuButton/MenuItems/MenuItem - never render raw divs with click handlers)**

**(You MUST use `data-*` attributes for styling states (data-open, data-focus, data-selected, data-hover, data-active) - NOT render props for class toggling)**

**(You MUST use the `anchor` prop on floating panels (MenuItems, ListboxOptions, ComboboxOptions, PopoverPanel) instead of manual positioning)**

**(You MUST use the `transition` prop with data-closed/data-enter/data-leave classes for animations - NOT the legacy Transition component enter/leave props)**

</critical_requirements>

---

**Auto-detection:** Headless UI, headlessui, @headlessui/react, Dialog, DialogPanel, DialogTitle, Menu, MenuButton, MenuItems, MenuItem, Listbox, ListboxButton, ListboxOptions, ListboxOption, Combobox, ComboboxInput, ComboboxButton, ComboboxOptions, ComboboxOption, Popover, PopoverButton, PopoverPanel, TabGroup, TabList, Tab, TabPanel, Disclosure, DisclosureButton, DisclosurePanel, Switch, RadioGroup, Radio, Transition, Field, Label, Description, Input, Fieldset, Legend, Checkbox, CloseButton, data-closed, data-open, anchor positioning

**When to use:**

- Building accessible overlay components (dialogs, popovers, dropdowns, menus) with utility-class styling
- Creating fully custom select/combobox/listbox controls with keyboard navigation
- Implementing tabs, disclosure/accordion, switch, radio group, or checkbox with custom styling
- Needing automatic ARIA attributes, focus trapping, and keyboard handling without visual opinions

**When NOT to use:**

- Pre-styled component library desired (use a design system or pre-built component kit)
- Simple native HTML elements suffice (plain `<select>`, `<input type="checkbox">`, `<details>`)
- Non-React projects (v2 is React-only; Vue version remains at v1)
- Need `asChild` polymorphism or more granular primitive control (consider alternative headless libraries)

**Package Installation:**

```bash
npm install @headlessui/react
```

**Examples:**

- [Core Patterns](examples/core.md) - Data-attribute styling, anchor positioning, transitions, `as` prop, `useClose`
- [Dialog & Modal](examples/dialog.md) - Modal overlays, form dialogs, slide-over panels, transitions
- [Menu & Dropdowns](examples/menu.md) - Dropdown action menus, sections, icons, keyboard shortcuts
- [Listbox & Combobox](examples/listbox-combobox.md) - Custom select, autocomplete, virtual scrolling
- [Tabs](examples/tabs.md) - Horizontal/vertical tabs, controlled state, badges
- [Popover & Disclosure](examples/popover-disclosure.md) - Floating panels, accordion, standalone transitions
- [Switch, RadioGroup & Checkbox](examples/switch-radio.md) - Toggle, option selection, checkbox
- [Form Components](examples/forms.md) - Field, Input, Label, Fieldset, cascading disabled state

**Quick API reference:** [reference.md](reference.md)

---

<philosophy>

## Philosophy

Headless UI provides **behavior-only** components: accessibility, keyboard navigation, focus management, and state handling are built in, while **all visual styling is your responsibility**. Style entirely via `className` using utility classes or any CSS approach.

**Core Design Principles:**

- **Unstyled by default**: No CSS shipped. Style entirely via `className`.
- **Accessible out of the box**: ARIA roles, attributes, and keyboard interactions are automatic.
- **Compound components**: Each UI pattern is composed of multiple coordinated parts (e.g., `Menu` + `MenuButton` + `MenuItems` + `MenuItem`).
- **Data attributes for state**: Components expose `data-open`, `data-focus`, `data-selected`, `data-hover`, `data-active`, `data-disabled`, `data-checked` for CSS-based state styling.
- **Built-in anchor positioning**: Floating panels (menus, listboxes, comboboxes, popovers) use Floating UI internally for automatic viewport-aware positioning.
- **Transition support**: The `transition` prop enables CSS transitions using `data-closed`, `data-enter`, `data-leave` attributes.

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Dialog (Modal)

Dialogs are always controlled components. You manage `open` state and pass `onClose`. Focus is automatically trapped within the dialog panel.

```tsx
<Dialog
  open={isOpen}
  onClose={() => setIsOpen(false)}
  className="relative z-50"
>
  <DialogBackdrop
    transition
    className="fixed inset-0 bg-black/30 duration-300 data-[closed]:opacity-0"
  />
  <div className="fixed inset-0 flex w-screen items-center justify-center p-4">
    <DialogPanel
      transition
      className="max-w-lg rounded-xl bg-white p-12 duration-300 data-[closed]:scale-95 data-[closed]:opacity-0"
    >
      <DialogTitle className="text-lg font-bold">Title</DialogTitle>
      <Description>Description text</Description>
    </DialogPanel>
  </div>
</Dialog>
```

**Key points:** `open`/`onClose` are required, `DialogTitle` sets aria-labelledby, `transition` enables CSS animations via `data-[closed]`

Full examples: [examples/dialog.md](examples/dialog.md)

---

### Pattern 2: Menu (Dropdown)

Menus provide dropdown behavior: arrow key navigation, type-ahead search, auto-close on selection.

```tsx
<Menu>
  <MenuButton className="rounded-md bg-gray-800 px-4 py-2 text-white">
    Options
  </MenuButton>
  <MenuItems
    anchor="bottom start"
    transition
    className="w-52 rounded-xl bg-white p-1 shadow-lg [--anchor-gap:8px] data-[closed]:scale-95 data-[closed]:opacity-0"
  >
    <MenuItem>
      <button className="block w-full rounded-lg px-3 py-1.5 text-left data-[focus]:bg-gray-100">
        Edit
      </button>
    </MenuItem>
  </MenuItems>
</Menu>
```

**Key points:** `anchor` handles positioning, `data-[focus]` styles keyboard/mouse focus, items auto-close menu on click, use `MenuSection`/`MenuSeparator` for grouped menus

Full examples: [examples/menu.md](examples/menu.md)

---

### Pattern 3: Listbox (Custom Select)

Listbox replaces the native `<select>` with full styling control and keyboard navigation.

```tsx
<Listbox value={selected} onChange={setSelected}>
  <ListboxButton className="w-full rounded-lg py-2 pl-3 pr-10 text-left shadow-md">
    {selected.name}
  </ListboxButton>
  <ListboxOptions
    anchor="bottom"
    className="w-[var(--button-width)] rounded-xl bg-white p-1 shadow-lg [--anchor-gap:4px]"
  >
    <ListboxOption
      value={item}
      className="px-3 py-1.5 data-[focus]:bg-blue-100 data-[selected]:font-semibold"
    >
      {item.name}
    </ListboxOption>
  </ListboxOptions>
</Listbox>
```

**Key points:** Objects compared by `id` field by default (use `by` prop for custom), `multiple` prop for multi-select, `name` for form submission, `--button-width` matches dropdown to trigger width

Full examples: [examples/listbox-combobox.md](examples/listbox-combobox.md)

---

### Pattern 4: Combobox (Autocomplete)

Combobox combines a text input with a filterable dropdown. Filtering logic is your responsibility.

```tsx
<Combobox value={selected} onChange={setSelected} onClose={() => setQuery("")}>
  <ComboboxInput
    displayValue={(item: Item | null) => item?.name ?? ""}
    onChange={(e) => setQuery(e.target.value)}
  />
  <ComboboxOptions
    anchor="bottom"
    className="w-[var(--input-width)] rounded-xl bg-white shadow-lg [--anchor-gap:4px]"
  >
    <ComboboxOption
      value={item}
      className="px-3 py-1.5 data-[focus]:bg-blue-100"
    >
      {item.name}
    </ComboboxOption>
  </ComboboxOptions>
</Combobox>
```

**Key points:** `onClose` resets query state, `displayValue` formats selected item in input, `virtual={{ options }}` for 1000+ items (built-in virtualization), `--input-width` matches dropdown to input

Full examples: [examples/listbox-combobox.md](examples/listbox-combobox.md)

---

### Pattern 5: Popover

Popovers display floating non-modal content. They close on outside click, Escape, or tab-away.

```tsx
<Popover>
  <PopoverButton className="text-sm font-semibold data-[open]:text-blue-600">
    Solutions
  </PopoverButton>
  <PopoverPanel
    anchor="bottom start"
    transition
    className="w-80 rounded-xl bg-white p-4 shadow-lg [--anchor-gap:8px] data-[closed]:opacity-0"
  >
    <CloseButton as="a" href="/analytics">
      Analytics
    </CloseButton>
  </PopoverPanel>
</Popover>
```

**Key points:** `CloseButton` closes popover on click (useful for nav links), `PopoverGroup` manages sibling popover focus, `modal` prop for focus trapping

Full examples: [examples/popover-disclosure.md](examples/popover-disclosure.md)

---

### Pattern 6: Tabs

Tab components manage tabbed content with keyboard navigation (arrow keys, Home/End).

```tsx
<TabGroup>
  <TabList className="flex gap-4 border-b">
    <Tab className="px-3 py-2 text-sm data-[selected]:border-blue-500 data-[selected]:text-blue-600">
      Tab Name
    </Tab>
  </TabList>
  <TabPanels>
    <TabPanel>Content</TabPanel>
  </TabPanels>
</TabGroup>
```

**Key points:** `vertical` prop switches to Up/Down arrows, `selectedIndex`/`onChange` for controlled mode, `manual` requires Enter/Space to activate, Tab/TabPanel order matches automatically

Full examples: [examples/tabs.md](examples/tabs.md)

---

### Pattern 7: Disclosure (Accordion)

Disclosure provides show/hide toggle for accordion-style content.

```tsx
<Disclosure>
  <DisclosureButton className="flex w-full items-center justify-between rounded-lg bg-gray-100 px-4 py-2">
    Question text
    <span className="size-5 data-[open]:rotate-180" aria-hidden="true">
      &#9662;
    </span>
  </DisclosureButton>
  <DisclosurePanel
    transition
    className="px-4 pb-2 text-sm duration-200 data-[closed]:opacity-0"
  >
    Answer text
  </DisclosurePanel>
</Disclosure>
```

**Key points:** Each Disclosure manages its own state independently, `defaultOpen` for initial state, `data-[open]` on button for icon rotation

Full examples: [examples/popover-disclosure.md](examples/popover-disclosure.md)

---

### Pattern 8: Switch, RadioGroup & Checkbox

Toggle, option selection, and checkbox controls with form integration.

```tsx
// Switch
<Field className="flex items-center justify-between">
  <Label passive>Email notifications</Label>
  <Switch checked={enabled} onChange={setEnabled} name="notifications"
    className="group h-6 w-11 rounded-full bg-gray-200 data-[checked]:bg-blue-600">
    <span className="size-5 rounded-full bg-white group-data-[checked]:translate-x-5" />
  </Switch>
</Field>

// RadioGroup
<RadioGroup value={selected} onChange={setSelected}>
  <Radio value={option} className="data-[checked]:border-blue-500 data-[focus]:ring-2">
    <Label>{option.name}</Label>
  </Radio>
</RadioGroup>

// Checkbox
<Checkbox checked={agreed} onChange={setAgreed} name="terms"
  className="group size-5 rounded border data-[checked]:bg-blue-500">
  <svg className="size-4 text-white opacity-0 group-data-[checked]:opacity-100" viewBox="0 0 16 16" fill="currentColor">
    <path d="M12.207 4.793a1 1 0 010 1.414l-5 5a1 1 0 01-1.414 0l-2-2a1 1 0 011.414-1.414L6.5 9.086l4.293-4.293a1 1 0 011.414 0z" />
  </svg>
</Checkbox>
```

**Key points:** `passive` on Label prevents toggle on click (when label is distant from control), `name` enables form submission, `data-[checked]`/`group-data-[checked]` for state styling, `indeterminate` on Checkbox for third state

Full examples: [examples/switch-radio.md](examples/switch-radio.md)

---

### Pattern 9: Form Components

Headless UI v2 form primitives auto-generate IDs and wire ARIA attributes.

```tsx
<Fieldset className="space-y-6">
  <Legend className="text-lg font-semibold">Shipping Details</Legend>
  <Field>
    <Label className="text-sm font-medium">Full name</Label>
    <Description className="text-sm text-gray-500">Helper text</Description>
    <Input
      name="name"
      className="data-[focus]:outline-2 data-[focus]:outline-blue-500"
    />
  </Field>
  <Field disabled>
    <Label className="data-[disabled]:opacity-50">Promo code</Label>
    <Input className="data-[disabled]:bg-gray-100" />
  </Field>
</Fieldset>
```

**Key points:** Field auto-generates `id`/`aria-labelledby`/`aria-describedby` (no manual `htmlFor`), disabled Field cascades to all children, Fieldset+Legend group related fields

Full examples: [examples/forms.md](examples/forms.md)

---

### Pattern 10: Anchor Positioning

Floating panels accept an `anchor` prop for viewport-aware positioning.

```tsx
// Position values: "top", "top start", "top end", "bottom", "bottom start", "bottom end",
//                  "left", "left start", "left end", "right", "right start", "right end"

<MenuItems anchor="bottom start" className="[--anchor-gap:8px] [--anchor-offset:4px] [--anchor-padding:12px]">

// Match trigger width
<ListboxOptions className="w-[var(--button-width)]">
<ComboboxOptions className="w-[var(--input-width)]">

// Object syntax for full control
<MenuItems anchor={{ to: "bottom start", gap: 8, offset: 4, padding: 12 }}>
```

**CSS Variables:** `--anchor-gap` (space between trigger/panel), `--anchor-offset` (horizontal offset), `--anchor-padding` (viewport edge minimum), `--button-width`/`--input-width` (trigger dimensions)

---

### Pattern 11: Data Attributes for Styling

Headless UI v2 exposes data attributes on all components for CSS-based state styling. Preferred over render props.

| Attribute       | Components                                           | Purpose                           |
| --------------- | ---------------------------------------------------- | --------------------------------- |
| `data-open`     | Dialog, Menu, Popover, Disclosure, Listbox, Combobox | Component is open                 |
| `data-closed`   | All with transition support                          | Closed state (for transitions)    |
| `data-focus`    | MenuItem, ListboxOption, ComboboxOption, Tab, inputs | Has keyboard/mouse focus          |
| `data-selected` | ListboxOption, ComboboxOption, Tab                   | Currently selected                |
| `data-checked`  | Checkbox, Switch, Radio                              | Control is checked/on             |
| `data-disabled` | All interactive components                           | Component is disabled             |
| `data-hover`    | All interactive components                           | Mouse hover (ignored on touch)    |
| `data-active`   | All interactive components                           | Mouse press (cleared on drag-off) |

```tsx
// Direct styling
<MenuItem><button className="data-[focus]:bg-blue-100 data-[disabled]:opacity-50">Edit</button></MenuItem>

// Parent state styling with group
<Switch className="group ...">
  <span className="group-data-[checked]:translate-x-5" />
</Switch>

// Transition styling
<DialogPanel transition className="duration-200 data-[closed]:opacity-0 data-[closed]:scale-95">
```

</patterns>

---

<decision_framework>

## Decision Framework

### Component Selection

```
What interaction pattern do you need?

Modal blocking interaction?
  -> Dialog (close on Escape, outside click, focus trapped)

Dropdown with actions?
  -> Menu (arrow key navigation, type-ahead, auto-close on select)

Custom select (single/multi)?
  -> Listbox (keyboard navigation, form integration)

Searchable select?
  -> Combobox (text input + filterable dropdown)
  -> Large list (1000+)? -> Use virtual prop

Floating non-modal content?
  -> Popover (click to toggle, close on outside click)

Tabbed content?
  -> TabGroup (arrow key navigation, automatic ARIA)

Show/hide toggle?
  -> Disclosure (single toggle, accordion-style)

Boolean toggle?
  -> Switch (on/off, form integration)

Option selection from small set?
  -> RadioGroup (arrow key cycling, card-style options)

Custom checkbox?
  -> Checkbox (checked/unchecked/indeterminate)

Form field with auto ARIA?
  -> Field + Label + Description + Input/Select/Textarea
```

### Transition Approach

```
How to animate components?

Simple fade/scale?
  -> transition prop + data-[closed] classes (recommended)

Different enter/leave animations?
  -> Stack data attributes: data-[closed]:data-[enter]: / data-[closed]:data-[leave]:

Coordinated multi-element animations?
  -> Transition + TransitionChild components

JavaScript animation library?
  -> Use static prop to disable internal state management
  -> Conditionally render based on your animation library's presence detection
```

</decision_framework>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Using render props for class toggling instead of `data-*` attributes (breaks RSC compatibility, verbose code)
- Missing controlled state for Dialog (`open` and `onClose` are both required)
- Building manual dropdown/popover positioning instead of using the `anchor` prop
- Not providing DialogTitle (screen readers have no context for the dialog)

**Medium Priority Issues:**

- Using the legacy Transition component `enter`/`enterFrom`/`enterTo`/`leave`/`leaveFrom`/`leaveTo` class props instead of `data-[closed]`/`data-[enter]`/`data-[leave]` (v2.1+ pattern is simpler)
- Manually wiring `id`, `htmlFor`, `aria-labelledby`, `aria-describedby` when Field/Label/Description auto-handle this
- Not using `onClose` callback to reset Combobox query state
- Forgetting `multiple` prop when Listbox/Combobox should support multiple selection

**Common Mistakes:**

- Filtering Combobox options inside the component instead of deriving from state (causes stale filter results)
- Using `data-[state]` with CSS `transition` but forgetting `duration-*` class (no visible animation)
- Nesting a Popover inside a Dialog without considering focus trap implications
- Using Menu for navigation (Menu is for actions; use links/buttons directly for navigation, or Popover for nav panels)

**Gotchas and Edge Cases:**

- `data-hover` is intelligently ignored on touch devices to prevent sticky hover states (this is intentional, not a bug)
- `data-active` is removed when dragging off the element (unlike CSS `:active` which persists)
- `data-changing` on Switch/Checkbox is only true for two animation frames (used for transition timing)
- Dialog renders in a `#headlessui-portal-root` container automatically (no explicit Portal component needed)
- Combobox `onClose` fires when dropdown closes (use it to reset query, not `onChange`)
- Listbox/Combobox compare objects by `id` field by default; use `by` prop for custom comparison
- Tab component renders as `Fragment` by default, not `button` (wrap content or use `as="button"`)
- Virtual scrolling in Combobox uses a render function on `ComboboxOptions`, not mapping `ComboboxOption` children
- Headless UI v2 is React-only; the Vue version remains at v1.x

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use the v2 compound component anatomy - e.g. Menu/MenuButton/MenuItems/MenuItem - never render raw divs with click handlers)**

**(You MUST use `data-*` attributes for styling states (data-open, data-focus, data-selected, data-hover, data-active) - NOT render props for class toggling)**

**(You MUST use the `anchor` prop on floating panels (MenuItems, ListboxOptions, ComboboxOptions, PopoverPanel) instead of manual positioning)**

**(You MUST use the `transition` prop with data-closed/data-enter/data-leave classes for animations - NOT the legacy Transition component enter/leave props)**

**Failure to follow these rules will break accessibility, keyboard navigation, and viewport-aware positioning.**

</critical_reminders>
