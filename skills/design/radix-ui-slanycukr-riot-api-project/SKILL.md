---
name: radix-ui
description: Build accessible, unstyled React UI components with Radix Primitives
when_to_use: When you need accessible, composable UI components that give you full control over styling while ensuring WCAG compliance
---

# Radix UI Primitives Skill

Radix UI Primitives provides low-level, unstyled React components with built-in accessibility, keyboard navigation, and focus management. Perfect for building design systems and custom UI components.

## Quick Start

### Basic Dialog Example

```jsx
import * as Dialog from "@radix-ui/react-dialog";
import { Cross2Icon } from "@radix-ui/react-icons";

function BasicDialog() {
  return (
    <Dialog.Root>
      <Dialog.Trigger asChild>
        <button className="btn-primary">Edit profile</button>
      </Dialog.Trigger>
      <Dialog.Portal>
        <Dialog.Overlay className="dialog-overlay" />
        <Dialog.Content className="dialog-content">
          <Dialog.Title className="dialog-title">Edit profile</Dialog.Title>
          <Dialog.Description className="dialog-description">
            Make changes to your profile here.
          </Dialog.Description>

          <div className="dialog-fields">
            <input placeholder="Name" defaultValue="John Doe" />
            <input placeholder="Username" defaultValue="@johndoe" />
          </div>

          <div className="dialog-actions">
            <Dialog.Close asChild>
              <button className="btn-primary">Save changes</button>
            </Dialog.Close>
          </div>

          <Dialog.Close asChild>
            <button className="dialog-close" aria-label="Close">
              <Cross2Icon />
            </button>
          </Dialog.Close>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
```

### Dropdown Menu Example

```jsx
import * as DropdownMenu from "@radix-ui/react-dropdown-menu";
import { HamburgerMenuIcon, CheckIcon } from "@radix-ui/react-icons";

function UserMenu() {
  const [showBookmarks, setShowBookmarks] = React.useState(true);

  return (
    <DropdownMenu.Root>
      <DropdownMenu.Trigger asChild>
        <button className="icon-btn" aria-label="Menu">
          <HamburgerMenuIcon />
        </button>
      </DropdownMenu.Trigger>

      <DropdownMenu.Portal>
        <DropdownMenu.Content className="dropdown-content" sideOffset={5}>
          <DropdownMenu.Item className="dropdown-item">
            New Tab <div className="shortcut">⌘+T</div>
          </DropdownMenu.Item>
          <DropdownMenu.Item className="dropdown-item">
            New Window <div className="shortcut">⌘+N</div>
          </DropdownMenu.Item>

          <DropdownMenu.Separator className="dropdown-separator" />

          <DropdownMenu.CheckboxItem
            className="dropdown-item"
            checked={showBookmarks}
            onCheckedChange={setShowBookmarks}
          >
            <DropdownMenu.ItemIndicator className="item-indicator">
              <CheckIcon />
            </DropdownMenu.ItemIndicator>
            Show Bookmarks
          </DropdownMenu.CheckboxItem>

          <DropdownMenu.Arrow className="dropdown-arrow" />
        </DropdownMenu.Content>
      </DropdownMenu.Portal>
    </DropdownMenu.Root>
  );
}
```

## Common Patterns

### Primitive Components

Radix provides 30+ primitive components for common UI patterns:

```jsx
// Accordion with animation
import * as Accordion from "@radix-ui/react-accordion";

function FAQAccordion() {
  return (
    <Accordion.Root type="single" collapsible className="accordion">
      <Accordion.Item value="item-1" className="accordion-item">
        <Accordion.Header>
          <Accordion.Trigger className="accordion-trigger">
            Is it accessible?
            <ChevronDownIcon className="accordion-chevron" />
          </Accordion.Trigger>
        </Accordion.Header>
        <Accordion.Content className="accordion-content">
          Yes. It adheres to WAI-ARIA design patterns.
        </Accordion.Content>
      </Accordion.Item>
    </Accordion.Root>
  );
}

// Tooltip with delay
import * as Tooltip from "@radix-ui/react-tooltip";

function TooltipExample() {
  return (
    <Tooltip.Provider delayDuration={800}>
      <Tooltip.Root>
        <Tooltip.Trigger asChild>
          <button className="icon-btn">
            <InfoIcon />
          </button>
        </Tooltip.Trigger>
        <Tooltip.Portal>
          <Tooltip.Content className="tooltip" sideOffset={5}>
            Additional information
            <Tooltip.Arrow className="tooltip-arrow" />
          </Tooltip.Content>
        </Tooltip.Portal>
      </Tooltip.Root>
    </Tooltip.Provider>
  );
}
```

### Accessibility Features

Radix automatically handles accessibility:

```jsx
// All components include proper ARIA attributes
// Focus management is handled automatically
// Keyboard navigation works out of the box
// Screen reader support is built-in

// Example: Select with proper labeling
import * as Select from "@radix-ui/react-select";

function AccessibleSelect() {
  return (
    <Select.Root>
      <Select.Trigger aria-label="Select a fruit">
        <Select.Value placeholder="Choose a fruit…" />
        <Select.Icon>
          <ChevronDownIcon />
        </Select.Icon>
      </Select.Trigger>

      <Select.Portal>
        <Select.Content>
          <Select.Viewport>
            <Select.Group>
              <Select.Label>Fruits</Select.Label>
              <Select.Item value="apple">
                <Select.ItemText>Apple</Select.ItemText>
                <Select.ItemIndicator>
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

### Composition with asChild

Compose Radix primitives with your own components:

```jsx
// Use your existing button styles
import { Dialog, Tooltip } from "@radix-ui/react-dialog";
import { Button } from "./your-design-system";

function ComposedDialog() {
  return (
    <Dialog.Root>
      <Dialog.Trigger asChild>
        <Button variant="primary">Open Dialog</Button>
      </Dialog.Trigger>

      <Dialog.Portal>
        <Dialog.Overlay />
        <Dialog.Content>
          <Dialog.Title>Dialog Title</Dialog.Title>
          <Dialog.Close asChild>
            <Button variant="secondary">Close</Button>
          </Dialog.Close>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}

// Multiple primitives on one element
function TooltipDialogButton() {
  return (
    <Dialog.Root>
      <Tooltip.Root>
        <Tooltip.Trigger asChild>
          <Dialog.Trigger asChild>
            <Button variant="primary">Open Dialog</Button>
          </Dialog.Trigger>
        </Tooltip.Trigger>
        <Tooltip.Portal>
          <Tooltip.Content>Opens a modal dialog</Tooltip.Content>
        </Tooltip.Portal>
      </Tooltip.Root>

      {/* Dialog content */}
    </Dialog.Root>
  );
}
```

### Custom Component Abstractions

Create your own simplified APIs:

```jsx
// Custom Dialog wrapper
import * as DialogPrimitive from "@radix-ui/react-dialog";

export const CustomDialog = ({ children, trigger, title }) => {
  return (
    <DialogPrimitive.Root>
      <DialogPrimitive.Trigger asChild>{trigger}</DialogPrimitive.Trigger>
      <DialogPrimitive.Portal>
        <DialogPrimitive.Overlay className="overlay" />
        <DialogPrimitive.Content className="content">
          <DialogPrimitive.Title>{title}</DialogPrimitive.Title>
          {children}
          <DialogPrimitive.Close asChild>
            <button className="close-btn">×</button>
          </DialogPrimitive.Close>
        </DialogPrimitive.Content>
      </DialogPrimitive.Portal>
    </DialogPrimitive.Root>
  );
};

// Usage
<CustomDialog title="Settings" trigger={<Button>Open Settings</Button>}>
  <div>Settings content here</div>
</CustomDialog>;
```

### Styling with Data Attributes

Style components based on their state:

```css
/* Accordion animations */
.accordion-content[data-state="open"] {
  animation: slideDown 300ms ease-out;
}

.accordion-content[data-state="closed"] {
  animation: slideUp 300ms ease-out;
}

/* Dropdown positioning */
.dropdown-content {
  transform-origin: var(--radix-dropdown-menu-content-transform-origin);
}

.dropdown-content[data-side="top"] {
  animation: slideUp 0.3s ease-out;
}

.dropdown-content[data-side="bottom"] {
  animation: slideDown 0.3s ease-out;
}

/* Focus states */
.dropdown-item[data-highlighted] {
  background: #f0f0f0;
}

.dropdown-item[data-state="checked"] {
  background: #e0e0e0;
}
```

### Advanced Patterns

```jsx
// Controlled components for async operations
function AsyncDialog() {
  const [open, setOpen] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    await submitForm();
    setLoading(false);
    setOpen(false);
  };

  return (
    <Dialog.Root open={open} onOpenChange={setOpen}>
      <Dialog.Trigger asChild>
        <Button>Open Form</Button>
      </Dialog.Trigger>
      <Dialog.Portal>
        <Dialog.Content>
          <form onSubmit={handleSubmit}>
            <input name="email" type="email" required />
            <Button type="submit" disabled={loading}>
              {loading ? "Submitting…" : "Submit"}
            </Button>
          </form>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}

// Popover with collision detection
function SmartPopover() {
  return (
    <Popover.Root>
      <Popover.Trigger asChild>
        <Button>Click me</Button>
      </Popover.Trigger>
      <Popover.Portal>
        <Popover.Content
          className="popover"
          sideOffset={10}
          collisionPadding={20}
        >
          Content that avoids screen edges
          <Popover.Arrow className="popover-arrow" />
        </Popover.Content>
      </Popover.Portal>
    </Popover.Root>
  );
}
```
