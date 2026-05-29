---
name: dotfiles-editing
description: Help editing vim/tmux/zsh configurations. Use when user mentions "edit vim config", "modify tmux", "change zsh", "add plugin", "customize neovim", "update alias", "init.lua", "vimrc", "tmux.conf", "zshrc", or configuration changes.
---

# dotfiles Configuration Editing

vim/tmux/zsh設定の編集とテストを支援する。

## File Structure Overview

### Neovim

| File | Purpose |
|------|---------|
| `init.lua` | Main entry point |
| `vim/lua/lazy-config.lua` | Plugin management (lazy.nvim) |
| `vim/lua/map.lua` | Key mappings |
| `vim/lua/edit.lua` | Editor settings |
| `vim/ftplugin/*.vim` | Filetype-specific settings |
| `vim/snippets/*.snip` | Custom snippets |

### tmux

| File | Purpose |
|------|---------|
| `tmux.conf` | Main configuration |
| `tmux_readme.md` | Keybinding reference |

### zsh

| File | Purpose |
|------|---------|
| `zshrc` | Main configuration |
| `zshenv` | Environment variables |
| `zsh/alias.zsh` | Shell aliases |
| `zsh/zinit.zsh` | Plugin management |

For complete file structure, see [references/file-structure.md](references/file-structure.md).

## Editing Guidelines

### Add Neovim Plugin

Edit `vim/lua/lazy-config.lua`:

```lua
{
  "author/plugin-name",
  config = function()
    -- configuration
  end,
},
```

### Add tmux Plugin

Edit `tmux.conf`:

```
set -g @plugin 'tmux-plugins/plugin-name'
```

### Add Shell Alias

Edit `zsh/alias.zsh`:

```bash
alias name='command'
```

### Add Environment Variable

Edit `zshenv`:

```bash
export VAR_NAME="value"
```

## Testing Changes

Use Docker sandbox to test:

```bash
make shell
# Inside container:
source ~/.zshrc              # zsh
tmux source ~/.tmux.conf     # tmux
:source $MYVIMRC             # neovim
```

## Best Practices

1. Test changes in Docker before committing
2. Add comments explaining configuration intent
3. Make incremental changes, test each one
