---
name: research-git-patterns
description: Git-aware skill for finding implementation patterns and retrieving story context from git history. Use when searching for similar implementations or understanding how a feature was built. To use this skill, you must have a story ID (e.g., "US-001-auth-login-admin"). Use research-user-stories skill to find the story ID.
---

# Research Git Patterns

## When to Use

INVOKE when user asks about:

- How a feature was implemented
- Finding similar code patterns
- Understanding implementation history
- Retrieving story context

## Git Commands for Story Retrieval

### Find All Commits for a Story

```bash
# Get full implementation history
git log --grep="US-001-auth-login-admin" --oneline --graph

# Get detailed changes with code
git log --grep="US-001-auth-login-admin" -p --follow

# Get just the files changed
git diff --name-only main...$(git log --grep="US-001-auth-login-admin" -1 --format=%H)
```

### Analyze Implementation Patterns

```bash
# Find similar authentication implementations
git log --grep="auth\|login\|clerk" --oneline

# See how rate limiting was implemented across stories
git log -S"RateLimiter" -p

# Find all FastAPI endpoint additions
git log --diff-filter=A -- "apps/server/src/api/**/*.py"
```

### Extract Story Context

```bash
# Get story implementation timeline
git log --grep="US-001-auth-login-admin" --format="%ai %s" | sort

# Calculate implementation time
git log --grep="US-001-auth-login-admin" --format="%at" | awk 'NR==1{first=$1} END{print (last-first)/3600 " hours"}'

# Get test coverage evolution
git log --grep="US-001-auth-login-admin" --format="%h" | xargs -I {} sh -c 'git show {}:coverage.json 2>/dev/null | jq .total'
```

### Build Complete Context

```bash
# Create story summary
story="US-001-auth-login-admin"
echo "=== Story $story Implementation ==="
echo "\n📝 Commits:"
git log --grep="$story" --oneline

echo "\n📁 Files Modified:"
git diff --name-status main...$(git log --grep="$story" -1 --format=%H)

echo "\n✅ Tests Added:"
git diff main...$(git log --grep="$story" -1 --format=%H) -- "*test*.py" --name-only

echo "\n📊 Statistics:"
git log --grep="$story" --shortstat | grep -E "files? changed"
```

## Pattern Mining

### Find Reusable Patterns

```python
# Example: Find all endpoint security patterns
patterns = {
    "auth": "git log -S'@router.post.*Depends.*get_current_user' -p",
    "rate_limit": "git log -S'RateLimiter' -p",
    "validation": "git log -S'@validator' -p",
    "error_handling": "git log -S'HTTPException' -p"
}
```

### Generate Implementation Template

```bash
# Extract common backend structure from story
git show --format="" --name-only $(git log --grep="US-001-auth-login-admin" --format=%H) |
  grep "apps/server" |
  sed 's|apps/server/||' |
  sort -u
```

## Context Building for Claude

When building context from git:

1. **Start with story commits**

   ```bash
   git log --grep="US-XXX" --oneline
   ```

2. **Get implementation details**

   ```bash
   git show <commit-hash>
   ```

3. **Find related patterns**

   ```bash
   git log -S"<key-concept>" --oneline
   ```

4. **Build file history**
   ```bash
   git log --follow -p -- <file-path>
   ```

## Integration with User Stories

The minimal user story files reference git commits. Use these commands to expand context:

```bash
# From user story: "Implementation: git log --grep='US-001-auth-login-admin'"
# Expand to full context:
git log --grep="US-001-auth-login-admin" --stat --format=fuller
```

## Efficiency Tips

1. **Use git aliases** for common patterns:

   ```bash
   git config --global alias.story 'log --grep'
   git config --global alias.pattern 'log -S'
   ```

2. **Cache results** in Memory MCP:

   - Story implementation summaries
   - Common patterns
   - Reusable code blocks

3. **Batch operations** for multiple stories:
   ```bash
   for story in US-001-auth-login-admin US-002 US-003; do
     echo "=== $story ==="
     git log --grep="$story" --oneline
   done
   ```

## Error Recovery

If git history is unclear:

1. Check commit message conventions
2. Use broader search patterns
3. Fallback to file-based search
4. Ask user for clarification

## Performance Metrics

Git operations are typically:

- `git log --grep`: <100ms
- `git show`: <50ms per commit
- `git diff`: <200ms for feature branch
- Full story context: <2 seconds

Compare to file reading:

- Multiple file reads: 500ms-2s
- Context building: 2-5s
- Pattern searching: 1-3s

**Git approach is 3-5x faster for context retrieval**
