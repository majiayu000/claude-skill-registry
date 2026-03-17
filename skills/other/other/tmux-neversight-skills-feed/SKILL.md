---
name: tmux
description: Control interactive terminal sessions via tmux. Use when tasks need persistent REPLs, parallel CLI agents, or any process requiring a TTY that simple shell execution cannot handle.
metadata:
  os:
    - darwin
    - linux
  requires:
    bins:
      - tmux
---

# tmux Skill

Use tmux only when you need an interactive TTY. Prefer exec background mode for long-running, non-interactive tasks.

## Quickstart

```bash
SOCKET_DIR="${TMUX_SOCKET_DIR:-${TMPDIR:-/tmp}/tmux-sockets}"
mkdir -p "$SOCKET_DIR"
SOCKET="$SOCKET_DIR/tmux.sock"
SESSION=my-session

tmux -S "$SOCKET" new -d -s "$SESSION" -n shell
tmux -S "$SOCKET" send-keys -t "$SESSION":0.0 -- 'PYTHON_BASIC_REPL=1 python3 -q' Enter
tmux -S "$SOCKET" capture-pane -p -J -t "$SESSION":0.0 -S -200
```

## Essential Commands

| Action            | Command                                                  |
| ----------------- | -------------------------------------------------------- |
| Send text         | `tmux -S "$SOCKET" send-keys -t target -l -- "$cmd"`     |
| Send Enter/Ctrl-C | `tmux -S "$SOCKET" send-keys -t target Enter` / `C-c`    |
| Capture output    | `tmux -S "$SOCKET" capture-pane -p -J -t target -S -200` |
| List sessions     | `tmux -S "$SOCKET" list-sessions`                        |
| Kill session      | `tmux -S "$SOCKET" kill-session -t "$SESSION"`           |
| Kill server       | `tmux -S "$SOCKET" kill-server`                          |

## Conventions

- **Socket**: `TMUX_SOCKET_DIR` env var (default `${TMPDIR:-/tmp}/tmux-sockets`)
- **Target format**: `session:window.pane` (defaults to `:0.0`)
- **Python REPLs**: Set `PYTHON_BASIC_REPL=1` to avoid readline issues

## Helper Scripts

```bash
./scripts/find-sessions.sh -S "$SOCKET"        # list sessions
./scripts/find-sessions.sh --all               # scan all sockets
./scripts/wait-for-text.sh -t sess:0.0 -p 'pattern' [-T 20] [-i 0.5]
```

## Parallel Agents Example

```bash
SOCKET="${TMPDIR:-/tmp}/agents.sock"
for i in 1 2 3; do tmux -S "$SOCKET" new-session -d -s "agent-$i"; done
tmux -S "$SOCKET" send-keys -t agent-1 "codex --yolo 'Fix bug'" Enter

# Poll for completion
tmux -S "$SOCKET" capture-pane -p -t agent-1 -S -3 | grep -q "❯" && echo "Done"
```
