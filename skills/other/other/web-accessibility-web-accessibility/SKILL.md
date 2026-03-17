---
name: web-accessibility-web-accessibility
description: WCAG, ARIA, keyboard navigation
---

# Accessibility

> **Quick Guide:** All interactive elements keyboard accessible. Use Radix UI for ARIA patterns. WCAG AA minimum (4.5:1 text contrast). Proper form labels and error handling. Test with axe DevTools and screen readers.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST ensure all interactive elements are keyboard accessible with visible focus indicators)**

**(You MUST use Radix UI components for built-in ARIA patterns instead of manual implementation)**

**(You MUST maintain WCAG AA minimum contrast ratios - 4.5:1 for text, 3:1 for UI components)**

**(You MUST never use color alone to convey information - always add icons, text, or patterns)**

</critical_requirements>

---

**Auto-detection:** Accessibility (a11y), WCAG compliance, ARIA patterns, keyboard navigation, screen reader support, Radix UI, focus management

**When to use:**

- Implementing keyboard navigation and focus management
- Using Radix UI for accessible component patterns (built-in a11y)
- Ensuring WCAG AA color contrast (4.5:1 text, 3:1 UI components)
- Testing with axe DevTools and screen readers
- Building interactive components (buttons, forms, modals, tables)
- Adding dynamic content updates (live regions, status messages)

**When NOT to use:**

- Working on backend/API code with no UI
- Writing build scripts or configuration files
- Creating documentation or non-rendered content
- Working with CLI tools (different accessibility considerations)

**Target:** WCAG 2.2 Level AA compliance (minimum), AAA where feasible

**Key patterns covered:**

- Keyboard navigation standards (tab order, focus management, skip links, Escape to close)
- ARIA patterns with Radix UI components (prefer Radix for built-in accessibility)
- WCAG 2.2 AA compliance minimum (contrast ratios, semantic HTML, touch targets 24x24px minimum)
- Screen reader support (role-based queries, hidden content, live regions)

**Detailed Resources:**

- For code examples, see [examples/](examples/) directory:
  - [core.md](examples/core.md) - Skip links, semantic HTML, landmarks, button vs link
  - [forms.md](examples/forms.md) - Form validation, error handling, Radix select
  - [focus.md](examples/focus.md) - Modal dialogs, focus indicators
  - [color.md](examples/color.md) - Contrast, color-independent indicators, tokens
  - [tables.md](examples/tables.md) - Sortable data tables
  - [touch-targets.md](examples/touch-targets.md) - Touch target sizing
  - [screen-reader.md](examples/screen-reader.md) - sr-only, hiding decorative content
  - [testing.md](examples/testing.md) - Role queries, jest-axe, Lighthouse CI
- For decision frameworks and anti-patterns, see [reference.md](reference.md)

---

<philosophy>

## Philosophy

Accessibility ensures digital products are usable by everyone, including users with disabilities. This skill applies the principle that **accessibility is a requirement, not a feature** - it should be built in from the start, not retrofitted.

Key philosophy:

- **Semantic HTML first** - Use native elements for built-in accessibility
- **Radix UI for complex patterns** - Leverage tested, accessible component primitives
- **Progressive enhancement** - Start with keyboard, add mouse interactions on top
- **WCAG as baseline** - Meet AA minimum, aim for AAA where feasible

</philosophy>

---

<patterns>

## Core Patterns

### Keyboard Navigation Standards

**CRITICAL: All interactive elements must be keyboard accessible**

#### Tab Order

- **Logical flow** - Tab order must follow visual reading order (left-to-right, top-to-bottom)
- **No keyboard traps** - Users can always tab away from any element
- **Skip repetitive content** - Provide skip links to main content
- **tabindex rules:**
  - `tabindex="0"` - Adds element to natural tab order (use sparingly)
  - `tabindex="-1"` - Programmatic focus only (modal content, headings)
  - Never use `tabindex > 0` (creates unpredictable tab order)

#### Focus Management

- **Visible focus indicators** - Always show clear focus state (never `outline: none` without replacement)
- **Focus on open** - When opening modals/dialogs, move focus to first interactive element or close button
- **Focus on close** - Restore focus to trigger element when closing modals/dialogs
- **Focus trapping** - Trap focus inside modals using Radix UI or manual implementation
- **Programmatic focus** - Use `element.focus()` for dynamic content (search results, error messages)

#### Keyboard Shortcuts

- **Standard patterns:**
  - `Escape` - Close modals, cancel actions, clear selections
  - `Enter/Space` - Activate buttons and links
  - `Arrow keys` - Navigate lists, tabs, menus, sliders
  - `Home/End` - Jump to first/last item
  - `Tab/Shift+Tab` - Navigate between interactive elements

#### Skip Links

**MANDATORY for pages with navigation**

- Place skip link as first focusable element
- Visually hidden until focused
- Allow users to skip navigation and jump to main content
- Multiple skip links for complex layouts (skip to navigation, skip to sidebar, etc.)

---

### ARIA with Radix UI

**Prefer Radix UI components** - They handle ARIA automatically:

- `Dialog` - focus trapping, Escape to close, aria-modal
- `Select` - keyboard navigation, aria-selected, listbox pattern
- `Tabs` - arrow key navigation, aria-selected
- `Tooltip` - proper timing, keyboard support
- `Popover` - focus management, click outside to close

#### Component-Specific ARIA

**Buttons:**

- `aria-label` - For icon-only buttons
- `aria-pressed` - For toggle buttons
- `aria-expanded` - For expandable sections
- `aria-disabled` - Use with `disabled` attribute

**Forms:**

- `aria-required` - Required fields (use with `required`)
- `aria-invalid` - Invalid fields
- `aria-describedby` - Link to error messages, helper text
- `aria-errormessage` - Explicit error message reference

**Navigation:**

- `aria-current="page"` - Current page in navigation
- `aria-label` - Describe navigation purpose ("Main navigation", "Footer navigation")

**Modals/Dialogs:**

- `role="dialog"` or `role="alertdialog"`
- `aria-modal="true"`
- `aria-labelledby` - Points to dialog title
- `aria-describedby` - Points to dialog description

**Tables:**

- `scope="col"` and `scope="row"` for headers
- `<caption>` for table description
- `aria-sort` for sortable columns

#### Live Regions

**Use for dynamic content updates:**

- `aria-live="polite"` - Announce when user is idle (status messages, non-critical updates)
- `aria-live="assertive"` - Announce immediately (errors, critical alerts)
- `aria-atomic="true"` - Announce entire region content
- `role="status"` - For status messages (implies `aria-live="polite"`)
- `role="alert"` - For error messages (implies `aria-live="assertive"`)

**Best practices:**

- Keep messages concise and meaningful
- Clear old messages before new ones
- Don't spam with rapid updates (debounce)

---

### Color Contrast & Visual Design

**Text contrast (AA):**

- Normal text (< 18px): 4.5:1 minimum
- Large text (>= 18px or >= 14px bold): 3:1 minimum
- AAA (recommended): 7:1 for normal, 4.5:1 for large

**Non-text contrast:**

- UI components (buttons, form inputs): 3:1 minimum
- Focus indicators: 3:1 against background
- Icons (functional): 3:1 minimum

**Color Independence:**

- Add icons to color-coded states (check for success, X for error)
- Use text labels with status colors
- Provide patterns/textures in charts
- Underline links in body text

---

### Semantic HTML

**Always use semantic HTML:**

- `<button>` for actions (not `<div onclick>`)
- `<a>` for navigation (not `<div onclick>`)
- `<nav>` for navigation sections
- `<main>` for primary content (one per page)
- `<header>` and `<footer>` for page sections
- `<ul>/<ol>` for lists
- `<table>` for tabular data (not divs with grid CSS)
- `<form>` with proper `<label>` associations

**Never:**

- Use `<div>` or `<span>` for interactive elements
- Use click handlers on non-interactive elements without proper role
- Use tables for layout
- Use placeholder as label replacement

---

### Form Accessibility

**Label Associations:**

- Always use proper `<label>` with `for` attribute
- Or wrap input inside label element

**Error Handling:**

- `aria-invalid="true"` on invalid fields
- `aria-describedby` linking to error message
- `role="alert"` on error messages for screen reader announcement
- Visual error indicators (icons, border color)
- Error summary at top of form for multiple errors

**Required Fields:**

- `required` attribute for browser validation
- `aria-required="true"` for screen readers
- Visual indicator (asterisk, "required" text)
- Legend/description explaining required fields

**Input Types:**

- `type="email"` - Email keyboard
- `type="tel"` - Phone keyboard
- `type="number"` - Number keyboard
- `type="date"` - Date picker
- `type="search"` - Search keyboard

---

### Focus Indicators

**Minimum requirements:**

- 3:1 contrast ratio against background
- 2px minimum thickness
- Clear visual difference from unfocused state
- Consistent across all interactive elements

**Use `:focus-visible` for better UX:**

- `:focus` - Shows on mouse click (annoying)
- `:focus-visible` - Shows only for keyboard navigation (better)

---

### Touch Target Sizes

**WCAG 2.2 Target Size Requirements:**

**Level AA (2.5.8 Target Size Minimum):**

- Minimum: 24x24 CSS pixels
- OR adequate spacing from adjacent targets (24px between closest points)
- Exceptions: inline text links, user agent controls, essential designs

**Level AAA (2.5.5 Target Size Enhanced):**

- Minimum: 44x44 CSS pixels (recommended for best UX)

**Interactive elements:**

- Buttons: 24x24px minimum (44x44px recommended)
- Links in text: Inline exemption applies, but increase padding where feasible
- Form inputs: 24px height minimum (44px recommended)
- Icons: 24x24px minimum touch target

**Spacing:**

- 8px minimum between adjacent touch targets
- More spacing on mobile (12-16px recommended)
- Alternative: 24px spacing allows smaller targets

---

### Screen Reader Support

**Visually Hidden Content:**

- Use `.sr-only` class for screen reader only text
- Use `aria-label` for icon-only buttons
- Use empty `alt=""` for decorative images

**Hidden from Screen Readers:**

- `aria-hidden="true"` for decorative content
- Empty `alt=""` for decorative images

---

### Motion and Animation Accessibility

**WCAG 2.3.3 Animation from Interactions (AAA):**

Motion can cause nausea, dizziness, or vestibular disorders for some users. Provide motion alternatives:

**Use `prefers-reduced-motion` media query:**

```css
/* Approach 1: Disable animations when user prefers reduced motion */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

/* Approach 2: Only animate when user has no preference */
@media (prefers-reduced-motion: no-preference) {
  .animated-element {
    animation: slide-in 300ms ease-out;
  }
}
```

**Key principles:**

- `reduce` means minimize, not eliminate all motion - essential animations can remain
- Replace motion effects (scale, rotate, slide) with non-motion effects (fade, dissolve, color change)
- Provide pause/stop controls for auto-playing content longer than 5 seconds
- Avoid parallax scrolling effects or provide alternatives

---

### WCAG 2.2 New Success Criteria

**WCAG 2.2** (October 2023) added 9 new success criteria. Key ones for developers:

**Level A:**

- **3.2.6 Consistent Help** - Help mechanisms (contact, chat) must appear in same relative order across pages
- **3.3.7 Redundant Entry** - Previously entered info must be auto-populated or available for selection

**Level AA:**

- **2.4.11 Focus Not Obscured (Minimum)** - Focused element must not be entirely hidden by other content (sticky headers, modals)
- **2.5.7 Dragging Movements** - Provide single-pointer alternative to drag operations
- **2.5.8 Target Size (Minimum)** - 24x24px minimum or adequate spacing
- **3.3.8 Accessible Authentication** - No cognitive function tests (CAPTCHAs) unless alternatives exist

**Level AAA:**

- **2.4.12 Focus Not Obscured (Enhanced)** - No part of focus indicator hidden
- **2.4.13 Focus Appearance** - Focus indicator 2px perimeter, 3:1 contrast
- **3.3.9 Accessible Authentication (Enhanced)** - Stricter CAPTCHA requirements

**Removed from WCAG 2.2:**

- **4.1.1 Parsing** - Obsolete due to modern browser error correction

</patterns>

---

<testing>

## Testing Approach

**RECOMMENDED: Multi-layered testing strategy**

### Automated Testing

**Use Testing Library's role-based queries:**

```typescript
const button = screen.getByRole("button", { name: "Submit" });
const switchElement = within(feature).getByRole("switch");
```

**Additional tools:**

- **jest-axe** - Automated accessibility testing in Jest unit tests
- **vitest-axe** - Same API as jest-axe, but for Vitest projects
- **cypress-axe** - E2E accessibility testing with Cypress
- **axe-core** - Runtime accessibility testing (v4.10+ supports WCAG 2.2)
- **eslint-plugin-jsx-a11y** - Lint-time accessibility checks

**Note:** axe-core finds ~57% of WCAG issues automatically. Always combine with manual testing.

### Manual Testing Checklist

**Keyboard navigation:**

- [ ] Tab through all interactive elements in logical order
- [ ] Activate buttons with Enter/Space
- [ ] Close modals with Escape
- [ ] Navigate dropdowns with arrows
- [ ] No keyboard traps
- [ ] Focus indicators visible on all elements

**Screen reader:**

- [ ] All images have alt text (or alt="" if decorative)
- [ ] Form inputs have labels
- [ ] Error messages are announced
- [ ] Button purposes are clear
- [ ] Headings create logical outline
- [ ] Landmarks are labeled
- [ ] Live regions announce updates
- [ ] Tables have proper headers

**Visual:**

- [ ] Color contrast meets WCAG AA (4.5:1 text, 3:1 UI)
- [ ] Information not conveyed by color alone
- [ ] Text resizable to 200% without horizontal scroll
- [ ] Touch targets meet 24x24px minimum (AA) or 44x44px (AAA recommended)
- [ ] Focus indicators have 3:1 contrast
- [ ] Animations respect prefers-reduced-motion

### Screen Reader Testing

**Test with multiple screen readers:**

- **NVDA** (Windows) - Free, most popular
- **JAWS** (Windows) - Industry standard
- **VoiceOver** (macOS/iOS) - Built-in
- **TalkBack** (Android) - Built-in

</testing>

---

## Resources

**Official guidelines:**

- WCAG 2.2 Guidelines: https://www.w3.org/WAI/WCAG22/quickref/
- What's New in WCAG 2.2: https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/
- WAI-ARIA Authoring Practices: https://www.w3.org/WAI/ARIA/apg/
- WAI-ARIA 1.3 Draft (new roles: suggestion, comment, mark): https://w3c.github.io/aria/

**Note:** WAI-ARIA 1.3 is still in draft (as of January 2024). New roles like `suggestion`, `comment`, and `mark` are not yet widely supported by browsers and assistive technologies.

**Tools:**

- axe DevTools: https://www.deque.com/axe/devtools/
- axe-core API: https://github.com/dequelabs/axe-core/blob/develop/doc/API.md
- WAVE: https://wave.webaim.org/
- WebAIM Contrast Checker: https://webaim.org/resources/contrastchecker/

**Testing libraries:**

- jest-axe: https://github.com/nickcolley/jest-axe
- vitest-axe: https://github.com/chaance/vitest-axe
- cypress-axe: https://github.com/component-driven/cypress-axe

**Screen readers:**

- NVDA Screen Reader: https://www.nvaccess.org/
- Keyboard Navigation Guide: https://webaim.org/articles/keyboard/

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST ensure all interactive elements are keyboard accessible with visible focus indicators)**

**(You MUST use Radix UI components for built-in ARIA patterns instead of manual implementation)**

**(You MUST maintain WCAG AA minimum contrast ratios - 4.5:1 for text, 3:1 for UI components)**

**(You MUST never use color alone to convey information - always add icons, text, or patterns)**

**Failure to follow these rules will make the site unusable for keyboard users, screen reader users, and color-blind users - violating WCAG 2.2 Level AA compliance.**

</critical_reminders>
