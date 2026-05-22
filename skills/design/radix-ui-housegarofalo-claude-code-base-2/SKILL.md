---
name: radix-ui
description: Build accessible React components with Radix UI primitives. Covers unstyled components, accessibility features, composition patterns, and styling integration. Use for accessible UI development, custom design systems, and headless component architecture.
---

# Radix UI Primitives

Build accessible, unstyled React component primitives that you can customize with your own styles.

## Instructions

1. **Use primitives** - Radix provides behavior, you provide styles
2. **Maintain accessibility** - Don't remove built-in ARIA handling
3. **Compose components** - Build complex UIs from primitive parts
4. **Style as needed** - Use CSS, Tailwind, or CSS-in-JS
5. **Handle events** - Use provided callbacks for full control

## Installation

```bash
# Install individual primitives
npm install @radix-ui/react-dialog
npm install @radix-ui/react-dropdown-menu
npm install @radix-ui/react-tabs
npm install @radix-ui/react-accordion
npm install @radix-ui/react-popover
npm install @radix-ui/react-tooltip
npm install @radix-ui/react-select
npm install @radix-ui/react-checkbox
```

## Core Components

### Dialog

```tsx
import * as Dialog from '@radix-ui/react-dialog';

export function DialogDemo() {
  return (
    <Dialog.Root>
      <Dialog.Trigger asChild>
        <button className="px-4 py-2 bg-blue-600 text-white rounded-lg">
          Open Dialog
        </button>
      </Dialog.Trigger>

      <Dialog.Portal>
        <Dialog.Overlay className="fixed inset-0 bg-black/50 animate-fade-in" />
        <Dialog.Content className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white rounded-xl p-6 w-full max-w-md shadow-xl animate-scale-in">
          <Dialog.Title className="text-lg font-semibold">
            Edit Profile
          </Dialog.Title>
          <Dialog.Description className="text-gray-500 mt-2">
            Make changes to your profile here.
          </Dialog.Description>

          <div className="mt-4 space-y-4">
            <input
              className="w-full px-3 py-2 border rounded-lg"
              placeholder="Name"
            />
          </div>

          <div className="mt-6 flex justify-end gap-3">
            <Dialog.Close asChild>
              <button className="px-4 py-2 border rounded-lg">
                Cancel
              </button>
            </Dialog.Close>
            <button className="px-4 py-2 bg-blue-600 text-white rounded-lg">
              Save
            </button>
          </div>

          <Dialog.Close asChild>
            <button
              className="absolute top-4 right-4 p-1"
              aria-label="Close"
            >
              <XIcon />
            </button>
          </Dialog.Close>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
```

### Dropdown Menu

```tsx
import * as DropdownMenu from '@radix-ui/react-dropdown-menu';

export function DropdownMenuDemo() {
  return (
    <DropdownMenu.Root>
      <DropdownMenu.Trigger asChild>
        <button className="p-2 rounded-lg hover:bg-gray-100">
          <MenuIcon />
        </button>
      </DropdownMenu.Trigger>

      <DropdownMenu.Portal>
        <DropdownMenu.Content
          className="min-w-[200px] bg-white rounded-lg shadow-lg border p-1 animate-slide-down"
          sideOffset={5}
        >
          <DropdownMenu.Item className="px-3 py-2 rounded-md hover:bg-gray-100 cursor-pointer outline-none focus:bg-gray-100">
            Edit
          </DropdownMenu.Item>
          <DropdownMenu.Item className="px-3 py-2 rounded-md hover:bg-gray-100 cursor-pointer outline-none focus:bg-gray-100">
            Duplicate
          </DropdownMenu.Item>

          <DropdownMenu.Separator className="h-px bg-gray-200 my-1" />

          <DropdownMenu.Item className="px-3 py-2 rounded-md hover:bg-red-50 text-red-600 cursor-pointer outline-none focus:bg-red-50">
            Delete
          </DropdownMenu.Item>

          <DropdownMenu.Arrow className="fill-white" />
        </DropdownMenu.Content>
      </DropdownMenu.Portal>
    </DropdownMenu.Root>
  );
}
```

### Tabs

```tsx
import * as Tabs from '@radix-ui/react-tabs';

export function TabsDemo() {
  return (
    <Tabs.Root defaultValue="account" className="w-full">
      <Tabs.List className="flex border-b">
        <Tabs.Trigger
          value="account"
          className="px-4 py-2 border-b-2 border-transparent data-[state=active]:border-blue-600 data-[state=active]:text-blue-600"
        >
          Account
        </Tabs.Trigger>
        <Tabs.Trigger
          value="password"
          className="px-4 py-2 border-b-2 border-transparent data-[state=active]:border-blue-600 data-[state=active]:text-blue-600"
        >
          Password
        </Tabs.Trigger>
      </Tabs.List>

      <Tabs.Content value="account" className="p-4">
        <h3 className="font-semibold">Account Settings</h3>
        <p className="text-gray-500 mt-2">
          Manage your account settings and preferences.
        </p>
      </Tabs.Content>

      <Tabs.Content value="password" className="p-4">
        <h3 className="font-semibold">Change Password</h3>
        <p className="text-gray-500 mt-2">
          Update your password here.
        </p>
      </Tabs.Content>
    </Tabs.Root>
  );
}
```

### Accordion

```tsx
import * as Accordion from '@radix-ui/react-accordion';
import { ChevronDownIcon } from '@radix-ui/react-icons';

export function AccordionDemo() {
  return (
    <Accordion.Root type="single" collapsible className="w-full">
      <Accordion.Item value="item-1" className="border-b">
        <Accordion.Header>
          <Accordion.Trigger className="flex justify-between items-center w-full py-4 text-left font-medium hover:underline group">
            Is it accessible?
            <ChevronDownIcon className="transition-transform group-data-[state=open]:rotate-180" />
          </Accordion.Trigger>
        </Accordion.Header>
        <Accordion.Content className="overflow-hidden data-[state=open]:animate-slide-down data-[state=closed]:animate-slide-up">
          <div className="pb-4 text-gray-500">
            Yes. It adheres to the WAI-ARIA design pattern.
          </div>
        </Accordion.Content>
      </Accordion.Item>

      <Accordion.Item value="item-2" className="border-b">
        <Accordion.Header>
          <Accordion.Trigger className="flex justify-between items-center w-full py-4 text-left font-medium hover:underline group">
            Is it unstyled?
            <ChevronDownIcon className="transition-transform group-data-[state=open]:rotate-180" />
          </Accordion.Trigger>
        </Accordion.Header>
        <Accordion.Content className="overflow-hidden data-[state=open]:animate-slide-down data-[state=closed]:animate-slide-up">
          <div className="pb-4 text-gray-500">
            Yes. It's unstyled by default, giving you full control.
          </div>
        </Accordion.Content>
      </Accordion.Item>
    </Accordion.Root>
  );
}
```

### Select

```tsx
import * as Select from '@radix-ui/react-select';
import { ChevronDownIcon, CheckIcon } from '@radix-ui/react-icons';

export function SelectDemo() {
  return (
    <Select.Root>
      <Select.Trigger className="inline-flex items-center justify-between px-4 py-2 border rounded-lg min-w-[200px] bg-white">
        <Select.Value placeholder="Select a fruit" />
        <Select.Icon>
          <ChevronDownIcon />
        </Select.Icon>
      </Select.Trigger>

      <Select.Portal>
        <Select.Content className="bg-white rounded-lg shadow-lg border overflow-hidden">
          <Select.Viewport className="p-1">
            <Select.Group>
              <Select.Label className="px-3 py-2 text-xs text-gray-500">
                Fruits
              </Select.Label>

              <Select.Item
                value="apple"
                className="flex items-center px-3 py-2 rounded-md cursor-pointer outline-none hover:bg-gray-100 data-[highlighted]:bg-gray-100"
              >
                <Select.ItemText>Apple</Select.ItemText>
                <Select.ItemIndicator className="ml-auto">
                  <CheckIcon />
                </Select.ItemIndicator>
              </Select.Item>

              <Select.Item
                value="banana"
                className="flex items-center px-3 py-2 rounded-md cursor-pointer outline-none hover:bg-gray-100 data-[highlighted]:bg-gray-100"
              >
                <Select.ItemText>Banana</Select.ItemText>
                <Select.ItemIndicator className="ml-auto">
                  <CheckIcon />
                </Select.ItemIndicator>
              </Select.Item>
            </Select.Group>
          </Select.Viewport>
        </Select.Content>
      </Select.Portal>
    </Select.Root>
  );
}
```

### Tooltip

```tsx
import * as Tooltip from '@radix-ui/react-tooltip';

export function TooltipDemo() {
  return (
    <Tooltip.Provider delayDuration={300}>
      <Tooltip.Root>
        <Tooltip.Trigger asChild>
          <button className="p-2 rounded-lg hover:bg-gray-100">
            <InfoIcon />
          </button>
        </Tooltip.Trigger>

        <Tooltip.Portal>
          <Tooltip.Content
            className="bg-gray-900 text-white px-3 py-2 rounded-lg text-sm animate-fade-in"
            sideOffset={5}
          >
            This is a tooltip
            <Tooltip.Arrow className="fill-gray-900" />
          </Tooltip.Content>
        </Tooltip.Portal>
      </Tooltip.Root>
    </Tooltip.Provider>
  );
}
```

### Checkbox

```tsx
import * as Checkbox from '@radix-ui/react-checkbox';
import { CheckIcon } from '@radix-ui/react-icons';

export function CheckboxDemo() {
  return (
    <div className="flex items-center gap-2">
      <Checkbox.Root
        id="terms"
        className="w-5 h-5 rounded border-2 border-gray-300 flex items-center justify-center data-[state=checked]:bg-blue-600 data-[state=checked]:border-blue-600"
      >
        <Checkbox.Indicator>
          <CheckIcon className="w-4 h-4 text-white" />
        </Checkbox.Indicator>
      </Checkbox.Root>
      <label htmlFor="terms" className="text-sm">
        Accept terms and conditions
      </label>
    </div>
  );
}
```

## Data Attributes for Styling

Radix uses data attributes for component states:

```css
/* Style based on state */
[data-state="open"] { /* open state */ }
[data-state="closed"] { /* closed state */ }
[data-state="checked"] { /* checked state */ }
[data-state="unchecked"] { /* unchecked state */ }
[data-disabled] { /* disabled state */ }
[data-highlighted] { /* keyboard highlighted */ }
[data-placeholder] { /* placeholder shown */ }

/* Tailwind variants */
data-[state=open]:rotate-180
data-[state=checked]:bg-blue-600
data-[disabled]:opacity-50
```

## Accessibility Features

All Radix primitives include:
- Keyboard navigation
- Focus management
- ARIA attributes
- Screen reader support
- Reduced motion support

## Best Practices

1. **Use asChild** - Merge props with your own components
2. **Portal overlays** - Use Portal for dialogs/menus to escape stacking contexts
3. **Handle focus** - Let Radix manage focus, don't override
4. **Data attributes** - Use data-state for styling, not JS
5. **Composition** - Combine primitives for complex patterns

## When to Use

- Building custom design systems
- Projects requiring full styling control
- Accessible component development
- Headless UI architecture
- React applications of any scale

## Notes

- Primitives are completely unstyled
- Each primitive is a separate package
- Works with any styling solution
- TypeScript types included
- MIT licensed
