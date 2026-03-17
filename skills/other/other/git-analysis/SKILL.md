---
name: git-analysis
description: Analyze git repository changes, branch differences, and commit history. Use when analyzing branches, comparing changes, examining commit history, or preparing for PR/commit operations.
---

# Git Analysis

This Skill provides comprehensive git repository analysis capabilities for understanding branch changes, commit history, and code differences.

## Capabilities

- Analyze branch differences and merge bases
- Extract structured commit history
- Identify changed files and their statistics
- Determine default branches and remote configuration
- Support PR creation, code review, and commit operations

## When to Use

Use this Skill when you need to:
- Analyze what changed in a branch
- Prepare information for PR creation
- Review commit history
- Compare branches
- Understand code changes for commits or reviews

## Core Analysis Steps

### 1. Identify Default Branch

Get the repository's default branch (usually `main` or `master`):

```bash
git symbolic-ref refs/remotes/origin/HEAD | sed 's@^refs/remotes/origin/@@'
```

This identifies the base branch for comparison.

### 2. Find Merge Base

Determine where the current branch diverged from the default branch:

```bash
# Get merge base
git merge-base origin/<default-branch> HEAD
```

The merge base is the commit where the branch diverged, not the current state of the base branch.

### 3. Analyze Changes

Get comprehensive change information:

```bash
# List commits from merge base
git log --oneline <merge-base>..HEAD

# Get detailed commit information
git log --format="%H|%s|%an|%ae|%ad" --date=iso <merge-base>..HEAD

# Get file statistics
git diff --stat <merge-base>..HEAD

# Get full diff
git diff <merge-base>..HEAD
```

### 4. Check Current State

Understand unstaged and staged changes:

```bash
# Check untracked files
git status

# Check staged changes
git diff --cached

# Check unstaged changes
git diff
```

## Helper Scripts

This Skill includes helper scripts for common operations:

### get_branch_diff.sh

Extracts branch differences including:
- Default branch name
- Merge base commit
- Commit list with statistics
- Changed files summary

Usage:
```bash
bash scripts/get_branch_diff.sh
```

Output format:
```
DEFAULT_BRANCH: main
MERGE_BASE: abc123def456
COMMITS: 5
CHANGED_FILES: 12
```

### get_commit_history.sh

Extracts detailed commit history in structured format:

Usage:
```bash
bash scripts/get_commit_history.sh <merge-base>
```

Output format (one commit per line):
```
hash|subject|author_name|author_email|date
```

## Best Practices

1. **Always use merge-base**: Compare from merge base, not from current base branch state
2. **Run commands in parallel**: When gathering multiple pieces of information, run independent git commands in parallel
3. **Structure the output**: Parse git output into structured data for easier consumption
4. **Handle errors gracefully**: Check if commands succeed before proceeding

## Common Patterns

### Pattern 1: Full Branch Analysis

```bash
# Get all information in parallel
git status &
git diff --cached &
git diff &
DEFAULT_BRANCH=$(git symbolic-ref refs/remotes/origin/HEAD | sed 's@^refs/remotes/origin/@@')
MERGE_BASE=$(git merge-base origin/$DEFAULT_BRANCH HEAD)
git log --oneline $MERGE_BASE..HEAD
git diff --stat $MERGE_BASE..HEAD
wait
```

### Pattern 2: Commit History Extraction

```bash
# Get structured commit data
MERGE_BASE=$(git merge-base origin/$(git symbolic-ref refs/remotes/origin/HEAD | sed 's@^refs/remotes/origin/@@') HEAD)
git log --format="%H|%s|%an|%ae|%ad" --date=iso $MERGE_BASE..HEAD
```

### Pattern 3: Change Summary

```bash
# Get high-level change summary
MERGE_BASE=$(git merge-base origin/$(git symbolic-ref refs/remotes/origin/HEAD | sed 's@^refs/remotes/origin/@@') HEAD)
echo "Commits: $(git log --oneline $MERGE_BASE..HEAD | wc -l)"
echo "Files changed: $(git diff --stat $MERGE_BASE..HEAD | tail -1)"
```

## Integration with Other Skills

This Skill works well with:
- `github-pr-best-practices`: Use git analysis results to generate PR content
- Commit message generation: Analyze changes to create meaningful commit messages
- Code review: Understand what changed for review purposes

## Error Handling

Handle common git errors:

```bash
# Check if in git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "Error: Not in a git repository"
    exit 1
fi

# Check if remote exists
if ! git ls-remote origin > /dev/null 2>&1; then
    echo "Error: Remote 'origin' not found"
    exit 1
fi

# Check if branch has commits
if [ -z "$(git log --oneline $MERGE_BASE..HEAD)" ]; then
    echo "Warning: No commits found in branch"
fi
```

## Output Format Recommendations

When presenting git analysis results:

1. **Summary first**: Start with high-level statistics
2. **Structured data**: Use consistent formatting for easy parsing
3. **Contextual information**: Include branch names and dates
4. **Actionable insights**: Highlight what's important for the task

Example output structure:
```
Branch Analysis Summary
-----------------------
Base branch: main
Current branch: feature/new-feature
Diverged at: abc123d (2025-01-15)

Changes:
- 5 commits
- 12 files changed
- 234 insertions, 89 deletions

Recent commits:
1. feat(api): add new endpoint (2025-01-16)
2. test(api): add endpoint tests (2025-01-16)
3. docs(api): update API documentation (2025-01-17)
...
```

## Related Git Commands Reference

See [REFERENCE.md](REFERENCE.md) for detailed git command documentation and advanced usage patterns.
