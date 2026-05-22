---
name: web-accessibility
description: Build accessible web applications following WCAG guidelines. Use when implementing ARIA patterns, keyboard navigation, screen reader support, or ensuring accessibility compliance. Triggers on accessibility, a11y, WCAG, ARIA, screen reader, keyboard navigation.
---

# Web Accessibility (WCAG 2.1)

Build accessible web applications that work for everyone.

## ARIA Patterns

### Button
```tsx
<button
  type="button"
  aria-pressed={isPressed}
  aria-disabled={isDisabled}
  onClick={handleClick}
>
  Toggle Feature
</button>
```

### Modal Dialog
```tsx
<div
  role="dialog"
  aria-modal="true"
  aria-labelledby="modal-title"
  aria-describedby="modal-description"
>
  <h2 id="modal-title">Confirm Action</h2>
  <p id="modal-description">Are you sure you want to proceed?</p>
  <button onClick={onConfirm}>Confirm</button>
  <button onClick={onCancel}>Cancel</button>
</div>
```

### Navigation Menu
```tsx
<nav aria-label="Main navigation">
  <ul role="menubar">
    <li role="none">
      <a role="menuitem" href="/home">Home</a>
    </li>
    <li role="none">
      <button
        role="menuitem"
        aria-haspopup="true"
        aria-expanded={isOpen}
      >
        Products
      </button>
      {isOpen && (
        <ul role="menu" aria-label="Products submenu">
          <li role="none">
            <a role="menuitem" href="/products/new">New</a>
          </li>
        </ul>
      )}
    </li>
  </ul>
</nav>
```

## Keyboard Navigation

### Focus Management
```tsx
import { useEffect, useRef } from 'react';

function Modal({ isOpen, onClose, children }) {
  const modalRef = useRef<HTMLDivElement>(null);
  const previousFocus = useRef<HTMLElement | null>(null);

  useEffect(() => {
    if (isOpen) {
      previousFocus.current = document.activeElement as HTMLElement;
      modalRef.current?.focus();
    } else {
      previousFocus.current?.focus();
    }
  }, [isOpen]);

  // Trap focus within modal
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Escape') {
      onClose();
    }
    
    if (e.key === 'Tab') {
      const focusable = modalRef.current?.querySelectorAll(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
      );
      
      if (focusable && focusable.length > 0) {
        const first = focusable[0] as HTMLElement;
        const last = focusable[focusable.length - 1] as HTMLElement;
        
        if (e.shiftKey && document.activeElement === first) {
          e.preventDefault();
          last.focus();
        } else if (!e.shiftKey && document.activeElement === last) {
          e.preventDefault();
          first.focus();
        }
      }
    }
  };

  if (!isOpen) return null;

  return (
    <div
      ref={modalRef}
      role="dialog"
      aria-modal="true"
      tabIndex={-1}
      onKeyDown={handleKeyDown}
    >
      {children}
    </div>
  );
}
```

## Color Contrast

Minimum contrast ratios (WCAG AA):
- Normal text: 4.5:1
- Large text (18pt+): 3:1
- UI components: 3:1

```typescript
function getContrastRatio(color1: string, color2: string): number {
  const lum1 = getLuminance(color1);
  const lum2 = getLuminance(color2);
  const lighter = Math.max(lum1, lum2);
  const darker = Math.min(lum1, lum2);
  return (lighter + 0.05) / (darker + 0.05);
}

function getLuminance(hex: string): number {
  const rgb = hexToRgb(hex);
  const [r, g, b] = rgb.map((c) => {
    c = c / 255;
    return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
  });
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}
```

## Accessible Forms

```tsx
<form onSubmit={handleSubmit}>
  <div>
    <label htmlFor="email">
      Email address
      <span aria-hidden="true">*</span>
      <span className="sr-only">(required)</span>
    </label>
    <input
      id="email"
      type="email"
      aria-required="true"
      aria-invalid={errors.email ? 'true' : 'false'}
      aria-describedby={errors.email ? 'email-error' : undefined}
    />
    {errors.email && (
      <p id="email-error" role="alert" className="error">
        {errors.email}
      </p>
    )}
  </div>
  
  <button type="submit">Submit</button>
</form>
```

## Screen Reader Only Content

```css
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
```

## Testing

```bash
# Automated testing
npm install -D axe-core @axe-core/react

# In tests
import { axe, toHaveNoViolations } from 'jest-axe';
expect.extend(toHaveNoViolations);

test('component is accessible', async () => {
  const { container } = render(<MyComponent />);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
```

## Resources

- **WCAG 2.1 Guidelines**: https://www.w3.org/WAI/WCAG21/quickref/
- **ARIA Authoring Practices**: https://www.w3.org/WAI/ARIA/apg/
