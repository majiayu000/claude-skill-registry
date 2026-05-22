---
name: design-review
description: >
  Comprehensive UI/UX design review with live environment testing, responsive validation,
  accessibility compliance (WCAG 2.1 AA), and visual consistency analysis using Playwright.
  Use when user runs /design-review, /review:design-review, requests a "design review",
  "UI review", "UX audit", or mentions "review the design", "check accessibility", "responsive testing".
disable-model-invocation: true
argument-hint: "[output-directory]"
---

# Design Review

World-class design review following standards of top Silicon Valley companies (Stripe, Airbnb, Linear).

## Parse Arguments

**Output Path Configuration**:
- If `$ARGUMENTS` is provided and non-empty: Use `$ARGUMENTS` as the output directory
- Otherwise: Use default `./reviews/design/`

## Git Analysis

GIT STATUS:

```
!`git status`
```

FILES MODIFIED:

```
!`git diff --name-only origin/HEAD...`
```

COMMITS:

```
!`git log --no-decorate origin/HEAD...`
```

DIFF CONTENT:

```
!`git diff --merge-base origin/HEAD`
```

Review the complete diff above to understand the scope of UI/UX changes.

## Core Methodology

**"Live Environment First"** — Always assess the interactive experience before diving into static analysis or code. Prioritize the actual user experience over theoretical perfection.

## Prerequisites

- A live preview environment (local dev server or staging URL)
- Playwright CLI for automated browser testing (refer to the `playwright:playwright-cli` skill for full command reference)

## Review Phases

Execute each phase systematically. See [WORKFLOW.md](WORKFLOW.md) for detailed checklists.

| Phase | Focus | Key Actions |
|-------|-------|-------------|
| 0 | Preparation | Analyze PR/description, review code diff, set up preview, configure viewport (1440x900) |
| 1 | Interaction | Execute user flows, test interactive states (hover/active/disabled), verify confirmations |
| 2 | Responsiveness | 7 viewport tiers (375–1920px), between-breakpoint sweeps, zoom reflow (400%), container queries |
| 3 | Visual Polish | Layout alignment, typography hierarchy, color consistency, image quality |
| 4 | Accessibility | Automated axe-core scan + manual keyboard sequence (Tab order, focus traps, Enter/Space) |
| 5 | Robustness | Form validation, content overflow, loading/empty/error states, edge cases |
| 6 | Code Health | Component reuse, design tokens (no magic numbers), pattern adherence |
| 7 | Content & Console | Grammar, text clarity, browser console errors/warnings |

## Confidence & Signal Quality

Before reporting any finding, score confidence 1-10:

| Confidence | Action | Requirement |
|------------|--------|-------------|
| 9-10 | Report | Measurable failure with concrete evidence (screenshot, axe output, contrast ratio) |
| 7-8 | Report | Design system violation with specific token/rule reference |
| 5-6 | Suppress | Plausible but speculative — no system rule to cite |
| Below 5 | Discard | Aesthetic preference or subjective opinion |

**Finding caps**: Max **8 meaningful findings** (Blocker + High-Priority + Medium-Priority) and max **2 Nits** per review. If more exist, keep the highest-confidence items and note "additional observations available on request."

**Self-reflection**: After generating all candidate findings, re-evaluate each in context of the full set. Remove redundant, low-signal, or opinion-only items. Apply false positive filtering from [WORKFLOW.md](WORKFLOW.md).

## Triage Matrix

Categorize every finding using confidence thresholds:

- **[Blocker]**: Measurable failure requiring immediate fix — broken layout, keyboard trap, contrast <4.5:1, element inaccessible, content overflow (confidence >=8)
- **[High-Priority]**: Documented system violation — wrong design token, WCAG AA violation, responsive breakage (confidence >=7)
- **[Medium-Priority]**: Inconsistency with evidence — spacing/alignment with comparison screenshot (confidence >=6)
- **[Nit]**: Minor aesthetic detail, optional — max 2 per review
- **[Praise]**: Acknowledge a good design decision — max 1 per review

## Communication Principles

1. **Problems Over Prescriptions**: Describe problems and their impact, not technical solutions. Example: Instead of "Change margin to 16px", say "The spacing feels inconsistent with adjacent elements."
2. **Evidence-Based**: Provide screenshots for visual issues. Reference specific design tokens or WCAG criteria.
3. **Start Positive**: Begin with acknowledgment of what works well.

## Output Instructions

1. **Create output directory** using Bash: `mkdir -p {output-directory}`
2. **Save the report** to: `{output-directory}/{YYYY-MM-DD}_{HH-MM-SS}_design-review.md`

Include this header:

```markdown
# Design Review Report

**Date**: {ISO 8601 date}
**Branch**: {current branch name}
**Commit**: {short commit hash}
**Reviewer**: Claude Code (design-review)

---
```

3. **Display the full report** to the user in the chat
4. **Confirm the save**: Report saved to: {output-directory}/{filename}

## Resources

- [WORKFLOW.md](WORKFLOW.md) - Detailed phase-by-phase checklists, false positive filtering, confidence scoring guide, and report template
- [EXAMPLES.md](EXAMPLES.md) - Sample design review reports
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues with environment, viewports, accessibility, and output
