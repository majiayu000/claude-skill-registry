---
name: subagent-driven-development
description: (ePost) Use when a plan has 3+ independent tasks, phases have non-overlapping file ownership, or user says "parallel implementation", "execute all phases" — provides per-task subagent dispatch with two-stage review
user-invocable: false

metadata:
  agent-affinity: [epost-project-manager, epost-fullstack-developer, epost-planner]
  keywords: [parallel, subagent, dispatch, implementation-loop, two-stage-review]
  platforms: [all]
  connections:
    enhances: [plan]
---

# Subagent-Driven Development

## When to Use

Activate when a plan has 3+ independent tasks that can be implemented and reviewed separately. Do NOT use for single-task or tightly-coupled work.

## Per-Task Loop

For each task in the plan:

1. **Dispatch Implementer** — Fresh subagent with task context (see `references/implementer-prompt.md`)
2. **Spec Review** — Fresh subagent verifies code matches spec (see `references/spec-reviewer-prompt.md`)
3. **Quality Review** — Fresh subagent reviews code quality (see `references/code-quality-reviewer-prompt.md`)
4. **Fix Loop** — If either review fails: fix → re-review (max 3 iterations)
5. **Mark Done** — Update plan TODO, move to next task

## Two-Stage Review

Every task gets TWO independent reviews, in order:

### Stage 1: Spec Compliance
- Does the code do what the spec says?
- Line-by-line comparison against requirements
- Output: ✅ matches / ❌ deviates with file:line

### Stage 2: Code Quality
- Is the code well-written?
- Security, performance, maintainability
- Only runs AFTER spec compliance passes

## Rules

- Never start work on main/master without user consent
- Never skip either review stage
- Never dispatch parallel implementation subagents (serial only — one task at a time)
- Each subagent gets a FRESH context (no stale state)
- Max 3 fix-review iterations per task; escalate to user after 3

## Task Dispatch Order

1. Foundation tasks first (shared utilities, types, config)
2. Independent features in plan order
3. Integration tasks last (wire components together)

## Prompt Templates

- `references/implementer-prompt.md` — Task context and self-review checklist
- `references/spec-reviewer-prompt.md` — Skeptical spec comparison
- `references/code-quality-reviewer-prompt.md` — Quality review after spec passes

### Related Skills
- `verification-before-completion` — Verify each task before marking done
- `code-review` — Quality review patterns
- `plan` — Plan structure that feeds task dispatch
