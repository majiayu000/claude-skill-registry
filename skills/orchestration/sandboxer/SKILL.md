---
name: sandboxer
description: "Manage Claude Code terminal sessions via Sandboxer web dashboard. Use when: (1) listing running Claude Code sessions, (2) checking what a Claude session is doing, (3) sending commands to a Claude session, (4) creating or killing sessions, (5) user mentions 'sandboxer' or 'session'."
metadata:
  {
    "openclaw":
      {
        "emoji": "🖥️",
        "requires": { "bins": ["curl", "tmux", "jq"] }
      }
  }
---

# Sandboxer

Manage Claude Code sessions running in tmux via HTTP API.

**All commands run locally - no SSH needed.**

## Health Check (Run First!)

Before using any commands, verify Sandboxer is running:

```bash
curl -sf http://localhost:8081/api/sessions >/dev/null && echo "✓ Sandboxer is running" || echo "✗ Sandboxer not reachable"
```

**If Sandboxer is not reachable:**

```
✗ Sandboxer is not installed or not running on this machine.

To install Sandboxer, run:
  claude --dangerously-skip-permissions "clone github.com/chriopter/sandboxer to /home/sandboxer/git/sandboxer, read README.md for install instructions, then install sandboxer"

To start if already installed:
  sudo systemctl start sandboxer

See: https://github.com/chriopter/sandboxer
```

## List Sessions

```bash
curl -s http://localhost:8081/api/sessions | jq
```

Filter by project:

```bash
curl -s http://localhost:8081/api/sessions | jq '.[] | select(.name | contains("PROJECT"))'
```

## Read Session Output

See what Claude is doing:

```bash
tmux capture-pane -t "SESSION_NAME" -p | tail -80
```

## Send Command to Session

Forward user requests to Claude Code:

```bash
tmux send-keys -t "SESSION_NAME" "implement feature X" Enter
```

Then wait 10-30s and read output to check result.

## Create Session

```bash
curl -s "http://localhost:8081/create?type=claude&dir=/path/to/project"
```

Types: `claude`, `bash`, `lazygit`

## Kill Session

```bash
curl -s "http://localhost:8081/kill?session=SESSION_NAME"
```

## Workflow: Forward Tasks to Claude

When user says "do X" or "implement Y":

1. Find the right session: `curl -s http://localhost:8081/api/sessions | jq`
2. Send command: `tmux send-keys -t "SESSION" "do X" Enter`
3. Wait 10-30 seconds
4. Read result: `tmux capture-pane -t "SESSION" -p | tail -80`
5. Report back to user

## Web Dashboard

URL: `https://YOUR_SERVER:8080`

Shows live terminal previews. May require password.

## Installation

See [GitHub README](https://github.com/chriopter/sandboxer#install) for setup instructions.
