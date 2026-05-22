---
name: ux-accessibility-patterns
description: Focus management, keyboard navigation, ARIA attributes, and screen reader considerations for TMNL
triggers:
  - accessibility
  - a11y
  - aria
  - focus
  - keyboard navigation
  - screen reader
  - tabindex
---

# UX Accessibility Patterns

TMNL implements keyboard-first navigation with comprehensive ARIA attributes and focus management. This skill documents accessibility patterns for interactive components, overlays, and navigation.

## Overview

TMNL's accessibility strategy:
- **Keyboard-first** - All interactions accessible via keyboard
- **ARIA semantics** - Proper roles, labels, and live regions
- **Focus management** - Predictable focus flow, trap in modals
- **Screen reader friendly** - Announcements for dynamic content
- **Progressive enhancement** - Works without JavaScript where possible

**Target Compliance**: WCAG 2.1 Level AA

## Canonical Sources

### Primary Files
- `/src/lib/overlays/visual/renderers/ToastRenderer.tsx` - Toast ARIA patterns
- `/src/lib/overlays/visual/renderers/ModalRenderer.tsx` - Modal focus trap
- `/src/components/base/BaseModal/BaseModal.tsx` - Modal accessibility
- `/src/lib/hotkeys/hooks/useGlobalHotkeys.tsx` - Keyboard event handling
- `/src/lib/slider/v1/types.ts` - Slider ARIA props

### Key Type Definitions
- `/src/lib/slider/v1/types.ts` - `ariaLabel`, `ariaValueText` props
- `/src/components/base/BaseModal/types.ts` - Modal semantic props

## Patterns

### 1. Focus Management in Modals

**Pattern**: Trap focus within modal, restore on close.

**Canonical Implementation**: `/src/components/base/BaseModal/BaseModal.tsx`

```tsx
// Focus trap pattern
const ModalContent = forwardRef<HTMLDivElement, ModalContentProps>(
  ({ children, className, onEscapeKeyDown }, ref) => {
    const { isOpen, close } = useModal()
    const contentRef = useRef<HTMLDivElement>(null)

    // Focus trap on open
    useEffect(() => {
      if (!isOpen || !contentRef.current) return

      const previouslyFocused = document.activeElement as HTMLElement

      // Focus first focusable element in modal
      const focusable = contentRef.current.querySelectorAll(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
      )
      const firstFocusable = focusable[0] as HTMLElement
      firstFocusable?.focus()

      // Restore focus on close
      return () => {
        previouslyFocused?.focus()
      }
    }, [isOpen])

    // Trap Tab key within modal
    const handleKeyDown = (e: KeyboardEvent<HTMLDivElement>) => {
      if (e.key === 'Tab') {
        const focusable = contentRef.current!.querySelectorAll(
          'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        )
        const first = focusable[0] as HTMLElement
        const last = focusable[focusable.length - 1] as HTMLElement

        if (e.shiftKey && document.activeElement === first) {
          e.preventDefault()
          last.focus()
        } else if (!e.shiftKey && document.activeElement === last) {
          e.preventDefault()
          first.focus()
        }
      }

      if (e.key === 'Escape') {
        e.preventDefault()
        onEscapeKeyDown?.(e)
        close()
      }
    }

    return (
      <div
        ref={contentRef}
        role="dialog"
        aria-modal="true"
        onKeyDown={handleKeyDown}
      >
        {children}
      </div>
    )
  }
)
```

**ARIA Attributes**:
```tsx
// Modal overlay
<div
  className="modal-backdrop"
  aria-hidden="true" // Hide backdrop from screen readers
/>

// Modal content
<div
  role="dialog"
  aria-modal="true"      // Indicates modal behavior
  aria-labelledby="modal-title"  // Associates title
  aria-describedby="modal-description" // Associates description
>
  <h2 id="modal-title">Settings</h2>
  <p id="modal-description">Configure your preferences</p>
</div>
```

### 2. Keyboard Navigation in Lists/Grids

**Pattern**: Arrow keys navigate, Home/End jump to boundaries.

**Implementation Example**:
```tsx
function NavigableList({ items }: { items: string[] }) {
  const [focusedIndex, setFocusedIndex] = useState(0)
  const listRef = useRef<HTMLDivElement>(null)

  const handleKeyDown = (e: KeyboardEvent<HTMLDivElement>) => {
    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault()
        setFocusedIndex((i) => Math.min(i + 1, items.length - 1))
        break
      case 'ArrowUp':
        e.preventDefault()
        setFocusedIndex((i) => Math.max(i - 1, 0))
        break
      case 'Home':
        e.preventDefault()
        setFocusedIndex(0)
        break
      case 'End':
        e.preventDefault()
        setFocusedIndex(items.length - 1)
        break
      case 'Enter':
      case ' ':
        e.preventDefault()
        handleSelect(items[focusedIndex])
        break
    }
  }

  return (
    <div
      ref={listRef}
      role="listbox"
      aria-activedescendant={`item-${focusedIndex}`}
      onKeyDown={handleKeyDown}
      tabIndex={0}
    >
      {items.map((item, index) => (
        <div
          key={item}
          id={`item-${index}`}
          role="option"
          aria-selected={index === focusedIndex}
          tabIndex={-1} // Not directly focusable, managed by parent
        >
          {item}
        </div>
      ))}
    </div>
  )
}
```

**AG-Grid Accessibility**:
TMNL's data grids inherit AG-Grid's built-in keyboard navigation:
- Arrow keys: Cell navigation
- Tab: Move between grid and other controls
- Enter: Edit cell
- Escape: Cancel edit
- Page Up/Down: Scroll viewport
- Home/End: Jump to first/last column
- Ctrl+Home/End: Jump to first/last row

### 3. ARIA Live Regions for Dynamic Content

**Pattern**: Announce dynamic changes to screen readers.

**Canonical Implementation**: `/src/lib/overlays/visual/renderers/ToastRenderer.tsx`

```tsx
// Toast notifications as live regions
<div
  role="alert"         // For errors/warnings (interrupts)
  aria-live="polite"   // For info/success (doesn't interrupt)
  style={toastContainerStyles}
>
  {content}
</div>

// Variant-specific live regions
const TOAST_ARIA_ROLES = {
  error: "alert",        // Assertive, interrupts
  warning: "alert",
  success: "status",     // Polite
  info: "status",
}

const TOAST_ARIA_LIVE = {
  error: "assertive",
  warning: "assertive",
  success: "polite",
  info: "polite",
}

<div
  role={TOAST_ARIA_ROLES[variant]}
  aria-live={TOAST_ARIA_LIVE[variant]}
>
  {message}
</div>
```

**Loading State Announcements**:
```tsx
// Loading indicator
<div
  role="status"
  aria-live="polite"
  aria-busy="true"
>
  <span className="sr-only">Loading data...</span>
  <LoadingSpinner aria-hidden="true" />
</div>

// Completion announcement
<div
  role="status"
  aria-live="polite"
  aria-busy="false"
>
  <span className="sr-only">Data loaded successfully</span>
</div>
```

**Screen Reader Only Text**:
```tsx
// Visually hidden but announced
<span className="sr-only">
  {loaded} of {total} items loaded
</span>

// CSS for sr-only class
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}
```

### 4. Slider/Range Input Accessibility

**Pattern**: Proper ARIA attributes for custom sliders.

**Canonical Implementation**: `/src/lib/slider/v1/types.ts`

```typescript
export interface SliderProps {
  // Accessibility props
  ariaLabel?: string         // "Volume control"
  ariaValueText?: string     // "-12.5 dB" (human-readable value)
}

// In slider component
<div
  role="slider"
  aria-label={ariaLabel ?? "Slider"}
  aria-valuemin={config.min}
  aria-valuemax={config.max}
  aria-valuenow={value}
  aria-valuetext={ariaValueText ?? format(value, config.precision, config.unit)}
  aria-orientation={config.orientation}
  tabIndex={0}
  onKeyDown={handleKeyDown}
>
  {/* Visual slider */}
</div>
```

**Keyboard Controls for Sliders**:
```tsx
const handleKeyDown = (e: KeyboardEvent) => {
  const step = config.step ?? 1
  const largeStep = step * 10
  const sensitivity = e.shiftKey ? 0.1 : e.ctrlKey ? 0.01 : 1

  switch (e.key) {
    case 'ArrowRight':
    case 'ArrowUp':
      e.preventDefault()
      dispatch({ type: 'INCREMENT', amount: step * sensitivity })
      break
    case 'ArrowLeft':
    case 'ArrowDown':
      e.preventDefault()
      dispatch({ type: 'DECREMENT', amount: step * sensitivity })
      break
    case 'PageUp':
      e.preventDefault()
      dispatch({ type: 'INCREMENT', amount: largeStep })
      break
    case 'PageDown':
      e.preventDefault()
      dispatch({ type: 'DECREMENT', amount: largeStep })
      break
    case 'Home':
      e.preventDefault()
      dispatch({ type: 'SET_VALUE', value: config.min })
      break
    case 'End':
      e.preventDefault()
      dispatch({ type: 'SET_VALUE', value: config.max })
      break
  }
}
```

### 5. Button Accessibility

**Pattern**: Semantic buttons with proper ARIA labels.

```tsx
// Icon-only button
<button
  onClick={handleDelete}
  aria-label="Delete item"
  className="p-2"
>
  <TrashIcon aria-hidden="true" /> {/* Hide icon from SR */}
</button>

// Button with tooltip
<button
  onClick={handleSave}
  aria-label="Save changes"
  aria-describedby="save-tooltip"
>
  Save
</button>
<div id="save-tooltip" role="tooltip" className="sr-only">
  Saves your changes to local storage
</div>

// Toggle button
<button
  onClick={toggleSidebar}
  aria-label={isOpen ? "Close sidebar" : "Open sidebar"}
  aria-pressed={isOpen}
  aria-expanded={isOpen}
>
  <MenuIcon aria-hidden="true" />
</button>
```

### 6. Focus Visible Styling

**Pattern**: Show focus indicator only for keyboard navigation, not mouse clicks.

**CSS Implementation**:
```css
/* Hide focus ring on mouse click, show on keyboard nav */
*:focus {
  outline: none; /* Remove default */
}

*:focus-visible {
  outline: 2px solid var(--tmnl-focus-ring, #3b82f6);
  outline-offset: 2px;
}

/* Button focus styles */
button:focus-visible {
  outline: 2px solid var(--tmnl-focus-ring, #3b82f6);
  outline-offset: 2px;
}

/* Input focus styles */
input:focus-visible,
textarea:focus-visible,
select:focus-visible {
  outline: none;
  border-color: var(--tmnl-focus-ring, #3b82f6);
  box-shadow: 0 0 0 1px var(--tmnl-focus-ring, #3b82f6);
}
```

**Tailwind Classes**:
```tsx
<button className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2">
  Click me
</button>
```

### 7. Skip Links

**Pattern**: Allow keyboard users to skip navigation.

```tsx
function App() {
  return (
    <>
      <a
        href="#main-content"
        className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-50 focus:px-4 focus:py-2 focus:bg-white focus:text-black"
      >
        Skip to main content
      </a>

      <header>
        <nav>{/* ... */}</nav>
      </header>

      <main id="main-content" tabIndex={-1}>
        {/* Main content */}
      </main>
    </>
  )
}

// CSS for conditional visibility
.sr-only {
  /* Visually hidden by default */
}

.focus\:not-sr-only:focus {
  position: static;
  width: auto;
  height: auto;
  /* ... make visible on focus */
}
```

### 8. Input Scope for Native Suppression

**Pattern**: Prevent global hotkeys from interfering with text input.

**Canonical Implementation**: `/src/lib/hotkeys/hooks/useGlobalHotkeys.tsx`

```tsx
// Check if event target is an input element
const isInputElement = (element: EventTarget | null): boolean => {
  if (!(element instanceof HTMLElement)) return false

  const tagName = element.tagName.toLowerCase()
  const isContentEditable = element.isContentEditable

  return (
    tagName === 'input' ||
    tagName === 'textarea' ||
    tagName === 'select' ||
    isContentEditable
  )
}

// In keyboard handler
const handleKeyDown = (e: KeyboardEvent) => {
  // For input elements, only allow escape key through
  if (isInputElement(e.target)) {
    if (e.key !== 'Escape') return
  }

  // Process hotkey
  const result = processKeyboardEvent(e, bindings, sequence)
  if (result.shouldPreventDefault) {
    e.preventDefault()
  }
}
```

**Input-Scoped vs Global Hotkeys**:
```typescript
// Global scope - always active
hotkeyActions.addBinding(registry, {
  key: ['ctrl+s'],
  commandId: 'save',
  scope: ScopeId.Global,
})

// Input scope - only active when input focused
hotkeyActions.addBinding(registry, {
  key: ['escape'],
  commandId: 'cancel-edit',
  scope: ScopeId.Input,
})
```

## Examples

### Example 1: Accessible Command Palette

```tsx
import { useMinibuffer } from '@/lib/minibuffer'

function CommandPalette() {
  const {
    isActive,
    input,
    completions,
    selectedIndex,
    ops,
  } = useMinibuffer()

  const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault()
        ops.selectNext()
        break
      case 'ArrowUp':
        e.preventDefault()
        ops.selectPrevious()
        break
      case 'Enter':
        e.preventDefault()
        ops.confirm()
        break
      case 'Escape':
        e.preventDefault()
        ops.cancel()
        break
    }
  }

  if (!isActive) return null

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="command-palette-label"
    >
      <label id="command-palette-label" className="sr-only">
        Command palette
      </label>

      <input
        type="text"
        value={input}
        onChange={(e) => ops.setInput(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Enter command..."
        aria-autocomplete="list"
        aria-controls="command-list"
        aria-activedescendant={`command-${selectedIndex}`}
        autoFocus
      />

      <ul
        id="command-list"
        role="listbox"
        aria-label="Available commands"
      >
        {completions.map((completion, index) => (
          <li
            key={completion.id}
            id={`command-${index}`}
            role="option"
            aria-selected={index === selectedIndex}
            onClick={() => {
              ops.selectIndex(index)
              ops.confirm()
            }}
          >
            {completion.label}
          </li>
        ))}
      </ul>
    </div>
  )
}
```

### Example 2: Accessible Data Grid with Keyboard Nav

```tsx
import { AgGridReact } from 'ag-grid-react'

function AccessibleDataGrid({ rowData, columnDefs }) {
  return (
    <div
      className="ag-theme-tmnl"
      role="region"
      aria-label="Data table"
    >
      <AgGridReact
        rowData={rowData}
        columnDefs={columnDefs}
        // AG-Grid accessibility features
        suppressCellFocus={false}  // Enable cell focus
        enableCellTextSelection={true}
        ensureDomOrder={true}      // Maintain DOM order for SR
        // Keyboard navigation (built-in)
        navigateToNextCell={(params) => {
          // Custom navigation logic if needed
          return params.nextCellPosition
        }}
      />
    </div>
  )
}
```

### Example 3: Accessible Toast with Screen Reader Announcement

```tsx
import { useToast } from '@/lib/overlays'

function NotificationButton() {
  const toast = useToast()

  const handleSuccess = () => {
    toast.success(
      <div>
        <strong>File saved</strong>
        <p>Your changes have been saved successfully.</p>
      </div>,
      {
        position: "top-center",
        duration: 5000,
      }
    )
  }

  return (
    <button
      onClick={handleSuccess}
      aria-label="Save file"
    >
      Save
    </button>
  )
}

// ToastRenderer automatically includes ARIA:
// <div role="alert" aria-live="polite">
//   <strong>File saved</strong>
//   <p>Your changes have been saved successfully.</p>
// </div>
```

## Anti-Patterns

### DON'T: Use divs as Buttons

```tsx
// WRONG - Not keyboard accessible, no semantics
<div onClick={handleClick}>
  Click me
</div>

// CORRECT - Use semantic button
<button onClick={handleClick}>
  Click me
</button>

// If you MUST use div (rare cases)
<div
  role="button"
  tabIndex={0}
  onClick={handleClick}
  onKeyDown={(e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault()
      handleClick()
    }
  }}
>
  Click me
</div>
```

### DON'T: Remove Focus Outlines Globally

```css
/* WRONG - Breaks keyboard navigation */
* {
  outline: none !important;
}

/* CORRECT - Use :focus-visible */
*:focus {
  outline: none;
}

*:focus-visible {
  outline: 2px solid var(--tmnl-focus-ring);
  outline-offset: 2px;
}
```

### DON'T: Use placeholder as Label

```tsx
// WRONG - Placeholder disappears on focus
<input type="text" placeholder="Email address" />

// CORRECT - Use label
<label htmlFor="email">Email address</label>
<input id="email" type="text" placeholder="you@example.com" />

// Or visually hidden label
<label htmlFor="email" className="sr-only">Email address</label>
<input id="email" type="text" placeholder="Email address" />
```

### DON'T: Trap Focus Without Escape Hatch

```tsx
// WRONG - No way to close modal with keyboard
<div role="dialog" aria-modal="true">
  <h2>Settings</h2>
  <button onClick={close}>Close</button> {/* Only mouse accessible */}
</div>

// CORRECT - Escape key closes modal
<div
  role="dialog"
  aria-modal="true"
  onKeyDown={(e) => {
    if (e.key === 'Escape') close()
  }}
>
  <h2>Settings</h2>
  <button onClick={close}>Close</button>
</div>
```

### DON'T: Use aria-hidden on Interactive Elements

```tsx
// WRONG - Button is hidden from screen readers
<button aria-hidden="true" onClick={handleSave}>
  Save
</button>

// CORRECT - Icon is hidden, button is accessible
<button onClick={handleSave} aria-label="Save file">
  <SaveIcon aria-hidden="true" />
</button>
```

### DON'T: Auto-Focus Aggressively

```tsx
// WRONG - Steals focus from user's current location
useEffect(() => {
  inputRef.current?.focus()
}, []) // Runs on every render

// CORRECT - Only focus when modal opens
useEffect(() => {
  if (isOpen && inputRef.current) {
    inputRef.current.focus()
  }
}, [isOpen])
```

## Testing Accessibility

### Manual Testing Checklist

1. **Keyboard Navigation**:
   - [ ] Tab moves focus through interactive elements in logical order
   - [ ] Shift+Tab moves backward
   - [ ] Enter/Space activate buttons
   - [ ] Arrow keys navigate lists/menus
   - [ ] Escape closes modals/overlays
   - [ ] All interactive elements are reachable via keyboard

2. **Focus Indicators**:
   - [ ] Focus ring visible on keyboard navigation
   - [ ] Focus ring NOT visible on mouse click
   - [ ] Focus ring has sufficient contrast (3:1 minimum)
   - [ ] Focus doesn't get trapped unintentionally

3. **Screen Reader** (VoiceOver on macOS, NVDA on Windows):
   - [ ] All images have alt text
   - [ ] Buttons announce their purpose
   - [ ] Form inputs announce their labels
   - [ ] Live regions announce dynamic changes
   - [ ] Modal announces "dialog" role
   - [ ] Headings create proper document outline

4. **Color Contrast**:
   - [ ] Normal text: 4.5:1 contrast ratio
   - [ ] Large text (18pt+): 3:1 contrast ratio
   - [ ] UI components: 3:1 contrast ratio
   - [ ] Test with browser DevTools contrast checker

### Automated Testing Tools

**Browser Extensions**:
- [axe DevTools](https://www.deque.com/axe/devtools/) - Free accessibility checker
- [WAVE](https://wave.webaim.org/extension/) - Visual accessibility evaluation
- [Lighthouse](https://developer.chrome.com/docs/lighthouse/) - Built into Chrome DevTools

**Jest + Testing Library**:
```tsx
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { axe, toHaveNoViolations } from 'jest-axe'

expect.extend(toHaveNoViolations)

test('modal is accessible', async () => {
  const { container } = render(<Modal open={true} />)

  // Automated a11y check
  const results = await axe(container)
  expect(results).toHaveNoViolations()

  // Keyboard navigation
  const closeButton = screen.getByRole('button', { name: /close/i })
  await userEvent.tab()
  expect(closeButton).toHaveFocus()

  await userEvent.keyboard('{Enter}')
  expect(screen.queryByRole('dialog')).not.toBeInTheDocument()
})
```

### ARIA Validator

Use [ARIA APG](https://www.w3.org/WAI/ARIA/apg/) patterns as reference:
- **Dialog (Modal)**: https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/
- **Listbox**: https://www.w3.org/WAI/ARIA/apg/patterns/listbox/
- **Slider**: https://www.w3.org/WAI/ARIA/apg/patterns/slider/
- **Alert**: https://www.w3.org/WAI/ARIA/apg/patterns/alert/

## Related Skills

- `ux-interaction-patterns` - Keyboard shortcuts, modifier keys
- `ux-feedback-patterns` - Screen reader announcements for toasts
- `ux-overlay-patterns` - Modal focus trap, drawer accessibility

## References

- WCAG 2.1: https://www.w3.org/WAI/WCAG21/quickref/
- ARIA Authoring Practices: https://www.w3.org/WAI/ARIA/apg/
- WebAIM: https://webaim.org/
- Modal Focus Trap: `/src/components/base/BaseModal/BaseModal.tsx`
- Toast ARIA: `/src/lib/overlays/visual/renderers/ToastRenderer.tsx`
- Hotkey Input Scoping: `/src/lib/hotkeys/hooks/useGlobalHotkeys.tsx`
