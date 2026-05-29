---
name: worktrees
description: Use when starting feature work that needs isolation from current workspace or before executing implementation plans - creates isolated git worktrees with beads integration via bd worktree commands
---

# Git Worktrees

Git worktrees create isolated workspaces sharing the same repository, allowing work on multiple branches simultaneously without switching.

**Primary tool:** `bd worktree` — handles git worktree + beads integration automatically.

---

## When to Use

- Parallel subagents need filesystem isolation
- Feature work that shouldn't affect current workspace
- Separate builds/servers running simultaneously
- Before executing implementation plans

---

## Setup: Ensure .worktrees/ is Ignored

**Before creating any worktrees**, ensure `.worktrees/` is in `.gitignore`. This is a one-time setup that covers all future worktrees:

```bash
# Check if .worktrees/ is already ignored
git check-ignore -q .worktrees/ || echo '.worktrees/' >> .gitignore
```

If you added the line, commit it:
```bash
git add .gitignore && git commit -m "Ignore .worktrees/ directory"
```

**Why this matters:** Without this, beads adds each worktree individually to `.gitignore`, creating noise. With `.worktrees/` ignored, all worktrees underneath are automatically covered.

---

## Creating a Worktree

**All worktrees go under `.worktrees/` in the repo root.** This is the standard location.

```bash
bd worktree create .worktrees/feature-auth
```

**What it does automatically:**
1. Creates git worktree at the specified path
2. Sets up `.beads/redirect` pointing to main repo's database
3. Creates the branch (same name as the directory by default)

**With custom branch name:**
```bash
bd worktree create .worktrees/bugfix --branch fix-123
```

---

## After Creation

### 1. Enter Worktree

```bash
cd .worktrees/feature-auth
```

### 2. Run Project Setup

```bash
# Node.js
[ -f package.json ] && npm install

# Rust
[ -f Cargo.toml ] && cargo build

# Go
[ -f go.mod ] && go mod download
```

### 3. Verify Baseline

```bash
npm test  # or cargo test, go test ./...
```

**If tests fail:** Report failures, ask whether to proceed.

### 4. Verify Beads Shared

```bash
bd ready  # Should show same beads as main workspace
```

---

## Listing Worktrees

```bash
bd worktree list
```

Or standard git:
```bash
git worktree list
```

---

## Removing a Worktree

Use `bd worktree remove` — includes safety checks:

```bash
bd worktree remove feature-auth
```

**Safety checks (automatic):**
- Uncommitted changes
- Unpushed commits
- Stashes

**Skip checks (not recommended):**
```bash
bd worktree remove feature-auth --force
```

---

## Worktree Info

Check current worktree status:

```bash
bd worktree info
```

---

## Quick Reference

| Task | Command |
|------|---------|
| Ensure .worktrees/ ignored | `git check-ignore -q .worktrees/ \|\| echo '.worktrees/' >> .gitignore` |
| Create worktree | `bd worktree create .worktrees/<name>` |
| Create with branch | `bd worktree create .worktrees/<name> --branch <branch>` |
| List worktrees | `bd worktree list` |
| Remove worktree | `bd worktree remove .worktrees/<name>` |
| Check status | `bd worktree info` |
| Verify beads sync | `bd ready` (in worktree) |

---

## Why bd worktree?

| Manual git worktree | bd worktree |
|---------------------|-------------|
| Separate commands for git + beads | Single command |
| No beads redirect setup | Automatic redirect to main DB |
| No safety checks on remove | Checks for uncommitted/unpushed |

---

## Example Workflow

```bash
# One-time: ensure .worktrees/ is ignored
git check-ignore -q .worktrees/ || echo '.worktrees/' >> .gitignore

# Create isolated workspace
bd worktree create .worktrees/feature-auth

# Enter and setup
cd .worktrees/feature-auth
npm install
npm test  # ✓ 47 passing

# Verify beads shared
bd ready  # Shows same issues as main

# Work on feature...
bd claim auth-001

# When done
cd ../..
bd worktree remove .worktrees/feature-auth
```

---

## Known Limitations

### Daemon Mode

Daemon mode does not work correctly with user-created git worktrees. Worktrees share the same `.git` directory and beads database, but the daemon doesn't track which branch each worktree has checked out.

**Solution**: Use direct mode in worktrees:
```bash
bd --no-daemon <command>
# Or set environment variable
export BEADS_NO_DAEMON=1
```

### Two Types of Worktrees

Don't confuse these:

| Type | Location | Purpose |
|------|----------|---------|
| User worktrees | `.worktrees/<name>` | Parallel feature work (you create these) |
| Beads internal | `.git/beads-worktrees/beads-sync` | Sync-branch commits (beads creates this) |

The internal worktree is hidden and managed by beads for the sync-branch feature. Don't manually modify it.

### SKIP_WORKTREE Issues

If `git status` doesn't show changes to `.beads/*.jsonl` files, check for SKIP_WORKTREE flags:

```bash
git ls-files -v .beads/
# 'h' prefix = SKIP_WORKTREE set (changes hidden)
# 'H' prefix = normal tracking
```

**Fix**: Remove and re-add the files:
```bash
git rm --cached .beads/issues.jsonl
git add .beads/issues.jsonl
```

Or run `bd sync` which sets the correct index flags.

---

## Fallback (No Beads)

If beads isn't installed, use manual git worktree:

```bash
# Verify ignored
git check-ignore -q .worktrees/ || echo '.worktrees/' >> .gitignore

# Create
git worktree add .worktrees/feature-auth -b feature-auth

# Remove
git worktree remove .worktrees/feature-auth
```

But you lose: automatic gitignore, beads sync, and safety checks.
