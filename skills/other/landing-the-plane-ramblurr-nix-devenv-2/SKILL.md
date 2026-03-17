---
name: landing-the-plane
description: Checklist for finishing work, pushing a branch, and opening a ready-for-review PR with tests and tracker updates. Use when asked to "land the plane"
---

# Landing the Plane

When someone asks you to "land the plane", they want you to wrap up the current body of work cleanly—no loose ends, no hidden surprises. Use this checklist any time that phrase shows up.

> **Non-negotiable:** you MUST complete ALL steps below. The plane is NOT landed until `git push` succeeds. NEVER stop before pushing. NEVER say "ready to push when you are!" - that is a FAILURE. Even if the work started on `main`, cut a feature branch, push it, create the PR, and flip it out of draft before you check this box.


**MANDATORY WORKFLOW - COMPLETE ALL STEPS:**

1. Cut a feature branch if needed, stage and commit (only the files relevant to the task). If there's a dirty index, and those files are not related to the task `git stash`

    Commit message rules:
    - Never mention beads, bd issues in the commit message
    - Never use emoji in the commit message
    - Never mention Claude/AI/LLMS/Coding Agents in the commit message
    - Do not list or mention files in the commit message (that is redundant, the commit itself has a list of files)
    - Do not include other redundant or obvious information
    - Use `git log -n 10` to look at past 10 commits, follow a similar commit message style (number of lines, casing etc)
    
2. File beads issues for any remaining work that needs follow-up
3. Ensure all quality gates pass (only if code changes were made) - run tests, linters, formatters, builds (file P0 issues if broken)
4. Update beads issues - close finished work, update status
5. **PUSH TO REMOTE - NON-NEGOTIABLE** - This step is MANDATORY. Execute ALL commands below:
   ```bash
   # Pull first to catch any remote changes (git stash if necessary to clean the working dir)
   git pull --rebase

   # If conflicts in .beads/beads.jsonl, resolve thoughtfully:
   #   - git checkout --theirs .beads/beads.jsonl (accept remote)
   #   - bd import -i .beads/beads.jsonl (re-import)
   #   - Or manual merge, then import

   # Sync the database (exports to JSONL, commits)
   bd sync

   # MANDATORY: Push everything to remote
   # DO NOT STOP BEFORE THIS COMMAND COMPLETES
   git push # add appropriate branch flags

   # MANDATORY: Verify push succeeded
   git status  # MUST show "up to date with origin/main"
   ```

   **CRITICAL RULES:**
   - The plane has NOT landed until `git push` completes successfully
   - NEVER stop before `git push` - that leaves work stranded locally
   - NEVER say "ready to push when you are!" - YOU must push, not the user
   - If `git push` fails, resolve the issue and retry until it succeeds
   - The user is managing multiple agents - unpushed work breaks their coordination workflow

5. **Clean up git state** - Clear old stashes and prune dead remote branches:
   ```bash
   # If you are NOT in a worktree:
   git remote prune origin       # Clean up deleted remote branches
   git switch main               # Switch back to main
   git pull --rebase             # Sync main with remote

   # But if you ARE not in a worktree:
   # then merge the worktree 


   ```
6. **Verify clean state** - Ensure all changes are committed AND PUSHED, no untracked files remain
7. **Choose a follow-up issue for next session**
   - Provide a prompt for the user to give to you in the next session
   - Format: "Continue work on bd-X: [issue title]. [Brief context about what's been done and what's next]"

**REMEMBER: Landing the plane means EVERYTHING is pushed to remote. No exceptions. No "ready when you are". PUSH IT.**


## 1. Quality Gates
- Run the full automated test suite plus linters/formatters that the project relies on *in the feature branch you’ll merge*.
- Confirm that the code you wrote is covered by automated tests; add or expand tests if any path would otherwise go unverified.
- When a review uncovers a bug/regression, follow this micro-loop before touching the fix:
  1. **Write (or extend) a failing test** that reproduces the issue. Default to a generative `proptest!` so the failing input can shrink and be re-run later.
  2. Run the pre-commit suite, commit that red test by itself, and push so the failing state is visible on the PR/branch.
  3. Implement the fix in a separate commit, push it, and reply to the original feedback thread with the fixing commit hash/summary.
  4. Ping the human reviewer to kick off the next review once the fix is in place.


## 2. Code & Repo Hygiene
- Strip out temporary logging, printlns, dbg! calls, feature flags, sleep statements, and other debug aids that should not ship.
- Remove throwaway files, scripts, or notes that were only needed during exploration.
- Remove untracked build artifacts, log files, or editor temp files that accidentally appeared. Ensure `.gitignore` is correct.


## 3. Tracking & Documentation
- Update/close beads issues ,ensuring status, notes, and acceptance criteria are satisfied.
- Refresh any affected docs (README, QUICKSTART, ADRs, runbooks, prompts/ documents) so they reflect the new reality.
