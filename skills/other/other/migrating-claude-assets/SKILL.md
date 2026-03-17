---
name: migrating-claude-assets
description: Migrates Claude Code skills and commands from dotfiles to home-manager in this workstation repo. Use when adding or moving skills/commands to be managed by Nix.
---

# Migrating Claude Assets to Home-Manager

## Overview

This repo manages Claude Code skills and commands via home-manager. Source files live in `assets/claude/`, deployed to `~/.claude/` via symlinks.

## File Locations

| Type | Source | Deployed to |
|------|--------|-------------|
| Commands | `assets/claude/commands/<name>.md` | `~/.claude/commands/<name>.md` |
| Skills | `assets/claude/skills/<name>/SKILL.md` | `~/.claude/skills/<name>/SKILL.md` |
| References | `assets/claude/skills/<name>/references/*.md` | `~/.claude/skills/<name>/references/*.md` |

## Migration Steps

### 1. Copy files to assets

```bash
# For a command
cp ~/.claude/commands/my-command.md assets/claude/commands/

# For a skill (may have references/)
cp -r ~/.claude/skills/my-skill assets/claude/skills/
```

### 2. Add home.file entries

Edit `users/dev/home.base.nix`, add entries after existing ones (~line 166):

```nix
# For a command
home.file.".claude/commands/my-command.md".source = "${assetsPath}/claude/commands/my-command.md";

# For a skill
home.file.".claude/skills/my-skill/SKILL.md".source = "${assetsPath}/claude/skills/my-skill/SKILL.md";

# For each reference file (if any)
home.file.".claude/skills/my-skill/references/FOO.md".source = "${assetsPath}/claude/skills/my-skill/references/FOO.md";
```

### 3. Remove existing files (before applying)

Home-manager can't overwrite regular files with symlinks:

```bash
# On macOS
rm ~/.claude/commands/my-command.md
# or
rm -rf ~/.claude/skills/my-skill

# On devbox (if existed there too)
rm -rf ~/.claude/skills/my-skill
```

### 4. Commit and push

```bash
git add assets/claude/ users/dev/home.base.nix
git commit -m "Migrate my-skill to home-manager"
git push origin main
```

### 5. Apply

**macOS:**
```bash
sudo darwin-rebuild switch --flake ~/Code/workstation#Y0FMQX93RR-2
```

**Devbox:**
```bash
cd ~/projects/workstation && git pull
nix run home-manager -- switch --flake .#dev
```

## Notes

- Each file needs explicit `home.file` entry (not recursive)
- Skills deploy to both macOS and devbox via shared `home.base.nix`
- Skill frontmatter: needs `name:` and `description:` fields
- Command frontmatter: needs `description:` field
