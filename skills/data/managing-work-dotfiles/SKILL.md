---
name: managing-work-dotfiles
description: Use this skill when working with work-specific dotfiles managed by yadm-work. This includes pulling remote changes, committing and pushing work dotfile changes, modifying work configuration files, viewing tracked work files, resolving merge conflicts, and maintaining the work dotfiles repository at Spotify GHE. Triggers on "work dotfiles", "yadm-work", "spotify dotfiles", or work-related config management.
---

# Managing Work Dotfiles

This skill manages work-specific dotfiles using a separate git bare repo, keeping them isolated from personal dotfiles.

## Repository Info

- **Remote**: `git@ghe.spotify.net:thopper/dotfiles.git`
- **Work tree**: `$HOME`
- **Git directory**: `~/.local/share/yadm-work/repo.git`
- **Function**: `yadm-work` (defined in `~/.config/fish/fish-work.fish`)

## Key Principle: Use yadm-work

The `yadm-work` function wraps git with the correct directories:

```bash
yadm-work status
yadm-work add <file>
yadm-work commit -m "message"
yadm-work push
```

This is equivalent to:
```bash
git --git-dir="$HOME/.local/share/yadm-work/repo.git" --work-tree="$HOME" <command>
```

## Initial Setup

If not yet initialized on a new machine:

```bash
# Create the directory
mkdir -p ~/.local/share/yadm-work

# Clone as bare repo
git clone --bare git@ghe.spotify.net:thopper/dotfiles.git ~/.local/share/yadm-work/repo.git

# Checkout files to home directory
yadm-work checkout
```

## Getting Current State

```bash
yadm-work status          # Show modified/staged files
yadm-work ls-files        # List all tracked work files
yadm-work diff            # Show unstaged changes
yadm-work remote -v       # Verify remote is Spotify GHE
```

## Core Operations

### Pull from Remote

```bash
yadm-work pull
```

If merge conflicts occur:
1. Run `yadm-work status` to see conflicted files
2. Edit files to resolve conflicts
3. Stage resolved files: `yadm-work add <file>`
4. Complete the merge: `yadm-work commit`

### Commit and Push Changes

```bash
yadm-work add <file>           # Stage specific file
yadm-work add -u               # Stage all modified tracked files
yadm-work commit -m "message"  # Commit with message
yadm-work push                 # Push to Spotify GHE
```

### Modify Configuration Files

1. Find the relevant file: `yadm-work ls-files | grep -i <pattern>`
2. Read and understand the current config
3. Make the requested changes
4. Stage, commit, and push:
   ```bash
   yadm-work add <modified-file>
   yadm-work commit -m "Update <config> to <what was changed>"
   yadm-work push
   ```

## Adding/Removing Files

### Add a new file to tracking

```bash
yadm-work add <new-file>
yadm-work commit -m "Add <file> to work dotfiles"
yadm-work push
```

**Important**: When adding new files under `~/.claude/`, also update `~/.claude/README.md` to document them:

```bash
# After adding new .claude files, update the README
yadm-work add ~/.claude/README.md
yadm-work commit -m "Update README with new <item>"
yadm-work push
```

### Stop tracking a file (without deleting it)

```bash
yadm-work rm --cached <file>
yadm-work commit -m "Stop tracking <file>"
yadm-work push
```

## Avoiding Conflicts with Personal Dotfiles

**Critical**: Never track the same file in both personal (`yadm`) and work (`yadm-work`) repos.

Check before adding:
```bash
# Check if file is in personal dotfiles
yadm ls-files | grep <filename>

# Check if file is in work dotfiles
yadm-work ls-files | grep <filename>
```

## Currently Tracked Files

```
~/.claude/README.md
~/.claude/skills/add-knowledge/
~/.claude/skills/investigating-pagerduty-incidents/
~/.claude/skills/managing-work-dotfiles/
~/.claude/skills/monitor-deploy/
```

## Useful Commands

```bash
yadm-work log --oneline -10    # Recent commits
yadm-work show HEAD            # Last commit details
yadm-work stash                # Stash changes temporarily
yadm-work stash pop            # Restore stashed changes
```
