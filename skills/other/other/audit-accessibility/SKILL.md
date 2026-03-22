---
name: audit-accessibility
description: Audit a feature for WCAG 2.1 AA compliance using POUR principles when the user asks to check accessibility, audit a11y, or verify WCAG compliance
author: chalk
version: "1.0.0"
metadata-version: "3"
allowed-tools: Read, Glob, Grep, Write
argument-hint: "[feature or component to audit for accessibility]"
read-only: false
destructive: false
idempotent: false
open-world: false
user-invocable: true
tags: audit, accessibility, a11y
---

# Audit Accessibility

## Overview

Generate a WCAG 2.1 AA compliance audit for a specific feature or component, organized by the POUR principles (Perceivable, Operable, Understandable, Robust). Produces a concrete checklist with testing instructions, keyboard navigation paths, screen reader expectations, and color contrast requirements.

## Workflow

1. **Read feature context** -- Scan `.chalk/docs/product/` for the PRD describing the feature. Check `.chalk/docs/engineering/` for component architecture and any existing a11y guidelines. Read the source code for the feature's UI components to understand the actual implementation.

2. **Parse the audit target** -- Extract from `$ARGUMENTS` the feature, page, or component to audit. If unspecified, ask the user to name a specific feature -- auditing the entire application at once produces shallow results.

3. **Determine the next file number** -- Read filenames in `.chalk/docs/engineering/` to find the highest numbered file. The next number is `highest + 1`.

4. **Audit Perceivable** -- Check:
   - All images have meaningful alt text (decorative images use `alt=""`)
   - Color is not the only means of conveying information
   - Text meets contrast ratios (4.5:1 for normal text, 3:1 for large text)
   - Content is readable at 200% zoom
   - Media has captions or transcripts

5. **Audit Operable** -- Check:
   - All interactive elements are reachable via keyboard (Tab, Shift+Tab, Enter, Space, Escape, Arrow keys)
   - Document the expected keyboard navigation path through the feature
   - Focus order matches visual order
   - No keyboard traps
   - Focus indicators are visible
   - Touch targets are at least 44x44 CSS pixels

6. **Audit Understandable** -- Check:
   - Form inputs have visible labels (not just placeholders)
   - Error messages identify the field and describe how to fix the error
   - Consistent navigation and naming patterns
   - Language is set on the page element

7. **Audit Robust** -- Check:
   - Semantic HTML elements used appropriately (buttons, links, headings, landmarks)
   - ARIA roles, states, and properties are correct and necessary
   - Components work with major screen readers (VoiceOver, NVDA, JAWS)
   - No ARIA is better than bad ARIA

8. **Write the file** -- Save to `.chalk/docs/engineering/<n>_a11y_audit_<feature-slug>.md`.

9. **Confirm** -- Share the file path and highlight the highest-severity issues that block users from completing tasks.

## Output

- **File**: `.chalk/docs/engineering/<n>_a11y_audit_<feature-slug>.md`
- **Format**: Plain markdown with POUR-organized checklist, each item marked pass/fail/needs-review with specific testing instructions
- **First line**: `# Accessibility Audit: <Feature Name>`

## Anti-patterns

- **Checklist without testing instructions** -- "Check color contrast" is not actionable. Specify which elements, what the current ratio is, and what the target ratio should be.
- **ARIA overuse** -- Adding `role="button"` to a `<button>` is redundant. Adding ARIA to fix semantic HTML problems is treating symptoms. Prefer native HTML elements.
- **Keyboard testing only with Tab** -- Many components require Arrow keys (tabs, menus, radio groups), Escape (modals, dropdowns), Space (checkboxes), and Enter (buttons, links). Document the full expected keyboard interaction model.
- **Ignoring screen reader output** -- An element can be technically accessible but produce nonsensical screen reader output. Specify what the screen reader should announce for each interactive element.
- **Treating a11y as a one-time audit** -- Note which checks should be automated in CI and which require manual testing on each release.
