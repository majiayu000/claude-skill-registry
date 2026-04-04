---
name: accessibility-patterns
description: Provides web accessibility best practices for semantic HTML, ARIA, keyboard navigation, color contrast, and screen reader patterns. Use when building UI components, reviewing accessibility, or when user mentions 'a11y', 'accessibility', 'ARIA', 'screen reader', 'keyboard navigation', 'WCAG'.
---

# Accessibility Patterns

Reference guide for building inclusive, accessible web interfaces that comply with WCAG 2.1 AA standards.

## Core Principles (POUR)

| Principle | Meaning | Key Question |
|-----------|---------|-------------|
| **Perceivable** | Content is available to all senses | Can users see, hear, or read it? |
| **Operable** | Interface works with all input methods | Can users navigate with keyboard only? |
| **Understandable** | Content and UI are predictable | Can users understand and recover from errors? |
| **Robust** | Works across assistive technologies | Does it work with screen readers and future tools? |

## Semantic HTML Reference

Use the right element for the job. Semantic HTML provides accessibility for free.

### Document Structure

```html
<header>     <!-- Site/section header, landmarks for screen readers -->
<nav>        <!-- Navigation links, announced as "navigation" -->
<main>       <!-- Primary content, skip-to target -->
<article>    <!-- Self-contained content (blog post, card) -->
<section>    <!-- Thematic grouping with heading -->
<aside>      <!-- Tangentially related (sidebar, callout) -->
<footer>     <!-- Site/section footer -->
```

### Interactive Elements

| Need | Use | NOT |
|------|-----|-----|
| Clickable action | `<button>` | `<div onclick>` or `<span onclick>` |
| Navigation link | `<a href="...">` | `<div onclick="navigate()">` |
| Text input | `<input type="text">` | `<div contenteditable>` |
| Selection | `<select>` + `<option>` | Custom dropdown without ARIA |
| Toggle | `<input type="checkbox">` | `<div class="toggle">` |
| Form group | `<fieldset>` + `<legend>` | `<div class="form-group">` |

### Heading Hierarchy

```html
<!-- CORRECT: Logical hierarchy, no skipped levels -->
<h1>Page Title</h1>
  <h2>Section</h2>
    <h3>Subsection</h3>
    <h3>Subsection</h3>
  <h2>Another Section</h2>

<!-- WRONG: Skipped levels, multiple h1, heading for styling -->
<h1>Title</h1>
<h1>Another Title</h1>  <!-- Only one h1 per page -->
  <h4>Jumped from h1 to h4</h4>  <!-- Skipped h2, h3 -->
```

## ARIA Roles, States, and Properties

ARIA supplements HTML semantics. The first rule of ARIA: **do not use ARIA if native HTML provides the semantics.**

### Landmark Roles

Most of these are already implied by semantic HTML.

| Role | HTML Equivalent | When to Use ARIA |
|------|----------------|-----------------|
| `banner` | `<header>` (top-level) | Nested headers needing landmark |
| `navigation` | `<nav>` | Rarely needed |
| `main` | `<main>` | Rarely needed |
| `complementary` | `<aside>` | Rarely needed |
| `contentinfo` | `<footer>` (top-level) | Nested footers needing landmark |
| `search` | `<search>` | Browsers without `<search>` support |
| `form` | `<form>` (with name) | Forms without accessible name |
| `region` | `<section>` (with name) | Generic labeled regions |

### Common ARIA Attributes

| Attribute | Purpose | Example |
|-----------|---------|---------|
| `aria-label` | Invisible label for element | `<button aria-label="Close dialog">X</button>` |
| `aria-labelledby` | Points to visible label element | `<div aria-labelledby="heading-id">` |
| `aria-describedby` | Points to descriptive text | `<input aria-describedby="password-help">` |
| `aria-expanded` | Toggle/disclosure state | `<button aria-expanded="false">Menu</button>` |
| `aria-hidden` | Hide from assistive tech | `<span aria-hidden="true">decorative icon</span>` |
| `aria-live` | Announce dynamic content | `<div aria-live="polite">Status: Saved</div>` |
| `aria-required` | Field is required | `<input aria-required="true">` (prefer `required` attr) |
| `aria-invalid` | Field has validation error | `<input aria-invalid="true">` |
| `aria-current` | Current item in a set | `<a aria-current="page">Home</a>` |
| `aria-disabled` | Disabled but focusable | `<button aria-disabled="true">Submit</button>` |

### Live Regions

For content that updates dynamically (notifications, status messages, chat).

```html
<!-- Polite: announced after current speech finishes -->
<div aria-live="polite" aria-atomic="true">
  3 items in your cart
</div>

<!-- Assertive: interrupts current speech (use sparingly) -->
<div aria-live="assertive" role="alert">
  Error: Payment failed. Please try again.
</div>

<!-- Status: polite + role=status (form feedback, progress) -->
<div role="status">
  Saving... Done!
</div>
```

| Politeness | When to Use |
|------------|------------|
| `polite` | Status updates, cart counts, non-urgent info |
| `assertive` | Errors, warnings, time-sensitive alerts |
| `off` | Disable announcements (default) |

## Keyboard Navigation

### Focus Management Rules

| Rule | Implementation |
|------|---------------|
| All interactive elements are focusable | Use native HTML elements or `tabindex="0"` |
| Focus order matches visual order | Source order = visual order, avoid CSS reordering |
| Focus is visible | Never `outline: none` without a visible alternative |
| No keyboard traps | User can always Tab away (except modal dialogs) |
| Skip links available | First focusable element skips to main content |

### Skip Link Pattern

```html
<!-- First element in <body>, visually hidden until focused -->
<a href="#main-content" class="skip-link">
  Skip to main content
</a>

<!-- ... navigation ... -->

<main id="main-content" tabindex="-1">
  <!-- Content starts here -->
</main>
```

```css
.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  padding: 8px 16px;
  background: #000;
  color: #fff;
  z-index: 100;
  transition: top 0.2s;
}

.skip-link:focus {
  top: 0;
}
```

### Key Bindings Reference

| Pattern | Expected Keys |
|---------|--------------|
| Buttons | Enter or Space to activate |
| Links | Enter to follow |
| Checkboxes | Space to toggle |
| Radio buttons | Arrow keys to move, Space to select |
| Tabs | Arrow keys to switch, Tab to exit tab list |
| Menus | Arrow keys to navigate, Enter to select, Escape to close |
| Dialogs | Escape to close, Tab trapped inside, focus on close or first element |
| Dropdowns | Arrow keys to navigate, Enter to select, Escape to close |

### Tab Trap for Modals

```javascript
function trapFocus(dialog) {
  const focusable = dialog.querySelectorAll(
    'a[href], button:not([disabled]), input:not([disabled]), ' +
    'select:not([disabled]), textarea:not([disabled]), [tabindex="0"]'
  );
  const first = focusable[0];
  const last = focusable[focusable.length - 1];

  dialog.addEventListener('keydown', (e) => {
    if (e.key !== 'Tab') return;

    if (e.shiftKey) {
      if (document.activeElement === first) {
        last.focus();
        e.preventDefault();
      }
    } else {
      if (document.activeElement === last) {
        first.focus();
        e.preventDefault();
      }
    }
  });

  first.focus();
}
```

## Color Contrast Requirements

### WCAG 2.1 AA Minimums

| Content Type | Minimum Ratio | Example |
|-------------|--------------|---------|
| Normal text (<18px / <14px bold) | 4.5:1 | #595959 on #FFFFFF = 7:1 |
| Large text (>=18px / >=14px bold) | 3:1 | #767676 on #FFFFFF = 4.5:1 |
| UI components & graphical objects | 3:1 | Borders, icons, focus indicators |
| Decorative / logos | No requirement | Brand logos are exempt |

### Testing Contrast

```bash
# Browser DevTools: Inspect element > Color picker shows ratio
# Chrome: Lighthouse > Accessibility audit
# Firefox: Accessibility Inspector > Check for issues
```

### Do Not Rely on Color Alone

```html
<!-- BAD: Color is the only indicator -->
<span style="color: red;">Error in this field</span>

<!-- GOOD: Color + icon + text -->
<span class="error">
  <svg aria-hidden="true"><!-- error icon --></svg>
  Error: Email address is required
</span>

<!-- BAD: Link distinguished only by color -->
<p>Read our <span style="color: blue;">terms of service</span></p>

<!-- GOOD: Link has underline (and color) -->
<p>Read our <a href="/terms">terms of service</a></p>
```

## Form Accessibility

### Labels and Instructions

```html
<!-- Every input MUST have a label -->
<label for="email">Email address</label>
<input type="email" id="email" name="email" required
       aria-describedby="email-help">
<p id="email-help">We will never share your email.</p>

<!-- Group related fields -->
<fieldset>
  <legend>Shipping Address</legend>
  <label for="street">Street</label>
  <input type="text" id="street" name="street">
  <label for="city">City</label>
  <input type="text" id="city" name="city">
</fieldset>
```

### Error Messages

```html
<!-- Associate error with input -->
<label for="password">Password</label>
<input type="password" id="password" name="password"
       aria-invalid="true"
       aria-describedby="password-error">
<p id="password-error" role="alert">
  Password must be at least 8 characters.
</p>
```

### Required Fields

```html
<!-- Use both native and visual indicators -->
<label for="name">
  Full name <span aria-hidden="true">*</span>
</label>
<input type="text" id="name" name="name" required
       aria-required="true">

<!-- Explain the asterisk at the form top -->
<p>Fields marked with <span aria-hidden="true">*</span>
   <span class="sr-only">asterisk</span> are required.</p>
```

## Component Patterns

### Accessible Button

```html
<!-- Native button (best) -->
<button type="button" onclick="doAction()">
  Save Changes
</button>

<!-- Icon-only button (needs label) -->
<button type="button" aria-label="Close dialog">
  <svg aria-hidden="true" focusable="false">
    <!-- X icon SVG -->
  </svg>
</button>

<!-- Loading state -->
<button type="button" aria-disabled="true" aria-busy="true">
  <span aria-hidden="true">Saving...</span>
  <span class="sr-only">Saving changes, please wait</span>
</button>
```

### Accessible Tabs

```html
<div role="tablist" aria-label="Account settings">
  <button role="tab" id="tab-1" aria-selected="true"
          aria-controls="panel-1" tabindex="0">
    Profile
  </button>
  <button role="tab" id="tab-2" aria-selected="false"
          aria-controls="panel-2" tabindex="-1">
    Security
  </button>
</div>

<div role="tabpanel" id="panel-1" aria-labelledby="tab-1"
     tabindex="0">
  <!-- Profile content -->
</div>

<div role="tabpanel" id="panel-2" aria-labelledby="tab-2"
     tabindex="0" hidden>
  <!-- Security content -->
</div>
```

### Accessible Dialog

```html
<dialog id="confirm-dialog" aria-labelledby="dialog-title"
        aria-describedby="dialog-desc">
  <h2 id="dialog-title">Confirm Deletion</h2>
  <p id="dialog-desc">
    This action cannot be undone. Are you sure?
  </p>
  <div>
    <button type="button" autofocus>Cancel</button>
    <button type="button" class="danger">Delete</button>
  </div>
</dialog>
```

### Screen Reader Only Text

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
  border-width: 0;
}
```

```html
<!-- Provide context that's visually obvious but not to screen readers -->
<button>
  <svg aria-hidden="true"><!-- trash icon --></svg>
  <span class="sr-only">Delete item: Running Shoes</span>
</button>
```

## Image Accessibility

| Image Type | Alt Text Rule | Example |
|------------|--------------|---------|
| Informative | Describe the content | `alt="Bar chart showing 40% growth in Q3"` |
| Decorative | Empty alt | `alt=""` (NOT omitted, empty string) |
| Functional (in link/button) | Describe the action | `alt="Search"` on a magnifying glass icon |
| Complex (chart/diagram) | Brief alt + long description | `alt="Sales data" aria-describedby="chart-desc"` |
| Text in image | Reproduce the text | `alt="Sale: 50% off all items"` |

```html
<!-- Informative image -->
<img src="team.jpg" alt="Our team of 12 engineers at the 2024 retreat">

<!-- Decorative image (empty alt, not missing) -->
<img src="divider.png" alt="">

<!-- Complex image with long description -->
<img src="architecture.png" alt="System architecture diagram"
     aria-describedby="arch-desc">
<div id="arch-desc">
  <p>The system consists of three layers: a React frontend
     communicating via REST API with a Node.js backend,
     which connects to a PostgreSQL database...</p>
</div>
```

## Common Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| `<div onclick>` as button | Not focusable, no keyboard, no role | Use `<button>` |
| Missing `alt` on `<img>` | Screen reader reads filename | Add descriptive `alt` or `alt=""` |
| `outline: none` without replacement | Focus indicator invisible | Use custom `:focus-visible` styles |
| Color-only indication | Invisible to colorblind users | Add icon, text, or pattern |
| Auto-playing media | Disorienting, blocks screen readers | Require user interaction to play |
| `tabindex > 0` | Unpredictable focus order | Use `0` or `-1` only |
| Missing form labels | Input purpose unknown to screen readers | Add `<label>` with `for` attribute |
| Using `title` as primary label | Not reliably announced | Use `aria-label` or visible label |
| Placeholder as label | Disappears on input, low contrast | Use visible `<label>` element |
| Mouse-only interactions (hover) | Inaccessible without mouse | Support focus and keyboard too |
| Missing language attribute | Wrong pronunciation by screen reader | Add `lang="en"` on `<html>` |
| ARIA overuse | More fragile than native HTML | Use semantic HTML first |

## Testing Checklist

### Automated Testing

- [ ] Run axe-core or Lighthouse accessibility audit
- [ ] Validate HTML (invalid HTML breaks assistive tech)
- [ ] Check color contrast ratios with automated tools
- [ ] Run ESLint with `eslint-plugin-jsx-a11y` (React projects)

### Manual Testing

- [ ] Navigate entire page with keyboard only (Tab, Enter, Escape, Arrows)
- [ ] Verify visible focus indicator on all interactive elements
- [ ] Test with screen reader (VoiceOver, NVDA, or JAWS)
- [ ] Zoom to 200% -- content reflows, nothing is cut off
- [ ] Test with browser in high-contrast mode
- [ ] Verify all images have appropriate alt text
- [ ] Check that page has logical heading hierarchy
- [ ] Confirm form errors are announced and associated with inputs
- [ ] Test all modals/dialogs for focus trap and Escape to close

### Screen Reader Quick Test

| Test | Expected Behavior |
|------|-------------------|
| Read page top to bottom | Logical, complete content |
| Navigate by headings (H key) | All sections reachable |
| Navigate by landmarks (D key) | Header, nav, main, footer announced |
| Tab through interactive elements | All buttons/links/inputs reachable |
| Activate a button | Action performed, state change announced |
| Fill out a form | Labels read, errors announced |
| Open/close a dialog | Focus moves in, Escape closes, focus returns |
