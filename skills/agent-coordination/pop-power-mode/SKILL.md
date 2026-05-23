---
name: power-mode
description: "Multi-agent orchestration system using Claude Code's native background agents (2.0.64+) for true parallel collaboration. Enables shared context, sync barriers between phases, and coordinator oversight. Use for complex tasks benefiting from parallel execution (epics, large refactors, multi-phase features). Do NOT use for simple tasks or sequential workflows - the coordination overhead isn't justified."
hooks:
  Stop:
    - script: "${CLAUDE_PLUGIN_ROOT}/../../shared-py/hooks/save-power-mode-report.py"
      once: true
---

# Pop Power Mode

Multi-agent orchestration using Claude Code's **native background agents** for true parallel collaboration.

**Core principle:** Agents work in parallel via `run_in_background: true`, share discoveries via file, and coordinate through sync barriers.

## Architecture: Native Async (Claude Code 2.0.64+)

```
┌─────────────────────────────────────────────────────────────────┐
│                   NATIVE ASYNC POWER MODE                        │
├─────────────────────────────────────────────────────────────────┤
│   ┌───────────┐  ┌───────────┐  ┌───────────┐                  │
│   │  Agent 1  │  │  Agent 2  │  │  Agent 3  │                  │
│   │background │  │background │  │background │                  │
│   └─────┬─────┘  └─────┬─────┘  └─────┬─────┘                  │
│         └──────────────┼──────────────┘                         │
│                        │                                        │
│                ┌───────▼───────┐                               │
│                │  Main Agent   │  ← Coordinator (TaskOutput)   │
│                │  (Polling)    │                               │
│                └───────────────┘                               │
├─────────────────────────────────────────────────────────────────┤
│ Requirements: Claude Code 2.0.64+ (no external dependencies)   │
│ Setup: Zero config - just run /popkit:power start              │
└─────────────────────────────────────────────────────────────────┘
```

## Tier Comparison

| Feature            | Free       | Premium ($9/mo)  | Pro ($29/mo)     |
| ------------------ | ---------- | ---------------- | ---------------- |
| Mode               | File-based | Native Async     | Native Async     |
| Max Agents         | 2          | 5                | 10               |
| Parallel Execution | Sequential | ✅ True parallel | ✅ True parallel |
| Sync Barriers      | Basic      | ✅ Phase-aware   | ✅ Phase-aware   |
| Insight Sharing    | Basic      | ✅ Full          | ✅ Full          |
| Redis Fallback     | ❌         | ❌               | ✅ Optional      |

### Free Tier: File-Based Mode

Free tier users get file-based coordination:

- Works with 2 agents (sequential)
- Shared context via `.claude/popkit/insights.json`
- Good for learning Power Mode concepts
- Zero setup required

### Premium Tier: Native Async Mode

Premium users unlock native async capabilities:

- Up to 5 agents working in **true parallel**
- Uses Claude Code's `Task(run_in_background: true)` API
- Main agent polls via `TaskOutput(block: false)`
- Phase-aware sync barriers
- Full insight sharing

### Pro Tier: Full Power

Pro users get maximum capabilities:

- Up to 10 parallel agents
- Optional Redis fallback for high-volume scenarios
- Team coordination features

## Overview

**Inspired by:**

- ZigBee/Z-Wave mesh networks (failover, redundancy)
- DeepMind's objective-driven agents (constrained exploration)
- Node-RED (flow-based coordination)

**When to use:**

- Complex tasks requiring multiple specialized agents
- Tasks that benefit from parallel exploration
- When agents need to share discoveries in real-time
- Large implementations with distinct subtasks

**When NOT to use:**

- Simple, single-agent tasks
- Tasks requiring tight sequential dependency
- When Redis is unavailable
- Quick fixes or small changes

## Prerequisites

### Native Async Mode (Default - Zero Config)

- Claude Code 2.0.64 or later
- Premium or Pro tier
- **No additional setup required!**

## Activation

### Method 1: Command (Recommended)

```
/popkit:power start "Build user authentication with tests and docs"
```

### Method 2: Issue-Driven

```
/popkit:dev work #45 -p
```

### Method 3: Auto-Detection

```
# Power Mode auto-enables for issues labeled "epic" or "power-mode"
/popkit:dev work #45
```

## How It Works

### 1. Define Objective

Power mode requires a clear objective with:

- **Description**: What we're building
- **Success criteria**: How we know we're done
- **Phases**: Ordered stages of work
- **Boundaries**: What agents can't do

```python
Objective:
  description: "Build user authentication"
  success_criteria:
    - "Login endpoint works"
    - "Tests pass"
    - "Documentation updated"
  phases: [explore, design, implement, test, document]
  boundaries:
    - file_patterns: ["src/auth/**", "tests/auth/**"]
    - restricted_tools: []
```

### 2. Mode Selection

The mode selector automatically chooses the best mode:

1. **Native Async** (if Claude Code 2.0.64+) → 5-10 parallel agents (recommended)
2. **File-based** (always available) → 2 sequential agents (fallback)

### 3. Coordinator Starts

**Native Async Mode:**

- Main agent becomes coordinator
- Spawns background agents via `Task(run_in_background: true)`
- Polls progress via `TaskOutput(block: false)`
- Manages phase transitions

### 4. Agents Work in Parallel

Each background agent:

- Receives its subtask and phase
- Works independently
- Shares insights via `.claude/popkit/insights.json`
- Returns results when complete

### 5. Insight Sharing

Agents share discoveries via JSON file:

```json
{
  "insights": [
    {
      "agent": "code-explorer",
      "content": "Found existing User model at src/models",
      "tags": ["model", "database"],
      "phase": "explore"
    }
  ]
}
```

### 6. Sync Barriers

Between phases:

- Coordinator waits for all `TaskOutput` to complete
- Aggregates results from phase
- Spawns next batch of agents
- Process continues until all phases complete

### 7. Completion

When objective met:

- Coordinator aggregates all results
- Patterns saved for future
- State cleared from `.claude/popkit/power-state.json`

## Communication Channels

Uses file-based communication:
| File | Purpose |
|------|---------|
| `.claude/popkit/insights.json` | Shared discoveries |
| `.claude/popkit/power-state.json` | Session state |

## Guardrails

**Automatic protections:**

- Protected paths (.env, secrets, .git)
- Human-required actions (deploy, delete prod data)
- Drift detection (working outside scope)
- Unconventional approach detection

**Human escalation triggers:**

- Modifying security configuration
- Pushing to main/production
- Accessing credentials
- Bulk file deletions
- Actions that might be "cheating"

## Example Workflow

```
User: /popkit:power-mode "Build a REST API with user authentication"

[Coordinator starts, creates objective]

Phase 1: EXPLORE (parallel)
├── code-explorer → Analyzes existing codebase
├── researcher → Researches auth best practices
└── architect → Reviews project structure

[Insights shared via Redis]
explorer → "Found existing User model at src/models"
researcher → "JWT recommended for stateless auth"
architect → "Routes pattern: src/routes/{feature}/"

[SYNC BARRIER - wait for all]

Phase 2: DESIGN (coordinator routes insights)
└── code-architect → Designs auth system
    (receives all Phase 1 insights automatically)

[SYNC BARRIER]

Phase 3: IMPLEMENT (parallel with check-ins)
├── rapid-prototyper → Implements endpoints
│   ├── Check-in 1: "Created login route"
│   ├── Check-in 2: "Added JWT generation"
│   └── Check-in 3: "Need: User model location"
│       ← Receives: "src/models/user.ts" from explorer
│
├── test-writer → Writes tests in parallel
│   └── Check-in: "Testing login endpoint"
│
└── docs-maintainer → Updates documentation
    └── Check-in: "Documenting API endpoints"

[SYNC BARRIER]

Phase 4: REVIEW
└── code-reviewer → Reviews all changes
    (receives aggregated results from all agents)

[Complete - results aggregated, patterns saved]
```

## Configuration

Edit `power-mode/config.json`:

```json
{
  "intervals": {
    "checkin_every_n_tools": 5,
    "heartbeat_seconds": 15
  },
  "limits": {
    "max_parallel_agents": 6,
    "max_runtime_minutes": 30
  },
  "guardrails": {
    "protected_paths": [".env*", "**/secrets/**"],
    "drift_detection": { "enabled": true }
  }
}
```

## Deactivation

```bash
# Use command (recommended)
/popkit:power stop

# Or clear state file
rm .claude/popkit/power-state.json
```

## Troubleshooting

### Native Async Mode

**Claude Code version too old:**

- Update Claude Code to 2.0.64+
- Check version: `claude --version`
- Power Mode will fall back to file mode

**Background agents not spawning:**

- Verify you have Premium/Pro tier
- Check `.claude/popkit/power-state.json` for errors
- Free tier is limited to file-based mode

**Insights not sharing:**

- Check `.claude/popkit/insights.json` exists
- Verify file permissions

### General

**Drift alerts:**

- Agent working outside scope boundaries
- Update boundaries or reassign task

## Integration

**Works with:**

- All popkit agents (they gain check-in capability)
- Existing skills (run within power mode context)
- Output styles (check-ins use power-mode-checkin format)

**Coordinator agent:**

- `power-coordinator` - Can be invoked as coordinator

**Related skills:**

- `pop-subagent-dev` - Single-session alternative
- `pop-executing-plans` - Parallel session alternative
