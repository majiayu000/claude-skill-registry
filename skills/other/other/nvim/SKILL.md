---
name: nvim
description: "Use when troubleshooting Neovim/LazyVim plugin errors, updating plugins after breaking changes, or diagnosing colorscheme/startup issues."
argument-hint: "[debug | update | fix <plugin>]"
context: default
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash(nvim --version:*)
  - Bash(nvim --headless:*)
  - Bash(tmux new-session -d -s nvim-debug:*)
  - Bash(tmux kill-session -t nvim-debug:*)
  - Bash(tmux capture-pane -t nvim-debug:*)
  - Bash(ls:*)
  - Bash(cat /tmp/nvim-debug*:*)
  - Bash(git -C ~/.local/share/nvim/lazy:*)
  - Bash(chezmoi diff:*)
  - Bash(chezmoi status:*)
  - Bash(sleep:*)
  # Requires user approval:
  # - Edit/Write (config changes)
  # - chezmoi apply (deploys to destination)
  # - git add/commit (version control)
  # - rm cache, cp lockfile (destructive/overwrite)
---

# Neovim/LazyVim Troubleshooting & Updates

## Arguments

```
$ARGUMENTS
```

## Reference

LazyVim docs: `docs/reference/lazyvim-github-io.txt`. If missing, run `/gitingest https://github.com/LazyVim/lazyvim.github.io docs/**.md` first.

## Key Paths

| What | Source (edit here) | Installed (read-only) |
|------|-------------------|----------------------|
| Plugin specs | `home/dot_config/nvim/lua/plugins/` | `~/.config/nvim/lua/plugins/` |
| Lockfile | `home/dot_config/nvim/lazy-lock.json` | `~/.config/nvim/lazy-lock.json` |
| Installed plugins | — | `~/.local/share/nvim/lazy/<plugin>/` |

**Always edit source (`home/dot_config/nvim/`), never destination. Deploy with `chezmoi apply`.**

## Mode: `debug` (default)

**Use tmux, not headless** — `--headless` skips lazy-loaded UI plugins (bufferline, noice, lualine), hiding real errors.

1. Copy debug script: `cp .claude/skills/nvim/nvim-debug.lua /tmp/nvim-debug.lua`
2. Launch: `tmux new-session -d -s nvim-debug -x 200 -y 50 "nvim -S /tmp/nvim-debug.lua"`
3. Wait + read: `sleep 8 && cat /tmp/nvim-debug-output.txt`
4. Check `[ERROR]` lines — these come from `snacks.notifier` history (where LazyVim routes errors)

## Mode: `fix <plugin>`

1. **Compare lockfiles** — if installed differs from source, version drift caused the break
2. **Check plugin history**: `git -C ~/.local/share/nvim/lazy/<plugin> log --oneline --grep="refactor!\|BREAKING" --all`
3. **Check upstream LazyVim**: `grep -rl "<plugin>" ~/.local/share/nvim/lazy/LazyVim/lua/lazyvim/` — they often fix breaking changes first
4. **Edit source** in `home/dot_config/nvim/lua/plugins/`, then `chezmoi diff` and `chezmoi apply`
5. **Clear compiled cache** if theme-related: `rm -rf ~/.cache/catppuccin`
6. **Re-run debug mode** to verify
7. **Sync lockfile**: `cp ~/.config/nvim/lazy-lock.json home/dot_config/nvim/lazy-lock.json`

## Mode: `update`

1. Run `:Lazy update` in Neovim (or headless equivalent)
2. Debug mode → fix any breakage → sync lockfile back to source

## Anti-patterns

- **Never** use inline `-c "lua ..."` — shell escaping mangles quotes. Write temp Lua files.
- **Never** edit `~/.config/nvim/` directly — chezmoi owns the destination.
- **Never** ignore lockfile drift — sync installed back to source or breakage recurs.

## Examples

```
/nvim                    → Run debug, report errors
/nvim fix catppuccin     → Fix catppuccin after breaking update
/nvim update             → Update all plugins, fix breakage
```
