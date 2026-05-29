---
name: wcag-accessibility
description: UI must comply with WCAG 2.2 Level AA, as required by the European Accessibility Act (EN 301 549). Do not deviate without deliberate justification. Disabled UI elements are explicitly exempt from colour contrast requirements. Use when designing, building, or reviewing any user-facing interface for accessibility compliance.
metadata:
  priority: 9
  docs:
    - "https://www.w3.org/TR/WCAG22/"
    - "https://www.etsi.org/deliver/etsi_en/301500_302000/301549/03.02.01_60/en_301549v030201p.pdf"
  pathPatterns:
    - "**/*.tsx"
    - "**/*.jsx"
    - "**/*.vue"
    - "**/*.svelte"
    - "**/*.html"
    - "**/*.css"
    - "**/*.scss"
    - "components/**"
    - "src/components/**"
    - "design-system/**"
  promptSignals:
    phrases:
      - "accessibility"
      - "wcag"
      - "a11y"
      - "contrast"
      - "contrast ratio"
      - "screen reader"
      - "aria"
      - "focus"
      - "focus visible"
      - "keyboard navigation"
      - "keyboard"
      - "colour blind"
retrieval:
  aliases:
    - wcag
    - accessibility
    - a11y
    - EN 301 549
    - European Accessibility Act
    - contrast
    - screen reader
    - aria
  intents:
    - check accessibility compliance
    - fix contrast ratio
    - add keyboard navigation
    - make component screen-reader friendly
    - meet EU accessibility requirements
  examples:
    - is this colour contrast accessible
    - make this component keyboard navigable
    - check this UI against WCAG
    - does this meet EU accessibility standards
---

# WCAG Accessibility (EN 301 549 / European Standard)

## The Standard

The **European Accessibility Act (EAA)** requires digital products and services in the EU to meet **EN 301 549**, which references **WCAG 2.2 Level AA** as the technical baseline. This is not optional — it is a legal requirement for products operating in the EU market.

**Default: always build to WCAG 2.2 AA.** Deviating requires explicit, documented justification. Do not skip accessibility requirements because of timeline pressure or design preference.

WCAG 2.2 AA organises requirements under four principles: **Perceivable, Operable, Understandable, Robust**.

---

## Perceivable

Users must be able to perceive all content and UI components.

### Colour Contrast
| Context | Minimum ratio | Enhanced (AAA) |
|---|---|---|
| Normal text (< 18pt / < 14pt bold) | **4.5 : 1** | 7 : 1 |
| Large text (≥ 18pt / ≥ 14pt bold) | **3 : 1** | 4.5 : 1 |
| UI components and graphical objects | **3 : 1** | — |

**Disabled elements are exempt.** WCAG explicitly excludes inactive UI components from contrast requirements (WCAG 1.4.3 exception). A disabled button may use low-contrast text — this is intentional and correct, as it communicates the unavailable state.

Do not use colour as the only means of conveying information (e.g. a red border alone to indicate an error — add an icon or text label).

### Text Alternatives
- Every meaningful image needs `alt` text describing its content or function
- Decorative images use `alt=""` so screen readers skip them
- Icons used as buttons need an accessible label: `aria-label` or visually hidden text
- Charts and data visualisations need a text summary or data table alternative

### Captions and Transcripts
- Video content needs captions
- Audio-only content needs a transcript

---

## Operable

Users must be able to operate all UI components.

### Keyboard Navigation
All interactive elements must be reachable and operable by keyboard alone.

- Every button, link, input, and control must receive focus via Tab
- Focus order must follow the visual reading order of the page
- No keyboard traps — users must be able to navigate away from any component
- Modal dialogs must trap focus inside while open, and return focus to the trigger element on close

### Focus Visibility
A visible focus indicator is required on every interactive element (WCAG 2.2 strengthens focus visibility requirements).

```css
/* Minimum: do not remove focus outline without a replacement */
:focus-visible {
  outline: 2px solid var(--color-focus);
  outline-offset: 2px;
}
```

Never use `outline: none` without providing a custom focus style. The focus ring is not a design problem to eliminate — it is a navigation tool.

### Touch Target Size
Interactive elements on touch devices must be at least **24×24px** (WCAG 2.2) — **44×44px** is the recommended comfortable minimum (Apple HIG, Material Design). Small icon buttons need padding to reach this size even if the visual icon is smaller.

### No Seizure Triggers
Nothing on screen should flash more than 3 times per second.

### Skip Links
Pages with repeated navigation must provide a "Skip to main content" link as the first focusable element, so keyboard users can bypass navigation on every page.

---

## Understandable

Users must be able to understand the content and how the UI works.

### Language
- Set `lang` attribute on the `<html>` element: `<html lang="fi">` or `<html lang="en">`
- Mark inline content in a different language with `lang` on that element

### Labels and Instructions
- Every form input must have a visible label — not just a placeholder (placeholders disappear on input)
- Required fields must be indicated — do not rely on colour alone; add an asterisk and a legend
- Error messages must be associated with their input via `aria-describedby`

### Predictability
- Components that look the same must behave the same (see Consistency and Standards)
- Navigation must appear in the same location across pages
- Opening a new tab or window must be communicated in advance

### Error Identification
- Form validation errors must identify which field failed
- Errors must be described in text — not only by colour or icon

---

## Robust

Content must be interpreted reliably by assistive technologies.

### Semantic HTML
Use the correct HTML element for the job. Semantics convey role, state, and structure to screen readers for free.

```html
<!-- Correct -->
<button>Save</button>
<nav aria-label="Main navigation">...</nav>
<h1>Page title</h1>

<!-- Wrong — requires manual ARIA to replicate what the element provides natively -->
<div onclick="save()">Save</div>
<div class="nav">...</div>
<div class="heading">Page title</div>
```

### ARIA — Use Sparingly
ARIA supplements HTML semantics where native elements fall short. It does not fix broken HTML.

**Rule: no ARIA is better than incorrect ARIA.** Incorrect ARIA actively breaks screen reader output.

Required patterns:
- `aria-label` or `aria-labelledby` for components with no visible text label
- `aria-expanded` on toggles, accordions, and dropdowns
- `aria-live` regions for dynamic content updates (toast notifications, search results)
- `role="dialog"` with `aria-modal="true"` on modal overlays
- `aria-current="page"` on the active navigation item

### Status Messages
Dynamic updates (success toasts, loading states, error counts) must be announced to screen readers via `aria-live` or `role="status"` — they will not be announced automatically unless the focused element changes.

---

## The Disabled Element Exception

WCAG 1.4.3 explicitly states: *"Text or images of text that are part of an inactive user interface component… have no contrast requirement."*

This means:
- Disabled buttons, inputs, and links **may** use low-contrast text and colours
- The visual dimming of disabled states is both correct and compliant
- Do not add artificial contrast to disabled elements — the reduced contrast communicates "this is unavailable"

---

## Review Checklist

| Area | Check |
|---|---|
| Contrast | All active text ≥ 4.5:1 (normal) or 3:1 (large/UI) |
| Contrast | Disabled elements exempt — intentionally low contrast is fine |
| Colour | Colour is never the only information carrier |
| Keyboard | All interactive elements reachable and operable by keyboard |
| Focus | Visible focus indicator on every interactive element |
| Touch | Interactive targets ≥ 44×44px on touch surfaces |
| Labels | Every input has a visible label (not just placeholder) |
| Errors | Validation errors identify the field and describe the problem in text |
| HTML | Semantic elements used correctly; ARIA only where needed |
| Language | `lang` attribute set on `<html>` |
| Skip link | "Skip to main content" as first focusable element |
| Live regions | Dynamic updates announced via `aria-live` or `role="status"` |
