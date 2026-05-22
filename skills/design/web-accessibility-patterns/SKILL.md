---
name: web-accessibility-patterns
version: "1.0"
description: >
  Web accessibility patterns including semantic HTML, ARIA attributes, and keyboard navigation.
  PROACTIVELY activate for: (1) using semantic HTML elements correctly, (2) adding ARIA labels for icons and dynamic content, (3) implementing keyboard navigation.
  Triggers: "accessibility", "a11y", "aria"
group: ui
core-integration:
  techniques:
    primary: ["structured_decomposition"]
    secondary: []
  contracts:
    input: "none"
    output: "none"
  patterns: "none"
  rubrics: "none"
---

# Web Accessibility Patterns

## Semantic HTML Foundation

Use correct elements:

```tsx
// GOOD
<button onClick={handleClick}>Submit</button>
<nav>...</nav>
<main>...</main>
<article>...</article>
<aside>...</aside>
<header>...</header>
<footer>...</footer>

// BAD
<div onClick={handleClick}>Submit</div>
<div className="nav">...</div>
```

## ARIA Attributes

### Icon-Only Buttons

```tsx
<Button variant="ghost" size="icon" aria-label="Close dialog">
  <X size={16} />
</Button>

<Button variant="ghost" size="icon" aria-label="Open menu">
  <Menu size={16} />
</Button>
```

### Form Fields

```tsx
<div>
  <Label htmlFor="email">Email</Label>
  <Input
    id="email"
    type="email"
    aria-describedby="email-description email-error"
    aria-invalid={!!error}
    aria-required="true"
  />
  <p id="email-description" className="text-sm text-muted-foreground">
    We'll never share your email
  </p>
  {error && (
    <p id="email-error" className="text-sm text-destructive" role="alert">
      {error}
    </p>
  )}
</div>
```

### Loading States

```tsx
<div aria-live="polite" aria-busy={isLoading}>
  {isLoading ? <Skeleton /> : <Content />}
</div>

<Button disabled={isLoading} aria-disabled={isLoading}>
  {isLoading ? (
    <>
      <Loader className="animate-spin" aria-hidden="true" />
      <span className="sr-only">Loading</span>
      Submitting...
    </>
  ) : (
    'Submit'
  )}
</Button>
```

### Expandable Content

```tsx
function Accordion({ title, children, isOpen, onToggle }) {
  const contentId = useId();

  return (
    <div>
      <button
        aria-expanded={isOpen}
        aria-controls={contentId}
        onClick={onToggle}
      >
        {title}
      </button>
      <div id={contentId} hidden={!isOpen}>
        {children}
      </div>
    </div>
  );
}
```

## Keyboard Navigation

### Custom Interactive Element

```tsx
<div
  role="button"
  tabIndex={0}
  onClick={handleClick}
  onKeyDown={(e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      handleClick();
    }
  }}
>
  Interactive element
</div>
```

### Keyboard Trap for Modals

```tsx
function Modal({ isOpen, onClose, children }) {
  const modalRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!isOpen) return;

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };

    // Focus trap - keep focus within modal
    const focusableElements = modalRef.current?.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );

    document.addEventListener('keydown', handleKeyDown);
    focusableElements?.[0]?.focus();

    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  return (
    <div ref={modalRef} role="dialog" aria-modal="true">
      {children}
    </div>
  );
}
```

## Focus Management

### Visible Focus Styles

```tsx
<Button className="
  focus-visible:outline-none
  focus-visible:ring-2
  focus-visible:ring-ring
  focus-visible:ring-offset-2
">
  Accessible focus state
</Button>
```

### Skip Link

```tsx
// Add at very top of page
<a
  href="#main-content"
  className="
    sr-only focus:not-sr-only
    focus:absolute focus:top-4 focus:left-4
    focus:z-50 focus:px-4 focus:py-2
    focus:bg-background focus:text-foreground
  "
>
  Skip to main content
</a>

// Main content target
<main id="main-content" tabIndex={-1}>
  ...
</main>
```

## Screen Reader Only Content

```tsx
// Visually hidden but announced
<span className="sr-only">Opens in new tab</span>

// Or with Tailwind
<span className="absolute w-px h-px p-0 -m-px overflow-hidden whitespace-nowrap border-0">
  Screen reader only text
</span>
```

## Color and Contrast

```tsx
// Use semantic colors that have proper contrast
<p className="text-foreground">Primary text - high contrast</p>
<p className="text-muted-foreground">Secondary text - still readable</p>

// Error states
<p className="text-destructive">Error message</p>

// Don't rely on color alone
<span className="text-destructive flex items-center gap-2">
  <AlertCircle size={16} aria-hidden="true" />
  Required field
</span>
```

## Common ARIA Roles

| Role | Use Case |
|------|----------|
| `button` | Clickable non-button elements |
| `dialog` | Modal dialogs |
| `alert` | Important messages |
| `status` | Status updates |
| `navigation` | Navigation sections |
| `tablist`, `tab`, `tabpanel` | Tab interfaces |
| `menu`, `menuitem` | Dropdown menus |

## Anti-Patterns

- `<div onClick>` instead of `<button>`
- Icon without `aria-label`
- Redundant `aria-label` on elements with text
- Missing keyboard support for custom interactive elements
- Removing focus outlines without replacement
- Color as only indicator of state

## Best Practices

- Semantic HTML first
- ARIA for icons and dynamic content
- Keyboard navigation for all interactive elements
- Focus visible styles
- Proper heading hierarchy (h1 -> h2 -> h3)
- Sufficient color contrast (4.5:1 for text)
- Descriptive link text (not "click here")

---

**Related Skills**: `shadcn-component-scaffolding`, `framer-motion-interactive-animation`
