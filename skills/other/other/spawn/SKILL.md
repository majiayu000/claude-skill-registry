---
name: spawn
description: "Skills for spawning external processes - AI coding agents and generic CLI commands in new terminal windows. Parent skill category for agent and terminal spawning."
type: category
---

# Spawn Skills

This directory contains skills for spawning external processes in new terminal windows.

## Overview

Spawn skills enable Claude Code to launch external processes:
- **AI coding agents** (Claude, Codex, Gemini, Cursor, OpenCode, Copilot)
- **Generic CLI commands** (ffmpeg, curl, python, npm, etc.)

Both use the `fork_terminal` utility to create isolated terminal sessions.

## Child Skills

| Skill | Description | Use Case |
|-------|-------------|----------|
| [agent](./agent/SKILL.md) | Spawn AI coding agents | Multi-provider orchestration |
| [terminal](./terminal/SKILL.md) | Spawn generic CLI commands | Non-AI command execution |

## When to Use

### Use spawn:agent when:
- Delegating tasks to external AI providers
- Need interactive CLI sessions with AI agents
- Browser-based authentication is required
- Real-time streaming output needed

### Use spawn:terminal when:
- Running non-AI CLI commands (ffmpeg, curl, etc.)
- Need interactive terminal for user input
- Long-running processes that shouldn't block Claude

### Use orchestration:native-invoke instead when:
- Automating multi-provider tasks
- Need parallel execution across providers
- Clean result collection is important
- No interactive/TTY requirements

## Core Utility

Both skills use the `fork_terminal` Python utility:

```python
# Located at: ./agent/fork_terminal.py
from fork_terminal import fork_terminal

# Basic usage
result = fork_terminal("command", capture=True)

# With logging
result = fork_terminal("command", log_to_file=True, log_agent_output=True)
```

## Quick Reference

```
spawn/
├── SKILL.md           # This file
├── agent/             # AI agent spawning
│   ├── SKILL.md
│   ├── cookbook/      # Per-agent cookbooks
│   │   ├── claude-code.md
│   │   ├── codex-cli.md
│   │   ├── gemini-cli.md
│   │   ├── cursor-cli.md
│   │   ├── opencode-cli.md
│   │   └── copilot-cli.md
│   └── prompts/       # Reusable prompt templates
└── terminal/          # Generic CLI spawning
    ├── SKILL.md
    └── cookbook/
        └── cli-command.md
```

## Related Skills

- **orchestration/native-invoke** - Task-based CLI invocation (preferred for automation)
- **multi-agent-orchestration** - Higher-level provider routing
- **model-discovery** - Current model names for providers

## See Also

- `.claude/ai-dev-kit/dev-tools/orchestration/providers/` - Shell scripts for each provider
- `/ai-dev-kit:delegate` - Command for manual delegation
