---
description: Detect potential file conflicts between active PRs and current work
tags: [git, conflict, parallel-development, operations]
techStack: [git, gh-cli]
appliesTo: ["parallel sessions", "before merge", "conflict detection"]
alwaysApply: false
---

# Conflict Check

> **Category**: Operations
> **Last Updated**: January 2026

---

## Purpose

Proactively detect potential merge conflicts by comparing files changed in your current branch with:
1. Files changed in other active PRs
2. Files changed in master since your branch diverged

**Use Cases**:
- Before starting a new project (check for overlapping work)
- Before marking a PR "Ready for Review"
- After another PR merges to master
- When running parallel Claude Code sessions

---

## Applies When

- Running multiple Claude Code sessions in parallel
- Before merging a PR
- User says "check for conflicts", "conflict check", "file overlap"
- **Trigger phrases**: `/conflict-check`, "check conflicts", "file overlap"

---

## Workflow

### Step 1: Gather Current Branch Info

```powershell
# Get current branch name
git branch --show-current

# Get files changed in current branch vs master
git fetch origin master
git diff --name-only origin/master...HEAD
```

Store as: `current_branch_files`

### Step 2: Get Active PRs

```powershell
# List all open PRs (excluding current branch)
gh pr list --state open --json number,title,headRefName,files
```

**Parse output:**
```
FOR EACH PR:
  - PR number
  - Title
  - Branch name
  - Files changed
```

### Step 3: Detect Overlaps

```
FOR EACH active PR:
  overlap = intersection(current_branch_files, pr_files)

  IF overlap is not empty:
    ADD to conflicts list:
      - PR #, title, branch
      - Overlapping files
```

### Step 4: Check Master Divergence

```powershell
# Files changed in master since branch diverged
git log origin/master --name-only --pretty=format: --since="$(git log -1 --format=%ci HEAD~10)" | sort -u
```

Compare with `current_branch_files` for additional overlap risk.

### Step 5: Present Results

**If no conflicts:**
```
✅ No file conflicts detected

Your branch: {branch-name}
Files changed: {N} files
Active PRs checked: {M} PRs

Safe to proceed with merge.
```

**If conflicts detected:**
```
⚠️ Potential Conflicts Detected

Your branch: {branch-name}
Files changed: {N} files

Overlapping PRs:
──────────────────
PR #{number}: {title}
  Branch: {branch}
  Overlapping files:
    - src/server/api/SomeFile.cs
    - src/client/pcf/Component/index.ts

PR #{number2}: {title2}
  Branch: {branch2}
  Overlapping files:
    - CLAUDE.md

Recommendations:
1. Coordinate with PR owners on shared files
2. Consider merging one PR first, then rebase
3. If same session: designate file ownership

Run rebase after other PR merges:
  git fetch origin master
  git rebase origin/master
  git push --force-with-lease
```

---

## Quick Commands

```powershell
# Full conflict check (run this skill)
/conflict-check

# Manual: See files in other PRs
gh pr list --json number,title,files --jq '.[] | "\(.number): \(.title) - \(.files | length) files"'

# Manual: See specific PR files
gh pr view 101 --json files --jq '.files[].path'

# Manual: Compare branches
git diff --name-only HEAD origin/feature/other-branch

# Manual: See master changes since you branched
git log origin/master --name-only --oneline HEAD..origin/master
```

---

## Integration Points

### With project-pipeline

At project planning time, check for overlapping work:

```
DURING Step 1 (Validate SPEC.md):
  → Identify likely files to be modified (from spec scope)
  → Run /conflict-check to detect overlap with active PRs
  → WARN if significant overlap detected
  → ASK: Proceed anyway, coordinate, or wait?
```

### With task-execute

At end of each task:

```
AFTER task completion, BEFORE commit:
  → git fetch origin master
  → Check if master has changes to files you modified
  → IF overlap: Recommend rebase before push
```

### With push-to-github

Before creating/updating PR:

```
DURING Step 1 (Pre-flight checks):
  → Run conflict check
  → IF conflicts: WARN and recommend resolution strategy
```

---

## Decision Tree

```
Running /conflict-check
│
├─ Fetch current branch files
│
├─ Fetch active PR files
│
├─ Calculate overlaps
│
└─ Overlaps found?
    │
    ├─ NO → "✅ Safe to proceed"
    │
    └─ YES → Show overlapping files
        │
        ├─ Same session owns both → "Merge PR #{X} first, then rebase"
        │
        ├─ Different owners → "Coordinate with PR owner"
        │
        └─ Can split work → "Consider file ownership split"
```

---

## Example Output

**User**: `/conflict-check`

**Output (no conflicts)**:
```
✅ No file conflicts detected

Your branch: feature/dark-mode
Files changed: 12 files
Active PRs checked: 3 PRs

Safe to proceed with merge.
```

**Output (conflicts found)**:
```
⚠️ Potential Conflicts Detected

Your branch: feature/dark-mode
Files changed: 12 files

Overlapping PRs:
──────────────────
PR #98: chore: project planning updates
  Branch: work/project-planning-and-documentation
  Overlapping files:
    - .claude/skills/INDEX.md
    - CLAUDE.md

Recommendations:
1. PR #98 is close to merge - wait for it to complete
2. After merge: git fetch origin && git rebase origin/master
3. Then push your updated branch
```

---

## Related Skills

- `worktree-setup` - Parallel session management
- `push-to-github` - Pre-push conflict detection
- `project-pipeline` - Project planning overlap detection
- `task-execute` - End-of-task sync check

---

*This skill enables proactive conflict detection for parallel Claude Code development workflows.*
