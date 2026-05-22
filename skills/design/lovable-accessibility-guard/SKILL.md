---
name: lovable-accessibility-guard
description: "Ensure all Lovable UI generations meet WCAG 2.1 AA/AAA accessibility standards with contrast, semantic HTML, keyboard navigation, and screen reader support."
homepage: https://lovable.dev
user-invocable: true
disable-model-invocation: false
metadata: {"openclaw":{"emoji":"♿"}}
---

# Lovable Accessibility Guard

## Purpose

Ensure every Lovable-generated interface meets WCAG 2.1 AA (or AAA) standards. Use in **enforce** mode to bake accessibility into new generations, or **audit** mode to review and fix existing output. Covers contrast, semantic HTML, keyboard navigation, screen reader support, motion safety, and touch targets.

> **Platform context**: Lovable generates React + TypeScript + Tailwind CSS + shadcn/ui apps. shadcn/ui components use Radix UI primitives which provide built-in ARIA attributes and keyboard handling. This skill ensures those defaults are preserved and gaps are filled.

## Inputs

| Parameter | Required | Values                                                        | Default |
|-----------|----------|---------------------------------------------------------------|---------|
| `level`   | yes      | AA, AAA                                                       | —       |
| `mode`    | yes      | enforce, audit                                                | —       |
| `focus`   | no       | contrast, semantics, keyboard, screenreader, motion, touch, all | all   |

## Workflow

### 1. Color Contrast Verification

Check all text/background pairings against WCAG thresholds:

| Element Type                        | AA Ratio | AAA Ratio |
|-------------------------------------|----------|-----------|
| Body text (≤1rem, regular weight)   | 4.5:1    | 7:1       |
| Large text (≥1.25rem bold, ≥1.5rem) | 3:1      | 4.5:1     |
| UI components & graphical objects   | 3:1      | 3:1       |
| Placeholder text on input bg        | 4.5:1    | 7:1       |
| Disabled elements                   | Exempt (must be visually distinguishable) | — |

**Fix method**: Adjust text color darker (light bg) or lighter (dark bg), preserving hue. Stay within brand palette when possible. If no in-palette color meets requirements, shift lightness only.

### 2. Semantic HTML Structure

Ensure proper document structure:

- **Heading hierarchy**: One `<h1>` per page. No skipped levels. Heading level = content hierarchy, not visual size.
- **Landmarks**: `<header>`, `<nav aria-label="...">`, `<main>`, `<aside>`, `<footer>`. One `<main>` per page.
- **Lists**: Related items (nav links, feature lists, grids) use `<ul>` or `<ol>`, not `<div>` stacks.
- **Forms**: Every input has an associated `<label>` via `for`/`id`. Grouped fields use `<fieldset>` + `<legend>`.
- **Links vs buttons**: `<a>` for navigation, `<button>` for actions. Never `<div onClick>`.
- **Tables**: Data tables use `<table>`, `<thead>`, `<tbody>`, `<th scope="col|row">`. Never use tables for layout.

### 3. Keyboard Navigation

- **Tab order**: All interactive elements reachable via Tab in logical reading order. No `tabindex > 0`.
- **Focus indicator**: Every focusable element has visible focus: `outline: 2px solid {accent}; outline-offset: 2px`. Never `outline: none` without a custom replacement.
- **Skip link**: First focusable element = "Skip to main content" link. Visually hidden, visible on focus. Links to `<main id="main-content">`.
- **Modal focus trap**: Focus moves inside modal on open. Tab cycles within. Escape closes. Focus returns to trigger.
- **Dropdowns**: Arrow Up/Down navigates. Enter/Space selects. Escape closes. Home/End jumps to first/last.
- **Custom components**: Follow WAI-ARIA Authoring Practices for roles and keyboard patterns.

> **Note**: shadcn/ui uses Radix UI which provides focus trapping and keyboard navigation for Dialog, DropdownMenu, Select, etc. Verify these defaults are not overridden.

### 4. Screen Reader Support

- **Images**: All `<img>` have `alt`. Meaningful: descriptive alt. Decorative: `alt=""`. Complex: `alt` + `aria-describedby`.
- **Icon-only buttons**: Must have `aria-label`. Example: `<button aria-label="Close dialog">✕</button>`.
- **Dynamic content**: Use `aria-live="polite"` (non-urgent) or `aria-live="assertive"` (critical alerts).
- **Form errors**: Errors associated via `aria-describedby`. Error state: `aria-invalid="true"`.
- **Toggle states**: `aria-checked`, `aria-expanded`, `aria-pressed`, `aria-selected` as appropriate.
- **Loading states**: `aria-busy="true"` + `aria-label="Loading {content}"`. Announce completion via `aria-live`.
- **Page title**: Unique, descriptive `<title>` per page.

### 5. Motion and Sensory Safety

- **Reduced motion**: All animations wrapped in `@media (prefers-reduced-motion: no-preference)`. Fallback: instant state changes.
- **Color independence**: Never convey information by color alone. Add text, icons, or patterns alongside color.
- **Flash threshold**: No content flashes more than 3 times per second.
- **Auto-play**: No auto-playing video/audio. If required, provide visible pause/stop within 3 seconds. Mute by default.

### 6. Responsive and Touch Accessibility

- **Touch targets**: All interactive elements ≥ 44px × 44px (WCAG 2.5.5).
- **Text scaling**: UI functional at 200% browser zoom. No horizontal scrolling at 200% on ≥320px viewport.
- **Reflow**: At 320px CSS width, all content reflows to single column. Exceptions: maps, data tables, code blocks.
- **Text spacing**: UI intact when line-height=1.5×, paragraph spacing=2×, letter-spacing=0.12×, word-spacing=0.16×.

## Output Format

- **Enforce mode**: Accessibility constraint instructions formatted as a Lovable prompt prefix. Prepend to any generation prompt.
- **Audit mode**: Structured checklist report listing specific issues with exact fix instructions for each.

## Guardrails

- Never remove focus indicators without providing a visible replacement.
- `aria-hidden="true"` must never be on focusable elements.
- Never rely on color alone for meaning — always pair with text, icon, or pattern.
- Never create keyboard traps — every area must be escapable via Tab or Escape.
- Never auto-play audio/video without immediate keyboard-accessible pause controls.
- Contrast fixes must stay within brand palette when possible.
- Accessibility fixes must not degrade visual design. Goal: inclusive design, not compromise.

## Failure Handling

| Problem | Follow-up Prompt |
|---------|-----------------|
| Contrast failure | "The {element} text (#{text_hex}) on (#{bg_hex}) has {ratio}:1, needs {required}:1. Change to #{suggested_hex} for {new_ratio}:1 within brand palette." |
| Missing semantics | "Replace div-based nav with `<nav aria-label='Main navigation'>`. Wrap content in `<main id='main-content'>`. Add `<footer>`. Fix heading hierarchy: change h3 to h2." |
| Missing focus styles | "Add `outline: 2px solid {accent}; outline-offset: 2px` to all interactive elements. Add skip-to-content link as first element in body." |
| Missing ARIA | "Add `aria-label` to icon-only buttons. Add `alt` to images. Add `aria-live='polite'` to notifications. Add `aria-expanded` to accordions." |
| No reduced motion | "Wrap animations in `@media (prefers-reduced-motion: no-preference)`. Add fallback setting animation-duration and transition-duration to 0.01ms." |

## Examples

### Example 1: Enforce AA on New SaaS Dashboard

**Input**: `level=AA`, `mode=enforce`, `focus=all`

**Prompt prefix for Lovable**:
```
ACCESSIBILITY REQUIREMENTS (prepend to your generation):

1. CONTRAST: All body text meets 4.5:1 against background. Large text (≥20px bold) meets 3:1. All UI controls (buttons, inputs, icons) meet 3:1 against adjacent colors.

2. STRUCTURE: Use semantic HTML — one h1, proper heading hierarchy, <nav>, <main>, <footer>. Form inputs have <label> elements. Use <button> for actions, <a> for navigation.

3. KEYBOARD: All interactive elements focusable via Tab. Add visible focus ring (2px solid outline, 2px offset). Include "Skip to main content" link. Modal dialogs trap focus and close with Escape.

4. SCREEN READER: Add alt text to images, aria-label to icon buttons, aria-live regions for dynamic content, aria-invalid for form errors.

5. MOTION: Wrap animations in @media (prefers-reduced-motion: no-preference). No auto-playing media.

6. TOUCH: Interactive targets minimum 44px × 44px. Responsive layout reflows at 320px.
```

### Example 2: Audit Existing Landing Page

**Input**: `level=AAA`, `mode=audit`, `focus=contrast,keyboard`

**Audit output format**:
```
ACCESSIBILITY AUDIT — WCAG 2.1 AAA

❌ CONTRAST ISSUES:
1. Hero subtitle (#9ca3af) on white (#ffffff): 2.8:1 (needs 7:1). Fix: Change to #4b5563 (7.3:1).
2. CTA button text (#ffffff) on (#8b5cf6): 3.1:1 (needs 4.5:1 for AAA body text). Fix: Use #1e1b4b on (#c4b5fd) or darken button to (#6d28d9).

❌ KEYBOARD ISSUES:
1. Card components use <div onClick> — not focusable. Fix: Change to <button> or add tabindex="0" + onKeyDown handler.
2. No skip-to-content link. Fix: Add as first element in <body>.
3. Mobile menu has no focus trap. Fix: Trap focus when open, close on Escape.

✅ PASSING:
- Heading hierarchy correct (h1 → h2 → h3)
- Form inputs have labels
- Navigation uses <nav> landmark
```

## Security & Privacy

This skill generates text prompts only. It does not access external endpoints, transmit data, or execute code. All output is prompt text intended for the Lovable.dev platform.

## Trust Statement

This skill contains no executable scripts. It produces Lovable-compatible prompt instructions and audit checklists for WCAG compliance. It does not access the filesystem, network, or any external service.
