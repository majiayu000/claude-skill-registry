---
name: ntm
description: "Named Tmux Manager - Multi-agent orchestration for Claude Code, Codex, and Gemini in tiled tmux panes. Visual dashboards, command palette, context rotation, robot mode API, work assignment, safety system. Go CLI."
---

# NTM — Named Tmux Manager

A Go CLI that transforms tmux into a **multi-agent command center** for orchestrating Claude Code, Codex, and Gemini agents in parallel. Spawn, manage, and coordinate AI agents across tiled panes with stunning TUI, automated context rotation, and deep integrations with the Agent Flywheel ecosystem.

## Why This Exists

Managing multiple AI coding agents is painful:
- **Window chaos**: Each agent needs its own terminal
- **Context switching**: Jumping between windows breaks flow
- **No orchestration**: Same prompt to multiple agents requires manual copy-paste
- **Session fragility**: Disconnecting from SSH loses all agent sessions
- **No visibility**: Hard to see agent status at a glance

NTM solves all of this with one session containing many agents, persistent across SSH disconnections.

## Quick Start

```bash
# Install
curl -fsSL https://raw.githubusercontent.com/Dicklesworthstone/ntm/main/install.sh | bash

# Add shell integration
echo 'eval "$(ntm init zsh)"' >> ~/.zshrc && source ~/.zshrc

# Interactive tutorial
ntm tutorial

# Check dependencies
ntm deps -v

# Create multi-agent session
ntm spawn myproject --cc=2 --cod=1 --gmi=1

# Send prompt to all Claude agents
ntm send myproject --cc "Explore this codebase and summarize its architecture."

# Open command palette (or press F6 after `ntm bind`)
ntm palette myproject
```

## Session Creation

### Spawn Agents

```bash
ntm spawn myproject --cc=3 --cod=2 --gmi=1   # 3 Claude + 2 Codex + 1 Gemini
ntm quick myproject --template=go             # Full project scaffold + agents
ntm create myproject --panes=10               # Empty panes only
ntm spawn myproject --profiles=architect,implementer,tester
```

### Agent Flags

| Flag | Agent | CLI Command |
|------|-------|-------------|
| `--cc=N` | Claude Code | `claude` |
| `--cod=N` | Codex CLI | `codex` |
| `--gmi=N` | Gemini CLI | `gemini` |

### Add More Agents

```bash
ntm add myproject --cc=2              # Add 2 more Claude agents
ntm add myproject --cod=1 --gmi=1     # Add mixed agents
```

## Sending Prompts

```bash
ntm send myproject --cc "Implement user auth"     # To all Claude
ntm send myproject --cod "Write unit tests"       # To all Codex
ntm send myproject --gmi "Review and document"    # To all Gemini
ntm send myproject --all "Review current state"   # To ALL agents
ntm interrupt myproject                           # Ctrl+C to all
```

## Session Navigation

| Command | Alias | Description |
|---------|-------|-------------|
| `ntm list` | `lnt` | List all tmux sessions |
| `ntm attach` | `rnt` | Attach to session |
| `ntm status` | `snt` | Show pane details with agent counts |
| `ntm view` | `vnt` | Unzoom, tile layout, attach |
| `ntm zoom` | `znt` | Zoom to specific pane |
| `ntm dashboard` | `dash`, `d` | Interactive visual dashboard |
| `ntm kill` | `knt` | Kill session (`-f` to force) |

## Command Palette

Fuzzy-searchable TUI with pre-configured prompts:

```bash
ntm palette myproject    # Open palette
ntm bind                 # Set up F6 keybinding
ntm bind --key=F5        # Use different key
```

### Palette Features

- Animated gradient banner with Catppuccin themes
- Fuzzy search with live filtering
- Pin/favorite commands (`Ctrl+P` / `Ctrl+F`)
- Live preview pane with metadata
- Quick select with numbers 1-9
- Visual target selector (All/Claude/Codex/Gemini)

### Palette Navigation

| Key | Action |
|-----|--------|
| `↑/↓` or `j/k` | Navigate |
| `1-9` | Quick select |
| `Enter` | Select command |
| `Esc` | Back / Quit |
| `?` | Help overlay |
| `Ctrl+P` | Pin/unpin |
| `Ctrl+F` | Favorite |

## Interactive Dashboard

```bash
ntm dashboard myproject   # Or: ntm dash myproject
```

### Dashboard Features

- Visual pane grid with color-coded agent cards
- Live agent counts (Claude/Codex/Gemini/User)
- Token velocity badges (tokens-per-minute)
- Context usage indicators (green/yellow/orange/red)
- Real-time refresh with `r`

### Dashboard Navigation

| Key | Action |
|-----|--------|
| `↑/↓` or `j/k` | Navigate panes |
| `1-9` | Quick select |
| `z` or `Enter` | Zoom to pane |
| `r` | Refresh |
| `c` | View context |
| `m` | Open Agent Mail |
| `q` | Quit |

## Output Capture

```bash
ntm copy myproject:1              # Copy specific pane
ntm copy myproject --all          # Copy all panes
ntm copy myproject --cc           # Copy Claude panes only
ntm copy myproject --pattern 'ERROR'  # Filter by regex
ntm copy myproject --code         # Extract code blocks only
ntm copy myproject --output out.txt   # Save to file
ntm save myproject -o ~/logs      # Save all outputs
```

## Monitoring & Analysis

```bash
ntm activity myproject --watch    # Real-time activity
ntm health myproject              # Health status
ntm watch myproject --cc          # Stream output
ntm extract myproject --lang=go   # Extract code blocks
ntm diff myproject cc_1 cod_1     # Compare panes
ntm grep 'error' myproject -C 3   # Search with context
ntm analytics --days 7            # Session statistics
ntm locks myproject --all-agents  # File reservations
```

### Activity States

| State | Icon | Description |
|-------|------|-------------|
| WAITING | ● | Idle, ready for work |
| GENERATING | ▶ | Producing output |
| THINKING | ◐ | Processing (no output yet) |
| ERROR | ✗ | Encountered error |
| STALLED | ◯ | Stopped unexpectedly |

## Checkpoints

```bash
ntm checkpoint save myproject -m "Before refactor"
ntm checkpoint list myproject
ntm checkpoint show myproject 20251210-143052
ntm checkpoint delete myproject 20251210-143052 -f
```

## Context Window Rotation

NTM monitors context usage and auto-rotates agents before exhausting context.

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

### Automatic Compaction Recovery

When context is compacted, NTM sends a recovery prompt:

```toml
[context_rotation.recovery]
enabled = true
prompt = "Reread AGENTS.md so it's still fresh in your mind. Use ultrathink."
include_bead_context = true   # Include project state from bv
```

## Robot Mode (AI Automation)

Machine-readable JSON output for AI agents and automation.

### State Inspection

```bash
ntm --robot-status              # Sessions, panes, agent states
ntm --robot-context=SESSION     # Context window usage
ntm --robot-snapshot            # Unified state: sessions + beads + mail
ntm --robot-tail=SESSION        # Recent pane output
ntm --robot-inspect-pane=SESS   # Detailed pane inspection
ntm --robot-files=SESSION       # File changes with attribution
ntm --robot-metrics=SESSION     # Session metrics
ntm --robot-plan                # bv execution plan
ntm --robot-dashboard           # Dashboard summary
ntm --robot-health              # Project health
```

### Agent Control

```bash
ntm --robot-send=SESSION --msg="Fix auth" --type=claude
ntm --robot-spawn=SESSION --spawn-cc=2 --spawn-wait
ntm --robot-interrupt=SESSION
ntm --robot-assign=SESSION --assign-beads=bd-1,bd-2
ntm --robot-replay=SESSION --replay-id=ID
```

### Bead Management

```bash
ntm --robot-bead-claim=BEAD_ID --bead-assignee=agent
ntm --robot-bead-create --bead-title="Fix bug" --bead-type=bug
ntm --robot-bead-show=BEAD_ID
ntm --robot-bead-close=BEAD_ID --bead-close-reason="Fixed"
```

### CASS Integration

```bash
ntm --robot-cass-search="auth error" --cass-since=7d
ntm --robot-cass-context="how to implement auth"
ntm --robot-cass-status
```

### Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Success |
| `1` | Error |
| `2` | Unavailable/Not implemented |

## Work Distribution

Integration with BV for intelligent work assignment:

```bash
ntm work triage               # Full triage with recommendations
ntm work triage --by-label    # Group by domain
ntm work triage --quick       # Quick wins only
ntm work alerts               # Stale issues, priority drift, cycles
ntm work search "JWT auth"    # Semantic search
ntm work impact src/api/*.go  # Impact analysis
ntm work next                 # Single best next action
```

### Intelligent Assignment

```bash
ntm --robot-assign=myproject --assign-strategy=balanced  # Default
ntm --robot-assign=myproject --assign-strategy=speed     # Maximize throughput
ntm --robot-assign=myproject --assign-strategy=quality   # Best agent-task match
ntm --robot-assign=myproject --assign-strategy=dependency # Unblock downstream
```

### Agent Capability Matrix

| Agent | Best At |
|-------|---------|
| **Claude** | Analysis, refactoring, documentation, architecture |
| **Codex** | Feature implementation, bug fixes, quick tasks |
| **Gemini** | Documentation, analysis, features |

## Profiles & Personas

```bash
ntm profiles list                    # List profiles
ntm profiles show architect          # Show details
ntm spawn myproject --profiles=architect,implementer,tester
ntm spawn myproject --profile-set=backend-team
```

### Built-in Profiles

`architect`, `implementer`, `reviewer`, `tester`, `documenter`

## Agent Mail Integration

```bash
ntm mail send myproject --to GreenCastle "Review API changes"
ntm mail send myproject --all "Checkpoint: sync status"
ntm mail inbox myproject
ntm mail read myproject --agent BlueLake
ntm mail ack myproject 42
```

### Pre-commit Guard

```bash
ntm hooks guard install    # Prevent conflicting commits
ntm hooks guard uninstall
```

## Notifications

Multi-channel notifications for events:

```toml
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

`agent.error`, `agent.crashed`, `agent.rate_limit`, `rotation.needed`, `session.created`, `session.killed`, `health.degraded`

## Alerting System

### Alert Types

| Type | Severity | Description |
|------|----------|-------------|
| `unhealthy` | High | Agent enters unhealthy state |
| `degraded` | Medium | Agent performance degrades |
| `rate_limited` | Medium | API rate limit detected |
| `restart_failed` | High | Restart attempt failed |
| `max_restarts` | Critical | Restart limit exceeded |

```bash
ntm --robot-alerts
ntm --robot-dismiss-alert=ALERT_ID
```

## Command Hooks

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

## Safety System

Blocks dangerous commands from AI agents:

```bash
ntm safety status              # Protection status
ntm safety check "git reset --hard"
ntm safety install             # Install git wrapper + Claude hook
ntm safety uninstall
```

### Protected Commands

| Pattern | Risk | Action |
|---------|------|--------|
| `git reset --hard` | Loses uncommitted changes | Block |
| `git push --force` | Overwrites remote history | Block |
| `rm -rf /` | Catastrophic deletion | Block |
| `DROP TABLE` | Database destruction | Block |

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

### Review Pipeline

```bash
ntm send myproject --cc "implement feature X"
ntm send myproject --cod "review Claude's code"
ntm send myproject --gmi "write tests for edge cases"
```

## Configuration

```bash
ntm config init          # Create ~/.config/ntm/config.toml
ntm config show          # Show current config
ntm config project init  # Create .ntm/config.toml in project
```

### Example Config

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
| `NTM_PROFILE` | Enable performance profiling |

## Themes & Display

### Color Themes

| Theme | Description |
|-------|-------------|
| `auto` | Detect light/dark |
| `mocha` | Default dark, warm |
| `latte` | Light variant |
| `nord` | Arctic-inspired |
| `plain` | No color |

### Agent Colors

| Agent | Color |
|-------|-------|
| Claude | Mauve (Purple) |
| Codex | Blue |
| Gemini | Yellow |
| User | Green |

### Display Width Tiers

| Width | Behavior |
|-------|----------|
| <120 cols | Stacked layout |
| 120-199 cols | List/detail split |
| 200-239 cols | Wider gutters |
| 240+ cols | Full detail |

## Pane Naming Convention

Pattern: `<project>__<agent>_<number>`

- `myproject__cc_1` - First Claude
- `myproject__cod_2` - Second Codex
- `myproject__gmi_1` - First Gemini

Status indicators: **C** = Claude, **X** = Codex, **G** = Gemini, **U** = User

## Shell Aliases

After `eval "$(ntm init zsh)"`:

| Category | Aliases |
|----------|---------|
| Agent Launch | `cc`, `cod`, `gmi` |
| Session | `cnt`, `sat`, `qps` |
| Agent Mgmt | `ant`, `bp`, `int` |
| Navigation | `rnt`, `lnt`, `snt`, `vnt`, `znt` |
| Dashboard | `dash`, `d` |
| Output | `cpnt`, `svnt` |
| Utilities | `ncp`, `knt`, `cad` |

## Installation

```bash
# One-liner (recommended)
curl -fsSL https://raw.githubusercontent.com/Dicklesworthstone/ntm/main/install.sh | bash

# Homebrew
brew install dicklesworthstone/tap/ntm

# Go install
go install github.com/Dicklesworthstone/ntm/cmd/ntm@latest

# Docker
docker pull ghcr.io/dicklesworthstone/ntm:latest
```

## Upgrade

```bash
ntm upgrade              # Check and install updates
ntm upgrade --check      # Check only
ntm upgrade --yes        # Auto-confirm
```

## Tmux Essentials

| Keys | Action |
|------|--------|
| `Ctrl+B, D` | Detach |
| `Ctrl+B, [` | Scroll/copy mode |
| `Ctrl+B, z` | Toggle zoom |
| `Ctrl+B, Arrow` | Navigate panes |
| `F6` | Open NTM palette (after `ntm bind`) |

## Integration with Flywheel

| Tool | Integration |
|------|-------------|
| **Agent Mail** | Message routing, file reservations, pre-commit guard |
| **BV** | Work distribution, triage, assignment strategies |
| **CASS** | Search past sessions via robot mode |
| **CM** | Procedural memory for agent handoffs |
| **DCG** | Safety system integration |
| **UBS** | Auto-scanning on file changes |
