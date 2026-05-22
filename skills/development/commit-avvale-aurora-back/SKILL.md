---
name: commit
description: >
  Commit and push changes to remote repository following Conventional Commits.
  Trigger: User runs /commit command.
disable-model-invocation: true
---

## When to Use

- User explicitly runs `/commit` command
- User asks to "commit and push" changes

---

## Execution Flow

### Step 1: Analyze Current State

Run these commands in parallel to understand the repository state:

```bash
# See all changed files (staged and unstaged)
git status

# See unstaged changes
git diff

# See staged changes
git diff --staged

# See recent commit style (for consistency)
git log --oneline -5
```

### Step 2: Validate Changes

Before proceeding, verify:

1. **There are actual changes** - If `git status` shows nothing to commit, inform user and stop
2. **No sensitive files** - Check for `.env`, credentials, secrets. Warn user if found
3. **Changes are related** - If changes span multiple unrelated features, suggest splitting commits

### Step 3: Generate Commit Message

Follow **Conventional Commits** format (see `.claude/skills/conventional-commits/SKILL.md`):

```
<type>(<scope>): <subject>

[optional body]
```

**Rules:**
- Analyze the diff to determine the correct `type` (feat, fix, refactor, etc.)
- Use the affected module/component as `scope`
- Write subject in imperative mood, lowercase, no period
- Add body only if the "why" isn't obvious from the subject

### Step 4: Stage and Commit

```bash
# Stage all changes (or specific files if user requested)
git add .

# Commit with HEREDOC for proper formatting
git commit -m "$(cat <<'EOF'
<type>(<scope>): <subject>

<optional body>
EOF
)"
```

### Step 5: Push to Remote

```bash
# Check if branch has upstream
git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null

# If upstream exists:
git push

# If NO upstream (new branch):
git push -u origin $(git branch --show-current)
```

### Step 6: Verify Success

```bash
# Confirm push succeeded
git status

# Show the commit that was pushed
git log --oneline -1
```

---

## Output Format

After successful execution, display:

```
Commit: <hash> <type>(<scope>): <subject>
Branch: <branch-name>
Remote: origin/<branch-name>
Status: Pushed successfully
```

If there were issues:

```
Error: <description of what went wrong>
Suggestion: <how to fix it>
```

---

## Edge Cases

### No Changes
```
No changes to commit. Working tree is clean.
```

### New Branch (No Upstream)
Automatically use `git push -u origin <branch>` to set upstream.

### Merge Conflicts
```
Cannot commit: merge conflicts detected.
Resolve conflicts in: <list of files>
Then run /commit again.
```

### Pre-commit Hook Failure
If commit fails due to hooks (linting, tests):
1. Show the error
2. Suggest fixes
3. User can run `/commit` again after fixing

---

## Commands Reference

```bash
# Analysis
git status                          # Changed files
git diff                            # Unstaged changes
git diff --staged                   # Staged changes
git log --oneline -5                # Recent commits

# Commit
git add .                           # Stage all
git add <file>                      # Stage specific
git commit -m "message"             # Create commit

# Push
git push                            # Push to upstream
git push -u origin <branch>         # Push and set upstream
git branch --show-current           # Get current branch name

# Verification
git log --oneline -1                # Last commit
git rev-parse --abbrev-ref @{u}     # Check upstream
```

---

## Related Skills

- **conventional-commits**: Commit message format and rules
- **commit-pr**: Extends this skill to also create a Pull Request

---

## Anti-Patterns

| Avoid | Do Instead |
|-------|------------|
| Committing without reviewing diff | Always run `git diff` first |
| Generic messages like "fix bug" | Be specific: `fix(auth): resolve token expiration` |
| Committing secrets/credentials | Check for `.env` files before staging |
| Force pushing without warning | Never force push; warn user if needed |
