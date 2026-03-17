---
name: modern-git
description: Modern Git command best practices for AI agents. Use modern, purposeful commands introduced in Git 2.23+ instead of legacy multi-purpose commands. Teaches when to use `git switch` (branch operations), `git restore` (file operations), and other safer alternatives to improve clarity and reduce errors.
---

# Modern Git Commands

**Purpose:** This skill teaches AI agents to use modern, intuitive Git commands instead of legacy multi-purpose commands like `git checkout`. Modern commands are clearer, safer, and make code intent more obvious.

## Core Principles

1. **Use `git switch` for branch operations** - NOT `git checkout`
2. **Use `git restore` for file operations** - NOT `git checkout --`
3. **Use `git push --force-with-lease`** - NOT `git push --force`
4. **Be explicit about intent** - Clear commands prevent mistakes

## Quick Reference

### Branch Operations → Use `git switch`

```bash
# ✓ CORRECT: Modern commands
git switch main                    # Switch to existing branch
git switch -c feature-branch       # Create and switch to new branch
git switch -                       # Switch to previous branch

# ✗ AVOID: Legacy commands
git checkout main                  # Overloaded command, unclear intent
git checkout -b feature-branch     # Same operation, less clear
git checkout -                     # Same, but what does "-" mean?
```

**Why:** `git switch` has a single, clear purpose: branch operations. It provides better error messages and is harder to misuse.

### File Operations → Use `git restore`

```bash
# ✓ CORRECT: Modern commands
git restore src/app.js                        # Discard working directory changes
git restore --staged src/app.js               # Unstage file
git restore --source=abc123 src/app.js        # Restore from specific commit
git restore --staged --worktree src/app.js    # Unstage AND discard

# ✗ AVOID: Legacy commands
git checkout -- src/app.js                    # Requires confusing "--" separator
git reset HEAD src/app.js                     # "reset" sounds destructive
git checkout abc123 -- src/app.js             # Unclear what's happening
```

**Why:** `git restore` is dedicated to file operations with explicit flags (`--staged`, `--worktree`, `--source`) that make intent crystal clear.

### Force Push → Use `--force-with-lease`

```bash
# ✓ CORRECT: Safe force push
git push --force-with-lease origin feature-branch

# ✗ AVOID: Dangerous force push
git push --force origin feature-branch
```

**Why:** `--force-with-lease` checks if the remote branch has been updated by others before force pushing. Prevents accidental overwrites.

## Decision Trees

### "I need to switch branches"

```
Do you need to create the branch first?
├─ YES → git switch -c <new-branch>
└─ NO  → git switch <existing-branch>

Special cases:
├─ Previous branch → git switch -
└─ With uncommitted changes → git stash && git switch <branch> && git stash pop
                              OR git switch -c <new-branch>  (bring changes with you)
```

### "I need to fix a file"

```
What do you want to fix?
├─ Discard working directory changes
│  └─> git restore <file>
│
├─ Unstage file (keep changes in working directory)
│  └─> git restore --staged <file>
│
├─ Discard AND unstage
│  └─> git restore --staged --worktree <file>
│
└─ Restore from specific commit
   └─> git restore --source=<commit> <file>
```

### "I need to force push"

```
Why do you need to force push?
├─ After rebase/amend (common, safe scenario)
│  └─> git push --force-with-lease origin <branch>
│
├─ To overwrite remote (rare, potentially dangerous)
│  ├─ Are you SURE no one else has pushed?
│  │  ├─ YES → git push --force-with-lease origin <branch>
│  │  └─ NO  → git fetch && git rebase origin/<branch>
│  │
│  └─> Tip: ALWAYS prefer --force-with-lease over --force
```

## Common Workflows

### Workflow 1: Start New Feature

```bash
# ✓ CORRECT
git switch main
git pull
git switch -c feature/new-feature

# ✗ AVOID
git checkout main
git pull
git checkout -b feature/new-feature
```

### Workflow 2: Discard File Changes

```bash
# ✓ CORRECT
git restore src/broken.js          # Single file
git restore .                      # All files in current directory

# ✗ AVOID
git checkout -- src/broken.js
git checkout -- .
```

### Workflow 3: Unstage and Discard

```bash
# ✓ CORRECT
git restore --staged --worktree src/app.js

# OR two steps for clarity
git restore --staged src/app.js    # Unstage
git restore src/app.js              # Then discard

# ✗ AVOID
git reset HEAD src/app.js
git checkout -- src/app.js
```

### Workflow 4: Restore from Specific Commit

```bash
# ✓ CORRECT
git restore --source=abc123 src/legacy.js
git restore --source=HEAD~3 src/config.js

# ✗ AVOID
git checkout abc123 -- src/legacy.js
git checkout HEAD~3 -- src/config.js
```

### Workflow 5: Safe Rebase and Push

```bash
# ✓ CORRECT
git switch feature-branch
git rebase main
git push --force-with-lease origin feature-branch

# ✗ AVOID
git checkout feature-branch
git rebase main
git push --force origin feature-branch
```

## Safety Guidelines

### 1. Always Use Modern Commands for Common Operations

| Operation | Use This | NOT This |
|-----------|----------|----------|
| Switch branch | `git switch <branch>` | `git checkout <branch>` |
| Create branch | `git switch -c <branch>` | `git checkout -b <branch>` |
| Discard changes | `git restore <file>` | `git checkout -- <file>` |
| Unstage | `git restore --staged <file>` | `git reset HEAD <file>` |
| Force push | `git push --force-with-lease` | `git push --force` |

### 2. Be Explicit About Intent

```bash
# ✓ GOOD: Intent is obvious
git restore --staged src/app.js           # Clearly unstaging
git restore --source=HEAD~1 src/app.js    # Clearly restoring from parent commit

# ✗ UNCLEAR: What's happening?
git checkout -- src/app.js                # Restoring? From where?
git checkout HEAD~1 -- src/app.js         # Is this switching branches or restoring?
```

### 3. Protect Against Accidents

```bash
# ✓ SAFE: --force-with-lease protects against overwrites
git push --force-with-lease origin feature-branch

# ✗ DANGEROUS: Can overwrite others' work
git push --force origin feature-branch

# ✓ SAFE: git switch refuses to switch with uncommitted changes
git switch main  # Errors if uncommitted changes

# ✗ RISKY: Need to remember --discard flag
git switch --discard-changes main  # Only use when you WANT to lose changes
```

### 4. Use Stash for Experimentation

```bash
# ✓ SAFE: Can recover if experiment fails
git stash push -m "Before risky operation"
# Try risky operation
git restore --source=old-commit .
# If it fails:
git stash pop  # Recover

# ✗ RISKY: No recovery option
git restore --source=old-commit .
# Changes lost forever!
```

## When Legacy Commands Are Still OK

Some scenarios don't have modern equivalents:

```bash
# Exploring history (detached HEAD)
git checkout abc123                # Still acceptable
git switch --detach abc123         # More explicit alternative

# Complex remote tracking
git checkout -b local origin/remote  # Still commonly used
```

**Rule of thumb:** If there's a modern equivalent for your use case, use it. Legacy commands are OK only when no modern alternative exists.

## Common Mistakes to Avoid

### Mistake 1: Using `git checkout` for Everything

```bash
# ✗ BAD: Unclear intent, error-prone
git checkout main
git checkout -b feature
git checkout -- src/app.js

# ✓ GOOD: Clear intent for each operation
git switch main
git switch -c feature
git restore src/app.js
```

### Mistake 2: Forgetting `--force-with-lease`

```bash
# ✗ BAD: Can overwrite others' commits
git rebase main
git push --force origin feature-branch

# ✓ GOOD: Safe against overwrites
git rebase main
git push --force-with-lease origin feature-branch
```

### Mistake 3: Confusing `--staged` and `--worktree`

```bash
# ✗ WRONG: Only unstages, doesn't discard changes
git restore --staged src/app.js
# File still modified in working directory!

# ✓ CORRECT: Specify both if you want both
git restore --staged --worktree src/app.js
# OR
git restore --staged src/app.js  # Unstage
git restore src/app.js            # Then discard
```

### Mistake 4: Not Checking Before Discarding

```bash
# ✗ RISKY: Blindly discarding without checking
git restore .

# ✓ SAFE: Check what you're losing first
git status
git diff
git restore .
```

## Integration with AI Code Generation

When generating Git commands in code or documentation:

### 1. Default to Modern Commands

```markdown
# ✓ GOOD: Use modern commands in examples
To discard your changes, run:
\`\`\`bash
git restore src/app.js
\`\`\`

# ✗ AVOID: Don't teach legacy commands
To discard your changes, run:
\`\`\`bash
git checkout -- src/app.js
\`\`\`
```

### 2. Explain Why Modern Commands Are Better

```markdown
# ✓ GOOD: Educate users
Use `git switch` instead of `git checkout` for branch operations.
This makes your intent clearer and provides better error messages.

# ✗ INSUFFICIENT: Just showing command without context
Use `git switch main` to switch branches.
```

### 3. Use Consistent Command Patterns

```bash
# ✓ GOOD: Consistent modern commands throughout
git switch develop
git pull
git switch -c feature/new-feature
git restore --staged accidental-file.js

# ✗ INCONSISTENT: Mixing old and new
git checkout develop
git pull
git switch -c feature/new-feature
git checkout -- accidental-file.js
```

## Reference Documentation

For detailed comparisons and advanced scenarios:

- **[Command Comparison](./references/command-comparison.md)** - Side-by-side legacy vs modern command comparisons
- **[Migration Guide](./references/migration-guide.md)** - Detailed patterns for complex scenarios

## Summary Table

| Use Case | Command | Key Flags | Notes |
|----------|---------|-----------|-------|
| Switch to branch | `git switch <branch>` | `-c` (create), `-` (previous) | Replaces `git checkout <branch>` |
| Discard file changes | `git restore <file>` | `--worktree` (default) | Replaces `git checkout -- <file>` |
| Unstage file | `git restore --staged <file>` | `--staged` | Replaces `git reset HEAD <file>` |
| Restore from commit | `git restore --source=<commit> <file>` | `--source` | Replaces `git checkout <commit> -- <file>` |
| Force push safely | `git push --force-with-lease` | `--force-with-lease` | Replaces `git push --force` |

## Key Takeaway

**Always prefer modern commands for clarity, safety, and better error messages. Your future self (and code reviewers) will thank you.**

When in doubt:
- Branch operations → `git switch`
- File operations → `git restore`
- Force push → `--force-with-lease`
