---
name: ntm
description: "Named Tmux Manager - orchestrate multiple AI coding agents (Claude Code, Codex, Gemini) in tiled tmux panes with visual dashboards, command palette, context rotation, Agent Mail integration, and robot mode for automation."
---

# NTM - Named Tmux Manager

A powerful tmux session management tool for orchestrating multiple AI coding agents in parallel. Spawn, manage, and coordinate Claude Code, Codex, and Gemini agents across tiled panes with stunning TUI, automated context rotation, and deep integrations.

## Quick Start

```bash
# Check dependencies
ntm deps -v

# Shell integration (add to ~/.zshrc)
eval "$(ntm init zsh)"

# Interactive tutorial
ntm tutorial

# Create a multi-agent session
ntm spawn myproject --cc=2 --cod=1 --gmi=1

# Send a prompt to all Claude agents
ntm send myproject --cc "Explore this codebase and summarize its architecture."

# Open the command palette (or press F6 after `ntm bind`)
ntm palette myproject
```

## Session Creation

### Spawn Agents

```bash
# Spawn with specific agent counts
ntm spawn myproject --cc=3 --cod=2 --gmi=1

# Quick project setup (creates dir, git init, VSCode settings, spawns agents)
ntm quick myproject --template=go
ntm spawn myproject --cc=2

# Just create empty panes (no agents)
ntm create myproject --panes=10

# Using profiles/personas
ntm spawn myproject --profiles=architect,implementer,tester
ntm spawn myproject --profile-set=backend-team
```

### Agent Flags

| Flag | Agent Type | CLI |
|------|------------|-----|
| `--cc=N` | Claude Code | `claude` |
| `--cod=N` | Codex CLI | `codex` |
| `--gmi=N` | Gemini CLI | `gemini` |

### Add More Agents

```bash
# Add 2 more Claude agents to existing session
ntm add myproject --cc=2

# Add mixed agents
ntm add myproject --cod=1 --gmi=1
```

## Sending Prompts

### Broadcast to Agent Types

```bash
# Send to all Claude agents
ntm send myproject --cc "Implement the user auth module"

# Send to all Codex agents
ntm send myproject --cod "Write unit tests for auth"

# Send to all Gemini agents
ntm send myproject --gmi "Review and document the API"

# Send to ALL agents (excludes user pane)
ntm send myproject --all "Review the current codebase state"
```

### Interrupt All Agents

```bash
# Send Ctrl+C to all agent panes
ntm interrupt myproject
```

## Session Navigation

| Command | Alias | Description |
|---------|-------|-------------|
| `ntm list` | `lnt` | List all tmux sessions |
| `ntm attach` | `rnt` | Attach to session |
| `ntm status` | `snt` | Show detailed status with agent counts |
| `ntm view` | `vnt` | Unzoom, tile layout, attach |
| `ntm zoom` | `znt` | Zoom to specific pane |
| `ntm dashboard` | `dash`, `d` | Interactive visual dashboard |
| `ntm kill` | `knt` | Kill session (`-f` to force) |

```bash
# View session status (shows C/X/G/U indicators)
ntm status myproject

# View all panes in tiled layout
ntm view myproject

# Zoom to pane 3
ntm zoom myproject 3

# Kill session (with confirmation)
ntm kill myproject

# Force kill (no prompt)
ntm kill -f myproject
```

## Command Palette

Fuzzy-searchable TUI with pre-configured prompts:

```bash
# Open palette for session
ntm palette myproject

# Or press F6 in tmux (after running ntm bind)
ntm bind                    # Set up F6 keybinding
ntm bind --key=F5           # Use different key
ntm bind --show             # Show current binding
```

### Palette Features

- Animated gradient banner with Catppuccin themes
- Fuzzy search through all commands
- Pin/favorite commands (`Ctrl+P` / `Ctrl+F`)
- Live preview pane with prompt metadata
- Quick select with numbers 1-9
- Visual target selector (All/Claude/Codex/Gemini)
- Help overlay with `?` or `F1`

### Palette Navigation

| Key | Action |
|-----|--------|
| `↑/↓` or `j/k` | Navigate commands |
| `1-9` | Quick select command |
| `Enter` | Select command |
| `Esc` | Back / Quit |
| `?` | Help overlay |
| `Ctrl+P` | Pin/unpin command |
| `Ctrl+F` | Favorite/unfavorite |

## Interactive Dashboard

Visual monitoring for any session:

```bash
ntm dashboard myproject
# Or: ntm dash myproject
# Or: d myproject (with shell aliases)
```

### Dashboard Features

- Visual pane grid with color-coded agent cards
- Live agent counts (Claude/Codex/Gemini/User)
- Token velocity badges (tokens-per-minute)
- Context usage indicators (green/yellow/orange/red)
- Real-time refresh with `r`
- Quick zoom with `z` or `Enter`
- Context shortcuts with `c`, mail with `m`

### Dashboard Navigation

| Key | Action |
|-----|--------|
| `↑/↓` or `j/k` | Navigate panes |
| `1-9` | Quick select pane |
| `z` or `Enter` | Zoom to pane |
| `r` | Refresh pane data |
| `c` | View context usage |
| `m` | Open Agent Mail |
| `q` or `Esc` | Quit dashboard |

## Output Capture

### Copy Output

```bash
# Copy specific pane
ntm copy myproject:1

# Copy all pane outputs
ntm copy myproject --all

# Copy only Claude panes
ntm copy myproject --cc

# Filter lines by regex
ntm copy myproject --pattern 'ERROR'

# Extract only code blocks
ntm copy myproject --code

# Save to file instead of clipboard
ntm copy myproject --output errors.txt

# Last N lines
ntm copy myproject --cc -l 500
```

### Save Outputs

```bash
# Save all outputs to timestamped files
ntm save myproject -o ~/logs

# Save only Codex outputs
ntm save myproject --cod -o ~/logs
```

## Monitoring & Analysis

```bash
# Real-time agent activity
ntm activity myproject --watch

# Health status
ntm health myproject

# Stream agent output
ntm watch myproject --cc

# Extract code blocks from output
ntm extract myproject --lang=go

# Compare two panes
ntm diff myproject cc_1 cod_1

# Search pane output
ntm grep 'error' myproject -C 3

# Session analytics
ntm analytics --days 7

# File reservation locks
ntm locks myproject --all-agents
```

## Checkpoints

Save and restore session state:

```bash
# Create checkpoint
ntm checkpoint save myproject -m "Before refactor"

# List checkpoints
ntm checkpoint list myproject

# Show checkpoint details
ntm checkpoint show myproject 20251210-143052

# Delete checkpoint
ntm checkpoint delete myproject 20251210-143052 -f
```

## Context Window Management

NTM monitors context usage and auto-rotates agents before they exhaust context.

### How It Works

1. **Monitoring**: Token usage estimated per agent
2. **Warning**: Alert at 80% usage
3. **Compaction**: Try `/compact` or summarization first
4. **Rotation**: Fresh agent with handoff summary if needed

### Context Indicators

| Color | Usage | Status |
|-------|-------|--------|
| Green | < 40% | Plenty of room |
| Yellow | 40-60% | Comfortable |
| Orange | 60-80% | Approaching threshold |
| Red | > 80% | Needs attention |

### Compaction Recovery

When an agent's context is compacted, NTM auto-sends a recovery prompt to help regain project context, optionally including bead state from `bv`.

## Agent Mail Integration

Multi-agent coordination across sessions:

```bash
# Send message to specific agent
ntm mail send myproject --to GreenCastle "Review the API changes"

# Send to all agents
ntm mail send myproject --all "Checkpoint: sync and report status"

# View inboxes
ntm mail inbox myproject

# Read specific agent's mail
ntm mail read myproject --agent BlueLake

# Acknowledge message
ntm mail ack myproject 42
```

### Pre-commit Guard

Prevent commits that conflict with other agents' file reservations:

```bash
ntm hooks guard install
ntm hooks guard uninstall
```

## Robot Mode (AI Automation)

Machine-readable JSON output for integration with AI agents:

### State Inspection

```bash
ntm --robot-status              # Sessions, panes, agent states
ntm --robot-context=SESSION     # Context window usage per agent
ntm --robot-snapshot            # Unified state: sessions + beads + mail
ntm --robot-tail=SESSION        # Recent pane output
ntm --robot-plan                # bv execution plan
ntm --robot-health              # Project health summary
ntm --robot-dashboard           # Dashboard summary
```

### Agent Control

```bash
ntm --robot-send=SESSION --msg="Fix auth" --type=claude
ntm --robot-spawn=SESSION --spawn-cc=2 --spawn-wait
ntm --robot-interrupt=SESSION
ntm --robot-assign=SESSION --assign-beads=bd-1,bd-2
```

### CASS Integration

```bash
ntm --robot-cass-search="auth error" --cass-since=7d
ntm --robot-cass-context="how to implement auth"
ntm --robot-cass-status
```

## Profiles & Personas

Define agent behavioral characteristics:

```bash
# List available profiles
ntm profiles list

# Show profile details
ntm profiles show architect

# Filter by agent or tag
ntm profiles list --agent claude --tag review

# Spawn with profiles
ntm spawn myproject --profiles=architect,implementer,tester
```

### Built-in Profiles

- `architect` - High-level design and review
- `implementer` - Feature implementation
- `reviewer` - Code review and quality
- `tester` - Testing and validation
- `documenter` - Documentation

## Notifications

Multi-channel notifications for events:

```bash
# Configure in ~/.config/ntm/config.toml
[notifications]
enabled = true
events = ["agent.error", "agent.crashed", "agent.rate_limit"]

[notifications.desktop]
enabled = true

[notifications.webhook]
enabled = true
url = "https://hooks.slack.com/..."
```

### Event Types

| Event | Description |
|-------|-------------|
| `agent.error` | Agent hit an error |
| `agent.crashed` | Agent exited unexpectedly |
| `agent.rate_limit` | Rate limit hit |
| `rotation.needed` | Context rotation needed |
| `session.created` | New session spawned |

## Command Hooks

Run custom scripts on NTM events:

```toml
# ~/.config/ntm/hooks.toml

[[command_hooks]]
event = "post-spawn"
command = "notify-send 'NTM' 'Agents spawned'"

[[command_hooks]]
event = "pre-send"
command = "echo \"$(date): $NTM_MESSAGE\" >> ~/.ntm-send.log"
```

### Available Events

`pre-spawn`, `post-spawn`, `pre-send`, `post-send`, `pre-add`, `post-add`, `pre-shutdown`, `post-shutdown`

## Multi-Agent Strategies

### Divide and Conquer

```bash
ntm send myproject --cc "design the database schema"
ntm send myproject --cod "implement the models"
ntm send myproject --gmi "write tests"
```

### Competitive Comparison

```bash
ntm send myproject --all "implement a rate limiter"
ntm view myproject  # Compare side-by-side
```

### Specialist Teams

```bash
ntm send myproject --cc "focus on architecture and review"
ntm send myproject --cod "focus on implementation"
ntm send myproject --gmi "focus on testing and docs"
```

### Review Pipeline

```bash
ntm send myproject --cc "implement feature X"
# Wait, then:
ntm send myproject --cod "review Claude's code"
ntm send myproject --gmi "write tests for edge cases"
```

## Shell Aliases

After `eval "$(ntm init zsh)"`:

| Category | Aliases |
|----------|---------|
| Agent Launch | `cc`, `cod`, `gmi` |
| Session | `cnt`, `sat`, `qps` (create, spawn, quick) |
| Agent Mgmt | `ant`, `bp`, `int` (add, send, interrupt) |
| Navigation | `rnt`, `lnt`, `snt`, `vnt`, `znt` |
| Dashboard | `dash`, `d` |
| Output | `cpnt`, `svnt` |
| Utilities | `ncp`, `knt`, `cad` |

## Configuration

```bash
ntm config init          # Create default config
ntm config show          # Show current config
ntm config project init  # Create .ntm/config.toml in project
```

### Config File (`~/.config/ntm/config.toml`)

```toml
projects_base = "~/Developer"

[agents]
claude = 'claude --dangerously-skip-permissions'
codex = "codex --dangerously-bypass-approvals-and-sandbox"
gemini = "gemini --yolo"

[tmux]
default_panes = 10
palette_key = "F6"

[context_rotation]
enabled = true
warning_threshold = 0.80
rotate_threshold = 0.95
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `NTM_PROJECTS_BASE` | Base directory for projects |
| `NTM_THEME` | Color theme: `auto`, `mocha`, `latte`, `nord`, `plain` |
| `NTM_ICONS` | Icon set: `nerd`, `unicode`, `ascii` |
| `NTM_REDUCE_MOTION` | Disable animations |

## Pane Naming Convention

Panes follow the pattern: `<project>__<agent>_<number>`

- `myproject__cc_1` - First Claude agent
- `myproject__cod_2` - Second Codex agent
- `myproject__gmi_1` - First Gemini agent

In status output:
- **C** = Claude
- **X** = Codex
- **G** = Gemini
- **U** = User pane

## Upgrade

```bash
ntm upgrade               # Check and install updates
ntm upgrade --check       # Check only
ntm upgrade --yes         # Auto-confirm
```

## Requirements

- tmux (any recent version)
- At least one agent CLI: `claude`, `codex`, or `gemini`
- Optional: `bv` for beads, Agent Mail MCP for coordination
