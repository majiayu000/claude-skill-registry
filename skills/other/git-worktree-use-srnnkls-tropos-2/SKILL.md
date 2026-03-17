---
name: git-worktree-use
description: Create isolated git worktrees with safety verification. Use when starting feature work needing isolation or before executing plans - systematic directory selection and baseline verification.
---

# Using Git Worktrees

Git worktrees create isolated workspaces sharing the same repository.

**Core principle:** Systematic directory selection + safety verification = reliable isolation.

---

## When to Use

**Use for:**
- Feature work needing isolation from current workspace
- Parallel work on multiple branches
- Before executing implementation plans

**Don't use for:**
- Quick fixes on current branch
- Single-file changes
- When isolation isn't needed

---

## Directory Selection Process

Follow this priority order:

### 1. Check Existing Directories

```bash
ls -d .worktrees 2>/dev/null     # Preferred (hidden)
ls -d worktrees 2>/dev/null      # Alternative
```

**If found:** Use that directory. If both exist, `.worktrees` wins.

### 2. Check Project Config

Look for worktree directory preference in project documentation (CLAUDE.md, README, etc.).

**If preference specified:** Use it without asking.

### 3. Ask User

If no directory exists and no preference found:

```
No worktree directory found. Where should I create worktrees?

1. .worktrees/ (project-local, hidden)
2. ~/worktrees/<project-name>/ (global location)

Which would you prefer?
```

---

## Safety Verification

### For Project-Local Directories

**MUST verify .gitignore before creating worktree:**

```bash
grep -q "^\.worktrees/$" .gitignore || grep -q "^worktrees/$" .gitignore
```

**If NOT in .gitignore:**
1. Add appropriate line to .gitignore
2. Commit the change
3. Proceed with worktree creation

**Why critical:** Prevents accidentally committing worktree contents.

### For Global Directory

No .gitignore verification needed - outside project entirely.

---

## Creation Steps

### 1. Detect Project Name

```bash
project=$(basename "$(git rev-parse --show-toplevel)")
```

### 2. Create Worktree

```bash
git worktree add "$path" -b "$BRANCH_NAME"
cd "$path"
```

### 3. Run Project Setup

Auto-detect and run appropriate setup:

```bash
# Detect project type and install dependencies
if [ -f package.json ]; then npm install; fi
if [ -f Cargo.toml ]; then cargo build; fi
if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
if [ -f pyproject.toml ]; then pip install -e .; fi
if [ -f go.mod ]; then go mod download; fi
```

### 4. Verify Clean Baseline

Run tests to ensure worktree starts clean:

```bash
# Use project-appropriate command
npm test / cargo test / pytest / go test ./...
```

**If tests fail:** Report failures, ask whether to proceed or investigate.

**If tests pass:** Report ready.

### 5. Report Location

```
Worktree ready at <full-path>
Tests passing (<N> tests, 0 failures)
Ready to implement <feature-name>
```

---

## Quick Reference

| Situation | Action |
|-----------|--------|
| `.worktrees/` exists | Use it (verify .gitignore) |
| `worktrees/` exists | Use it (verify .gitignore) |
| Both exist | Use `.worktrees/` |
| Neither exists | Check config then ask user |
| Not in .gitignore | Add it immediately + commit |
| Tests fail | Report failures + ask |

---

## Red Flags

**Never:**
- Create worktree without .gitignore verification (project-local)
- Skip baseline test verification
- Proceed with failing tests without asking
- Assume directory location when ambiguous

**Always:**
- Follow directory priority: existing > config > ask
- Verify .gitignore for project-local
- Auto-detect and run project setup
- Verify clean test baseline

---

## Integration

**Use with:**
- `brainstorm` - After design approval, set up workspace
- `task-dispatch` - Work happens in this worktree
- `completion-verify` - Verify baseline before and after
