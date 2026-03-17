---
name: osc52-clipboard
description: Use when copy/paste doesn't work over SSH, or clipboard not syncing between local and remote, or setting up terminal remoting
---

# OSC 52 Clipboard Setup

## Overview

OSC 52 is an escape sequence that allows remote terminals to write to the local system clipboard over SSH. This enables yanking in Neovim on the devbox and pasting locally on macOS.

## How It's Configured in This Repo

### tmux (`assets/tmux/extra.conf`)

```tmux
set -s set-clipboard on              # Accept OSC 52 from apps
set -gq allow-passthrough on         # tmux 3.3+ passthrough support
set -as terminal-features ',xterm-256color:clipboard'  # Ms capability
```

### Neovim (`assets/nvim/lua/user/settings.lua`)

```lua
-- HOW to talk to clipboard (use OSC 52 escape sequences)
vim.g.clipboard = "osc52"

-- WHEN to use clipboard (sync unnamed register with +)
vim.opt.clipboard = "unnamedplus"
```

**Both are required:** `vim.g.clipboard` sets the provider, `vim.opt.clipboard` makes yanks use it by default.

### Local Terminal (iTerm2)

Preferences → General → Selection → Enable "Applications in terminal may access clipboard"

## Testing

### Test 1: Raw SSH (no tmux)

```bash
ssh devbox
printf '\033]52;c;%s\007' "$(printf 'test-raw' | base64 | tr -d '\n')"
# Cmd+V locally should paste "test-raw"
```

### Test 2: Inside tmux

```bash
ssh devbox
tmux new
printf '\033]52;c;%s\007' "$(printf 'test-tmux' | base64 | tr -d '\n')"
# Cmd+V locally should paste "test-tmux"
```

### Test 3: Inside Neovim

```bash
nvim somefile
# Yank a line with `yy`
# Cmd+V locally should paste the line
```

### Test 4: Verify nvim settings

```vim
:lua print(vim.g.clipboard)
" Should print: osc52

:lua print(vim.o.clipboard)
" Should print: unnamedplus
```

## Troubleshooting

**If Tests 1 & 2 pass but Test 3 fails (nvim yanks don't reach clipboard):**

Check that `vim.opt.clipboard = "unnamedplus"` is set. Without this, yanks go to the unnamed register, not the `+` register that OSC 52 uses.

```vim
:lua print(vim.o.clipboard)
" Should print: unnamedplus
```

**If Test 2 fails (tmux)**, check:

```bash
tmux show -s set-clipboard    # Should be: on
tmux info | grep 'Ms:'        # Should NOT say [missing]
```

**After changing tmux config:** Must restart tmux server, not just detach/attach:

```bash
tmux kill-server
```

## Local Terminal Support

| Terminal | Support |
|----------|---------|
| iTerm2 | Works with "Allow clipboard access" enabled |
| WezTerm | Works out of the box |
| kitty | Works (may need `clipboard_control` config) |
| GNOME Terminal / VTE | Does NOT support OSC 52 |

## Note on Paste

OSC 52 is primarily for **copy** (yank → local clipboard). Pasting from local clipboard into remote nvim typically uses your terminal's paste function (Cmd+V in insert mode, or terminal's paste bracketing).

## Images

OSC 52 only handles **text**. For sharing images with Claude Code over SSH, use the [screenshot-to-devbox](../screenshot-to-devbox/SKILL.md) helper script, which:

1. Takes a screenshot on macOS
2. Uploads it to the devbox via scp
3. Copies the remote path to clipboard

Then paste the path into Claude Code:
```
Analyze this image: /home/dev/.cache/claude-images/screenshot-20240115-143022-12345.png
```
