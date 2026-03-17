---
name: auto-merge
description: Merge an existing PR after rebasing, running review-pass, ensuring CI passes, and addressing review comments.
allowed-tools: Bash, Read, Task, Glob, Grep, Edit, Write, TodoWrite
---

# Auto-Merge Skill

## Purpose

Merge a PR that's ready for integration. Handles rebase, code review, CI verification, and comment resolution autonomously.

## Usage

```
/auto-merge <PR#>
```

**Example:** `/auto-merge 91`

## Prerequisites

- PR must exist and be open
- User must have merge permissions
- CI must be configured (or skippable)

---

## Step Execution Pattern

Each step has explicit entry/exit criteria. Verify success before proceeding to the next step.

```
For each Step N:
  1. Verify entry criteria are met
  2. Execute the action
  3. Verify exit criteria (check output, run validation)
  4. Only proceed to Step N+1 after verification passes

If verification fails: STOP and report. Do not skip to later steps.
```

This ensures the workflow progresses through each stage completely rather than jumping ahead.

---

## Workflow

### Step 1: Fetch PR Information

**Entry:** PR number provided
**Exit:** Have PR metadata (number, title, branch, state, mergeable status), checkpoint updated

```bash
gh pr view <PR#> --json number,title,headRefName,baseRefName,state,mergeable,reviewDecision,statusCheckRollup
```

Verify before proceeding:
- PR is open (`state == "OPEN"`)
- PR is against main/master
- Store branch name for later steps

**Extract linked issue** (for checkpoint tracking):

```bash
# Get issue number from PR body (looks for "Closes #123" or "Fixes #123")
gh pr view <PR#> --json body --jq '.body' | grep -oP '(?:Closes|Fixes|Resolves)\s*#\K\d+'
```

**Update checkpoint** (if issue found and workflow exists):

```bash
# 1. Find workflow (note the id from output)
pnpm checkpoint workflow find {issue_number}

# 2. Set phase to merge (use id from step 1)
pnpm checkpoint workflow set-phase "{workflow_id}" merge
```

Setting phase to `merge` at the START allows correct resume if interrupted.

---

### Step 2: Checkout and Rebase

**Entry:** Have PR branch name from Step 1
**Exit:** On PR branch, rebased onto latest main, no conflicts

```bash
# Fetch latest
git fetch origin main
git fetch origin <branch>

# Checkout PR branch
git checkout <branch>

# Rebase onto main
git rebase origin/main
```

**If conflicts:**
1. Attempt to resolve simple conflicts
2. If complex conflicts, report and abort
3. User intervention required for complex cases

Verify before proceeding: `git status` shows clean working tree on PR branch.

---

### Step 3: Check Review Comments

**Entry:** On PR branch, rebased, clean working tree
**Exit:** All existing review comments addressed or noted

Check for existing review comments BEFORE running review agents:

```bash
gh api repos/{owner}/{repo}/pulls/<PR#>/comments --jq '.[] | select(.position != null) | {user: .user.login, body: .body, path: .path, line: .line}'
```

For each comment:
1. Read the comment content and suggestion
2. If valid and actionable: apply the fix now
3. If already addressed or outdated: note as resolved
4. If needs clarification: note for later

**If fixes applied:**
```bash
git add -A
git commit -m "fix: address review comments"
```

Verify before proceeding: All actionable comments addressed.

---

### Step 4: Run Review Pass (MANDATORY)

**Entry:** On PR branch, rebased, clean working tree
**Exit:** Review agents completed, findings addressed, any fixes committed

**CRITICAL:** Do NOT skip this step. Run all review agents.

| Agent | Purpose | Status |
|-------|---------|--------|
| `code-simplifier:code-simplifier` | Simplify changed code | ☐ |
| `pr-review-toolkit:code-reviewer` | Check bugs and quality | ☐ |
| `pr-review-toolkit:silent-failure-hunter` | Find silent failures | ☐ |

For each agent:
1. Launch via Task tool
2. Apply fixes with confidence >= 60%
3. Mark as complete (☑)

If changes made:
```bash
git add -A
git commit -m "refactor: address review findings"
```

**Verify before proceeding:** All three agents must show ☑. If any skipped, do NOT proceed.

---

### Step 5: Push Updates

**Entry:** Review pass complete, any fixes committed locally
**Exit:** Branch pushed to remote with all local commits

```bash
git push --force-with-lease origin <branch>
```

**Note:** Use `--force-with-lease` for safety after rebase.

Verify before proceeding: Push succeeded (check exit code), remote branch updated.

---

### Step 6: Verify CI Status

**Entry:** Branch pushed to remote
**Exit:** All CI checks green

```bash
gh pr checks <PR#> --watch
```

**If CI fails:**
1. Analyze failure logs
2. Fix the issue
3. Commit: `fix: resolve CI failure`
4. Push and wait for CI
5. Repeat until green (max 3 attempts)

Verify before proceeding: `gh pr checks <PR#>` shows all checks passed.

---

### Step 7: Handle Review Comments (Post-CI)

**Entry:** CI checks green
**Exit:** No unresolved blocking comments, or all comments addressed

```bash
# Get unresolved comments
gh api repos/{owner}/{repo}/pulls/<PR#>/comments --jq '.[] | select(.position != null)'
```

For each unresolved comment:
1. Read the comment content
2. Evaluate if valid concern
3. If valid: make the fix, commit, push
4. If resolved or outdated: note as addressed

**If changes were made:** Return to Step 6 (Verify CI) before proceeding. Changes may have broken the build.

Verify before proceeding: No pending review comments requiring action.

---

### Step 8: Verify Merge Readiness

**Entry:** CI green, no unresolved comments
**Exit:** PR confirmed mergeable

Check all conditions:
- [ ] CI green
- [ ] No unresolved blocking comments
- [ ] Branch is up-to-date with main
- [ ] PR is mergeable

```bash
gh pr view <PR#> --json mergeable,mergeStateStatus
```

Verify before proceeding: `mergeable == "MERGEABLE"` and `mergeStateStatus == "CLEAN"`.

---

### Step 9: Merge PR

**Entry:** PR verified mergeable
**Exit:** PR merged, branch deleted, checkpoint updated

```bash
gh pr merge <PR#> --squash --delete-branch
```

**Merge strategy:** Squash (consolidates commits)

Verify merge succeeded: `gh pr view <PR#> --json state` shows `state == "MERGED"`.

**Update checkpoint** (if workflow exists):

```bash
# 1. Get merge commit SHA (run separately, note the output)
git fetch origin main
git rev-parse origin/main

# 2. Find workflow (note the id from output)
pnpm checkpoint workflow find {issue_number}

# 3. Mark merged (use literal SHA and workflow_id from steps 1-2)
pnpm checkpoint workflow set-merged "{workflow_id}" "{merge_sha}"
```

Per checkpoint-patterns.md: always use separate commands, never shell variables.

This enables `/auto-milestone --continue` to know the issue is complete.

---

### Step 10: Cleanup

**Entry:** PR merged
**Exit:** On main branch, pulled latest, ready for next operation

```bash
# Return to main
git checkout main
git pull origin main
```

Verify completion: `git branch --show-current` shows `main`, `git status` shows clean.

---

## Error Handling

### Rebase Conflicts

```
CONFLICT: Rebase failed with conflicts

Files with conflicts:
- {file1}
- {file2}

Action required: Manual conflict resolution
```

Abort and report to user.

### CI Failure (Max Retries)

```
CI FAILURE: Unable to fix after 3 attempts

Last failure:
{error summary}

Action required: Manual investigation
```

Leave PR in current state, report to user.

### Merge Blocked

```
MERGE BLOCKED

Reason: {mergeable status}

Possible causes:
- Required reviews not approved
- Status checks pending
- Branch protection rules
```

Report and exit.

## Configuration

See `config.md` for:
- Max CI retry attempts
- Confidence threshold for fixes
- Merge strategy options

## Output Format

```
AUTO-MERGE COMPLETE

## PR Merged
- PR: #<number>
- Title: <title>
- Branch: <branch> -> main

## Review Pass
- Simplifications: <count>
- Issues fixed: <count>
- Commits added: <count>

## CI Status
- Checks: <passed>/<total>
- Attempts: <count>

## Comments Addressed
- Resolved: <count>
- Skipped: <count>

## Merge
- Strategy: squash
- Branch deleted: yes

## Post-Merge
- Main updated: yes
- On branch: main
```

## Limitations

- Cannot resolve complex merge conflicts
- Cannot address comments requiring major refactoring
- Cannot bypass branch protection rules
- Max 3 CI fix attempts

## Related Skills

- `/auto-issue` - Create PR from issue
- `/auto-milestone` - Process milestone issues
- `board-manager` - Update issue status
