---
name: tools-bug-triad-review
description: Run a weekly adversarial bug triad (finder, skeptic, arbiter) to maximize bug discovery coverage and emit a scored verified bug list.
operating_mode: AUDIT
trigger_conditions: weekly bug review, adversarial bug audit, finder skeptic arbiter, verify bug list, red-team bug hunt
related_skills: tools-bug-scan, lp-do-build, ops-ci-fix
---

# Bug Triad Review

Use this skill when the user wants a high-recall, adversarial bug review that intentionally tolerates false positives and then filters them through a skeptic + final arbiter pass.

## Weekly Cadence

Run once per week for the default codebase sweep. Prefer a fixed day and artifact path so trends are easy to compare.

- Artifact root: `docs/audits/bug-triad/<YYYY-MM-DD>/`
- Required files:
  - `finder.md`
  - `skeptic.md`
  - `arbiter.md`
  - `verified-bugs.md`

## Inputs

Use these as evidence for all three phases:

1. Static bug scan output (`pnpm bug-scan` or `pnpm bug-scan:changed` + optional JSON mode).
2. Targeted code reads around hotspots.
3. Relevant runtime errors, lint/typecheck diagnostics, or prior incident notes.

If scope is unspecified, default to changed-files plus critical paths touched in the last week.

## Execution Workflow

1. Build evidence packet
- Collect scanner output and key code references.
- Normalize each candidate issue with a stable ID (`BUG-001`, `BUG-002`, ...).

2. Run Finder pass
- Use the Finder prompt from `references/phase-prompts.md`.
- Enforce scoring: `Low=+1`, `Medium=+5`, `Critical=+10`.
- Output to `finder.md` with total score.

3. Run Skeptic pass
- Feed `finder.md` into the Skeptic prompt.
- Challenge every bug; prefer `DISPROVE` only when confidence is high (2x penalty awareness).
- Output to `skeptic.md` with final skeptic score.

4. Run Arbiter pass
- Feed `finder.md` + `skeptic.md` into the Arbiter prompt.
- Arbiter resolves truth for each disputed bug and produces final accepted list.
- Output to `arbiter.md`.

5. Publish verified bug list
- Create `verified-bugs.md` containing only `VERDICT: REAL BUG` items.
- Group by severity, include file references and concise fix direction.

## Output Contract

Every run must report:

- Run date and scope reviewed.
- Finder total score.
- Skeptic final score.
- Counts: reported, disproved, accepted, confirmed-real.
- Verified bug list grouped by `Critical`, `Medium`, `Low`.

## Guardrails

- Do not invent evidence; every bug must cite concrete repo location(s).
- False positives are allowed in Finder pass, but Arbiter output must be evidence-based.
- If evidence is insufficient to decide, Arbiter must mark confidence `Low` and call out exact missing evidence.
- Do not skip skeptic or arbiter phases; this skill is triad-by-design.

## Escalation

Escalate to `lp-do-plan` / `lp-do-build` when:

- confirmed critical bugs require coordinated fixes,
- the same bug class appears across multiple packages,
- weekly trend shows regressions for two consecutive runs.
