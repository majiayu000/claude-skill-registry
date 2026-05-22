---
name: web-design-guidelines
version: 2.0.0
description: "[Frontend] Review UI code for web interface design compliance covering WCAG 2.2/3.0 accessibility, responsive design, performance, usability, and modern best practices. Use when asked to 'review my UI', 'check accessibility', 'audit design', 'review UX', 'check responsive design', or 'check my site against best practices'. Actions: review, check, audit, analyze, validate. Topics: accessibility, WCAG, ARIA, semantic HTML, focus states, forms, animation, typography, content handling, images, performance, Core Web Vitals, navigation, touch interaction, responsive design, mobile-first, dark mode, internationalization, hydration."
argument-hint: <file-or-pattern>
---

# Web Interface Design Guidelines

Comprehensive code review for web interface compliance with industry standards including WCAG 2.2, Core Web Vitals, and modern UX best practices.

## Summary

**Goal:** Review UI code for compliance with WCAG 2.2 accessibility, responsive design, performance (Core Web Vitals), and modern UX best practices.

| Step | Action | Key Notes |
|------|--------|-----------|
| 1 | Read specified files | Or prompt user for files/pattern |
| 2 | Check against all rules | Accessibility, responsive, performance, usability |
| 3 | Output findings | Terse `file:line` format, grouped by file |
| 4 | Skip explanations | Unless fix is non-obvious |

**Key Principles:**
- Semantic HTML first — use native elements over ARIA whenever possible
- Minimum 4.5:1 contrast ratio for normal text, 3:1 for large text
- All interactive elements must be keyboard accessible with visible focus states

## How to Use

1. Read the specified files (or prompt user for files/pattern)
2. Check against all rules below
3. Output findings in terse `file:line` format
4. Group by file, state issue + location, skip explanations unless fix is non-obvious

---

## 1. Accessibility (WCAG 2.2 Compliance)

### 1.1 Semantic HTML (First Rule)

> "If you can use a native HTML element with built-in semantics, use it instead of ARIA."

- Use `<button>` for actions, `<a>`/`<Link>` for navigation (NEVER `<div onClick>` or `<span onClick>`)
- Use semantic containers: `<header>`, `<main>`, `<nav>`, `<footer>`, `<aside>`, `<section>`, `<article>`
- Use heading hierarchy `<h1>`–`<h6>` in logical order (no skipping levels)
- Use `<label>` with `for`/`htmlFor` for form controls
- Use `<table>` for tabular data (not CSS grids for data tables)
- Use `<ul>`/`<ol>` for lists
- Include skip link to main content: `<a href="#main">Skip to content</a>`

### 1.2 ARIA Usage

> "No ARIA is better than bad ARIA" – Sites with ARIA average 41% more errors than those without.

- Only use ARIA when no native HTML equivalent exists (custom widgets like tabs, trees, comboboxes)
- Icon-only buttons MUST have `aria-label`: `<button aria-label="Close">`
- Decorative icons MUST have `aria-hidden="true"`
- Async updates (toasts, validation) MUST use `aria-live="polite"` (reserve `assertive` for critical errors)
- Collapsed sections need `aria-expanded="false"`, expanded need `aria-expanded="true"`
- Hidden elements need `aria-hidden="true"` to exclude from screen readers
- Invalid form fields need `aria-invalid="true"`
- Required fields need `aria-required="true"` or HTML `required`

### 1.3 Images & Media

- All `<img>` MUST have `alt` attribute
- Decorative images: `alt=""` (empty, not missing)
- Informative images: descriptive `alt` text explaining content/purpose
- Complex images (charts, diagrams): provide long description or `aria-describedby`
- Background images with meaning: provide text alternative nearby
- Video: provide captions and transcripts
- Audio: provide transcripts

### 1.4 Color & Contrast

- **Normal text**: minimum 4.5:1 contrast ratio
- **Large text** (18px+ or 14px+ bold): minimum 3:1 contrast ratio
- **UI components** (buttons, inputs, icons): minimum 3:1 contrast ratio
- NEVER rely solely on color to convey meaning (add icons, text, or patterns)
- Test with colorblind simulation tools
- Error states: don't just use red—add icons or text

---

## 2. Focus & Keyboard Navigation

### 2.1 Focus Visibility

- Interactive elements MUST have visible focus indicator
- NEVER use `outline: none` or `outline-none` without replacement
- Use `:focus-visible` over `:focus` (avoids focus ring on click)
- Focus indicator minimum: 2px thick, 3:1 contrast against adjacent colors
- Use `focus-visible:ring-*` (Tailwind) or custom focus styles
- Group related controls with `:focus-within`

### 2.2 Keyboard Accessibility

- ALL interactive elements must be reachable via Tab/Shift+Tab
- Logical tab order matching visual layout
- Custom widgets need keyboard handlers: `onKeyDown`/`onKeyUp`
- Modals/dialogs: trap focus inside, return focus on close
- Collapsible elements: Enter/Space to toggle
- Escape key should close modals, dropdowns, tooltips
- Never use `tabindex` > 0 (disrupts natural order)
- `tabindex="-1"` for programmatically focusable but not tabbable elements
- `tabindex="0"` to make non-interactive elements focusable (when ARIA role requires it)

---

## 3. Forms

### 3.1 Labels & Association

- Every input MUST have a visible `<label>` with `for`/`htmlFor` matching input `id`
- OR wrap input inside `<label>` element
- Placeholder is NOT a substitute for label
- Group related inputs with `<fieldset>` and `<legend>`
- Checkboxes/radios: label + control share single hit target (no dead zones)

### 3.2 Input Attributes

- Use correct `type`: `email`, `tel`, `url`, `number`, `password`, `search`, `date`
- Use `inputmode` for mobile keyboards: `numeric`, `tel`, `email`, `url`, `decimal`
- Use meaningful `name` attributes
- Use `autocomplete` for common fields: `name`, `email`, `tel`, `street-address`, `postal-code`, `cc-number`
- Use `autocomplete="off"` on non-auth fields to avoid password manager triggers
- Disable `spellCheck` on emails, codes, usernames: `spellCheck={false}`

### 3.3 Validation & Error Handling

- NEVER block paste: no `onPaste` + `preventDefault()`
- Show inline errors next to the field, not just at form top
- Focus first error on submit
- Use `aria-invalid="true"` and `aria-describedby` for error messages
- Submit button stays enabled until request starts; show spinner during request
- Warn before navigation with unsaved changes (`beforeunload` or router guard)

### 3.4 Placeholders

- Placeholders should show example format, not instructions
- End with ellipsis: `"Search…"`, `"e.g., john@example.com"`
- Placeholder contrast: minimum 4.5:1 (don't use light gray)

---

## 4. Animation & Motion

### 4.1 Reduced Motion (REQUIRED)

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

- Honor `prefers-reduced-motion` media query
- Provide reduced alternative (fade instead of slide) or disable animation
- Test: Windows Settings → Accessibility → Animation effects OFF
- Test: Mac System Settings → Accessibility → Display → Reduce motion ON

### 4.2 Performance-Safe Animations

- ONLY animate `transform` and `opacity` (GPU-accelerated, no reflows)
- NEVER animate: `width`, `height`, `top`, `left`, `margin`, `padding`, `font-size`
- NEVER use `transition: all` — list properties explicitly: `transition: transform 200ms, opacity 200ms`
- Set correct `transform-origin`
- SVG transforms: use `<g>` wrapper with `transform-box: fill-box; transform-origin: center`

### 4.3 Timing Guidelines

- Micro-interactions (buttons, hovers): 100-200ms
- Small UI changes (tooltips, dropdowns): 200-300ms
- Medium transitions (modals, panels): 300-500ms
- Large movements (page transitions): 500-800ms
- Anything over 1 second feels slow
- Animations should be interruptible — respond to user input mid-animation

---

## 5. Typography

### 5.1 Font Sizes

- Body text: minimum 16px (1rem)
- Mobile: 14-16px minimum
- Use relative units: `rem`, `em`, `%` (not `px` on root `<html>`)
- Allow text to scale to 200% without loss of content (WCAG requirement)

### 5.2 Line Height & Length

- Body text: `line-height: 1.5` minimum (WCAG AA)
- Headings: `line-height: 1.2-1.35`
- Optimal line length: 50-75 characters (66 is sweet spot)
- Mobile: 30-50 characters per line
- Use `max-width: 65ch` or similar for text containers

### 5.3 Typography Characters

- Use proper ellipsis: `…` not `...`
- Use curly quotes: `"` `"` `'` `'` not straight quotes `"` `'`
- Use non-breaking spaces where needed: `10&nbsp;MB`, `⌘&nbsp;K`, brand names
- Loading states end with ellipsis: `"Loading…"`, `"Saving…"`

### 5.4 Number Formatting

- Use `font-variant-numeric: tabular-nums` for number columns, comparisons, counters
- Use `text-wrap: balance` or `text-wrap: pretty` on headings (prevents widows/orphans)

### 5.5 Font Loading

- Limit to 2-3 font families
- Limit to 3 font weights per family
- Use `font-display: swap` for custom fonts
- Provide fallback font stack
- Preload critical fonts: `<link rel="preload" as="font" crossorigin>`

---

## 6. Content Handling

### 6.1 Text Overflow

- Text containers must handle long content:
  - `truncate` / `text-overflow: ellipsis`
  - `line-clamp-*` / `-webkit-line-clamp`
  - `break-words` / `word-break: break-word`
- Flex children need `min-w-0` / `min-width: 0` to allow text truncation
- Test with very long strings (50+ chars without spaces)

### 6.2 Empty States

- Handle empty strings, null, undefined gracefully
- Handle empty arrays — show meaningful empty state, not broken UI
- Anticipate: short, average, and very long user inputs

### 6.3 Content Guidelines

- Active voice: "Install the CLI" not "The CLI will be installed"
- Title Case for headings and buttons (Chicago style)
- Use numerals: "8 deployments" not "eight deployments"
- Specific button labels: "Save API Key" not "Continue" or "Submit"
- Error messages include fix/next step, not just the problem
- Use second person ("you"); avoid first person ("I", "we")
- Use `&` over "and" where space-constrained

---

## 7. Images & Media

### 7.1 Dimensions & Layout Shift

- `<img>` MUST have explicit `width` and `height` attributes (prevents CLS)
- Or use `aspect-ratio` CSS property
- Reserve space with container aspect ratio

### 7.2 Loading Strategy

- Below-fold images: `loading="lazy"`
- Above-fold critical images: `fetchpriority="high"` or framework's `priority`
- Use `decoding="async"` for non-critical images

### 7.3 Optimization

- Use modern formats: WebP, AVIF
- Provide responsive images with `srcset` and `sizes`
- Compress images appropriately
- Use CDN for image delivery

---

## 8. Performance (Core Web Vitals)

### 8.1 LCP (Largest Contentful Paint)

- Target: < 2.5 seconds
- Preload critical resources: `<link rel="preload">`
- Add `<link rel="preconnect">` for CDN/asset domains
- Optimize largest image/text block

### 8.2 CLS (Cumulative Layout Shift)

- Target: < 0.1
- Always specify image/video dimensions
- Reserve space for dynamic content (ads, embeds)
- Use `scroll-margin-top` on heading anchors
- Avoid inserting content above existing content

### 8.3 INP (Interaction to Next Paint)

- Target: < 200ms
- No layout reads during render: avoid `getBoundingClientRect`, `offsetHeight`, `offsetWidth`, `scrollTop` in render path
- Batch DOM reads/writes — don't interleave
- Prefer uncontrolled inputs; controlled inputs must be cheap per keystroke
- Debounce expensive handlers

### 8.4 Lists & Virtualization

- Large lists (>50 items): virtualize with `virtua`, `react-window`, `@tanstack/virtual`, or `content-visibility: auto`
- Paginate or infinite scroll for large datasets

---

## 9. Navigation & State

### 9.1 URL Reflects State

- Filters, tabs, pagination, sort order → URL query params
- Deep-link all stateful UI (if uses `useState`, consider URL sync)
- Use libraries like `nuqs`, `next-usequerystate`, or router state

### 9.2 Links vs Buttons

- Links (`<a>`/`<Link>`) for navigation — supports Cmd/Ctrl+click, middle-click, right-click → "Open in new tab"
- Buttons (`<button>`) for actions that don't navigate

### 9.3 Destructive Actions

- Destructive actions need confirmation modal OR undo window
- NEVER immediate deletion without recovery option
- Show clear warning about consequences

---

## 10. Touch & Mobile Interaction

### 10.1 Touch Targets

- Minimum touch target: 44×44px (Apple HIG) or 48×48dp (Material)
- WCAG 2.2: minimum 24×24 CSS pixels
- Adequate spacing between targets (8px+ gap)

### 10.2 Touch Behavior

- Use `touch-action: manipulation` (prevents double-tap zoom delay)
- Set `-webkit-tap-highlight-color` intentionally (or transparent)
- Use `overscroll-behavior: contain` in modals/drawers/sheets

### 10.3 Drag & Drop

- During drag: disable text selection (`user-select: none`)
- Use `inert` on dragged elements
- Provide keyboard alternative for drag operations (WCAG)

### 10.4 Focus on Mobile

- Use `autoFocus` sparingly — desktop only, single primary input
- Avoid `autoFocus` on mobile (may cause viewport jump)

---

## 11. Layout & Safe Areas

### 11.1 Safe Areas

- Full-bleed layouts need `env(safe-area-inset-*)` for notches, home indicators
- Bottom fixed elements: `padding-bottom: env(safe-area-inset-bottom)`

### 11.2 Overflow Management

- Avoid unwanted scrollbars: check for content overflow
- Use `overflow-x: hidden` carefully (only when justified)
- Prefer Flexbox/Grid over JavaScript measurement for layout

### 11.3 Responsive Design

- Mobile-first approach: start with mobile styles, add larger breakpoints
- Use fluid typography: `clamp()` for font sizes
- Use container queries for component-level responsiveness
- Test at common breakpoints: 320px, 375px, 768px, 1024px, 1440px

---

## 12. Dark Mode & Theming

### 12.1 System Integration

- Use `color-scheme: dark` on `<html>` for dark themes (fixes scrollbar, inputs, form controls)
- Match `<meta name="theme-color">` to page background
- Native `<select>`: set explicit `background-color` and `color` (Windows dark mode fix)

### 12.2 User Preference

- Honor `prefers-color-scheme` media query
- Provide manual toggle that persists preference
- Ensure all UI elements work in both modes

---

## 13. Internationalization (i18n)

### 13.1 Locale-Aware Formatting

- Dates/times: use `Intl.DateTimeFormat`, not hardcoded formats
- Numbers/currency: use `Intl.NumberFormat`, not hardcoded formats
- Relative time: use `Intl.RelativeTimeFormat`

### 13.2 Language Detection

- Detect language via `Accept-Language` header or `navigator.languages`
- NEVER use IP geolocation for language detection

### 13.3 RTL Support

- Use logical CSS properties: `margin-inline-start` not `margin-left`
- Set `dir="rtl"` on `<html>` for RTL languages
- Test layout in RTL mode

---

## 14. Hydration Safety (SSR/SSG)

### 14.1 Controlled Inputs

- Inputs with `value` prop MUST have `onChange` handler
- Or use `defaultValue` for uncontrolled inputs

### 14.2 Client-Only Content

- Date/time rendering: guard against hydration mismatch (server vs client timezone)
- Use `suppressHydrationWarning` only where truly needed
- Dynamic content based on `window`/`localStorage`: render client-side only

---

## 15. Interactive States

### 15.1 Hover & Active States

- Buttons and links MUST have `hover:` state (visual feedback)
- Interactive states should increase contrast/prominence
- Hover → Active → Focus progression should be visually clear

### 15.2 Disabled States

- Use `disabled` attribute, not just styling
- Disabled elements: reduced opacity (0.5-0.6), `cursor: not-allowed`
- Consider `aria-disabled="true"` if element should remain focusable

---

## Anti-Patterns Checklist

**Flag these immediately:**

| Pattern                                                    | Issue                                             |
| ---------------------------------------------------------- | ------------------------------------------------- |
| `user-scalable=no` or `maximum-scale=1`                    | Disables zoom — accessibility violation           |
| `onPaste` + `preventDefault()`                             | Blocks paste — UX hostile                         |
| `transition: all`                                          | Performance issue — list properties               |
| `outline: none` / `outline-none` without focus replacement | Removes focus indicator — accessibility violation |
| `<div onClick>` or `<span onClick>`                        | Should be `<button>` or `<a>`                     |
| `<img>` without `width`/`height`                           | Causes layout shift (CLS)                         |
| `<img>` without `alt`                                      | Missing alt text — accessibility violation        |
| Form inputs without `<label>`                              | Missing label — accessibility violation           |
| Icon buttons without `aria-label`                          | Screen reader can't identify action               |
| Hardcoded date/number formats                              | Should use `Intl.*` APIs                          |
| `autoFocus` without clear justification                    | May cause issues on mobile                        |
| Large arrays with `.map()` without virtualization          | Performance issue for 50+ items                   |
| `tabindex` > 0                                             | Disrupts natural tab order                        |
| Color-only indicators                                      | Fails colorblind users                            |
| Placeholder as label                                       | Label disappears on input                         |

---

## Output Format

Group by file. Use `file:line` format (VS Code/IDE clickable). Terse findings.

```text
## src/components/Button.tsx

src/components/Button.tsx:42 - icon button missing aria-label
src/components/Button.tsx:18 - input lacks associated label
src/components/Button.tsx:55 - animation missing prefers-reduced-motion check
src/components/Button.tsx:67 - transition: all → list specific properties
src/components/Button.tsx:89 - div with onClick → use <button>

## src/components/Modal.tsx

src/components/Modal.tsx:12 - missing overscroll-behavior: contain
src/components/Modal.tsx:34 - "..." → use "…" (proper ellipsis)
src/components/Modal.tsx:78 - no focus trap for modal dialog

## src/components/Card.tsx

✓ No issues found

## Summary

- 8 accessibility issues
- 3 performance issues
- 2 UX issues
- Priority: Fix accessibility issues first (WCAG compliance)
```

State issue + location. Skip explanation unless fix non-obvious. No preamble.

---

## References

- [WCAG 2.2 Guidelines](https://www.w3.org/WAI/WCAG22/quickref/)
- [WAI-ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/)
- [MDN Accessibility Guide](https://developer.mozilla.org/en-US/docs/Web/Accessibility)
- [Core Web Vitals](https://web.dev/vitals/)
- [prefers-reduced-motion](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion)

## Related EasyPlatform Docs

- [SCSS Styling Guide](docs/claude/scss-styling-guide.md) - Angular/BEM patterns, platform-specific SCSS conventions
- [Frontend Patterns](docs/claude/frontend-patterns.md) - Angular component hierarchy, state management


## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
