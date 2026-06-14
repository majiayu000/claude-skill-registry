---
name: review-fix-grill-loop
description: Grill the current changes — fan out parallel review subagents over the working-tree + branch-vs-base diff, resolve each confirmed finding with multiple architectural solutions, fix in verified batches with auto-revert, re-review only changed files, and loop until no critical/high/medium finding remains. Use when the user says "grill my changes", "review-fix loop", "review and fix my diff until clean", "keep reviewing and fixing until no issues", or "grill loop". Diff-scoped sibling of audit-project (whole-project) with a resolve stage and a medium severity floor.
metadata:
  short-description: Diff-scoped review→resolve→fix loop until clean
---

# Review-fix-grill-loop — diff-scoped review→resolve→fix loop

`review-fix-grill-loop` is a `correct` op-cell. It restores the invariant: **no open finding at or above the severity floor (confidence ≥ medium) remains in the current change-set.** It is not a one-pass critique — it selects reviewers from the diff, resolves each confirmed finding with three architectural solutions, fixes in verified batches with auto-revert, re-reviews only changed files, and stops only at a clean diff, a user decision gate, the iteration cap, or a stall.

**Self-contained by design.** This skill bundles its own `references/review-roster.md` and `references/false-positive-contract.md`, copied and adapted from `audit-project`. They share an ancestor with that skill; a canonical edit to one must be hand-propagated to the other (no CI enforces it). Orchestration specifics — change-scope resolution, severity floor, resolve gate, double-loop — live in `references/orchestration.md`.

## When to Apply / NOT

Apply when the user wants their **current changes** reviewed and fixed iteratively until clean: a dirty working tree, a feature branch, "grill my diff", "review and fix until no issues".

NOT:
- Whole-project / release-readiness audit → `audit-project` (this skill is diff-scoped by contract; widening to `.` means you wanted `audit-project`).
- Read-only opinion, no fixes → `review`.
- Behavior-preserving compression only → `simplify`.
- A single known verifier failure or bug → `fix`.
- GitHub PR review comments → `gh-address-comments`.

## Inputs and Flags

- `scope` (optional path/glob/ref) — overrides the change-set default; grills that path instead of the resolved diff.
- `against <ref>` — explicit base-ref override for diff resolution (mirrors `simplify against <ref>`).
- `--severity-floor <critical|high|medium>` — terminating floor; default `medium`.
- `--max-iterations N` — outer-loop cap; scope-adaptive (default tier `5`, grows to `15` with change-set complexity per `references/orchestration.md`); an explicit value overrides the derived cap.
- `--quick` — single review pass; no resolve, no fix, no loop. Reports findings and exits.
- `--domain <reviewer>` — run one reviewer domain only; same consolidation contract applies.
- `--resume` — load `.outline/review-fix-grill/queue.json` if present and continue. A queue written before scope-adaptive caps lacks `caps`; re-derive it from `changedFiles[]` (Phase 2) on resume rather than assuming a scalar `maxIterations`.

## State and Artifacts

- `.outline/review-fix-grill/queue.json` — scope, floor, selected reviewers, raw + consolidated findings, `resolveDecisions[]`, `belowFloor[]`, verification results, decisions, hash history. Schema in `references/false-positive-contract.md`.
- `.outline/review-fix-grill/iterations/<n>.json` — per outer iteration: changed files, fix batches, verifier command/output summary, re-review hash.

Distinct directory from `.outline/audit/` so a `--resume` never cross-reads `audit-project`'s queue.

## Workflow

Full recipes live in the references; the phase order is:

1. **Resolve change-scope** — three-source union (tracked diff vs base, staged, untracked-not-ignored) per `references/orchestration.md` Phase 1. Empty union → exit, launch no agents. The resolved `changedFiles[]` is the only universe for every later phase.
2. **Detect shape + signals** — compute framework flags and priority signals over `changedFiles[]` only.
3. **Review (parallel)** — select ≤10 reviewers (4 core: `code-quality`, `security`, `performance`, `test-quality`; conditional by diff surface). Dispatch in one parallel batch with role prompts from `references/review-roster.md` and the mandatory JSON schema. Reviewers are read-only and return JSON only.
4. **Consolidate** — apply `references/false-positive-contract.md` exactly: normalize, honor dismissals only with non-empty reason, dedupe, blocked-ratio gate **before** any zero-check, extract below-floor findings to `belowFloor[]`.
5. **Resolve gate** — for each confirmed open at-or-above-floor finding, emit `VALID/NOT-AN-ISSUE/NEEDS-CLARIFICATION` + three distinct solutions + a recommendation + in-scope/out-of-scope. `NEEDS CLARIFICATION` and `out-of-scope` escalate to `AskUserQuestion`; the rest feed the fix queue with the recommended approach. Spec in `references/orchestration.md`.
6. **Fix (verified batches)** — reuse the `fix` loop in findings mode: one minimal patch per attempt, checkpoint commit, repo-native verifier + guard, KEEP on green / `git revert HEAD --no-edit` on red, up to `caps.attemptsPerItem` attempts per item (scope-adaptive `3–5`, = initial + reworks) before SKIP. Refuse on protected branches (`main`/`master`/`release/*`) before entering the loop. Verifier discovery per `fix/references/verifiers.md`.
7. **Targeted re-review + loop** — re-review changed files only (contract routing), re-consolidate, re-run the blocked-ratio gate, then test the loop condition.

**Loop condition:** `openAtOrAboveFloor > 0 && iteration < caps.maxIterations`, counting only `severity ≥ floor && confidence ≥ medium`. At each iteration boundary with findings remaining, fire the decision gate (`continue-fixing` / `create-issues-for-rest` / `move-remainder-to-debt` / `leave-in-queue`); a repeated stall hash drops the `continue-fixing` recommendation.

**Double loop:** both caps are scope-adaptive (derived in Phase 2, see `references/orchestration.md` "Scope-adaptive caps"). The outer cap (`caps.maxIterations`, `5–15`; `--max-iterations` overrides) counts review→resolve→fix→re-review cycles; the inner `fix` cap (`caps.fixAttemptCap`, `20–80`) counts fix attempts within a batch. Keep the two counters distinct in any progress output.

## Completion

Complete only when one is true:
- zero open at-or-above-floor findings after consolidation and re-review;
- the user chose a deferral path at a decision gate;
- the iteration cap was reached and queue/below-floor artifacts are current;
- a stall was surfaced and the user deferred.

Report: change-scope + base ref, selected reviewers, outer iterations, critical/high/medium fixed, remaining at-or-above-floor, below-floor count, resolve decisions (including any out-of-scope escalations), verifier commands run, regressions rolled back, queue path.

## Anti-patterns

- **Widening to the whole repo.** This skill grills the diff; `.` is `audit-project`'s job.
- **Looping on low / style nits.** The floor + confidence guard exist to prevent that; do not chase low-confidence subjective findings.
- **Silently widening the diff to fix a finding.** Out-of-scope fixes escalate to the user, never auto-apply to unchanged files.
- **Fix before resolve/consolidation.** Raw reviewer output is untrusted until deduped, false-positive-checked, and resolved.
- **Honoring empty false-positive flags.** Dismissal without a reason is forced open.
- **Suppressing tests or guards** to land a fix. Never disable a verifier.
- **Shipping placeholders.** "TODO: fix later" is a failed grill fix.

## Validation Gates

| Gate | Pass Criteria | Blocking |
|---|---|---|
| Change-scope resolved | Non-empty three-source union (tracked diff + staged + untracked); empty → clean exit, no agents | Yes |
| Context detected | Framework flags + priority signals over changed files collected or marked unavailable | Yes |
| Caps derived | `scopeTier` + `caps.{maxIterations,fixAttemptCap,attemptsPerItem}` computed in Phase 2 and persisted to the queue (re-derived on `--resume` if absent) | Yes |
| Reviewer roster selected | 4 core + justified conditional reviewers (≤10 total), OR exactly the single reviewer named by `--domain` | Yes |
| Parallel dispatch | Selected reviewers launched in one batch with role prompts + schema | Yes |
| Findings schema valid | Every finding has file, line, severity, category, description, suggestion, confidence, false-positive fields | Yes for queue ingestion |
| False-positive contract | Empty-reason dismissals forced open; blocked-ratio gate before zero-check | Yes |
| Below-floor extracted | Sub-floor + low-confidence findings routed to `belowFloor[]`, not the fix queue | Yes |
| Resolve gate executed | Each confirmed at-or-above-floor finding has a recorded resolve decision; out-of-scope/needs-clarification escalated | Yes |
| Fix verification | Repo-native verifier run after every batch | Yes when a verifier exists |
| Regression rollback | Failing batch reverted with `git revert HEAD --no-edit` and noted | Yes |
| Targeted re-review | Only changed files re-reviewed | Yes |
| Stall detection | Identical open at/above-floor hash twice triggers decision gate | Yes |
| Completion invariant | Zero open at/above-floor or explicit user deferral path | Yes |

Under `--quick` the loop terminates after consolidation + below-floor extraction; the resolve, fix-verification, regression-rollback, targeted-re-review, and completion-invariant gates apply only to the full loop and are bypassed.

## See also

- `audit-project` — whole-project sibling; shares the roster + contract ancestry.
- `review` — read-only branch review, no fixes.
- `simplify` — behavior-preserving compression of a change-set.
- `fix` — the verified-batch fix loop this skill reuses.
- `resolve` — the validity + multi-solution analysis this skill's resolve gate is modeled on.
