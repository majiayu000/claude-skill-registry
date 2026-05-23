---
name: tmux
description: Manage concurrent background processes using tmux. Use when spawning dev servers, running long-running tasks, monitoring multiple processes, or capturing output from background commands without blocking the main session.
allowed-tools:
  - Bash
---

# Tmux Skill

This skill empowers you to manage multiple concurrent processes (like servers, watchers, or long builds) using `tmux` directly from the `Bash` tool.

Since you are likely already running inside a tmux session, you can spawn new windows or panes to handle these tasks without blocking your main communication channel.

## 1. Verify Environment & Check Status

First, verify you are running inside tmux:

```bash
echo $TMUX
```

If this returns empty, you are not running inside tmux and these commands will not work as expected.

Once verified, check your current windows:

```bash
tmux list-windows
```

## 2. Spawn a Background Process

To run a command (e.g., a dev server) in a way that persists and can be inspected:

1.  **Create a new detached window** with a specific name. This keeps it isolated and easy to reference.

    ```bash
    tmux new-window -n "server-log" -d
    ```

    _(Replace "server-log" with a relevant name for your task)_

2.  **Send the command** to that window.
    ```bash
    tmux send-keys -t "server-log" "npm start" C-m
    ```
    _(`C-m` simulates the Enter key)_

## 3. Inspect Output (Read Logs)

You can read the output of that pane at any time without switching your context.

**Get the current visible screen:**

```bash
tmux capture-pane -p -t "server-log"
```

**Get the entire history (scrollback):**

```bash
tmux capture-pane -p -S - -t "server-log"
```

_Use this if the output might have scrolled off the screen._

## 4. Interact with the Process

If you need to stop or restart the process:

**Send Ctrl+C (Interrupt):**

```bash
tmux send-keys -t "server-log" C-c
```

**Kill the window (Clean up):**

```bash
tmux kill-window -t "server-log"
```

## 5. Advanced: Chaining Commands

You can chain multiple tmux commands in a single invocation using `';'` (note the quotes to avoid interpretation by the shell). This is faster and cleaner than running multiple `tmux` commands.

Example: Create window and start process in one go:

```bash
tmux new-window -n "server-log" -d ';' send-keys -t "server-log" "npm start" C-m
```

## Summary of Pattern

1. `tmux new-window -n "ID" -d`
2. `tmux send-keys -t "ID" "CMD" C-m`
3. `tmux capture-pane -p -t "ID"`

---

## 6. Multi-Model Fan Out Pattern

Used when you want to get perspectives from multiple AI models in parallel (e.g., GPT-5.2, Gemini Pro).

### Setup

```bash
# Kill existing session, create new with multiple windows
tmux kill-session -t model-consult 2>/dev/null
tmux new-session -d -s model-consult -n gpt5 ';' new-window -t model-consult -n gemini
```

### Send Queries

Use heredoc to avoid quote escaping issues:

```bash
tmux send-keys -t model-consult:gpt5 'cat <<EOF | opencode run --model openai/gpt-5.2 -
Your prompt here
EOF
echo ###DONE###' C-m
```

### Poll for Completion

```bash
tmux capture-pane -p -S - -t model-consult:gpt5 | tail -50
# Look for ###DONE### marker
```

Poll every ~10 seconds. Queries typically take 2-5 minutes.

### Capture Full Output

```bash
tmux capture-pane -p -S - -t model-consult:gpt5
```

The `-S -` flag captures full scrollback history, not just visible screen.

### Cleanup

```bash
tmux kill-session -t model-consult
```

### Model Aliases Reference

| Alias | Model ID |
|-------|----------|
| GPT | `openai/gpt-5.2` |
| Gemini Pro | `google/gemini-3-pro-preview` |

Run `opencode models` for full list.

### Key Learnings

1. USE HEREDOC (`cat <<EOF`) to avoid quote escaping nightmares
2. ADD `###DONE###` marker to know when query completes
3. USE `-S -` flag with `capture-pane` to get full scrollback
4. POLL every 10 seconds - queries can take 2-5 minutes
