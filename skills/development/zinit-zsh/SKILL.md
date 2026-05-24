---
name: zinit-zsh
description: Zinit zsh plugin manager configuration and binary installs. This skill should be used when adding zsh plugins, installing CLI tools via gh-r releases, configuring completions, managing turbo/wait loading, using ice modifiers (sbin, atclone, atpull, as, from), troubleshooting plugin load order, working with OMZ snippets, or modifying .zshrc and ~/.config/zsh/ files in this stow-managed dotfiles repo.
version: 1.0.0
last_updated: 2026-01-23
zinit_version: "zdharma-continuum"
---

# Zinit ZSH Plugin Manager

Manage zsh plugins, CLI binary installs, and completions using zinit in this dotfiles repo.

## Repo Structure

This repo uses GNU Stow. Files symlink to `$HOME`:
- `.zshrc` - main zinit config, plugin definitions, binary installs
- `.config/zsh/` - modular zsh configs loaded via `zinit snippet`
  - `plugins.zsh` - additional plugin loads
  - `aliases.zsh` - shell aliases
  - `exports.zsh` - PATH and env vars
  - `completions.zsh` - completion setup
  - `completions/` - custom completion files (_just, _inv, etc.)
  - `history.zsh`, `keys.zsh`, `styles.zsh` - other configs

## Quick Reference

### Binary Install Pattern (gh-r)

```zsh
zinit as"null" wait lucid from"gh-r" for \
    sbin"binary-name"  owner/repo
```

### With Completion Generation

```zsh
zinit for \
    from'gh-r' \
    sbin'tool' \
    atclone'./tool completion zsh > _tool' atpull'%atclone' as'completion' \
  @owner/repo
```

### OMZ Plugin/Snippet

```zsh
zinit wait lucid for \
    OMZP::plugin-name \
    OMZL::lib-file.zsh
```

### Build from Source

```zsh
zinit for \
    as'null' \
    configure'--prefix=$PWD' \
    make'install' \
    sbin \
  @owner/repo
```

## Key Ice Modifiers

| Ice | Purpose |
|-----|---------|
| `from'gh-r'` | Download from GitHub releases |
| `sbin'pattern -> name'` | Create bin symlink in $ZPFX/bin |
| `wait"N"` | Turbo load after N seconds |
| `lucid` | Suppress "Loaded..." message |
| `atclone"cmd"` | Run on clone |
| `atpull'%atclone'` | Run atclone on update |
| `as'completion'` | Register as completion |
| `as'null'` | Don't source as plugin |

## Detailed References

For comprehensive patterns and troubleshooting, see:
- `references/ice-modifiers.md` - all ice options with examples
- `references/patterns.md` - common install patterns
- `references/troubleshooting.md` - load order, debugging
