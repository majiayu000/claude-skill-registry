---
name: ca-checkpoint
description: Periodic multi-reviewer sweep of the whole codebase — surfaces a triaged checkpoint report.
argument-hint: (none)
---

# /ca-checkpoint — codebase sweep

Periodic sweep of the entire codebase with the reviewer fleet, funneled to a single dated report. Surfaces findings — not a promotion gate, enforces no sign-off.

## Flow

1. Build the unit list — the same fleet as `/ca-review`, scoped to the whole codebase against the
   `<project-root>/.codearbiter/` docs:

   | Reviewer | Reads |
   |---|---|
   | `security-reviewer` | `security-controls.md`; reviews security posture |
   | `auth-crypto-reviewer` | `security-controls.md`; authn/crypto/key/secret paths |
   | `dependency-reviewer` | dependency manifests; license + supply-chain posture |
   | `migration-reviewer` | migration history; safety + classification |
   | `coverage-auditor` | test coverage vs. obligations across the tree |
   | `architecture-drift-reviewer` | `decisions/`; drift between code and accepted ADRs |

2. Route to `dispatching-parallel-agents` with that unit list (read-only batch). It dedupes, then
   funnels through `finding-triage` → `checkpoint-aggregator`.
3. `checkpoint-aggregator` writes the dated report to
   `<project-root>/.codearbiter/checkpoints/YYYY-MM-DD.md`: findings by severity with
   file:line, and out-of-scope items marked inline `[NEEDS-TRIAGE]`.
4. Write the current override **count** to `<project-root>/.codearbiter/last-checkpoint` — the
   integer baseline the startup briefing subtracts for its overrides-since-checkpoint counter. The value is
   the number of non-comment, non-blank lines in `overrides.log` at this moment (`0` if the log is
   absent). This re-zeros the `over:N` segment until the next `/ca-override`. Write a bare integer,
   not a timestamp — the briefing treats any value above the current total as stale and falls back
   to showing every override.
5. Report the checkpoint path.

## Hard gate

Read-only except writing the checkpoint doc and `last-checkpoint` — MUST NOT modify code. MUST NOT
consume raw reviewer output — only the `finding-triage` → `checkpoint-aggregator` verdict. MUST NOT
resolve a `[CONFIRM-NN]` surfaced during the sweep by guessing. The report surfaces findings; it does
not block or sign off anything.

## When NOT to use

- Reviewing just the current diff → `/ca-review`.
- A pre-implementation threat model → `/ca-threat-model`.
- ADR health only → `/ca-adr-status`.
- A whole-codebase deep audit → `/ca-tribunal` (checkpoint is the lean periodic sweep; tribunal its rare deep counterpart).
