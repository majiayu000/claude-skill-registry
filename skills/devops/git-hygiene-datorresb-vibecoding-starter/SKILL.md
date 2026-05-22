---
name: git-hygiene
description: Project-agnostic skill for git commit hygiene, linking tasks to commits, and maintaining clean repository state.
---

# Git Hygiene Skill

## Core Principle

**Never leave uncommitted files after task completion.**

- Each task = one commit (clear traceability)
- Commits link to tasks via task ID references
- Clean repository state between sessions
- Atomic changes that can be reviewed and reverted independently

## Commit Message Format

**Standard Format:**
```
[task-id] Brief description (imperative mood, <70 chars)

Optional longer explanation if needed:
- Why this change was made
- What problems it solves
- Any breaking changes or important context
```

**Examples:**

Good:
```
[task-38.1] Archive CLAUDE.md before refactoring

Preserving original documentation structure before migration to new format.
```

```
[task-12.3] Add user authentication middleware

Implements JWT-based auth for protected routes. Middleware validates tokens
and attaches user context to request object.
```

```
[task-5.2] Fix paragraph spacing in essay typography
```

Bad (avoid):
```
Updated files  # No task reference, vague
[task-12.3] Added some auth stuff  # Not imperative, unclear
Fixed bug  # No task reference or specificity
```

**Imperative Mood Guide:**
- ✅ "Add", "Fix", "Update", "Remove", "Refactor"
- ❌ "Added", "Fixed", "Updated", "Removed", "Refactored"
- Think: "This commit will [your message]"

## When to Commit

### Commit Immediately After:
1. **Task Completion** - As soon as work is done and verified
2. **Subagent Work Approval** - After reviewing subagent output (don't leave their changes uncommitted)
3. **Significant Checkpoint** - Natural breakpoint in large task (still reference same task ID)

### Before:
1. **Switching Tasks** - Never leave Task A uncommitted when starting Task B
2. **Ending Session** - Repository should be clean for next session
3. **Creating PR** - Ensure all work is committed before opening pull request

### Never:
- Batch multiple unrelated tasks into one commit
- Leave work uncommitted overnight or between sessions
- Commit mid-task unless it's a natural checkpoint

## Linking Commits to Tasks

**After every commit, update the task with commit reference:**

```bash
# 1. Make commit
git add [files]
git commit -m "[task-38.1] Archive CLAUDE.md before refactoring"

# 2. Get commit hash
git log -1 --format="%H %s"

# 3. Update task with commit reference
# Use task_edit with notesAppend field
```

**Task Note Format:**
```
✅ Committed: abc1234 - [task-38.1] Archive CLAUDE.md before refactoring
```

**Why This Matters:**
- Traceability: Find code changes from task descriptions
- Debugging: Understand why changes were made
- Handoff: Next session knows what's been completed
- Audit: Track progress and decision history

## Pre-Commit Checklist

**ALWAYS verify before committing:**

```bash
# 1. Check what's staged
git status
git diff --staged

# 2. Verify only intended files
# Remove unintended files: git reset HEAD <file>

# 3. Verify CLAUDE.md updates (if subdirectory work)
# If you worked in a subdirectory with CLAUDE.md, include it
git add path/to/subdir/CLAUDE.md

# 4. Security check
# No .env files, no credentials.json, no API keys
# If secrets detected, warn user and abort

# 5. Run tests (if applicable)
# npm test, pytest, cargo test, etc.

# 6. Run linters (if applicable)
# eslint, black, rustfmt, etc.

# 7. Commit
git commit -m "[task-id] Description"
```

**Files to INCLUDE in Commits:**
- Implementation files (code, markdown, config)
- **CLAUDE.md updates (if subdirectory work)** - Critical for project memory
- Test files (if tests added/modified)
- Documentation updates related to the work

**Files to NEVER Commit:**
- `.env`, `.env.local`, `.env.production`
- `credentials.json`, `secrets.yaml`, `config.private.*`
- API keys, tokens, passwords (even in comments)
- Large binary files without LFS
- `node_modules/`, `__pycache__/`, build artifacts (should be in .gitignore)

**If User Requests Committing Secrets:**
- Warn explicitly about security risk
- Suggest alternatives (environment variables, secret management)
- Only proceed if user confirms understanding of risk

## Branch Strategy

### Small Projects / Solo Work:
- **Main branch commits** - Direct to main for atomic changes
- Fast iteration, low overhead
- Suitable when no team review needed

### Team Projects / Large Features:
- **Feature branches** - `feature/task-38-refactor-claude-md`
- **Pull request workflow** - Review before merge
- **Branch naming**: `feature/task-[id]-[brief-description]`

### Branch Commands:
```bash
# Create feature branch
git checkout -b feature/task-38-refactor-claude-md

# Work and commit on branch
git add [files]
git commit -m "[task-38.1] Archive CLAUDE.md before refactoring"

# Push to remote
git push -u origin feature/task-38-refactor-claude-md

# Create PR (use gh cli or web interface)
gh pr create --title "[task-38] Refactor CLAUDE.md structure" --body "..."
```

## Never Do (Critical Safety Rules)

### Destructive Operations:
- ❌ `git push --force` (unless user explicitly requests and understands risk)
- ❌ `git push --force` to main/master (warn user even if requested)
- ❌ `git reset --hard` without confirming uncommitted work is backed up
- ❌ `git clean -fd` without user confirmation

### Security:
- ❌ Commit files with secrets, credentials, API keys
- ❌ Commit sensitive customer data or PII
- ❌ Override .gitignore to force-add sensitive files

### Workflow:
- ❌ Leave work uncommitted between sessions (creates confusion)
- ❌ Batch unrelated tasks into single commit (breaks traceability)
- ❌ Skip task-commit linking (loses context)
- ❌ Use `git commit --amend` unless user explicitly requests (can cause confusion with remotes)

### Git Config:
- ❌ Modify git config (user.name, user.email) without explicit user request
- ❌ Skip commit hooks (--no-verify) unless user explicitly requests

## Troubleshooting Common Issues

### Uncommitted Work Before Switching Tasks:
```bash
# Option 1: Commit if work is complete
git add [files]
git commit -m "[task-X] Brief description"

# Option 2: Stash if work is incomplete
git stash save "WIP: task-X incomplete work"
# Resume later: git stash pop
```

### Committed to Wrong Branch:
```bash
# If commit NOT pushed yet:
git reset HEAD~1  # Undo commit, keep changes
git stash  # Save changes
git checkout correct-branch
git stash pop
git commit -m "[task-id] Description"
```

### Accidentally Staged Secrets:
```bash
# Remove from staging
git reset HEAD .env

# If already committed but NOT pushed:
git reset HEAD~1  # Undo commit
# Remove secrets from file
git add [files]
git commit -m "[task-id] Description"

# If already pushed - immediate action required
# Warn user: secrets are now public, must be rotated
```

## Quality Verification

**Before Marking Task Complete:**

1. ✅ Work committed with proper task reference
2. ✅ Commit message follows format (imperative mood, <70 chars)
3. ✅ Task updated with commit hash in notes
4. ✅ **CLAUDE.md updated and committed (if subdirectory work)**
5. ✅ `git status` shows clean working directory
6. ✅ No secrets or credentials in committed files
7. ✅ Tests pass (if applicable)
8. ✅ Linting passes (if applicable)

**Session End Checklist:**

```bash
# Verify clean state
git status  # Should show "nothing to commit, working tree clean"

# Verify recent commits linked to tasks
git log --oneline -5  # Should see [task-id] references

# Verify remote is up to date (if pushing)
git push  # Or confirm intentionally not pushing
```

## Integration with Task Management

**Task Creation → Implementation → Commit → Link:**

1. **Create task** with clear description and acceptance criteria
2. **Mark task in progress** when starting work
3. **Implement changes** following task requirements
4. **Commit with task reference** in message
5. **Update task notes** with commit hash
6. **Mark task complete** after verification

**Example Workflow:**

```bash
# 1. Task created in Backlog: task-42 "Add search functionality"
# 2. Mark in progress: task_edit(id='task-42', status='In Progress')

# 3. Implement
# [write code]

# 4. Commit
git add src/search.js tests/search.test.js
git commit -m "[task-42] Add search functionality

Implements full-text search with fuzzy matching and filtering."

# 5. Link commit to task
# task_edit(id='task-42', notesAppend=['✅ Committed: abc1234 - Add search functionality'])

# 6. Mark complete
# task_edit(id='task-42', status='Done')
```

This creates complete traceability: Task → Code → Commit → Verification.
