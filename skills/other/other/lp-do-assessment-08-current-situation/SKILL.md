---
name: lp-do-assessment-08-current-situation
description: Current situation elicitation for new startups (ASSESSMENT-08). Captures launch surface, inventory/product readiness, commercial architecture, and pre-locked channel decisions. Produces operator-context artifact for intake sync.
---

# lp-do-assessment-08-current-situation — Current Situation (ASSESSMENT-08)

Load: ../_shared/assessment/assessment-base-contract.md

Elicits and records what the operator directly knows about the business before ASSESSMENT intake runs. Captures launch surface, inventory/product readiness, commercial architecture, and pre-locked channel decisions. All fields are either confirmed or explicitly marked as open gaps.

## Invocation

```
/lp-do-assessment-08-current-situation --business <BIZ>
```

Required:
- `--business <BIZ>` — 3-4 character business identifier

**Business resolution pre-flight:** If `--business` is absent or the directory `docs/business-os/strategy/<BIZ>/` does not exist, apply `_shared/business-resolution.md` before any other step.

## Operating Mode

ELICIT + WRITE

This skill:
- Reads existing business strategy docs to extract any already-documented operator context
- Pre-populates a draft artifact from whatever is already on record
- Surfaces gaps and asks the operator to fill or confirm each field
- Writes the final ASSESSMENT-08 artifact

Does NOT:
- Research external sources (that is ASSESSMENT-01–ASSESSMENT-07 territory)
- Make strategic recommendations about which options to pursue
- Set field values the operator has not confirmed

## Required Inputs (pre-flight)

Required:
- `--business <BIZ>` — business identifier

Optional (read if present, note gap if absent):
- `docs/business-os/strategy/<BIZ>/plan.user.md` — may contain operational context
- `docs/business-os/startup-baselines/<BIZ>/<YYYY-MM-DD>-assessment-intake-packet.user.md` — may contain pre-recorded observed fields
- `docs/business-os/strategy/<BIZ>/s0c-option-select.user.md` — may contain execution constraints (from ASSESSMENT-03)
- Any other strategy or brief docs under `docs/business-os/strategy/<BIZ>/`

If upstream ASSESSMENT-01–ASSESSMENT-07 artifacts are absent, note the gap but proceed — ASSESSMENT-08 captures operator-direct knowledge only and does not depend on research outputs.

---

## Steps

Load: modules/steps.md

---

## Output Contract and Quality Gate

Load: modules/output-and-quality.md

---

## Completion Message

> "Operator evidence recorded: `docs/business-os/strategy/<BIZ>/<YYYY-MM-DD>-operator-context.user.md`. [N] fields confirmed, [M] gaps logged in Section E."
>
> "All eight ASSESSMENT precursors (ASSESSMENT-01–ASSESSMENT-08) now present for <BIZ>. The next `/startup-loop start` or `advance` call will trigger ASSESSMENT intake sync automatically."

---

## Integration

**Upstream (ASSESSMENT-07):** Runs after `/lp-do-assessment-07-measurement-profiling --business <BIZ>` produces <YYYY-MM-DD>-measurement-profile.user.md.

**Downstream:** `modules/assessment-intake-sync.md` reads this artifact as `Precursor-ASSESSMENT-08`. Section E gaps feed intake Section F (Missing-Data Checklist). Section D channel pre-decisions are preserved as operator-locked rows in intake Section D.
