---
name: pr
description: Prepare and open a pull request for the current branch after validating the full diff and checks.
---

# Make a PR

Create a pull request for the current branch's changes.

## Workflow

1. **Commit any uncommitted work.** Check `git status` — if there are staged or unstaged changes, commit them before proceeding. Everything that's part of this PR should be in a commit.

2. **Understand the full scope of changes.** Run these in parallel:

   ```bash
   git fetch origin
   git log --oneline origin/master..HEAD
   git diff origin/master..HEAD --stat
   ```

   Read through the actual diffs and changed files — don't just look at filenames. You need to understand what changed and why to write a good PR.

3. **Merge in master** so you're testing against the latest code:

   ```bash
   git merge --no-edit origin/master
   ```

   Fix any merge conflicts before proceeding. Use `--no-edit` so repo merge
   settings do not drop you into an interactive editor mid-workflow.

4. **Regenerate impacted goldens before validation.** If the diff changes prompt rendering, bridge responses, MCP tool output, replay behavior, or exported game data, search existing goldens for the affected behavior and regenerate every stale prompt/export now. Do not assume only newly added tests need updates, and do not wait for CI to remind you.

5. **Run `make check`** (lint, typecheck, tests). Fix any failures before proceeding. Do not create a PR with failing checks.

   After validation, run `git status` again before pushing. Local test/build commands can dirty tracked files (for example `website/package-lock.json` metadata churn from npm). Commit intentional artifacts or clean incidental churn before you open the PR.

   Pitfall: if `make check` fails in website-related targets with `npm ERR! EEXIST` symlink errors, or `verify-schema-types` claims `website/src/types/game-export.d.ts` is stale on an otherwise clean tree, check whether parallel `npm install` runs are racing inside the website targets before assuming the generated types actually need regeneration.
   Pitfall: `make check` runs through `scripts/checks/quiet_check.py`, so it can stay silent for minutes while long subchecks run. If it looks hung, inspect the process tree (for example with `pstree -ap <quiet_check_pid>`) to see which subcheck is active before assuming it is stuck.

6. **Write the PR title and body.** The PR description must explain **why** these changes exist, not just what they do. A reviewer can read the diff to see *what* changed — the PR body should tell them *why* it changed, what problem it solves, and any context they'd need to evaluate the approach.

   Bad (just restates the diff):
   > - Add `timeout` parameter to `fetch_game_data()`
   > - Update `config.json` to include `timeout_secs` field
   > - Add test for timeout behavior

   Good (explains the motivation):
   > Grok 4 base has a 32% timeout rate at the current 45s limit because it's
   > a slow model. Increase the LLM request timeout to 120s so slower models
   > can finish reasoning without getting cut off.

   The summary bullets should be a mix of what and why — lead with the motivation, then mention key implementation details only when they're non-obvious.

7. **Push and create the PR:**

   ```bash
   git push -u origin HEAD
   gh pr create --title "<concise title>" --body "$(cat <<'EOF'
   ## Summary
   <2-5 bullets mixing why and what>

   ## Test plan
   <bulleted checklist — what you verified>

   🤖 Generated with [Claude Code](https://claude.com/claude-code)
   EOF
   )"
   ```

8. **Report the PR URL** to the user.

9. **Watch CI and address feedback.** Run the watcher — it polls every 30s, returns as soon as any check fails or all pass (up to 30 min):

   ```bash
   uv run python scripts/watch_pr.py
   ```

   - **Exit 0** (all green, no comments): Done.
   - **Exit 1** (CI failed): The output lists failed checks with links. Investigate with `gh run view <run-id> --log-failed` (extract the run ID from the check URL). Fix the root cause, then do the full push-edit-watch cycle (see AGENTS.md § Pull Requests).
   - **Exit 2** (review feedback): The output lists top-level reviews, general comments, and inline diff comments. For inline comments, read the full context with `gh api repos/{owner}/{repo}/pulls/{number}/comments`. Address each one, then do the full push-edit-watch cycle.
   - **Exit 3** (both): Address both, then push-edit-watch.
   - **Exit 4** (timeout): Re-run this step.

   **Cap at 3 fix iterations.** If after 3 rounds CI still fails or new feedback keeps arriving, report the situation to the user and stop.

## Guidelines

- **Title**: Short, imperative, under 70 characters. Describes the outcome, not the mechanism (e.g., "Fix timeout for slow models" not "Add timeout_secs config parameter").
- **Summary**: Start with the *problem* or *motivation*, then describe the solution. A reader should understand why this PR exists from the first bullet alone.
- **Test plan**: List what you actually verified — `make check`, manual testing, screenshots, specific scenarios. Don't list things you didn't do.
- **One logical change per PR** — don't bundle unrelated work.
- If the branch has many commits, the PR description should synthesize the overall change, not enumerate every commit.
