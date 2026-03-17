---
name: git:status
description: Show worktrees with PR status and TODO files overview
---

# Git Status

Show comprehensive status of worktrees, their PRs, and TODO files.

## Quick Status

Run these commands to get full project status:

```bash
# 1. Worktrees with PR status
echo "=== Worktrees ===" && \
git worktree list --porcelain | grep -E "^worktree|^branch" | paste - - | \
while read wt branch; do
  dir=$(echo "$wt" | sed 's/worktree //')
  br=$(echo "$branch" | sed 's|branch refs/heads/||')
  pr=$(gh pr list --head "$br" --json number,state,title --jq '.[0] | "PR #\(.number) [\(.state)]"' 2>/dev/null || echo "No PR")
  printf "%-50s %-30s %s\n" "$dir" "$br" "$pr"
done

# 2. TODO files
echo "" && echo "=== TODO Files ===" && \
ls -1 TODO_*.md 2>/dev/null | while read f; do
  title=$(head -1 "$f" | sed 's/^# //')
  printf "%-40s %s\n" "$f" "$title"
done
```

## Detailed Worktree Status

```bash
# Show worktrees with full PR details
git worktree list | while read dir commit branch; do
  branch=$(echo "$branch" | tr -d '[]')
  echo "=== $branch ==="
  echo "  Path: $dir"
  gh pr list --head "$branch" --json number,title,state,url,statusCheckRollup \
    --jq '.[] | "  PR #\(.number): \(.title)\n  State: \(.state)\n  URL: \(.url)\n  Checks: \([.statusCheckRollup[]? | .conclusion] | group_by(.) | map("\(.[0]): \(length)") | join(", "))"' 2>/dev/null || echo "  No PR"
  echo ""
done
```

## PR Status Only

```bash
# Quick PR status for open PRs by author
gh pr list --author @me --state open \
  --json number,title,headRefName,statusCheckRollup \
  --jq '.[] | "PR #\(.number) [\(.headRefName)]: \([.statusCheckRollup[]? | select(.conclusion == "FAILURE")] | length) failures"'
```

## TODO Files Overview

```bash
# List TODO files with first line (title)
for f in TODO_*.md; do
  [ -f "$f" ] && printf "%-45s %s\n" "$f" "$(head -1 "$f" | sed 's/^# //')"
done

# Find TODO files mentioning specific branch
grep -l "branch-name" TODO_*.md 2>/dev/null
```

## Combined Status Table

For a formatted table output:

```bash
echo "| Worktree | Branch | PR | CI Status |"
echo "|----------|--------|----|-----------| "
git worktree list --porcelain | grep -E "^worktree|^branch" | paste - - | \
while read wt branch; do
  dir=$(basename "$(echo "$wt" | sed 's/worktree //')")
  br=$(echo "$branch" | sed 's|branch refs/heads/||')
  pr_info=$(gh pr list --head "$br" --json number,statusCheckRollup \
    --jq '.[0] | "#\(.number) \([.statusCheckRollup[]? | select(.conclusion == "FAILURE")] | length) fail"' 2>/dev/null)
  [ -z "$pr_info" ] && pr_info="No PR"
  echo "| $dir | $br | $pr_info |"
done
```

## Related Skills

- `git:worktree` - Manage worktrees
- `hypershift:cluster` - HyperShift cluster management
