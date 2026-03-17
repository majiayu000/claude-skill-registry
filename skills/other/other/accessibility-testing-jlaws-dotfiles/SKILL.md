---
name: accessibility-testing
description: "Audit and test web accessibility with automated scanning, manual screen reader testing, and WCAG 2.2 remediation. Use when auditing accessibility, fixing WCAG violations, testing with screen readers, or implementing accessible components."
---

# Accessibility Testing

## Automated Testing Setup

**axe-core**: Use `AxePuppeteer` with `.withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])` for automated audits. Exclude non-audited regions with `.exclude()`.

**jest-axe**: Use `toHaveNoViolations()` matcher in component tests.

### CLI Tools

```bash
npx @axe-core/cli https://example.com
npx pa11y https://example.com --standard WCAG2AA --threshold 0
lighthouse https://example.com --only-categories=accessibility
```

**CI/CD**: Run `npx pa11y` against localhost in CI. Gate PRs on zero WCAG2AA violations.

## Manual Screen Reader Testing

### Testing Priority

```
Minimum: NVDA + Firefox (Win), VoiceOver + Safari (Mac), VoiceOver + Safari (iOS)
Full:    + JAWS + Chrome (Win), TalkBack + Chrome (Android)
```

### VoiceOver (macOS) Commands

```
VO = Ctrl + Option
Toggle:            Cmd + F5
Next/Prev element: VO + Right/Left Arrow
Enter/Exit group:  VO + Shift + Down/Up
Read all:          VO + A
Activate:          VO + Space
Rotor:             VO + U (navigate by headings, links, forms, landmarks)
Next heading:      VO + Cmd + H
Next form control: VO + Cmd + J
Next link:         VO + Cmd + L
```

### NVDA (Windows) Commands

```
NVDA modifier = Insert
Say all:           NVDA + Down Arrow
Elements list:     NVDA + F7
Quick keys (browse mode):
  H/Shift+H  Heading next/prev    D/Shift+D  Landmark next/prev
  F           Next form field      B           Next button
  K           Next link            T           Next table
Table nav:         Ctrl + Alt + Arrows
Mode switch:       NVDA + Space (browse <-> focus)
```

### JAWS Quick Keys

```
H  Next heading    T  Next table      F  Next form field
B  Next button     ;  Next landmark   G  Next graphic
Insert + F7  Link list    Insert + F6  Heading list
```

### Test Script (All Screen Readers)

1. **Page load** - Title announced? Main landmark found? Skip link works?
2. **Landmark nav** - All main areas reachable? Properly labeled?
3. **Heading nav** - Logical structure? All sections discoverable?
4. **Form testing** - Labels read? Required fields announced? Errors announced? Focus moved to error?
5. **Interactive elements** - Each announces role + state? Activates with Enter/Space?
6. **Dynamic content** - Updates announced? Modal traps focus? Focus returns on close?

### Common Screen Reader Fixes

```html
<!-- Button without visible text -->
<button aria-label="Close dialog"><svg aria-hidden="true">...</svg></button>

<!-- Dynamic content not announced -->
<div role="status" aria-live="polite">New results loaded</div>

<!-- Form error not read -->
<input type="email" aria-invalid="true" aria-describedby="email-error">
<span id="email-error" role="alert">Invalid email</span>
```

## WCAG 2.2 Audit Checklist

### Critical Violations (Blockers)

- [ ] All functional images have alt text; decorative images `alt=""`
- [ ] All interactive elements keyboard accessible (no traps)
- [ ] All form inputs have associated labels
- [ ] Color contrast: 4.5:1 text, 3:1 large text/UI components
- [ ] No auto-playing media without controls

### Serious Violations

- [ ] Skip to main content link present
- [ ] Page titles unique and descriptive
- [ ] Heading hierarchy logical (no skipped levels)
- [ ] ARIA landmarks defined (main, nav, etc.)
- [ ] Focus indicator visible on all elements (3:1 contrast)
- [ ] `<html lang="en">` attribute set

### Forms & Interaction

- [ ] Error messages identify field and describe problem
- [ ] Required fields indicated (not color-only)
- [ ] `aria-invalid="true"` + `aria-describedby` on error fields
- [ ] Live regions: `role="status"` (polite) / `role="alert"` (assertive)
- [ ] Modal dialogs: `role="dialog"`, `aria-modal="true"`, focus trap, Esc to close

### Responsive & Motion

- [ ] Content reflows at 320px (no horizontal scroll)
- [ ] Text resizes to 200% without loss
- [ ] `@media (prefers-reduced-motion: reduce)` disables animations
- [ ] `@media (prefers-contrast: high)` increases contrast

## Remediation Patterns

**Keyboard nav widgets**: Custom interactive widgets need: `tabindex="0"`, `role`, `aria-expanded`, and keydown handler for Enter/Space (activate), Escape (close), Arrow keys (navigate).

**Focus management for modals**: Save `document.activeElement` before opening. Trap Tab/Shift+Tab within modal's focusable elements. Restore focus on close.

**Tab interface**: Use `role="tablist"`/`role="tab"`/`role="tabpanel"` with `aria-selected`, `aria-controls`, `aria-labelledby`. Arrow keys navigate tabs, Home/End jump to first/last.

**Color contrast**: Use `@media (prefers-contrast: high)` and visible `:focus` outlines (3px solid, 2px offset).

## Cross-References

- **frontend:design-system-patterns** -- accessible headless components, ARIA defaults
- **frontend:form-patterns** -- accessible forms, labels, error messages, aria-describedby
- **frontend:web-animation-patterns** -- reduced-motion preferences, prefers-reduced-motion
