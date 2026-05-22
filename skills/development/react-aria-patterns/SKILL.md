---
name: react-aria-patterns
description: React Aria (Adobe) accessible component patterns for building WCAG-compliant interactive UI with hooks. Use when implementing buttons, dialogs, comboboxes, menus, and other accessible components in React applications.
context: fork
agent: accessibility-specialist
version: 1.0.0
tags: [accessibility, react, aria, a11y, react-aria, wcag, hooks, adobe]
allowed-tools: [Read, Write, Grep, Glob, Bash]
author: SkillForge
user-invocable: false
---

# React Aria Patterns

Build accessible UI components using Adobe's React Aria hooks library with React 19 patterns.

## When to Use

- Building accessible buttons, links, and toggles with keyboard/screen reader support
- Implementing modal dialogs with proper focus management and trapping
- Creating autocomplete/combobox components with filtering and selection
- Building menu systems with roving tabindex and proper ARIA roles
- Implementing accessible tables, listboxes, and selection patterns

## Quick Reference

### useButton - Accessible Button Component

```tsx
import { useRef } from 'react';
import { useButton, useFocusRing, mergeProps } from 'react-aria';
import type { AriaButtonProps } from 'react-aria';

function Button(props: AriaButtonProps & { className?: string }) {
  const ref = useRef<HTMLButtonElement>(null);
  const { focusProps, isFocusVisible } = useFocusRing();
  const { buttonProps } = useButton(props, ref);

  return (
    <button
      {...mergeProps(buttonProps, focusProps)}
      ref={ref}
      className={`${props.className ?? ''} ${isFocusVisible ? 'ring-2 ring-blue-500' : ''}`}
    >
      {props.children}
    </button>
  );
}
```

### useDialog - Modal Dialog with Focus Management

```tsx
import { useRef } from 'react';
import { useDialog, useModalOverlay, FocusScope, mergeProps } from 'react-aria';
import { useOverlayTriggerState } from 'react-stately';

function Modal({ state, title, children }) {
  const ref = useRef<HTMLDivElement>(null);
  const { modalProps, underlayProps } = useModalOverlay({}, state, ref);
  const { dialogProps, titleProps } = useDialog({ 'aria-label': title }, ref);

  return (
    <div {...underlayProps} className="fixed inset-0 z-50 bg-black/50 flex items-center justify-center">
      <FocusScope contain restoreFocus autoFocus>
        <div {...mergeProps(modalProps, dialogProps)} ref={ref} className="bg-white rounded-lg p-6">
          <h2 {...titleProps} className="text-xl font-semibold mb-4">{title}</h2>
          {children}
        </div>
      </FocusScope>
    </div>
  );
}
```

### useComboBox - Accessible Autocomplete

```tsx
import { useRef } from 'react';
import { useComboBox, useFilter } from 'react-aria';
import { useComboBoxState } from 'react-stately';

function ComboBox(props) {
  const { contains } = useFilter({ sensitivity: 'base' });
  const state = useComboBoxState({ ...props, defaultFilter: contains });
  const inputRef = useRef(null), buttonRef = useRef(null), listBoxRef = useRef(null);

  const { buttonProps, inputProps, listBoxProps, labelProps } = useComboBox(
    { ...props, inputRef, buttonRef, listBoxRef }, state
  );

  return (
    <div className="relative inline-flex flex-col">
      <label {...labelProps}>{props.label}</label>
      <div className="flex">
        <input {...inputProps} ref={inputRef} className="border rounded-l px-3 py-2" />
        <button {...buttonProps} ref={buttonRef} className="border rounded-r px-2">&#9660;</button>
      </div>
      {state.isOpen && (
        <ul {...listBoxProps} ref={listBoxRef} className="absolute top-full w-full border bg-white">
          {[...state.collection].map((item) => (
            <li key={item.key} className="px-3 py-2 hover:bg-gray-100">{item.rendered}</li>
          ))}
        </ul>
      )}
    </div>
  );
}
```

## Key Decisions

| Decision | Option A | Option B | Recommendation |
|----------|----------|----------|----------------|
| Hook vs Component | `useButton` hooks | `Button` from react-aria-components | **Hooks** for control, Components for speed |
| Focus Management | Manual `tabIndex` | `FocusScope` component | **FocusScope** - trapping, restore, auto-focus |
| Virtual Lists | Native scroll | `useVirtualizer` + `useListBox` | **Virtualizer** for lists > 100 items |
| State Management | Local useState | react-stately hooks | **react-stately** - designed for a11y |

## Anti-Patterns (FORBIDDEN)

```tsx
// NEVER use div with onClick for interactive elements
<div onClick={handleClick}>Click me</div>  // Missing keyboard support!

// ALWAYS use useButton or native button
const { buttonProps } = useButton({ onPress: handleClick }, ref);
<div {...buttonProps} ref={ref}>Click me</div>

// NEVER handle focus manually for modals
useEffect(() => { modalRef.current?.focus(); }, []);  // Incomplete!

// ALWAYS use FocusScope for modals/overlays
<FocusScope contain restoreFocus autoFocus>
  <div role="dialog">...</div>
</FocusScope>

// NEVER forget aria-live for dynamic announcements
<div>{errorMessage}</div>  // Screen readers won't announce!

// ALWAYS use aria-live for status updates
<div aria-live="polite" className="sr-only">{errorMessage}</div>

// NEVER omit label associations
<input type="text" placeholder="Email" />  // No accessible name!

// ALWAYS associate labels properly
<label {...labelProps}>Email</label>
<input {...inputProps} />
```

## Related Skills

- `a11y-testing` - Automated accessibility testing with jest-axe and Playwright
- `focus-management` - Advanced focus patterns and keyboard navigation
- `design-system-starter` - Building accessible component libraries
- `i18n-date-patterns` - Internationalization for accessible content

## Capability Details

### useButton-hook
**Keywords:** button, useButton, press, tap, keyboard, click, onPress, focus ring
**Solves:**
- How to create accessible custom buttons
- Handling keyboard and pointer interactions consistently
- Focus ring visibility management with useFocusRing

### useDialog-modal
**Keywords:** dialog, modal, useDialog, useModalOverlay, FocusScope, overlay, trap
**Solves:**
- Building accessible modal dialogs with proper ARIA roles
- Focus trapping within overlays using FocusScope
- Restoring focus to trigger element on close

### useComboBox-autocomplete
**Keywords:** combobox, autocomplete, useComboBox, typeahead, filter, select, dropdown
**Solves:**
- Accessible autocomplete/typeahead inputs with filtering
- Keyboard navigation through options (arrow keys, enter, escape)
- Screen reader announcements for selection changes

### focus-scope-management
**Keywords:** focus, FocusScope, contain, restore, autoFocus, trap, keyboard navigation
**Solves:**
- Trapping focus within modals and popovers (contain prop)
- Restoring focus to trigger elements on unmount (restoreFocus prop)
- Auto-focusing first focusable element (autoFocus prop)
