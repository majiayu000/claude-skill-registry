---
name: solve-issue
description: Claim exactly one issue, fix it, and create a pull request starting from a clean origin/master branch.
---

# Solve an Issue

Pick and solve exactly **one** issue, then create a PR.

## Workflow

0. **Preflight check** — before doing anything else, verify the branch is clean and up to date:

   ```bash
   git fetch origin
   ```

   Then check that:
   - `git status --porcelain` is empty (no uncommitted changes)
   - `git rev-parse HEAD` equals `git rev-parse origin/master` (no extra commits)
   - the current branch has **no open PR** (`gh pr list --head "$(git branch --show-current)" --state open --json number,title,url`)

   If any check fails, **stop immediately** and tell the user. Do not proceed — solve-issue must start from a clean branch that matches `origin/master` exactly and is not already tied to an open PR.

1. **Resolve a user-supplied issue argument** — only if the user explicitly passed an issue name/path. Use your judgment to determine the issue file they very obviously meant before invoking the claim script.

   Canonicalize the argument to the basename expected by `scripts/autoclaim_issue.py`:
   - Issue filenames are prefixed `p1-...`, `p2-...`, `p3-...`, `p4-...`, or `blocked-...`
   - If they passed `issues/<name>.json5`, strip the leading `issues/`
   - If they passed `<name>` without `.json5`, try `<name>.json5`
   - If they passed a path or near-exact basename that uniquely identifies one file under `issues/`, use that file's basename

   Do **not** silently switch to a different issue or auto-pick a replacement. If there is no single obvious match, **stop immediately** and ask the user to clarify instead of guessing.

2. **Check blocked issues** — before auto-claiming, check if any blocked issues deserve to be unblocked. Skip this step if the user explicitly passed an issue name.

   ```bash
   uv run python scripts/query_issues.py
   ```

   Look at the output. If any `blocked-` issue has **higher priority** (lower number) than the highest-priority unblocked issue:

   1. Read the blocked issue's JSON5 file — the `blocked` field is a string describing why it's blocked
   2. Investigate whether the blocker has been resolved: check the codebase, git history, external conditions described in the blocker string
   3. If the blocker **IS resolved**: remove the `blocked` field from the JSON, rename the file from `blocked-<name>.json` to `p{priority}-<name>.json`, and commit the change (include it in your working branch). Then claim that issue in step 3.
   4. If the blocker **is NOT resolved**: skip it and continue to step 3 with auto-claim

   This ensures high-priority issues don't stay blocked longer than necessary.

3. **Claim an issue** by running:

   ```bash
   uv run python scripts/autoclaim_issue.py
   ```

   This auto-picks the highest-priority unclaimed issue, skipping issues with a truthy `blocked` field (those have preconditions that need manual review). The `blocked` field can be `true` or a string describing the blocker.

   **Only if the user explicitly passed an issue name** (e.g. `/solve-issue populate-deck-strategies` or `/solve-issue issues/populate-deck-strategies.json5`), claim that resolved canonical issue instead:

   ```bash
   uv run python scripts/autoclaim_issue.py <resolved-issue-name>
   ```

   Never pick a specific issue on your own — always use the auto-pick unless the user told you which issue to work on.

   - If the script **succeeds** (exit 0): immediately inspect the current branch PR (`gh pr view --json body,url`) and extract the `<!-- claim: ... -->` tag from that PR body. Treat that PR claim tag as the authoritative claimed issue for all later steps. If there is no open PR or the claim tag is missing/mismatched, **stop immediately** and tell the user the claim workflow is inconsistent.
   - If you later merge `origin/master` and the claimed issue file was renamed (for example because issue filename prefixes changed), immediately update the PR body to use the new canonical `<!-- claim: ... -->` tag before continuing. `finalize_issue_pr.py` preserves the current PR tag verbatim.
   - If the script **fails** (exit 1 or 2): **stop immediately**. Tell the user no issue was claimed and do NOT proceed. You must not work on any issue you haven't successfully claimed — no exceptions. The claiming system prevents multiple Claudes from working on the same issue; bypassing it causes wasted work and merge conflicts.
4. **Check if already fixed** — before planning anything, check whether the issue was already resolved and the issue file just wasn't cleaned up. Do this by:
   - Finding when the authoritative claimed issue file was created (`git log --diff-filter=A -- issues/<filename>.json5`)
   - Reviewing git history since that date for commits that look like they address the issue
   - Reading the relevant code to see if the described bug/problem still exists
   - For debt-ratchet cleanup issues, verify the current enforcement file/path in the tree instead of trusting the issue text verbatim; related PRs can move a check from one test file to another while leaving the issue description stale
   - For lint-ignore cleanup issues, verify the underlying violation without the ignore in effect (for example `ruff check --isolated ...`); a normal lint run can still pass because the suppression you are trying to remove is active

   If the issue **is already fixed**: skip the planning/implementation steps entirely. Just delete the issue file, commit it, push, and finalize the PR as a cleanup. The PR title should be something like "Clean up outdated issue: \<title\>" and the body should briefly explain that the issue was already resolved (mention the commit or change that fixed it). Conceptually this is a zero-line fix — the only change is removing the stale issue file.

   If the issue **is NOT fixed**: continue to step 5.
5. **Enter plan mode** — explore the codebase, design your approach, and present it to the user for feedback before writing any code. This is the user's chance to redirect you if the approach is wrong.

   Start the plan with a short **issue context** recap in plain language: what the bug/task actually is, how it shows up today, and why the proposed fix addresses it. Do not assume the user remembers the issue details from when they filed it.

   **Your plan must end with this checklist** (copy it verbatim into your plan):

   ```markdown
   ## Post-implementation checklist
   - [ ] Implement the changes described above
   - [ ] Add/update tests
   - [ ] Run `make check` (lint, typecheck, tests)
   - [ ] Delete the issue file and include deletion in the commit
   - [ ] Run `/simplify` to review changed code
   - [ ] Push final changes: `git push origin HEAD`
   - [ ] Finalize PR: `uv run python scripts/finalize_issue_pr.py --title "..." --body "..."`
   ```

   This checklist survives the plan mode boundary and ensures no steps are skipped even if earlier context is compressed.
6. After the plan is approved, **create tasks** from the checklist using `TaskCreate`. Mark each task in_progress when you start it and completed when you finish it.
   - If `TaskCreate` is unavailable in the current Codex session, mirror the checklist in `update_plan` instead and keep the statuses current there.
7. Implement the fix. Push progress:

   ```bash
   git push origin HEAD
   ```

8. Update tests to expect the correct behavior
   - If your code changes prompt rendering, bridge responses, MCP tool output, replay behavior, or exported game data, proactively search existing goldens for the affected prompt fragment or behavior and regenerate every impacted golden before moving on. Do not assume a newly added golden is the only file that needs updating, and do not wait for CI to discover stale goldens you could have found locally.
9. Run `make check` to verify lint, typecheck, and tests pass

   - If you need live progress or a concrete failing sub-target, prefer `make check VERBOSE=1` over launching a second blind `make check`. The quiet wrapper can hide long-running child jobs, and overlapping retries leave duplicate Maven/pytest work chewing through the same branch.
   - If the quiet wrapper prints some target results and then appears stuck, inspect the listed failing sub-targets directly instead of waiting indefinitely. The expensive child jobs may already be done, and targeted reruns (`make format-check`, `make test`, etc.) recover the concrete failures faster.
   - For large Java refactors, especially under `Mage.Client.Bridge/`, use a module-scoped Maven loop for fast feedback while iterating (for example `mvn -pl Mage.Client.Bridge -DskipTests compile` or `mvn -pl Mage.Client.Bridge test -Dtest=...`). Still finish with the full `make check` before deleting the issue file or finalizing the PR.

10. Delete the issue file (e.g., `rm issues/<issue-filename>.json5`) and **include the deletion in the commit** — the issue removal must ship with the fix

    - If you merged `origin/master` after claiming, re-check whether the issue file was renamed (for example to add a priority prefix or `blocked-` prefix) and delete the renamed path that now exists on your branch.

11. **Document ALL issues you discover** during exploration, even if you're only fixing one. Future Claudes benefit from this documentation!
12. Run `/simplify` to review the changed code for reuse, quality, and efficiency, and fix any issues found. If `/simplify` is unavailable in the current session, do the equivalent manually by reviewing your diff for unnecessary duplication, dead code, and avoidable complexity, then continue.
    - While doing that manual review, inspect `website/package-lock.json` before you commit. `make check` / website tooling can add incidental `"peer": true` lockfile churn even when you did not intentionally change website dependencies; drop unrelated lockfile noise so the issue PR stays scoped.
13. Push final changes and finalize the PR. The script extracts the `<!-- claim: ... -->` tag from the current PR body and appends it to your new body automatically:

    ```bash
    uv run python scripts/finalize_issue_pr.py --title "<concise PR title>" --body "<PR description with summary, test plan>"
    ```

    The PR body must include a short **issue context** section near the top that explains what the original issue was and why this change fixes it. Write it for a reader who may not remember the issue they filed days earlier.

    Then mark the PR as ready-for-review.

14. **Watch CI and address feedback.** Run the watcher — it polls every 30s, returns as soon as any check fails or all pass (up to 30 min):

    ```bash
    uv run python scripts/watch_pr.py
    ```

    - **Exit 0** (all green, no comments): Done — leave remaining issues for the next Claude.
    - **Exit 1** (CI failed): The output lists failed checks with links. Investigate with `gh run view <run-id> --log-failed` (extract the run ID from the check URL). Fix the root cause, then do the full push-edit-watch cycle (see AGENTS.md § Pull Requests).
    - **Exit 2** (review feedback): The output lists top-level reviews, general comments, and inline diff comments. For inline comments, read the full context with `gh api repos/{owner}/{repo}/pulls/{number}/comments`. Address each one, then do the full push-edit-watch cycle.
    - **Exit 3** (both): Address both, then push-edit-watch.
    - **Exit 4** (timeout): Re-run this step.

    **Cap at 3 fix iterations.** If after 3 rounds CI still fails or new feedback keeps arriving, report the situation to the user and stop.

## Abandoning an Issue

If you determine an issue isn't worth fixing after claiming it, do **not** improvise claim cleanup. If the current tree has a documented abandon helper, use it. Otherwise stop, tell Gregor the issue should be abandoned, and wait for direction before touching the PR claim metadata manually.

Then restart from step 1 to pick a different issue.

## Is It Worth Fixing?

Not every quirk deserves a fix. For issues that seem one-in-a-million or where it's not realistically possible to determine the original author's intent, it's fine to give up and handle it gracefully. Being correct on fewer things is better than being _wrong_.

## Important

- One issue per PR — keeps PRs small and reviewable
- Don't chain multiple issues — after CI is green and feedback is addressed, stop
