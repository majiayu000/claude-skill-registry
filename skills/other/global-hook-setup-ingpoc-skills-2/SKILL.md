---
name: global-hook-setup
description: "Use when setting up global hooks for Claude Code enforcement. Load when ~/.claude/hooks/ is missing or incomplete, or when explicitly requested. Installs 7 project-agnostic hooks (state transitions, git hygiene, outcome tracking). Run once per machine."
keywords: hooks, global, setup, enforcement, state-machine, git
---

# Global Hook Setup

One-time setup for global Claude Code hooks. These hooks work across all projects.

## Purpose

Installs 8 project-agnostic hooks that enforce DESIGN-v2 determinism:

- State machine integrity
- Git hygiene
- Learning layer (outcome tracking)
- Session checkpoints

## When to Use

| Situation | Action |
| --------- | ------ |
| First time setup | Run full setup |
| ~/.claude/hooks/ missing | Run full setup |
| After updating hooks | Re-run setup |
| Manual verification | Run verify script |

## Quick Check

```bash
# Check if global hooks exist
ls ~/.claude/hooks/
```

Expected output:

```text
verify-state-transition.py
require-commit-before-tested.py
require-outcome-update.py
link-feature-to-trace.py
markdownlint-fix.sh
remind-decision-trace.sh
session-end.sh
feature-commit.sh
```

## Setup Steps

### 1. Install Hooks

```bash
~/.claude/skills/global-hook-setup/scripts/setup-global-hooks.sh
```

This creates:

- `~/.claude/hooks/` directory
- 8 hook files
- Executable permissions (chmod +x)

### 2. Verify Installation

```bash
~/.claude/skills/global-hook-setup/scripts/verify-global-hooks.sh
```

## Hooks Installed

| Hook | Event | Purpose | Blocks? |
| ---- | ----- | ------- | ------- |
| `verify-state-transition.py` | PreToolUse | Valid state transitions only | Yes |
| `require-commit-before-tested.py` | PreToolUse | Git clean before tested | Yes |
| `require-outcome-update.py` | PreToolUse | Update trace outcome | Yes |
| `link-feature-to-trace.py` | PostToolUse | Auto-link features | No |
| `markdownlint-fix.sh` | PostToolUse | Auto-fix .md linting | No |
| `remind-decision-trace.sh` | SessionEnd | Remind to log decisions | No |
| `session-end.sh` | SessionEnd | Checkpoint commit | No |
| `feature-commit.sh` | CLI utility | Feature commit helper | N/A |

**Note**: `feature-commit.sh` is a CLI utility (not a hook). Use: `~/.claude/hooks/feature-commit.sh <feature-id> [message]`

## Settings.json Configuration

Setup script configures `~/.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {"type": "command", "command": "python3 ~/.claude/hooks/verify-state-transition.py"},
          {"type": "command", "command": "python3 ~/.claude/hooks/require-commit-before-tested.py"},
          {"type": "command", "command": "python3 ~/.claude/hooks/require-outcome-update.py"}
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {"type": "command", "command": "python3 ~/.claude/hooks/link-feature-to-trace.py"},
          {"type": "command", "command": "/bin/bash ~/.claude/hooks/markdownlint-fix.sh"}
        ]
      }
    ],
    "SessionEnd": [
      {
        "hooks": [
          {"type": "command", "command": "/bin/bash ~/.claude/hooks/session-end.sh"},
          {"type": "command", "command": "/bin/bash ~/.claude/hooks/remind-decision-trace.sh"}
        ]
      }
    ]
  }
}
```

## Exit Criteria (Code Verified)

```bash
# Directory exists
[ -d ~/.claude/hooks ]

# All hooks exist and executable
[ -x ~/.claude/hooks/verify-state-transition.py ]
[ -x ~/.claude/hooks/require-commit-before-tested.py ]
[ -x ~/.claude/hooks/require-outcome-update.py ]
[ -x ~/.claude/hooks/link-feature-to-trace.py ]
[ -x ~/.claude/hooks/markdownlint-fix.sh ]
[ -x ~/.claude/hooks/remind-decision-trace.sh ]
[ -x ~/.claude/hooks/session-end.sh ]
[ -x ~/.claude/hooks/feature-commit.sh ]

# Verify script passes
~/.claude/skills/global-hook-setup/scripts/verify-global-hooks.sh
```

## Scripts

| Script | Purpose |
| ------ | ------- |
| `setup-global-hooks.sh` | Main setup (install + configure + validate) |
| `configure-settings.py` | Configure settings.json with hook entries |
| `validate-settings.py` | Validate hooks configured in settings.json |
| `verify-global-hooks.sh` | Verify hook files exist |
| `install-hooks.sh` | Copy from templates |

## Troubleshooting

| Problem | Solution |
| ------- | -------- |
| Hooks not found | Re-run setup script |
| Permission denied | Run: `chmod +x ~/.claude/hooks/*` |
| Verification fails | Check hook syntax, ensure python3 available |
| Already exists | Setup is idempotent, safe to re-run |

## Next Steps

After global hooks: Set up project-specific hooks with `project-hook-setup` skill.
