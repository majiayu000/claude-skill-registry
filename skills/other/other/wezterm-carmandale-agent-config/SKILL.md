---
name: wezterm
description: "Control WezTerm terminal emulator via CLI. Manage panes, tabs, workspaces, and execute commands in running terminals."
---

# WezTerm Skill

Use the `wezterm` CLI to control and interact with WezTerm terminal instances.

## CLI Location

```bash
/Applications/WezTerm.app/Contents/MacOS/wezterm
```

Or add to PATH for easier access.

## Listing and Connecting

List all WezTerm panes:
```bash
wezterm cli list
```

List in JSON format:
```bash
wezterm cli list --format json
```

List clients (GUI windows):
```bash
wezterm cli list-clients
```

## Pane Management

Get current pane ID:
```bash
wezterm cli get-pane-direction
```

Split pane horizontally (new pane to right):
```bash
wezterm cli split-pane --right
```

Split pane vertically (new pane below):
```bash
wezterm cli split-pane --bottom
```

Split with specific command:
```bash
wezterm cli split-pane --right -- htop
```

Move focus between panes:
```bash
wezterm cli activate-pane-direction up
wezterm cli activate-pane-direction down
wezterm cli activate-pane-direction left
wezterm cli activate-pane-direction right
```

Activate specific pane by ID:
```bash
wezterm cli activate-pane --pane-id <pane-id>
```

## Tab Management

Create new tab:
```bash
wezterm cli spawn
```

Create tab with command:
```bash
wezterm cli spawn -- vim
```

Create tab in specific domain:
```bash
wezterm cli spawn --domain-name SSH:server
```

Activate tab by index:
```bash
wezterm cli activate-tab --tab-index 0
```

Activate tab relative:
```bash
wezterm cli activate-tab --tab-relative 1   # next tab
wezterm cli activate-tab --tab-relative -1  # previous tab
```

## Sending Commands to Panes

Send text to a pane:
```bash
wezterm cli send-text --pane-id <pane-id> "ls -la\n"
```

Send text to current pane:
```bash
wezterm cli send-text "echo hello\n"
```

## Workspaces

List workspaces:
```bash
wezterm cli list --format json | jq '.[].workspace' | sort -u
```

## Zoom

Toggle pane zoom:
```bash
wezterm cli zoom-pane --toggle
```

Zoom pane:
```bash
wezterm cli zoom-pane --zoom
```

Unzoom:
```bash
wezterm cli zoom-pane --unzoom
```

## Multiplexer Domains

List domains (local, SSH, etc.):
```bash
wezterm cli list --format json | jq '.[].domain_name' | sort -u
```

Connect to SSH domain:
```bash
wezterm cli spawn --domain-name SSH:myserver
```

## Configuration

Config file:
```
~/.config/wezterm/wezterm.lua
```

Show effective config:
```bash
wezterm show-keys
```

## Launching

Start new window:
```bash
wezterm start
```

Start with command:
```bash
wezterm start -- htop
```

Start in directory:
```bash
wezterm start --cwd /path/to/dir
```

Connect to running mux server:
```bash
wezterm connect unix
```
