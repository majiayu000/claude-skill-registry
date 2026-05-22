---
name: accessibility-auditing
description: Audit web pages and components for accessibility issues following WCAG 2.1 guidelines. Use when checking for accessibility compliance, fixing a11y issues, ensuring screen reader compatibility, or improving keyboard navigation. Triggers on requests like "audit accessibility", "check a11y", "fix accessibility issues", "screen reader support", "keyboard navigation", or "WCAG compliance".
---

# Accessibility Auditing

Audit and improve accessibility for WCAG 2.1 AA compliance.

## Process

1. **Identify scope** - Which pages/components to audit?
2. **Automated checks** - Run linting and browser tools
3. **Manual testing** - Keyboard navigation, screen reader
4. **Document issues** - Severity, location, fix
5. **Implement fixes** - Priority order

## WCAG 2.1 Checklist

### Perceivable

**Images**
```tsx
// Required: alt text for informational images
<img src={article.image} alt={article.imageAlt || article.title} />

// Decorative images: empty alt
<img src="/decorative-border.png" alt="" role="presentation" />
```

**Color Contrast**
- Normal text: 4.5:1 minimum
- Large text (18px+): 3:1 minimum
- Use theme CSS variables which meet contrast requirements

**Video/Audio**
```tsx
// Captions for video content
<video>
  <track kind="captions" src="/captions.vtt" srclang="en" label="English" />
</video>
```

### Operable

**Keyboard Navigation**
```tsx
// All interactive elements focusable
<button onClick={handleClick}>Click me</button>  // Good: button is focusable

// Custom elements need tabindex
<div role="button" tabIndex={0} onClick={handleClick} onKeyDown={handleKeyDown}>
  Click me
</div>

// Skip links for main content
<a href="#main-content" className="sr-only focus:not-sr-only">
  Skip to main content
</a>
```

**Focus Indicators**
```tsx
// Visible focus states
className="focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2"
```

**Focus Trapping (Modals)**
```tsx
// Trap focus within modal
useEffect(() => {
  const focusableElements = modal.querySelectorAll(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  );
  const first = focusableElements[0];
  const last = focusableElements[focusableElements.length - 1];

  function handleTab(e: KeyboardEvent) {
    if (e.key === 'Tab') {
      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault();
        last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault();
        first.focus();
      }
    }
  }
  // ...
}, []);
```

### Understandable

**Form Labels**
```tsx
// Always associate labels with inputs
<label htmlFor="email">Email</label>
<input id="email" type="email" name="email" />

// Or use aria-label for icon-only buttons
<button aria-label="Close modal">
  <XIcon />
</button>
```

**Error Messages**
```tsx
// Associate errors with inputs
<input
  id="email"
  aria-invalid={!!error}
  aria-describedby={error ? "email-error" : undefined}
/>
{error && (
  <p id="email-error" role="alert" className="text-red-500">
    {error}
  </p>
)}
```

**Language**
```tsx
// Declare page language
<html lang="en">
```

### Robust

**Semantic HTML**
```tsx
// Use appropriate elements
<nav>...</nav>           // Navigation
<main>...</main>         // Main content
<article>...</article>   // Article content
<aside>...</aside>       // Sidebar
<header>...</header>     // Header
<footer>...</footer>     // Footer

// Use headings in order
<h1>Page Title</h1>
<h2>Section</h2>
<h3>Subsection</h3>
```

**ARIA Roles and States**
```tsx
// Live regions for dynamic content
<div aria-live="polite" aria-atomic="true">
  {statusMessage}
</div>

// Loading states
<button aria-busy={loading} disabled={loading}>
  {loading ? 'Saving...' : 'Save'}
</button>

// Expanded/collapsed
<button aria-expanded={isOpen} aria-controls="menu">
  Menu
</button>
<div id="menu" hidden={!isOpen}>...</div>
```

## Common Issues in This Project

### Admin Tables
- Ensure sortable columns are keyboard accessible
- Add scope attributes to table headers
- Announce sort changes with aria-live

### Media Library
- All images need alt text (use title field)
- Video players need keyboard controls
- Upload progress announced to screen readers

### Forms
- All fields need visible labels
- Required fields marked with aria-required
- Error states linked with aria-describedby

### Navigation
- Mobile menu needs aria-expanded
- Current page indicated with aria-current="page"
- Dropdown menus keyboard navigable

## Testing Tools

```bash
# ESLint a11y plugin (add to eslint.config.mjs)
npm install eslint-plugin-jsx-a11y --save-dev

# Playwright a11y testing
npm install @axe-core/playwright --save-dev
```

## Output

Provide accessibility audit results:
1. Issue list with severity (Critical/Serious/Moderate/Minor)
2. WCAG criterion violated
3. Location (file:line or selector)
4. Recommended fix with code example
