---
name: hook-development
description: "[Utility] Guide for developing Claude Code hooks - shell commands that execute automatically in response to tool calls and notifications. Use this when users want to create, debug, or optimize hooks for automating workflows like linting, formatting, notifications, or custom validations. Supports PreToolUse, PostToolUse, Stop, SubagentStop, SessionStart, SessionEnd, UserPromptSubmit, PreCompact, Notification events."
---

# Hook Development for Claude Code Plugins

## Overview

Hooks are event-driven automation scripts that execute in response to Claude Code events. Use hooks to validate operations, enforce policies, add context, and integrate external tools into workflows.

## Hook Types

### Prompt-Based Hooks (Recommended)
Use LLM-driven decision making for context-aware validation.

### Command Hooks
Execute bash commands for deterministic checks.

## Hook Events

| Event | When | Use For |
|-------|------|---------|
| PreToolUse | Before tool | Validation, modification |
| PostToolUse | After tool | Feedback, logging |
| UserPromptSubmit | User input | Context, validation |
| Stop | Agent stopping | Completeness check |
| SubagentStop | Subagent done | Task validation |
| SessionStart | Session begins | Context loading |
| SessionEnd | Session ends | Cleanup, logging |
| PreCompact | Before compact | Preserve context |
| Notification | User notified | Logging, reactions |

## Environment Variables

- `$CLAUDE_PROJECT_DIR` - Project root path
- `$CLAUDE_PLUGIN_ROOT` - Plugin directory
- `$CLAUDE_ENV_FILE` - SessionStart only: persist env vars here

## Best Practices

- Use prompt-based hooks for complex logic
- Use ${CLAUDE_PLUGIN_ROOT} for portability
- Validate all inputs in command hooks
- Set appropriate timeouts