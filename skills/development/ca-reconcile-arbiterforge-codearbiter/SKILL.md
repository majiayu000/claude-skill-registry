---
name: ca-reconcile
description: SMARTS arbitration — reconcile architectural artifacts against the scaffold and prior decisions; every variance resolved by an explicit, user-attributed choice.
argument-hint: "(none) | \"<ADR-id | artifact | scope>\""
---

# $ca-reconcile — architectural arbitration

Reconciles the project's architectural artifacts against the scaffold and prior decisions, or challenges a specific ADR that is wrong, stale, or in conflict with another. Presents SMARTS analyses and recommendations but never arbitrates — every variance is resolved by an explicit user choice recorded in the decision log with user attribution. With no argument it runs a full reconciliation pass; an argument scopes it to a named ADR, conflict, or artifact.

## Routes to

The `decision-variance` skill (`${CLAUDE_PLUGIN_ROOT}/routines/decision-variance/SKILL.md`). It locates
the three architectural artifacts by exact filename — `01-architecture-breakdown.md`,
`02-phased-build-plan.md`, `03-task-backlog.md` (under `<project-root>/.codearbiter/plans/`) —
and indexes the append-only decision log at
`<project-root>/.codearbiter/decisions/decision-log.md`. It MAY dispatch the
`decision-challenger` agent (`${CLAUDE_PLUGIN_ROOT}/agents/decision-challenger.md`) to stress-test an
in-scope ADR — optional, not forced. Each variance ends in one of three user-chosen outcomes:

1. **Ratify** — the existing decision stands; the SMARTS analysis and re-affirmation are logged.
2. **Supersede** — a new decision is recorded by appending a log entry whose `Supersedes:` references
   the prior one; a replacement ADR is authored via `$ca-adr`.
3. **Surface as `[CONFIRM-NN]`** — unresolvable now; a numbered placeholder is added to
   `<project-root>/.codearbiter/open-questions.md`.

## When NOT to use

- Author a brand-new ADR with no prior conflict → `$ca-adr`.
- Check ADR health (aged, unchallenged, unresolved CONFIRM-NN) → `$ca-adr-status`.
- A general architectural discussion without recording a decision → `$ca-btw`.
- A rule conflict between project docs and code → `$ca-conflict`.
- Routine git text-merge conflicts — this is architectural reconciliation, not merge resolution.

## Hard gate

MUST NOT record an arbitration decision without an explicit user choice; decline "you decide" /
"use your best judgment" with a structural refusal (the only delegation is the user verbatim accepting
the recommendation, logged as such in `Decided by:`). MUST match the three artifacts by exact
filename. The decision log is append-only — MUST NOT edit or rebuild a prior entry; supersede by
appending. MUST NOT modify the artifacts, scaffold, or code to "fix" a variance. MUST NOT author an
ADR as the disposition of a routine finding — ADRs are authored only via `$ca-adr` with user
attribution.
