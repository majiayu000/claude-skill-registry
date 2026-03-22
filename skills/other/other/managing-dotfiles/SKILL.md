---
name: managing-dotfiles
description: Manage dotfiles tracked in ~/.claude/dotfiles/ using GNU Stow. Use when adding config files to dotfiles, stowing/unstowing packages, or troubleshooting symlink conflicts.
---

# Dotfiles Management with GNU Stow

Manage dotfiles tracked in `~/.claude/dotfiles/` using GNU Stow — a symlink farm manager that mirrors directory structure from a source package into `$HOME`.

## Directory Convention

Each package under `dotfiles/` mirrors the home directory structure:

```text
dotfiles/
├── tmux/.config/tmux/tmux.conf    →  ~/.config/tmux/tmux.conf
├── git/.gitconfig                 →  ~/.gitconfig
├── nvim/.config/nvim/init.lua     →  ~/.config/nvim/init.lua
└── zsh/.zshrc                     →  ~/.zshrc
```

The package name (e.g. `tmux`, `git`) is just an organizational label. The internal directory structure determines where symlinks land.

## Adding a New Package

Three steps:

```bash
# 1. Create the package directory mirroring $HOME structure
mkdir -p ~/.claude/dotfiles/<pkg>/<path-relative-to-home>

# 2. Move the existing config into the package
mv ~/<path-to-config> ~/.claude/dotfiles/<pkg>/<path-relative-to-home>/

# 3. Stow to create the symlink
stow -d ~/.claude/dotfiles -t ~ <pkg>
```

Example — adding starship config:

```bash
mkdir -p ~/.claude/dotfiles/starship/.config
mv ~/.config/starship.toml ~/.claude/dotfiles/starship/.config/starship.toml
stow -d ~/.claude/dotfiles -t ~ starship
```

## Common Commands

```bash
# Stow a package (create symlinks)
stow -d ~/.claude/dotfiles -t ~ <pkg>

# Unstow a package (remove symlinks)
stow -d ~/.claude/dotfiles -t ~ -D <pkg>

# Re-stow (unstow + stow, useful after restructuring)
stow -d ~/.claude/dotfiles -t ~ -R <pkg>

# Dry run (see what would happen without doing it)
stow -d ~/.claude/dotfiles -t ~ -n -v <pkg>

# Stow all packages at once
make dotfiles
```

## Installing Stow

```bash
# macOS
brew install stow

# Debian/Ubuntu
apt install stow

# Fedora/RHEL
dnf install stow
```

## Troubleshooting

### Conflict: existing target is not a symlink

Stow won't overwrite real files. Use `--adopt` to pull the existing file into the package, then stow:

```bash
stow -d ~/.claude/dotfiles -t ~ --adopt <pkg>
```

**Warning**: `--adopt` replaces the package file with the existing target file. If your package version is newer, back it up first or use `git diff` after adopting.

### Conflict: target is a symlink managed by another package

Two stow packages can't own the same target path. Check which package owns it:

```bash
ls -la <conflicting-path>
```

Then decide which package should own the file and remove the duplicate.

### Stow created a directory symlink instead of file symlinks

Stow uses "tree folding" — if a package is the only owner of a directory, it symlinks the directory itself rather than individual files. This is usually fine. If you need file-level symlinks (e.g., because the directory has other non-stowed files), use `--no-folding`:

```bash
stow -d ~/.claude/dotfiles -t ~ --no-folding <pkg>
```
