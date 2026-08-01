---
name: ca-chore
description: Sanctioned lane for non-behavioral work — docs-only edits, dependency bumps, reverts. Type-scaled gates; no TDD demanded of prose.
argument-hint: "<docs|deps|revert> <description or SHA>"
---

# /ca-chore — non-behavioral change lane

The sanctioned path for work that has no behavioral surface to test-drive. Three types, each with
the gates that fit it — and nothing it doesn't need. Everything still exits through `commit-gate`
(classification `docs` / `chore` / `revert`) and lands via branch/PR.

## Types

**docs** — README, comments, CHANGELOG, `.codearbiter/` prose, typo fixes.
- Gates: secrets scan over the diff; diff review (no behavioral code change smuggled in);
  anti-slop copy pass on any user-facing doc in the change; `commit-gate`.
- **Anti-slop copy pass** — for any user-facing doc the change touches (repo-root community docs
  and `docs/**`; not codeArbiter's own framework bodies), load
  `<plugin-root>/includes/anti-slop-design/INDEX.md`, then `core.md` and the
  `medium-documents` leaf (§7.A.1), and run the §3.A em-dash ban and the §3.B copy self-audit over
  the authored prose before `commit-gate`. The `H-13` PostToolUse reminder surfaces §3.A separator
  dashes as you write, so the pass is a confirmation, not a discovery.
- No `tdd` — prose has no failing test to write.

**deps** — bump an existing dependency's version (manifest + lockfile together, never one without
the other).
- Gates: dispatch `dependency-reviewer` (same vetting as `/ca-add-dep` — license, provenance,
  supply chain, changelog of the bump); full test suite green after the bump; `commit-gate`.
- A bump that requires code changes to adopt is not a chore — route the code change through
  `/ca-feature` or `/ca-fix`.

**revert** — back out a named commit.
- Gates: `git revert <SHA>` (never hand-edited backout); full suite green after the revert; the
  commit message references the reverted SHA and the reason; `commit-gate`.
- No new regression test demanded — the revert restores already-tested behavior. If the revert is
  fixing a defect the suite missed, open `/ca-fix` afterward to pin it.

## Flow

1. Classify `$ARGUMENTS` into one of the three types. Anything with a behavioral code change beyond
   a mechanical revert is NOT a chore — redirect to `/ca-feature` or `/ca-fix` and stop.
2. Run the type's gates above.
3. Exit through `commit-gate` with the matching classification, then
   `finishing-a-development-branch` as usual.

## Hard gate

MUST reject a change containing behavioral code (beyond the revert itself) — that is `/ca-feature`
or `/ca-fix` territory. MUST keep manifest and lockfile changes in the same commit for `deps`.
MUST run the full suite for `deps` and `revert`. MUST run the anti-slop copy pass on any user-facing
doc a `docs` change authors or edits. Never skips `commit-gate`.

## When NOT to use

- Any new or changed behavior → `/ca-feature` / `/ca-fix`.
- Adding a NEW dependency → `/ca-add-dep`.
- Restructuring code → `/ca-refactor`.
