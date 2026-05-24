---
name: pr
description: Create a pull request from current work. Handles branch creation, commits, push, and PR creation. Detects branch protection and guides through the PR workflow.
---

Base directory for this skill: /home/chapel/Projects/kynetic-spec/.claude/skills/pr

# PR Skill

Create and merge pull requests. This skill handles PR creation; for the review-to-merge cycle, use `@pr-review-merge` workflow.

## Quick Start

```bash
# Create PR from current work
/pr

# After PR created, start review workflow
kspec workflow start @pr-review-merge
kspec workflow next  # Work through each gate
```

## When to Use

- After completing work that needs to be merged via PR
- When direct push to main is blocked by branch protection
- To ship changes in a reviewable format

## Workflow

### Step 1: Detect Context

```bash
# Get current branch
git branch --show-current

# Check for uncommitted changes
git status --porcelain

# Check remote and parse owner/repo
git remote get-url origin
```

### Step 2: Check Branch Protection (Optional)

If on `main`, optionally check if PRs are required. Note: The rulesets API can fail silently or require special permissions, so don't rely on it - just try to push and handle rejection gracefully.

```bash
gh api repos/{owner}/{repo}/rulesets --jq '.[] | select(.enforcement == "active") | .rules[] | select(.type == "pull_request")' 2>/dev/null
```

### Step 3: Determine Branch Strategy

**Branch name auto-generation - just do it, don't ask:**

Generate a branch name automatically and proceed without confirmation:
1. If there's a completed/in-progress kspec task: use `fix/<task-slug>` or `feat/<task-slug>`
2. If recent commits have conventional format: derive from commit message (e.g., `fix: foo bar` → `fix/foo-bar`)
3. If unpushed commits exist: summarize their intent

**Do NOT ask for confirmation.** The user ran `/pr` because they want a PR created. Just generate the best name and proceed. Only ask if you truly have no context to generate a name (rare).

**If on `main` with uncommitted changes:**
1. Auto-generate branch name (see above)
2. Create branch: `git checkout -b <branch-name>`
3. Stage and commit changes
4. Push with `-u origin <branch-name>`

**If on `main` with committed but unpushed changes:**
1. Auto-generate branch name from commit messages
2. Create branch from current HEAD: `git checkout -b <branch-name>`
3. Reset main to origin/main:
   ```bash
   git checkout main
   git reset --hard origin/main
   git checkout <branch-name>
   ```
4. Push branch

**If already on feature branch:**
1. Commit any uncommitted changes
2. Push to origin

### Step 4: Create PR

```bash
gh pr create --title "<title>" --body "$(cat <<'EOF'
## Summary
<bullet points>

## Test plan
<checklist>

Task: @<task-ref>
Spec: @<spec-ref>

Generated with [Claude Code](https://claude.ai/code)
EOF
)"
```

**Title generation:**
- If linked to kspec task: Use task title
- If conventional commit in last commit: Use that
- Otherwise: Ask user

**Body generation:**
- Summarize changes from `git diff main...HEAD`
- Include task/spec references if available
- Add test plan checklist

### Step 5: Report

Display:
- PR URL
- Branch name
- Summary of what was included

## Review & Merge Workflow

After creating a PR, use the `@pr-review-merge` workflow for the review-to-merge cycle:

```bash
kspec workflow start @pr-review-merge
```

This enforces quality gates:
1. All CI checks complete and passing
2. All review comments addressed (automated AND human)
3. All @claude requests completed
4. All review threads resolved
5. **Final CI re-verification** before merge decision
6. Explicit merge decision

**CRITICAL: After ANY push, re-verify CI from the beginning.** Prior CI checks are invalidated by new commits. Never merge without fresh CI verification on current HEAD.

**Do not merge while CI is running or blocking.** Wait for all checks to complete. Only skip gates if user explicitly says to merge anyway.

## Merge Strategy

Use merge commits (not squash) to preserve kspec trailers:
- `Task: @task-slug`
- `Spec: @spec-ref`

These enable `kspec log @ref` to find related commits. Squashing flattens commit messages and loses traceability.

## Arguments

- `<branch-name>` (optional): Name for the feature branch
- `--title "<title>"` (optional): PR title
- `--draft` (optional): Create as draft PR

## Integration with kspec

**Before creating PR:**
```bash
# Check for in-progress tasks
npm run dev -- task list --status in_progress
```

If in-progress task found:
- Suggest branch name based on task slug
- Include task reference in PR body
- Remind to complete task after merge

**Suggested commit format:**
```
<type>: <description>

Task: @<task-slug>
Spec: @<spec-ref>

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

## Branch Naming

Auto-generate names based on context (in priority order):
1. **From kspec task**: `fix/<task-slug>` or `feat/<task-slug>` based on task type
2. **From commit message**: Parse conventional commit prefix and description
3. **From diff summary**: Derive from changed files/functionality

Do NOT present multiple-choice options. Generate the best name and ask for simple y/n confirmation.

## Error Handling

**No remote configured:**
```
Error: No git remote configured. Add one with:
  git remote add origin <url>
```

**PR already exists:**
```bash
gh pr list --head <branch> --json number,url
```
If exists, show URL instead of creating new.

**Push rejected:**
Check if branch exists on remote with different history. Offer:
- Force push (if user confirms)
- Create new branch with suffix

## Example Usage

```
User: /pr
Agent: [Detects 2 unpushed commits on main, auto-generates branch name from commits]
Agent: [Creates branch fix/ready-task-secondary-sort, resets main, pushes]
Agent: [Creates PR]

PR created: https://github.com/owner/repo/pull/5
Branch: fix/ready-task-secondary-sort
```

The user asked for a PR - just create it. No confirmations needed.

## Worktree Support (Future)

For complex, long-running work, consider `/isolate` pattern:
- Create worktree: `git worktree add worktrees/<task-id> -b <task-id>`
- Work in isolation
- Land with `/land` when ready

This skill focuses on the simple case of shipping current work.
