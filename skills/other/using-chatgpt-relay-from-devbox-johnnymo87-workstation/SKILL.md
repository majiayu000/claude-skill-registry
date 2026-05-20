---
name: using-chatgpt-relay-from-devbox
description: Send ChatGPT queries from devbox via ask-question CLI. Use when /ask-question fails with "Server not running" or when setting up chatgpt-relay for first time on devbox.
allowed-tools: [Bash, Read]
---

# Using chatgpt-relay from Devbox

The `ask-question` CLI runs on devbox and talks to `ask-question-server` running on macOS with a real browser.

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│  DEVBOX (NixOS)                                                         │
│                                                                         │
│  Claude Code → /ask-question → ask-question CLI                         │
│                                      │                                  │
│                                      │ HTTP POST                        │
│                                      ▼                                  │
│                          localhost:3033 (tunnel)                        │
└─────────────────────────────────────│───────────────────────────────────┘
                                      │ SSH reverse tunnel
                                      │
┌─────────────────────────────────────│───────────────────────────────────┐
│  MACOS (local machine)              ▼                                   │
│                                                                         │
│                          ask-question-server:3033                       │
│                                      │                                  │
│                                      ▼                                  │
│                              Chromium (headless)                        │
│                              + ChatGPT session                          │
└─────────────────────────────────────────────────────────────────────────┘
```

## Setup

### 1. On macOS: Start the server

```bash
cd ~/Code/chatgpt-relay
npm install
ask-question-login          # One-time: log into ChatGPT in browser
ask-question-server         # Keep running
```

### 2. On macOS: Create SSH reverse tunnel

When connecting to devbox, add a reverse tunnel:

```bash
ssh -R 3033:localhost:3033 devbox
```

Or add to your SSH config:

```
Host devbox
    HostName <devbox-ip>
    User dev
    RemoteForward 3033 localhost:3033
```

### 3. On devbox: Install the CLI

```bash
cd ~/projects/chatgpt-relay
npm install
npm link
```

### 4. On devbox: Verify connection

```bash
# Check tunnel is working
curl -s http://localhost:3033/health | jq .
# Expected: {"ok":true}

# Test a query
ask-question "What is 2+2?"
```

## Environment Variables

The CLI uses `ASK_QUESTION_SERVER_URL` (default: `http://127.0.0.1:3033`).

With the SSH reverse tunnel, the default works. If using a different setup:

```bash
export ASK_QUESTION_SERVER_URL=http://localhost:3033
```

## Troubleshooting

### "Server not running or not responding"

1. **Check tunnel on devbox:**
   ```bash
   curl -s http://localhost:3033/health
   ```
   If no response, the SSH tunnel isn't active.

2. **Check server on macOS:**
   ```bash
   curl -s http://localhost:3033/health
   ```
   If no response, start `ask-question-server`.

3. **Reconnect with tunnel:**
   ```bash
   # On macOS, reconnect to devbox with -R flag
   ssh -R 3033:localhost:3033 devbox
   ```

### "No session found" or "Login required"

On macOS:
```bash
ask-question-login
```

### Tunnel drops on disconnect

The SSH tunnel only exists while your SSH connection is active. If you disconnect, reconnect with the `-R` flag.

For persistent tunnels, consider:
- Using `autossh` for automatic reconnection
- Running the tunnel in a separate tmux pane

### Response timeout

Default is 20 minutes. For complex questions:
```bash
ask-question -t 1800000 -f question.md -o answer.md
```
