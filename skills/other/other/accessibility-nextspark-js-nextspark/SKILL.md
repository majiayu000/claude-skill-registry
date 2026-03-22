---
name: accessibility
description: |
  Accessibility (a11y) patterns for this Next.js application.
  Covers WCAG 2.1 AA compliance, ARIA attributes, keyboard navigation, focus management, and screen reader support.
  Use this skill when implementing accessible UI components or validating accessibility requirements.
allowed-tools: Read, Glob, Grep
version: 1.0.0
---

# Accessibility Skill

Patterns for implementing WCAG 2.1 Level AA compliant components with proper ARIA attributes, keyboard navigation, and screen reader support.

## Architecture Overview

```
ACCESSIBILITY LAYERS:

Semantic HTML Foundation:
├── <button> for buttons (not <div>)
├── <nav> for navigation regions
├── <form> and <fieldset> for forms
├── <a> for links
└── Heading hierarchy (h1-h6)

ARIA Enhancement:
├── Landmark roles (navigation, main, complementary)
├── State attributes (aria-expanded, aria-current)
├── Relationship attributes (aria-labelledby, aria-describedby)
└── Live regions (aria-live, role="alert")

Visual Accessibility:
├── Color contrast (4.5:1 minimum)
├── Focus indicators (focus-visible:ring-2)
├── Motion reduction (prefers-reduced-motion)
└── Text scaling support

Keyboard Accessibility:
├── Tab order management
├── Focus trapping in modals
├── Escape key handling
└── Arrow key navigation (where appropriate)
```

## When to Use This Skill

- Implementing interactive UI components
- Adding ARIA attributes to custom elements
- Validating accessibility requirements
- Ensuring keyboard navigation works
- Testing with screen readers

## WCAG Compliance Standards

### Level AA Requirements (Minimum)

| Criterion | Requirement | Implementation |
|-----------|-------------|----------------|
| **1.4.3** Color Contrast | 4.5:1 for normal text, 3:1 for large text | Use semantic color tokens |
| **1.4.11** Non-text Contrast | 3:1 for UI components | Focus rings, borders |
| **2.1.1** Keyboard | All functionality via keyboard | Tab navigation, Enter/Space |
| **2.4.3** Focus Order | Logical focus sequence | DOM order, tabIndex |
| **2.4.7** Focus Visible | Visible focus indicator | `focus-visible:ring-2` |
| **4.1.2** Name, Role, Value | Accessible names for elements | Labels, aria-label |

### POUR Principles

- **Perceivable**: Content visible to all users (contrast, alt text)
- **Operable**: Interface usable via keyboard and assistive tech
- **Understandable**: Clear, predictable interface
- **Robust**: Compatible with current and future assistive tech

## ARIA Attribute Patterns

### Landmark Roles

```typescript
// Navigation with accessible label
<nav role="navigation" aria-label="pagination">
  <ul>
    <li><a href="/page/1">1</a></li>
    <li><a href="/page/2" aria-current="page">2</a></li>
  </ul>
</nav>

// Breadcrumb navigation
<nav aria-label="breadcrumb">
  <ol>
    <li><a href="/">Home</a></li>
    <li aria-current="page">Products</li>
  </ol>
</nav>

// Main content area
<main role="main" id="main-content">
  {/* Page content */}
</main>
```

### Dynamic State Attributes

```typescript
// Accordion/Collapsible
<button
  aria-expanded={isOpen}
  aria-controls={`content-${id}`}
  onClick={() => setIsOpen(!isOpen)}
>
  Section Title
</button>
<div
  id={`content-${id}`}
  aria-hidden={!isOpen}
  hidden={!isOpen}
>
  {/* Collapsible content */}
</div>

// Tabs
<div role="tablist" aria-label="Settings tabs">
  <button
    role="tab"
    aria-selected={activeTab === 'general'}
    aria-controls="panel-general"
    tabIndex={activeTab === 'general' ? 0 : -1}
  >
    General
  </button>
</div>
<div
  role="tabpanel"
  id="panel-general"
  aria-labelledby="tab-general"
  hidden={activeTab !== 'general'}
>
  {/* Tab content */}
</div>

// Menu/Dropdown
<button
  aria-haspopup="menu"
  aria-expanded={isOpen}
  aria-controls="menu-items"
>
  Options
</button>
<div
  id="menu-items"
  role="menu"
  aria-hidden={!isOpen}
>
  <button role="menuitem">Edit</button>
  <button role="menuitem">Delete</button>
</div>
```

### Form Accessibility

```typescript
// core/components/ui/form.tsx pattern
<FormItem>
  <FormLabel htmlFor={formItemId}>
    Email
  </FormLabel>
  <FormControl>
    <Input
      id={formItemId}
      aria-describedby={
        !error
          ? formDescriptionId
          : `${formDescriptionId} ${formMessageId}`
      }
      aria-invalid={!!error}
      aria-required={required}
    />
  </FormControl>
  <FormDescription id={formDescriptionId}>
    We'll never share your email.
  </FormDescription>
  {error && (
    <FormMessage id={formMessageId} role="alert">
      {error.message}
    </FormMessage>
  )}
</FormItem>
```

### Live Regions

```typescript
// Status announcements (polite)
<div aria-live="polite" aria-atomic="true" className="sr-only">
  {statusMessage}
</div>

// Error alerts (assertive)
<div role="alert" className="text-destructive">
  {errorMessage}
</div>

// Toast notifications
<div
  role="status"
  aria-live="polite"
  aria-atomic="true"
>
  {notification}
</div>
```

## Keyboard Navigation Patterns

### Focus Indicators

All interactive elements use the standardized focus ring:

```typescript
// Button focus pattern
<button
  className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-background"
>
  Click me
</button>

// Input focus pattern
<input
  className="focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
/>

// Custom focus indicator
<div
  tabIndex={0}
  className="focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
  onKeyDown={(e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault()
      handleAction()
    }
  }}
>
  Interactive element
</div>
```

### Tab Order Management

```typescript
// Logical tab order (follows DOM)
<header>
  <nav tabIndex={0}>...</nav>  {/* First */}
</header>
<main tabIndex={0}>...</main>  {/* Second */}
<aside tabIndex={0}>...</aside> {/* Third */}

// Remove from tab order
<div tabIndex={-1}>
  {/* Programmatically focusable but not in tab order */}
</div>

// Skip link pattern
<a
  href="#main-content"
  className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-50 focus:bg-background focus:px-4 focus:py-2"
>
  Skip to main content
</a>
```

### Focus Trap (Modals)

Radix UI handles focus trapping automatically in dialogs:

```typescript
// core/components/ui/dialog.tsx
import * as DialogPrimitive from '@radix-ui/react-dialog'

// Radix Dialog automatically:
// - Traps focus within modal
// - Returns focus on close
// - Handles Escape key
// - Manages aria-hidden on background

<DialogPrimitive.Root>
  <DialogPrimitive.Trigger>Open</DialogPrimitive.Trigger>
  <DialogPrimitive.Portal>
    <DialogPrimitive.Overlay />
    <DialogPrimitive.Content>
      {/* Focus is trapped here */}
      <DialogPrimitive.Close>
        <span className="sr-only">Close</span>
        <X aria-hidden="true" />
      </DialogPrimitive.Close>
    </DialogPrimitive.Content>
  </DialogPrimitive.Portal>
</DialogPrimitive.Root>
```

## Screen Reader Support

### Screen Reader Only Text

```typescript
// Visually hidden but announced by screen readers
<span className="sr-only">Close dialog</span>

// Icon button with accessible name
<Button variant="ghost" size="icon">
  <X aria-hidden="true" />
  <span className="sr-only">Close</span>
</Button>

// More pages indicator
<span aria-hidden="true">...</span>
<span className="sr-only">More pages</span>
```

### Decorative Icons

```typescript
// Hide decorative icons from screen readers
<ChevronRight aria-hidden="true" className="h-4 w-4" />

// Separator in breadcrumb
<span role="presentation" aria-hidden="true">/</span>

// Loading spinner
<Loader2
  aria-hidden="true"
  className="h-4 w-4 animate-spin"
/>
<span className="sr-only">Loading...</span>
```

### Accessible Names Strategy

```typescript
// 1. Visible text (preferred)
<button>Delete Item</button>

// 2. aria-label for icon-only buttons
<button aria-label="Delete item">
  <TrashIcon aria-hidden="true" />
</button>

// 3. aria-labelledby for complex labels
<div id="dialog-title">Confirm Deletion</div>
<div aria-labelledby="dialog-title">
  {/* Content described by title */}
</div>

// 4. Form labels
<Label htmlFor="email">Email address</Label>
<Input id="email" type="email" />
```

## Color Contrast

### OKLCH Color System

The theme uses OKLCH color space for perceptually uniform colors:

```css
/* contents/themes/default/styles/globals.css */
:root {
  /* High contrast pairs */
  --primary: oklch(0.2050 0 0);           /* Dark */
  --primary-foreground: oklch(0.9850 0 0); /* Light - 4.5:1+ contrast */

  --destructive: oklch(0.5770 0.2450 27.3250);
  --destructive-foreground: oklch(1 0 0);

  /* Focus ring with sufficient contrast */
  --ring: oklch(0.7080 0 0);
}

.dark {
  /* Inverted for dark mode */
  --primary: oklch(0.9220 0 0);
  --primary-foreground: oklch(0.2050 0 0);
}
```

### Semantic Color Usage

```typescript
// ✅ CORRECT - Use semantic tokens that guarantee contrast
<p className="text-foreground">Primary text</p>
<p className="text-muted-foreground">Secondary text</p>
<button className="bg-primary text-primary-foreground">
  Action
</button>

// ❌ WRONG - Arbitrary colors may not have proper contrast
<p className="text-gray-400">Low contrast text</p>
<button className="bg-blue-300 text-blue-100">
  Poor contrast
</button>
```

## Component Patterns

### Slider/Range Component

```typescript
// core/components/ui/double-range.tsx
<div
  ref={thumbMinRef}
  role="slider"
  aria-label="Minimum value"
  aria-valuemin={min}
  aria-valuemax={max}
  aria-valuenow={localValue[0]}
  tabIndex={disabled ? -1 : 0}
  className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
  onKeyDown={handleKeyDown}  // Arrow keys to adjust
/>
```

### Pagination Component

```typescript
// core/components/ui/pagination.tsx
<nav role="navigation" aria-label="pagination">
  <PaginationPrevious aria-label="Go to previous page" />

  {pages.map((page) => (
    <PaginationLink
      aria-current={page === current ? 'page' : undefined}
    >
      {page}
    </PaginationLink>
  ))}

  <PaginationNext aria-label="Go to next page" />
</nav>
```

### Alert Component

```typescript
// core/components/ui/alert.tsx
<div
  ref={ref}
  role="alert"
  className={cn(alertVariants({ variant }), className)}
  {...props}
/>
```

## Testing Accessibility

### Tools

- **ESLint Plugin:** `eslint-plugin-jsx-a11y` for linting
- **Jest:** `jest-axe` for unit testing
- **Cypress:** `cypress-axe` for E2E testing
- **Manual:** Keyboard navigation, screen reader testing

### Jest-axe Example

```typescript
import { axe, toHaveNoViolations } from 'jest-axe'

expect.extend(toHaveNoViolations)

test('should have no accessibility violations', async () => {
  const { container } = render(<MyComponent />)
  const results = await axe(container)
  expect(results).toHaveNoViolations()
})
```

### Manual Testing Checklist

1. **Keyboard Navigation:**
   - Tab through all interactive elements
   - Verify logical focus order
   - Escape key closes modals
   - Enter/Space activates buttons

2. **Screen Reader:**
   - VoiceOver (Mac) or NVDA (Windows)
   - Verify content is announced correctly
   - Check form labels and error messages
   - Verify live regions announce updates

3. **Visual:**
   - Check focus indicators are visible
   - Verify contrast with browser devtools
   - Test with zoom (200%)

## Anti-Patterns

```typescript
// ❌ NEVER: Div as button
<div onClick={handleClick}>Click me</div>

// ✅ CORRECT: Use semantic button
<button onClick={handleClick}>Click me</button>

// ❌ NEVER: Icon-only button without accessible name
<button><TrashIcon /></button>

// ✅ CORRECT: Add aria-label or sr-only text
<button aria-label="Delete item">
  <TrashIcon aria-hidden="true" />
</button>

// ❌ NEVER: Remove focus indicator completely
<button className="outline-none focus:outline-none">
  No focus indicator
</button>

// ✅ CORRECT: Custom focus indicator
<button className="focus-visible:ring-2 focus-visible:ring-ring">
  Visible focus
</button>

// ❌ NEVER: Low contrast text
<p className="text-gray-300 bg-white">Hard to read</p>

// ✅ CORRECT: Use semantic tokens
<p className="text-muted-foreground bg-background">Readable</p>

// ❌ NEVER: Missing form labels
<input type="email" placeholder="Email" />

// ✅ CORRECT: Proper label association
<Label htmlFor="email">Email</Label>
<input id="email" type="email" />

// ❌ NEVER: Images without alt text
<img src="/logo.png" />

// ✅ CORRECT: Descriptive alt or empty for decorative
<img src="/logo.png" alt="Company Logo" />
<img src="/decorative.png" alt="" aria-hidden="true" />

// ❌ NEVER: Auto-playing media without controls
<video autoPlay src="/video.mp4" />

// ✅ CORRECT: User controls and captions
<video controls>
  <source src="/video.mp4" />
  <track kind="captions" src="/captions.vtt" />
</video>
```

## Checklist

Before finalizing component accessibility:

- [ ] Semantic HTML elements used (button, nav, form, etc.)
- [ ] All interactive elements keyboard accessible
- [ ] Focus indicators visible (focus-visible:ring-2)
- [ ] ARIA attributes correct (aria-expanded, aria-controls, etc.)
- [ ] Form fields have associated labels
- [ ] Error messages use role="alert"
- [ ] Icons have aria-hidden="true"
- [ ] Icon-only buttons have aria-label or sr-only text
- [ ] Color contrast meets 4.5:1 (text) / 3:1 (UI)
- [ ] Screen reader text (.sr-only) where needed
- [ ] Tab order is logical
- [ ] Modals trap focus and return it on close
- [ ] Live regions announce dynamic content

## Related Skills

- `shadcn-components` - Accessible UI component patterns
- `react-patterns` - Component architecture
- `tailwind-theming` - Color contrast tokens
- `cypress-e2e` - Accessibility testing
