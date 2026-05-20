---
name: tmux
description: |
  Complete tmux terminal multiplexer management: sessions, windows, panes, layouts, scripting, and configuration.
  Auto-activates on: "tmux", "session", "window", "pane", "split", "attach", "detach", "multiplexer".
license: MIT
compatibility: Requires tmux (3.0+). Works on Linux/macOS/WSL.
metadata:
  version: "1.0"
allowed-tools: Bash Read Edit Write Glob Grep
---

# tmux

Complete tmux management for terminal multiplexing.

## Core Concepts

```
┌─────────────────────────────────────────────────────────────┐
│ SERVER (one per socket)                                     │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ SESSION ($0, $1, ...)                                 │  │
│  │  ┌─────────────────┐  ┌─────────────────┐            │  │
│  │  │ WINDOW (@0)     │  │ WINDOW (@1)     │  ...       │  │
│  │  │  ┌────┬────┐   │  │  ┌────────────┐ │            │  │
│  │  │  │PANE│PANE│   │  │  │   PANE     │ │            │  │
│  │  │  │ %0 │ %1 │   │  │  │    %2      │ │            │  │
│  │  │  └────┴────┘   │  │  └────────────┘ │            │  │
│  │  └─────────────────┘  └─────────────────┘            │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

- **Server**: Background process managing all state
- **Session** (`$id`): Named container of windows, persists after detach
- **Window** (`@id`): Tab-like container of panes within a session
- **Pane** (`%id`): Individual terminal within a window
- **Client**: Terminal attached to a session

## Router

| User says | Load reference | Do |
|---|---|---|
| list sessions / status | `references/session-management.md` | inspect sessions |
| new session / create session | `references/session-management.md` | create session |
| attach / detach | `references/session-management.md` | attach/detach |
| kill session | `references/session-management.md` | terminate session |
| new window / create window | `references/window-management.md` | create window |
| rename window | `references/window-management.md` | rename window |
| kill window / close window | `references/window-management.md` | close window |
| switch window | `references/window-management.md` | navigate windows |
| split / new pane | `references/pane-management.md` | split pane |
| resize pane | `references/pane-management.md` | resize pane |
| move pane / swap pane | `references/pane-management.md` | rearrange panes |
| kill pane / close pane | `references/pane-management.md` | close pane |
| layout | `references/layouts.md` | apply/manage layouts |
| copy / paste / buffer | `references/copy-mode.md` | copy mode operations |
| config / tmux.conf / settings | `references/configuration.md` | configure tmux |
| keybind / bind / unbind | `references/keybindings.md` | key bindings |
| script / automate / send-keys | `references/scripting.md` | scripting/automation |
| capture / log / output | `references/scripting.md` | capture pane content |
| help / keys / cheatsheet | inline | show key reference |

## Default Key Bindings (Prefix: `C-b`)

### Session

| Key | Action |
|-----|--------|
| `d` | Detach from session |
| `s` | List/switch sessions |
| `$` | Rename session |
| `(` / `)` | Previous/next session |

### Window

| Key | Action |
|-----|--------|
| `c` | Create window |
| `&` | Kill window (confirm) |
| `,` | Rename window |
| `0-9` | Switch to window N |
| `n` / `p` | Next/previous window |
| `l` | Last window |
| `w` | List windows |
| `f` | Find window |

### Pane

| Key | Action |
|-----|--------|
| `%` | Split horizontally (left/right) |
| `"` | Split vertically (top/bottom) |
| `x` | Kill pane (confirm) |
| `o` | Cycle panes |
| `q` | Show pane numbers |
| `z` | Toggle zoom |
| `{` / `}` | Swap pane left/right |
| `!` | Break pane to window |
| Arrows | Navigate panes |
| `Space` | Cycle layouts |
| `C-o` | Rotate panes |

### Copy Mode

| Key | Action |
|-----|--------|
| `[` | Enter copy mode |
| `]` | Paste buffer |
| `=` | Choose paste buffer |
| `#` | List buffers |

## Quick Reference

```bash
# Session
tmux new -s name              # Create named session
tmux attach -t name           # Attach to session
tmux ls                       # List sessions
tmux kill-session -t name     # Kill session

# Window
tmux new-window -n name       # Create named window
tmux select-window -t :N      # Go to window N
tmux rename-window name       # Rename current window

# Pane
tmux split-window -h          # Split horizontal
tmux split-window -v          # Split vertical
tmux select-pane -t :.N       # Go to pane N
tmux resize-pane -D 5         # Resize down 5 lines

# Info
tmux list-keys                # All key bindings
tmux info                     # Server info
```

## Safety Rules

- **Confirm before kill**: Always confirm before `kill-session`, `kill-window`, `kill-pane`
- **Check attachments**: Before killing, check if session has active clients
- **Preserve work**: Warn if panes have running processes
- **Config backup**: Before editing `~/.tmux.conf`, suggest backup

## Confirmation Policy

**Read-only (always OK)**:
- `tmux ls`, `list-sessions`, `list-windows`, `list-panes`
- `tmux info`, `show-options`, `display-message`
- `tmux list-keys`, `list-buffers`

**Requires confirmation**:
- `kill-session`, `kill-window`, `kill-pane`
- `kill-server`
- Editing `~/.tmux.conf`
- `send-keys` to panes (can affect running processes)

## Environment Variables

| Variable | Description |
|----------|-------------|
| `TMUX` | Socket path (set inside tmux) |
| `TMUX_PANE` | Current pane ID |

Check if inside tmux: `[ -n "$TMUX" ]`

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "no server running" | Start with `tmux` or `tmux new` |
| "sessions should be nested" | Unset `$TMUX` or use `tmux -u` |
| Detached session lost | Check `tmux ls`, attach with `tmux attach` |
| Colors not working | Set `TERM=xterm-256color` or `set -g default-terminal "tmux-256color"` |
| Mouse not working | `set -g mouse on` in config |
