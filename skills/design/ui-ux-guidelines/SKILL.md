---
name: ui-ux-guidelines
description: Implementation details for accessible, performant interfaces. Use alongside vercel-design-guidelines for detailed technical guidance on interactions, animations, and forms.
allowed-tools: Read, Grep, Glob, Edit
---

# UI/UX Implementation Details

> **Note:** For high-level design rules (hit targets, focus rings, contrast, etc.), defer to `vercel-design-guidelines` which fetches live standards from Vercel. This skill provides implementation-specific details.

## Interactions

### Keyboard & Focus

- **MUST**: Full keyboard support per [WAI-ARIA APG](https://www.w3.org/WAI/ARIA/apg/patterns/)
- **MUST**: Manage focus (trap, move, return) per APG patterns
- **MUST**: Group focus with `:focus-within` where appropriate

### Touch & Input

- **MUST**: `touch-action: manipulation` to prevent double-tap zoom
- **MUST**: Set `-webkit-tap-highlight-color` to match design
- **MUST**: Mobile `<input>` font-size ≥16px to prevent iOS zoom, or use:
  ```html
  <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, viewport-fit=cover">
  ```

### Form Behavior

- **MUST**: Hydration-safe inputs (no lost focus/value)
- **NEVER**: Block paste in `<input>`/`<textarea>`
- **MUST**: Enter submits text input; in `<textarea>`, Cmd/Ctrl+Enter submits
- **MUST**: Keep submit enabled until request starts; use idempotency key
- **MUST**: Allow submitting incomplete forms to surface validation
- **MUST**: Errors inline next to fields; on submit, focus first error
- **MUST**: `autocomplete` + meaningful `name`; correct `type` and `inputmode`
- **SHOULD**: Disable spellcheck for emails/codes/usernames
- **SHOULD**: Placeholders end with ellipsis and show example (e.g., `sk-012345...`)
- **MUST**: Warn on unsaved changes before navigation
- **MUST**: Compatible with password managers & 2FA
- **MUST**: Trim values to handle text expansion trailing spaces
- **MUST**: No dead zones on checkboxes/radios; label+control share hit target

### State & Navigation

- **MUST**: URL reflects state (filters/tabs/pagination). Prefer [nuqs](https://nuqs.dev)
- **MUST**: Back/Forward restores scroll
- **MUST**: Links use `<a>`/`<Link>` (support Cmd/Ctrl/middle-click)

### Feedback

- **SHOULD**: Optimistic UI with reconciliation; on failure show error or Undo
- **MUST**: Confirm destructive actions or provide Undo window
- **MUST**: Use polite `aria-live` for toasts/inline validation
- **SHOULD**: Ellipsis for follow-ups ("Rename...") and loading ("Saving...")

### Touch/Drag

- **MUST**: Delay first tooltip; subsequent peers no delay
- **MUST**: `overscroll-behavior: contain` in modals/drawers
- **MUST**: During drag, disable text selection and set `inert` on dragged element

---

## Animation

- **SHOULD**: Prefer CSS > Web Animations API > JS libraries
- **MUST**: Animations are interruptible and input-driven (avoid autoplay)
- **MUST**: Correct `transform-origin` (motion starts where it "physically" should)

### Cross-Browser

- **MUST**: Apply CSS transforms to SVG children (`<g>`), not parent `<svg>`
- **MUST**: Set `transform-box: fill-box` and `transform-origin: center` on SVG
- **SHOULD**: Use `translateZ(0)` or `will-change: transform` for text anti-aliasing artifacts

---

## Layout

- **SHOULD**: Optical alignment; adjust by +/-1px when perception beats geometry
- **MUST**: Deliberate alignment to grid/baseline/edges
- **SHOULD**: Balance icon/text lockups (stroke/weight/size/spacing/color)
- **MUST**: Verify mobile, laptop, ultra-wide (simulate at 50% zoom)
- **MUST**: Respect safe areas (`env(safe-area-inset-*)`)
- **MUST**: Avoid unwanted scrollbars; fix overflows

---

## Content & Accessibility

- **SHOULD**: Inline help first; tooltips last resort
- **MUST**: Skeletons mirror final content (avoid layout shift)
- **MUST**: `<title>` matches current context
- **MUST**: No dead ends; always offer next step/recovery
- **MUST**: Design empty/sparse/dense/error states
- **SHOULD**: Curly quotes (" "); avoid widows/orphans
- **MUST**: Tabular numbers for comparisons (`font-variant-numeric: tabular-nums`)
- **MUST**: Redundant status cues (not color-only); icons have text labels
- **MUST**: Use ellipsis character `...` (not `...`)
- **MUST**: `scroll-margin-top` on headings; include "Skip to content" link
- **MUST**: Resilient to user-generated content (short/avg/very long)
- **MUST**: Locale-aware dates/times/numbers/currency
- **MUST**: Use non-breaking spaces: `10&nbsp;MB`, `Cmd&nbsp;+&nbsp;K`
- **MUST**: Detect language via `Accept-Language` header, NOT IP geolocation

---

## Performance

- **SHOULD**: Test iOS Low Power Mode and macOS Safari
- **MUST**: Measure reliably (disable extensions that skew runtime)
- **MUST**: Track and minimize re-renders (React DevTools/React Scan)
- **MUST**: Profile with CPU/network throttling
- **MUST**: Batch layout reads/writes; avoid reflows/repaints
- **MUST**: Mutations complete in <500ms
- **SHOULD**: Prefer uncontrolled inputs; make controlled loops cheap
- **MUST**: Virtualize large lists ([virtua](https://github.com/inokawa/virtua)) or `content-visibility: auto`
- **MUST**: Preload only above-the-fold images; lazy-load rest
- **MUST**: Prevent CLS from images (explicit dimensions)
- **SHOULD**: `<link rel="preconnect">` for asset/CDN domains
- **SHOULD**: Preload critical fonts; subset via `unicode-range`
- **SHOULD**: Move expensive work to Web Workers

---

## Design

- **SHOULD**: Layered shadows (ambient + direct)
- **SHOULD**: Crisp edges via semi-transparent borders + shadows
- **SHOULD**: Nested radii: child <= parent; concentric
- **SHOULD**: Hue consistency: tint borders/shadows/text toward bg hue
- **MUST**: Accessible charts (color-blind-friendly palettes)
- **MUST**: Increase contrast on `:hover`/`:active`/`:focus`
- **SHOULD**: Set `<meta name="theme-color">` to match page background
- **MUST**: Set `color-scheme: dark` on `<html>` in dark themes
- **MUST**: On Windows, set explicit `background-color` and `color` on `<select>`
- **SHOULD**: Avoid gradient banding (use masks when needed)

---

## Common Violations

### Blocking paste
```tsx
// Bad
<input onPaste={(e) => e.preventDefault()} />

// Good
<input type="email" autoComplete="email" />
```

### Non-semantic button
```tsx
// Bad
<div onClick={handleClick}>Click me</div>

// Good
<button onClick={handleClick}>Click me</button>
```

### Windows select dark mode
```tsx
// Bad
<select><option>Option 1</option></select>

// Good
<select className="bg-white dark:bg-gray-900 text-black dark:text-white">
  <option>Option 1</option>
</select>
```

---

## References

- [WAI-ARIA APG Patterns](https://www.w3.org/WAI/ARIA/apg/patterns/)
- [APCA Contrast Calculator](https://apcacontrast.com/)
- [nuqs - URL State Management](https://nuqs.dev)
- [virtua - List Virtualization](https://github.com/inokawa/virtua)
