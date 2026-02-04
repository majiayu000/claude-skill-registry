---
name: managing-dotfiles
description: Use this skill when working with personal dotfiles managed by yadm. This includes pulling remote changes, committing and pushing dotfile changes, modifying configuration files (shell, editor, terminal, git, etc.), viewing tracked files, resolving merge conflicts, and maintaining the dotfiles repository. For work dotfiles, use the managing-work-dotfiles skill instead.
---

# Managing Personal Dotfiles with Yadm

This skill manages **personal** dotfiles using [yadm](https://yadm.io/) (Yet Another Dotfiles Manager).

> **Note**: For work-specific dotfiles (Spotify GHE), use the `managing-work-dotfiles` skill with `yadm-work` commands.

## Repository Info

- **Remote**: Your dotfiles git repository
- **Work tree**: `$HOME`
- **Yadm repo**: `~/.local/share/yadm/repo.git`

## Getting Current State

Always start by checking the current state:

```bash
yadm status          # Show modified/staged files
yadm ls-files        # List all tracked files
yadm diff            # Show unstaged changes
```

## Managed Files Reference

Run `yadm ls-files` to get the authoritative list. Common categories:

| Category | Files |
|----------|-------|
| **Shell** | `.config/fish/` (config.fish, aliases, env, functions, keybindings, plugins) |
| **Editor** | `.vimrc`, `Library/Application Support/Code/User/` (settings.json, keybindings.json) |
| **Terminal** | `.tmux.conf`, `.config/ghostty/config`, `.config/starship.toml` |
| **Git** | `.gitconfig`, `.gitignore`, `.gitmodules` |
| **Claude** | `.claude/skills/` (commit, creating-pull-requests, managing-dotfiles) |
| **Yadm** | `.config/yadm/` (bootstrap, hooks, README, install-hooks.sh) |
| **Other** | `.config/bat/config`, `.config/ruff/pyproject.toml`, `.duti`, `.hushlogin`, `Caddyfile` |

## Core Operations

### Pull from Remote

```bash
yadm pull
```

If merge conflicts occur:
1. Run `yadm status` to see conflicted files
2. Edit files to resolve conflicts (remove conflict markers)
3. Stage resolved files: `yadm add <file>`
4. Complete the merge: `yadm commit`

### Commit and Push Changes

```bash
yadm add <file>           # Stage specific file
yadm add -u               # Stage all modified tracked files
yadm commit -m "message"  # Commit with message
yadm push                 # Push to remote
```

**Commit conventions** (from commit skill):
- No AI/Claude attribution
- No Co-Authored-By headers

### Modify Configuration Files

When asked to modify a config (e.g., "update tmux to do X"):

1. Find the relevant file: `yadm ls-files | grep -i tmux`
2. Read and understand the current config
3. Make the requested changes
4. Stage, commit, and push:
   ```bash
   yadm add <modified-file>
   yadm commit -m "Update <config> to <what was changed>"
   yadm push
   ```

## Adding/Removing Files

### Add a new file to tracking

```bash
yadm add <new-file>
yadm commit -m "Add <file> to dotfiles"
yadm push
```

### Stop tracking a file (without deleting it)

```bash
yadm rm --cached <file>
yadm commit -m "Stop tracking <file>"
yadm push
```

## Pre-commit Hooks

Pre-commit is configured via `~/.pre-commit-config.yaml`. Hooks check for:
- Private keys and secrets
- Large files (>500KB)
- Trailing whitespace
- Merge conflicts

Run manually:
```bash
yadm enter pre-commit run --all-files
```

If a commit fails due to pre-commit fixes, stage the fixes and retry.

## Self-Management

This skill is itself tracked by yadm at `~/.claude/skills/managing-dotfiles/`.

When updating this skill:
1. Make changes to the skill files
2. Commit with yadm:
   ```bash
   yadm add ~/.claude/skills/managing-dotfiles/
   yadm commit -m "Update managing-dotfiles skill"
   yadm push
   ```

When files are added/removed from yadm tracking, update the "Managed Files Reference" section above if the categories change significantly.

## Useful Commands

See `yadm-command-reference.md` for a quick reference of common yadm commands.

## Bootstrap (New System Setup)

On a new system after cloning:
```bash
yadm bootstrap
```

This runs `~/.config/yadm/bootstrap` which installs Homebrew, uv, vim-plug, and other dependencies.
