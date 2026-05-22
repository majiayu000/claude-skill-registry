---
name: accessibility-wcag
description: Build accessible web applications meeting WCAG 2.1 AA standards. Covers ARIA attributes, keyboard navigation, screen reader optimization, focus management, color contrast, semantic HTML, and accessible components. Use for a11y audits, accessible UI development, and inclusive design.
---

# Accessibility & WCAG Compliance

Build inclusive, accessible interfaces that work for all users.

## Instructions

1. **Use semantic HTML first** - ARIA is a last resort, not a first choice
2. **Ensure keyboard navigation** - All interactive elements must be keyboard accessible
3. **Provide text alternatives** - Images, icons, and media need accessible descriptions
4. **Maintain focus visibility** - Never remove focus outlines without replacement
5. **Test with assistive technologies** - Use screen readers and keyboard-only navigation

## WCAG 2.1 AA Requirements

### Color Contrast Ratios
- **Normal text**: 4.5:1 minimum
- **Large text** (18pt+ or 14pt bold): 3:1 minimum
- **UI components**: 3:1 minimum
- **Focus indicators**: 3:1 minimum

### Focus Management
```tsx
// Visible focus styles
<button className="
  focus:outline-none
  focus-visible:ring-2
  focus-visible:ring-blue-500
  focus-visible:ring-offset-2
">
  Click me
</button>

// Focus trap for modals
import { FocusTrap } from '@headlessui/react';

function Modal({ isOpen, children }) {
  return isOpen ? (
    <FocusTrap>
      <div role="dialog" aria-modal="true">
        {children}
      </div>
    </FocusTrap>
  ) : null;
}
```

## Semantic HTML

### Use Correct Elements

```tsx
// Good - semantic
<nav aria-label="Main navigation">
  <ul>
    <li><a href="/home">Home</a></li>
    <li><a href="/about">About</a></li>
  </ul>
</nav>

<main>
  <article>
    <header>
      <h1>Article Title</h1>
      <time dateTime="2024-01-15">January 15, 2024</time>
    </header>
    <section aria-labelledby="intro">
      <h2 id="intro">Introduction</h2>
      <p>Content...</p>
    </section>
  </article>
</main>

// Bad - div soup
<div class="nav">
  <div class="nav-item">Home</div>
</div>
```

### Heading Hierarchy

```tsx
// Correct heading order
<h1>Page Title</h1>          // Only one per page
  <h2>Section</h2>
    <h3>Subsection</h3>
    <h3>Subsection</h3>
  <h2>Section</h2>
    <h3>Subsection</h3>
```

## ARIA Patterns

### Live Regions

```tsx
// Announce dynamic changes
<div
  role="status"
  aria-live="polite"
  aria-atomic="true"
>
  {statusMessage}
</div>

// For urgent alerts
<div
  role="alert"
  aria-live="assertive"
>
  {errorMessage}
</div>
```

### Accessible Forms

```tsx
function AccessibleForm() {
  const [errors, setErrors] = useState<Record<string, string>>({});

  return (
    <form aria-describedby="form-instructions">
      <p id="form-instructions" className="sr-only">
        Required fields are marked with an asterisk
      </p>

      <div>
        <label htmlFor="email">
          Email <span aria-hidden="true">*</span>
          <span className="sr-only">(required)</span>
        </label>
        <input
          id="email"
          type="email"
          required
          aria-required="true"
          aria-invalid={!!errors.email}
          aria-describedby={errors.email ? "email-error" : undefined}
        />
        {errors.email && (
          <p id="email-error" role="alert" className="text-red-600">
            {errors.email}
          </p>
        )}
      </div>

      <button type="submit">Submit</button>
    </form>
  );
}
```

### Accessible Buttons

```tsx
// Icon-only button
<button
  type="button"
  aria-label="Close dialog"
  onClick={onClose}
>
  <XIcon aria-hidden="true" />
</button>

// Toggle button
<button
  type="button"
  aria-pressed={isActive}
  onClick={() => setIsActive(!isActive)}
>
  {isActive ? 'Active' : 'Inactive'}
</button>

// Loading button
<button
  type="submit"
  disabled={isLoading}
  aria-busy={isLoading}
  aria-disabled={isLoading}
>
  {isLoading ? (
    <>
      <Spinner aria-hidden="true" />
      <span className="sr-only">Loading...</span>
    </>
  ) : (
    'Submit'
  )}
</button>
```

### Accessible Modal

```tsx
function AccessibleModal({ isOpen, onClose, title, children }) {
  const modalRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (isOpen) {
      // Store current focus
      const previousFocus = document.activeElement;

      // Focus modal
      modalRef.current?.focus();

      // Handle escape key
      const handleEscape = (e: KeyboardEvent) => {
        if (e.key === 'Escape') onClose();
      };
      document.addEventListener('keydown', handleEscape);

      // Trap focus and restore on close
      return () => {
        document.removeEventListener('keydown', handleEscape);
        (previousFocus as HTMLElement)?.focus();
      };
    }
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
      ref={modalRef}
      tabIndex={-1}
    >
      <h2 id="modal-title">{title}</h2>
      {children}
      <button onClick={onClose}>Close</button>
    </div>
  );
}
```

## Keyboard Navigation

### Required Keyboard Support

| Element | Keys |
|---------|------|
| Buttons | Enter, Space |
| Links | Enter |
| Checkboxes | Space |
| Radio buttons | Arrow keys |
| Tabs | Arrow keys, Home, End |
| Menus | Arrow keys, Enter, Escape |
| Modals | Tab (trapped), Escape |

### Skip Link

```tsx
// First element in body
<a
  href="#main-content"
  className="
    sr-only focus:not-sr-only
    focus:absolute focus:top-4 focus:left-4
    focus:z-50 focus:bg-white focus:px-4 focus:py-2
  "
>
  Skip to main content
</a>

<main id="main-content" tabIndex={-1}>
  {/* Page content */}
</main>
```

## Screen Reader Utilities

```tsx
// Visually hidden but screen reader accessible
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

// Show on focus (for skip links)
.sr-only-focusable:focus {
  position: static;
  width: auto;
  height: auto;
  margin: 0;
  overflow: visible;
  clip: auto;
  white-space: normal;
}
```

## Testing Checklist

### Automated Testing
- [ ] Run axe-core or similar automated a11y scanner
- [ ] Check color contrast with browser devtools
- [ ] Validate HTML for semantic correctness

### Manual Testing
- [ ] Navigate entire page with keyboard only (Tab, Enter, Space, Arrow keys)
- [ ] Test with screen reader (NVDA, VoiceOver, JAWS)
- [ ] Verify focus is visible and logical order
- [ ] Check all images have alt text
- [ ] Verify form labels are associated
- [ ] Test at 200% zoom

### Screen Reader Testing Commands

**VoiceOver (Mac)**
- Cmd + F5: Toggle VoiceOver
- Ctrl + Option + arrows: Navigate
- Ctrl + Option + Space: Activate

**NVDA (Windows)**
- Insert + Space: Toggle browse mode
- H: Next heading
- Tab: Next focusable element

## Common Issues to Avoid

1. **Missing alt text** - Every `<img>` needs alt (empty for decorative)
2. **Missing form labels** - Every input needs associated label
3. **Low contrast** - Check all text meets 4.5:1 ratio
4. **Keyboard traps** - Users must be able to navigate away
5. **Missing focus styles** - Never `outline: none` without replacement
6. **Auto-playing media** - Provide pause controls
7. **Timing issues** - Avoid time limits or provide extensions

## When to Use

- Building any web application
- Conducting accessibility audits
- Fixing a11y issues
- Creating component libraries
- Meeting legal compliance requirements

## Notes

- WCAG 2.1 AA is the standard requirement for most organizations
- Some industries require AAA compliance
- Test with real users with disabilities when possible
- Accessibility benefits all users (SEO, mobile, etc.)
