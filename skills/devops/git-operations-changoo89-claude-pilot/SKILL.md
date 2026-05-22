---
name: git-operations
description: Use when pushing, pulling, or merging changes. Handles retries, conflicts, and error recovery.
---

# SKILL: Git Operations

> **Purpose**: Safe push/pull/merge operations with retry logic and error handling
> **Target**: All git operations

---

## Quick Start

### When to Use This Skill
- Pushing changes to remote
- Pulling latest changes
- Merging branches
- Resolving merge conflicts

### Quick Reference
```bash
# Push with retry (3 attempts, 2s delay)
git_push_with_retry() {
  local branch="${1:-$(git rev-parse --abbrev-ref HEAD)}"
  for attempt in {1..3}; do
    git push origin "$branch" 2>&1 && return 0
    echo "Retry $attempt/3..." && sleep 2
  done
  return 1
}

# Pull with fast-forward only
git pull --ff-only || echo "Manual merge required"
```

---

## Core Operations

### Push with Retry

**Purpose**: Handle transient network failures with exponential backoff (3 attempts, 2s/4s/8s delay)

```bash
git_push_with_retry() {
  local remote="${1:-origin}"
  local branch="${2:-$(git rev-parse --abbrev-ref HEAD)}"
  local max_attempts=3
  local wait_times=(2 4 8)  # Exponential backoff

  echo "🔄 Pushing to $remote/$branch..."

  for attempt in $(seq 1 $max_attempts); do
    # Attempt push
    if git push "$remote" "$branch" 2>&1; then
      echo "✓ Push successful"
      return 0
    fi

    local exit_code=$?
    local error_output="$(git push "$remote" "$branch" 2>&1 || true)"

    # Classify error
    if echo "$error_output" | grep -qiE "non-fast-forward|rejected|protected"; then
      echo "❌ Push rejected (non-fast-forward or protected branch)"
      echo "   Run: git pull --rebase && git push"
      return 1
    elif echo "$error_output" | grep -qiE "authentication|permission|credentials"; then
      echo "❌ Authentication error"
      echo "   Check git credentials: git config --list | grep credential"
      return 1
    fi

    # Retry for network/transient errors
    if [ $attempt -lt $max_attempts ]; then
      local wait_time=${wait_times[$((attempt-1))]}
      echo "⚠️  Push failed (attempt $attempt/$max_attempts), retrying in ${wait_time}s..."
      sleep "$wait_time"
    else
      echo "❌ Push failed after $max_attempts attempts"
      return 1
    fi
  done

  return 1
}
```

**Error Classification**:
- **Non-retryable** (return 1): non-fast-forward, rejected, protected branch, authentication
- **Retryable** (continue loop): network errors, connection timeout, transient failures
- **No remote** (handled by caller): Remote doesn't exist

**Retry Strategy**:
- Max attempts: 3
- Wait times: 2s, 4s, 8s (exponential backoff)
- Exit on non-retryable errors immediately

### Pull with Safety Checks

**Purpose**: Avoid destructive merges, ensure clean working tree

```bash
git_pull_safe() {
  # Check for uncommitted changes
  git diff-index --quiet HEAD -- || { echo "Uncommitted changes" >&2; return 1; }

  # Fast-forward only
  git pull --ff-only || { echo "Manual merge required" >&2; return 1; }
}
```

### Merge with Verification

**Purpose**: Safe branch merging with conflict detection

```bash
git_merge_safe() {
  local source="$1"
  local target="${2:-$(git rev-parse --abbrev-ref HEAD)}"

  git checkout "$target" || return 1
  if git merge "$source" --no-ff --no-edit; then
    echo "✓ Merged $source into $target"
  else
    echo "⚠️  Conflicts in:" && git diff --name-only --diff-filter=U
    echo "Resolve, then: git add <files> && git commit"
    return 1
  fi
}
```

---

## Error Handling & Recovery

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to connect` | Network issue | Retry with `git_push_with_retry` |
| `rejected (non-fast-forward)` | Remote has new commits | Pull first, then push |
| `conflict` | Branches diverged | Manual merge required |
| `uncommitted changes` | Dirty working tree | Commit or stash first |

### Conflict Resolution

```bash
# After merge conflict
git status  # List conflicted files
vim conflicted-file.ts  # Resolve markers
git add conflicted-file.ts
git commit

# Abort operations
git merge --abort  # Abort merge
git rebase --abort  # Abort rebase
git reset --hard HEAD  # Reset to safe state
```

### Error Recovery Pattern

```bash
git_operation_with_fallback() {
  eval "$1" && return 0
  case "$(git status 2>&1)" in
    *connection*) return 2 ;;  # Retryable
    *conflict*) return 3 ;;    # Needs intervention
    *) return 1 ;;             # Fatal
  esac
}
```

---

## Related Skills

- **using-git-worktrees**: Parallel development in isolated workspaces
- **git-master**: Comprehensive git workflow mastery

---

**Version**: claude-pilot 4.2.0
