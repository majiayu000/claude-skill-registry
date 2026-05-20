---
name: git-find-fork
description: "Finds the true merge-base/fork-point of a git branch, detecting history rewrites from rebases and squashes. Handles unknown parent branches. Triggers on keywords: find fork, merge-base, branch fork point, where did branch start, git fork, branch origin"
project-agnostic: true
allowed-tools:
  - Bash
  - Read
---

# Git Find Fork

Determines the true fork point of a branch, accounting for rebases, squashes, and unknown parent branches.

## Workflow

### Step 1: Identify Current State

```bash
BRANCH=$(git rev-parse --abbrev-ref HEAD)
HEAD_SHA=$(git rev-parse --short HEAD)
```

### Step 2: Find Candidate Parent Branches

When parent is unknown, find closest by commit count:

```bash
git branch -a --format='%(refname:short)' | while read b; do
  [[ "$b" == "$BRANCH" ]] && continue
  base=$(git merge-base "$b" HEAD 2>/dev/null) || continue
  count=$(git rev-list --count "$base..HEAD")
  echo "$count $base $b"
done | sort -n | head -5
```

Lowest count = closest parent.

### Step 3: Get Merge-Base

```bash
PARENT="main"  # or detected from Step 2
MERGE_BASE=$(git merge-base "$PARENT" HEAD)
```

### Step 4: Detect History Rewriting

```bash
REFLOG_ORIGIN=$(git reflog show "$BRANCH" --format='%H %gs' | grep 'branch: Created' | awk '{print $1}')

if [[ "$REFLOG_ORIGIN" != "$MERGE_BASE" ]]; then
  echo "HISTORY REWRITTEN"
  # Check if reflog commit still ancestor
  git merge-base --is-ancestor "$REFLOG_ORIGIN" HEAD 2>/dev/null && echo "Partial rebase" || echo "Full rebase/squash"
fi
```

### Step 5: Detect Squash

```bash
COMMIT_COUNT=$(git rev-list --count "$MERGE_BASE..HEAD")
[[ "$COMMIT_COUNT" -eq 1 ]] && echo "Branch appears SQUASHED"
```

### Step 6: Find Orphaned References (Optional)

```bash
# Tags pointing to orphaned commits
for tag in $(git tag); do
  tag_sha=$(git rev-parse "$tag" 2>/dev/null)
  git merge-base --is-ancestor "$tag_sha" HEAD 2>/dev/null || echo "Orphaned: $tag -> $tag_sha"
done
```

## Output Format

| Field | Value |
|-------|-------|
| Branch | `{branch_name}` |
| HEAD | `{sha}` |
| Parent Branch | `{parent}` |
| Merge-Base | `{sha}` - "{commit message}" |
| Commits Since Fork | `{count}` |
| History Rewritten | Yes/No |
| Squashed | Yes/No |

## Key Principle

`git merge-base` gives the fork point for CURRENT history state. Original fork point after rebase/squash must be recovered from reflog, tags, or dangling objects (none guaranteed to exist).
