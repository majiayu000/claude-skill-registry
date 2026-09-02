---
name: simplify
description: 'Use when the user says "simplify this diff" or asks for a compression pass over a change-set. Decomposes the diff into reuse, quality, and efficiency axes; applies validated findings as atomic issue-class commits; auto-reverts regressions. Not for dead-code sweeps — use deslop.'
---

# Simplify: axis-decomposed compression pass on a diff

## Contract

| Field | Bound contract |
|---|---|
| Trigger | User asks to simplify a diff, PR, or branch: "simplify this diff", "tighten up", or "compress a change-set" |
| Authority | reversible-local: write only named local artifacts (working-tree and VCS commits); rollback via `git revert HEAD --no-edit` |
| Side effect | Applies simplification survivors as atomic issue-class commits to the working change-set; auto-reverts any commit that regresses |
| Done | Exit 0: simplification landed as issue-class commits, every fix commit is green, and no new bloat was introduced |

## Inputs

Must be supplied:
- An explicit diff scope or a base ref resolvable from HEAD

Optional:
- User-named files when no git context exists (unborn HEAD or no `.git/`)

Derived from the diff:
- Three parallel read-only review agents (reuse / quality / efficiency), each scoped to the diff

## Procedure

1. **Phase 1: Detect diff scope.** Capture every commit since the branch diverged from its base, including staged and unstaged changes. Do not guess the base. Resolve via the first base ref that exists, then run `git diff <base>`:
   1. `git merge-base HEAD origin/main`
   2. `git merge-base HEAD origin/master`
   3. `git merge-base HEAD main`
   4. `git merge-base HEAD master`
   5. `@{upstream}`

   If none of the five resolve, gate on two ordered checks:
   - Check A: `git rev-parse --verify HEAD 2>/dev/null`. If it fails, HEAD is unborn. Skip `git diff`; fall through to user-named files or no-git-context path.
   - Check B: only if Check A succeeded, `git rev-parse --verify HEAD^ 2>/dev/null`. If it fails, HEAD is the root commit. Use `git diff HEAD`. Surface: "scope: working-tree only, on root commit".
   - Otherwise: committed history exists but no base ref resolves. Print an explicit error and abort. Do not fall back to `git diff HEAD`; that would silently drop committed work.

   If no git context or HEAD is unborn, use user-named files supplied in the invocation. Empty after all valid resolutions → exit 11.

   **Explicit-base override:** `simplify against <ref>` bypasses the resolution above and runs `git --no-pager diff "<ref>"` directly.

   Done when: the diff is captured or an exit code is returned.

2. **Phase 2: Dispatch three review agents in one `task` call.** Issue a single `task` tool call with a `tasks` array of three items, never three sequential messages. Each agent receives `<axis-prompt from references/> + "\n\n---\n\nDIFF:\n" + <captured diff>`. All three agents are read-only; disjoint axes; independence asserted in the spawn message:
   > "Three agents dispatched in parallel. Axes are disjoint by construction: reuse-axis owns Graft (existing-utility detection), quality-axis owns Excess + Sprawl on code shape, efficiency-axis owns Excess + Sprawl on execution cost. All three agents are read-only; none edits files; none reads or writes shared mutable state."

   Agent type: `Explore` (read-only).

   Axes:
   - reuse (Agent 1): four rules (REPLACE, DUPLICATE, INLINE-COULD-USE-UTILITY, STDLIB-REIMPLEMENT). Detects new code written where a utility already exists.
   - quality (Agent 2): nine patterns (redundant-state, parameter-sprawl, copy-paste-variation, leaky-abstractions, stringly-typed, redundant-structural-nesting, nested-conditionals, unnecessary-comments, dead-code-unused-imports-exports). Detects unnecessary surface and structure without functional cause.
   - efficiency (Agent 3): seven patterns (unnecessary-work, missed-concurrency, hot-path-bloat, recurring-no-op-updates, unnecessary-existence-checks, memory-listener-leaks, overly-broad-operations). Detects work that need not happen and structure that bloats hot paths.

   See `references/orchestration.md` for the concrete dispatch shape and shell snippet.

   Done when: all three agents return their findings.

3. **Phase 3: Audit, then apply.** Wait for all three agents. Aggregate findings by `{axis, file, line, issue-class}`. Deduplicate identical cross-axis findings: keep each once, attribute it to the first reporter, and note the second axis as a co-signer. Dispatch a Reviewer agent (also `Explore`-typed and read-only) to audit the composed list for completeness, consistency, accuracy, and scope. The Reviewer's output is the **validated survivor set**. The orchestrator applies survivors directly, one issue class per atomic commit, and drops non-survivors without comment or re-adjudication. After each commit, run repo-native tests. On red, auto-revert via `git revert HEAD --no-edit` and stop that class's run.

   Commit sequencing by class:
   1. Duplicate commit: reuse-axis survivors + any other axis flagged `issue-class: duplicate`
   2. Excess-surface commit: quality-axis + efficiency-axis survivors flagged `issue-class: excess-surface`
   3. Structure commit: quality-axis + efficiency-axis survivors flagged `issue-class: structure`

   Commit message format: capitalized imperative subject, ≤50 chars target, ≤72 hard, no trailing period.

   After the final commit, audit the simplify patch itself for unneeded surface, duplicated logic, structure without cause, or a broken consumer contract. If the audit finds any, revert the entire simplify chain via `git revert <first-simplify-commit>^..HEAD --no-edit` and exit 14.

   Done when: all survivor commits are applied and green, or an exit code is returned.

## Failure and recovery
| Exit code | Trigger | Recovery |
|---|---|---|
| 0 | Clean | — |
| 11 | Empty diff after all fallbacks | Pass-through, no work to do |
| 12 | Findings emitted but survivor set empty after Reviewer audit | Report attached, no patch applied |
| 13 | Behavior regression on a fix commit | Offending commit auto-reverted; stop simplify run for that class; already-landed commits remain |
| 14 | Post-fix audit caught new bloat in the simplify patch | Entire simplify chain reverted; orchestrator may re-plan and re-invoke |
| 15 | Mixed-concern commit (bundles more than one issue-class) | Must split before merging |

Partial-result rule: commits already landed before a failure remain. A rollback does not revert previously successful class commits.

Non-mutation rule: sequential dispatch (not a single `task` call with a `tasks` array of three items) is rejected at the validation gate before any agent runs.

## Output
Terminal classification with an exit code. On exit 0: the change-set is compressed along reuse / quality / efficiency axes with one atomic commit per issue class, every fix commit green, and no new bloat introduced.
