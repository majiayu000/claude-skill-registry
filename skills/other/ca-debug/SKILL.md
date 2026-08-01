---
name: ca-debug
description: Investigate-then-decide root-cause analysis for a defect whose cause is unknown. No code changes — exits to /ca-fix, /ca-adr, or a no-action close.
argument-hint: "<observed symptom>"
---

# /ca-debug — root-cause investigation

Investigates a defect, anomaly, or unexpected behavior whose cause is not yet known. Separates investigation from implementation: no code is modified while debugging. Describe the symptom with enough fidelity that another operator could reproduce it — observed behavior, reproduction steps (or intermittent-trigger profile), and environment. Vague descriptions ("it's flaky") are rejected; the orchestrator asks for clarification before routing.

If the cause is already known and a regression test is already named, invoke `/ca-fix` directly.

## Routes to

The `debug` skill (`<plugin-root>/routines/debug/SKILL.md`) — five gated phases: symptom
capture, hypothesis generation, evidence gathering, root-cause decision, handoff. Phase 4 forces one
named exit:

- **(a) Confirmed bug → `/ca-fix`**, carrying the confirmed bug statement, cited evidence, and a named
  regression test obligation tied to the minimal repro.
- **(b) Behavior/design ambiguity → `/ca-adr`**, with the ambiguity statement and evidence ledger,
  authored only with explicit user attribution.
- **(c) No-action close** — symptom and rationale appended to
  `<project-root>/.codearbiter/open-tasks.md`.

A real finding that is out of scope for those exits is marked inline `[NEEDS-TRIAGE]` and the
investigation continues.

## When NOT to use

- Known bug with a named regression test → `/ca-fix` directly.
- Design discussion with no failing behavior → `/ca-adr`.
- New feature → `/ca-feature`.
- A general "why does it behave this way" question with no defect → `/ca-btw`.
- Re-entry from inside `/ca-fix` or `/ca-adr` → exit that command first (routing-cycle prevention).

## Hard gate

MUST NOT modify any code during Phases 1–5 — code changes belong to `/ca-fix`. MUST exit Phase 4 with
exactly one of (a)/(b)/(c). Exit (a) MUST carry a regression test obligation. Exit (b) MUST obtain
user attribution before any `/ca-adr`. MUST NOT promote INCONCLUSIVE evidence to CONFIRMED without a
cited source.
