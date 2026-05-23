---
name: lifecycle-hooks
description: >-
  Behavioral rules and lifecycle event handlers for the core-tools package.
  Defines automated behaviors that trigger at specific points in the agent workflow.
  (converted from hooks)
dependencies: []
---

# Lifecycle Hooks

## On before_action

**Trigger:** Fires before the agent executes any action
**Applies when:** Action is a file write, file edit, or shell command

Auto-approve file operations targeting deep-analysis session and cache directories.
This allows the deep-analysis workflow to write session files without requiring user approval for each operation.

The implementation logic is in **references/auto-approve-da-session.sh**. This script:
- Reads action context from stdin as JSON
- Checks if the target path matches `.agents/sessions/__da_live__/`, `.agents/sessions/exploration-cache/`, or `.agents/sessions/da-*/`
- For matching paths: approves the operation automatically
- For non-matching paths: passes through to normal permission flow

## Integration Notes

**What this component does:** Defines automated behavioral rules that were originally enforced by platform lifecycle hooks.

**Origin:** Converted from 1 lifecycle hook (PreToolUse)

**Capabilities needed:**
- Event/lifecycle hook system (if the target harness supports one)
- Alternatively, implement as middleware, conditional checks, or manual review steps

**Adaptation guidance:**
- This behavior was originally enforced automatically by the platform. In the target harness, it may need to be implemented as middleware, event handlers, or manual review steps.
- The script in `references/` can be executed directly if the harness supports shell-based hooks.
