---
name: push-pr
description: >
  Push commits and create or update pull requests with smart branch management.
  Use when user says "push this", "push my changes", "create a PR", "open a pull request",
  "make a PR", "submit for review", or mentions pushing code or creating PRs.
  Also triggers on "send this up", "open PR", "pr please".
model: claude-sonnet-4-5
context: fork
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
  - Skill
  - AskUserQuestion
---

# Push & PR

Push commits and create/update pull requests with automatic branch management.

## Arguments

Parse flexibly:
- **status**: `1`=opened, `2`=draft, `3`=ready (default: new=opened, update=draft)
- **base-branch**: Target branch (default: `main`)

## Workflow

### 1. Pre-Flight

```bash
git status --porcelain
git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null
git fetch origin
```

If uncommitted changes detected, use `Skill: commit` to commit first.

### 2. Branch Management (Critical)

**Detect situation:**
```bash
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
UNPUSHED=$(git rev-list origin/$CURRENT_BRANCH..HEAD --count 2>/dev/null || echo "0")
```

**If on main/master with unpushed commits → CUT FEATURE BRANCH:**

1. Analyze commits to generate descriptive branch name (e.g., `feat/add-user-auth`)
2. Create feature branch from HEAD
3. Reset main to origin
4. Switch to feature branch

```bash
git log origin/main..HEAD --oneline
git checkout -b feat/descriptive-name
git checkout main && git reset --hard origin/main
git checkout feat/descriptive-name
```

**If already on feature branch:** Skip, proceed to PR.

### 3. PR Status

```bash
BRANCH=$(git rev-parse --abbrev-ref HEAD)
gh pr list --head "$BRANCH" --json number,state
```

Use provided status argument, or default: new PR=opened, update=draft.

### 4. Context Gathering

```bash
BASE=${BASE_BRANCH:-main}
git log $BASE..HEAD --oneline
git diff $BASE...HEAD --stat
git diff $BASE...HEAD
```

### 5. Push

```bash
BRANCH=$(git rev-parse --abbrev-ref HEAD)
if git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null; then
    git push
else
    git push -u origin "$BRANCH"
fi
```

### 6. PR Creation/Update

**New PR:** Generate concise title and description from commits and diff.

```bash
gh pr create --title "title" --body "description" --base main
# If status=ready: gh pr ready
```

**Existing PR:** Add comment with new commits, update status if needed.

```bash
PR_NUM=$(gh pr list --head "$BRANCH" --json number -q '.[0].number')
gh pr comment $PR_NUM --body "New commits..."
```

## Constraints

- NO Co-authored-by or AI signatures
- NO "Generated with Claude Code"
- NO emojis in title/description
- Use existing git user config only

## PR Format

```markdown
## Summary
[2-3 bullets: what and why]

## Changes
- Key change 1
- Key change 2

## Commits
- `abc1234` - message 1

## Files Changed
[Significant files with notes]
```

## Edge Cases

- No remote → suggest `git remote add origin <url>`
- No gh CLI → report requirement
- Branch behind → pull/rebase first
- No commits → report nothing to push

## Output

Report: branch pushed, PR URL, status (opened/draft/ready).
