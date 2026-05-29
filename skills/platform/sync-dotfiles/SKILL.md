---
name: sync-dotfiles
description: Use when user asks to sync, update, or install dotfiles, or when setting up a new machine
---

# Sync Dotfiles

Syncs dotfiles from `~/projects/jasonkuhrt/dotfiles` to the system.

## Command

```bash
~/projects/jasonkuhrt/dotfiles/sync
```

**Options:**
- `-v, --verbose` - Show full output
- `--migrate` - Run pending migrations after sync
- `--migrate-only` - Only run migrations, skip sync

## Important

**Claude Code cannot run this directly** - the script requires sudo for:
- Homebrew casks
- Touch ID for sudo setup
- Changing default shell
- Power management settings

**Instruct the user to run it manually** in their terminal.

## What It Does

- Symlinks config files (fish, git, zed, nvim, ssh, etc.)
- Installs Homebrew packages from Brewfile
- Sets up Node.js via pnpm
- Configures macOS defaults (keyboard, Finder, Dock)
- Installs Fisher plugins for fish shell
- Installs npm global packages
