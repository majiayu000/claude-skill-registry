---
name: researching
description:
  Use when requirements are fuzzy, multiple technical approaches exist, or
  change affects architecture, API, data, or security
---

# Researching Skill

Use when the how is unclear; output is a chosen approach with evidence.

**Prerequisites:** If what/why is unclear, use **discovering** skill first.

## Quick Reference

| Track          | When                         | Output                               |
| -------------- | ---------------------------- | ------------------------------------ |
| Fast (default) | Standard decisions           | Brief: problem, decision, risks      |
| Full           | API/security/multi-subsystem | Research brief + optional design doc |

## When to Use

- Requirements are fuzzy or incomplete
- Multiple plausible approaches exist (spike, proof of concept needed)
- Change affects architecture, API, data, or security

Skip if: obvious bug, trivial change, pattern already exists.

## Fast vs Full Track

```
Is it high-risk?
├── No → Fast Track (default)
└── Yes → Full Track
    ├── Changes public API
    ├── Security/data implications
    ├── Team disagreement
    └── Touches multiple subsystems
```

## Core Rule

**Evidence before opinions.** Never recommend anything until facts are gathered:
what already exists in code, which constraints are real, what decisions were
made before. If evidence is missing — label it as assumption and lower
confidence.

## Quick Rules

- One question at a time while clarifying requirements
- If multiple interpretations exist, clarify before researching
- State assumptions explicitly with confidence (H/M/L)

## When to Ask vs Act

**Ask** (one question at a time; prefer multiple choice) if:

- Multiple interpretations
- Critical context missing
- Answer would change direction

**Act** (state assumptions + confidence) if:

- Default interpretation is clear
- Request is specific
- Assumptions are easy to verify

## Workflow

### Fast Track (default)

1. **Clarify & Frame** — purpose, constraints, success criteria
2. **Collect Signals** — code, docs, history
3. **Options + Decision** — 2-3 options, pick one
4. **Brief** — Problem (1-2 sentences), Decision, Key Risks (1-3 bullets)

### Full Track

| Phase        | Focus                                | Output                         |
| ------------ | ------------------------------------ | ------------------------------ |
| 0. Frame     | Problem, non-goals, success criteria | Constraints                    |
| 1. Signals   | Code, docs, history                  | Current state + assumptions    |
| 2. Options   | 2-4 approaches with trade-offs       | Comparison                     |
| 3. Evaluate  | Decide using Phase 0 criteria        | Recommendation + fallback plan |
| 4. Artifacts | Research brief (always)              | Optional: design doc           |

**Research Brief template:** Problem & Context → Constraints → Current State →
Options Compared → Recommendation → Risks

## Stop Conditions

Stop research when:

- Decision criteria are satisfied
- Remaining unknowns won't change the decision
- Next step is prototype/measurement

## Best Practices

- **Assumptions + Confidence** — label assumptions (H/M/L), propose quick
  validation
- **Spike as Research** — 30-90 min spike with clear question and success metric
- **Checkpoints (Full Track)** — after each phase: "Constraints complete? Which
  risks matter?"

## Common Mistakes

| Mistake                            | Fix                                 |
| ---------------------------------- | ----------------------------------- |
| Recommend without evidence         | Gather facts first, then opinions   |
| Single option, no alternatives     | Always 2-3 options with trade-offs  |
| Drift into tangential topics       | Stay connected to problem statement |
| Hide uncertainty behind confidence | State unknowns explicitly           |
| Finalize with disputed framing     | Resolve framing first               |
