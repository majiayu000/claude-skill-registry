---
name: using-git-worktrees
description: Use when starting feature work that needs isolation from current workspace or before executing implementation plans - creates isolated git worktrees with smart directory selection and safety verification
---

# Using Git Worktrees

**Announce at start:** "I'm using the using-git-worktrees skill to set up an isolated workspace."

## Directory Selection (Priority Order)

### 1. Check Existing Directories
```bash
ls -d .worktrees 2>/dev/null     # Preferred (hidden)
ls -d worktrees 2>/dev/null      # Alternative
```
If both exist, `.worktrees` wins.

### 2. Check CLAUDE.md
```bash
grep -i "worktree.*director" CLAUDE.md 2>/dev/null
```
If preference specified, use it.

### 3. Ask User
```
No worktree directory found. Where should I create worktrees?
1. .worktrees/ (project-local, hidden)
2. ~/.config/superpowers/worktrees/<project-name>/ (global)
```

## Safety Verification

**For project-local directories: MUST verify ignored before creating.**

```bash
git check-ignore -q .worktrees 2>/dev/null
```

**If NOT ignored:** Add to .gitignore, commit, then proceed.

**For global directory (~/.config/superpowers/worktrees):** No verification needed.

## Creation Steps

```bash
# 1. Detect project
project=$(basename "$(git rev-parse --show-toplevel)")

# 2. Create worktree
git worktree add "$path" -b "$BRANCH_NAME"
cd "$path"

# 3. Auto-detect and run setup
[ -f package.json ] && npm install
[ -f Cargo.toml ] && cargo build
[ -f requirements.txt ] && pip install -r requirements.txt
[ -f pyproject.toml ] && poetry install
[ -f go.mod ] && go mod download

# 4. Verify clean baseline
# Run project-appropriate test command
# If tests fail: report failures, ask whether to proceed

# 5. Report
# "Worktree ready at <path>, tests passing (N tests, 0 failures)"
```

## Quick Reference

| Situation | Action |
|-----------|--------|
| `.worktrees/` exists | Use it (verify ignored) |
| `worktrees/` exists | Use it (verify ignored) |
| Both exist | Use `.worktrees/` |
| Neither exists | Check CLAUDE.md, then ask user |
| Directory not ignored | Add to .gitignore + commit |
| Tests fail in baseline | Report failures + ask |

## Integration

- **Called by:** brainstorming (after design approved), any skill needing isolation
- **Pairs with:** finishing-a-development-branch (cleanup after), executing-plans / subagent-driven-development (work happens here)
