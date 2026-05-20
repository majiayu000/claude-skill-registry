---
name: base-ui-react
description: MUI Base UI unstyled React components with Floating UI. Use for accessible components, Radix UI migration, render props API, or encountering positioning, popup, v1.0 beta issues.

  Keywords: base-ui, @base-ui-components/react, mui base ui, unstyled components, accessible components,
  render props, radix alternative, radix migration, floating-ui, positioner pattern, headless ui,
  accessible dialog, accessible select, accessible popover, accessible tooltip, accessible accordion,
  number field, cloudflare workers ui, beta components
license: MIT
metadata:
  version: "2.0.0"
  last_verified: "2025-11-18"
  production_tested: true
  token_savings: "~62%"
  errors_prevented: 10
  templates_included: 7
  references_included: 3
---

# Base UI React

**Status**: Beta (v1.0.0-beta.4) ⚠️ | **Last Verified**: 2025-11-18

---

## What Is Base UI?

MUI's unstyled, accessible React component library:
- 27+ accessible components
- Render props pattern
- Full styling control
- Floating UI integration
- Alternative to Radix UI

**Beta status:** v1.0.0-beta.4 (stable v1.0 expected Q4 2025)

---

## Quick Start

### Install

```bash
bun add @base-ui-components/react
```

### Basic Dialog

```typescript
import * as Dialog from '@base-ui-components/react/dialog';

export function MyDialog() {
  return (
    <Dialog.Root>
      <Dialog.Trigger>Open</Dialog.Trigger>
      <Dialog.Portal>
        <Dialog.Backdrop />
        <Dialog.Popup>
          <Dialog.Title>Title</Dialog.Title>
          <Dialog.Description>Content</Dialog.Description>
          <Dialog.Close>Close</Dialog.Close>
        </Dialog.Popup>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
```

### Basic Select

```typescript
import * as Select from '@base-ui-components/react/select';

<Select.Root>
  <Select.Trigger>
    <Select.Value placeholder="Select" />
  </Select.Trigger>
  <Select.Portal>
    <Select.Positioner>
      <Select.Popup>
        <Select.Option value="1">Option 1</Select.Option>
        <Select.Option value="2">Option 2</Select.Option>
      </Select.Popup>
    </Select.Positioner>
  </Select.Portal>
</Select.Root>
```

**Load `references/setup-guide.md` for complete examples.**

---

## Core Components

**Available (27+):**
- Dialog
- Select
- Popover
- Tooltip
- Accordion
- NumberField
- Checkbox
- Switch
- Tabs
- Slider
- And more...

---

## Critical Rules

### Always Do ✅

1. **Use Portal** for popups (Dialog, Select, Popover)
2. **Use Positioner** for floating elements
3. **Add Backdrop** for modal dialogs
4. **Style with Tailwind** (or any CSS)
5. **Use render props** (not asChild like Radix)
6. **Test accessibility** (ARIA built-in)
7. **Handle Portal edge cases** (SSR, hydration)
8. **Check beta docs** for breaking changes
9. **Use TypeScript** for better DX
10. **Test on target browsers**

### Never Do ❌

1. **Never use asChild** (use render function instead)
2. **Never skip Portal** for popups (positioning breaks)
3. **Never skip Positioner** (Floating UI won't work)
4. **Never assume API stability** (beta software)
5. **Never skip accessibility testing**
6. **Never use with React <19** (requires React 19+)
7. **Never skip Backdrop** for modals
8. **Never hardcode z-index** (use Portal)
9. **Never skip SSR testing** (hydration issues)
10. **Never assume Radix compatibility** (different API)

---

## With Tailwind

```typescript
<Dialog.Popup className="rounded-lg bg-white p-6 shadow-xl dark:bg-gray-800">
  <Dialog.Title className="text-xl font-bold text-gray-900 dark:text-white">
    Dialog Title
  </Dialog.Title>
  <Dialog.Description className="mt-2 text-gray-600 dark:text-gray-300">
    Dialog content here
  </Dialog.Description>
  <Dialog.Close className="mt-4 rounded bg-blue-500 px-4 py-2 text-white hover:bg-blue-600">
    Close
  </Dialog.Close>
</Dialog.Popup>
```

---

## Common Use Cases

### Use Case 1: Modal Dialog

```typescript
<Dialog.Root>
  <Dialog.Trigger className="btn">Open Modal</Dialog.Trigger>
  <Dialog.Portal>
    <Dialog.Backdrop className="fixed inset-0 bg-black/50" />
    <Dialog.Popup className="fixed left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 rounded-lg bg-white p-6">
      <Dialog.Title>Confirm Action</Dialog.Title>
      <Dialog.Description>Are you sure?</Dialog.Description>
      <Dialog.Close>Cancel</Dialog.Close>
    </Dialog.Popup>
  </Dialog.Portal>
</Dialog.Root>
```

### Use Case 2: Dropdown Select

```typescript
<Select.Root>
  <Select.Trigger className="flex items-center gap-2 rounded border px-4 py-2">
    <Select.Value placeholder="Select option" />
  </Select.Trigger>
  <Select.Portal>
    <Select.Positioner className="z-50">
      <Select.Popup className="rounded border bg-white shadow-lg">
        <Select.Option value="1" className="px-4 py-2 hover:bg-gray-100">
          Option 1
        </Select.Option>
        <Select.Option value="2" className="px-4 py-2 hover:bg-gray-100">
          Option 2
        </Select.Option>
      </Select.Popup>
    </Select.Positioner>
  </Select.Portal>
</Select.Root>
```

### Use Case 3: Tooltip

```typescript
import * as Tooltip from '@base-ui-components/react/tooltip';

<Tooltip.Root>
  <Tooltip.Trigger>Hover me</Tooltip.Trigger>
  <Tooltip.Portal>
    <Tooltip.Positioner>
      <Tooltip.Popup className="rounded bg-gray-900 px-2 py-1 text-sm text-white">
        Tooltip text
      </Tooltip.Popup>
    </Tooltip.Positioner>
  </Tooltip.Portal>
</Tooltip.Root>
```

---

## Beta Considerations

**Stable for production:**
- Dialog
- Popover
- Tooltip
- Select
- Accordion

**Use with caution:**
- NumberField (API may change)
- Complex form components

**Migration path:**
- v1.0 stable expected Q4 2025
- Breaking changes will be documented
- Codemods likely provided

---

## vs Radix UI

| Feature | Base UI | Radix UI |
|---------|---------|----------|
| Pattern | Render props | asChild |
| Positioning | Floating UI built-in | Manual |
| Beta | Yes | Stable |
| Tree-shaking | Better | Good |
| Bundle size | Smaller | Larger |

**When to use Base UI:**
- Prefer render props
- Need built-in positioning
- Want smaller bundle
- Okay with beta

**When to use Radix:**
- Need stability
- Prefer asChild pattern
- Established ecosystem

---

## Resources

**References** (`references/`):
- `example-reference.md` - Detailed component examples and patterns
- `migration-from-radix.md` - Complete migration guide from Radix UI (includes render prop pattern explanation)
- `setup-guide.md` - Installation and setup walkthrough

**Templates** (`templates/`):
- `Accordion.tsx` - Accordion component with render props
- `Dialog.tsx` - Modal dialog example
- `NumberField.tsx` - Number input with validation
- `Popover.tsx` - Popover with positioning
- `Select.tsx` - Select dropdown
- `Tooltip.tsx` - Tooltip component
- `migration-example.tsx` - Radix to Base UI migration example

---

## Official Documentation

- **Base UI**: <https://base-ui.mui.com/>
- **Components**: <https://base-ui.mui.com/components/>
- **Migration Guide**: <https://base-ui.mui.com/base-ui/getting-started/migration/>

---

**Questions? Issues?**

1. Check `references/setup-guide.md` for setup
2. Review beta status warnings
3. See official docs for latest updates
4. Consider Radix if need stability
