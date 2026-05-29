---
name: dotfiles-commit
description: Instructions for committing changes to config files in the home directory using the dotfiles bare git repo.
---

# Committing Dotfiles Changes

This user manages config files in their home directory using a bare git repository. Use the `dotfiles` alias instead of regular `git` commands.

## The Dotfiles Alias

```bash
dotfiles='git --git-dir=$HOME/.dotfiles --work-tree=$HOME'
```

This alias points to a bare git repo at `~/.dotfiles` with the work tree set to `$HOME`.

## Workflow for Committing Changes

### 1. Check Status

```bash
dotfiles status
```

This shows modified, staged, and untracked config files.

### 2. View Changes

```bash
dotfiles diff <file>
```

Review what changed before committing.

### 3. Stage Files

```bash
dotfiles add <file>
```

Only stage the specific config file(s) being committed.

### 4. Commit

```bash
dotfiles commit -m "Short descriptive message"
```

### 5. Push (if requested)

```bash
dotfiles push
```

Only push when explicitly asked.

## Commit Message Style

Based on existing commits, use short descriptive messages:
- `nvim: Set default tab size to 2 spaces`
- `Improve shell, git, tmux, and ssh configs`
- `Add shell, git, ssh, and tool configs`

Prefix with the tool/config name when the change is specific to one tool.

## Important Notes

- Always use `dotfiles` instead of `git` for home directory config files
- The repo tracks files across `$HOME`, so be careful what you add
- Check `dotfiles status` to see what files are tracked/modified
- Don't add sensitive files (credentials, tokens, etc.)
