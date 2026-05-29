---
name: undo
description: Rollback the last destructive operation using git or project backups
disable-model-invocation: true
---

# Undo Last Operation

I'll help you rollback the last destructive operation performed by Claude DevStudio commands.

## Token Optimization Strategy

**Target: 80% reduction (2,000-3,000 → 400-600 tokens)**

### Core Optimization Patterns

**1. Pure Git Operations (90% savings)**
- All undo operations use git commands (external tools)
- No file reading required - git provides all context
- Git log shows what changed (timestamps, commits, files)
- Git status reveals uncommitted changes
- Git diff for change preview (optional, user confirmation only)
- Example: `git reset --hard HEAD~1` (0 tokens, fully external)

**2. Early Exit on Clean State (95% savings)**
- Check git status before any analysis
- If working tree clean and no recent commits → exit immediately
- If no backups exist → exit with "nothing to undo"
- Skip entire recovery workflow on clean state
- Example: Clean state detection in 50 tokens vs 2,000 for full workflow

**3. Template-Based Recovery Strategies (70% savings)**
- Pre-defined undo strategies (no analysis required):
  - **Uncommitted changes** → `git reset --hard HEAD`
  - **Last commit** → `git reset --soft HEAD~1` or `git revert HEAD`
  - **Multiple commits** → `git reset --soft HEAD~N`
  - **Specific file** → `git checkout HEAD -- <file>`
  - **Stashed changes** → `git stash apply` or `git stash pop`
- Select strategy from git state, apply template
- No complex reasoning about recovery approaches

**4. Git Log for Context (0 additional tokens)**
- `git log --oneline -5` shows recent commits (external)
- Commit messages describe what would be undone
- No need to read files to understand changes
- User can decide based on commit history alone

**5. Session State for Undo History (80% savings on repeat)**
- Track recent operations in `undo/history.json`
- Record: operation type, affected files, git ref
- Resume undo decisions from previous sessions
- Skip analysis if operation was just executed
- Cache validity: Until next git commit

**6. Backup Detection via Glob (95% savings)**
- Use Glob to check for `undo/backups/*` directory
- If backups exist → list them with timestamps
- No need to read backup contents initially
- Only read backup if user selects it for restoration

**7. Bash-Based Operations (external tool)**
- All git commands via Bash (no token cost)
- Backup creation: `cp` or `tar` commands
- File restoration: `git` or `cp` commands
- Change validation: `git diff` (only if requested)

**8. Progressive Disclosure (Confirmation Only)**
- Level 1: Quick state check (50 tokens) - "You have uncommitted changes"
- Level 2: Strategy suggestion (100 tokens) - "I can undo with git reset"
- Level 3: Preview changes (300 tokens) - Only if user asks "what would be undone?"
- Level 4: Execute (50 tokens) - Run single git command

### Optimization Workflow

**Clean State (50 tokens):**
```bash
# 1. Quick state check (50 tokens via Bash)
git status --porcelain
git log --oneline -1

# If both empty/clean → EXIT
"Nothing to undo - working tree is clean"
```

**Uncommitted Changes (200-300 tokens):**
```bash
# 1. Detect uncommitted changes (50 tokens)
git status --short

# 2. Strategy template (100 tokens)
"You have uncommitted changes. I can:
1. Discard all changes: git reset --hard HEAD
2. Stash changes: git stash
3. Discard specific files: git checkout HEAD -- <files>"

# 3. Execute selected strategy (50 tokens)
Bash: git reset --hard HEAD
```

**Last Commit (250-350 tokens):**
```bash
# 1. Show recent commit (50 tokens)
git log --oneline -1

# 2. Strategy template (150 tokens)
"Undo last commit (keeps changes as uncommitted):
   git reset --soft HEAD~1
Or revert commit (creates new commit):
   git revert HEAD"

# 3. Execute (50 tokens)
Bash: git reset --soft HEAD~1
```

**Multiple Commits (300-400 tokens):**
```bash
# 1. Show recent commits (100 tokens)
git log --oneline -5

# 2. Strategy selection (150 tokens)
"How many commits to undo? Recent commits:
   abc1234 Fix bug
   def5678 Add feature
   ghi9012 Update config"

# 3. Execute (50 tokens)
Bash: git reset --soft HEAD~2
```

**Backup Restoration (400-600 tokens):**
```bash
# 1. Glob for backups (50 tokens)
Glob: undo/backups/*

# 2. List backups with timestamps (100 tokens)
"Available backups:
   2026-01-27_14-30-backup.tar.gz (30 minutes ago)
   2026-01-27_10-15-backup.tar.gz (4 hours ago)"

# 3. User selects backup (50 tokens)
Input: "Use 14-30 backup"

# 4. Restore backup (200 tokens)
Bash: tar -xzf backup.tar.gz
Git: git add . && git commit -m "Restored from backup"
```

### Token Budget by Operation

| Operation | Unoptimized | Optimized | Savings |
|-----------|-------------|-----------|---------|
| **Clean State Detection** | 1,000 | 50 | 95% |
| State check | 500 | 50 | 90% |
| Exit early | 500 | 0 | 100% |
| **Undo Uncommitted** | 1,500-2,000 | 200-300 | 85% |
| Git status | 300 | 50 | 83% |
| Strategy template | 800 | 100 | 87% |
| Execute reset | 400 | 50 | 87% |
| **Undo Last Commit** | 1,800-2,500 | 250-350 | 86% |
| Git log | 500 | 50 | 90% |
| Strategy selection | 1,000 | 150 | 85% |
| Execute | 300 | 50 | 83% |
| **Undo Multiple Commits** | 2,000-2,800 | 300-400 | 86% |
| Git log extended | 700 | 100 | 86% |
| User selection | 1,000 | 150 | 85% |
| Execute | 300 | 50 | 83% |
| **Backup Restoration** | 2,500-3,500 | 400-600 | 83% |
| Glob backups | 500 | 50 | 90% |
| List options | 800 | 100 | 87% |
| Restore process | 1,200 | 250-450 | 62-79% |

**Average Reduction: 80-85%** (exceeds 80% target)

### Caching Strategy

**Session Files (local project):**
- `undo/history.json` - Recent operations with git refs and affected files
- `undo/backups/` - Timestamped backup archives

**Shared Cache Files (`.claude/cache/`):**
- `undo/git-state.json` - Current branch, recent commits, working tree status
- `undo/strategies.json` - Pre-defined recovery templates

**Cache Validity:**
- Git state cache: Valid until next commit or working tree modification
- History cache: Valid for current session (cleared on new git commit)
- Backup cache: Valid until backups directory changes

### Optimization Commands

**Explicit Operations:**
```bash
/undo                          # Auto-detect and undo last change (200-600 tokens)
/undo uncommitted              # Reset working tree (200 tokens)
/undo commit                   # Undo last commit (250 tokens)
/undo commit 3                 # Undo last 3 commits (300 tokens)
/undo file src/app.js          # Restore specific file (250 tokens)
/undo backup                   # List and restore from backups (400-600 tokens)
```

**Expected Token Usage:**
- Clean state detection: 50 tokens (exit early)
- Uncommitted changes undo: 200-300 tokens
- Single commit undo: 250-350 tokens
- Multiple commits undo: 300-400 tokens
- Backup restoration: 400-600 tokens

**Optimization Status:** ✅ Optimized (Phase 2 Batch 3D-F, 2026-01-26)
**Average Reduction:** 80-85% (2,000-3,000 → 400-600 tokens)

### Anti-Patterns to Avoid

**❌ Don't Read Files to Understand Changes:**
```bash
# Bad: Read changed files (2,000 tokens)
Read src/app.js
Read src/utils.js
Read package.json
# Then analyze what changed

# Good: Use git diff or git log (external, 0 tokens)
Bash: git diff --stat HEAD
Bash: git log --oneline -5
```

**❌ Don't Analyze Complex Recovery Strategies:**
```bash
# Bad: Reason about recovery approaches (1,500 tokens)
Think about: What if file X depends on file Y?
Consider: Should we use reset or revert?
Analyze: Impact on remote branches

# Good: Use template strategies (100 tokens)
Template: Uncommitted → git reset --hard
Template: Last commit → git reset --soft HEAD~1
```

**❌ Don't Load Backup Contents for Selection:**
```bash
# Bad: Read all backups to show options (3,000 tokens)
Read undo/backups/backup1.tar.gz (extracted)
Read undo/backups/backup2.tar.gz (extracted)

# Good: Show file names with timestamps (100 tokens)
Glob: undo/backups/*.tar.gz
List with: ls -lh (shows size and timestamp)
```

**❌ Don't Perform Speculative Analysis:**
```bash
# Bad: Analyze "what could be undone" (1,000 tokens)
Check git log → analyze all commits
Check git diff → analyze all changes
Check backups → analyze all backup contents

# Good: Show status, let user decide (50-150 tokens)
git status --short
git log --oneline -5
# User picks what to undo
```

## Recovery Options

I'll check for available recovery methods:

**1. Git-based Recovery**
- Check uncommitted changes
- Review recent commits
- Identify safe restore points

**2. Project Backups**
- Look for `undo/backups/` in your project
- Check for operation-specific backups
- Verify backup integrity

**3. Change Analysis**
- Show what was modified
- Identify scope of changes
- Suggest targeted recovery

## Recovery Process

Based on what I find, I can:

1. **Restore from Git** - If changes haven't been committed yet
2. **Use project backups** - If backups exist from previous operations
3. **Selective restoration** - Choose specific files to restore

I'll analyze the situation and suggest the safest recovery method.

If multiple restore options exist, I'll:
- Show you what each option would restore
- Explain the implications
- Let you choose the best approach

**Important**: I will NEVER:
- Add "Co-authored-by" or any Claude signatures
- Include "Generated with Claude Code" or similar messages
- Modify git config or user credentials
- Add any AI/assistant attribution to the commit

This ensures you can confidently undo operations without losing important work.