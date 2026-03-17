---
name: nean-design-review
description: Visual design review using Playwright screenshots against nean-styleguide.
argument-hint: "[--base-url <url>] [--routes /,/settings] [--no-fix]"
allowed-tools: Bash, Read, Glob, Grep, Write
---

## Purpose

Capture screenshots at multiple breakpoints and evaluate against nean-styleguide. Report issues, then (with approval) fix and run tests to confirm.

## Arguments

- `--base-url <url>` — App URL (default: http://localhost:4200)
- `--routes <paths>` — Comma-separated routes (default: discover from `app.routes.ts`)
- `--no-fix` — Report only, don't offer to fix

## Workflow

### 1. Setup

- Ensure dev servers running (`npm run dev`)
- Discover routes if not specified (scan for route configurations)

### 2. Capture screenshots

Use Playwright to capture each route at:

- Mobile: 390×844
- Tablet: 834×1194
- Desktop: 1440×900

Save to `playwright-artifacts/design-review/` (don't commit).

### 3. Evaluate against nean-styleguide

Review each screenshot for:

- **Responsiveness** — intentional adaptation, not just stacking
- **Typography** — no banned fonts, contributes voice
- **Spacing/hierarchy** — premium feel, clear visual order
- **Color** — uses semantic tokens, proper contrast
- **Accessibility** — visible focus states, adequate tap targets
- **PrimeNG customization** — not using default themes unchanged
- **Anti-patterns** — no unchanged PrimeNG defaults, card nesting, decorative effects

For each issue, note:

- Route and viewport
- Severity: `must-fix` | `should-fix` | `nice-to-have`
- What violates nean-styleguide
- Concrete fix

### 4. Report results

Summary of screens/viewports reviewed + findings by severity.

### 5–6. Approval gate, fix and confirm

See `/shared-review-workflow` for severity definitions, approval gate protocol, and fix constraints. After fixes, re-capture affected screenshots and run `/nean-unit-test`.

## Reference

For Playwright setup, screenshot scripts, and evaluation checklist, see `reference/nean-design-review-reference.md`
