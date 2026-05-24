---
name: pr-merge-temporal
description: Merge multiple PRs into a temporal integration branch before merging to base, with ordered conflict resolution. Use when you want to validate a set of PRs together on a staging branch before advancing the base branch.
---
# Smart Merge to Temporal Branch

Merge multiple PRs into a temporal integration branch for validation before merging to base.

## Process

1. **Detect base branch**: Identify the default branch via `git remote show origin` or repo conventions.

2. **Enumerate PRs**: List all PRs to merge. For each, fetch the latest HEAD.

3. **Create temporal branch**: Fetch latest and branch from the remote base tip.
   ```
   git fetch origin
   git checkout -b temporal/<timestamp> origin/<base>
   ```

4. **Determine merge order**:
   - If the user specifies an order, use that.
   - Otherwise, compute dependency/topological order (if PR B depends on PR A, merge A first).
   - If PRs are independent with no clear ordering, present the list and ask the user to confirm or reorder before proceeding.

5. **Sequential merge with conflict handling** — for each PR in order:
   a. Attempt `git merge --no-ff <pr-branch>` into the temporal branch.
   b. If merge succeeds cleanly, continue to next PR.
   c. If conflicts occur:
      - Analyze each conflict using `difft` and codebase context.
      - Apply resolution using structural understanding (prefer base for formatting, PR for logic).
      - If a conflict cannot be resolved with confidence, abort (`git merge --abort`), stop, and report the conflict with both sides and a recommended resolution.
   d. After each successful merge, run available build/test commands to catch regressions early.

6. **Validate temporal branch**: Once all PRs are merged, run full build/test suite if available.

7. **Report results**: Present the validated temporal branch to the user. Do NOT merge into base automatically — only advance base if the user explicitly requests it.

8. **Abort conditions** — stop the queue and report if:
   - A conflict cannot be safely auto-resolved.
   - A post-merge build/test fails.
   - A PR has been superseded or closed.
   The temporal branch is abandoned: `git checkout <base>` — base remains untouched.

## Output

Report for each PR: merged successfully, conflicts resolved (with details), or blocked (with reason). Include the temporal branch name for user review.
