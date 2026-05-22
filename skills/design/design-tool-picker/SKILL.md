---
name: design-tool-picker
description: Help choose the right design tool based on your current task. Use when unsure whether to use frontend-design, ui-ux-designer, visual-validator, or ui-code-auditor.
---

# Design Tool Picker

When users ask "which design tool should I use?" or seem unsure about design tooling, guide them with this decision tree.

## Quick Reference

| Your Situation | Recommended Tool | Type | Invocation |
|----------------|------------------|------|------------|
| Writing new UI code | `frontend-design` | skill | Loaded automatically |
| Need a design system template | `ux-brief` | command | `/majestic:ux-brief` |
| Refining existing UI iteratively | `ui-ux-designer` | agent | `Task(majestic-engineer:design:ui-ux-designer)` |
| Verifying visual changes match intent | `visual-validator` | agent | `Task(majestic-engineer:qa:visual-validator)` |
| Reviewing code for accessibility | `ui-code-auditor` | agent | `Task(majestic-engineer:qa:ui-code-auditor)` |
| Styling React components | `tailwind-styling` | skill | `Skill(majestic-react:tailwind-styling)` |

---

## Decision Flow

### Question 1: Do you have code written, or are you starting fresh?

**Starting fresh →** Choose based on what you need:
- Need design system from scratch: `/majestic:ux-brief`
- Just need design guidance while coding: `frontend-design` skill (auto-loads)

**Have code →** Continue to Question 2

---

### Question 2: Is the issue visual (layout, colors, spacing) or code quality (a11y, patterns)?

**Visual issues →** Continue to Question 3

**Code quality →** `ui-code-auditor` agent
- Reviews source code for accessibility violations
- Detects missing alt text, aria-labels, form labels
- Finds animation anti-patterns, touch target issues
- Returns findings with file:line references

---

### Question 3: Can you run the UI and take screenshots?

**Yes →** Continue to Question 4

**No →** `frontend-design` skill
- Provides design patterns for typography, color, motion
- Reference while coding without needing running UI

---

### Question 4: Do you want to iterate on the design or verify it's correct?

**Iterate →** `ui-ux-designer` agent
- Takes screenshots, analyzes, implements changes
- Multiple iteration cycles (default 10)
- Progressive refinement through visual feedback

**Verify →** `visual-validator` agent
- Checks if changes achieved intended goals
- Validates accessibility, design system compliance
- Returns structured pass/fail verdict

---

## Tool Comparison

### Screenshot-Based Tools (Visual)

| Tool | Purpose | When to Use |
|------|---------|-------------|
| `ui-ux-designer` | Iterative refinement | "Make this look better" |
| `visual-validator` | Verification | "Did my changes work?" |

Both require browser tools and running UI.

### Code-Based Tools (Static)

| Tool | Purpose | When to Use |
|------|---------|-------------|
| `ui-code-auditor` | Accessibility/quality audit | "Check my code for a11y issues" |
| `frontend-design` | Design guidance | "How should I style this?" |

Work on source code without running UI.

### Creation Tools

| Tool | Purpose | When to Use |
|------|---------|-------------|
| `ux-brief` command | Generate design system | "Create a design system for my project" |
| `tailwind-styling` | Tailwind patterns | "Help me use Tailwind effectively" |

---

## Common Workflows

### New Feature with UI

1. `/majestic:ux-brief` if no design system exists
2. `frontend-design` skill while implementing
3. `ui-code-auditor` before PR to catch a11y issues
4. `visual-validator` to verify visuals match intent

### Fix Visual Bug

1. `ui-ux-designer` if iterating to find the right fix
2. `visual-validator` to confirm fix worked

### Accessibility Audit

1. `ui-code-auditor` for code-level violations
2. `visual-validator` for visual accessibility (contrast, focus states)

### Design System Update

1. `/majestic:ux-brief` to update design system docs
2. `visual-validator` to verify components match spec
