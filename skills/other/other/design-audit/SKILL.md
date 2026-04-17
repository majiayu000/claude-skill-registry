---
name: design-audit
description: "Run technical quality checks across accessibility, performance, responsive design, theming, and anti-patterns. Generate a scored report with P0-P3 severity ratings. Report-only — documents issues for other skills to fix. Triggers on audit the design, check accessibility, technical review, performance audit, a11y check."
argument-hint: "[area (feature, page, component...)]"
---

Run systematic **technical** quality checks and generate a scored report. Don't fix issues — document them for other commands to address.

This is a code-level audit, not a design critique. Check what's measurable and verifiable in the implementation.

## Preparation

Read `~/.claude/skills/minoan-frontend-design/SKILL.md` for anti-pattern guidance. Check `.design-context.md` for project context if it exists.

## Diagnostic Scan

Check 5 dimensions. Score each 0-4 using `~/.claude/skills/minoan-frontend-design/references/heuristics-scoring.md` criteria.

### 1. Accessibility
- Contrast ratios < 4.5:1 (or 7:1 for AAA)
- Missing ARIA: interactive elements without proper roles, labels, states
- Keyboard: missing focus indicators, illogical tab order, keyboard traps
- Semantic HTML: heading hierarchy, landmarks, divs-as-buttons
- Form issues: inputs without labels, poor error messaging

**Score**: 0=Inaccessible, 1=Major gaps, 2=Partial effort, 3=WCAG AA mostly met, 4=WCAG AA fully met

### 2. Performance
- Layout thrashing: reading/writing layout properties in loops
- Expensive animations: animating width/height/top/left instead of transform/opacity
- Missing optimization: no lazy loading, unoptimized assets
- Bundle size: unnecessary imports, unused dependencies

**Score**: 0=Severe issues, 1=Major problems, 2=Partial optimization, 3=Mostly optimized, 4=Fast and lean

### 3. Responsive Design
- Fixed widths that break on mobile
- Touch targets < 44x44px
- Horizontal scroll on narrow viewports
- Missing breakpoints or mobile variants

**Score**: 0=Desktop-only, 1=Major failures, 2=Works on mobile with rough edges, 3=Responsive with minor issues, 4=Fluid across all viewports

### 4. Theming
- Hard-coded colors not using design tokens
- Broken dark mode or missing dark variants
- Inconsistent token usage, mixing token types
- Pure black (#000) or pure gray without tint

**Score**: 0=No theming, 1=Minimal tokens, 2=Inconsistent tokens, 3=Good with minor gaps, 4=Full token system

### 5. Anti-Patterns
Check against the rejection guidelines in the minoan skill and the full checklist in `~/.claude/skills/minoan-frontend-design/references/anti-patterns.md`. Look for AI slop tells, side-tab borders, gradient text, generic fonts, and all other tells.

**Score**: 0=AI slop gallery (5+ tells), 1=Heavy AI aesthetic (3-4), 2=Some tells (1-2), 3=Mostly clean, 4=Distinctive and intentional

## Report

### Audit Health Score

| # | Dimension | Score | Key Finding |
|---|-----------|-------|-------------|
| 1 | Accessibility | ? | |
| 2 | Performance | ? | |
| 3 | Responsive Design | ? | |
| 4 | Theming | ? | |
| 5 | Anti-Patterns | ? | |
| **Total** | | **??/20** | |

**Rating bands**: 18-20 Excellent, 14-17 Good, 10-13 Acceptable, 6-9 Poor, 0-5 Critical

### Anti-Patterns Verdict

Pass/fail: does this look AI-generated? List specific tells.

### Findings by Severity

Tag every issue **P0-P3**. For each:
- **[P?] Issue name**
- **Location**: Component, file, line
- **Category**: Accessibility / Performance / Theming / Responsive / Anti-Pattern
- **Impact**: How it affects users
- **Recommendation**: How to fix

### Systemic Issues

Recurring problems indicating gaps rather than one-off mistakes.

### Positive Findings

What's working well — good practices to maintain.

### Recommended Actions

List commands in priority order (P0 first). End with `/design-polish` if fixes were recommended.

For UX-level issues (hierarchy, emotional resonance, cognitive load), run `/design-critique`.

> Re-run `/design-audit` after fixes to see your score improve.
