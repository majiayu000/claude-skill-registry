---
name: ark-ui
description: Builds accessible UI components with Ark UI headless primitives for React, Vue, Solid, and Svelte. Use when creating custom-styled components with robust state management and accessibility built-in.
---

# Ark UI

Headless component library with 45+ accessible components powered by state machines.

## Quick Start

```bash
npm install @ark-ui/react
```

```tsx
import { Accordion } from '@ark-ui/react'

function App() {
  return (
    <Accordion.Root defaultValue={['react']}>
      <Accordion.Item value="react">
        <Accordion.ItemTrigger>
          What is React?
          <Accordion.ItemIndicator>
            <ChevronDownIcon />
          </Accordion.ItemIndicator>
        </Accordion.ItemTrigger>
        <Accordion.ItemContent>
          React is a JavaScript library for building user interfaces.
        </Accordion.ItemContent>
      </Accordion.Item>
    </Accordion.Root>
  )
}
```

## Core Concepts

### Anatomy Pattern

Ark UI uses compound components with dot notation:

```tsx
<Component.Root>
  <Component.Trigger />
  <Component.Content>
    <Component.Item />
  </Component.Content>
</Component.Root>
```

### Data Attributes for Styling

Components expose state via data attributes:

```css
/* Base styles */
[data-scope="accordion"][data-part="trigger"] {
  display: flex;
  justify-content: space-between;
}

/* State-based styles */
[data-state="open"] {
  background-color: #f0f0f0;
}

[data-state="closed"] {
  background-color: white;
}

[data-disabled] {
  opacity: 0.5;
}

[data-focus] {
  outline: 2px solid blue;
}
```

### With Tailwind CSS

```tsx
<Accordion.ItemTrigger className="
  flex justify-between w-full px-4 py-2
  data-[state=open]:bg-gray-100
  data-[focus]:ring-2 data-[focus]:ring-blue-500
  data-[disabled]:opacity-50
">
  Trigger Text
</Accordion.ItemTrigger>
```

## Components

### Accordion

```tsx
import { Accordion } from '@ark-ui/react'
import { ChevronDownIcon } from 'lucide-react'

function AccordionDemo() {
  return (
    <Accordion.Root defaultValue={['item-1']} multiple>
      {items.map((item) => (
        <Accordion.Item key={item.value} value={item.value}>
          <Accordion.ItemTrigger>
            {item.title}
            <Accordion.ItemIndicator>
              <ChevronDownIcon />
            </Accordion.ItemIndicator>
          </Accordion.ItemTrigger>
          <Accordion.ItemContent>
            {item.content}
          </Accordion.ItemContent>
        </Accordion.Item>
      ))}
    </Accordion.Root>
  )
}
```

### Dialog

```tsx
import { Dialog, Portal } from '@ark-ui/react'

function DialogDemo() {
  return (
    <Dialog.Root>
      <Dialog.Trigger>Open Dialog</Dialog.Trigger>
      <Portal>
        <Dialog.Backdrop className="fixed inset-0 bg-black/50" />
        <Dialog.Positioner className="fixed inset-0 flex items-center justify-center">
          <Dialog.Content className="bg-white rounded-lg p-6 max-w-md w-full">
            <Dialog.Title className="text-lg font-semibold">
              Dialog Title
            </Dialog.Title>
            <Dialog.Description className="mt-2 text-gray-600">
              Dialog description text here.
            </Dialog.Description>
            <div className="mt-4 flex justify-end gap-2">
              <Dialog.CloseTrigger className="px-4 py-2 text-gray-600">
                Cancel
              </Dialog.CloseTrigger>
              <button className="px-4 py-2 bg-blue-500 text-white rounded">
                Confirm
              </button>
            </div>
          </Dialog.Content>
        </Dialog.Positioner>
      </Portal>
    </Dialog.Root>
  )
}
```

### Menu

```tsx
import { Menu, Portal } from '@ark-ui/react'

function MenuDemo() {
  return (
    <Menu.Root>
      <Menu.Trigger className="px-4 py-2 bg-gray-100 rounded">
        Open Menu
      </Menu.Trigger>
      <Portal>
        <Menu.Positioner>
          <Menu.Content className="bg-white shadow-lg rounded-lg p-1 min-w-[160px]">
            <Menu.Item value="edit" className="px-3 py-2 hover:bg-gray-100 rounded cursor-pointer">
              Edit
            </Menu.Item>
            <Menu.Item value="duplicate" className="px-3 py-2 hover:bg-gray-100 rounded cursor-pointer">
              Duplicate
            </Menu.Item>
            <Menu.Separator className="h-px bg-gray-200 my-1" />
            <Menu.Item value="delete" className="px-3 py-2 text-red-600 hover:bg-red-50 rounded cursor-pointer">
              Delete
            </Menu.Item>
          </Menu.Content>
        </Menu.Positioner>
      </Portal>
    </Menu.Root>
  )
}
```

### Select

```tsx
import { Select, Portal } from '@ark-ui/react'
import { CheckIcon, ChevronDownIcon } from 'lucide-react'

const items = [
  { label: 'React', value: 'react' },
  { label: 'Vue', value: 'vue' },
  { label: 'Svelte', value: 'svelte' },
]

function SelectDemo() {
  return (
    <Select.Root items={items}>
      <Select.Label>Framework</Select.Label>
      <Select.Control>
        <Select.Trigger className="flex items-center justify-between w-full px-4 py-2 border rounded">
          <Select.ValueText placeholder="Select a framework" />
          <Select.Indicator>
            <ChevronDownIcon />
          </Select.Indicator>
        </Select.Trigger>
      </Select.Control>
      <Portal>
        <Select.Positioner>
          <Select.Content className="bg-white shadow-lg rounded-lg p-1">
            {items.map((item) => (
              <Select.Item
                key={item.value}
                item={item}
                className="flex items-center justify-between px-3 py-2 hover:bg-gray-100 rounded cursor-pointer"
              >
                <Select.ItemText>{item.label}</Select.ItemText>
                <Select.ItemIndicator>
                  <CheckIcon />
                </Select.ItemIndicator>
              </Select.Item>
            ))}
          </Select.Content>
        </Select.Positioner>
      </Portal>
    </Select.Root>
  )
}
```

### Combobox

```tsx
import { Combobox, Portal } from '@ark-ui/react'
import { useState } from 'react'

const allItems = [
  { label: 'React', value: 'react' },
  { label: 'Vue', value: 'vue' },
  { label: 'Svelte', value: 'svelte' },
  { label: 'Solid', value: 'solid' },
]

function ComboboxDemo() {
  const [items, setItems] = useState(allItems)

  const handleInputChange = ({ inputValue }) => {
    const filtered = allItems.filter((item) =>
      item.label.toLowerCase().includes(inputValue.toLowerCase())
    )
    setItems(filtered)
  }

  return (
    <Combobox.Root items={items} onInputValueChange={handleInputChange}>
      <Combobox.Label>Framework</Combobox.Label>
      <Combobox.Control>
        <Combobox.Input className="w-full px-4 py-2 border rounded" placeholder="Search..." />
        <Combobox.Trigger>
          <ChevronDownIcon />
        </Combobox.Trigger>
      </Combobox.Control>
      <Portal>
        <Combobox.Positioner>
          <Combobox.Content className="bg-white shadow-lg rounded-lg p-1">
            {items.map((item) => (
              <Combobox.Item
                key={item.value}
                item={item}
                className="px-3 py-2 hover:bg-gray-100 rounded cursor-pointer"
              >
                <Combobox.ItemText>{item.label}</Combobox.ItemText>
                <Combobox.ItemIndicator>
                  <CheckIcon />
                </Combobox.ItemIndicator>
              </Combobox.Item>
            ))}
          </Combobox.Content>
        </Combobox.Positioner>
      </Portal>
    </Combobox.Root>
  )
}
```

### Tabs

```tsx
import { Tabs } from '@ark-ui/react'

function TabsDemo() {
  return (
    <Tabs.Root defaultValue="react">
      <Tabs.List className="flex gap-1 border-b">
        <Tabs.Trigger
          value="react"
          className="px-4 py-2 data-[selected]:border-b-2 data-[selected]:border-blue-500"
        >
          React
        </Tabs.Trigger>
        <Tabs.Trigger
          value="vue"
          className="px-4 py-2 data-[selected]:border-b-2 data-[selected]:border-blue-500"
        >
          Vue
        </Tabs.Trigger>
        <Tabs.Trigger
          value="svelte"
          className="px-4 py-2 data-[selected]:border-b-2 data-[selected]:border-blue-500"
        >
          Svelte
        </Tabs.Trigger>
        <Tabs.Indicator className="bg-blue-500 h-0.5" />
      </Tabs.List>
      <Tabs.Content value="react" className="p-4">React content</Tabs.Content>
      <Tabs.Content value="vue" className="p-4">Vue content</Tabs.Content>
      <Tabs.Content value="svelte" className="p-4">Svelte content</Tabs.Content>
    </Tabs.Root>
  )
}
```

### Switch

```tsx
import { Switch } from '@ark-ui/react'

function SwitchDemo() {
  return (
    <Switch.Root>
      <Switch.Control className="
        relative w-11 h-6 bg-gray-200 rounded-full
        data-[state=checked]:bg-blue-500
        transition-colors
      ">
        <Switch.Thumb className="
          block w-5 h-5 bg-white rounded-full shadow
          translate-x-0.5 data-[state=checked]:translate-x-5
          transition-transform
        " />
      </Switch.Control>
      <Switch.Label className="ml-2">Enable notifications</Switch.Label>
      <Switch.HiddenInput />
    </Switch.Root>
  )
}
```

### Checkbox

```tsx
import { Checkbox } from '@ark-ui/react'
import { CheckIcon, MinusIcon } from 'lucide-react'

function CheckboxDemo() {
  return (
    <Checkbox.Root>
      <Checkbox.Control className="
        w-5 h-5 border-2 rounded
        data-[state=checked]:bg-blue-500 data-[state=checked]:border-blue-500
        data-[state=indeterminate]:bg-blue-500 data-[state=indeterminate]:border-blue-500
      ">
        <Checkbox.Indicator>
          <CheckIcon className="w-4 h-4 text-white" />
        </Checkbox.Indicator>
        <Checkbox.Indicator indeterminate>
          <MinusIcon className="w-4 h-4 text-white" />
        </Checkbox.Indicator>
      </Checkbox.Control>
      <Checkbox.Label className="ml-2">Accept terms</Checkbox.Label>
      <Checkbox.HiddenInput />
    </Checkbox.Root>
  )
}
```

### Slider

```tsx
import { Slider } from '@ark-ui/react'

function SliderDemo() {
  return (
    <Slider.Root defaultValue={[50]} min={0} max={100}>
      <Slider.Label>Volume</Slider.Label>
      <Slider.ValueText />
      <Slider.Control className="relative flex items-center w-full h-5">
        <Slider.Track className="w-full h-2 bg-gray-200 rounded-full">
          <Slider.Range className="h-full bg-blue-500 rounded-full" />
        </Slider.Track>
        <Slider.Thumb
          index={0}
          className="w-5 h-5 bg-white border-2 border-blue-500 rounded-full shadow"
        />
      </Slider.Control>
    </Slider.Root>
  )
}

// Range slider
<Slider.Root defaultValue={[25, 75]}>
  <Slider.Control>
    <Slider.Track>
      <Slider.Range />
    </Slider.Track>
    <Slider.Thumb index={0} />
    <Slider.Thumb index={1} />
  </Slider.Control>
</Slider.Root>
```

### Tooltip

```tsx
import { Tooltip, Portal } from '@ark-ui/react'

function TooltipDemo() {
  return (
    <Tooltip.Root>
      <Tooltip.Trigger className="px-4 py-2 bg-gray-100 rounded">
        Hover me
      </Tooltip.Trigger>
      <Portal>
        <Tooltip.Positioner>
          <Tooltip.Content className="bg-gray-900 text-white px-3 py-2 rounded text-sm">
            <Tooltip.Arrow>
              <Tooltip.ArrowTip className="border-t-gray-900" />
            </Tooltip.Arrow>
            Tooltip content
          </Tooltip.Content>
        </Tooltip.Positioner>
      </Portal>
    </Tooltip.Root>
  )
}
```

### Popover

```tsx
import { Popover, Portal } from '@ark-ui/react'

function PopoverDemo() {
  return (
    <Popover.Root>
      <Popover.Trigger className="px-4 py-2 bg-blue-500 text-white rounded">
        Open Popover
      </Popover.Trigger>
      <Portal>
        <Popover.Positioner>
          <Popover.Content className="bg-white shadow-lg rounded-lg p-4 max-w-sm">
            <Popover.Arrow>
              <Popover.ArrowTip />
            </Popover.Arrow>
            <Popover.Title className="font-semibold">Popover Title</Popover.Title>
            <Popover.Description className="mt-2 text-gray-600">
              This is the popover content.
            </Popover.Description>
            <Popover.CloseTrigger className="absolute top-2 right-2">
              <XIcon />
            </Popover.CloseTrigger>
          </Popover.Content>
        </Popover.Positioner>
      </Portal>
    </Popover.Root>
  )
}
```

### DatePicker

```tsx
import { DatePicker, Portal } from '@ark-ui/react'

function DatePickerDemo() {
  return (
    <DatePicker.Root>
      <DatePicker.Label>Date</DatePicker.Label>
      <DatePicker.Control>
        <DatePicker.Input className="px-4 py-2 border rounded" />
        <DatePicker.Trigger>
          <CalendarIcon />
        </DatePicker.Trigger>
      </DatePicker.Control>
      <Portal>
        <DatePicker.Positioner>
          <DatePicker.Content className="bg-white shadow-lg rounded-lg p-4">
            <DatePicker.View view="day">
              <DatePicker.Context>
                {(api) => (
                  <>
                    <DatePicker.ViewControl>
                      <DatePicker.PrevTrigger>
                        <ChevronLeftIcon />
                      </DatePicker.PrevTrigger>
                      <DatePicker.ViewTrigger>
                        <DatePicker.RangeText />
                      </DatePicker.ViewTrigger>
                      <DatePicker.NextTrigger>
                        <ChevronRightIcon />
                      </DatePicker.NextTrigger>
                    </DatePicker.ViewControl>
                    <DatePicker.Table>
                      <DatePicker.TableHead>
                        <DatePicker.TableRow>
                          {api.weekDays.map((day, i) => (
                            <DatePicker.TableHeader key={i}>
                              {day.narrow}
                            </DatePicker.TableHeader>
                          ))}
                        </DatePicker.TableRow>
                      </DatePicker.TableHead>
                      <DatePicker.TableBody>
                        {api.weeks.map((week, i) => (
                          <DatePicker.TableRow key={i}>
                            {week.map((day, j) => (
                              <DatePicker.TableCell key={j} value={day}>
                                <DatePicker.TableCellTrigger>
                                  {day.day}
                                </DatePicker.TableCellTrigger>
                              </DatePicker.TableCell>
                            ))}
                          </DatePicker.TableRow>
                        ))}
                      </DatePicker.TableBody>
                    </DatePicker.Table>
                  </>
                )}
              </DatePicker.Context>
            </DatePicker.View>
          </DatePicker.Content>
        </DatePicker.Positioner>
      </Portal>
    </DatePicker.Root>
  )
}
```

### Toast

```tsx
import { Toaster, createToaster } from '@ark-ui/react'

const toaster = createToaster({
  placement: 'bottom-end',
  overlap: true,
  gap: 16,
})

function ToastDemo() {
  return (
    <>
      <button
        onClick={() => {
          toaster.create({
            title: 'Success',
            description: 'Your changes have been saved.',
            type: 'success',
          })
        }}
      >
        Show Toast
      </button>

      <Toaster toaster={toaster}>
        {(toast) => (
          <Toast.Root key={toast.id}>
            <Toast.Title>{toast.title}</Toast.Title>
            <Toast.Description>{toast.description}</Toast.Description>
            <Toast.CloseTrigger>Close</Toast.CloseTrigger>
          </Toast.Root>
        )}
      </Toaster>
    </>
  )
}
```

## Controlled vs Uncontrolled

```tsx
// Uncontrolled (internal state)
<Accordion.Root defaultValue={['item-1']}>
  {/* ... */}
</Accordion.Root>

// Controlled (external state)
const [value, setValue] = useState(['item-1'])

<Accordion.Root value={value} onValueChange={(details) => setValue(details.value)}>
  {/* ... */}
</Accordion.Root>
```

## API Patterns

### onValueChange

```tsx
<Select.Root
  onValueChange={(details) => {
    console.log(details.value)       // Selected value(s)
    console.log(details.items)       // Selected item(s)
  }}
>
```

### onOpenChange

```tsx
<Dialog.Root
  onOpenChange={(details) => {
    console.log(details.open)        // boolean
  }}
>
```

## Best Practices

1. **Use Portal** - Wrap overlays in Portal for proper stacking
2. **Style with data attributes** - Use `data-[state=open]` patterns
3. **Provide accessible labels** - Use Label components
4. **Handle keyboard** - All components have built-in keyboard support
5. **Use HiddenInput** - For form integration with checkboxes/switches

## Reference Files

- [references/components.md](references/components.md) - Complete component list
- [references/patterns.md](references/patterns.md) - Common patterns
