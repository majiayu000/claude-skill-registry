---
name: pr-merge-base
description: Merge one or more PRs into the base branch with queue-like sequencing and conflict resolution. Use when merging PRs that may conflict with each other or the base, requiring ordered application and intelligent conflict handling.
---
# Smart Merge to Base Branch

Merge one or more PRs into the base branch (main/master) using queue-like sequencing.

## Process

1. **Detect base branch**: Identify the default branch (`main`, `master`, or repo-specific) via `git remote show origin` or repo conventions.

2. **Enumerate PRs**: List all PRs to merge. For each, fetch the latest HEAD.

3. **Create checkpoint**: Record the current base branch tip as a rollback point.
   ```
   CHECKPOINT=$(git rev-parse HEAD)
   ```

4. **Create integration branch**: Work on a temporary branch to validate before touching base.
   ```
   git checkout -b merge-queue/<timestamp> <base>
   ```

5. **Determine merge order**:
   - If the user specifies an order, use that.
   - Otherwise, compute dependency/topological order (if PR B depends on PR A, merge A first).
   - If PRs are independent with no clear ordering, present the list and ask the user to confirm or reorder before proceeding.

6. **Sequential merge with conflict handling** — for each PR in order:
   a. Attempt `git merge --no-ff <pr-branch>` into the integration branch.
   b. If merge succeeds cleanly, continue to next PR.
   c. If conflicts occur:
      - Analyze each conflict file using `difft` and codebase context.
      - Apply resolution using structural understanding (prefer base for formatting, PR for logic).
      - If a conflict cannot be resolved with confidence, **abort this merge** (`git merge --abort`), **stop and report** the conflict to the user with both sides and a recommended resolution.
   d. After each successful merge, verify the build still passes (if build commands are available).

7. **Validate integration branch**: Once all PRs are merged on the integration branch, run full build/test suite if available.

8. **Report results**: Present the validated integration branch to the user. Do NOT advance the base branch automatically — only update base if the user explicitly requests it.

9. **Abort conditions** — stop the queue and report if:
   - A conflict cannot be safely auto-resolved.
   - A post-merge build/test fails.
   - A PR has been superseded or closed.
   Roll back: `git checkout <base> && git branch -D merge-queue/<timestamp>` — base remains untouched at checkpoint.

## Output

Report for each PR: merged successfully, conflicts resolved (with details), or blocked (with reason).
