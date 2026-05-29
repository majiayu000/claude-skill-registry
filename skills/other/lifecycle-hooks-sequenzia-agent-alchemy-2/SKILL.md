---
name: lifecycle-hooks
description: Behavioral rules and lifecycle event handlers for the core-tools package. Defines automated behaviors that trigger at specific points in the agent workflow. (converted from hooks)
dependencies: []
---

# Lifecycle Hooks

This skill defines behavioral rules that were originally enforced by platform lifecycle hooks. These rules describe automated behaviors that trigger at specific points in the agent workflow.

---

## On before_action

**Trigger:** Fires before the agent executes any action (file write, shell command, etc.)
**Applies when:** Action matches `Write|Edit|Bash`

This rule auto-approves file operations targeting deep-analysis session and cache directories. It prevents permission prompts from interrupting autonomous exploration workflows.

The implementation logic is in **references/auto-approve-da-session.sh**. This script:
- Reads action context from stdin (JSON with action type and parameters)
- Checks if the target file path or command references session directories (`.agents/sessions/__da_live__/`, `.agents/sessions/exploration-cache/`, `.agents/sessions/da-*/`)
- If matched, approves the action automatically
- If not matched, passes through to normal permission flow (no opinion)

## Integration Notes

**What this component does:** Defines automated behavioral rules that were originally enforced by platform lifecycle hooks.

**Origin:** Converted from 1 lifecycle hook (PreToolUse/before_action)

**Capabilities needed:**
- Event/lifecycle hook system (if the target harness supports one)
- Alternatively, implement as middleware, conditional checks, or manual review steps

**Adaptation guidance:**
- This behavior was originally enforced automatically by the platform. In the target harness, it may need to be implemented as middleware, event handlers, or manual review steps.
- The command hook script in `references/` can be executed directly if the harness supports shell-based hooks.
- The auto-approval targets session file operations to enable uninterrupted deep analysis workflows.
