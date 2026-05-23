---
name: lp-do-assessment-01-problem-statement
description: Problem framing for new startups (ASSESSMENT-01). Produces a falsifiable problem statement artifact before entering ASSESSMENT intake. Upstream of lp-do-assessment-02-solution-profiling.
---

# lp-do-assessment-01-problem-statement — Problem Framing (ASSESSMENT-01)

Produces a clear, falsifiable problem statement before the operator enters S0 (Intake). Run this when starting from a customer problem rather than a committed product hypothesis.

Load: ../_shared/assessment/assessment-base-contract.md

## Invocation

```
/lp-do-assessment-01-problem-statement --business <BIZ>
```

Required:
- `--business <BIZ>` — 3-4 character business identifier (e.g., PET, HEAD, BRIK)

**Business resolution pre-flight:** If `--business` is absent or the directory `docs/business-os/strategy/<BIZ>/` does not exist, apply `_shared/business-resolution.md` before any other step.

## Operating Mode

READ-THEN-WRITE

This skill:
- Reads existing business docs and operator-provided problem descriptions
- Produces one structured problem statement artifact
- Does NOT recommend solutions, select product types, or score demand
- Does NOT ask whether to proceed — operator decides after reviewing the artifact

## Inputs

Required:
- `--business <BIZ>` — business identifier

Optional (read if present):
- Inline problem description provided by the operator at invocation
- Any file path provided by the operator

Search paths (scan in order, use what exists):
- `docs/business-os/strategy/<BIZ>/` — strategy docs, briefs, notes
- `docs/business-os/startup-baselines/<BIZ>/*` — baseline docs

If no files exist, work from operator-provided description only. Do not block on missing files.

## Steps

Load: modules/steps.md

## Output Contract

Load: modules/output-template.md

## Quality Gate

Load: modules/quality-gate.md

## Integration

**Upstream (S0):** `/startup-loop start --start-point problem` triggers this skill before S0 intake begins.

**Downstream:** `/lp-do-assessment-02-solution-profiling --business <BIZ>` reads `docs/business-os/strategy/<BIZ>/<YYYY-MM-DD>-problem-statement.user.md` as its primary input. Do not proceed to solution space if a STOP advisory is present without operator acknowledgement.

## Reference Artifacts

High-quality examples to consult before writing:
- `docs/business-os/strategy/HEAD/<YYYY-MM-DD>-problem-statement.user.md` — CI accessory retention business; strong on: confidence tagging, problem boundary, user group demographic grounding, structured kill conditions
- `docs/business-os/strategy/HBAG/<YYYY-MM-DD>-problem-statement.user.md` — artisan bag accessories; strong on: forced-choice binary Core Problem framing, workarounds table, documented failure states, "Unblocked by:" kill condition format, research appendix separation
