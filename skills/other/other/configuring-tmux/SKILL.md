---
name: configuring-tmux
description: Build, review, and troubleshoot tmux configurations with modern best practices. Use when creating tmux.conf from scratch, adding plugins, configuring themes, integrating with Neovim, setting up session management, or debugging tmux issues.
---

# tmux Configuration Skill

Help users build, review, and maintain modern tmux configurations. Always check
for an existing config before proposing changes. Prefer the XDG config path.

## Before Making Changes

1. Check tmux version: `tmux -V`
2. Check existing config: `~/.config/tmux/tmux.conf` then `~/.tmux.conf`
3. Check if TPM is installed: `ls ~/.config/tmux/plugins/tpm` or `ls ~/.tmux/plugins/tpm`
4. Read the current config before editing

## Config File Location

Prefer the XDG-compliant path (supported since tmux 3.1):

```text
~/.config/tmux/tmux.conf      # modern (preferred)
~/.tmux.conf                   # legacy (still works)
```

If migrating, move the file and remove the old one.

## Essential Baseline Config

These are near-universal best practices. Start here:

```bash
# -- Prefix --
unbind C-b
set -g prefix C-a
bind C-a send-prefix

# -- General --
set -g mouse on
set -g base-index 1
setw -g pane-base-index 1
set -g renumber-windows on
set -g history-limit 50000
set -g display-time 4000
set -g status-interval 5
set -g focus-events on
set -sg escape-time 0
set -g set-clipboard on

# -- Terminal & Colors --
set -g default-terminal "tmux-256color"
set -ag terminal-overrides ",xterm-256color:RGB"

# -- Copy Mode (vi) --
setw -g mode-keys vi
bind -T copy-mode-vi v send -X begin-selection
bind -T copy-mode-vi y send -X copy-pipe-and-cancel

# -- Easy reload --
bind r source-file ~/.config/tmux/tmux.conf \; display "Reloaded!"

# -- Pane splitting (intuitive keys) --
bind | split-window -h -c "#{pane_current_path}"
bind - split-window -v -c "#{pane_current_path}"
unbind '"'
unbind %

# -- New windows keep current path --
bind c new-window -c "#{pane_current_path}"
```

## Plugin Manager (TPM)

TPM is the standard. Install to the XDG plugins directory:

```bash
git clone https://github.com/tmux-plugins/tpm ~/.config/tmux/plugins/tpm
```

In tmux.conf (must be at the BOTTOM):

```bash
# -- Plugins --
set -g @plugin 'tmux-plugins/tpm'
set -g @plugin 'tmux-plugins/tmux-sensible'

# Initialize TPM (keep these at the very bottom)
set-environment -g TMUX_PLUGIN_MANAGER_PATH '~/.config/tmux/plugins/'
run '~/.config/tmux/plugins/tpm/tpm'
```

**IMPORTANT**: The `set-environment` line tells TPM where plugins live. Without
it, TPM defaults to `~/.tmux/plugins/` and plugins end up split across two
locations.

After adding plugins: `prefix + I` to install, `prefix + U` to update.

### Installing plugins headlessly (outside tmux)

```bash
tmux start-server \; source-file ~/.config/tmux/tmux.conf
~/.config/tmux/plugins/tpm/bin/install_plugins
```

### Plugins that need a build step

**tmux-thumbs** is written in Rust. After TPM clones it, build it:

```bash
cd ~/.config/tmux/plugins/tmux-thumbs && cargo build --release
```

Without this, `prefix + Space` silently fails.

## Plugin Tiers

### Tier 1: Essential (install these first)

| Plugin                        | Purpose                               |
| ----------------------------- | ------------------------------------- |
| `tmux-plugins/tmux-sensible`  | Sane defaults everyone agrees on      |
| `tmux-plugins/tmux-resurrect` | Save/restore sessions across restarts |
| `tmux-plugins/tmux-continuum` | Auto-save sessions every 15 min       |
| `tmux-plugins/tmux-yank`      | System clipboard integration          |

### Tier 2: Power User

| Plugin                           | Purpose                                   |
| -------------------------------- | ----------------------------------------- |
| `laktak/extrakto`                | Fuzzy-select text from pane with fzf      |
| `fcsonline/tmux-thumbs`          | Vimium-like hint copy (Rust, needs build) |
| `sainnhe/tmux-fzf`               | Fuzzy find sessions/windows/panes         |
| `tmux-plugins/tmux-pain-control` | Standard pane navigation bindings         |

### Tier 3: Nice to Have

| Plugin                           | Purpose                              |
| -------------------------------- | ------------------------------------ |
| `tmux-plugins/tmux-open`         | Open highlighted file/URL            |
| `27medkamal/tmux-session-wizard` | Session management with fzf + zoxide |
| `tmux-plugins/tmux-fzf-url`      | Open URLs from pane                  |

## Neovim Integration

For seamless pane/split navigation between tmux and Neovim:

**Option A: All-in-one** — `aserowy/tmux.nvim` (nav + clipboard + resize)
**Option B: Navigation only** — `alexghergh/nvim-tmux-navigation` (Lua)
**Option C: Classic** — `christoomey/vim-tmux-navigator`

The tmux side needs matching keybindings. See [REFERENCE.md](REFERENCE.md) for setup.

## Themes

**catppuccin/tmux** — Modular status line with widgets, most popular modern theme:

```bash
set -g @plugin 'catppuccin/tmux'
set -g @catppuccin_flavor 'mocha'  # latte, frappe, macchiato, mocha
```

**dracula/tmux** — Feature-rich status bar with system info widgets.
**tokyo-night** — Matching theme if you use tokyo-night in your editor.

## tmux 3.6 Features Worth Using

- **Scrollbars**: `set -g pane-scrollbars on`
- **Popup windows**: `display-popup` for floating terminals/menus
- **Mode 2031**: Auto dark/light theme detection
- **Performance**: Better handling of slow terminals and fast output

## Troubleshooting Checklist

1. **Colors wrong?** Check `echo $TERM` inside tmux — should be `tmux-256color`
2. **Slow escape?** Set `escape-time 0` (tmux-sensible does this)
3. **Clipboard not working over SSH?** Ensure `set -g set-clipboard on` in config.
   tmux-yank uses OSC-52. Terminal must support it (iTerm2, kitty, WezTerm do).
4. **Plugins not loading?** TPM `run` line must be the LAST line in config.
   Run `prefix + I` after adding new plugins.
5. **tmux-thumbs not working?** It's Rust — needs `cargo build --release` after install.
6. **Plugins in wrong directory?** With XDG path, you need
   `set-environment -g TMUX_PLUGIN_MANAGER_PATH '~/.config/tmux/plugins/'`
   before the TPM `run` line.
7. **After upgrade issues?** Kill all tmux servers: `tmux kill-server`
8. **Removed options still active after reload?** `prefix + r` (source-file) does
   NOT unset removed options — they persist in tmux's memory. To clear a stale
   option: `tmux set-option -gu @option-name`. To verify what's live:
   `tmux show-options -g | grep pattern`. This is critical when iterating on
   plugin configs like `@thumbs-regexp-N` — old regexps stay active and can
   cause silent failures even after removing them from tmux.conf.

## tmux-thumbs Custom Patterns

tmux-thumbs uses Rust's `regex` crate. Add custom patterns with `@thumbs-regexp-N`.

**IMPORTANT**: When adding/removing/changing `@thumbs-regexp-N` patterns, you MUST
manually unset old values — config reload doesn't clear them:

```bash
# Unset a specific pattern
tmux set-option -gu @thumbs-regexp-1

# Check what's currently live
tmux show-options -g | grep thumbs

# Nuclear option: unset all thumbs settings
for opt in $(tmux show-options -g | grep @thumbs | cut -d' ' -f1); do
  tmux set-option -gu "$opt"
done
```

After clearing, reload config (`prefix + r`) to re-apply only what's in tmux.conf.

Useful settings:

- `@thumbs-osc52 1` — clipboard works over SSH
- `@thumbs-contrast 1` — hints show in brackets for readability

Useful patterns for coding workflows:

```bash
set -g @thumbs-regexp-1 '\S+\.\w+:\d+'            # file:line (src/main.rs:42)
set -g @thumbs-regexp-2 '\b[a-f0-9]{7,12}\b'       # short commit/change IDs
```

**Caution**: Test patterns one at a time. A bad regex causes thumbs to crash
silently (`|| true` in tmux-thumbs.sh swallows all errors). If thumbs flashes
and shows nothing, unset all `@thumbs-regexp-N` and add them back individually.

See [REFERENCE.md](REFERENCE.md) for detailed plugin configs and advanced patterns.
