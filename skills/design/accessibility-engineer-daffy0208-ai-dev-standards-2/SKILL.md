---
name: Accessibility Engineer
description: Implement accessibility (a11y) best practices to make applications usable by everyone. Use when building UIs, conducting accessibility audits, or ensuring WCAG compliance. Covers screen readers, keyboard navigation, ARIA attributes, and inclusive design patterns.
version: 1.0.0
---

# Accessibility Engineer

Build for everyone - accessibility is not optional.

## Core Principle

**Accessibility is a civil right, not a feature.**

1 in 4 adults in the US has a disability. Accessible design benefits everyone:

- Blind users (screen readers)
- Low vision users (zoom, high contrast)
- Deaf users (captions)
- Motor disabilities (keyboard-only)
- Cognitive disabilities (clear language)
- Temporary disabilities (broken arm)
- Situational limitations (bright sunlight, noisy environment)

## WCAG Compliance Levels

**Level A:** Minimum (legal requirement)
**Level AA:** Industry standard (aim for this)
**Level AAA:** Gold standard (difficult to achieve for all content)

**Target: WCAG 2.1 AA compliance**

---

## Pillar 1: Semantic HTML

### Use the Right Elements

```jsx
// ❌ Bad: Divs for everything (no semantic meaning)
<div onClick={handleClick}>Click me</div>
<div>Menu</div>

// ✅ Good: Semantic HTML
<button onClick={handleClick}>Click me</button>
<nav>Menu</nav>
```

### Document Structure

```jsx
// ✅ Proper heading hierarchy
<h1>Page Title</h1>
  <h2>Section 1</h2>
    <h3>Subsection 1.1</h3>
  <h2>Section 2</h2>

// ❌ Bad: Skipping levels
<h1>Page Title</h1>
  <h4>Section 1</h4> // Skipped h2, h3
```

### Landmarks

```jsx
<header>
  <nav aria-label="Main navigation">
    {/* Navigation links */}
  </nav>
</header>

<main>
  <article>
    {/* Main content */}
  </article>

  <aside>
    {/* Sidebar */}
  </aside>
</main>

<footer>
  {/* Footer content */}
</footer>
```

---

## Pillar 2: Keyboard Navigation

### All Interactive Elements Must Be Keyboard Accessible

```jsx
// ✅ Button is keyboard accessible by default
<button onClick={handleClick}>Click me</button>

// ❌ Div requires extra work
<div onClick={handleClick}>Click me</div> // Can't tab to it!

// ✅ If you must use div, add keyboard support
<div
  role="button"
  tabIndex={0}
  onClick={handleClick}
  onKeyDown={(e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      handleClick()
    }
  }}
>
  Click me
</div>
```

### Tab Order

```jsx
// ✅ Natural tab order (follows DOM order)
<input />
<button>Submit</button>
<a href="/help">Help</a>

// ❌ Don't use tabIndex > 0 (breaks natural order)
<button tabIndex={5}>Button</button> // Anti-pattern!

// ✅ tabIndex=-1 to remove from tab order
<div tabIndex={-1}>Not keyboard focusable</div>
```

### Focus Management

```jsx
// Modal: Trap focus inside
function Modal({ isOpen, onClose, children }) {
  const modalRef = useRef()

  useEffect(() => {
    if (!isOpen) return

    // Focus first focusable element
    const firstFocusable = modalRef.current.querySelector('button, input, a')
    firstFocusable?.focus()

    // Trap focus
    function handleTab(e) {
      if (e.key !== 'Tab') return

      const focusableElements = modalRef.current.querySelectorAll(
        'button, input, a, [tabindex]:not([tabindex="-1"])'
      )

      const first = focusableElements[0]
      const last = focusableElements[focusableElements.length - 1]

      if (e.shiftKey) {
        if (document.activeElement === first) {
          last.focus()
          e.preventDefault()
        }
      } else {
        if (document.activeElement === last) {
          first.focus()
          e.preventDefault()
        }
      }
    }

    document.addEventListener('keydown', handleTab)
    return () => document.removeEventListener('keydown', handleTab)
  }, [isOpen])

  return isOpen ? (
    <div role="dialog" aria-modal="true" ref={modalRef}>
      {children}
      <button onClick={onClose}>Close</button>
    </div>
  ) : null
}
```

### Skip Links

```jsx
// Allow keyboard users to skip navigation
<a href="#main-content" className="skip-link">
  Skip to main content
</a>

<nav>{/* Navigation */}</nav>

<main id="main-content">
  {/* Main content */}
</main>

// CSS
.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  background: #000;
  color: #fff;
  padding: 8px;
}

.skip-link:focus {
  top: 0;
}
```

---

## Pillar 3: ARIA Attributes

### Only Use ARIA When Semantic HTML Isn't Enough

```jsx
// ✅ Semantic HTML (no ARIA needed)
<button>Click me</button>

// ❌ Unnecessary ARIA
<button role="button" aria-label="Click me">Click me</button>

// ✅ ARIA needed (custom widget)
<div role="tab" aria-selected={isActive} aria-controls="panel-1">
  Tab 1
</div>
```

### Common ARIA Attributes

**aria-label** - Provides accessible name:

```jsx
<button aria-label="Close dialog">
  <XIcon /> {/* Visual only */}
</button>

<input type="search" aria-label="Search products" />
```

**aria-labelledby** - References another element:

```jsx
<h2 id="dialog-title">Delete Account</h2>
<div role="dialog" aria-labelledby="dialog-title">
  {/* Dialog content */}
</div>
```

**aria-describedby** - Additional description:

```jsx
<input
  type="password"
  aria-describedby="password-requirements"
/>
<div id="password-requirements">
  Must be at least 8 characters
</div>
```

**aria-live** - Announce dynamic content:

```jsx
// Polite: Wait for user to finish
<div aria-live="polite">
  {itemsAddedToCart} items added to cart
</div>

// Assertive: Interrupt immediately (use sparingly)
<div aria-live="assertive" role="alert">
  Error: Payment failed
</div>
```

**aria-expanded** - Collapsible content:

```jsx
<button
  aria-expanded={isOpen}
  aria-controls="dropdown-menu"
  onClick={() => setIsOpen(!isOpen)}
>
  Menu
</button>

<div id="dropdown-menu" hidden={!isOpen}>
  {/* Menu items */}
</div>
```

**aria-hidden** - Hide from screen readers:

```jsx
// Decorative icons
<span aria-hidden="true">★</span>

// Don't hide interactive elements!
// ❌ Bad
<button aria-hidden="true">Click me</button>
```

---

## Pillar 4: Forms & Inputs

### Labels

```jsx
// ✅ Good: Explicit label
<label htmlFor="email">Email</label>
<input id="email" type="email" />

// ✅ Good: Implicit label
<label>
  Email
  <input type="email" />
</label>

// ❌ Bad: No label (placeholder is not a label!)
<input type="email" placeholder="Email" />
```

### Error Messages

```jsx
function EmailInput({ error }) {
  const errorId = 'email-error'

  return (
    <>
      <label htmlFor="email">Email</label>
      <input
        id="email"
        type="email"
        aria-invalid={!!error}
        aria-describedby={error ? errorId : undefined}
      />
      {error && (
        <div id={errorId} role="alert">
          {error}
        </div>
      )}
    </>
  )
}
```

### Required Fields

```jsx
<label htmlFor="name">
  Name <span aria-label="required">*</span>
</label>
<input id="name" type="text" required aria-required="true" />
```

---

## Pillar 5: Color & Contrast

### Minimum Contrast Ratios (WCAG AA)

- Normal text (< 18pt): 4.5:1
- Large text (≥ 18pt or 14pt bold): 3:1
- UI components: 3:1

```jsx
// ❌ Bad: Insufficient contrast
<button style={{ background: '#ddd', color: '#aaa' }}>
  Submit // 1.5:1 contrast - fails!
</button>

// ✅ Good: Sufficient contrast
<button style={{ background: '#0066cc', color: '#ffffff' }}>
  Submit // 8:1 contrast - passes!
</button>
```

### Don't Use Color Alone

```jsx
// ❌ Bad: Color only
<span style={{ color: 'red' }}>Error</span>
<span style={{ color: 'green' }}>Success</span>

// ✅ Good: Color + icon/text
<span style={{ color: 'red' }}>
  <ErrorIcon aria-hidden="true" />
  Error
</span>
```

---

## Pillar 6: Images & Media

### Alt Text

```jsx
// ✅ Informative images
<img src="chart.png" alt="Sales increased 50% in Q4" />

// ✅ Decorative images
<img src="decorative-border.png" alt="" /> // Empty alt

// ❌ Bad: No alt or redundant alt
<img src="photo.jpg" /> // Missing alt
<img src="photo.jpg" alt="Photo" /> // Useless
```

### Complex Images

```jsx
<figure>
  <img src="complex-chart.png" alt="Sales data for 2024" />
  <figcaption>
    <details>
      <summary>Detailed description</summary>
      <p>Q1: $100k, Q2: $150k, Q3: $180k, Q4: $220k. Shows 50% growth year-over-year.</p>
    </details>
  </figcaption>
</figure>
```

### Video Captions

```jsx
<video controls>
  <source src="video.mp4" type="video/mp4" />
  <track kind="captions" src="captions.vtt" srclang="en" label="English" default />
</video>
```

---

## Pillar 7: Testing

### Automated Testing

```bash
# Lighthouse accessibility audit
lighthouse https://example.com --only-categories=accessibility

# axe-core (Jest)
npm install --save-dev @axe-core/react jest-axe
```

```typescript
// Test with jest-axe
import { axe, toHaveNoViolations } from 'jest-axe'

expect.extend(toHaveNoViolations)

it('has no accessibility violations', async () => {
  const { container } = render(<Button>Click me</Button>)
  const results = await axe(container)

  expect(results).toHaveNoViolations()
})
```

### Manual Testing

**Keyboard Navigation:**

- Tab through entire page
- Enter/Space to activate buttons
- Arrow keys for radio groups
- Esc to close modals

**Screen Reader Testing:**

- **NVDA** (Windows, free)
- **JAWS** (Windows, paid)
- **VoiceOver** (Mac, built-in)

**Screen Reader Shortcuts:**

- Navigate by headings: H (next), Shift+H (previous)
- Navigate by landmarks: D (next), Shift+D (previous)
- List all links: Insert+F7 (NVDA)

---

## Common Patterns

### Accessible Button

```jsx
<button
  type="button"
  onClick={handleClick}
  disabled={isDisabled}
  aria-busy={isLoading}
  aria-label={ariaLabel}
>
  {children}
</button>
```

### Accessible Modal

```jsx
<div
  role="dialog"
  aria-modal="true"
  aria-labelledby="dialog-title"
  aria-describedby="dialog-description"
>
  <h2 id="dialog-title">Dialog Title</h2>
  <p id="dialog-description">Dialog description</p>

  <button onClick={onClose}>Close</button>
</div>
```

### Accessible Tabs

```jsx
<div>
  <div role="tablist">
    <button
      role="tab"
      aria-selected={activeTab === 'tab1'}
      aria-controls="panel1"
      onClick={() => setActiveTab('tab1')}
    >
      Tab 1
    </button>
    <button
      role="tab"
      aria-selected={activeTab === 'tab2'}
      aria-controls="panel2"
      onClick={() => setActiveTab('tab2')}
    >
      Tab 2
    </button>
  </div>

  <div id="panel1" role="tabpanel" hidden={activeTab !== 'tab1'}>
    Panel 1 content
  </div>

  <div id="panel2" role="tabpanel" hidden={activeTab !== 'tab2'}>
    Panel 2 content
  </div>
</div>
```

---

## Accessibility Checklist

### Semantic HTML

- [ ] Proper heading hierarchy (h1 → h2 → h3)
- [ ] Semantic landmarks (header, nav, main, footer)
- [ ] Lists use ul/ol/li
- [ ] Buttons for actions, links for navigation

### Keyboard

- [ ] All interactive elements keyboard accessible
- [ ] Visible focus indicators
- [ ] Logical tab order
- [ ] Skip links provided
- [ ] No keyboard traps

### ARIA

- [ ] Semantic HTML used first (ARIA only when needed)
- [ ] All interactive widgets have roles
- [ ] Dynamic content has aria-live
- [ ] Forms have proper labels and descriptions

### Color & Contrast

- [ ] Text contrast ≥ 4.5:1 (normal), ≥ 3:1 (large)
- [ ] Don't use color alone to convey info
- [ ] Focus indicators visible

### Images & Media

- [ ] All images have alt text
- [ ] Decorative images have empty alt
- [ ] Videos have captions
- [ ] Audio has transcripts

### Forms

- [ ] All inputs have labels
- [ ] Error messages associated with inputs
- [ ] Required fields indicated

### Testing

- [ ] Keyboard navigation tested
- [ ] Screen reader tested
- [ ] Automated tools run (axe, Lighthouse)
- [ ] Color blindness simulation tested

---

## Tools

- **axe DevTools** - Browser extension
- **Lighthouse** - Built into Chrome DevTools
- **WAVE** - Web accessibility evaluation tool
- **Color Contrast Analyzer** - Desktop app
- **NVDA** - Free screen reader (Windows)
- **VoiceOver** - Built-in screen reader (Mac)

---

## Related Resources

**Skills:**

- `ux-designer` - Accessible design patterns
- `frontend-builder` - Accessible React components
- `testing-strategist` - Accessibility testing

**External:**

- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [MDN Accessibility](https://developer.mozilla.org/en-US/docs/Web/Accessibility)
- [A11y Project](https://www.a11yproject.com/)
- [WebAIM](https://webaim.org/)

---

**Build for everyone.** ♿
