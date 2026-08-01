---
name: ca-adr-status
description: Report the health of Architecture Decision Records — aged, unchallenged, supersession candidates, unresolved CONFIRM-NN. Read-only.
argument-hint: "(none) | --adr N"
---

# /ca-adr-status — ADR health scan

Survey the health of recorded ADRs. Read-only — no file is modified. With `--adr N` the scan focuses
on a single ADR; with no argument it scans every ADR under
`<project-root>/.codearbiter/decisions/`.

## Routes to

The `decision-lifecycle` skill (`<plugin-root>/routines/decision-lifecycle/SKILL.md`) in its
health-scan mode. For each ADR it flags: aged decisions, `proposed` ADRs never challenged,
supersession candidates (a newer ADR or code pattern contradicts the decision), and unresolved
`[CONFIRM-NN]` placeholders. Findings aggregate into a structured report; nothing is changed.

## When NOT to use

- Author a new ADR → `/ca-adr`.
- Challenge or reconcile a specific ADR in depth → `/ca-reconcile`.
- Ask what a specific ADR says → `/ca-btw`.

## Hard gate

Read-only — MUST NOT modify any file. MUST NOT resolve a `[CONFIRM-NN]` found during the scan —
surface it and stop. A supersession candidate that contradicts an accepted ADR is flagged for
`/ca-conflict`.
