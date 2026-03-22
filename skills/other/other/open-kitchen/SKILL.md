---
name: open-kitchen
description: Open the AutoSkillit kitchen — reveals all kitchen MCP tools for this session. Human-only entry point.
disable-model-invocation: true
---

# Open Kitchen

Call the `open_kitchen` MCP tool to reveal all 24 kitchen tools for this session.

## Critical Constraints

**NEVER:**
- Skip calling `open_kitchen` and assume the kitchen is already open
- Call this skill from a headless or automated session (it is human-only)

**ALWAYS:**
- Call `open_kitchen` with no arguments
- Confirm to the user that kitchen tools are now available

## Steps

1. Call `open_kitchen` with no arguments.
2. Confirm the kitchen is open by displaying the list of newly available tools.
3. Inform the user that all kitchen tools are now available for this session.

The kitchen state is session-scoped. Each new Claude Code session starts with kitchen tools hidden. Use `/autoskillit:open-kitchen` to reveal them at the start of each session.
