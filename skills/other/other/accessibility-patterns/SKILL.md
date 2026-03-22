---
name: accessibility-patterns
description: "Accessibility patterns including WCAG 2.2 compliance, ARIA correctness, keyboard navigation, and screen reader compatibility. Use when writing or reviewing UI code with interactive elements, forms, or dynamic content."
durability: encoded-preference
---

# Accessibility Patterns

## WCAG 2.2 POUR Principles

### Perceivable
- All non-text content (images, icons, SVGs) has text alternatives. Decorative images use `alt=""` or `aria-hidden="true"`
- Color is never the sole means of conveying information (error states, status indicators)
- Text contrast meets 4.5:1 for normal text, 3:1 for large text (WCAG 1.4.3)
- Non-text contrast meets 3:1 for UI components and graphical objects (WCAG 1.4.11)
- Content reflows without horizontal scrolling at 320px width / 400% zoom (WCAG 1.4.10)
- Text spacing can be overridden without loss of content (WCAG 1.4.12)
- Content remains visible and functional in forced colors mode (`forced-colors: active`) and high contrast mode (`prefers-contrast: more`)

### Operable
- All interactive elements reachable and operable via keyboard alone
- No keyboard traps -- users can always Tab away from any element
- Focus order follows logical reading sequence
- Focus indicator is visible on every interactive element (WCAG 2.4.7, enhanced 2.4.13)
- Skip navigation link present and functional for bypassing repeated content (WCAG 2.4.1)
- Target size minimum 24x24 CSS pixels for pointer inputs (WCAG 2.5.8)
- Motion-triggered actions have alternatives and respect `prefers-reduced-motion` (WCAG 2.3.3)

### Understandable
- Page language declared via `lang` attribute on `<html>`
- Form inputs have visible labels (not just placeholder text)
- Error messages identify the field and describe how to fix the error
- Consistent navigation and identification across pages

### Robust
- HTML nesting and unique IDs correct for accessibility tree integrity (duplicate IDs break ARIA references, improper nesting confuses assistive technologies)
- Custom components use correct ARIA roles, states, and properties
- Status messages use `aria-live` regions (not focus changes) to announce updates
- Content works across browsers and assistive technologies

## Semantic HTML Before ARIA

Prefer native HTML elements over ARIA roles. ARIA should supplement, not replace, semantic HTML.

| Instead of | Use |
|------------|-----|
| `<div role="button">` | `<button>` |
| `<span role="link">` | `<a href>` |
| `<div role="heading" aria-level="2">` | `<h2>` |
| `<div role="navigation">` | `<nav>` |
| `<div role="main">` | `<main>` |
| `<div role="checkbox">` | `<input type="checkbox">` |

## ARIA Anti-Patterns (CRITICAL)

- `aria-label` on non-interactive, non-landmark elements (screen readers may ignore it)
- `aria-hidden="true"` on focusable elements (creates ghost focus)
- Redundant roles on semantic HTML (`<nav role="navigation">`, `<button role="button">`)
- `role="presentation"` or `role="none"` on elements with focusable descendants
- Using `aria-expanded` without a corresponding controlled region (`aria-controls`)
- `aria-live="assertive"` for non-urgent updates (use `polite` for most cases)

## Interactive Component Patterns

### Modals/Dialogs
- Focus moves into modal on open
- Focus is trapped inside modal (Tab cycles within)
- Escape closes the modal
- Focus returns to trigger element on close
- Background content has `aria-hidden="true"` or `inert`

### Tabs
- Tab key moves into/out of tablist; Arrow keys switch tabs
- `aria-selected` on active tab; `aria-controls` links tab to panel
- Home/End move to first/last tab

### Menus
- Arrow keys navigate menu items
- Enter/Space activates menu item
- Escape closes menu and returns focus to trigger
- `role="menu"` on container; `role="menuitem"` on items

### Carousels/Sliders
- Arrow keys move between slides
- Pause/stop control available and keyboard accessible
- Current position announced (e.g., "Slide 2 of 5")
- Auto-advancing respects `prefers-reduced-motion`

### Data Tables
- Headers associated with cells via `scope` or `headers` attributes
- Caption or `aria-label` describes table purpose
- Sortable columns operable via keyboard with sort direction announced

### Forms
- Every input has a programmatically associated `<label>` (via `for`/`id` or wrapping)
- Required fields use `aria-required="true"` or `required` attribute
- Error messages associated via `aria-describedby`
- Form validation errors announced to screen readers (via `aria-live` or focus management)

### Custom Widgets
- Follow WAI-ARIA Authoring Practices for keyboard interaction patterns
- Manage focus explicitly for composite widgets (menus, listboxes, trees)
- Announce state changes (expanded/collapsed, selected/deselected, checked/unchecked)

## Dynamic Content

- Route changes in SPAs announce the new page title to screen readers
- Loading states communicated via `aria-busy` or live region announcements
- Toast/notification content uses `role="status"` or `aria-live="polite"`
- Content added/removed dynamically updates the accessibility tree

## Common Failure Patterns

- Empty buttons or links (no text content, no `aria-label`)
- Form inputs with placeholder as the only label (placeholder disappears on input)
- Auto-playing media without pause controls
- Infinite scroll without keyboard-accessible "load more" alternative
- Drag-and-drop without keyboard alternative
- Custom select/dropdown that doesn't support arrow key navigation
- Focus lost after dynamic content updates (modal close, item deletion, SPA navigation)
- `tabindex` values > 0 creating unpredictable tab order
- Click handlers on non-interactive elements (`<div onClick>`) without role and keyboard support

## Framework-Specific Pitfalls

- **React**: Portals can break focus order; `useEffect` cleanup must restore focus; `key` changes can reset focus
- **Vue**: Transition groups may skip screen reader announcements; `v-if` removal loses focus
- **SPA Routers**: Route changes do not announce page title by default -- must implement manually

## Automated vs Manual Testing

Automated tools (axe-core, Lighthouse) catch ~30% of accessibility issues. They detect missing alt text, low contrast, missing labels. They CANNOT detect: logical reading order, keyboard interaction quality, focus management correctness, ARIA misuse in context, cognitive clarity of content. Both are required for genuine compliance.
