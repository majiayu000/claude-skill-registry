---
name: a11y
description: "Universal accessibility best practices and standards across all technologies (HTML, CSS, React, MUI, Astro, React Native). WCAG 2.1/2.2 Level AA compliance, semantic HTML, ARIA, keyboard navigation, color contrast. Trigger: When implementing UI components, adding interactive elements, or ensuring accessibility compliance."
allowed-tools:
  - documentation-reader
  - web-search
  - file-reader
---

# Accessibility (a11y) Skill

## Overview

This skill centralizes accessibility guidelines and best practices for all technologies and frameworks used in the project, including HTML, CSS, React, MUI, Astro, React Native, and more. It covers semantic structure, ARIA usage, color contrast, keyboard navigation, and compliance with WCAG and WAI-ARIA standards.

## Objective

Ensure all user interfaces meet accessibility standards (WCAG 2.1/2.2 Level AA minimum) across all technologies. This skill provides universal accessibility guidance that technology-specific skills can reference.

---

## When to Use

Use this skill when:

- Building UI components with interactive elements
- Implementing forms, modals, or custom widgets
- Adding dynamic content or live regions
- Ensuring keyboard navigation
- Reviewing accessibility compliance
- Testing with screen readers

Don't use this skill for:

- Technology-specific implementation (delegate to react, html, etc.)
- General coding patterns (use conventions skill)
- Pure backend logic (no UI)

---

## Critical Patterns

### ✅ REQUIRED: Semantic HTML Elements

```html
<!-- ✅ CORRECT: Semantic elements -->
<nav>
  <a href="/home">Home</a>
</nav>
<main>
  <article>Content</article>
</main>
<button onClick="{action}">Submit</button>

<!-- ❌ WRONG: Non-semantic divs -->
<div class="nav">
  <div onClick="{navigate}">Home</div>
</div>
<div class="main">
  <div>Content</div>
</div>
<div onClick="{action}">Submit</div>
```

### ✅ REQUIRED: Keyboard Accessibility

```typescript
// ✅ CORRECT: Keyboard events
<button
  onClick={handleClick}
  onKeyDown={(e) => e.key === 'Enter' && handleClick()}
>

// ❌ WRONG: Mouse-only events
<div onClick={handleClick}> // Not keyboard accessible
```

### ✅ REQUIRED: Form Labels

```html
<!-- ✅ CORRECT: Associated label -->
<label htmlFor="email">Email Address</label>
<input id="email" type="email" />

<!-- ❌ WRONG: No label association -->
<div>Email Address</div>
<input type="email" />
```

### ✅ REQUIRED: Alt Text for Images

```html
<!-- ✅ CORRECT: Descriptive alt for informative images -->
<img src="chart.png" alt="Sales increased 25% in Q4" />

<!-- ✅ CORRECT: Empty alt for decorative images -->
<img src="decorative-border.png" alt="" />

<!-- ❌ WRONG: Missing alt -->
<img src="chart.png" />
```

---

## Conventions

### Semantic HTML

- Use semantic elements (`<nav>`, `<main>`, `<article>`, `<aside>`, `<footer>`)
- Proper heading hierarchy (h1 → h2 → h3, no skipping levels)
- Use `<button>` for actions, `<a>` for navigation
- Form labels must be associated with inputs

### ARIA

- Use ARIA only when semantic HTML is insufficient
- Prefer native elements over ARIA roles
- Common patterns: `aria-label`, `aria-labelledby`, `aria-describedby`
- Required for dynamic content: `aria-live`, `aria-atomic`

### Keyboard Navigation

- All interactive elements must be keyboard accessible
- Logical tab order (use tabindex only when necessary)
- Visible focus indicators
- Escape key closes modals/dropdowns

### Color and Contrast

- Text contrast ratio 4.5:1 minimum (7:1 for Level AAA)
- Large text (18pt+) minimum 3:1
- Don't rely solely on color to convey information
- Test with color blindness simulators
- **UI component contrast 3:1** (WCAG 2.1)
- **Focus indicators contrast 3:1** (WCAG 2.2)

### Touch Targets & Interaction

- **Touch target size minimum 24x24px** (WCAG 2.2)
- Recommend 44x44px for better usability (WCAG 2.1 AAA)
- Adequate spacing between targets
- **No dragging movements required** unless essential (WCAG 2.2)

### Screen Readers

- Provide alternative text for images (`alt` attribute)
- Use `aria-hidden="true"` for decorative elements
- Announce dynamic content changes with `aria-live`
- Test with screen readers (NVDA, JAWS, VoiceOver)

## Decision Tree

**Interactive element (button, link)?** → Ensure keyboard accessible (Tab, Enter/Space), visible focus indicator, proper role and semantic element.

**Form field?** → Associate `<label>` with input (htmlFor/id), provide error messages with `aria-describedby`, announce errors with `aria-live`.

**Dynamic content change?** → Use `aria-live="polite"` for non-urgent updates, `aria-live="assertive"` for critical alerts, `aria-atomic="true"` if entire region should be read.

**Custom widget (dropdown, modal, tabs)?** → Follow WAI-ARIA Authoring Practices patterns, implement keyboard navigation (Arrow keys, Escape, Enter), manage focus properly.

**Image or icon?** → Decorative: `alt=""` or `aria-hidden="true"`. Informative: descriptive `alt` text. Icon-only button: `aria-label`.

**Color conveys meaning?** → Add text label, icon, or pattern. Verify 4.5:1 contrast ratio for text, 3:1 for UI components.

**Modal or overlay?** → Trap focus inside modal, restore focus on close, allow Escape to dismiss, use `aria-modal="true"` and `role="dialog"`.

**Loading or status change?** → Use `aria-busy="true"` during loading, `role="status"` for status messages, ensure screen reader announces completion.

---

## Edge Cases

WCAG 2.2 updates:\*\*

- **24x24px minimum target size** (lowered from 44x44, but 44x44 still recommended)
- **Focus appearance:** Focus indicators must have 3:1 contrast ratio
- **Dragging movements:** Provide single-pointer alternatives for drag operations
- **Redundant entry:** Don't make users re-enter information already provided
- **Accessible authentication:** Don't require cognitive function tests (CAPTCHAs should have alternatives)

\*\*
**Skip links:** Provide "Skip to main content" link as first focusable element for keyboard users to bypass navigation.

**Focus trap issues:** Libraries like React may interfere with focus management. Test focus trap explicitly in modals.

**ARIA live regions throttling:** Rapid updates may be throttled by screen readers. Debounce updates or use atomic regions.

**Touch target size:** Minimum 44x44 pixels for touch targets (WCAG 2.1). Use padding to increase clickable area.

**Hidden content:** Use `aria-hidden="true"` for visual-only elements. Use `sr-only` class for screen-reader-only text.

**Custom controls:** For complex widgets (datepickers, sliders), follow WAI-ARIA Authoring Practices patterns exactly.

---

## References

- https://www.w3.org/WAI/WCAG21/quickref/
- https://www.w3.org/WAI/ARIA/apg/
