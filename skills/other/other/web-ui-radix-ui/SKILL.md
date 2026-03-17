---
name: web-ui-radix-ui
description: Unstyled accessible UI primitives
---

# Radix UI Primitives

> **Quick Guide:** Radix UI provides unstyled, accessible primitives for building design systems. Use compound component patterns (Root, Trigger, Content), `asChild` for polymorphism, and `data-state` attributes for animations. Focus on behavior and accessibility - defer styling decisions to your styling solution. **Current: v1.4.x (May 2025)** - Full React 19 and RSC compatibility with new preview primitives.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use compound component anatomy - Root, Trigger, Portal, Content, Close - for overlay components)**

**(You MUST use `forwardRef` and spread all props when using `asChild` with custom components - unless using React 19+ where `ref` is a regular prop)**

**(You MUST use Portal for overlays to escape CSS stacking contexts and parent overflow constraints)**

**(You MUST provide accessible labels via Title/Description components or ARIA attributes - Dialog logs console errors for missing Title)**

</critical_requirements>

---

**Auto-detection:** Radix UI, radix-ui, @radix-ui, Dialog, Dropdown, DropdownMenu, Select, Popover, Tooltip, Accordion, Tabs, AlertDialog, asChild, Slot, Portal, data-state, OneTimePasswordField, PasswordToggleField, unstable_Form, Form.Field, Form.Message

**When to use:**

- Building accessible overlay components (dialogs, popovers, dropdowns, tooltips)
- Creating compound component APIs with multiple coordinated parts
- Implementing keyboard navigation and focus management
- Needing polymorphic components via `asChild` pattern

**When NOT to use:**

- Pre-styled components desired (use a component library built on Radix)
- Simple components without complex interactions (use plain HTML)
- Non-React projects (Radix primitives are React-specific)

**Package Installation:**

```bash
# Recommended: Unified tree-shakeable package (prevents version conflicts)
npm i radix-ui

# Alternative: Individual packages
npm i @radix-ui/react-dialog @radix-ui/react-dropdown-menu
```

**Detailed Resources:**

- For core code examples (Dialog, asChild, Slot), see [examples/core.md](examples/core.md)
- For overlay patterns (AlertDialog, controlled Dialog), see [examples/overlays.md](examples/overlays.md)
- For menu patterns (DropdownMenu, submenus), see [examples/menus.md](examples/menus.md)
- For animation patterns (data-state, CSS keyframes), see [examples/animation.md](examples/animation.md)
- For form patterns (Select), see [examples/forms.md](examples/forms.md)
- For navigation patterns (Accordion, Tabs), see [examples/navigation.md](examples/navigation.md)
- For preview components (OneTimePasswordField, PasswordToggleField), see [examples/preview.md](examples/preview.md)
- For decision frameworks and anti-patterns, see [reference.md](reference.md)

---

<philosophy>

## Philosophy

Radix UI Primitives provide behavioral and accessibility foundations without imposing visual design. Each primitive handles:

- **Accessibility**: ARIA attributes, roles, keyboard navigation, focus management
- **Behavior**: Open/close state, dismissal patterns, collision detection
- **Composition**: Compound components that work together as coordinated systems

**Radix is styling-agnostic:** Apply styles via `className` prop using your styling solution. The primitives expose `data-state` attributes for state-based styling.

**Compound Component Model:** Each primitive consists of multiple parts (Root, Trigger, Content, etc.) that share context. This enables flexible composition while maintaining coordinated behavior.

**React 19 & RSC Support (v1.4.3):** Full compatibility with React 19 and React Server Components. Enhanced keyboard handling avoids browser hotkey interference.

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Compound Component Anatomy

Radix primitives use a compound component pattern where multiple parts work together through shared context.

#### Standard Structure for Overlay Components

```typescript
import { Dialog } from "radix-ui";

// Root provides context and state management
// Trigger opens the dialog
// Portal renders content outside React tree
// Overlay covers the page
// Content contains the dialog body
// Close dismisses the dialog
// Title and Description provide accessibility

<Dialog.Root>
  <Dialog.Trigger>Open</Dialog.Trigger>
  <Dialog.Portal>
    <Dialog.Overlay className={className} />
    <Dialog.Content className={className}>
      <Dialog.Title>Dialog Title</Dialog.Title>
      <Dialog.Description>Accessible description</Dialog.Description>
      {/* Dialog content */}
      <Dialog.Close>Close</Dialog.Close>
    </Dialog.Content>
  </Dialog.Portal>
</Dialog.Root>
```

**Why this structure:** Root manages state and context, Portal escapes CSS stacking contexts, Overlay provides visual backdrop, Title/Description ensure screen reader accessibility

---

### Pattern 2: Controlled vs Uncontrolled State

Radix primitives support both controlled and uncontrolled state patterns.

#### Uncontrolled (Radix Manages State)

```typescript
// Let Radix manage internal state - simpler for basic use cases
<Dialog.Root defaultOpen={false}>
  <Dialog.Trigger>Open</Dialog.Trigger>
  <Dialog.Portal>
    <Dialog.Content>
      {/* Content */}
    </Dialog.Content>
  </Dialog.Portal>
</Dialog.Root>
```

**When to use:** Simple dialogs without external state requirements

#### Controlled (You Manage State)

```typescript
import { useState } from "react";
import { Dialog } from "radix-ui";

function ControlledDialog() {
  const [open, setOpen] = useState(false);

  const handleSave = async () => {
    await saveData();
    setOpen(false); // Programmatically close after async operation
  };

  return (
    <Dialog.Root open={open} onOpenChange={setOpen}>
      <Dialog.Trigger>Open</Dialog.Trigger>
      <Dialog.Portal>
        <Dialog.Content>
          <Dialog.Title>Edit Profile</Dialog.Title>
          <button onClick={handleSave}>Save</button>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
```

**When to use:** Programmatic control needed (close after async, open from external trigger, sync with URL state)

---

### Pattern 3: asChild for Polymorphism

The `asChild` prop enables Radix to merge behavior onto your custom components or different element types.

#### Changing Element Type

```typescript
import { Tooltip } from "radix-ui";

// Tooltip trigger defaults to button, but you may want a link
<Tooltip.Root>
  <Tooltip.Trigger asChild>
    <a href="/docs">Documentation</a>
  </Tooltip.Trigger>
  <Tooltip.Portal>
    <Tooltip.Content>View the docs</Tooltip.Content>
  </Tooltip.Portal>
</Tooltip.Root>
```

**Why good:** Radix passes all required props and event handlers to the anchor, maintaining accessibility

#### With Custom Components

```typescript
import { forwardRef } from "react";
import { Dialog } from "radix-ui";

// Custom component MUST use forwardRef and spread props
const CustomButton = forwardRef<HTMLButtonElement, React.ComponentProps<"button">>(
  ({ className, ...props }, ref) => {
    return <button ref={ref} className={className} {...props} />;
  }
);
CustomButton.displayName = "CustomButton";

// Use with asChild
<Dialog.Trigger asChild>
  <CustomButton className="custom-class">Open Dialog</CustomButton>
</Dialog.Trigger>
```

**Why this works:** forwardRef allows Radix to attach refs for positioning/focus, spreading props passes event handlers and ARIA attributes

---

### Pattern 4: Building Custom asChild Components with Slot

Use the `Slot` utility to build your own components with `asChild` support.

```typescript
import { forwardRef } from "react";
import { Slot } from "@radix-ui/react-slot";

export type ButtonProps = React.ComponentProps<"button"> & {
  asChild?: boolean;
};

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ asChild = false, className, ...props }, ref) => {
    const Comp = asChild ? Slot : "button";
    return <Comp ref={ref} className={className} {...props} />;
  }
);
Button.displayName = "Button";

// Usage - renders as button
<Button>Click me</Button>

// Usage with asChild - renders as anchor
<Button asChild>
  <a href="/page">Navigate</a>
</Button>
```

**Why good:** Slot merges all props onto the child element, eliminating wrapper elements while preserving behavior

---

### Pattern 5: Portal Usage for Overlays

Portal renders content outside the React component tree to escape CSS stacking contexts.

```typescript
import { Popover } from "radix-ui";

<Popover.Root>
  <Popover.Trigger>Toggle Popover</Popover.Trigger>
  <Popover.Portal>
    {/* Rendered in document.body, escaping parent overflow:hidden */}
    <Popover.Content className={className}>
      <Popover.Arrow />
      Popover content
    </Popover.Content>
  </Popover.Portal>
</Popover.Root>
```

**When to use:** All overlay components (dialogs, popovers, tooltips, dropdown menus)

#### Custom Portal Container

```typescript
import { useRef } from "react";
import { Dialog } from "radix-ui";

function DialogWithCustomContainer() {
  const containerRef = useRef<HTMLDivElement>(null);

  return (
    <>
      <div ref={containerRef} />
      <Dialog.Root>
        <Dialog.Trigger>Open</Dialog.Trigger>
        <Dialog.Portal container={containerRef.current}>
          <Dialog.Content>Content in custom container</Dialog.Content>
        </Dialog.Portal>
      </Dialog.Root>
    </>
  );
}
```

**When to use:** Micro-frontends, iframes, or specific DOM hierarchy requirements

---

### Pattern 6: Animation with data-state Attributes

Radix primitives expose `data-state` attributes for CSS-based animations. The unmount is suspended while exit animations complete.

#### CSS Keyframe Animation

```typescript
// Component
<Dialog.Portal>
  <Dialog.Overlay className="dialog-overlay" />
  <Dialog.Content className="dialog-content">
    {/* Content */}
  </Dialog.Content>
</Dialog.Portal>
```

```css
/* Styles - use your styling solution */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes fadeOut {
  from {
    opacity: 1;
  }
  to {
    opacity: 0;
  }
}

.dialog-overlay[data-state="open"] {
  animation: fadeIn 150ms ease-out;
}

.dialog-overlay[data-state="closed"] {
  animation: fadeOut 150ms ease-in;
}

.dialog-content[data-state="open"] {
  animation: fadeIn 150ms ease-out;
}

.dialog-content[data-state="closed"] {
  animation: fadeOut 150ms ease-in;
}
```

**Why CSS animations:** Radix detects animation end events and suspends unmount until completion

#### JavaScript Animation Libraries (Framer Motion)

```typescript
import { useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { Dialog } from "radix-ui";

function AnimatedDialog() {
  const [open, setOpen] = useState(false);

  return (
    <Dialog.Root open={open} onOpenChange={setOpen}>
      <Dialog.Trigger>Open</Dialog.Trigger>
      <AnimatePresence>
        {open && (
          <Dialog.Portal forceMount>
            <Dialog.Overlay asChild forceMount>
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
              />
            </Dialog.Overlay>
            <Dialog.Content asChild forceMount>
              <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.95 }}
              >
                <Dialog.Title>Animated Dialog</Dialog.Title>
              </motion.div>
            </Dialog.Content>
          </Dialog.Portal>
        )}
      </AnimatePresence>
    </Dialog.Root>
  );
}
```

**Why forceMount:** Prevents Radix from unmounting during JavaScript library exit animations

---

### Pattern 7: Focus Management

Radix handles focus automatically for accessible interactions.

#### Default Behavior

```typescript
// Focus automatically trapped in modal dialogs
// Focus returns to trigger on close
<Dialog.Root>
  <Dialog.Trigger>Open</Dialog.Trigger>
  <Dialog.Portal>
    <Dialog.Content>
      {/* Focus trapped here until closed */}
      <input autoFocus /> {/* Receives focus on open */}
    </Dialog.Content>
  </Dialog.Portal>
</Dialog.Root>
```

#### Custom Focus Control

```typescript
import { useRef } from "react";
import { AlertDialog } from "radix-ui";

function AlertDialogWithCustomFocus() {
  const cancelRef = useRef<HTMLButtonElement>(null);

  return (
    <AlertDialog.Root>
      <AlertDialog.Trigger>Delete</AlertDialog.Trigger>
      <AlertDialog.Portal>
        <AlertDialog.Content
          onOpenAutoFocus={(e) => {
            e.preventDefault();
            cancelRef.current?.focus(); // Focus cancel instead of first element
          }}
        >
          <AlertDialog.Title>Confirm Delete</AlertDialog.Title>
          <AlertDialog.Cancel ref={cancelRef}>Cancel</AlertDialog.Cancel>
          <AlertDialog.Action>Delete</AlertDialog.Action>
        </AlertDialog.Content>
      </AlertDialog.Portal>
    </AlertDialog.Root>
  );
}
```

**Why custom focus:** Destructive dialogs should focus the safe action (Cancel) by default

---

### Pattern 8: Accessible Labels

Radix provides Title and Description components for screen reader accessibility.

```typescript
import { Dialog } from "radix-ui";

<Dialog.Root>
  <Dialog.Trigger>Settings</Dialog.Trigger>
  <Dialog.Portal>
    <Dialog.Content
      aria-describedby={undefined} // Remove if no description
    >
      {/* Title is announced when dialog opens */}
      <Dialog.Title>Account Settings</Dialog.Title>

      {/* Description provides additional context */}
      <Dialog.Description>
        Manage your account preferences and security settings.
      </Dialog.Description>

      {/* Or visually hide but keep accessible */}
      <VisuallyHidden asChild>
        <Dialog.Description>
          This description is read by screen readers but not visible.
        </Dialog.Description>
      </VisuallyHidden>
    </Dialog.Content>
  </Dialog.Portal>
</Dialog.Root>
```

**Why mandatory:** Screen readers announce Title when dialog opens, Description provides context for the interaction

</patterns>

---

<integration>

## Integration Guide

**Radix is behavior-only:** Components are unstyled. Apply styles via `className` prop using your styling solution.

**Works with:**

- **Slot utility**: Build custom `asChild` components with `@radix-ui/react-slot`
- **Any CSS solution**: Styles applied via className prop
- **Animation libraries**: Use `forceMount` for JavaScript animation control

**Common Component Pairs:**

| Primitive    | Use Case                                                       |
| ------------ | -------------------------------------------------------------- |
| Dialog       | Modal dialogs, forms, confirmations                            |
| AlertDialog  | Destructive confirmations requiring explicit action            |
| DropdownMenu | Navigation menus, action menus                                 |
| Select       | Form selects with custom styling                               |
| Popover      | Non-modal floating content                                     |
| Tooltip      | Contextual information on hover/focus                          |
| Accordion    | Expandable content sections                                    |
| Tabs         | Tabbed interfaces                                              |
| Progress     | Progress bars (supports `value={undefined}` for indeterminate) |

**Preview Components (Unstable API):**

| Primitive            | Use Case                                         | Import Prefix | Version |
| -------------------- | ------------------------------------------------ | ------------- | ------- |
| OneTimePasswordField | OTP input with keyboard nav, paste, autofill     | `unstable_`   | 0.1.8   |
| PasswordToggleField  | Password visibility toggle with focus management | `unstable_`   | 0.1.3   |
| Form                 | Form validation with constraint API              | `unstable_`   | 0.1.8   |

**Note:** Preview components use `unstable_` prefix. APIs may change before stable release.

</integration>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST use compound component anatomy - Root, Trigger, Portal, Content, Close - for overlay components)**

**(You MUST use `forwardRef` and spread all props when using `asChild` with custom components - unless using React 19+ where `ref` is a regular prop)**

**(You MUST use Portal for overlays to escape CSS stacking contexts and parent overflow constraints)**

**(You MUST provide accessible labels via Title/Description components or ARIA attributes - Dialog logs console errors for missing Title)**

**Failure to follow these rules will break accessibility, focus management, and proper DOM rendering.**

</critical_reminders>
