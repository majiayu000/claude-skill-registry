---
name: ios-design-review
description: Visual design review of iOS screens against ios-styleguide.
argument-hint: "[--focus <feature>] [--no-fix]"
allowed-tools: Bash, Read, Glob, Grep, Write
---

## Purpose

Review iOS screens for ios-styleguide compliance, device adaptation, and accessibility. Report issues, then (with approval) fix and run tests to confirm.

## Arguments

- `--focus <feature>` — Limit to specific feature folder (default: all Features/)
- `--no-fix` — Report only, don't offer to fix

## Workflow

### 1. Collect screens

Scan `Features/**/` for `*View.swift` files to identify screens to review.

### 2. Evaluate against ios-styleguide

Review each screen for:

**Device adaptation**

- iPhone layout: focused, appropriate density
- iPad layout: uses space intentionally, not stretched iPhone
- Size class and orientation handling

**Liquid Glass**

- Used only for hierarchy/focus (nav bars, sheets, overlays)
- Not behind dense text, forms, or reading surfaces
- Respects reduce transparency setting

**Typography & hierarchy**

- Clear visual hierarchy
- Dynamic Type doesn't break layouts
- No banned fonts as primary

**Accessibility**

- VoiceOver labels on custom controls
- Tap targets ≥44pt
- Color not sole indicator

**"Not generic" bar**

- No unchanged SwiftUI defaults
- No repetitive patterns without hierarchy
- Purposeful restraint

For each issue, note:

- Screen/file
- Severity: `must-fix` | `should-fix` | `nice-to-have`
- What violates ios-styleguide
- Concrete fix

### 3. Report results

Summary of screens reviewed + findings by severity.

### 4–5. Approval gate, fix and confirm

See `/shared-review-workflow` for severity definitions, approval gate protocol, and fix constraints. After fixes, re-run lint/format and run `/ios-unit-test`.

## Reference

For evaluation checklists and preview testing, see `reference/ios-design-review-reference.md`
