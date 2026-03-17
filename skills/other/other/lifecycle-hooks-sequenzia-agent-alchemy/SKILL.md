---
name: lifecycle-hooks
description: "Behavioral rules and lifecycle event handlers for the core-tools package. Defines automated behaviors that trigger at specific points in the agent workflow. (converted from hooks)"
dependencies: []
---

# Lifecycle Hooks

This skill defines automated behaviors that trigger at specific points in the agent workflow for the core-tools package.

---

## On before_action

**Trigger:** Fires before the agent executes any action (file write, shell command, etc.)
**Applies when:** Action matches `Write|Edit|Bash`

Auto-approve file operations targeting deep-analysis session and cache directories. This allows the deep-analysis workflow to write session files (checkpoints, findings, cache) without requiring manual approval for each operation.

The implementation logic is in **references/auto-approve-da-session.sh**. This script:
- Checks if the file operation targets `.agents/sessions/__da_live__/`, `.agents/sessions/exploration-cache/`, or `.agents/sessions/da-*/` directories
- Auto-approves matching operations to enable autonomous session management
- Passes through all other operations to normal permission flow
- Expected input: Action context as JSON on stdin (with `tool_name` and `tool_input` fields)
- Expected output: JSON permission decision or empty (no opinion)

---

## Integration Notes

This skill documents lifecycle automation that was originally implemented as platform-specific hooks. When integrating with a specific agent platform:

- **Hook registration:** Map the `before_action` trigger to the platform's pre-execution hook mechanism (e.g., `PreToolUse` in Claude Code, pre-action middleware in other platforms)
- **Matcher pattern:** The trigger should only fire for file write, file edit, and shell command actions
- **Timeout:** The approval script should complete within 5 seconds
- **Fail-safe behavior:** If the script fails or times out, fall through to normal permission flow (never block the agent)
- **Path patterns:** The script matches against `.agents/sessions/` subdirectories specific to the deep-analysis workflow
