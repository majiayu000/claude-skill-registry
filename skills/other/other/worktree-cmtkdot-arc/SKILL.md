---
name: worktree
description: Use when executing beads in isolated git worktrees. Defines worktree lifecycle, naming conventions, safety verification, and merge-back strategy for parallel execution.
invocation: agent
---

# Worktree

Git worktree isolation for bead execution. Each worker gets a dedicated worktree on a dedicated branch, sharing the same `.git` object store. Eliminates file conflicts between parallel workers without serialization overhead.

## Directory Selection

The resolved directory is the **worktree root** (`<worktree-root>`). All lifecycle commands use this path. It can be project-local or external.

Follow this priority order:

### 1. Check Existing Directories

```bash
# Project-local
ls -d .worktrees 2>/dev/null     # Hidden, inside repo
ls -d worktrees 2>/dev/null      # Visible, inside repo

# External (sibling to repo)
project="$(basename "$(git rev-parse --show-toplevel)")"
ls -d "../${project}.worktrees" 2>/dev/null
```

If found, use that directory. Priority: `.worktrees` > `worktrees` > external sibling.

### 2. Check CLAUDE.md

```bash
grep -i "worktree.*director\|worktree.*root" CLAUDE.md 2>/dev/null
```

If a preference is specified (e.g., `../project.worktrees/`), use it without asking.

### 3. Check `.arc/config.json`

If `worktree_root` is set in `.arc/config.json`, use that path:

```bash
jq -r '.worktree_root // empty' .arc/config.json 2>/dev/null
```

### 4. Ask User

If no directory exists and no preference is configured:

```
No worktree directory found. Where should I create worktrees?

1. ../$(basename $(pwd)).worktrees/ (sibling to repo, outside git) (Recommended)
2. .worktrees/ (project-local, hidden)
```

Store the chosen path in `.arc/config.json` as `worktree_root` so subsequent runs reuse it.

## Safety Verification

### Project-local directories (`.worktrees/`, `worktrees/`)

Must verify the directory is git-ignored before creating worktrees:

```bash
git check-ignore -q .worktrees 2>/dev/null
```

If NOT ignored, fix immediately:

1. Add `.worktrees/` to `.gitignore`
2. Commit the change
3. Proceed with worktree creation

### External directories (`../project.worktrees/`, etc.)

No `.gitignore` verification needed — the directory is outside the repository.

## Naming Conventions

- **Branches**: `arc/<bead-id>` (e.g., `arc/PROJ-42`)
- **Directories**: `<worktree-root>/<bead-id>/` (e.g., `../myproject.worktrees/PROJ-42/` or `.worktrees/PROJ-42/`)

## Baseline Branch

The baseline branch is the starting point for all worktree branches.

- Configured via `.arc/config.json` field `worktree_baseline`
- Defaults to `"main"` if unset; can be overridden at execution time (e.g., `develop` for gitflow projects)
- All worktree branches are created from this baseline

## Worktree Lifecycle

Tied to bead execution phases:

### Create (Before Bead Execution)

```bash
git worktree add -b arc/<bead-id> <worktree-root>/<bead-id> <baseline>
```

### Use (During Bead Execution)

The worker operates entirely within the worktree directory. All file reads, edits, and verification commands resolve relative to the worktree root.

### Merge Back (After Bead Verification Passes)

After a bead's verification passes, merge the worktree branch into the baseline:

```bash
cd <project-root>
git merge --no-ff arc/<bead-id> -m "feat(<bead-id>): <bead objective summary>"
```

Merge-back happens sequentially in dependency order. If a merge conflict occurs, pause and surface to the lead/user — do not auto-resolve.

### Cleanup (After Merge)

```bash
git worktree remove <worktree-root>/<bead-id>
git branch -d arc/<bead-id>
```

After all beads close, prune stale worktrees:

```bash
git worktree prune
```

## Project Setup

On first worktree creation, auto-detect and run setup if dependencies are not already present:

```bash
# Node.js (skip if node_modules exists)
if [ -f package.json ] && [ ! -d node_modules ]; then npm install; fi

# Rust (skip if target exists)
if [ -f Cargo.toml ] && [ ! -d target ]; then cargo build; fi

# Python
if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
if [ -f pyproject.toml ]; then poetry install; fi

# Go
if [ -f go.mod ]; then go mod download; fi
```

Skip setup entirely if the shared structure already provides dependencies (e.g., `node_modules` symlinked or present).

## Merge Strategy

1. Merge-back in dependency order — beads whose dependents are waiting merge first.
2. TDD ordering: test branches merge before implementation branches.
3. Use `--no-ff` to preserve bead-scoped history in the merge graph.
4. If a merge conflict occurs during merge-back, mark the bead as `blocked` and surface to the lead/user.
5. Never force-merge or auto-resolve conflicts.

## Relationship to Superpowers

This skill replaces the need for the superpowers `using-git-worktrees` skill within Arc workflows. It follows the same directory selection and safety verification patterns but adds bead-aware lifecycle management including naming conventions, baseline tracking, dependency-ordered merge-back, and post-execution cleanup.

## Script Reference

Arc provides executable scripts for worktree lifecycle management. Agents and execution modes should use these scripts instead of running raw git commands:

- **Create**: `${CLAUDE_PLUGIN_ROOT}/scripts/worktree-create.sh [target-path] [branch-name] [options]`
  - Handles branch normalization, `.beads/redirect` setup, local config sync, dependency install
  - Reads baseline and worktree root from `.arc/config.json`
  - Run with `--help` for full options

- **Cleanup**: `${CLAUDE_PLUGIN_ROOT}/scripts/worktree-cleanup.sh <target> | --list | --prune`
  - Refuses to remove protected branches (main, master, develop, release/*, hotfix/*)
  - Checks for uncommitted changes and unpushed commits before removal
  - Run with `--help` for full options

- **Config sync**: `${CLAUDE_PLUGIN_ROOT}/scripts/worktree-sync-local.sh <target> [options]`
  - Manifest-driven sync of machine-local files (`.env`, keys, etc.)
  - Default manifest: `.arc/worktree-local.txt`

Scripts auto-resolve the worktree root, baseline branch, and beads redirect from `.arc/config.json` and project conventions.

## Related Skills

- `swarm` and `team` use this skill for parallel worker isolation when `--worktree` is enabled.
- `git-workflow` defines the safety rails that apply to worktree operations.
- `beads-schema` defines the bead structure that drives worktree naming and lifecycle.
