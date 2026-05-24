---
model: haiku
name: git-cli-agentic
description: Git commands optimized for AI agent workflows with porcelain output and deterministic execution patterns.
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git log:*), Bash(git branch:*), Bash(git remote:*), Bash(git add:*), Bash(git commit:*), Bash(git push:*), Bash(git restore:*), Read
---

# Git CLI Agentic Patterns

Optimized git commands for AI agent consumption using porcelain output and stable formats.

## Core Principle

Use `--porcelain` for machine-readable output that remains stable across Git versions and user configurations.

## Status Operations

### Porcelain Status

```bash
# Version 2 porcelain with branch info (recommended)
git status --porcelain=v2 --branch

# Version 1 porcelain (simpler)
git status --porcelain

# Short format (human-readable but stable)
git status --short --branch
```

**Porcelain v2 Format**:
```
# branch.oid <commit>
# branch.head <branch>
# branch.upstream <upstream>
# branch.ab +<ahead> -<behind>
1 <XY> <sub> <mH> <mI> <mW> <hH> <hI> <path>
2 <XY> <sub> <mH> <mI> <mW> <hH> <hI> <X><score> <path><tab><origPath>
? <path>
! <path>
```

**Status Codes**:

| Code | Meaning |
|------|---------|
| `M` | Modified |
| `A` | Added |
| `D` | Deleted |
| `R` | Renamed |
| `C` | Copied |
| `?` | Untracked |
| `!` | Ignored |

### Quick Checks

```bash
# Check if clean (empty output = clean)
git status --porcelain

# Count changed files
git status --porcelain | wc -l

# Check for uncommitted changes
git diff --quiet || echo "has changes"
```

## Diff Operations

### Stat Output

```bash
# File change summary
git diff --stat

# Numeric stats (machine-readable)
git diff --numstat

# Name and status only
git diff --name-status

# Names only
git diff --name-only
```

**Numstat Format**: `<added>\t<deleted>\t<filename>`

### Staged vs Unstaged

```bash
# Unstaged changes
git diff --numstat

# Staged changes
git diff --cached --numstat

# Both (working tree vs HEAD)
git diff HEAD --numstat
```

### Specific Comparisons

```bash
# Against specific commit
git diff $COMMIT --numstat

# Between branches
git diff main..feature --numstat

# Between commits
git diff $COMMIT1..$COMMIT2 --name-status
```

## Log Operations

### Custom Format

```bash
# Hash and subject only
git log --format='%H %s' -n 10

# Oneline (built-in)
git log --oneline -n 10

# With stats
git log --oneline --stat -n 5

# Machine-parseable with multiple fields
git log --format='%H|%an|%ae|%s' -n 10
```

**Format Placeholders**:

| Placeholder | Meaning |
|-------------|---------|
| `%H` | Full commit hash |
| `%h` | Short hash |
| `%s` | Subject |
| `%b` | Body |
| `%an` | Author name |
| `%ae` | Author email |
| `%ad` | Author date |
| `%cn` | Committer name |

### Filtering

```bash
# By author
git log --author="name" --oneline -n 10

# By date range
git log --since="2025-01-01" --oneline

# By path
git log --oneline -n 10 -- path/to/file

# Merge commits only
git log --merges --oneline -n 5
```

## Branch Operations

### Branch Info

```bash
# List with tracking info
git branch -vv

# Formatted output
git branch --format='%(refname:short) %(upstream:short) %(upstream:track)'

# Current branch only
git branch --show-current

# Remote branches
git branch -r --format='%(refname:short)'
```

### Tracking Status

```bash
# Ahead/behind count
git rev-list --left-right --count origin/main...HEAD

# Output: <behind>\t<ahead>
```

## Remote Operations

```bash
# List remotes with URLs
git remote -v

# Get specific remote URL
git remote get-url origin

# Show remote details
git remote show origin
```

## Staging Operations

```bash
# Stage specific files
git add path/to/file

# Stage all modified tracked files
git add -u

# Stage everything
git add -A

# Unstage file
git restore --staged path/to/file

# Discard changes
git restore path/to/file
```

## Commit Operations

```bash
# Simple commit
git commit -m "message"

# With body (heredoc)
git commit -m "$(cat <<'EOF'
Subject line

Body paragraph.

Co-Authored-By: Name <email>
EOF
)"

# Amend last commit (use carefully)
git commit --amend -m "new message"
```

## Push Operations

```bash
# Push current branch
git push origin HEAD

# Push to different remote branch (main-branch development)
git push origin main:feature-branch

# Push commit range
git push origin start^..end:feature-branch

# Set upstream
git push -u origin HEAD
```

## Agentic Optimizations

| Context | Command |
|---------|---------|
| Quick status | `git status --porcelain=v2 --branch` |
| Changed files | `git diff --name-status` |
| Staged changes | `git diff --cached --numstat` |
| Recent commits | `git log --format='%h %s' -n 5` |
| Branch tracking | `git branch -vv --format='%(refname:short) %(upstream:track)'` |
| Current branch | `git branch --show-current` |

## Error Handling in Context

Always include fallback for context expressions:

```markdown
- Git status: !`git status --porcelain=v2 --branch 2>/dev/null || echo "not a git repo"`
- Current branch: !`git branch --show-current 2>/dev/null || echo "detached"`
- Remote URL: !`git remote get-url origin 2>/dev/null || echo "no remote"`
```

## Combining with GH CLI

For GitHub-specific operations, combine with `gh` commands:

```bash
# Get repo owner/name
gh repo view --json nameWithOwner --jq '.nameWithOwner'

# Then use in git operations
git push origin main:$(gh pr view --json headRefName --jq '.headRefName')
```

## Best Practices

1. **Use porcelain v2** for status when parsing programmatically
2. **Use --numstat** for diff when counting changes
3. **Use custom --format** for log when extracting specific fields
4. **Always add 2>/dev/null fallback** in context expressions
5. **Prefer git switch/restore** over checkout for clarity
