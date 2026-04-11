---
name: design-critique
description: "Evaluate design from a UX perspective with quantitative scoring, anti-pattern detection, persona-based testing, and actionable feedback. This skill should be used when the user asks to review, critique, evaluate, or give feedback on a design or component, or says 'UX review,' 'design feedback,' or 'how does this look.'"
argument-hint: "[area (feature, page, component...)]"
---

Evaluate the design quality of a feature or component. Report-only — this skill documents issues but does not fix them.

## Preparation

Read `~/.claude/skills/minoan-frontend-design/SKILL.md` for aesthetic principles and anti-pattern guidance. If no `.design-context.md` exists in the project root, ask the user about audience and intended feel before proceeding — context determines whether a design choice is right or wrong.

## Step 1: LLM Design Review

Read the relevant source files (HTML, CSS, JS/TS) and visually inspect if browser automation is available.

Evaluate as a design director:

**AI Slop Detection**: Does this look like every other AI-generated interface? Check against the rejection guidelines in the minoan skill. Look for: AI color palette, gradient text, glassmorphism, hero metric layouts, identical card grids, generic fonts (including second-tier defaults like Fraunces, Instrument Sans, Outfit), side-tab accent borders. **The test**: if someone said "AI made this," would they believe immediately?

**Holistic Design Review**: Visual hierarchy (eye flow, primary action clarity), composition (balance, whitespace, rhythm), typography (hierarchy, readability, font choices), color (purposeful use, cohesion, accessibility), states & edge cases (empty, loading, error, success).

**Cognitive Load** (consult `~/.claude/skills/minoan-frontend-design/references/cognitive-load.md`):
Run the 8-item checklist. Report failure count: 0-1 = low (good), 2-3 = moderate, 4+ = critical. Count visible options at each decision point — if >4, flag it.

**Nielsen's Heuristics** (consult `~/.claude/skills/minoan-frontend-design/references/heuristics-scoring.md`):
Score each of the 10 heuristics 0-4.

## Step 2: Systematic Anti-Pattern Check

Walk through `~/.claude/skills/minoan-frontend-design/references/anti-patterns.md` checklist item by item against the code. For full technical dimension scoring (a11y, performance, responsive, theming, anti-patterns), recommend `/design-audit` — this step focuses on design-quality anti-patterns only, not technical implementation.

## Step 3: Combined Report

Synthesize both assessments. Note where they agree, where systematic checks caught issues the holistic review missed, and vice versa.

### Design Health Score

| # | Heuristic | Score | Key Issue |
|---|-----------|-------|-----------|
| 1 | Visibility of System Status | ? | |
| 2 | Match System / Real World | ? | |
| 3 | User Control and Freedom | ? | |
| 4 | Consistency and Standards | ? | |
| 5 | Error Prevention | ? | |
| 6 | Recognition Rather Than Recall | ? | |
| 7 | Flexibility and Efficiency | ? | |
| 8 | Aesthetic and Minimalist Design | ? | |
| 9 | Error Recovery | ? | |
| 10 | Help and Documentation | ? | |
| **Total** | | **??/40** | |

Be honest with scores. A 4 means genuinely excellent. Most real interfaces score 20-32.

### Anti-Patterns Verdict

Does this look AI-generated? Specific tells found. For full technical dimension scores (a11y, performance, responsive, theming), recommend `/design-audit`.

### What's Working

2-3 things done well. Be specific about why they work.

### Priority Issues

3-5 most impactful problems, ordered by importance. For each:
- **[P0-P3] What**: Name the problem
- **Why it matters**: How this hurts users
- **Fix**: Concrete suggestion
- **Suggested command**: `/design-audit`, `/design-polish`, `/minoan-frontend-design`, etc.

Severity definitions: P0 = blocks task completion, P1 = significant difficulty or WCAG violation, P2 = annoyance with workaround, P3 = nice-to-fix.

### Persona Red Flags

Consult `~/.claude/skills/minoan-frontend-design/references/personas.md`. Select 2-3 personas most relevant to this interface. For each, walk through the primary user action and list specific red flags:

**Alex (Power User)**: No keyboard shortcuts. Form requires 8 clicks. High abandonment risk.
**Jordan (First-Timer)**: Icon-only nav. Technical jargon in errors. Will abandon at step 2.

Be specific — name exact elements and interactions that fail each persona.

### Recommended Actions

List recommended commands in priority order. End with `/design-polish` as the final step if fixes were recommended.

For technical quality issues (contrast ratios, performance, responsive breakpoints), run `/design-audit`.

> Re-run `/design-critique` after fixes to see your score improve.
