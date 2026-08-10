---
name: accessibility-testing
description: Audit web interfaces against WCAG 2.1 AA/AAA standards, identify violations, and produce actionable remediation reports with code fixes. Use when the user requests accessibility testing or provides relevant inputs for this workflow.
license: MIT
metadata:
  author: AI Agent Skills Community
  version: 1.0.0
---

# Accessibility Testing

This skill enables the agent to perform thorough accessibility audits of web pages and components against the Web Content Accessibility Guidelines (WCAG) 2.1 at AA and AAA conformance levels. The agent identifies violations across four principles — Perceivable, Operable, Understandable, Robust — and generates structured compliance reports with specific code fixes. It covers automated checks (color contrast, missing alt text, ARIA misuse), semi-automated checks (keyboard navigation flows, focus management), and manual check guidance (screen reader announcements, cognitive load).

## Workflow

1. **Define Audit Scope and Conformance Target**: Determine which pages, components, or user flows to audit, and whether the target is WCAG 2.1 AA (most common legal requirement) or AAA (highest conformance). Identify the assistive technologies to consider: screen readers (NVDA on Windows, VoiceOver on macOS/iOS, TalkBack on Android), keyboard-only navigation, and magnification tools.

2. **Run Automated Scans**: Execute automated accessibility analysis using axe-core or Lighthouse. These tools detect approximately 30-40% of WCAG violations automatically, including missing alt attributes, insufficient color contrast ratios, missing form labels, duplicate IDs, invalid ARIA roles, and missing document language. Capture each violation with its WCAG criterion reference (e.g., 1.4.3 Contrast Minimum), severity (critical, serious, moderate, minor), the affected HTML element, and the CSS selector path.

3. **Perform Keyboard Navigation Testing**: Manually trace every interactive flow using only Tab, Shift+Tab, Enter, Space, Escape, and arrow keys. Verify that focus order matches visual order, that focus indicators are visible (minimum 2px outline with 3:1 contrast), that modal dialogs trap focus correctly, and that no keyboard traps exist. Document any flow where a keyboard user cannot complete a task that a mouse user can.

4. **Test with Screen Readers**: Navigate the page with at least one screen reader to verify that all content is announced correctly. Confirm that images have meaningful alt text (or `alt=""` for decorative images), that headings form a logical hierarchy (no skipped levels), that landmarks (`<nav>`, `<main>`, `<aside>`) are present, and that dynamic content updates are announced via `aria-live` regions.

5. **Generate the Compliance Report**: Produce a structured report organized by WCAG principle and criterion. For each violation, include: the criterion number and name, the severity level, the affected element's HTML snippet, an explanation of why it fails, and the specific code fix. Include a summary table with pass/fail counts per principle and an overall conformance statement.

6. **Provide Remediation Code**: For every violation, supply a concrete before-and-after code snippet showing the exact fix. Group fixes by component or page region so developers can address them systematically rather than one element at a time.

## Usage

Provide the agent with a URL, a block of HTML, or a React/Vue component. Specify the target conformance level (AA or AAA) and any assistive technology requirements. The agent will audit the content and return a structured report with code fixes.

## Examples

### Example 1: WCAG Compliance Audit Report

**User Request**: "Audit this login form for WCAG 2.1 AA compliance."

```html
<div class="login">
  <img src="logo.png">
  <input type="text" placeholder="Username">
  <input type="password" placeholder="Password">
  <div class="btn" onclick="login()">Sign In</div>
  <p style="color: #aaa; font-size: 12px;">Forgot your password?</p>
</div>
```

**Agent Response — Accessibility Audit Report**:

| # | Criterion | Severity | Element | Issue |
|---|-----------|----------|---------|-------|
| 1 | 1.1.1 Non-text Content | Critical | `<img src="logo.png">` | Image has no `alt` attribute. Screen readers cannot describe it. |
| 2 | 1.3.1 Info and Relationships | Critical | `<input placeholder="Username">` | Input has no associated `<label>`. Placeholder text is not a substitute for a label. |
| 3 | 1.3.1 Info and Relationships | Critical | `<input placeholder="Password">` | Same label issue as above. |
| 4 | 1.4.3 Contrast Minimum | Serious | `<p style="color: #aaa">` | Text color `#aaa` on white background has a contrast ratio of 2.32:1. AA requires 4.5:1 for text this size. |
| 5 | 2.1.1 Keyboard | Critical | `<div class="btn" onclick>` | A `<div>` is not focusable via keyboard. Users cannot Tab to or activate this button. |
| 6 | 4.1.2 Name, Role, Value | Critical | `<div class="btn" onclick>` | Element has no semantic role. Screen readers announce it as generic text, not as a button. |

**Remediation — Fixed Code**:

```html
<form class="login" onsubmit="login(event)">
  <img src="logo.png" alt="Acme Corp logo">

  <label for="username">Username</label>
  <input id="username" type="text" autocomplete="username" required>

  <label for="password">Password</label>
  <input id="password" type="password" autocomplete="current-password" required>

  <button type="submit" class="btn">Sign In</button>

  <a href="/forgot-password" style="color: #595959; font-size: 14px;">
    Forgot your password?
  </a>
</form>
```

Changes made: added `alt` to the image, replaced placeholder-only inputs with explicit `<label>` elements, replaced the `<div>` with a semantic `<button>`, changed the link color from `#aaa` (2.32:1) to `#595959` (7.0:1), wrapped the form in a `<form>` element for proper submit handling, and added `autocomplete` attributes.

### Example 2: Fixing a React Component

**User Request**: "Fix accessibility issues in this React notification component."

**Before (inaccessible)**:
```jsx
function Notification({ message, onClose }) {
  return (
    <div className="notification">
      <span>{message}</span>
      <span className="close-x" onClick={onClose}>✕</span>
    </div>
  );
}
```

**After (accessible)**:
```jsx
function Notification({ message, onClose }) {
  return (
    <div role="alert" aria-live="assertive" className="notification">
      <p>{message}</p>
      <button
        type="button"
        onClick={onClose}
        aria-label="Dismiss notification"
        className="close-btn"
      >
        ✕
      </button>
    </div>
  );
}
```

**Fixes applied**: (1) Added `role="alert"` and `aria-live="assertive"` so screen readers announce the notification immediately when it appears. (2) Replaced the `<span onClick>` with a `<button>` so it is keyboard-focusable and announced as an interactive control. (3) Added `aria-label="Dismiss notification"` because the "✕" character alone does not convey the button's purpose to screen reader users. (4) Changed the inner `<span>` to a `<p>` for proper text semantics.

## Best Practices

- **Run automated tools first, but never rely on them alone**: axe-core catches roughly 30-40% of WCAG issues. The remaining 60-70% require manual keyboard testing, screen reader verification, and cognitive review.
- **Test with real screen readers, not just ARIA validators**: An element may have correct ARIA markup but still produce confusing announcements. VoiceOver and NVDA sometimes interpret the same markup differently.
- **Fix critical and serious issues before moderate ones**: Prioritize violations that completely block access (missing keyboard operability, no alt text on functional images) over cosmetic issues (minor contrast shortfalls on decorative elements).
- **Use semantic HTML before reaching for ARIA**: A `<button>` needs no `role="button"`. A `<nav>` needs no `role="navigation"`. ARIA is a repair tool for situations where semantic HTML is not sufficient, not a replacement for it.
- **Include accessibility checks in CI pipelines**: Run axe-core or pa11y in automated tests so new violations are caught before they reach production. Fail the build on critical violations.
- **Document accessibility decisions**: When a component intentionally deviates from a guideline (e.g., a custom combobox pattern), document the rationale and the alternative approach used to maintain equivalent access.

## Edge Cases

- **Single-page applications with client-side routing**: Page navigation does not trigger a browser page load, so screen readers are not notified of the new content. Use an `aria-live="polite"` region to announce route changes, or programmatically move focus to the new page's `<h1>`.
- **Dynamic content loaded after initial render**: Content injected via JavaScript after page load is invisible to screen readers unless wrapped in an `aria-live` region or focus is explicitly managed. For toast notifications use `aria-live="assertive"`; for feed updates use `aria-live="polite"`.
- **Complex data tables**: Tables with merged cells, nested headers, or sortable columns require explicit `scope`, `headers`, and `aria-sort` attributes. Test that a screen reader user can understand which header applies to each data cell.
- **Custom interactive widgets (sliders, date pickers, comboboxes)**: These have no native HTML equivalent. Follow the WAI-ARIA Authoring Practices 1.2 patterns exactly, implementing the full keyboard interaction model specified for each widget type.
- **Third-party embedded content (iframes, widgets)**: You cannot fix accessibility inside a third-party iframe. Document the issue, add a descriptive `title` attribute to the `<iframe>`, and provide an accessible alternative when the embedded content is critical to the user flow.
