---
name: worktree
description: 'Use when work needs an isolated git worktree: new work, an existing ref, a gated feature workspace with baseline tests, or a manifest-tracked loop run. Not for plain branches: use create-branch.'
---

# Worktree isolation

## Contract

| Field | Bound contract |
|---|---|
| Trigger | A new isolated worktree or branch is requested, an existing ref or PR needs isolation, feature work needs a gated workspace with setup and baseline tests (feature-gate mode), or a run needs a manifest-tracked worktree (loop-run mode). |
| Authority | Reversible local: writes only the worktree directory, `.worktrees/` or `.loop-worktrees/` entries, a gitignore entry, symlinked hooks, and manifest bookkeeping; rollback is removing the worktree and reverting those entries. Loop-run mode never passes `--force` to `git worktree remove`. No remote mutation. |
| Side effect | Local write: creates or attaches an isolated git worktree and reports its exact path and status. Feature-gate mode also runs setup and the baseline test suite. Loop-run mode also maintains a status manifest under `.loop-worktrees/`. |
| Done | An isolated workspace exists that the harness can see and manage, with no phantom state. Feature-gate mode adds a green baseline suite or a surfaced failure. Loop-run mode adds a manifest where every worktree has a legal status and no removal used `--force`. |

## Inputs

1. Mode (required): one of `new-work`, `isolate-existing-ref`, `feature-gate`, `loop-run`. Default `new-work` when no ref is named and no gate or lifecycle is requested.
2. Ref to isolate (`isolate-existing-ref` only): a PR head, branch, or commit.
3. New branch name (optional): derived from the work description when omitted.
4. Base branch (optional): defaults to origin's default branch, else `main`.
5. Setup command (`feature-gate`, optional): project setup to run inside the worktree, for example `pnpm install --frozen-lockfile`. When omitted, no setup step runs.
6. `runId` (`loop-run`, required): unique run identifier used verbatim as a path segment and branch suffix; a single path segment (no `/`, not `.` or `..`).
7. `pattern` (`loop-run`, required at create): short work-pattern label kept on the manifest entry for audit.
8. Status for mark (`loop-run`, required): exactly one of `active`, `rejected`, `escalated`, `merged`, `stale`.
9. Cleanup set (`loop-run`, optional): status CSV, default `rejected,escalated`, plus an optional age cutoff `<n>` + `s|m|h|d` (for example `24h`).

## Procedure

1. Determine the mode from the inputs. Do not create a worktree for single-task work that can happen on a branch in the current checkout. Done when: the mode is decided and single-task work is ruled out.
2. Detect existing isolation before creating anything. Compare the resolved absolute git dir against the resolved absolute common git dir: run `git rev-parse --absolute-git-dir` and `(cd "$(git rev-parse --git-common-dir)" && pwd -P)`. If they are equal, this is a normal checkout; continue to step 3. Done when: the isolation state is known (normal checkout, submodule, or already isolated).
3. If the two paths differ, run `git rev-parse --show-superproject-working-tree`. Non-empty output means a submodule: in feature-gate mode stop and report that isolation must run from the superproject; in other modes treat it as a normal checkout and continue to step 4. Empty output means the run is already in an isolated worktree: report the worktree path (`git rev-parse --show-toplevel`) and current branch. In new-work and feature-gate modes proceed in place and skip to the mode steps. In isolate-existing-ref mode check the named ref out here unless it is already the current branch, then stop. Do not create another worktree. Done when: either already-isolated is handled, or the normal-checkout path continues to step 4.
4. Prefer the harness's native worktree primitive (for example Claude Code's `EnterWorktree`, a `/worktree` command, or a `--worktree` flag). Use it and continue to the mode steps. A behind-the-back `git worktree add` creates phantom state the harness cannot see, navigate to, or clean up. Done when: a native tool created the worktree, or no native tool exists and the git fallback is the next step.
5. If no native tool exists and steps 2-3 found no existing isolation, fall back to manual git worktree creation following `references/git-fallback.md`. In feature-gate mode, if creation fails (disk full, path conflict, locked index), fall back to in-place work on the current branch and report the fallback reason. Done when: the worktree exists under `.worktrees/` and the harness can see it via the tracked convention, or the feature-gate fallback is reported.
6. Mode `feature-gate`: after the worktree exists (or in place after a fallback), run these steps in order.
   a. Gitignore entry: if the worktree directory is not already matched by `.gitignore`, add an entry for it and commit the change; skip when already ignored. Done when: the worktree directory is ignored by git.
   b. Symlink hooks: locate the parent repository's hooks directory via `git rev-parse --git-common-dir` from the worktree and symlink the worktree's hooks directory to it so shared hooks apply; on failure (permission, cross-filesystem) report it and continue without hooks. Done when: hooks are linked or the failure is reported.
   c. Run setup: if a setup command was supplied, execute it inside the worktree (or in place after fallback); on non-zero exit surface the error and stop. Done when: setup exits zero or the error is surfaced.
   d. Gate on baseline tests: run the project's baseline test suite inside the worktree (or in place); on failure surface the failures and ask the user to proceed or investigate. Done when: the baseline suite is green, or failures are surfaced with a proceed-or-investigate question.
7. Mode `loop-run`: manage the run under `.loop-worktrees/` with these steps.
   a. Bind the root: run `git rev-parse --is-inside-work-tree`; on failure stop without mutating. The manifest is `.loop-worktrees/manifest.json` shaped exactly `{"version":1,"worktrees":[]}`; the mutex is `.loop-worktrees/.manifest.mutex`. If the manifest exists in any other shape, stop; never rewrite an unvalidated manifest. Add `.loop-worktrees/` to `.gitignore` so worktree contents never enter the index. Done when: the root is bound and the manifest shape is validated.
   b. Serialize manifest mutations with the mutex: before each read-modify-write, create the mutex with exclusive create; if it exists and its mtime is older than 30 seconds, remove it and retry; otherwise retry after a short backoff until a 30-second deadline, then fail naming the mutex path. Delete the mutex when the mutation ends, success or failure. Pure reads take no mutex. Done when: each mutation ran under the mutex and the mutex is released.
   c. Create: refuse a `runId` that is not a single path segment. Under the mutex, read the manifest: if an entry with the same id has status `active`, refuse and name its existing path. Otherwise run `git worktree add -b loop/<runId> .loop-worktrees/<runId> <base>`, which creates the branch and checks it out in one step. Replace any prior entry with the same id and append `{"id":<runId>,"path":".loop-worktrees/<runId>","branch":"loop/<runId>","baseBranch":<base>,"pattern":<pattern>,"createdAt":<ISO-8601 UTC>,"status":"active"}`. Write the manifest atomically: write a temp file in the same directory, then rename it over `manifest.json`. Done when: the worktree and branch exist and the manifest records them atomically.
   d. Mark: under the mutex, reject any status outside the five-value set; find the entry by id or fail naming the id; set its status; write the manifest atomically. Never delete entries to record outcomes; removal happens only in cleanup. Done when: the entry carries the new legal status.
   e. Cleanup: under the mutex, select entries whose status is in the requested set (default `rejected` and `escalated`; `active` is never selected, so mark a finished run terminal first) and, when a cutoff is given, whose `createdAt` is older than now minus the cutoff. For each selected entry run `git worktree remove .loop-worktrees/<id>` without `--force`; a git refusal, typically uncommitted or untracked files, is recorded as skipped with its reason and the entry stays in the manifest. Rewrite the manifest without the removed ids, atomically. Done when: every selected entry is removed or recorded as skipped with its reason.
   f. Reconcile: list git worktrees with `git worktree list --porcelain` and compare paths under `.loop-worktrees/` against the manifest. Worktrees registered with git but missing from the manifest are orphans: report them, and remove one only on explicit instruction, still without `--force`. Drop manifest entries whose directory no longer exists with an atomic manifest write. Treat a missing path as absent, not an error, since `rm -rf`, a crash mid-cleanup, or a container wipe can leave git listing a prunable entry. Done when: manifest and disk agree, or every divergence is reported.
8. Report the worktree's absolute path and current branch, and confirm the harness can see it (native tool) or that it lives under the tracked `.worktrees/` or `.loop-worktrees/` convention (git fallback). Done when: the path, branch, mode, and creation method are reported.

## Failure and recovery
- Already in an isolated worktree: do not create another. Report the existing path and proceed in place (new-work, feature-gate) or check out the named ref there (isolate-existing-ref).
- Ref already checked out elsewhere: report the existing checkout path; never create a second worktree for the same branch. Let the caller work in place or create a detached worktree at the same commit.
- "Worktree already exists": switch to it (`cd .worktrees/<branch>`) or remove it (`git worktree remove .worktrees/<branch>`) before recreating.
- "Cannot remove worktree: it is the current worktree": `cd` out first, then remove.
- Sandbox or permission error on `git worktree add`: report the failure and ask the user for a blocking decision (work in the current checkout vs stop). Work in the current checkout only on explicit confirmation. In feature-gate mode, fall back to in-place work on the current branch and report the fallback reason.
- Submodule detected in feature-gate mode: stop and report that isolation must run from the superproject.
- Hook symlink fails (feature-gate): continue without hooks and report the failure.
- Setup command exits non-zero (feature-gate): stop, surface the error output, and do not proceed to the test gate.
- Baseline tests fail (feature-gate): surface the failures and ask the user to proceed with the isolated workspace or investigate first.
- Not a git repository (loop-run): stop before any mutation.
- Manifest in an unexpected shape (loop-run): stop without rewriting; report the corrupt manifest as the blocked result.
- Mutex deadline of 30 seconds (loop-run): fail naming `.loop-worktrees/.manifest.mutex`; if no other process is running, a mutex older than 30 seconds is cleared by the stale rule on the next attempt.
- `runId` already active (loop-run): create refuses; reuse the existing worktree or pick a new id; never double-create.
- `loop/<runId>` branch already exists (loop-run): surface the git refusal, then use a new id or explicitly delete the leftover branch from a prior attempt with the same id.
- Unrecognized status (loop-run): mark refuses before touching the manifest.
- Manifest write fails after `git worktree add` succeeded (loop-run): roll back to the pre-call state with `git worktree remove .loop-worktrees/<runId>` then `git branch -D loop/<runId>` (the branch points at the base, so nothing unique is lost), then rethrow; if the worktree removal is refused, report the path as an orphan for reconciliation instead of forcing it.
- Cleanup removes nothing on a freshly marked entry (loop-run): the age cutoff is working; this is expected, not a silent failure.
- Non-converged: if isolation cannot be established and no fallback is confirmed, return the blocked result with the exact error and the paths inspected. Never claim the done predicate holds.

Partial-result rule: every manifest write is tmp-then-rename inside the mutex, so readers never see a torn file, and every worktree on disk is either registered or rolled back. No step is skipped without a reported reason.

## Output
- `new-work` and `isolate-existing-ref`: the isolated worktree's absolute path, current branch, mode used, and creation method (native tool or git fallback); or the existing worktree path and branch if already isolated.
- `feature-gate`: the workspace path and branch plus confirmation that the baseline suite is green; on in-place fallback, the current directory, branch, fallback reason, and test status; on test failure, the failure summary with a proceed-or-investigate question.
- `loop-run` create: the registered entry's worktree path, branch, and base branch. Mark: the entry id and its new status. Cleanup: `removed <path> (<status>)` and `skipped <path>: <git reason>` lines with counts. Reconcile: orphan paths and dropped entry ids. Reads: manifest rows `<status> <id> <branch> (<pattern>)`.
- Terminal classification: done only when the Done predicate for the active mode holds; otherwise blocked with the exact error and the paths inspected.
