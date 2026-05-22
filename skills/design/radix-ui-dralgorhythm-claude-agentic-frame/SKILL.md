---
name: radix-ui
description: Radix UI primitive patterns. Use when building accessible, unstyled UI components like dialogs, dropdowns, tooltips, tabs, and selects. Covers Tailwind styling, keyboard navigation, animations, and portal management.
---

# Radix UI

> **Platform:** Web only. For mobile modals/sheets, see the **expo-sdk** and **react-native-patterns** skills.

## Overview

Unstyled, accessible UI primitives for React with built-in keyboard navigation, focus management, and ARIA attributes. Designed to be composed with Tailwind CSS and Framer Motion.

**Version**: Latest (individual packages) or `radix-ui` unified package

**Install (individual packages)**:
```bash
pnpm add @radix-ui/react-dialog @radix-ui/react-dropdown-menu @radix-ui/react-select @radix-ui/react-tooltip @radix-ui/react-tabs
```

**Install (unified package)**:
```bash
pnpm add radix-ui
```

The unified `radix-ui` package bundles all primitives - use this for simpler dependency management.

## Workflows

**Adding a Dialog:**
1. [ ] Install: `pnpm add @radix-ui/react-dialog`
2. [ ] Import Dialog parts: Root, Trigger, Portal, Overlay, Content
3. [ ] Wrap Overlay and Content in Portal for proper stacking
4. [ ] Style with Tailwind and data-[state=] selectors
5. [ ] Test keyboard navigation (Esc to close, Tab trap)
6. [ ] Add Framer Motion animations if needed

**Adding a Select:**
1. [ ] Install: `pnpm add @radix-ui/react-select`
2. [ ] Import Select parts: Root, Trigger, Portal, Content, Item
3. [ ] Add Icon and Value to Trigger for visual feedback
4. [ ] Style open/closed states with data-[state=open]
5. [ ] Test keyboard (Arrow keys, Enter, Type-ahead)
6. [ ] Ensure proper z-index for Portal

**Adding Tooltips:**
1. [ ] Install: `pnpm add @radix-ui/react-tooltip`
2. [ ] Wrap app with TooltipProvider
3. [ ] Compose Trigger and Content for each tooltip
4. [ ] Set delayDuration for hover timing
5. [ ] Style with Tailwind arrows using data-[side=]
6. [ ] Verify screen reader announcements

## Dialog (Modal)

### Basic Modal Pattern

```tsx
// Individual package import
import * as Dialog from '@radix-ui/react-dialog';

// OR unified package import
// import { Dialog } from 'radix-ui';

function ModalExample() {
  return (
    <Dialog.Root>
      <Dialog.Trigger asChild>
        <button className="px-4 py-2 bg-blue-600 text-white rounded">
          Open Dialog
        </button>
      </Dialog.Trigger>

      <Dialog.Portal>
        <Dialog.Overlay className="fixed inset-0 bg-black/50 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0" />

        <Dialog.Content className="fixed left-[50%] top-[50%] translate-x-[-50%] translate-y-[-50%] max-h-[85vh] w-[90vw] max-w-[500px] rounded-lg bg-white p-6 shadow-lg data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[state=closed]:slide-out-to-left-1/2 data-[state=closed]:slide-out-to-top-[48%] data-[state=open]:slide-in-from-left-1/2 data-[state=open]:slide-in-from-top-[48%]">
          <Dialog.Title className="text-lg font-semibold mb-4">
            Dialog Title
          </Dialog.Title>

          <Dialog.Description className="text-sm text-gray-600 mb-4">
            Make changes to your profile here. Click save when you're done.
          </Dialog.Description>

          <div className="space-y-4">
            {/* Form content */}
            <input type="text" className="w-full px-3 py-2 border rounded" />
          </div>

          <div className="flex justify-end gap-2 mt-6">
            <Dialog.Close asChild>
              <button className="px-4 py-2 border rounded">Cancel</button>
            </Dialog.Close>
            <button className="px-4 py-2 bg-blue-600 text-white rounded">
              Save changes
            </button>
          </div>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
```

### Controlled Dialog

```tsx
import { useState } from 'react';
import * as Dialog from '@radix-ui/react-dialog';

function ControlledDialog() {
  const [open, setOpen] = useState(false);

  const handleSubmit = () => {
    // Process form
    setOpen(false);
  };

  return (
    <Dialog.Root open={open} onOpenChange={setOpen}>
      <Dialog.Trigger asChild>
        <button>Open</button>
      </Dialog.Trigger>
      {/* Portal, Overlay, Content... */}
    </Dialog.Root>
  );
}
```

### Dialog with Framer Motion

```tsx
import * as Dialog from '@radix-ui/react-dialog';
import { motion, AnimatePresence } from 'framer-motion';

function AnimatedDialog() {
  const [open, setOpen] = useState(false);

  return (
    <Dialog.Root open={open} onOpenChange={setOpen}>
      <Dialog.Trigger asChild>
        <button>Open</button>
      </Dialog.Trigger>

      <AnimatePresence>
        {open && (
          <Dialog.Portal forceMount>
            <Dialog.Overlay asChild>
              <motion.div
                className="fixed inset-0 bg-black/50"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
              />
            </Dialog.Overlay>

            <Dialog.Content asChild>
              <motion.div
                className="fixed left-[50%] top-[50%] max-w-[500px] rounded-lg bg-white p-6"
                initial={{ opacity: 0, scale: 0.95, x: '-50%', y: '-50%' }}
                animate={{ opacity: 1, scale: 1, x: '-50%', y: '-50%' }}
                exit={{ opacity: 0, scale: 0.95, x: '-50%', y: '-50%' }}
                transition={{ duration: 0.2 }}
              >
                {/* Content */}
              </motion.div>
            </Dialog.Content>
          </Dialog.Portal>
        )}
      </AnimatePresence>
    </Dialog.Root>
  );
}
```

## Select (Dropdown)

### Basic Select

```tsx
import * as Select from '@radix-ui/react-select';
import { ChevronDownIcon, CheckIcon } from '@radix-ui/react-icons';

function SelectExample() {
  return (
    <Select.Root defaultValue="apple">
      <Select.Trigger className="inline-flex items-center justify-between rounded px-4 py-2 text-sm bg-white border gap-2 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 data-[placeholder]:text-gray-400 min-w-[200px]">
        <Select.Value placeholder="Select a fruit..." />
        <Select.Icon>
          <ChevronDownIcon />
        </Select.Icon>
      </Select.Trigger>

      <Select.Portal>
        <Select.Content className="overflow-hidden bg-white rounded-md shadow-lg border">
          <Select.Viewport className="p-1">
            <Select.Item value="apple" className="relative flex items-center px-8 py-2 rounded text-sm hover:bg-blue-50 focus:bg-blue-100 outline-none cursor-pointer data-[disabled]:opacity-50 data-[disabled]:pointer-events-none">
              <Select.ItemIndicator className="absolute left-2">
                <CheckIcon />
              </Select.ItemIndicator>
              <Select.ItemText>Apple</Select.ItemText>
            </Select.Item>

            <Select.Item value="banana" className="relative flex items-center px-8 py-2 rounded text-sm hover:bg-blue-50 focus:bg-blue-100 outline-none cursor-pointer">
              <Select.ItemIndicator className="absolute left-2">
                <CheckIcon />
              </Select.ItemIndicator>
              <Select.ItemText>Banana</Select.ItemText>
            </Select.Item>

            <Select.Item value="orange" className="relative flex items-center px-8 py-2 rounded text-sm hover:bg-blue-50 focus:bg-blue-100 outline-none cursor-pointer">
              <Select.ItemIndicator className="absolute left-2">
                <CheckIcon />
              </Select.ItemIndicator>
              <Select.ItemText>Orange</Select.ItemText>
            </Select.Item>
          </Select.Viewport>
        </Select.Content>
      </Select.Portal>
    </Select.Root>
  );
}
```

### Grouped Select with Labels

```tsx
<Select.Root>
  <Select.Trigger>{/* ... */}</Select.Trigger>

  <Select.Portal>
    <Select.Content>
      <Select.Viewport>
        <Select.Group>
          <Select.Label className="px-8 py-2 text-xs font-semibold text-gray-500">
            Fruits
          </Select.Label>
          <Select.Item value="apple">{/* ... */}</Select.Item>
          <Select.Item value="banana">{/* ... */}</Select.Item>
        </Select.Group>

        <Select.Separator className="h-px bg-gray-200 my-1" />

        <Select.Group>
          <Select.Label className="px-8 py-2 text-xs font-semibold text-gray-500">
            Vegetables
          </Select.Label>
          <Select.Item value="carrot">{/* ... */}</Select.Item>
          <Select.Item value="broccoli">{/* ... */}</Select.Item>
        </Select.Group>
      </Select.Viewport>
    </Select.Content>
  </Select.Portal>
</Select.Root>
```

## Tooltip

### Basic Tooltip

```tsx
import * as Tooltip from '@radix-ui/react-tooltip';

// Wrap your app once
function App() {
  return (
    <Tooltip.Provider delayDuration={200}>
      <YourApp />
    </Tooltip.Provider>
  );
}

// Use in components
function TooltipExample() {
  return (
    <Tooltip.Root>
      <Tooltip.Trigger asChild>
        <button className="px-4 py-2 bg-gray-100 rounded">
          Hover me
        </button>
      </Tooltip.Trigger>

      <Tooltip.Portal>
        <Tooltip.Content
          className="bg-gray-900 text-white text-sm px-3 py-2 rounded shadow-lg max-w-xs data-[state=delayed-open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=delayed-open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=delayed-open]:zoom-in-95"
          sideOffset={5}
        >
          This is a helpful tooltip
          <Tooltip.Arrow className="fill-gray-900" />
        </Tooltip.Content>
      </Tooltip.Portal>
    </Tooltip.Root>
  );
}
```

### Tooltip with Dynamic Positioning

```tsx
<Tooltip.Content
  side="top"        // top | right | bottom | left
  align="center"    // start | center | end
  sideOffset={5}
  className="bg-gray-900 text-white px-3 py-2 rounded"
>
  Content
  <Tooltip.Arrow className="fill-gray-900" />
</Tooltip.Content>
```

## DropdownMenu

### Basic Dropdown Menu

```tsx
import * as DropdownMenu from '@radix-ui/react-dropdown-menu';

function DropdownExample() {
  return (
    <DropdownMenu.Root>
      <DropdownMenu.Trigger asChild>
        <button className="px-4 py-2 bg-white border rounded hover:bg-gray-50">
          Options
        </button>
      </DropdownMenu.Trigger>

      <DropdownMenu.Portal>
        <DropdownMenu.Content
          className="min-w-[220px] bg-white rounded-md shadow-lg border p-1"
          sideOffset={5}
        >
          <DropdownMenu.Item className="flex items-center px-3 py-2 text-sm rounded cursor-pointer hover:bg-blue-50 focus:bg-blue-100 outline-none">
            New Tab
            <span className="ml-auto text-xs text-gray-500">⌘T</span>
          </DropdownMenu.Item>

          <DropdownMenu.Item className="flex items-center px-3 py-2 text-sm rounded cursor-pointer hover:bg-blue-50 focus:bg-blue-100 outline-none">
            New Window
            <span className="ml-auto text-xs text-gray-500">⌘N</span>
          </DropdownMenu.Item>

          <DropdownMenu.Separator className="h-px bg-gray-200 my-1" />

          <DropdownMenu.Item
            className="flex items-center px-3 py-2 text-sm rounded cursor-pointer hover:bg-red-50 focus:bg-red-100 text-red-600 outline-none"
            onSelect={() => console.log('Delete')}
          >
            Delete
          </DropdownMenu.Item>
        </DropdownMenu.Content>
      </DropdownMenu.Portal>
    </DropdownMenu.Root>
  );
}
```

### Dropdown with Checkboxes and Radio Groups

```tsx
<DropdownMenu.Content>
  <DropdownMenu.CheckboxItem
    checked={showBookmarks}
    onCheckedChange={setShowBookmarks}
    className="flex items-center px-3 py-2 text-sm rounded cursor-pointer hover:bg-blue-50 outline-none"
  >
    <DropdownMenu.ItemIndicator className="mr-2">
      <CheckIcon />
    </DropdownMenu.ItemIndicator>
    Show Bookmarks
  </DropdownMenu.CheckboxItem>

  <DropdownMenu.Separator className="h-px bg-gray-200 my-1" />

  <DropdownMenu.RadioGroup value={view} onValueChange={setView}>
    <DropdownMenu.RadioItem
      value="grid"
      className="flex items-center px-3 py-2 text-sm rounded cursor-pointer hover:bg-blue-50 outline-none"
    >
      <DropdownMenu.ItemIndicator className="mr-2">
        <DotFilledIcon />
      </DropdownMenu.ItemIndicator>
      Grid View
    </DropdownMenu.RadioItem>

    <DropdownMenu.RadioItem value="list" className="flex items-center px-3 py-2 text-sm rounded cursor-pointer hover:bg-blue-50 outline-none">
      <DropdownMenu.ItemIndicator className="mr-2">
        <DotFilledIcon />
      </DropdownMenu.ItemIndicator>
      List View
    </DropdownMenu.RadioItem>
  </DropdownMenu.RadioGroup>
</DropdownMenu.Content>
```

## Tabs

### Basic Tabs

```tsx
import * as Tabs from '@radix-ui/react-tabs';

function TabsExample() {
  return (
    <Tabs.Root defaultValue="tab1" className="w-full">
      <Tabs.List className="flex border-b">
        <Tabs.Trigger
          value="tab1"
          className="px-4 py-2 text-sm font-medium border-b-2 border-transparent hover:text-blue-600 data-[state=active]:border-blue-600 data-[state=active]:text-blue-600 outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
        >
          Account
        </Tabs.Trigger>

        <Tabs.Trigger
          value="tab2"
          className="px-4 py-2 text-sm font-medium border-b-2 border-transparent hover:text-blue-600 data-[state=active]:border-blue-600 data-[state=active]:text-blue-600 outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
        >
          Password
        </Tabs.Trigger>

        <Tabs.Trigger
          value="tab3"
          className="px-4 py-2 text-sm font-medium border-b-2 border-transparent hover:text-blue-600 data-[state=active]:border-blue-600 data-[state=active]:text-blue-600 outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
        >
          Settings
        </Tabs.Trigger>
      </Tabs.List>

      <Tabs.Content value="tab1" className="p-4">
        <h3 className="text-lg font-semibold mb-2">Account Settings</h3>
        <p className="text-gray-600">Manage your account details here.</p>
      </Tabs.Content>

      <Tabs.Content value="tab2" className="p-4">
        <h3 className="text-lg font-semibold mb-2">Password Settings</h3>
        <p className="text-gray-600">Change your password here.</p>
      </Tabs.Content>

      <Tabs.Content value="tab3" className="p-4">
        <h3 className="text-lg font-semibold mb-2">General Settings</h3>
        <p className="text-gray-600">Configure application settings.</p>
      </Tabs.Content>
    </Tabs.Root>
  );
}
```

### Vertical Tabs

```tsx
<Tabs.Root defaultValue="tab1" orientation="vertical" className="flex gap-4">
  <Tabs.List className="flex flex-col gap-1 border-r pr-4">
    <Tabs.Trigger
      value="tab1"
      className="px-4 py-2 text-left text-sm rounded hover:bg-gray-100 data-[state=active]:bg-blue-100 data-[state=active]:text-blue-700"
    >
      Profile
    </Tabs.Trigger>
    <Tabs.Trigger
      value="tab2"
      className="px-4 py-2 text-left text-sm rounded hover:bg-gray-100 data-[state=active]:bg-blue-100 data-[state=active]:text-blue-700"
    >
      Billing
    </Tabs.Trigger>
  </Tabs.List>

  <div className="flex-1">
    <Tabs.Content value="tab1">{/* ... */}</Tabs.Content>
    <Tabs.Content value="tab2">{/* ... */}</Tabs.Content>
  </div>
</Tabs.Root>
```

## Styling with Tailwind

### Data Attribute Selectors

```tsx
// State-based styling
className="data-[state=open]:bg-blue-50 data-[state=closed]:bg-gray-50"

// Side-based styling (for positioned elements)
className="data-[side=top]:animate-slide-down data-[side=bottom]:animate-slide-up"

// Disabled state
className="data-[disabled]:opacity-50 data-[disabled]:pointer-events-none"

// Highlighted state (for keyboard navigation)
className="data-[highlighted]:bg-blue-100"

// Checked state
className="data-[state=checked]:bg-blue-600"
```

### Common Tailwind Patterns

```tsx
// Focus ring (keyboard navigation)
className="outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"

// Backdrop overlay
className="fixed inset-0 bg-black/50 backdrop-blur-sm"

// Centered modal
className="fixed left-[50%] top-[50%] translate-x-[-50%] translate-y-[-50%]"

// Dropdown content z-index
className="z-50 bg-white rounded-md shadow-lg"

// Smooth transitions
className="transition-colors duration-150"
```

## Accessibility

### Keyboard Navigation

All Radix components handle keyboard navigation automatically:

- **Dialog**: Esc to close, Tab trap inside modal
- **Select**: Arrow keys to navigate, Enter to select, type-ahead search
- **DropdownMenu**: Arrow keys to navigate, Enter to select
- **Tabs**: Arrow keys to switch tabs, Home/End for first/last
- **Tooltip**: Focus trigger shows tooltip

### ARIA Attributes

Radix components automatically add proper ARIA attributes:

```tsx
// Dialog adds:
// role="dialog"
// aria-labelledby (references Dialog.Title)
// aria-describedby (references Dialog.Description)

// Select adds:
// role="combobox"
// aria-expanded
// aria-controls

// Always provide Dialog.Title and Dialog.Description
<Dialog.Content>
  <Dialog.Title>Required for a11y</Dialog.Title>
  <Dialog.Description>Screen readers announce this</Dialog.Description>
</Dialog.Content>
```

### Focus Management

```tsx
// Auto-focus on mount
<Dialog.Content onOpenAutoFocus={(e) => {
  e.preventDefault(); // Prevent default focus
  customElementRef.current?.focus(); // Custom focus target
}}>

// Focus on close
<Dialog.Content onCloseAutoFocus={(e) => {
  e.preventDefault();
  triggerRef.current?.focus();
}}>
```

## Controlled vs Uncontrolled

### Uncontrolled (Default)

```tsx
// Component manages its own state
<Dialog.Root defaultOpen={false}>
  <Dialog.Trigger>Open</Dialog.Trigger>
  {/* ... */}
</Dialog.Root>

<Select.Root defaultValue="apple">
  <Select.Trigger>{/* ... */}</Select.Trigger>
</Select.Root>
```

### Controlled (Recommended for Complex UIs)

```tsx
// Parent manages state
const [open, setOpen] = useState(false);
const [value, setValue] = useState('');

<Dialog.Root open={open} onOpenChange={setOpen}>
  {/* ... */}
</Dialog.Root>

<Select.Root value={value} onValueChange={setValue}>
  {/* ... */}
</Select.Root>
```

## Portal Usage

### Why Use Portals

Portals render components outside the DOM hierarchy to avoid:
- z-index conflicts
- overflow: hidden clipping
- CSS transform issues

```tsx
// Without portal (may be clipped)
<Dialog.Content>{/* ... */}</Dialog.Content>

// With portal (renders at document.body)
<Dialog.Portal>
  <Dialog.Content>{/* ... */}</Dialog.Content>
</Dialog.Portal>

// Custom portal container
<Dialog.Portal container={customContainerRef.current}>
  <Dialog.Content>{/* ... */}</Dialog.Content>
</Dialog.Portal>
```

### Portal Best Practices

```tsx
// Always portal Overlay and Content together
<Dialog.Portal>
  <Dialog.Overlay />
  <Dialog.Content />
</Dialog.Portal>

// Use forceMount with AnimatePresence
<AnimatePresence>
  {open && (
    <Dialog.Portal forceMount>
      {/* Framer Motion components */}
    </Dialog.Portal>
  )}
</AnimatePresence>
```

## Best Practices

- **Use asChild prop** to compose with your own elements without wrapper divs
- **Always Portal overlays and dropdowns** to avoid z-index issues
- **Provide Title and Description** for Dialogs (accessibility requirement)
- **Use data-[state=] selectors** for styling open/closed states
- **Prefer controlled components** for complex state management
- **Add focus rings** with Tailwind outline-none + focus:ring-2
- **Use TooltipProvider once** at app root, not per tooltip
- **Combine with Framer Motion** using asChild and forceMount
- **Test keyboard navigation** for all interactive components
- **Set proper sideOffset** (usually 5-10px) for floating elements
- **Use consistent styling patterns** across all Radix components

## Anti-Patterns

- ❌ Forgetting Dialog.Portal (causes z-index issues)
- ❌ Missing Dialog.Title or Dialog.Description (fails a11y)
- ❌ Not using asChild with custom triggers (creates wrapper divs)
- ❌ Hardcoding colors instead of using data-[state=] selectors
- ❌ Multiple TooltipProviders (unnecessary overhead)
- ❌ Blocking onSelect propagation without e.preventDefault()
- ❌ Forgetting focus:ring styles (poor keyboard UX)
- ❌ Not testing with keyboard navigation
- ❌ Using controlled without onOpenChange/onValueChange
- ❌ Mixing controlled and uncontrolled patterns

## Feedback Loops

**Accessibility testing:**
```bash
# Test with keyboard only (no mouse)
# Tab through all interactive elements
# Esc should close Dialogs, Dropdowns, Selects
# Arrow keys should navigate menus and selects
```

**Screen reader testing:**
```bash
# macOS: VoiceOver (Cmd+F5)
# Verify Dialog.Title and Dialog.Description are announced
# Verify Select options are announced correctly
# Check for proper role attributes
```

**Visual regression:**
```tsx
// Test all states:
// - Closed vs Open
// - Hover vs Focus
// - Selected vs Unselected
// - Disabled states
// - Different viewport sizes
```

**Integration with Framer Motion:**
```tsx
// Use forceMount to control mounting
// Wrap in AnimatePresence for exit animations
// Test that focus management still works with animations
```
