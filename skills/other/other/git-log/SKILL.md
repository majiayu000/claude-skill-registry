---
name: git-log
description: Generate appropriate commit messages and maintain git log documentation. Use when preparing to commit changes, reviewing git history, or maintaining project change documentation. Provides commit message generation, git log maintenance, and quick command reference.
---

# Git Log - Commit & Documentation

Generate structured commit messages and maintain comprehensive git log documentation for the VRP toolkit project.

## When to Use

Use this skill when:
- Preparing to commit changes to the repository
- Reviewing git history to understand recent changes
- Maintaining the project's change documentation
- Need quick reference for common git commands
- Want to ensure consistent commit message formatting

## Core Workflow: Commit & Log

### Step 1: Analyze Changes
Before committing, analyze the current changes:
```bash
git status
git diff --staged  # If changes already staged
git diff           # If changes not staged
```

**Key questions to answer:**
- What files were modified/added/deleted?
- What is the nature of changes (feature, bug fix, docs, refactor)?
- What scope is affected (e.g., architecture, setup, migration)?

### Step 2: Generate Commit Message
Based on the changes, generate a commit message following Conventional Commits format:

**Format:** `<type>(<scope>): <subject>`

**Common types for this project:**
- `feat`: New feature or functionality
- `fix`: Bug fix
- `docs`: Documentation changes
- `refactor`: Code refactoring (no behavior change)
- `test`: Adding or updating tests
- `chore`: Maintenance tasks, dependency updates
- `style`: Code style changes (formatting, etc.)

**Common scopes for this project:**
- `architecture`: Changes to overall architecture
- `migration`: File migrations from SDR_stochastic
- `setup`: Project setup, installation, dependencies
- `alns`: ALNS algorithm changes
- `pdptw`: PDPTW problem definition
- `data`: Data layer changes
- `visualization`: Visualization tools
- `tutorials`: Tutorial notebooks

**Subject guidelines:**
- Use imperative mood: "add" not "added" or "adds"
- First letter lowercase
- No period at end
- Keep under 50 characters if possible

**Body (optional but recommended):**
- Explain what changed and why
- Use bullet points for multiple changes
- Reference issues or related work

**Examples:**
```
feat(architecture): implement unified Solver interface for problem-algorithm separation

- Create VRPProblem, VRPSolution, Solver abstract base classes
- Implement ALNSSolver adapter pattern
- Update quickstart tutorial to demonstrate new interface
```

```
chore: update migration progress (9/9 files)

- Update CLAUDE.md completed tasks section
- Add migration entry to MIGRATION_LOG.md
- Update progress statistics
```

### Step 3: Maintain Git Log Documentation
After committing, update the git log documentation file (`.claude/GIT_LOG.md`):

**File structure:**
```markdown
# Git Log - VRP Toolkit Project

*Comprehensive record of all commits with detailed information.*

## Recent Commits (newest first)

### 2026-01-01 - feat(architecture): implement unified Solver interface
**Hash:** 4569fa1
**Author:** [Author Name]
**Date:** 2026-01-01 12:34:56

**Changes:**
- Created base.py module with abstract base classes
- Implemented adapter pattern for backward compatibility
- Updated quickstart tutorial

**Files modified:**
- vrp_toolkit/algorithms/base.py
- vrp_toolkit/algorithms/alns/solver.py
- tutorials/01_quickstart.ipynb

---

### 2025-12-31 - chore: update migration progress (9/9)
**Hash:** 9590014
**Author:** [Author Name]
**Date:** 2025-12-31 10:20:30

**Changes:**
- Updated CLAUDE.md with completed migration status
- Added final migration entry to MIGRATION_LOG.md

**Files modified:**
- .claude/CLAUDE.md
- .claude/MIGRATION_LOG.md
```

**Update process:**
1. Extract commit information: `git log -1 --pretty=format:"%H|%an|%ad|%s" --date=iso`
2. Get changed files: `git show --name-only --pretty=format:"" HEAD`
3. Format entry using template above
4. Add to top of "Recent Commits" section in `.claude/GIT_LOG.md`
5. Keep only last 20-30 commits in main section (archive older ones if needed)

### Step 4: Execute Commit
Provide the user with exact commands to execute:

```bash
# Stage changes
git add [file1] [file2] ...

# Commit with generated message
git commit -m "feat(architecture): implement unified Solver interface

- Create VRPProblem, VRPSolution, Solver abstract base classes
- Implement ALNSSolver adapter pattern
- Update quickstart tutorial to demonstrate new interface"

# Push to remote (if desired)
git push
```

## Quick Command Reference

### Status & Diff
```bash
git status -s          # Short status
git diff               # Unstaged changes
git diff --staged      # Staged changes
git diff HEAD~1        # Compare with previous commit
```

### Commit Operations
```bash
git commit -am "msg"   # Stage tracked files and commit
git commit --amend     # Amend last commit
git commit --amend --no-edit  # Amend without changing message
```

### Branch Operations
```bash
git checkout -b feature-name  # Create and switch branch
git switch -c feature-name    # Modern equivalent
git branch -d branch-name     # Delete local branch
```

### History & Log
```bash
git log --oneline -10         # Last 10 commits, one line
git log --oneline --graph --all  # Graphical history
git show HEAD                 # Show last commit details
```

### Undo & Reset
```bash
git restore --staged file.py  # Unstage file
git restore file.py           # Discard unstaged changes
git reset --soft HEAD~1       # Undo commit, keep changes
```

## Integration with Other Skills

**update-progress:** After updating CLAUDE.md and MIGRATION_LOG.md, use git-workflow to commit the documentation updates.

**migrate-module:** After migrating files, use git-workflow to commit the migrated code.

**build-session-context:** Read GIT_LOG.md to understand recent changes when starting a session.

**update-task-board:** Use GIT_LOG.md to track completion of development tasks.

## Project-Specific Patterns

### Migration Commits
```bash
git add vrp_toolkit/problems/pdptw.py
git commit -m "feat(migration): migrate instance.py to pdptw.py

- Extract generic Instance class
- Add type hints and docstrings
- Create basic test suite"
```

### Progress Update Commits
```bash
git add .claude/CLAUDE.md .claude/MIGRATION_LOG.md
git commit -m "chore: update migration progress (5/9 files)

- Mark instance.py migration as completed
- Update progress statistics
- Add detailed migration entry"
```

### Tutorial/Example Commits
```bash
git add tutorials/01_quickstart.ipynb
git commit -m "docs: add quickstart tutorial

- Show basic instance creation
- Demonstrate ALNS solving
- Include visualization examples"
```

## GIT_LOG.md Maintenance

### Initial Setup
If `.claude/GIT_LOG.md` doesn't exist, create it with the structure above.

### Regular Updates
After each commit, update GIT_LOG.md with the new commit information.

### Archive Strategy
- Keep last 20 commits in "Recent Commits" section
- Move older commits to "Archive" section at bottom
- Consider monthly archives if volume is high

### Automation Notes
When AI uses this skill, it should:
1. Analyze current git changes
2. Generate appropriate commit message
3. Show user exact commands to execute
4. After commit, update GIT_LOG.md with new entry
5. Keep GIT_LOG.md organized and readable

## Troubleshooting

### Empty Commit Message
If commit message seems generic, ask:
- What specific functionality was added/fixed?
- Which files were most significantly changed?
- What problem does this change solve?

### Multiple Change Types
If changes include mixed types (e.g., feat and fix):
- Create separate commits if possible
- If must combine, use most significant type and explain in body

### Missing GIT_LOG.md
If file doesn't exist, create it with current commit history:
```bash
# Get last 20 commits for initial log
git log --oneline -20
```