---
name: fresh-eyes
description: >-
  Apply perspective-shift discipline to plans, code, and bugs. Re-examine work
  as if seeing it for the first time. Use when: (1) about to implement a feature
  or fix, (2) reviewing your own code after writing it, (3) diagnosing a bug
  where the obvious fix did not work, (4) catching blind spots from familiarity.
  Three modes: Planning, Review, Reflection.
category: principles
---

# Fresh Eyes

Re-examine work as if seeing it for the first time. Familiarity breeds blind spots. This skill forces perspective shifts at three stages: before building, after building, and after fixing.

## Core Philosophy

- Assume your first understanding is incomplete.
- Read code and plans literally, not through the lens of intent.
- Treat "obvious" as a warning sign, not a green light.
- Question decisions that feel automatic.
- Surface findings without filtering for convenience.

## Modes

### Planning Mode

**Trigger:** About to implement a feature, fix, or refactor. Plan exists but work has not started.

**Purpose:** Audit the plan for hidden complexity, missing acceptance criteria, and tech debt traps before committing to implementation.

**Deliverables:**
- Explicit acceptance criteria (extracted or written)
- Hidden complexity inventory
- Pre-mortem scenarios (what kills this in production?)
- Minimal test plan tied to acceptance criteria

See [references/planning-prompts.md](references/planning-prompts.md) for full prompt templates.

### Review Mode

**Trigger:** Code written and ready for review. You wrote it yourself or have been staring at it long enough to lose objectivity.

**Purpose:** Multi-pass review that forces you to see the diff as a stranger would. Each pass has a different lens.

**Deliverables:**
- Pass 1 findings: first impressions, naming confusion, flow surprises
- Pass 2 findings: edge cases, error paths, boundary conditions
- Pass 3 findings: regression risks, integration assumptions
- Structured findings (Blocker / Major / Minor / Structural Follow-up)

**Repeat condition:** Stop after 2 consecutive clean passes or a fixed timebox. Do not loop indefinitely.

See [references/review-prompts.md](references/review-prompts.md) for full prompt templates.

### Reflection Mode

**Trigger:** Bug fixed or incident resolved. The obvious fix worked (or did not). You want to understand why it happened and whether it will happen again.

**Purpose:** Build causal chains from symptom to root cause. Distinguish root causes from symptoms. Extract tech debt signals and regression test guidance.

**Deliverables:**
- Causal chain (symptom to root cause, each link justified)
- Root vs symptom determination with evidence
- Tech debt signals (patterns that enabled the bug)
- Regression test recommendations

See [references/reflection-prompts.md](references/reflection-prompts.md) for full prompt templates.

## Routing Table

| Context | Mode | Notes |
|---------|------|-------|
| Plan exists, work not started | Planning | Audit before committing |
| PR or diff ready for review | Review | Multi-pass with fresh perspective |
| Self-reviewing own code | Review | Especially valuable here |
| Bug fixed, want to understand why | Reflection | Causal chain analysis |
| Obvious fix failed | Reflection | Question assumptions |
| Post-incident analysis | Reflection | Extract patterns |
| Unclear requirements | Planning | Surface ambiguity early |

## Chaining with rick-rubin

fresh-eyes surfaces findings. rick-rubin provides scope-aware response to those findings.

Typical chain:
1. fresh-eyes Planning mode audits the plan.
2. rick-rubin (prompt A or B) trims scope based on findings.
3. Work proceeds with tighter scope and fewer blind spots.

Or after review:
1. fresh-eyes Review mode produces findings.
2. rick-rubin (prompt E or F) evaluates which findings require action vs deferral.

Do not duplicate rick-rubin's scope discipline logic. Cross-reference only.

## Rationalizations (All Rejected)

| Excuse | Why It's Wrong | Required Action |
|--------|----------------|-----------------|
| "I just wrote this, I know what it does" | That is exactly when blind spots form | Use Review mode |
| "The plan is clear" | Plans always look clear to the author | Use Planning mode |
| "The fix is obvious" | Obvious fixes hide root causes | Use Reflection mode |
| "I already reviewed this" | Same eyes, same blind spots | Do another pass with a different lens |
| "This is too small to audit" | Small changes carry outsized risk | At minimum, one Planning pass |
| "I'll reflect later" | Later never comes | Reflect now while context is fresh |

## Guardrails

- Do not use fresh-eyes as a delay tactic. Each mode has concrete deliverables and exit conditions.
- Do not loop Review passes indefinitely. Two clean passes or a timebox, then stop.
- Do not propose fixes in Planning mode. Surface problems only.
- Do not expand scope during Review. Flag structural issues as follow-ups, not blockers.
- For routine execution work, prefer lower-cost model tiers. Escalate for ambiguous root-cause reasoning. Reference `model-router` when explicit routing guidance is needed.
