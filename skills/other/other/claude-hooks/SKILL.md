---
name: claude-hooks
description: Claude Code hooks configuration specialist. Use when creating hooks for
  tool validation, logging, notifications, or custom automation in Claude Code.
author: Joseph OBrien
status: unpublished
updated: '2025-12-23'
version: 1.0.1
tag: skill
type: skill
---

# Claude Hooks Skill

Creates and configures hooks for Claude Code to automate workflows and extend functionality.

## What This Skill Does

- Creates PreToolUse validation hooks
- Sets up PostToolUse logging/cleanup
- Configures notification hooks
- Implements custom automation
- Documents hook patterns

## When to Use

- Tool execution validation
- Audit logging
- Custom notifications
- Workflow automation
- Security controls

## Reference Files

- `references/CLAUDE_HOOK.template.md` - Hook configuration examples and patterns

## Hook Events

| Event | Trigger | Use Case |
|-------|---------|----------|
| PreToolUse | Before tool executes | Validation, blocking |
| PostToolUse | After tool completes | Logging, cleanup |
| Notification | Claude sends notification | Alerts |
| Stop | Claude stops | Final reports |

## Configuration Location

Hooks are configured in `~/.claude/settings.json` under the `hooks` key.

## Best Practices

- Keep hooks fast (< 1 second)
- Handle errors gracefully
- Use specific matchers
- Test hooks independently
- Avoid verbose output
