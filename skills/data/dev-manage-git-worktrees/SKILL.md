---
name: dev_manage_git-worktrees
model: sonnet
tools:
  - Bash
  - Read
  - AskUserQuestion
description: |
  Use when starting feature work that needs isolation from current workspace or
  before executing implementation plans - creates isolated git worktrees with
  smart directory selection and safety verification.

  Triggers: "worktree", "isolated workspace", "feature branch isolation",
  "multiple branches", "parallel development"
---

# Using Git Worktrees

## Overview

Git worktrees create isolated workspaces sharing the same repository, allowing work on multiple branches simultaneously without switching.

**Core principle:** Systematic directory selection + safety verification = reliable isolation.

**Announce at start:** "I'm using the dev_manage_git-worktrees skill to set up an isolated workspace."

## Primary Sources

**Git Documentation**:
- `git worktree --help` - Complete git worktree reference
- `git worktree list` - Show all worktrees
- `git worktree remove` - Cleanup worktrees

**Integration**:
- `.claude/agents/git-operations/` - Delegates worktree setup to this skill
- `finishing-a-development-branch` skill - REQUIRED for cleanup after work complete

## Directory Selection Process

Follow this priority order:

### 1. Check Existing Directories

```bash
# Check in priority order
ls -d .worktrees 2>/dev/null     # Preferred (hidden)
ls -d worktrees 2>/dev/null      # Alternative
```

**If found:** Use that directory. If both exist, `.worktrees` wins.

### 2. Check CLAUDE.md

```bash
grep -i "worktree.*director" CLAUDE.md 2>/dev/null
```

**If preference specified:** Use it without asking.

### 3. Ask User

If no directory exists and no CLAUDE.md preference:

```
No worktree directory found. Where should I create worktrees?

1. .worktrees/ (project-local, hidden)
2. ~/.config/superpowers/worktrees/<project-name>/ (global location)

Which would you prefer?
```

## Safety Verification

### For Project-Local Directories (.worktrees or worktrees)

**MUST verify .gitignore before creating worktree:**

```bash
# Check if directory pattern in .gitignore
grep -q "^\.worktrees/$" .gitignore || grep -q "^worktrees/$" .gitignore
```

**If NOT in .gitignore:**

Per "Fix broken things immediately" principle:
1. Add appropriate line to .gitignore
2. Commit the change
3. Proceed with worktree creation

**Why critical:** Prevents accidentally committing worktree contents to repository.

### For Global Directory (~/.config/superpowers/worktrees)

No .gitignore verification needed - outside project entirely.

## Creation Steps

### 1. Detect Project Name

```bash
project=$(basename "$(git rev-parse --show-toplevel)")
```

### 2. Create Worktree

```bash
# Determine full path
case $LOCATION in
  .worktrees|worktrees)
    path="$LOCATION/$BRANCH_NAME"
    ;;
  ~/.config/superpowers/worktrees/*)
    path="~/.config/superpowers/worktrees/$project/$BRANCH_NAME"
    ;;
esac

# Create worktree with new branch
git worktree add "$path" -b "$BRANCH_NAME"
cd "$path"
```

### 3. Run Project Setup

Auto-detect and run appropriate setup:

```bash
# Node.js
if [ -f package.json ]; then npm install; fi

# Rust
if [ -f Cargo.toml ]; then cargo build; fi

# Python
if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
if [ -f pyproject.toml ]; then poetry install; fi

# Go
if [ -f go.mod ]; then go mod download; fi
```

### 4. Verify Clean Baseline

Run tests to ensure worktree starts clean:

```bash
# Examples - use project-appropriate command
npm test
cargo test
pytest
go test ./...
```

**If tests fail:** Report failures, ask whether to proceed or investigate.

**If tests pass:** Report ready.

### 5. Report Location

```
Worktree ready at <full-path>
Tests passing (<N> tests, 0 failures)
Ready to implement <feature-name>
```

## Complete Workflow Example

```bash
# 1. Announce
echo "I'm using the dev_manage_git-worktrees skill to set up an isolated workspace."

# 2. Check existing directories
if [ -d .worktrees ]; then
  DIR=".worktrees"
elif [ -d worktrees ]; then
  DIR="worktrees"
else
  # Check CLAUDE.md for preference
  PREF=$(grep -i "worktree.*directory" CLAUDE.md 2>/dev/null)
  # If no preference, ask user
  # ... (use AskUserQuestion tool)
fi

# 3. Verify .gitignore (project-local only)
if [[ $DIR == ".worktrees" ]] || [[ $DIR == "worktrees" ]]; then
  if ! grep -q "^$DIR/$" .gitignore; then
    echo "$DIR/" >> .gitignore
    git add .gitignore
    git commit -m "Add $DIR/ to .gitignore"
  fi
fi

# 4. Create worktree
git worktree add "$DIR/feature-auth" -b "feature/auth"
cd "$DIR/feature-auth"

# 5. Run setup
if [ -f package.json ]; then
  npm install
fi

# 6. Verify baseline
npm test

# 7. Report
echo "Worktree ready at $(pwd)"
echo "Tests passing (47 tests, 0 failures)"
echo "Ready to implement auth feature"
```

## Quick Reference

| Situation | Action |
|-----------|--------|
| `.worktrees/` exists | Use it (verify .gitignore) |
| `worktrees/` exists | Use it (verify .gitignore) |
| Both exist | Use `.worktrees/` |
| Neither exists | Check CLAUDE.md → Ask user |
| Directory not in .gitignore | Add it immediately + commit |
| Tests fail during baseline | Report failures + ask |
| No package.json/Cargo.toml | Skip dependency install |

## Common Mistakes

### ❌ Skipping .gitignore Verification

**Problem:** Worktree contents get tracked, pollute git status

**Fix:** Always grep .gitignore before creating project-local worktree

### ❌ Assuming Directory Location

**Problem:** Creates inconsistency, violates project conventions

**Fix:** Follow priority: existing > CLAUDE.md > ask

### ❌ Proceeding with Failing Tests

**Problem:** Can't distinguish new bugs from pre-existing issues

**Fix:** Report failures, get explicit permission to proceed

### ❌ Hardcoding Setup Commands

**Problem:** Breaks on projects using different tools

**Fix:** Auto-detect from project files (package.json, Cargo.toml, etc.)

## Integration Points

### Called By

- **git-operations** subagent - Delegates all worktree setup
- **brainstorming** skill (Phase 4) - REQUIRED when implementation follows design approval
- Any workflow needing isolated workspace

### Pairs With

- **finishing-a-development-branch** skill - REQUIRED for cleanup after work complete
- **executing-plans** or **subagent-driven-development** - Work happens in this worktree

## Worktree Cleanup

**After work complete**, use `finishing-a-development-branch` skill or manual cleanup:

```bash
# 1. Return to main worktree
cd /path/to/main/worktree

# 2. Remove branch worktree
git worktree remove .worktrees/feature-auth

# 3. Delete branch if merged
git branch -d feature/auth

# 4. Verify cleanup
git worktree list
```

## Red Flags

**Never:**
- Create worktree without .gitignore verification (project-local)
- Skip baseline test verification
- Proceed with failing tests without asking
- Assume directory location when ambiguous
- Skip CLAUDE.md check

**Always:**
- Follow directory priority: existing > CLAUDE.md > ask
- Verify .gitignore for project-local
- Auto-detect and run project setup
- Verify clean test baseline
- Announce skill usage at start

## Navigation Map

**For git operations**:
- Commit preparation → `.claude/agents/git-operations/`
- Pull request creation → `.claude/agents/git-operations/`
- General git workflow → `git --help`

**For worktree management**:
- Create worktree → This skill
- Remove worktree → `git worktree remove` or `finishing-a-development-branch` skill
- List worktrees → `git worktree list`

**For project setup**:
- Python projects → `pip install -r requirements.txt` or `poetry install`
- Node.js → `npm install` or `yarn install`
- Rust → `cargo build`
- Go → `go mod download`
