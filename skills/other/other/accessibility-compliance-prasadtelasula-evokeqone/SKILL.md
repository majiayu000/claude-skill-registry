---
name: accessibility-compliance
description: Implement WCAG 2.1 AA accessibility compliance with ARIA labels, keyboard navigation, screen reader support, and color contrast. Use when ensuring accessibility or fixing a11y issues.
allowed-tools: Read, Write, Edit, Bash, Glob
---

You implement WCAG 2.1 AA accessibility compliance for the QA Team Portal.

## Requirements from PROJECT_PLAN.md

- **Standard:** WCAG 2.1 AA compliance
- Keyboard navigation support
- Screen reader compatibility
- Color contrast standards (4.5:1 for text)
- ARIA labels on interactive elements
- Focus indicators visible
- Accessible forms and error messages

## WCAG 2.1 AA Requirements

### Perceivable
1. Text alternatives for non-text content
2. Captions for audio/video
3. Content can be presented in different ways
4. Color contrast minimum 4.5:1 (text), 3:1 (large text, UI components)

### Operable
1. Keyboard accessible (all functionality)
2. Enough time to read/use content
3. No content that causes seizures (flashing < 3 times per second)
4. Navigation and finding content

### Understandable
1. Readable and understandable text
2. Predictable operation
3. Input assistance (labels, error messages)

### Robust
1. Compatible with assistive technologies
2. Valid HTML
3. Name, role, value for UI components

## Implementation

### 1. Semantic HTML

**Use proper HTML5 elements:**

```typescript
// ❌ Wrong: Divs for everything
<div className="button" onClick={handleClick}>Click me</div>
<div className="nav">
  <div>Home</div>
  <div>About</div>
</div>

// ✅ Correct: Semantic elements
<button onClick={handleClick}>Click me</button>
<nav>
  <a href="/">Home</a>
  <a href="/about">About</a>
</nav>

// ✅ Proper document structure
<header>
  <nav>...</nav>
</header>
<main>
  <article>
    <h1>Page Title</h1>
    <section>
      <h2>Section Title</h2>
      <p>Content</p>
    </section>
  </article>
</main>
<footer>...</footer>
```

### 2. ARIA Labels and Roles

**Location:** `frontend/src/components/Navigation.tsx`

```typescript
export const Navigation = () => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  return (
    <header role="banner">
      <nav role="navigation" aria-label="Main navigation">
        <div className="container">
          <a href="/" aria-label="QA Team Portal Home">
            <img src="/logo.svg" alt="Evoke Logo" />
            <span>QA Team Portal</span>
          </a>

          {/* Desktop Menu */}
          <ul role="menubar" className="hidden md:flex">
            <li role="none">
              <a href="#team" role="menuitem">Team</a>
            </li>
            <li role="none">
              <a href="#updates" role="menuitem">Updates</a>
            </li>
            <li role="none">
              <a href="#tools" role="menuitem">Tools</a>
            </li>
          </ul>

          {/* Mobile Menu Toggle */}
          <button
            className="md:hidden"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            aria-label={mobileMenuOpen ? "Close menu" : "Open menu"}
            aria-expanded={mobileMenuOpen}
            aria-controls="mobile-menu"
          >
            {mobileMenuOpen ? <X /> : <Menu />}
          </button>
        </div>

        {/* Mobile Menu */}
        {mobileMenuOpen && (
          <div
            id="mobile-menu"
            role="menu"
            aria-label="Mobile navigation"
          >
            <a href="#team" role="menuitem">Team</a>
            <a href="#updates" role="menuitem">Updates</a>
            <a href="#tools" role="menuitem">Tools</a>
          </div>
        )}
      </nav>
    </header>
  )
}
```

### 3. Keyboard Navigation

**Focus Management:**

```typescript
// frontend/src/components/Modal.tsx
import { useEffect, useRef } from 'react'

export const Modal = ({ isOpen, onClose, children }) => {
  const modalRef = useRef<HTMLDivElement>(null)
  const previousFocusRef = useRef<HTMLElement | null>(null)

  useEffect(() => {
    if (isOpen) {
      // Store previous focus
      previousFocusRef.current = document.activeElement as HTMLElement

      // Focus first focusable element in modal
      const focusableElements = modalRef.current?.querySelectorAll(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
      )
      if (focusableElements && focusableElements.length > 0) {
        (focusableElements[0] as HTMLElement).focus()
      }

      // Trap focus inside modal
      const handleTab = (e: KeyboardEvent) => {
        if (e.key !== 'Tab') return

        const focusableContent = modalRef.current?.querySelectorAll(
          'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        )

        if (!focusableContent || focusableContent.length === 0) return

        const firstElement = focusableContent[0] as HTMLElement
        const lastElement = focusableContent[focusableContent.length - 1] as HTMLElement

        if (e.shiftKey) {
          if (document.activeElement === firstElement) {
            lastElement.focus()
            e.preventDefault()
          }
        } else {
          if (document.activeElement === lastElement) {
            firstElement.focus()
            e.preventDefault()
          }
        }
      }

      document.addEventListener('keydown', handleTab)

      return () => {
        document.removeEventListener('keydown', handleTab)
        // Restore previous focus
        previousFocusRef.current?.focus()
      }
    }
  }, [isOpen])

  // Close on Escape key
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isOpen) {
        onClose()
      }
    }

    document.addEventListener('keydown', handleEscape)
    return () => document.removeEventListener('keydown', handleEscape)
  }, [isOpen, onClose])

  if (!isOpen) return null

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
      ref={modalRef}
      className="fixed inset-0 z-50"
    >
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-black/50"
        onClick={onClose}
        aria-hidden="true"
      />

      {/* Modal Content */}
      <div className="fixed inset-0 flex items-center justify-center p-4">
        <div className="bg-white rounded-lg max-w-md w-full p-6">
          <h2 id="modal-title" className="text-2xl font-bold mb-4">
            Modal Title
          </h2>
          {children}
          <button onClick={onClose} className="mt-4">
            Close
          </button>
        </div>
      </div>
    </div>
  )
}
```

**Skip to Main Content:**

```typescript
// frontend/src/components/SkipToContent.tsx
export const SkipToContent = () => {
  return (
    <a
      href="#main-content"
      className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-50 focus:px-4 focus:py-2 focus:bg-primary focus:text-white focus:rounded"
    >
      Skip to main content
    </a>
  )
}

// Usage in App.tsx
<SkipToContent />
<Header />
<main id="main-content">
  {/* Page content */}
</main>
```

### 4. Form Accessibility

**Accessible Form:**

```typescript
// frontend/src/components/forms/AccessibleForm.tsx
export const LoginForm = () => {
  const [errors, setErrors] = useState<Record<string, string>>({})

  return (
    <form onSubmit={handleSubmit} noValidate>
      <div className="space-y-4">
        {/* Email Field */}
        <div>
          <label
            htmlFor="email"
            className="block text-sm font-medium mb-2"
          >
            Email <span aria-label="required" className="text-error">*</span>
          </label>
          <input
            id="email"
            name="email"
            type="email"
            required
            aria-required="true"
            aria-invalid={!!errors.email}
            aria-describedby={errors.email ? "email-error" : undefined}
            className={cn(
              "w-full px-3 py-2 border rounded-lg",
              errors.email ? "border-error" : "border-input"
            )}
          />
          {errors.email && (
            <p
              id="email-error"
              role="alert"
              className="text-sm text-error mt-1"
            >
              {errors.email}
            </p>
          )}
        </div>

        {/* Password Field */}
        <div>
          <label
            htmlFor="password"
            className="block text-sm font-medium mb-2"
          >
            Password <span aria-label="required" className="text-error">*</span>
          </label>
          <input
            id="password"
            name="password"
            type="password"
            required
            aria-required="true"
            aria-invalid={!!errors.password}
            aria-describedby={errors.password ? "password-error password-requirements" : "password-requirements"}
            className={cn(
              "w-full px-3 py-2 border rounded-lg",
              errors.password ? "border-error" : "border-input"
            )}
          />
          <p id="password-requirements" className="text-xs text-muted-foreground mt-1">
            Password must be at least 12 characters
          </p>
          {errors.password && (
            <p
              id="password-error"
              role="alert"
              className="text-sm text-error mt-1"
            >
              {errors.password}
            </p>
          )}
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          className="w-full bg-primary text-white py-2 px-4 rounded-lg hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2"
        >
          Sign In
        </button>
      </div>

      {/* Form-level error */}
      {errors.form && (
        <div
          role="alert"
          aria-live="assertive"
          className="mt-4 p-3 bg-error-light text-error rounded-lg"
        >
          {errors.form}
        </div>
      )}
    </form>
  )
}
```

### 5. Focus Indicators

**Custom Focus Styles:**

```css
/* frontend/src/index.css */

/* Remove default outline and add custom focus ring */
*:focus {
  outline: none;
}

*:focus-visible {
  outline: 2px solid hsl(var(--ring));
  outline-offset: 2px;
}

/* Button focus styles */
button:focus-visible,
a:focus-visible {
  outline: 2px solid hsl(var(--ring));
  outline-offset: 2px;
}

/* Input focus styles */
input:focus-visible,
textarea:focus-visible,
select:focus-visible {
  outline: 2px solid hsl(var(--ring));
  outline-offset: 2px;
  border-color: hsl(var(--ring));
}

/* Skip to content link */
.skip-to-content:focus {
  position: absolute;
  top: 1rem;
  left: 1rem;
  z-index: 9999;
  padding: 0.75rem 1rem;
  background: hsl(var(--primary));
  color: hsl(var(--primary-foreground));
  border-radius: 0.375rem;
}
```

### 6. Color Contrast

**Check and Fix Contrast:**

```typescript
// Use colors that meet WCAG AA standards

// ❌ Bad: Low contrast (2.5:1)
<p className="text-gray-400 bg-gray-200">Low contrast text</p>

// ✅ Good: High contrast (4.5:1+)
<p className="text-gray-900 bg-gray-100">High contrast text</p>

// ✅ Good: Using theme colors with proper contrast
<p className="text-foreground bg-background">Theme colors</p>
<button className="bg-primary text-primary-foreground">Button</button>

// For links, ensure visible distinction
<a href="#" className="text-primary underline hover:text-primary/90">
  Link text
</a>
```

**Contrast Checker Function:**

```typescript
// frontend/src/utils/colorContrast.ts
export const getContrastRatio = (color1: string, color2: string): number => {
  const getLuminance = (color: string) => {
    // Convert hex to RGB
    const rgb = parseInt(color.slice(1), 16)
    const r = (rgb >> 16) & 0xff
    const g = (rgb >> 8) & 0xff
    const b = (rgb >> 0) & 0xff

    // Calculate relative luminance
    const [rs, gs, bs] = [r, g, b].map(c => {
      c = c / 255
      return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4)
    })

    return 0.2126 * rs + 0.7152 * gs + 0.0722 * bs
  }

  const lum1 = getLuminance(color1)
  const lum2 = getLuminance(color2)

  const lighter = Math.max(lum1, lum2)
  const darker = Math.min(lum1, lum2)

  return (lighter + 0.05) / (darker + 0.05)
}

export const meetsWCAGAA = (color1: string, color2: string, isLargeText: boolean = false): boolean => {
  const contrast = getContrastRatio(color1, color2)
  return isLargeText ? contrast >= 3 : contrast >= 4.5
}

// Usage
console.log(meetsWCAGAA('#0066CC', '#FFFFFF')) // true (7.4:1)
console.log(meetsWCAGAA('#808080', '#FFFFFF')) // false (3.9:1)
```

### 7. Images and Alt Text

```typescript
// ❌ Bad: Missing alt text
<img src="/team/john.jpg" />

// ✅ Good: Descriptive alt text
<img src="/team/john.jpg" alt="John Doe, Senior QA Engineer" />

// ✅ Decorative images
<img src="/decoration.svg" alt="" aria-hidden="true" />

// ✅ Complex images with longer descriptions
<figure>
  <img
    src="/chart.png"
    alt="Bar chart showing test coverage by module"
    aria-describedby="chart-desc"
  />
  <figcaption id="chart-desc">
    The chart shows test coverage percentages for each module:
    Authentication (95%), User Management (88%), Reports (76%),
    Settings (92%).
  </figcaption>
</figure>
```

### 8. Live Regions for Dynamic Content

```typescript
// frontend/src/components/StatusMessage.tsx
export const StatusMessage = ({ message, type }: { message: string; type: 'success' | 'error' | 'info' }) => {
  return (
    <div
      role="status"
      aria-live={type === 'error' ? 'assertive' : 'polite'}
      aria-atomic="true"
      className={cn(
        "p-4 rounded-lg",
        {
          'bg-success-light text-success': type === 'success',
          'bg-error-light text-error': type === 'error',
          'bg-blue-50 text-blue-900': type === 'info',
        }
      )}
    >
      {message}
    </div>
  )
}

// Usage
<StatusMessage
  message="Team member created successfully"
  type="success"
/>
```

### 9. Accessible Data Tables

```typescript
// frontend/src/components/admin/AccessibleTable.tsx
export const TeamMembersTable = ({ members }: { members: TeamMember[] }) => {
  return (
    <table role="table" aria-label="Team members list">
      <caption className="sr-only">
        List of {members.length} team members
      </caption>
      <thead>
        <tr>
          <th scope="col">Photo</th>
          <th scope="col">Name</th>
          <th scope="col">Role</th>
          <th scope="col">Email</th>
          <th scope="col">Actions</th>
        </tr>
      </thead>
      <tbody>
        {members.map((member, index) => (
          <tr key={member.id}>
            <td>
              <img
                src={member.photo_url}
                alt={`${member.name}'s profile photo`}
                className="w-12 h-12 rounded-full"
              />
            </td>
            <th scope="row">{member.name}</th>
            <td>{member.role}</td>
            <td>{member.email}</td>
            <td>
              <button
                aria-label={`Edit ${member.name}`}
                className="mr-2"
              >
                Edit
              </button>
              <button
                aria-label={`Delete ${member.name}`}
              >
                Delete
              </button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}
```

### 10. Screen Reader Only Text

```css
/* frontend/src/index.css */

/* Screen reader only class */
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

/* Show on focus (for skip links) */
.sr-only:focus {
  position: static;
  width: auto;
  height: auto;
  padding: initial;
  margin: initial;
  overflow: visible;
  clip: auto;
  white-space: normal;
}
```

```typescript
// Usage
<span className="sr-only">Current page</span>
<button aria-label="Close menu">
  <X aria-hidden="true" />
  <span className="sr-only">Close</span>
</button>
```

## Accessibility Testing

### 1. Automated Testing with axe-core

```bash
cd frontend
npm install -D @axe-core/playwright
```

```python
# tests/e2e/test_accessibility.py
from axe_playwright_python import Axe

def test_homepage_accessibility(page):
    """Test homepage accessibility."""
    page.goto('http://localhost:5173')

    # Run axe accessibility scan
    axe = Axe()
    results = axe.run(page)

    violations = results['violations']

    if violations:
        print(f"\nFound {len(violations)} accessibility violations:\n")
        for violation in violations:
            print(f"❌ {violation['id']}: {violation['description']}")
            print(f"   Impact: {violation['impact']}")
            print(f"   Help: {violation['helpUrl']}")
            print(f"   Affected nodes: {len(violation['nodes'])}\n")

    # Assert no violations
    assert len(violations) == 0, f"Found {len(violations)} accessibility violations"

def test_admin_login_accessibility(page):
    """Test login form accessibility."""
    page.goto('http://localhost:5173/admin/login')

    axe = Axe()
    results = axe.run(page)

    assert len(results['violations']) == 0
```

### 2. Keyboard Navigation Testing

```python
# tests/e2e/test_keyboard_navigation.py
def test_keyboard_navigation(page):
    """Test keyboard navigation through the page."""
    page.goto('http://localhost:5173')

    # Start from top
    page.keyboard.press('Tab')

    # Should focus skip link first
    expect(page.locator('.skip-to-content')).to_be_focused()

    # Tab through navigation
    page.keyboard.press('Tab')
    expect(page.locator('nav a:nth-child(1)')).to_be_focused()

    # Test Enter key activation
    page.keyboard.press('Enter')
    # Should navigate

def test_modal_focus_trap(page):
    """Test focus is trapped inside modal."""
    page.goto('http://localhost:5173/admin/team-members')

    # Open modal
    page.click('button:has-text("Add Team Member")')

    # Tab through all focusable elements
    # Last Tab should cycle back to first element
    for _ in range(10):
        page.keyboard.press('Tab')

    # Focus should still be inside modal
    assert page.locator('[role="dialog"]').evaluate('el => el.contains(document.activeElement)')

    # Escape should close modal
    page.keyboard.press('Escape')
    expect(page.locator('[role="dialog"]')).not_to_be_visible()
```

### 3. Screen Reader Testing

**Test with actual screen readers:**
- **macOS:** VoiceOver (Cmd+F5)
- **Windows:** NVDA (free), JAWS (paid)
- **Linux:** Orca

**Test checklist:**
- [ ] All images have appropriate alt text
- [ ] All form inputs have labels
- [ ] Error messages are announced
- [ ] Dynamic content changes are announced (aria-live)
- [ ] Headings structure is logical
- [ ] Landmarks are properly identified (header, nav, main, footer)
- [ ] Lists are properly marked up

### 4. Color Contrast Testing

```bash
# Install contrast checker
npm install -D axe-core

# Run contrast check
npx axe http://localhost:5173 --rules=color-contrast
```

## WCAG 2.1 AA Checklist

### Perceivable
- [ ] All images have alt text
- [ ] Videos have captions (if applicable)
- [ ] Color is not the only means of conveying information
- [ ] Text contrast >= 4.5:1 (normal), >= 3:1 (large text 18pt+)
- [ ] Text can be resized to 200% without loss of content
- [ ] Images of text avoided (use real text)

### Operable
- [ ] All functionality available via keyboard
- [ ] No keyboard trap
- [ ] Skip to main content link present
- [ ] Page titles are descriptive
- [ ] Link purpose clear from link text or context
- [ ] Multiple ways to find pages (navigation, search, sitemap)
- [ ] Headings and labels are descriptive
- [ ] Focus indicator visible
- [ ] No time limits (or user can extend)
- [ ] No content flashing more than 3 times per second

### Understandable
- [ ] Language of page declared (html lang="en")
- [ ] Language of parts declared if different
- [ ] Navigation is consistent across pages
- [ ] Labels or instructions provided for user input
- [ ] Error messages are clear and helpful
- [ ] Error prevention for important actions (confirmation)
- [ ] Form fields have visible labels
- [ ] Required fields are indicated

### Robust
- [ ] HTML validates (use W3C validator)
- [ ] Name, role, value available for all UI components
- [ ] Status messages programmatically determinable (aria-live)
- [ ] Works with assistive technologies

## Accessibility Resources

**Tools:**
- **axe DevTools:** Browser extension for accessibility testing
- **Lighthouse:** Built into Chrome DevTools
- **WAVE:** Web accessibility evaluation tool
- **Color Contrast Analyzer:** Check color combinations
- **Screen readers:** NVDA (Windows), VoiceOver (macOS), JAWS (Windows)

**Documentation:**
- WCAG 2.1: https://www.w3.org/WAI/WCAG21/quickref/
- ARIA Authoring Practices: https://www.w3.org/WAI/ARIA/apg/
- MDN Accessibility: https://developer.mozilla.org/en-US/docs/Web/Accessibility

## Report

✅ WCAG 2.1 AA compliance achieved
✅ All images have descriptive alt text
✅ Semantic HTML used throughout
✅ ARIA labels added to interactive elements
✅ Keyboard navigation fully functional
✅ Focus indicators visible and clear
✅ Color contrast meets 4.5:1 minimum
✅ Forms fully accessible with proper labels
✅ Screen reader tested (VoiceOver/NVDA)
✅ Skip to content link implemented
✅ No accessibility violations found (axe-core)
✅ Automated tests passing
