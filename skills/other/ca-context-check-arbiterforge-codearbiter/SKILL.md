---
name: ca-context-check
description: Optional manual drift audit — report stale provenance-tracked docs, then per stale doc offer re-scout, re-baseline, or defer. Not the daily loop; commit-gate auto-heal owns routine maintenance.
argument-hint: (none)
---

# /ca-context-check — manual drift audit

An optional, on-demand audit for bypass cases: a merge or external edit
changed a tracked source file you are not about to commit, so commit-gate's
auto-heal did not fire. Routes to the `context-check` skill.

## When to use

Use this only when you believe drift was introduced outside a commit (e.g. a
direct push, a merge you did not author, a manual file edit while outside a
normal commit workflow). The SessionStart drift line (backed by
`startup_drift_line`) is the usual signal that this check is warranted.

## When NOT to use

- **Routine maintenance** — commit-gate auto-heal runs automatically on every
  commit that touches a `drift_trigger` source. No manual intervention needed
  for the common case.
- Full brownfield re-scan from scratch → `/ca-create-context`.
- Project state snapshot → `/ca-status`.

## Hard gate

Read-only unless the user explicitly chooses re-scout (partial scout run) or
re-baseline (hash update in `.codearbiter/.provenance/`). MUST NOT commit on
its own. MUST NOT modify any derived doc without an explicit user selection.
