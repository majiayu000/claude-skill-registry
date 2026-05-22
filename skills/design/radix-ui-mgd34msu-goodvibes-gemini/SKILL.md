---
name: radix-ui
description: Builds accessible components with Radix UI primitives including dialogs, dropdowns, tooltips, and form controls. Use when building accessible interfaces, creating headless components, or implementing complex UI patterns.
---

# Radix UI

Unstyled, accessible component primitives for building high-quality design systems.

## Quick Start

**Install individual components:**
```bash
npm install @radix-ui/react-dialog
npm install @radix-ui/react-dropdown-menu
npm install @radix-ui/react-tooltip
npm install @radix-ui/react-tabs
```

## Dialog

```tsx
import * as Dialog from '@radix-ui/react-dialog';

function Modal() {
  return (
    <Dialog.Root>
      <Dialog.Trigger asChild>
        <button>Open Modal</button>
      </Dialog.Trigger>

      <Dialog.Portal>
        <Dialog.Overlay className="fixed inset-0 bg-black/50" />
        <Dialog.Content className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white p-6 rounded-lg">
          <Dialog.Title className="text-lg font-bold">
            Modal Title
          </Dialog.Title>
          <Dialog.Description className="text-gray-500 mt-2">
            Modal description goes here.
          </Dialog.Description>

          <div className="mt-4">
            <p>Modal content</p>
          </div>

          <Dialog.Close asChild>
            <button className="absolute top-4 right-4">
              Close
            </button>
          </Dialog.Close>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
```

### Controlled Dialog

```tsx
function ControlledDialog() {
  const [open, setOpen] = useState(false);

  return (
    <Dialog.Root open={open} onOpenChange={setOpen}>
      <Dialog.Trigger asChild>
        <button>Open</button>
      </Dialog.Trigger>

      <Dialog.Portal>
        <Dialog.Overlay />
        <Dialog.Content>
          <Dialog.Title>Confirm</Dialog.Title>
          <div className="flex gap-2 mt-4">
            <button onClick={() => setOpen(false)}>Cancel</button>
            <button
              onClick={() => {
                handleConfirm();
                setOpen(false);
              }}
            >
              Confirm
            </button>
          </div>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
```

## Dropdown Menu

```tsx
import * as DropdownMenu from '@radix-ui/react-dropdown-menu';

function UserMenu() {
  return (
    <DropdownMenu.Root>
      <DropdownMenu.Trigger asChild>
        <button className="p-2 rounded-full hover:bg-gray-100">
          <UserIcon />
        </button>
      </DropdownMenu.Trigger>

      <DropdownMenu.Portal>
        <DropdownMenu.Content
          className="bg-white rounded-lg shadow-lg p-2 min-w-[200px]"
          sideOffset={5}
        >
          <DropdownMenu.Label className="px-2 py-1 text-sm text-gray-500">
            My Account
          </DropdownMenu.Label>

          <DropdownMenu.Item
            className="px-2 py-2 rounded cursor-pointer hover:bg-gray-100 outline-none"
            onSelect={() => navigate('/profile')}
          >
            Profile
          </DropdownMenu.Item>

          <DropdownMenu.Item className="px-2 py-2 rounded cursor-pointer hover:bg-gray-100 outline-none">
            Settings
          </DropdownMenu.Item>

          <DropdownMenu.Separator className="h-px bg-gray-200 my-1" />

          <DropdownMenu.Item
            className="px-2 py-2 rounded cursor-pointer hover:bg-red-100 text-red-600 outline-none"
            onSelect={handleLogout}
          >
            Logout
          </DropdownMenu.Item>

          <DropdownMenu.Arrow className="fill-white" />
        </DropdownMenu.Content>
      </DropdownMenu.Portal>
    </DropdownMenu.Root>
  );
}
```

### With Submenu

```tsx
<DropdownMenu.Root>
  <DropdownMenu.Trigger asChild>
    <button>Menu</button>
  </DropdownMenu.Trigger>

  <DropdownMenu.Portal>
    <DropdownMenu.Content>
      <DropdownMenu.Item>New Tab</DropdownMenu.Item>

      <DropdownMenu.Sub>
        <DropdownMenu.SubTrigger className="flex items-center justify-between">
          More Tools
          <ChevronRightIcon />
        </DropdownMenu.SubTrigger>

        <DropdownMenu.Portal>
          <DropdownMenu.SubContent>
            <DropdownMenu.Item>Developer Tools</DropdownMenu.Item>
            <DropdownMenu.Item>Task Manager</DropdownMenu.Item>
          </DropdownMenu.SubContent>
        </DropdownMenu.Portal>
      </DropdownMenu.Sub>
    </DropdownMenu.Content>
  </DropdownMenu.Portal>
</DropdownMenu.Root>
```

## Select

```tsx
import * as Select from '@radix-ui/react-select';
import { ChevronDownIcon, CheckIcon } from '@radix-ui/react-icons';

function SelectDemo() {
  return (
    <Select.Root>
      <Select.Trigger className="flex items-center justify-between w-[200px] px-3 py-2 border rounded">
        <Select.Value placeholder="Select a fruit" />
        <Select.Icon>
          <ChevronDownIcon />
        </Select.Icon>
      </Select.Trigger>

      <Select.Portal>
        <Select.Content className="bg-white rounded-lg shadow-lg overflow-hidden">
          <Select.ScrollUpButton className="flex items-center justify-center h-6">
            <ChevronUpIcon />
          </Select.ScrollUpButton>

          <Select.Viewport className="p-1">
            <Select.Group>
              <Select.Label className="px-6 py-1 text-sm text-gray-500">
                Fruits
              </Select.Label>
              <SelectItem value="apple">Apple</SelectItem>
              <SelectItem value="banana">Banana</SelectItem>
              <SelectItem value="orange">Orange</SelectItem>
            </Select.Group>

            <Select.Separator className="h-px bg-gray-200 my-1" />

            <Select.Group>
              <Select.Label className="px-6 py-1 text-sm text-gray-500">
                Vegetables
              </Select.Label>
              <SelectItem value="carrot">Carrot</SelectItem>
              <SelectItem value="potato">Potato</SelectItem>
            </Select.Group>
          </Select.Viewport>

          <Select.ScrollDownButton className="flex items-center justify-center h-6">
            <ChevronDownIcon />
          </Select.ScrollDownButton>
        </Select.Content>
      </Select.Portal>
    </Select.Root>
  );
}

function SelectItem({ children, value }: { children: string; value: string }) {
  return (
    <Select.Item
      value={value}
      className="flex items-center px-6 py-2 rounded cursor-pointer hover:bg-gray-100 outline-none data-[highlighted]:bg-gray-100"
    >
      <Select.ItemIndicator className="absolute left-1">
        <CheckIcon />
      </Select.ItemIndicator>
      <Select.ItemText>{children}</Select.ItemText>
    </Select.Item>
  );
}
```

## Tabs

```tsx
import * as Tabs from '@radix-ui/react-tabs';

function TabsDemo() {
  return (
    <Tabs.Root defaultValue="account" className="w-full">
      <Tabs.List className="flex border-b">
        <Tabs.Trigger
          value="account"
          className="px-4 py-2 data-[state=active]:border-b-2 data-[state=active]:border-blue-500"
        >
          Account
        </Tabs.Trigger>
        <Tabs.Trigger
          value="password"
          className="px-4 py-2 data-[state=active]:border-b-2 data-[state=active]:border-blue-500"
        >
          Password
        </Tabs.Trigger>
      </Tabs.List>

      <Tabs.Content value="account" className="p-4">
        <h3 className="font-bold">Account Settings</h3>
        <p>Manage your account settings here.</p>
      </Tabs.Content>

      <Tabs.Content value="password" className="p-4">
        <h3 className="font-bold">Password</h3>
        <p>Change your password here.</p>
      </Tabs.Content>
    </Tabs.Root>
  );
}
```

## Tooltip

```tsx
import * as Tooltip from '@radix-ui/react-tooltip';

function TooltipDemo() {
  return (
    <Tooltip.Provider delayDuration={300}>
      <Tooltip.Root>
        <Tooltip.Trigger asChild>
          <button>Hover me</button>
        </Tooltip.Trigger>

        <Tooltip.Portal>
          <Tooltip.Content
            className="bg-gray-900 text-white px-3 py-2 rounded text-sm"
            sideOffset={5}
          >
            Tooltip content
            <Tooltip.Arrow className="fill-gray-900" />
          </Tooltip.Content>
        </Tooltip.Portal>
      </Tooltip.Root>
    </Tooltip.Provider>
  );
}
```

## Popover

```tsx
import * as Popover from '@radix-ui/react-popover';

function PopoverDemo() {
  return (
    <Popover.Root>
      <Popover.Trigger asChild>
        <button>Open Popover</button>
      </Popover.Trigger>

      <Popover.Portal>
        <Popover.Content
          className="bg-white rounded-lg shadow-lg p-4 w-[300px]"
          sideOffset={5}
        >
          <div className="space-y-2">
            <h4 className="font-medium">Dimensions</h4>
            <div>
              <label className="text-sm">Width</label>
              <input className="w-full border rounded px-2 py-1" />
            </div>
            <div>
              <label className="text-sm">Height</label>
              <input className="w-full border rounded px-2 py-1" />
            </div>
          </div>

          <Popover.Close asChild>
            <button className="absolute top-2 right-2">
              <Cross2Icon />
            </button>
          </Popover.Close>
          <Popover.Arrow className="fill-white" />
        </Popover.Content>
      </Popover.Portal>
    </Popover.Root>
  );
}
```

## Accordion

```tsx
import * as Accordion from '@radix-ui/react-accordion';
import { ChevronDownIcon } from '@radix-ui/react-icons';

function AccordionDemo() {
  return (
    <Accordion.Root type="single" collapsible className="w-full">
      <Accordion.Item value="item-1" className="border-b">
        <Accordion.Header>
          <Accordion.Trigger className="flex items-center justify-between w-full py-4 group">
            <span>Is it accessible?</span>
            <ChevronDownIcon className="transition-transform group-data-[state=open]:rotate-180" />
          </Accordion.Trigger>
        </Accordion.Header>
        <Accordion.Content className="pb-4 text-gray-600">
          Yes. It adheres to the WAI-ARIA design pattern.
        </Accordion.Content>
      </Accordion.Item>

      <Accordion.Item value="item-2" className="border-b">
        <Accordion.Header>
          <Accordion.Trigger className="flex items-center justify-between w-full py-4 group">
            <span>Is it unstyled?</span>
            <ChevronDownIcon className="transition-transform group-data-[state=open]:rotate-180" />
          </Accordion.Trigger>
        </Accordion.Header>
        <Accordion.Content className="pb-4 text-gray-600">
          Yes. It's completely unstyled by default.
        </Accordion.Content>
      </Accordion.Item>
    </Accordion.Root>
  );
}
```

## Checkbox

```tsx
import * as Checkbox from '@radix-ui/react-checkbox';
import { CheckIcon } from '@radix-ui/react-icons';

function CheckboxDemo() {
  const [checked, setChecked] = useState<boolean | 'indeterminate'>(false);

  return (
    <div className="flex items-center gap-2">
      <Checkbox.Root
        checked={checked}
        onCheckedChange={setChecked}
        className="w-5 h-5 border rounded flex items-center justify-center data-[state=checked]:bg-blue-500 data-[state=checked]:border-blue-500"
      >
        <Checkbox.Indicator>
          <CheckIcon className="text-white" />
        </Checkbox.Indicator>
      </Checkbox.Root>
      <label>Accept terms</label>
    </div>
  );
}
```

## Switch

```tsx
import * as Switch from '@radix-ui/react-switch';

function SwitchDemo() {
  return (
    <div className="flex items-center gap-2">
      <label htmlFor="airplane-mode">Airplane Mode</label>
      <Switch.Root
        id="airplane-mode"
        className="w-11 h-6 bg-gray-200 rounded-full data-[state=checked]:bg-blue-500 relative"
      >
        <Switch.Thumb className="block w-5 h-5 bg-white rounded-full shadow transition-transform translate-x-0.5 data-[state=checked]:translate-x-[22px]" />
      </Switch.Root>
    </div>
  );
}
```

## Slider

```tsx
import * as Slider from '@radix-ui/react-slider';

function SliderDemo() {
  return (
    <Slider.Root
      defaultValue={[50]}
      max={100}
      step={1}
      className="relative flex items-center w-full h-5"
    >
      <Slider.Track className="bg-gray-200 relative grow rounded-full h-1">
        <Slider.Range className="absolute bg-blue-500 rounded-full h-full" />
      </Slider.Track>
      <Slider.Thumb className="block w-5 h-5 bg-white border-2 border-blue-500 rounded-full hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500" />
    </Slider.Root>
  );
}
```

## Alert Dialog

```tsx
import * as AlertDialog from '@radix-ui/react-alert-dialog';

function DeleteConfirmation() {
  return (
    <AlertDialog.Root>
      <AlertDialog.Trigger asChild>
        <button className="text-red-600">Delete</button>
      </AlertDialog.Trigger>

      <AlertDialog.Portal>
        <AlertDialog.Overlay className="fixed inset-0 bg-black/50" />
        <AlertDialog.Content className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white p-6 rounded-lg max-w-md">
          <AlertDialog.Title className="text-lg font-bold">
            Are you sure?
          </AlertDialog.Title>
          <AlertDialog.Description className="text-gray-500 mt-2">
            This action cannot be undone. This will permanently delete the item.
          </AlertDialog.Description>

          <div className="flex justify-end gap-3 mt-4">
            <AlertDialog.Cancel asChild>
              <button className="px-4 py-2 border rounded">Cancel</button>
            </AlertDialog.Cancel>
            <AlertDialog.Action asChild>
              <button className="px-4 py-2 bg-red-600 text-white rounded">
                Delete
              </button>
            </AlertDialog.Action>
          </div>
        </AlertDialog.Content>
      </AlertDialog.Portal>
    </AlertDialog.Root>
  );
}
```

## Best Practices

1. **Use asChild** - Compose with your own elements
2. **Style with data attributes** - `data-[state=open]`
3. **Add animations** - Use CSS transitions
4. **Keep accessible** - Don't remove ARIA attributes
5. **Wrap in Portals** - For proper stacking context

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Missing Portal | Wrap content in Portal |
| Removing accessibility | Keep provided ARIA |
| Direct child styling | Use asChild pattern |
| Missing Provider | Add Tooltip.Provider |
| Wrong event handler | Use onSelect, not onClick |

## Reference Files

- [references/components.md](references/components.md) - All components
- [references/styling.md](references/styling.md) - Styling patterns
- [references/accessibility.md](references/accessibility.md) - A11y features
