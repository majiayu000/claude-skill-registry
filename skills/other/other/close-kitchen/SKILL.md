---
name: close-kitchen
description: Close the AutoSkillit kitchen — hides kitchen MCP tools for this session.
disable-model-invocation: true
---

# Close Kitchen

Call the `close_kitchen` MCP tool to hide all 24 kitchen tools for this session.

## Critical Constraints

**NEVER:**
- Skip calling `close_kitchen` and assume the kitchen is already closed
- Call this skill from a headless or automated session (it is human-only)

**ALWAYS:**
- Call `close_kitchen` with no arguments
- Confirm to the user that kitchen tools are now hidden

## Steps

1. Call `close_kitchen` with no arguments.
2. Confirm the kitchen is closed.
3. Inform the user that kitchen tools are now hidden for this session.

Use `/autoskillit:open-kitchen` to reveal kitchen tools again when needed.
