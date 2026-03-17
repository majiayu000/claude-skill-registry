---
name: pr-create
description: Creates a pull request from current changes, monitors GitHub CI, and debugs any failures until CI passes. Use this when the user says "create pr", "make a pr", "open pull request", "submit pr", "pr for these changes", or wants to get their current work into a reviewable PR. Assumes the project uses git, is hosted on GitHub, and has GitHub Actions CI with automated checks (lint, build, tests, etc.). Does NOT merge - stops when CI passes and provides the PR link.
compatibility: Designed for Claude Code; requires TaskCreate, TaskUpdate, and TaskList tools
metadata:
  author: Garrick Aden-Buie (@gadenbuie)
  version: "1.1"
license: MIT
---

# PR Creator Skill

Get changes into a PR, monitor CI, fix any failures, and notify the user when the PR is ready for review.

The user may already have commits ready on a feature branch, or may have uncommitted changes, or both. Adapt the workflow to the current state.

## Task List Integration

**CRITICAL:** Use Claude Code's task list system for progress tracking and session recovery. Use TaskCreate, TaskUpdate, and TaskList tools throughout execution.

### Task Hierarchy
```
[Main Task] "Create PR: [branch-name]"
  └── [CI Task] "CI Run #1" (status: failed, reason: lint)
      └── [Fix Task] "Fix: lint"
  └── [CI Task] "CI Run #2" (status: failed, reason: test failures)
      └── [Fix Task] "Fix: test failures"
  └── [CI Task] "CI Run #3" (status: passed)
```

**At the start, always call TaskList to check for existing PR tasks.** If a "Create PR" task exists with status in_progress, resume using the Session Recovery section below.

## Process

### Step 1: Assess Current State

**Check for a `--reviewer` argument** in the user's message. If present, store the value for use in Step 5. It may be a GitHub handle (`@username`) or a name (`Jane Doe`).

**Create the main PR task:**
```
TaskCreate:
- subject: "Create PR: [branch-name or 'pending']"
- description: "Create pull request from current changes."
- activeForm: "Checking git status"

TaskUpdate:
- taskId: [pr task ID]
- status: "in_progress"
```

Determine the base branch and current state:

```bash
git status
git diff --stat
# Detect the default branch (main, master, develop, etc.)
gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name'
git log --oneline <base-branch>..HEAD
gh pr view 2>/dev/null
```

**Determine the starting point:**

| State | Next Step |
|-------|-----------|
| On base branch with uncommitted changes | Step 2 (create branch) |
| On feature branch with uncommitted changes | Step 3 (commit) |
| On feature branch with commits, nothing uncommitted | Step 4 (sync) |
| PR already exists for this branch | Inform user, ask whether to update or monitor CI |
| No changes anywhere | Inform user "No changes detected. Nothing to do." and stop |

**Update task with branch info:**
```
TaskUpdate:
- taskId: [pr task ID]
- subject: "Create PR: [actual-branch-name]"
- metadata: {"branch": "[branch-name]", "baseBranch": "[base-branch]"}
```

### Step 2: Create Branch (if needed)

If currently on the base branch:
```bash
git checkout -b <descriptive-branch-name>
```

Use the project's branch naming conventions if documented in CLAUDE.md or AGENTS.md. Otherwise use:
- `feat/short-description` for features
- `fix/short-description` for bug fixes
- `refactor/short-description` for refactoring
- `docs/short-description` for documentation

### Step 3: Stage and Commit Changes (if needed)

**Skip this step entirely if there are no uncommitted changes.**

Stage specific files rather than using `git add -A`:

```bash
git status
git add <file1> <file2> ...
git diff --cached --stat
git commit -m "$(cat <<'EOF'
<type>: <short summary>

<optional longer description>
EOF
)"
```

Follow the project's commit conventions if documented in CLAUDE.md or AGENTS.md. Otherwise use conventional commits: `feat:`, `fix:`, `refactor:`, `docs:`, `test:`, `chore:`.

**If the commit fails due to a pre-commit hook:**
1. Read the error output to understand what the hook requires
2. Fix the flagged issues
3. Stage the fixed files
4. Create a **new** commit (do NOT amend the previous commit)

### Step 4: Sync with Base Branch (if needed)

```bash
git fetch origin
git log --oneline HEAD..origin/<base-branch> | head -20
```

**If up to date** (no output), proceed to Step 5.

**If behind**, inform the user how many commits behind and offer options using `AskUserQuestion`:

1. **Rebase** (recommended when no PR exists yet)
2. **Merge** (safer with many commits or shared branches)
3. **Skip** (proceed without syncing)

**Do NOT rebase or merge without user confirmation.**

If conflicts arise, inform the user and help resolve them.

### Step 5: Draft PR Title and Body

**Get user approval on the PR content now**, before running pre-flight checks. This keeps the user engaged while they're focused on the task.

**5a. Gather context:**

```bash
git log --oneline <base-branch>..HEAD
git diff <base-branch>...HEAD --stat
```

**5b. Draft the PR title and body:**

Follow the project's PR conventions if documented in CLAUDE.md or AGENTS.md. Otherwise:

- **Title:** Under 70 characters, describes the change
- **Body:** Start with issue references on the first line (e.g. `Closes #45`), then a structured description:

```markdown
[issue references: Fixes #...]

## Summary
<summary>

## Verification
<how to verify>
```

Summary: Give an overview of the changes in the PR. The target audience is an experienced developer who works in this code base and needs to be informed about design or architectural changes. Highlight key decisions, structures and patterns.

Verification: include an example that demonstrates the changes in the PR as seen or used by the intended audience. For code packages, include a small, reproducible exmaple. For apps and interfaces, describe the steps required to see the new behavior.

**5c. Preview and get user approval:**

**CRITICAL:** Use `AskUserQuestion` to show the user the proposed PR title and body. Also include a reviewer question in this same interaction:

- If a `--reviewer` was provided, resolve and confirm the GitHub handle (see below), then show it as part of the preview.
- If no reviewer was given, ask in the same `AskUserQuestion` call whether they want to request a review from anyone (free-text, optional).

**Resolving a reviewer by name (not handle):**
If the reviewer value doesn't look like a GitHub handle (no `@`, not clearly a username), look up the correct handle:
```bash
# Check recent contributors in the repo first
gh api repos/{owner}/{repo}/contributors --jq '.[].login' | head -20

# Search GitHub users if not found in contributors
gh api search/users?q=<name>+in:name --jq '.items[] | "\(.login) \(.name // "")"' | head -10
```
Confirm the resolved handle with the user before storing it.

Store the confirmed reviewer handle in task metadata:
```
TaskUpdate:
- taskId: [pr task ID]
- metadata: {"reviewer": "<github-handle>"}
```

Include approval options directly in the `AskUserQuestion` call for the PR preview. The options should be:

1. **"Looks good, proceed"** *(default)* — approve and immediately continue to Step 6
2. **"Looks good, tell me what you'll do next"** — approve but show the plan outline before continuing

Do NOT create the PR until the user has selected one of these options.

**5d. Show plan outline (only if user selected option 2):**

Present the following before continuing:

> Here's what I'll do next:
>
> 1. **Run local checks** (if available for this project)
> 2. **Push** the branch to origin
> 3. **Create the PR** as a draft with the approved title and body
> 4. **Monitor CI** and fix any failures
> 5. **Publish the PR** (remove draft status) once CI passes
> 6. **Request a review** from `@<reviewer>` (if applicable)
>
> I'll auto-fix small issues (formatting, lint, type errors, test failures). If anything bigger comes up, I'll check with you first.

After showing the outline, ask one more `AskUserQuestion` to confirm before proceeding to Step 6.

### Step 6: Run Local Pre-flight Checks

**This step catches most CI failures before pushing.**

Determine the project's local check commands by consulting (in priority order):
1. CLAUDE.md or AGENTS.md in the project root (may specify lint, test, build commands)
2. Project config files: `package.json` (scripts), `Makefile`, `pyproject.toml`, `DESCRIPTION`, `Justfile`, `Taskfile.yml`, etc.
3. CI workflow files in `.github/workflows/` to understand what CI will run

Run the checks that are available locally. Common patterns:
- **Lint/format**: `npm run lint`, `ruff check`, `air format`, `biome check`, etc.
- **Build**: `npm run build`, `pip install -e .`, `devtools::check()`, etc.
- **Type check**: `npm run check-types`, `mypy`, `pyright`, etc.
- **Tests**: `npm test`, `pytest`, `devtools::test()`, `cargo test`, etc.

If no local check commands are discoverable, skip this step and rely on CI.

**Fixing failures:**

- **Obvious, mechanical fixes** — fix autonomously:
  - Formatting issues (run auto-formatter if available)
  - Lint errors with clear fixes
  - Simple build, test, or type errors with obvious corrections
  - Stage the fixed files and commit the fix (specific files, not `git add -A`)
  - Re-run the failing check to confirm it passes
  - ALWAYS call out changes made in this step in the final summary

- **Non-obvious failures** — use `AskUserQuestion` to present the issue and offer resolution options

### Step 7: Push Branch

```bash
git push -u origin <branch-name>
```

### Step 8: Create Pull Request

Create the PR as a **draft** so it is not prematurely sent for review while CI is still running.

**GitHub's markdown parser renders every newline literally — do not wrap long lines in the PR body. Write each paragraph as a single unbroken line.**

```bash
gh pr create --draft --title "<approved-title>" --body "$(cat <<'EOF'
<approved-body>
EOF
)"
```

**Capture the PR URL** and store in task metadata:
```
TaskUpdate:
- taskId: [pr task ID]
- metadata: {"prUrl": "<url>", "prNumber": <N>, "prTitle": "<title>", "commits": <count>}
```

### Step 9: Monitor CI

**Create a CI run task:**
```
TaskCreate:
- subject: "CI Run #[N]: monitoring"
- description: "Monitoring CI run for PR #[number]"
- activeForm: "Monitoring CI Run #[N]"

TaskUpdate:
- taskId: [ci task ID]
- addBlockedBy: [pr task ID]
- status: "in_progress"
```

Wait for CI to start, then monitor:

```bash
# List workflow runs for this PR
gh run list --branch <branch-name> --limit 5

# Watch a specific run silently until completion
# --exit-status returns exit code 0 on success, non-zero on failure
gh run watch <run-id> --exit-status > /dev/null 2>&1
echo "Exit: $?"

# Or check status without blocking
gh run view <run-id>
```

**IMPORTANT:** Do NOT run `gh run watch` without redirecting output. It generates thousands of lines of repeated status updates. Always redirect to `/dev/null` and rely on the exit code.

**Store run ID in task:**
```
TaskUpdate:
- taskId: [ci task ID]
- metadata: {"runId": "[run-id]", "status": "running"}
```

### Step 10: Handle CI Results

#### If CI Passes:

```
TaskUpdate:
- taskId: [ci task ID]
- subject: "CI Run #[N]: passed"
- status: "completed"
- metadata: {"status": "passed"}
```

**Publish the PR** (remove draft status):
```bash
gh pr ready <pr-number>
```

**Request a review** (if a reviewer was stored in task metadata):
```bash
gh pr edit <pr-number> --add-reviewer <github-handle>
```

- **STOP HERE** - do not merge
- Report to user with PR URL, branch, and CI status

#### If CI Fails:

```
TaskUpdate:
- taskId: [ci task ID]
- subject: "CI Run #[N]: failed"
- status: "completed"
- metadata: {"status": "failed", "failureReason": "[brief reason]"}
```

1. **Get failure details:**

   `--log-failed` can produce thousands of lines. Use a targeted approach:

   ```bash
   # Summary of which jobs/steps failed
   gh run view <run-id>

   # Failed logs, limited to the last 40 lines (where the error usually is)
   gh run view <run-id> --log-failed 2>&1 | tail -40

   # Search for specific errors if needed
   gh run view <run-id> --log-failed 2>&1 | grep -A 5 -B 5 "error\|Error\|FAIL\|failed"
   ```

   Work from the bottom of the output upward — the actual error is almost always near the end.

2. **Reproduce locally** using the project's local check commands (discovered in Step 6).

3. **Create a fix task:**
   ```
   TaskCreate:
   - subject: "Fix: [failure reason]"
   - description: "Fixing CI failure from Run #[N]: [detailed error]"
   - activeForm: "Fixing [failure reason]"

   TaskUpdate:
   - taskId: [fix task ID]
   - addBlockedBy: [ci task ID]
   - status: "in_progress"
   ```

4. **Fix the issue**, verify locally, then commit and push:
   ```bash
   git add <specific-files>
   git commit -m "$(cat <<'EOF'
   fix: <what was fixed>
   EOF
   )"
   git push
   ```

5. **Mark fix task completed:**
   ```
   TaskUpdate:
   - taskId: [fix task ID]
   - status: "completed"
   ```

6. **Return to Step 9** — monitor the new CI run (increment run number)

**Repeat until CI passes.**

### Step 11: Final Report

**Mark main PR task as completed.**

Call `TaskList` to gather all CI run and fix tasks, then generate the summary:

```markdown
## PR Ready for Review

**PR:** [#<number> <title>](<url>)
**Branch:** `<branch-name>` -> `<base-branch>`
**Commits:** <count>
**CI Status:** All checks passed
**Reviewer:** @<handle> (if requested)

### CI Runs
- Run #1: Failed (lint) -> Fixed in [hash]
- Run #2: Passed

**Note:** This PR has NOT been merged. Please review and merge manually.
```

### Session Recovery

If resuming from an interrupted session:

```
TaskList shows:
├── PR task in_progress, no CI tasks
│   └── PR was created, start monitoring CI (Step 9)
├── PR task in_progress, CI task in_progress
│   └── Resume monitoring CI run from task metadata runId
├── PR task in_progress, CI task failed, no fix task
│   └── Analyze failure and create fix task (Step 10)
├── PR task in_progress, fix task in_progress
│   └── Continue fixing, then push and monitor new CI run
├── PR task completed
│   └── PR is done, show final report
└── No tasks exist
    └── Fresh start (Step 1)
```

When resuming, use `gh run view <runId>` from CI task metadata to check if the run is still active, completed, or superseded. Inform the user of the current state before resuming.

## Important Rules

1. **NEVER merge the PR** - only create it and ensure CI passes
2. **NEVER force push** unless explicitly asked
3. **NEVER push to base branch directly**
4. **Continue fixing until CI passes** - don't give up after one failure
5. **Preserve commit history** - don't squash unless asked
6. **ALWAYS preview PR title and body** with the user before creating
7. **ALWAYS stage specific files** - never use `git add -A` or `git add .`
8. **NEVER amend commits** unless explicitly asked - always create new commits for fixes
9. **ALWAYS open PRs as drafts** - use `gh pr create --draft`; publish with `gh pr ready` only after CI passes
10. **NEVER request a review before CI passes**
11. **Do NOT wrap markdown lines** in PR bodies - GitHub renders every newline literally

## Error Handling

**Authentication issues:**
If `gh` commands fail with auth errors, inform the user to run `gh auth login`.

**Branch conflicts:**
Offer rebase or merge options. Resolve conflicts if any, then continue.

**PR already exists:**
Inform user a PR already exists for this branch. Ask if they want to update it or monitor its CI.

**Pre-commit hook failures:**
Read the hook error output, fix the flagged issues, stage the fixes, and create a new commit. Do NOT amend.
