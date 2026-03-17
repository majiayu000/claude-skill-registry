---
name: lambda-workflow
description: One lifecycle for Lambda repos: choose a bd task, start work, land the PR, and watch GitHub via Dumbwaiter MCP until it merges.
---

# Lambda Workflow

Use this skill whenever you touch delivery end-to-end—from grabbing a bd issue through merge/closure. Each phase builds on the last; do not skip ahead unless a human explicitly says so.

## Lifecycle Map
1. **Select & Claim Work** – pick an unblocked bd issue, understand scope, and claim it 
2. **Kick Off & Draft** – baseline tests, branch, and open a draft PR immediately so CI starts.
3. **Build & Validate** – implement with tests-first habits, keeping trackers and notes fresh.
4. **Land the Plane** – ready-for-review PR with full test/QA + repo hygiene.
5. **Monitor & Respond** – use the Dumbwaiter MCP to wait on GitHub signals (checks, reviews, comments, merge) and react.
6. **Close the Loop** – sync bd/dcos, close the issue, and record proof the change stuck.

## 1. Select & Claim the bd Task
- If `.beads/beads.db` is missing (fresh clone, new worktree, etc.), run `bd init --json` from the repo root so the local database hydrates from `.beads/issues.jsonl` before listing work.
- You may be handed a task: if so, choose that one. Otherwise, run `bd ready --json -n 0` before asking for work; respect blockers/dependencies, pick the first ready task and claim it. `bd update <id> --status in_progress --notes "Starting work on ${task description}"`.
- Commit the issues.jsonl changes immediately on main and push. This avoids multiple agents pulling the same task. If you get a conflict, revert the issues.jsonl changes, pull with rebase, and try again.
- Read the issue (and linked docs) end-to-end. Confirm acceptance criteria, implicit contracts, and dependent tasks. It is possible it is in a partially complete state: if so, pick up where it was left off.
- Clarify gaps before coding. Update the bd ticket with questions or new discoveries so history lives in `.beads/issues.jsonl`. Again, push these changes (and only these changes) directly to main.

## 2. Kick Off & Draft the PR
1. **Baseline the repo**
   - Sync with `git fetch --all` and `git pull --rebase origin main`.
   - Run the project’s test suite. If it fails on `main`, stop and escalate instead of piling on.
2. **Branch + tooling**
   - Create a fresh branch (`git checkout -b <short-task-name>`). Never work directly on `main`.
   - Verify `gh auth status` (or equivalent) so PR automation works later.
3. **Immediate draft PR**
   - Push the branch and open a **draft** PR sourced from the bd summary/acceptance criteria, including any questions or underspecified areas.
   - Preferred helper: `gh pr create --draft --title "..." --body-file body.md`. Be wary of quoting issues, it's easy to end up with "\n" characters in the PR.
   - Capture acceptance criteria + planned tests in the PR body so reviewers know how you’ll prove success.
4. **Plan validation**
   - Decide which automated + manual tests will prove the work. Note the plan in bd or the PR so it is reviewable before implementation.

## 3. Build & Validate Continuously
- Keep `git status -sb` clean; commit coherent checkpoints and push often so the draft PR reflects reality. Pull and rebase over origin/main before pushing each time.
- Treat failing feedback as a test design task:
  1. Write or extend a failing test that reproduces the bug/regression (default to `proptest!` or integration coverage when stateful sh loops).
  2. Run the suite, commit/push the red test alone.
  3. Fix the bug in a follow-up commit, push, and reply to the review thread with the fixing hash/summary.
- Strip debug aids (`dbg!`, `println!`, temporary flags) before moving to landing.
- For transactional upgrade/apply loops, add coverage that proves: atomic rollback on failure, lockfile sync after success, cross-device safety (rename EXDEV), and symlink preservation.
- You will commonly discover unexpected tasks while building; if they are directly necessary for the success of this task, add a bd subtask blocking this task and work on it first, on the same PR. If they are not, add them as discovered-from tasks in bd and continue, they can be done in the next round.

## 4. Land the Plane (Ready for Review)
1. **Quality gates**
   - Run the full suite (tests, linters, formatters) on the feature branch to a green state **after** your last rebase.
   - Add or expand tests until every change path is covered.
2. **Repo hygiene**
   - Remove throwaway files, logs, and manual scripts. Ensure `.gitignore` keeps artifacts out.
   - Rebase on the latest `main`, squash/reorder into meaningful commits, and confirm no stray stashes remain (`git stash list`). Make sure you only squash/reorder your commits! Commits must all be rebased on top of origin/main.
3. **PR**
   - Flip the draft PR to Ready using `gh pr ready` once all our tests pass, and we think the acceptance criteria are met. Close the bd task *now*, update bd notes with the PR URL, testing evidence, and any deviations from the original plan, and push.
   - Update the PR body with: summary, testing notes, linked bd issue, and known follow-ups.
   - Trigger automated review with a comment containing exactly `@codex review`; reply inline to every Codex comment with the commit hash that fixes it.

4. **Tracking**

## 5. Monitor & Respond with Dumbwaiter MCP
Once the PR is Ready, hand monitoring to the Dumbwaiter MCP so you don’t poll GitHub manually.

1. **Start a wait** (via MCP tools or `mcp__dumbwaiter__wait.start`):
   ```json
   {
     "provider": "github",
     "selector": { "owner": "ORG", "repo": "REPO", "pr": 123 },
     "condition": "checks_succeeded"
   }
   ```
   Capture the returned `wait_id`.
2. **Await completion**
   - Call `wait.await` with that `wait_id` to stream progress notifications (check statuses, workflow runs, etc.).
   - Use other conditions as needed: `pr_merged`, `checks_failed`, `comment_received` (plus filters), `changes_requested`, or `workflow_completed`.
   - If you only need polling, call `wait.status` on an interval; cancel via `wait.cancel` if superseded.
3. **React to outcomes**
   - On green checks → post the success + `wait_id` back to bd/PR notes.
   - On failures or change requests → surface the failing context and return to step 3. 
   - For comment streams, enable `condition: "comment_received"` with `filters.since` so every new review/comment notifies you in real time.
   - On merge, we're done, report success to user.
   - On approval: if we got approval _and_ we are in ready-for-review _and_ all the checks are passing _and_ we are rebased on top of origin/main, we are also done, but in this case we should report back to the user that the PR can now be merged, along with the URL of the PR for easy access. If everything but the rebasing is done, we can rebase and try again, again commenting "@codex review" after the commit lands and the tests pass in CI.

4. **Background durability**
   - Set `DUMBWAITER_DB` and `DUMBWAITER_WATCHER=1` if you need waits to survive process restarts. Always log the `wait_id` in bd so another agent can resume with `wait.status`.

## 6. Close the Loop
- After Dumbwaiter reports `pr_merged`, archive local branches/stashes so the next effort starts clean.

Following this workflow keeps the entire Lambda lifecycle observable: bd reflects intent, GitHub shows work-in-progress via draft PRs, Ready PRs meet the landing checklist, and Dumbwaiter MCP watches the PR until it merges.
