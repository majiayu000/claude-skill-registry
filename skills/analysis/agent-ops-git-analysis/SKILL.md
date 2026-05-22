---
name: agent-ops-git-analysis
description: "Analyze git repository for insights: contributor stats, commit patterns, branch health, and change analysis. Outputs actionable reports."
category: analysis
invokes: []
invoked_by: []
state_files:
  read: [constitution.md, focus.md]
  write: [focus.md]
---

# Git Analysis Skill

Generate repository insights and health reports from git history.

## Commands

All analysis uses standard `git` commands. No external dependencies required.

### Quick Stats

```bash
# Total commits
git rev-list --count HEAD

# Contributors count
git shortlog -sn --all | wc -l

# First and last commit dates
git log --reverse --format=%ci | head -1
git log -1 --format=%ci

# Files in repository
git ls-files | wc -l

# Lines of code (approximate)
git ls-files | xargs wc -l 2>/dev/null | tail -1
```

### Contributor Analysis

```bash
# Commits per author
git shortlog -sn --all

# Commits per author (last 30 days)
git shortlog -sn --since="30 days ago"

# Most active files by author
git log --author="Name" --name-only --pretty=format: | sort | uniq -c | sort -rn | head -20
```

### Commit Patterns

```bash
# Commits by day of week
git log --format=%ad --date=format:%A | sort | uniq -c | sort -rn

# Commits by hour
git log --format=%ad --date=format:%H | sort | uniq -c | sort -n

# Commits per month (last year)
git log --since="1 year ago" --format=%ad --date=format:%Y-%m | sort | uniq -c

# Average commits per day (last 30 days)
# commits / 30
```

### Branch Health

```bash
# List all branches with last commit date
git for-each-ref --sort=-committerdate refs/heads/ --format='%(committerdate:short) %(refname:short)'

# Stale branches (no commits in 90 days)
git for-each-ref --sort=committerdate refs/heads/ --format='%(committerdate:iso) %(refname:short)' | while read date branch; do
  if [[ $(date -d "$date" +%s) -lt $(date -d "90 days ago" +%s) ]]; then
    echo "STALE: $branch (last: $date)"
  fi
done

# Merged branches (candidates for deletion)
git branch --merged main | grep -v main

# Branches ahead/behind main
git for-each-ref --format='%(refname:short) %(upstream:track)' refs/heads
```

### Large Files Detection

```bash
# Find large files in history
git rev-list --objects --all | \
  git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' | \
  sed -n 's/^blob //p' | \
  sort -rnk2 | \
  head -20

# Current large files
git ls-files | xargs ls -la 2>/dev/null | sort -rnk5 | head -20
```

### Change Analysis

```bash
# Files most frequently changed (churn)
git log --name-only --pretty=format: | sort | uniq -c | sort -rn | head -20

# Recent hotspots (last 30 days)
git log --since="30 days ago" --name-only --pretty=format: | sort | uniq -c | sort -rn | head -20

# Diff stats between branches
git diff --stat main..feature-branch

# Changed files between commits
git diff --name-status <commit1> <commit2>
```

## Report Templates

### Quick Health Report

```markdown
# Repository Health Report
Generated: {date}

## Overview
- **Total Commits**: {count}
- **Contributors**: {count}
- **Age**: {first_commit_date} to {last_commit_date}
- **Files**: {file_count}

## Activity (Last 30 Days)
- Commits: {count}
- Active Contributors: {count}
- Most Changed Files:
  1. {file} ({changes} changes)
  2. ...

## Branch Status
- Active Branches: {count}
- Stale Branches (>90 days): {count}
- Merged (deletable): {count}

## Hotspots
Files with highest churn (potential refactoring candidates):
1. {file} - {change_count} changes
2. ...

## Recommendations
- {recommendations}
```

### Contributor Report

```markdown
# Contributor Activity Report
Generated: {date}
Period: {start_date} to {end_date}

## Summary
| Contributor | Commits | Lines Added | Lines Removed |
|-------------|---------|-------------|---------------|
| {name}      | {count} | +{added}    | -{removed}    |

## Activity by Day
{chart or table}

## Focus Areas
Most modified files per contributor...
```

### Diff Report

```markdown
# Change Analysis: {branch1} → {branch2}
Generated: {date}

## Summary
- Files Changed: {count}
- Lines Added: +{added}
- Lines Removed: -{removed}

## Changed Files
| File | Status | +/- |
|------|--------|-----|
| {path} | Modified | +{a}/-{r} |

## High-Impact Changes
Files with >100 lines changed...
```

## Invocation

When user asks for repository analysis:

1. **Determine scope**:
   - Full repository or specific branch?
   - Time period (all time, last N days)?
   - Focus area (contributors, health, changes)?

2. **Run appropriate commands**

3. **Generate report** using templates above

4. **Highlight actionable items**:
   - Stale branches to delete
   - Large files to consider removing
   - High-churn files that may need refactoring
   - Missing recent activity

## Example Invocations

**User**: "How healthy is this repo?"
→ Generate Quick Health Report

**User**: "Who's been most active this month?"
→ Generate Contributor Report for last 30 days

**User**: "What changed between main and feature-x?"
→ Generate Diff Report

**User**: "Any branches we should clean up?"
→ Run branch health commands, list candidates

## Notes

- All commands work with standard git (no external tools required)
- Commands are cross-platform (adjust date commands for Windows)
- Large repositories may need pagination/sampling for performance
- Respect `.gitignore` when analyzing files
